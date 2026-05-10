# -*- coding: utf-8 -*-
"""
P1) Doctor step (fastest win)

Validates modular source fragments before generating compile/module_*.py files.

Hard errors (stop build):
- Missing expected export assignment in any fragment file:
    SCRIPTS / MENUS / DIALOGS / SIMPLE_TRIGGERS / PRESENTATIONS / MISSION_TEMPLATES
- Duplicate top-level IDs for: scripts, menus, presentations, mission templates
- Dialogs/triggers order file problems:
    - missing order file
    - missing files listed in order file
    - duplicate entries in order file
    - fragment files not listed (STRICT)

Warnings (build continues):
- ZA order file does not cover all ZA fragments (they will be appended)

Warnings (build continues; QoL / harder-to-debug issues):
- Potential *global variable collisions* across presentations / mission templates.
  (e.g. "$g_presentation_obj_1" reused across many presentations)
  These aren't necessarily wrong, but they are a common source of UI state bugs.

Outputs:
- Writes docs/reports/doctor_report.txt (overwritten each run)
- Prints a short summary to console

Additional checks (v81+):
- Missing "# COST:" headers for ZY helper scripts (warning by default; can be strict)
- Forbidden slot-math string patterns like ":slot" + 1 (error by default; can be disabled)
- Non-ASCII characters in build scripts / .bat files (warning by default; can be strict)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
for _import_path in (ROOT, ROOT / "compile", ROOT / "compile" / "headers", ROOT / "compile" / "ids"):
    if str(_import_path) not in sys.path:
        sys.path.insert(0, str(_import_path))

SRC_SCRIPTS = ROOT / "src" / "scripts"
SRC_MENUS = ROOT / "src" / "menus"
SRC_DIALOGS = ROOT / "src" / "dialogs"
SRC_TRIGGERS = ROOT / "src" / "triggers"
SRC_PRESENTATIONS = ROOT / "src" / "presentations"
SRC_MISSION_TEMPLATES = ROOT / "src" / "mission_templates"
SRC_CONSTANTS = ROOT / "src" / "constants"
SRC_QUESTS = ROOT / "src" / "quests"

SRC_ROOT = ROOT / "src"

# QoL allowlist: top-level folders under src/ that are allowed to contain .py files
# without being compiled into module_*.py output.
# (This lets you keep small helper/config python files in src/ without noise.)
_SRC_PY_ALLOWLIST = {
    "config",
    "lib",
    "shared",
    "_shared",
}

ORDER_DIALOGS = SRC_DIALOGS / "_order_dialogs.txt"
ORDER_TRIGGERS = SRC_TRIGGERS / "_order_simple_triggers.txt"
ORDER_MENUS = SRC_MENUS / "_order_game_menus.txt"
ORDER_PRESENTATIONS = SRC_PRESENTATIONS / "_order_presentations.txt"
ORDER_MISSION_TEMPLATES = SRC_MISSION_TEMPLATES / "_order_mission_templates.txt"
ORDER_CONSTANTS = SRC_CONSTANTS / "_order_constants.txt"
ORDER_ZA = SRC_SCRIPTS / "ZA_hardcoded_game_scripts" / "_order_za_scripts.txt"

DOCS_DIR = ROOT / "docs"
DOCS_EDIT = DOCS_DIR / "edit"
DOCS_REPORTS = DOCS_DIR / "reports"
REPORT_PATH = DOCS_REPORTS / "doctor_report.txt"
REPORT_JSON_PATH = DOCS_REPORTS / "doctor_report.json"

# Optional allowlist to suppress known/expected global-var collision warnings.
ALLOWLIST_GLOBALS_PATH = DOCS_EDIT / "doctor_allowlist_globals.txt"

# Optional allowlist to suppress known/expected duplicate top-level IDs.
ALLOWLIST_DUPLICATE_IDS_PATH = DOCS_EDIT / "doctor_allowlist_duplicate_ids.txt"

# Optional allowlists for additional Doctor checks
ALLOWLIST_COST_PATH = DOCS_EDIT / "doctor_allowlist_missing_cost.txt"
ALLOWLIST_NONASCII_PATH = DOCS_EDIT / "doctor_allowlist_non_ascii.txt"
ALLOWLIST_FORBIDDEN_PATTERNS_PATH = DOCS_EDIT / "doctor_allowlist_forbidden_patterns.txt"
ALLOWLIST_STUBS_PATH = DOCS_EDIT / "doctor_allowlist_stubs.txt"
ALLOWLIST_DIALOG_DUPES_PATH = DOCS_EDIT / "doctor_allowlist_dialog_duplicates.txt"
BASELINE_FINDINGS_PATH = DOCS_EDIT / "doctor_baseline_findings.txt"

# Detect actual exports (assignment), not just a mention in comments.
_EXPORT_RE = {
    "SCRIPTS": re.compile(r"(?m)^\s*SCRIPTS\s*=\s*\["),
    "MENUS": re.compile(r"(?m)^\s*MENUS\s*=\s*\["),
    "DIALOGS": re.compile(r"(?m)^\s*DIALOGS\s*=\s*\["),
    "SIMPLE_TRIGGERS": re.compile(r"(?m)^\s*SIMPLE_TRIGGERS\s*=\s*\["),
    "PRESENTATIONS": re.compile(r"(?m)^\s*PRESENTATIONS\s*=\s*\["),
    "MISSION_TEMPLATES": re.compile(r"(?m)^\s*MISSION_TEMPLATES\s*=\s*\["),
}

# Quoted global vars like "$g_foo" or '$g_foo'
_GLOBAL_VAR_RE = re.compile(r"['\"](\$g_[A-Za-z0-9_]+)['\"]", re.IGNORECASE)

# ID-like references that commonly break during modularization/renames.
# These are usually referenced as *string literals* in operations like (call_script, "script_x").
_REF_STRING_PREFIXES = ("script_", "mnu_", "prsnt_", "mt_")

# These are usually referenced as *identifiers* (constants) like trp_player, itm_sword.
_REF_IDENT_PREFIXES = ("trp_", "itm_", "fac_", "p_", "pt_", "qst_", "scn_")

# Forbidden pattern: string-literal slot symbols accidentally used in arithmetic like ":pool_begin" + 1.
# This usually indicates a bad copy/paste from pseudo-code and will crash the build.
_FORBIDDEN_SLOT_MATH_RE = re.compile(r"[\"']:[A-Za-z0-9_]+[\"']\s*\+\s*\d+")

# Forbidden pattern: a this_or_next conditional chain whose next meaningful line is an action.
# In Warband's operation block syntax, this usually means the final condition was accidentally
# prefixed with this_or_next, causing the following action to be skipped/triggered unpredictably.
_THIS_OR_NEXT_RE = re.compile(r"\bthis_or_next\|")
_ACTION_AFTER_THIS_OR_NEXT_RE = re.compile(
    r"^\s*\(\s*(?:"
    r"assign|call_script|val_[A-Za-z0-9_]+|str_store_[A-Za-z0-9_]+|display_message|"
    r"troop_(?:set|add|remove)|party_(?:set|add|remove|clear)|faction_set|quest_set|"
    r"remove_party|spawn_around_party"
    r")\b"
)

# ZY helper scripts are expected to carry COST annotations in their headers.
_COST_HEADER_RE = re.compile(r"(?m)^\s*#\s*COST\s*:\s*")
_STUB_MARKER_RE = re.compile(r"(?i)\b(?:stub|placeholder|not implemented|todo|tbd|wip)\b")

# M&B 1.011 and Original SoD both have a handful of engine-facing entries whose
# order matters. The generated module files are the real build input, so Doctor
# validates these after src fragments have been assembled into compile/.
MB1011_HARDCODED_MENU_NAMES = [
    "start_game_1",
    "start_phase_2",
]

MB1011_HARDCODED_SCRIPT_NAMES = [
    "game_start",
    "game_event_party_encounter",
    "game_event_simulate_battle",
    "game_event_battle_end",
    "game_get_item_buy_price_factor",
    "game_get_item_sell_price_factor",
    "game_event_buy_item",
    "game_event_sell_item",
    "game_get_troop_wage",
    "game_get_total_wage",
    "game_get_join_cost",
    "game_get_prisoner_price",
    "game_check_prisoner_can_be_sold",
    "game_event_detect_party",
    "game_event_undetect_party",
    "game_get_statistics_line",
    "game_get_date_text",
    "game_get_money_text",
    "game_get_party_companion_limit",
    "game_reset_player_party_name",
    "game_get_party_prisoner_limit",
    "game_get_item_extra_text",
    "game_on_disembark",
    "game_context_menu_get_buttons",
    "game_event_context_menu_button_clicked",
    "game_get_skill_modifier_for_troop",
]

MB1011_HARDCODED_SKILL_NAMES = [
    "trade",
    "leadership",
    "prisoner_management",
    "reserved_1",
    "reserved_2",
    "reserved_3",
    "reserved_4",
    "persuasion",
    "engineer",
    "first_aid",
    "surgery",
    "wound_treatment",
    "inventory_management",
    "spotting",
    "pathfinding",
    "tactics",
    "tracking",
    "trainer",
    "reserved_5",
    "reserved_6",
    "reserved_7",
    "reserved_8",
    "looting",
    "horse_archery",
    "riding",
    "athletics",
    "shield",
    "weapon_master",
    "reserved_9",
    "reserved_10",
    "reserved_11",
    "reserved_12",
    "reserved_13",
    "power_draw",
    "power_throw",
    "power_strike",
    "ironflesh",
    "reserved_14",
    "reserved_15",
    "reserved_16",
    "reserved_17",
    "reserved_18",
]

MB1011_HARDCODED_ITEM_CODES_H_NAMES = [
    "no_item",
    "horse_meat",
    "practice_sword",
    "heavy_practice_sword",
    "practice_axe",
    "arena_axe",
    "arena_sword",
    "arena_sword_two_handed",
    "arena_lance",
    "practice_staff",
    "practice_lance",
    "practice_shield",
    "practice_bow",
    "practice_crossbow",
    "practice_javelin",
    "practice_throwing_daggers",
    "practice_throwing_daggers_100_amount",
    "practice_horse",
    "practice_arrows",
    "practice_bolts",
    "practice_arrows_10_amount",
    "practice_arrows_100_amount",
    "practice_bolts_9_amount",
    "practice_boots",
    "red_tourney_armor",
    "blue_tourney_armor",
    "green_tourney_armor",
    "gold_tourney_armor",
    "red_tourney_helmet",
    "blue_tourney_helmet",
    "green_tourney_helmet",
    "gold_tourney_helmet",
    "arena_shield_red",
    "arena_shield_blue",
    "arena_shield_green",
    "arena_shield_yellow",
    "arena_armor_white",
    "arena_armor_red",
    "arena_armor_blue",
    "arena_armor_green",
    "arena_armor_yellow",
    "arena_tunic_white",
    "arena_tunic_red",
    "arena_tunic_blue",
    "arena_tunic_green",
    "arena_tunic_yellow",
    "arena_helmet_red",
    "arena_helmet_blue",
    "arena_helmet_green",
    "arena_helmet_yellow",
    "steppe_helmet_white",
    "steppe_helmet_red",
    "steppe_helmet_blue",
    "steppe_helmet_green",
    "steppe_helmet_yellow",
    "tourney_helm_white",
    "tourney_helm_red",
    "tourney_helm_blue",
    "tourney_helm_green",
    "tourney_helm_yellow",
    "book_tactics",
    "book_persuasion",
    "book_leadership",
    "book_intelligence",
    "book_trade",
    "book_weapon_mastery",
    "book_engineering",
    "book_wound_treatment_reference",
    "book_training_reference",
    "book_surgery_reference",
    "smoked_fish",
    "dried_meat",
    "cattle_meat",
    "pork",
    "bread",
    "apples",
    "cheese",
    "chicken",
    "honey",
    "sausages",
    "cabbages",
    "butter",
    "wine",
    "ale",
    "spice",
    "salt",
    "grain",
    "flour",
    "iron",
    "oil",
    "pottery",
    "linen",
    "furs",
    "wool",
    "velvet",
    "tools",
]

MB1011_SPECIAL_DIALOG_STATES = [
    "start",
    "party_relieved",
    "prisoner_liberated",
    "enemy_defeated",
    "event_triggered",
    "close_window",
]

MB1011_NATIVE_RANGE_CONTRACTS = [
    ("kingdoms", "kingdoms_begin", "kingdoms_end", ROOT / "compile" / "ids" / "ID_factions.py"),
    ("kingdom heroes", "kingdom_heroes_begin", "kingdom_heroes_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("companions", "companions_begin", "companions_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("soldiers", "soldiers_begin", "soldiers_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("towns", "towns_begin", "towns_end", ROOT / "compile" / "ids" / "ID_parties.py"),
    ("castles", "castles_begin", "castles_end", ROOT / "compile" / "ids" / "ID_parties.py"),
    ("villages", "villages_begin", "villages_end", ROOT / "compile" / "ids" / "ID_parties.py"),
    ("centers", "centers_begin", "centers_end", ROOT / "compile" / "ids" / "ID_parties.py"),
    ("trade goods", "trade_goods_begin", "trade_goods_end", ROOT / "compile" / "ids" / "ID_items.py"),
    ("food", "food_begin", "food_end", ROOT / "compile" / "ids" / "ID_items.py"),
    ("readable books", "readable_books_begin", "readable_books_end", ROOT / "compile" / "ids" / "ID_items.py"),
    ("reference books", "reference_books_begin", "reference_books_end", ROOT / "compile" / "ids" / "ID_items.py"),
    ("armor merchants", "armor_merchants_begin", "armor_merchants_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("weapon merchants", "weapon_merchants_begin", "weapon_merchants_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("tavernkeepers", "tavernkeepers_begin", "tavernkeepers_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("goods merchants", "goods_merchants_begin", "goods_merchants_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("horse merchants", "horse_merchants_begin", "horse_merchants_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("mayors", "mayors_begin", "mayors_end", ROOT / "compile" / "ids" / "ID_troops.py"),
    ("village elders", "village_elders_begin", "village_elders_end", ROOT / "compile" / "ids" / "ID_troops.py"),
]

MB1011_HARDCODED_CONTRACTS = [
    ("menus", ROOT / "compile" / "module_game_menus.py", ROOT / "compile" / "ids" / "ID_menus.py", "menu_", MB1011_HARDCODED_MENU_NAMES),
    ("skills", ROOT / "compile" / "module_skills.py", ROOT / "compile" / "ids" / "ID_skills.py", "skl_", MB1011_HARDCODED_SKILL_NAMES),
    ("parties", ROOT / "compile" / "module_parties.py", ROOT / "compile" / "ids" / "ID_parties.py", "p_", ["main_party", "temp_party", "camp_bandits"]),
    ("party templates", ROOT / "compile" / "module_party_templates.py", ROOT / "compile" / "ids" / "ID_party_templates.py", "pt_", ["none", "rescued_prisoners", "enemy", "hero_party"]),
    ("troops", ROOT / "compile" / "module_troops.py", ROOT / "compile" / "ids" / "ID_troops.py", "trp_", ["player", "temp_troop", "game", "unarmed_troop"]),
    ("factions", ROOT / "compile" / "module_factions.py", ROOT / "compile" / "ids" / "ID_factions.py", "fac_", ["no_faction", "commoners", "outlaws"]),
    ("strings", ROOT / "compile" / "module_strings.py", ROOT / "compile" / "ids" / "ID_strings.py", "str_", ["no_string", "empty_string", "yes", "no"]),
    ("mission templates", ROOT / "compile" / "module_mission_templates.py", ROOT / "compile" / "ids" / "ID_mission_templates.py", "mst_", ["town_default", "conversation_encounter"]),
    ("items", ROOT / "compile" / "module_items.py", ROOT / "compile" / "ids" / "ID_items.py", "itm_", MB1011_HARDCODED_ITEM_CODES_H_NAMES),
]

MB1011_ENGINE_CALLBACK_CONTRACTS = [
    ("scripts", ROOT / "compile" / "module_scripts.py", ROOT / "compile" / "ids" / "ID_scripts.py", "script_", MB1011_HARDCODED_SCRIPT_NAMES),
    ("presentations", ROOT / "compile" / "module_presentations.py", ROOT / "compile" / "ids" / "ID_presentations.py", "prsnt_", ["game_credits"]),
]

@dataclass
class DoctorResult:
    errors: List[str]
    warnings: List[str]
    summary: List[str]
    timings_ms: Dict[str, int]

def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def _parse_id_assignments(path: Path) -> Dict[str, int]:
    if not path.exists():
        return {}
    raw = _read_text(path)
    assignments: Dict[str, int] = {}
    for match in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*(-?\d+)\s*$", raw):
        assignments[match.group(1)] = int(match.group(2))
    return assignments

def _parse_module_tuple_names(path: Path) -> List[str]:
    if not path.exists():
        return []
    raw = _read_text(path)
    list_vars = {
        "module_game_menus.py": "game_menus",
        "module_presentations.py": "presentations",
        "module_scripts.py": "scripts",
        "module_skills.py": "skills",
        "module_parties.py": "parties",
        "module_troops.py": "troops",
        "module_factions.py": "factions",
        "module_strings.py": "strings",
        "module_mission_templates.py": "mission_templates",
        "module_party_templates.py": "party_templates",
        "module_items.py": "items",
        "module_animations.py": "animations",
        "module_skins.py": "skins",
    }
    list_var = list_vars.get(path.name)
    if list_var:
        try:
            return _iter_top_level_tuple_ids(_extract_list_block(raw, list_var))
        except Exception:
            pass

    if path.name in {"module_items.py", "module_troops.py"}:
        pattern = re.compile(r"(?m)^\s{0,2}\[\s*[\"']([A-Za-z0-9_]+)[\"']\s*,")
    elif path.name in {"module_game_menus.py", "module_presentations.py", "module_scripts.py"}:
        pattern = re.compile(r"(?m)^\s{0,4}\(\s*(?:\n\s*)?[\"']([A-Za-z0-9_]+)[\"']\s*,")
    elif path.name == "module_mission_templates.py":
        pattern = re.compile(r"(?m)^\s{0,2}\(\s*(?:\n\s*)?[\"']([A-Za-z0-9_]+)[\"']\s*,")
    else:
        pattern = re.compile(r"(?m)^\s{2}\(\s*(?:\n\s*)?[\"']([A-Za-z0-9_]+)[\"']\s*,")
    return [match.group(1) for match in pattern.finditer(raw)]

def _check_generated_sequence_contract(
    label: str,
    module_path: Path,
    id_path: Path,
    id_prefix: str,
    expected_names: List[str],
    errors: List[str],
    warnings: List[str],
    *,
    check_ids: bool = True,
) -> None:
    module_names = _parse_module_tuple_names(module_path)
    if not module_names:
        errors.append(f"[MB1011] Missing or unparsable generated {label} file: {module_path.relative_to(ROOT).as_posix()}")
    else:
        for expected_index, expected_name in enumerate(expected_names):
            actual_name = module_names[expected_index] if expected_index < len(module_names) else "<missing>"
            if actual_name != expected_name:
                errors.append(
                    "[MB1011] Generated "
                    f"{label} order mismatch at index {expected_index}: expected {expected_name}, got {actual_name}"
                )

    if not check_ids:
        return

    id_assignments = _parse_id_assignments(id_path)
    if not id_assignments:
        warnings.append(f"[MB1011] Generated ID file not available for {label}: {id_path.relative_to(ROOT).as_posix()}")
        return
    for expected_index, expected_name in enumerate(expected_names):
        id_name = f"{id_prefix}{expected_name}"
        actual_index = id_assignments.get(id_name)
        if actual_index != expected_index:
            errors.append(
                "[MB1011] Generated "
                f"{label} ID mismatch for {id_name}: expected {expected_index}, got {actual_index}"
            )

def _check_generated_presence_contract(
    label: str,
    module_path: Path,
    id_path: Path,
    id_prefix: str,
    expected_names: List[str],
    errors: List[str],
    warnings: List[str],
    *,
    check_ids: bool = True,
) -> None:
    module_names = set(_parse_module_tuple_names(module_path))
    if not module_names:
        errors.append(f"[MB1011] Missing or unparsable generated {label} file: {module_path.relative_to(ROOT).as_posix()}")
    id_assignments = _parse_id_assignments(id_path) if check_ids else {}
    if check_ids and not id_assignments:
        warnings.append(f"[MB1011] Generated ID file not available for {label}: {id_path.relative_to(ROOT).as_posix()}")

    for expected_name in expected_names:
        if module_names and expected_name not in module_names:
            errors.append(f"[MB1011] Engine callback missing from generated {label}: {expected_name}")
        if id_assignments and f"{id_prefix}{expected_name}" not in id_assignments:
            errors.append(f"[MB1011] Engine callback ID missing from generated {label}: {id_prefix}{expected_name}")

def _check_skin_contract(errors: List[str], warnings: List[str]) -> None:
    skin_names = _parse_module_tuple_names(ROOT / "compile" / "module_skins.py")
    if not skin_names:
        errors.append("[MB1011] Missing or unparsable generated skins file: compile/module_skins.py")
        return
    for expected_index, expected_name in enumerate(("man", "woman")):
        actual_name = skin_names[expected_index] if expected_index < len(skin_names) else "<missing>"
        if actual_name != expected_name:
            errors.append(
                "[MB1011] Generated skin order mismatch at index "
                f"{expected_index}: expected {expected_name}, got {actual_name}"
            )

def _check_dialog_state_contract(errors: List[str], warnings: List[str]) -> None:
    dialog_path = ROOT / "compile" / "module_dialogs.py"
    if not dialog_path.exists():
        errors.append("[MB1011] Missing generated dialogs file: compile/module_dialogs.py")
        return
    dialog_literals = {literal for literal, _line in _iter_string_literals_with_linenos(_read_text(dialog_path))}
    for state in MB1011_SPECIAL_DIALOG_STATES:
        if state not in dialog_literals:
            errors.append(f"[MB1011] Special dialog state missing from generated dialogs: {state}")

def _check_animation_id_contract(errors: List[str], warnings: List[str], *, check_ids: bool = True) -> None:
    if not check_ids:
        generated_names = _parse_module_tuple_names(ROOT / "compile" / "module_animations.py")
        reference_names = _parse_module_tuple_names(ROOT / "References" / "Vanilla_Module_System" / "module_animations.py")
        if not generated_names or not reference_names:
            warnings.append("[MB1011] Vanilla animation source baseline unavailable; animation source order could not be checked.")
            return
        for expected_index, expected_name in enumerate(reference_names):
            if re.match(r"unused_(?:human|horse)_anim_", expected_name):
                continue
            actual_name = generated_names[expected_index] if expected_index < len(generated_names) else "<missing>"
            if actual_name != expected_name:
                errors.append(
                    "[MB1011] Generated animation source order mismatch at index "
                    f"{expected_index}: expected {expected_name}, got {actual_name}"
                )
        return

    generated_ids = _parse_id_assignments(ROOT / "compile" / "ids" / "ID_animations.py")
    if not generated_ids:
        errors.append("[MB1011] Missing generated animation IDs: compile/ids/ID_animations.py")
        return
    reference_path = ROOT / "References" / "Vanilla_Module_System" / "ID_animations.py"
    reference_ids = _parse_id_assignments(reference_path)
    if not reference_ids:
        warnings.append("[MB1011] Vanilla animation ID baseline unavailable; animation order could not be checked.")
        return
    for anim_id, expected_index in sorted(reference_ids.items(), key=lambda item: item[1]):
        if re.match(r"anim_unused_(?:human|horse)_anim_", anim_id):
            continue
        actual_index = generated_ids.get(anim_id)
        if actual_index != expected_index:
            errors.append(
                "[MB1011] Generated animation ID mismatch for "
                f"{anim_id}: expected {expected_index}, got {actual_index}"
            )

def _parse_module_constants(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    constants: Dict[str, str] = {}
    raw = _read_text(path)
    pattern = re.compile(
        r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:[\"']([^\"']+)[\"']|([A-Za-z_][A-Za-z0-9_]*)|(-?\d+))"
    )
    for match in pattern.finditer(raw):
        value = match.group(2) or match.group(3) or match.group(4) or ""
        constants[match.group(1)] = value
    return constants

def _resolve_constant_symbol(constants: Dict[str, str], name: str) -> str:
    value = constants.get(name, "")
    seen: Set[str] = set()
    while value in constants and value not in seen:
        seen.add(value)
        value = constants.get(value, "")
    return value

def _check_native_range_contracts(warnings: List[str], *, check_ids: bool = True) -> None:
    if not check_ids:
        return
    constants = _parse_module_constants(ROOT / "compile" / "module_constants.py")
    if not constants:
        warnings.append("[MB1011-RANGE] Generated module_constants.py unavailable; Native range contracts were not checked.")
        return
    for label, begin_name, end_name, id_path in MB1011_NATIVE_RANGE_CONTRACTS:
        begin_symbol = _resolve_constant_symbol(constants, begin_name)
        end_symbol = _resolve_constant_symbol(constants, end_name)
        if not begin_symbol or not end_symbol:
            warnings.append(f"[MB1011-RANGE] {label} range constants missing: {begin_name}/{end_name}")
            continue
        id_assignments = _parse_id_assignments(id_path)
        if not id_assignments:
            warnings.append(f"[MB1011-RANGE] {label} ID file unavailable: {id_path.relative_to(ROOT).as_posix()}")
            continue
        begin_index = id_assignments.get(begin_symbol)
        end_index = id_assignments.get(end_symbol)
        if begin_index is None or end_index is None:
            warnings.append(
                "[MB1011-RANGE] "
                f"{label} range points do not resolve to IDs: {begin_name}={begin_symbol}, {end_name}={end_symbol}"
            )
            continue
        if begin_index >= end_index:
            warnings.append(
                "[MB1011-RANGE] "
                f"{label} range is empty or inverted: {begin_symbol}={begin_index}, {end_symbol}={end_index}"
            )

def _write_mb1011_hardcoded_contract_report(errors: List[str], warnings: List[str], *, check_ids: bool = True) -> None:
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = DOCS_REPORTS / "mb1011_hardcoded_contract.md"
    lines = [
        "# M&B 1.011 Hardcoded Contract",
        "",
        "Doctor validates these generated compile-layer contracts after source fragments are assembled:",
        "",
        "- Startup menus: `start_game_1` and `start_phase_2` must keep generated IDs 0 and 1.",
        "- Engine callback scripts: `game_start` and the other `game_*` callbacks must exist by name; their generated order is not treated as hardcoded.",
        "- Engine callback presentations: `game_credits` must exist by name; Warband-only `game_start` and `game_escape` presentation callbacks stay absent.",
        "- Engine sentinels: first parties, party templates, troops, factions, strings, skills, mission templates, skins, and the Native `item_codes.h` item block keep their hardwired indices.",
        "- Animation IDs: used Native animation IDs are compared against the M&B 1.011 baseline; unused human/horse animation slots are left available for replacement.",
        "- Dialog states: engine-entered states (`start`, `party_relieved`, `prisoner_liberated`, `enemy_defeated`, `event_triggered`) and `close_window` must exist.",
        "- Native-script range contracts are checked separately as warnings because they are script/order contracts rather than executable-hardwired IDs.",
        "",
        "Current result:",
        "",
        f"- Generated ID file checks: {'enabled' if check_ids else 'deferred until process output exists'}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
    ]
    if errors:
        lines.append("")
        lines.append("## Errors")
        lines.extend(f"- {error}" for error in errors)
    if warnings:
        lines.append("")
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in warnings)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def check_generated_hardcoded_contract(*, check_ids: bool = True) -> Tuple[List[str], List[str]]:
    """Validate generated compile files against the M&B 1.011 hardcoded contract."""
    errors: List[str] = []
    warnings: List[str] = []

    for label, module_path, id_path, id_prefix, expected_names in MB1011_HARDCODED_CONTRACTS:
        _check_generated_sequence_contract(
            label,
            module_path,
            id_path,
            id_prefix,
            expected_names,
            errors,
            warnings,
            check_ids=check_ids,
        )

    for label, module_path, id_path, id_prefix, expected_names in MB1011_ENGINE_CALLBACK_CONTRACTS:
        _check_generated_presence_contract(
            label,
            module_path,
            id_path,
            id_prefix,
            expected_names,
            errors,
            warnings,
            check_ids=check_ids,
        )

    _check_skin_contract(errors, warnings)
    _check_dialog_state_contract(errors, warnings)
    _check_animation_id_contract(errors, warnings, check_ids=check_ids)
    _check_native_range_contracts(warnings, check_ids=check_ids)

    presentation_names = _parse_module_tuple_names(ROOT / "compile" / "module_presentations.py")
    presentation_ids = _parse_id_assignments(ROOT / "compile" / "ids" / "ID_presentations.py")
    for forbidden_name in ("game_start", "game_escape"):
        if forbidden_name in presentation_names:
            errors.append(f"[MB1011] Warband-only presentation callback is exported in M&B 1.011: {forbidden_name}")
        if f"prsnt_{forbidden_name}" in presentation_ids:
            errors.append(f"[MB1011] Warband-only presentation ID is generated in M&B 1.011: prsnt_{forbidden_name}")

    export_parties_path = ROOT / "_export" / "parties.txt"
    if check_ids and export_parties_path.exists():
        export_lines = [
            line.strip()
            for line in _read_text(export_parties_path).splitlines()
            if line.strip() and not line.startswith("partiesfile") and not re.fullmatch(r"\d+\s+\d+", line.strip())
        ]
        if export_lines and "p_main_party" not in export_lines[0]:
            errors.append("[MB1011] Exported parties.txt does not put p_main_party first.")

    _write_mb1011_hardcoded_contract_report(errors, warnings, check_ids=check_ids)
    return errors, warnings

def _doctor_report_artifacts() -> List[Dict[str, object]]:
    if not DOCS_REPORTS.exists():
        return []
    artifacts: List[Dict[str, object]] = []
    for path in sorted(DOCS_REPORTS.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file() or path == REPORT_JSON_PATH:
            continue
        try:
            size_bytes = path.stat().st_size
        except OSError:
            size_bytes = 0
        artifacts.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "name": path.name,
                "size_bytes": int(size_bytes),
            }
        )
    return artifacts

def _slowest_timings(timings_ms: Dict[str, int], limit: int = 8) -> List[Dict[str, object]]:
    return [
        {"name": name, "ms": int(ms)}
        for name, ms in sorted(timings_ms.items(), key=lambda item: (-item[1], item[0]))[: max(0, int(limit))]
    ]

def _rel(p: Path, base: Path) -> str:
    return str(p.relative_to(base)).replace("\\", "/")

def _iter_py_files(base: Path) -> List[Path]:
    if not base.exists():
        return []
    files = [p for p in base.rglob("*.py") if p.is_file()]
    files.sort(key=lambda x: str(x).lower())
    return files

def _check_compile_id_shadow_artifacts(errors: List[str]) -> None:
    """Generated ID modules must only live under compile/ids.

    The build wrapper runs process scripts with compile/process at the front of
    sys.path. A stray ID_*.py in compile/process can silently shadow the fresh
    compile/ids module and export shifted numeric IDs.
    """
    shadow_roots = (ROOT / "compile", ROOT / "compile" / "process")
    for shadow_root in shadow_roots:
        if not shadow_root.exists():
            continue
        for path in sorted(shadow_root.glob("ID_*.py"), key=lambda p: p.name.lower()):
            errors.append(
                "[COMPILE] Generated ID file is in a shadow-prone folder; "
                f"delete it and keep generated IDs under compile/ids only: {path.relative_to(ROOT).as_posix()}"
            )

def _iter_all_src_py_files() -> List[Path]:
    """All *.py under src/, excluding __pycache__."""
    if not SRC_ROOT.exists():
        return []
    files = [p for p in SRC_ROOT.rglob("*.py") if p.is_file() and "__pycache__" not in p.parts]
    files.sort(key=lambda x: str(x).lower())
    return files

def _check_sod_doctrine_registry(
    script_files: List[Path],
    constant_files: List[Path],
    warnings: List[str],
    errors: List[str],
) -> None:
    """Validate the SoD elite doctrine layer that governs noble/faith upgrades."""
    scripts_by_name = {p.name for p in script_files}
    required_scripts = {
        "sod_troop_init_doctrine_registry.py",
        "sod_troop_get_doctrine.py",
        "sod_troop_get_required_facility.py",
        "sod_troop_get_elite_tier.py",
        "sod_troop_is_noble.py",
        "sod_troop_is_faith_elite.py",
        "sod_troop_can_upgrade_at_center.py",
        "sod_troop_get_upgrade_cost.py",
        "sod_troop_get_faith_upgrade.py",
        "sod_troop_find_faith_candidate.py",
        "sod_troop_store_upgrade_fail_reason.py",
        "sod_artifact_get_doctrine_discount.py",
        "sod_artifact_lord_doctrine_bias.py",
    }
    for script_name in sorted(required_scripts - scripts_by_name):
        errors.append(f"SoD doctrine registry missing helper script: {script_name}")

    constants_raw = "\n".join(_read_text(p) for p in constant_files)
    required_constants = [
        "slot_troop_sod_doctrine_role",
        "slot_troop_sod_doctrine_tier",
        "slot_troop_sod_doctrine_facility",
        "slot_troop_sod_doctrine_flags",
        "slot_troop_sod_doctrine_cost_mult",
        "slot_troop_sod_doctrine_faith_upgrade",
        "slot_troop_sod_doctrine_culture",
        "slot_troop_sod_doctrine_faction",
        "slot_troop_sod_doctrine_special_req",
        "sod_elite_tier_noble",
        "sod_elite_tier_faith",
        "sod_doctrine_facility_chapter",
        "sod_doctrine_facility_temple",
        "sod_special_req_faith_ascension",
    ]
    for const_name in required_constants:
        if const_name not in constants_raw:
            errors.append(f"SoD doctrine registry missing constant: {const_name}")

    faith_helper = SRC_SCRIPTS / "ZY_helper_scripts" / "sod_troop_get_faith_upgrade.py"
    if faith_helper.exists():
        faith_raw = _read_text(faith_helper)
        required_candidates = [
            "trp_sod_ant_honor_guard1",
            "trp_sod_mar_condottieri1",
            "trp_sod_vil_high_chief1",
            "trp_sod_ade_magnate1",
            "trp_sod_zer_3_noble1",
        ]
        for candidate in required_candidates:
            if candidate not in faith_raw:
                errors.append(f"SoD faith doctrine mapping missing candidate: {candidate}")
        required_faith_outputs = [
            "trp_sod_faith1_foot",
            "trp_sod_faith2_foot",
            "trp_sod_faith3_foot",
            "trp_sod_faith4_foot",
            "trp_sod_faith5_foot",
        ]
        for faith_output in required_faith_outputs:
            if faith_output not in faith_raw:
                errors.append(f"SoD faith doctrine mapping missing faith output family: {faith_output}")

    registry = SRC_SCRIPTS / "ZY_helper_scripts" / "sod_troop_init_doctrine_registry.py"
    if registry.exists():
        registry_raw = _read_text(registry)
        required_registry_tokens = [
            "sod_doctrine_facility_chapter",
            "sod_doctrine_facility_temple",
            "sod_special_req_chapter",
            "sod_special_req_faith_ascension",
            "slot_troop_sod_doctrine_culture",
            "slot_troop_sod_doctrine_faction",
        ]
        for token in required_registry_tokens:
            if token not in registry_raw:
                errors.append(f"SoD doctrine registry does not assign required metadata token: {token}")

    set_slot_re = re.compile(
        r"troop_set_slot\s*,\s*[\"'](?P<src>trp_[A-Za-z0-9_]+)[\"']\s*,\s*"
        r"slot_troop_sod_upgrade[12]\s*,\s*[\"'](?P<dst>trp_[A-Za-z0-9_]+)[\"']"
    )
    for p in script_files:
        raw = _read_text(p)
        for match in set_slot_re.finditer(raw):
            if match.group("src") == match.group("dst"):
                errors.append(
                    f"SoD upgrade self-loop in {_rel(p, ROOT)}: {match.group('src')} upgrades to itself"
                )

def _check_sod_threat_board_registry(
    script_files: List[Path],
    menu_files: List[Path],
    trigger_files: List[Path],
    quest_files: List[Path],
    constant_files: List[Path],
    warnings: List[str],
    errors: List[str],
) -> None:
    """Validate the regional threat board contract layer."""
    scripts_by_name = {p.name for p in script_files}
    required_scripts = {
        "sod_threat_board_init_registry.py",
        "sod_threat_board_generate_offers.py",
        "sod_threat_board_accept_contract.py",
        "sod_threat_board_normalize_center.py",
        "sod_threat_board_spawn_target.py",
        "sod_threat_board_complete_contract.py",
        "sod_threat_board_fail_contract.py",
        "sod_threat_board_describe_offer.py",
        "sod_threat_board_describe_active_contract.py",
        "sod_threat_board_apply_regional_pressure.py",
        "sod_threat_board_get_archetype.py",
        "sod_threat_board_note_party_defeated.py",
    }
    for script_name in sorted(required_scripts - scripts_by_name):
        errors.append(f"Regional threat board missing helper script: {script_name}")

    constants_raw = "\n".join(_read_text(p) for p in constant_files)
    required_constants = [
        "sod_threat_type_pirates",
        "sod_threat_type_deserters",
        "sod_threat_type_relic_thieves",
        "sod_threat_type_rogue_company",
        "sod_threat_type_cattle_raiders",
        "sod_threat_type_faction_problem",
        "slot_party_sod_threat_type",
        "slot_party_sod_threat_active_quest",
        "slot_quest_sod_threat_target_party",
        "slot_quest_sod_threat_ready_to_claim",
    ]
    for const_name in required_constants:
        if const_name not in constants_raw:
            errors.append(f"Regional threat board missing constant: {const_name}")

    quest_raw = "\n".join(_read_text(p) for p in quest_files)
    if "regional_threat_contract" not in quest_raw:
        errors.append("Regional threat board missing qst_regional_threat_contract quest entry")

    menu_raw = "\n".join(_read_text(p) for p in menu_files)
    if "regional_threat_board" not in menu_raw:
        errors.append("Regional threat board menu is missing")
    if "Check the job board." not in menu_raw:
        errors.append("Regional threat board is not exposed from center menus")

    trigger_raw = "\n".join(_read_text(p) for p in trigger_files)
    if "script_sod_threat_board_fail_contract" not in trigger_raw:
        errors.append("Regional threat board expiration trigger is missing")

    registry = SRC_SCRIPTS / "ZY_helper_scripts" / "sod_threat_board_get_archetype.py"
    if registry.exists():
        registry_raw = _read_text(registry)
        required_templates = [
            "pt_bandits",
            "pt_sea_raiders",
            "pt_deserters",
            "pt_sod_merc_deserters",
            "pt_mountain_bandits",
            "pt_ravaging_bandits",
            "pt_mercenaries",
            "pt_sod_mercs",
            "pt_troublesome_bandits",
            "pt_forest_bandits",
            "pt_serpent_host_ravaging_bandits",
            "pt_bc_bandits",
        ]
        for template in required_templates:
            if template not in registry_raw:
                errors.append(f"Regional threat archetype registry missing party template: {template}")

        archetype_count = len(re.findall(r"eq,\s*\":archetype\",\s*sod_threat_archetype_", registry_raw))
        if archetype_count < 12:
            errors.append("Regional threat archetype registry has fewer than 12 curated archetypes")

    report_path = DOCS_REPORTS / "regional_threat_board_report.txt"
    report_lines = [
        "Regional Threat Board Report",
        "",
        "Archetypes: 12 curated v1 contracts",
        "Threat types: pirates, deserters, relic thieves, rogue companies, cattle raiders, faction problems",
        "Interfaces: center board menu, camp report entry, quest-backed active contract",
        "Lifecycle: generate offers, accept, spawn/mark target, defeat, claim, expire/fail",
        "Integrations: mercenary guild favor, artifact bounty rewards, village cattle pressure, faction/center relations",
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


_BUILDING_SLOT_NAME_RE = re.compile(r"\bslot_center_has_[A-Za-z0-9_]+\b")
_BUILDING_SLOT_ASSIGNMENT_RE = re.compile(r"(?m)^\s*(slot_center_has_[A-Za-z0-9_]+)\s*=\s*([0-9]+)\b")


def _load_building_slot_constants(raw: str) -> Tuple[Dict[str, int], Dict[str, int], Dict[int, List[str]]]:
    slot_constants: Dict[str, int] = {}
    name_counts: Dict[str, int] = {}
    value_to_names: Dict[int, List[str]] = {}
    for match in _BUILDING_SLOT_ASSIGNMENT_RE.finditer(raw):
        slot_name = match.group(1)
        slot_value = int(match.group(2))
        slot_constants[slot_name] = slot_value
        name_counts[slot_name] = name_counts.get(slot_name, 0) + 1
        value_to_names.setdefault(slot_value, []).append(slot_name)
    return slot_constants, name_counts, value_to_names


def _duplicate_values(values: List[int]) -> List[int]:
    counts: Dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return sorted(value for value, count in counts.items() if count > 1)


def _check_building_registry_consistency(
    constant_files: List[Path],
    source_files: List[Path],
    warnings: List[str],
    errors: List[str],
) -> None:
    try:
        from src.constants.building_registry import BUILDING_REGISTRY as building_registry, validate_building_registry
    except Exception as exc:
        errors.append(f"[BUILDING] Failed to import building registry helpers: {exc}")
        return

    registry_issues = validate_building_registry()
    if registry_issues:
        errors.append(f"[BUILDING] validate_building_registry reported {len(registry_issues)} issue(s).")
        errors.extend(f"[BUILDING] {issue}" for issue in registry_issues)

    module_constants_path = next((p for p in constant_files if p.name == "module_constants.py"), None)
    if module_constants_path is None:
        errors.append("[BUILDING] Missing src/constants/module_constants.py for building consistency checks.")
        return

    raw_constants = _read_text(module_constants_path)
    slot_constants, slot_name_counts, slot_value_to_names = _load_building_slot_constants(raw_constants)
    slot_name_by_value = {value: names[0] for value, names in slot_value_to_names.items() if names}

    duplicate_slot_names = sorted(name for name, count in slot_name_counts.items() if count > 1)
    if duplicate_slot_names:
        errors.append(
            "[BUILDING] module_constants defines duplicate slot name assignment(s): "
            + ", ".join(duplicate_slot_names[:40])
        )
        if len(duplicate_slot_names) > 40:
            errors.append(f"[BUILDING] ...and {len(duplicate_slot_names) - 40} more duplicate slot name(s)")

    duplicate_slot_values = sorted(value for value, names in slot_value_to_names.items() if len(names) > 1)
    if duplicate_slot_values:
        errors.append(
            "[BUILDING] module_constants defines overlapping slot value(s): "
            + ", ".join(
                f"{slot_name_by_value.get(value, str(value))}={value}" for value in duplicate_slot_values[:40]
            )
        )
        if len(duplicate_slot_values) > 40:
            errors.append(f"[BUILDING] ...and {len(duplicate_slot_values) - 40} more overlapping slot value(s)")

    registry_by_value: Dict[int, Dict[str, object]] = {}
    registry_by_name: Dict[str, Dict[str, object]] = {}
    for definition in building_registry:
        if not isinstance(definition, dict):
            continue
        slot_value = definition.get("building_slot")
        if isinstance(slot_value, int):
            registry_by_value[slot_value] = definition
        slot_name = definition.get("building_key")
        if isinstance(slot_name, str):
            registry_by_name[slot_name] = definition

    registry_values = set(registry_by_value)
    registry_names = set(registry_by_name)
    defined_values = set(slot_constants.values())
    defined_names = set(slot_constants.keys())

    missing_registry_values = sorted(registry_values - defined_values)
    if missing_registry_values:
        missing_labels = [slot_name_by_value.get(value, str(value)) for value in missing_registry_values[:40]]
        errors.append(
            "[BUILDING] Registry slots missing from module_constants slot definitions: "
            + ", ".join(missing_labels)
        )
        if len(missing_registry_values) > 40:
            errors.append(f"[BUILDING] ...and {len(missing_registry_values) - 40} more registry slot(s)")

    non_building_center_slots = {"slot_center_has_bandits"}
    extra_defined_names = sorted(
        name
        for name in defined_names
        if slot_constants.get(name) not in registry_values and name not in non_building_center_slots
    )
    if extra_defined_names:
        errors.append(
            "[BUILDING] module_constants defines slot_center_has_* constants not present in the building registry: "
            + ", ".join(extra_defined_names[:40])
        )
        if len(extra_defined_names) > 40:
            errors.append(f"[BUILDING] ...and {len(extra_defined_names) - 40} more unregistered slot(s)")

    center_list_slots: Dict[str, Set[int]] = {"village": set(), "town": set(), "castle": set()}
    center_list_hits = 0
    for match in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*\[", raw_constants):
        var_name = match.group(1)
        if "build" not in var_name.lower():
            continue
        try:
            body = _extract_list_block(raw_constants, var_name)
        except Exception:
            continue
        slot_names = _BUILDING_SLOT_NAME_RE.findall(body)
        if not slot_names:
            continue
        matched_centers = [center for center in ("village", "town", "castle") if center in var_name.lower()]
        if not matched_centers:
            continue
        center_list_hits += 1
        for slot_name in slot_names:
            slot_value = slot_constants.get(slot_name)
            if slot_value is None:
                continue
            for center in matched_centers:
                center_list_slots[center].add(slot_value)

    if center_list_hits == 0:
        warnings.append(
            "[BUILDING] No center-specific building lists were discovered in module_constants.py; UI coverage checks were limited."
        )

    slot_center_types: Dict[int, Set[str]] = {}
    for center_type, slot_values in center_list_slots.items():
        for slot_value in slot_values:
            slot_center_types.setdefault(slot_value, set()).add(center_type)

    for slot_value, definition in registry_by_value.items():
        expected_types = set(definition.get("allowed_center_types", ()))
        actual_types = slot_center_types.get(slot_value, set())
        slot_name = slot_name_by_value.get(slot_value, str(slot_value))

        if expected_types and not actual_types:
            errors.append(f"[BUILDING] {slot_name} has no center-list coverage in module_constants.py")
            continue

        missing_types = sorted(expected_types - actual_types)
        extra_types = sorted(actual_types - expected_types)
        if missing_types:
            errors.append(
                f"[BUILDING] {slot_name} is missing center-list coverage for: {', '.join(missing_types)}"
            )
        if extra_types:
            errors.append(
                f"[BUILDING] {slot_name} appears in center lists it should not: {', '.join(extra_types)}"
            )

    for fp in source_files:
        raw = _read_text(fp)
        rel = fp.relative_to(ROOT).as_posix()
        for token, line_no, _ in _iter_identifier_tokens_with_linenos(raw):
            if not token.startswith("slot_center_has_"):
                continue
            if token not in slot_constants:
                errors.append(f"[BUILDING] {rel}:{line_no} references undefined slot constant {token}")
                continue
            if token not in defined_names:
                errors.append(f"[BUILDING] {rel}:{line_no} references building slot {token} missing from registry")

    report_path = DOCS_REPORTS / "building_registry_report.txt"
    report_lines = [
        "Building Registry Report",
        "========================",
        "",
        "Purpose: data-driven matrix for construction UI, validation, effects, and balance review.",
        f"Registry entries: {len(list(building_registry))}",
        "",
        "Compatibility:",
        "- Existing slot_center_has_* save slots are preserved.",
        "- module_constants center building lists are checked against registry allowed_center_types.",
        "- script_get_improvement_details remains as a compatibility wrapper.",
        "",
        "Runtime APIs:",
        "- script_get_building_definition",
        "- script_get_building_display_name",
        "- script_get_building_description",
        "- script_get_building_cost",
        "- script_get_building_prerequisites",
        "- script_can_build_improvement",
        "- script_validate_construction_choice",
        "- script_get_center_building_effect_totals",
        "- script_apply_weekly_building_effects",
        "",
        "Matrix:",
        "slot | key | centers | category | tier | cost | build_days | prereqs | upgrade_from | upgrade_to | exclusive_group | effects | upkeep",
        "--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---",
    ]
    for definition in sorted(building_registry, key=lambda d: (str(d.get("ui_category", "")), str(d.get("building_key", "")))):
        slot_value = definition.get("building_slot")
        slot_name = slot_name_by_value.get(slot_value, str(slot_value))
        centers = ",".join(definition.get("allowed_center_types", ())) or "-"
        prereqs = ",".join(slot_name_by_value.get(v, str(v)) for v in definition.get("prerequisite_buildings", ())) or "-"
        upgrade_from = ",".join(slot_name_by_value.get(v, str(v)) for v in definition.get("upgrade_from", ())) or "-"
        upgrade_to = ",".join(slot_name_by_value.get(v, str(v)) for v in definition.get("upgrade_to", ())) or "-"
        effects = ",".join(
            f"{tag}:{definition.get('effect_numbers', ())[idx] if idx < len(definition.get('effect_numbers', ())) else 0}"
            for idx, tag in enumerate(definition.get("effect_tags", ()))
        ) or "-"
        report_lines.append(
            " | ".join(
                [
                    slot_name,
                    str(definition.get("building_key", "-")),
                    centers,
                    str(definition.get("ui_category", "-")),
                    str(definition.get("tier", 0)),
                    str(definition.get("cost", 0)),
                    str(definition.get("build_days") if definition.get("build_days") is not None else "-"),
                    prereqs,
                    upgrade_from,
                    upgrade_to,
                    str(definition.get("exclusive_group") or "-"),
                    effects,
                    str(definition.get("weekly_upkeep", 0)),
                ]
            )
        )
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def _scan_tokens_by_file(files: List[Path], pattern: str) -> Dict[str, List[str]]:
    rx = re.compile(pattern)
    result: Dict[str, List[str]] = {}
    for fp in files:
        raw = _read_text(fp)
        hits = sorted(set(rx.findall(raw)))
        if hits:
            result[fp.relative_to(ROOT).as_posix()] = hits
    return result


def _count_pattern(files: List[Path], pattern: str) -> int:
    rx = re.compile(pattern)
    total = 0
    for fp in files:
        total += len(rx.findall(_read_text(fp)))
    return total


def _quest_fragment_style(path: Path) -> str:
    raw = _read_text(path)
    if "quest_chain_from_specs" in raw or "quest_template_spec" in raw or "quest_stage_spec" in raw:
        return "schema-backed"
    if "QUESTS" in raw:
        return "legacy tuple"
    return "helper/runtime"


def _quest_ids_from_fragment(path: Path) -> List[str]:
    raw = _read_text(path)
    ids: List[str] = []
    for match in re.finditer(r'\(\s*"([a-z][a-z0-9_]*)"\s*,', raw):
        quest_id = match.group(1)
        if quest_id not in ids:
            ids.append(quest_id)
    for match in re.finditer(r'quest_template_spec\(\s*"([a-z][a-z0-9_]*)"', raw):
        quest_id = match.group(1)
        if quest_id not in ids:
            ids.append(quest_id)
    return ids


def _write_quest_architecture_report(
    quest_files: List[Path],
    script_files: List[Path],
    dialog_files: List[Path],
    menu_files: List[Path],
    trigger_files: List[Path],
    mission_template_files: List[Path],
    constant_files: List[Path],
) -> None:
    report_path = DOCS_REPORTS / "quest_architecture_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)

    source_sets = {
        "scripts": script_files,
        "dialogs": dialog_files,
        "menus": menu_files,
        "triggers": trigger_files,
        "mission_templates": mission_template_files,
        "quests": quest_files,
        "constants": constant_files,
    }
    all_runtime_files = script_files + dialog_files + menu_files + trigger_files + mission_template_files
    all_source_files = all_runtime_files + quest_files + constant_files

    quest_inventory = []
    total_quest_ids = 0
    schema_backed = 0
    for path in sorted(quest_files, key=lambda p: p.relative_to(ROOT).as_posix()):
        if "_preamble" in path.parts or path.name.startswith("quest_"):
            continue
        quest_ids = _quest_ids_from_fragment(path)
        style = _quest_fragment_style(path)
        if style == "schema-backed":
            schema_backed += 1
        total_quest_ids += len(quest_ids)
        quest_inventory.append((path.relative_to(ROOT).as_posix(), style, quest_ids))

    entry_patterns = {
        "generation": r"script_get_random_quest|script_get_dynamic_quest|script_random_town_random_quest|script_sod_threat_board_generate_offers",
        "acceptance": r"script_start_quest|quest_accepted|script_sod_threat_board_accept_contract",
        "live_progression": r"quest_set_slot|quest_get_slot|quest_slot_eq|check_quest_active|check_quest_succeeded|check_quest_failed|setup_quest_text|add_quest_note",
        "battle_hooks": r"total_victory|encounter|agent_killed|lead_charge|mission_|battle|party_defeated|script_sod_threat_board_note_party_defeated",
        "completion_failure": r"script_succeed_quest|script_finish_quest|script_fail_quest|script_end_quest|script_abort_quest|quest_completed|quest_failed|quest_expired",
        "rewards": r"slot_quest_xp_reward|slot_quest_gold_reward|troop_add_gold|add_xp|change_player_relation|change_player_honor|add_renown",
        "expiration": r"slot_quest_expiration_days|dont_give_again|quest_expired|expiration|deadline",
        "npc_dialogue": r"\$g_talk_troop|dialog|lord_start|village_elder|guildmaster|mayor|quest_ask|request_mission",
    }

    entry_counts: Dict[str, Dict[str, int]] = {}
    for phase, pattern in entry_patterns.items():
        entry_counts[phase] = {
            label: _count_pattern(files, pattern)
            for label, files in source_sets.items()
            if files
        }

    storage_patterns = {
        "quest_slots": r"slot_quest_[A-Za-z0-9_]+",
        "troop_slots": r"slot_troop_[A-Za-z0-9_]*(?:quest|mission|prisoner|cur_center)[A-Za-z0-9_]*",
        "party_slots": r"slot_party_[A-Za-z0-9_]*(?:quest|mission|threat|target)[A-Za-z0-9_]*",
        "globals": r"\$[A-Za-z0-9_]*(?:qst|quest|mission|talk|random_quest|merchant_offered)[A-Za-z0-9_]*",
        "quest_ids": r"qst_[A-Za-z0-9_]+",
    }
    storage_maps = {
        label: sorted(
            set(
                token
                for file_tokens in _scan_tokens_by_file(all_source_files, pattern).values()
                for token in file_tokens
            )
        )
        for label, pattern in storage_patterns.items()
    }

    dependency_ops = {
        "read_state": r"quest_get_slot|quest_slot_eq|check_quest_active|check_quest_succeeded|check_quest_failed|quest_slot_ge",
        "mutate_state": r"quest_set_slot|script_start_quest|script_succeed_quest|script_fail_quest|script_end_quest|script_finish_quest|script_abort_quest",
        "dialogue_entry": r"script_get_random_quest|request_mission|quest_ask|lord_start|village_elder|guildmaster",
        "time_entry": r"slot_quest_expiration_days|dont_give_again|deadline|expiration",
        "battle_entry": r"total_victory|mission|battle|party_defeated|encounter",
    }
    dependency_by_file: Dict[str, Dict[str, int]] = {}
    for fp in all_runtime_files:
        raw = _read_text(fp)
        row = {name: len(re.findall(pattern, raw)) for name, pattern in dependency_ops.items()}
        if any(row.values()):
            dependency_by_file[fp.relative_to(ROOT).as_posix()] = row

    reference_108 = ROOT.parent / "References" / "108" / "108_quest_system.md"
    reference_note = "108 reference found" if reference_108.exists() else "108 reference not found in expected workspace path"

    lines = [
        "Quest Architecture Report",
        "=========================",
        "",
        "Purpose: source-of-truth audit for rebuilding quests into a structured, event-driven domain model.",
        f"Generated by: build/doctor.py",
        f"108 comparison source: {reference_note}",
        "",
        "Phase Coverage",
        "--------------",
        "- Phase 1 audit: implemented in this report.",
        "- Phase 2 domain model: implemented by src/quests/quest_domain.py, quest_schema.py, and quest_specs.py.",
        "- Phase 3 state machine: implemented by src/quests/quest_runtime.py.",
        "- Phase 4 event-driven progression: implemented by src/quests/quest_events.py and runtime dispatch hooks.",
        "- Phase 5 NPC state model: implemented by QuestNPCState plus legacy troop/dialog state mapping in this report.",
        "- Phase 6 dynamic generation: implemented by src/quests/quest_generation.py with weighted templates, world-context inputs, cooldown metadata, and generated offers.",
        "- Phase 7 authoring DSL: implemented by src/quests/quest_dsl.py with reusable stage decorators, reward/failure bundles, branches, and quest-family helpers.",
        "- Phase 8 validation and diagnostics: implemented by src/quests/quest_diagnostics.py plus docs/reports/quest_diagnostics_report.txt.",
        "- Phase 9 script/compiler integration: implemented by runtime adapter scripts, quest runtime slots, engine hook dispatch, and docs/reports/quest_engine_integration_report.txt.",
        "- Phase 10 battle-integrated quest actions: implemented by battle action slots, mission callbacks, prisoner/capture hooks, and docs/reports/quest_battle_integration_report.txt.",
        "- Phase 11 quest journal and concurrency: implemented by journal slots/scripts, camp report UI, archive counters, priority categories, and docs/reports/quest_journal_report.txt.",
        "- Phase 12 branching quest chains: implemented by chain slots/scripts, delayed resume heartbeats, runtime outcome hooks, and docs/reports/quest_branching_report.txt.",
        "- Phase 13 rewards, consequences, and reputation: implemented by outcome slots/scripts, completion/failure adapters, journal summaries, and docs/reports/quest_outcome_report.txt.",
        "- Phase 14 narrative and dialogue integration: implemented by quest memory slots/scripts, flavor-dialogue fragments, and quest-aware reaction lines.",
        "- Phase 15 content migration strategy: implemented by docs/reports/quest_migration_report.txt and the quest migration planner helpers.",
        "",
        "Domain Types",
        "------------",
        "- QuestTemplate",
        "- QuestChain",
        "- QuestStage",
        "- QuestOffer",
        "- QuestRuntime",
        "- QuestJournal",
        "- QuestCondition",
        "- QuestAction",
        "- QuestTrigger",
        "- QuestReward",
        "- QuestFailure",
        "- QuestNPCState",
        "- QuestWorldContext",
        "- QuestGenerationContext",
        "- QuestGenerationRule",
        "- DynamicQuestTemplate",
        "- GeneratedQuestOffer",
        "- QuestBranch",
        "- QuestDiagnostic",
        "- QuestDiagnosticsReport",
        "",
        "Dynamic Generation Surface",
        "--------------------------",
        "- Inputs: faction_war_state, settlement_danger, economy_state, player_relation, player_renown, party_size, nearby_threats, recent_battles, center_ownership, prisoner_state, trade_routes, regional_unrest.",
        "- Quest types: rescue, escort, hunt, delivery, sabotage, defense, diplomacy, recruitment, investigation, revenge, retaliation, infiltration, siege_support, recovery, assassination, relief_supply, prisoner_exchange.",
        "- Selection model: template rules score world context into weight and difficulty; region tags, faction personality weights, recent-offer cooldown filtering, renown, and party size influence generated offers.",
        "- Default catalog: src/quests/quest_generation.py ships first-pass templates for every Phase 6 quest type so engine adapters can request region-aware offers without static one-off lists.",
        "",
        "Authoring DSL Surface",
        "---------------------",
        "- Chain/stage primitives: quest_chain, quest_stage, quest_blueprint, quest_branch, quest_optional_stage, quest_timed_stage, quest_repeatable_stage.",
        "- Bundles: quest_reward_bundle and quest_failure_bundle package common gold, XP, renown, honor, relation, and cooldown payloads with stable metadata.",
        "- Quest-family helpers: delivery_quest, hunt_quest, escort_quest, rescue_quest, siege_quest, diplomacy_quest, ambush_quest, investigation_quest.",
        "- Validation: doctor runs a DSL smoke chain that builds optional, timed, repeatable, delivery, hunt, escort, rescue, siege, diplomacy, ambush, and investigation examples.",
        "",
        "Diagnostics Surface",
        "-------------------",
        "- Build-time validation covers identifiers, duplicate quest IDs, duplicate stage IDs, missing stage links, invalid transitions, unreachable branches/stages, condition/action syntax, reward/failure payloads, and impossible generation configs.",
        "- Source reports: docs/reports/quest_diagnostics_report.txt records quest source line mapping, chain/stage graph diagnostics, dependency notes, and cross-fragment conflicts.",
        "- Failure mode: doctor promotes hard quest graph/generation errors into human-readable build failures while leaving suspicious-but-legal authoring patterns as warnings.",
        "",
        "Engine Integration Surface",
        "--------------------------",
        "- Runtime slots: slot_quest_sod_runtime_state/stage/template/chain/flags/last_event/last_actor/last_party/last_center/last_day/progress/target/metadata.",
        "- Adapter scripts: sod_quest_runtime_accept/update/complete/fail/abort/init_metadata plus sod_quest_event_dispatch and sod_quest_dispatch_active_event.",
        "- Hook points: script_start_quest, script_succeed_quest, script_fail_quest, script_abort_quest, script_cancel_quest, script_end_quest, game_event_battle_end, game_event_party_encounter, and a daily simple trigger.",
        "- Generated output remains legacy-compatible quest tuples while carrying runtime-compatible metadata through quest slots and event constants.",
        "",
        "Battle Quest Surface",
        "--------------------",
        "- Objective actions: kill target, capture target, protect target, survive timer, break siege line, hold position, destroy force, escort during battle, free prisoner, rescue allied captain, defeat wave.",
        "- Mission callbacks: quest_battle_agent_defeated uses a normal-M&B-safe agent-state scan; quest_battle_tick handles timed/hold/siege-line rescue objectives; lead_charge initializes active battle objectives.",
        "- Transfer hooks: script_remove_troop_from_prison and script_event_hero_taken_prisoner_by_player feed free-prisoner and capture-target objectives into the same event layer.",
        "",
        "Quest Journal Surface",
        "---------------------",
        "- Journal slots: flags, priority, chain progress, stage progress, category, archive day, and sort key.",
        "- Categories: pinned, main, side, urgent, completed archive, failed archive.",
        "- UI: camp reports exposes mnu_quest_journal_report with active capacity, priority buckets, archive totals, and expiration warnings.",
        "- Concurrency: sod_quest_journal_capacity_default sets the recommended active quest cap while legacy native active quests remain supported.",
        "",
        "Branching Chain Surface",
        "-----------------------",
        "- Chain slots: id, step, branch, choice, lock state, resume day, ending, flags, next quest, and previous quest.",
        "- Branch scripts: linear success/failure continuation, explicit player choice branches, faction-alignment branches, hidden unlocks, lockouts, resettable chains, alternate ending markers, and delayed resume.",
        "- Runtime hooks: quest completion and failure invoke the chain outcome adapter; daily quest runtime updates resume delayed branches when their campaign day arrives.",
        "- Journal visibility: the quest journal appends branch counts, delayed resumes, locked paths, and hidden unlock totals.",
        "",
        "Migration Surface",
        "-----------------",
        "- Legacy tuple fragments continue to compile while the migration planner ranks files by conversion risk.",
        "- Small chain fragments and structured template bundles are the preferred first migration targets.",
        "- Repeated quest families should be normalized into shared helper patterns before special cases are converted.",
        "- Generated reports capture a recommended migration order so authors can remove duplication incrementally instead of all at once.",
        "",
        "Quest Outcome Surface",
        "---------------------",
        "- Reward slots cover gold, XP, NPC relation, faction standing, center relation, renown, honor, troop/member rewards, item rewards, prisoners, titles, access flags, discounts, follow-up quests, and prosperity/world changes.",
        "- Consequence slots cover relation loss, reputation loss, regional instability, quest lockouts, delayed availability, chain failure, and alternate quest availability through follow-up reveal states.",
        "- Runtime hooks: quest completion applies configured rewards once; quest failure applies configured consequences once.",
        "- Journal visibility: the quest journal appends configured/applied outcome counters, world-changing outcome counts, and follow-up unlock totals.",
        "",
        "Runtime Quest States",
        "--------------------",
        "- inactive, offered, accepted, active, paused, stage_complete, completed, failed, aborted, expired, hidden, locked, revealed",
        "",
        "Runtime Stage States",
        "--------------------",
        "- pending, active, completed, failed, skipped, branched, optional, timed_out",
        "",
        "Quest Fragment Inventory",
        "------------------------",
        f"- Quest fragment files: {len(quest_inventory)}",
        f"- Quest IDs discovered in fragments: {total_quest_ids}",
        f"- Schema-backed fragments: {schema_backed}",
        "",
    ]
    for rel, style, quest_ids in quest_inventory:
        sample = ", ".join(quest_ids[:12])
        if len(quest_ids) > 12:
            sample += f", ... (+{len(quest_ids) - 12})"
        lines.append(f"- {rel}: {style}; {len(quest_ids)} quest id(s): {sample or '-'}")

    lines.extend(["", "Quest Entry Point Counts", "------------------------"])
    for phase, counts in entry_counts.items():
        count_text = ", ".join(f"{label}={count}" for label, count in sorted(counts.items()) if count)
        lines.append(f"- {phase}: {count_text or 'no direct hits'}")

    lines.extend(["", "State Storage Map", "-----------------"])
    for label, tokens in storage_maps.items():
        sample = ", ".join(tokens[:40])
        if len(tokens) > 40:
            sample += f", ... (+{len(tokens) - 40})"
        lines.append(f"- {label}: {len(tokens)} token(s): {sample or '-'}")

    lines.extend(["", "Dependency Chart", "----------------"])
    for rel, row in sorted(dependency_by_file.items()):
        row_text = ", ".join(f"{key}={value}" for key, value in row.items() if value)
        lines.append(f"- {rel}: {row_text}")

    lines.extend(
        [
            "",
            "Gap Analysis Versus 108",
            "-----------------------",
            "- Quest generation: dynamic templates now score world context into QuestOffer records. Remaining seam: progressively route legacy random quest selection and town/village/lord offer menus through generate_dynamic_quest_offers.",
            "- Quest acceptance: legacy script_start_quest/dialog acceptance exists; QuestRuntime supports offered/accepted/active. Remaining seam: add thin script adapters where new authored chains need engine-side state mirroring.",
            "- Live progression: legacy quest slots and checks are widespread; QuestRuntime supports reconcile and staged progression. Remaining seam: move one quest family at a time from polling to subscriptions.",
            "- Battle hooks: Ponavosa has victory/mission hooks and the threat board defeat hook; 108 has explicit in-battle random quest tracking. Remaining seam: centralize battle events through a quest event dispatcher script layer.",
            "- Completion/failure: legacy succeed/fail/end scripts are present; QuestRuntime has complete/fail/abort/expire. Remaining seam: unify reward/cleanup calls behind domain actions.",
            "- Rewards: legacy rewards are scattered across dialogs/scripts; QuestReward exists. Remaining seam: migrate reward payloads into QuestReward specs for reportability.",
            "- Consequences: legacy consequences occur in one-off scripts; QuestAction/QuestFailure can model them. Remaining seam: author consequence metadata for major quest families.",
            "- Quest expiration: slot_quest_expiration_days and don't-give-again flows exist; QuestRuntime supports expired/timed_out. Remaining seam: dispatch time_passed events to active runtimes.",
            "- Quest chains: prison_break_chain is schema-backed and chain-ready; many legacy quest groups remain flat tuples. Remaining seam: convert lord/mayor/village quest families into QuestChainSpec groups.",
            "- NPC dialogue integration: dialogs are the dominant entry surface; QuestNPCState exists. Remaining seam: map quest-giver cooldowns/completions/failures into QuestNPCState-backed helpers.",
            "- Authoring DSL: reusable helpers now exist for large quest-chain authoring. Remaining seam: migrate older tuple quest families into DSL-authored chains as content is touched.",
            "- Validation and diagnostics: doctor now writes source-line quest diagnostics and validates domain/generation smoke graphs. Remaining seam: move migrated quest families through domain objects so every chain can emit full stage graph diagnostics instead of legacy tuple-only ID checks.",
            "- Engine integration: runtime adapters and event dispatch hooks now exist. Remaining seam: migrate individual quest families from one-off slot polling into event-specific handler scripts that consume sod_quest_event_* metadata.",
            "- Battle integration: lead_charge has generalized battle objective callbacks. Remaining seam: add the common callback bundle to siege and quest-specific mission templates as their content is migrated.",
            "- Journal integration: player-facing report and counters now exist. Remaining seam: add per-quest pin/unpin controls and richer chain/stage display as quest families migrate to structured metadata.",
            "",
            "Recommended Next Migration Slices",
            "-------------------------------",
            "- Add thin engine adapters that gather settlement danger, trade route, prisoner, and threat-board context into QuestGenerationContext before replacing static mayor/village random-offer selection.",
            "- Convert mayor/village hunt and delivery quests into QuestTemplateSpec records first; they have clear acceptance/progress/completion loops.",
            "- Add engine adapter scripts for quest_event_dispatch, quest_runtime_set_state, and quest_runtime_set_stage_state only after one family is ready to consume them.",
            "- Keep legacy tuple QUESTS output as the compiler boundary until all dialogs/scripts are migrated.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_quest_generation_registry(errors: List[str], warnings: List[str]) -> None:
    try:
        from src.quests.quest_generation import (
            DEFAULT_DYNAMIC_QUEST_TEMPLATES,
            QUEST_GENERATION_INPUTS,
            QUEST_GENERATION_TYPES,
            QuestGenerationContext,
            generate_dynamic_quest_offers,
        )
    except Exception as exc:
        errors.append(f"Quest dynamic generation registry failed to import: {exc}")
        return

    required_inputs = {
        "faction_war_state",
        "settlement_danger",
        "economy_state",
        "player_relation",
        "player_renown",
        "party_size",
        "nearby_threats",
        "recent_battles",
        "center_ownership",
        "prisoner_state",
        "trade_routes",
        "regional_unrest",
    }
    missing_inputs = sorted(required_inputs - set(QUEST_GENERATION_INPUTS))
    if missing_inputs:
        errors.append(f"Quest dynamic generation missing input(s): {', '.join(missing_inputs)}")

    required_types = {
        "rescue",
        "escort",
        "hunt",
        "delivery",
        "sabotage",
        "defense",
        "diplomacy",
        "recruitment",
        "investigation",
        "revenge",
        "retaliation",
        "infiltration",
        "siege_support",
        "recovery",
        "assassination",
        "relief_supply",
        "prisoner_exchange",
    }
    missing_types = sorted(required_types - set(QUEST_GENERATION_TYPES))
    if missing_types:
        errors.append(f"Quest dynamic generation missing type constant(s): {', '.join(missing_types)}")

    template_types = {template.quest_type for template in DEFAULT_DYNAMIC_QUEST_TEMPLATES}
    missing_template_types = sorted(required_types - template_types)
    if missing_template_types:
        warnings.append(
            "Quest dynamic generation has no default template for type(s): "
            + ", ".join(missing_template_types)
        )

    try:
        context = QuestGenerationContext(
            faction_war_state=1,
            settlement_danger=4,
            economy_state=-2,
            player_relation=20,
            player_renown=450,
            party_size=95,
            nearby_threats=4,
            recent_battles=2,
            center_ownership=1,
            prisoner_state=1,
            trade_routes=2,
            regional_unrest=4,
            faction_id="fac_kingdom_1",
            center_id="p_town_1",
            region="heartlands",
        )
        offers = generate_dynamic_quest_offers(DEFAULT_DYNAMIC_QUEST_TEMPLATES, context, limit=5)
    except Exception as exc:
        errors.append(f"Quest dynamic generation smoke test failed: {exc}")
        return

    if not offers:
        errors.append("Quest dynamic generation smoke test produced no offers")
    for generated in offers:
        if generated.weight <= 0:
            errors.append(f"Quest dynamic generation produced non-positive weight for {generated.offer.offer_id}")
        if not generated.offer.offer_id:
            errors.append("Quest dynamic generation produced an offer without an offer_id")


def _check_sod_law_framework(
    script_files: List[Path],
    menu_files: List[Path],
    trigger_files: List[Path],
    pres_files: List[Path],
    constant_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    constants_raw = "\n".join(_read_text(p) for p in constant_files)
    script_raw = "\n".join(_read_text(p) for p in script_files)
    menu_raw = "\n".join(_read_text(p) for p in menu_files)
    trigger_raw = "\n".join(_read_text(p) for p in trigger_files)
    pres_raw = "\n".join(_read_text(p) for p in pres_files)

    required_constants = [
        "slot_faction_law_1",
        "slot_faction_law_10",
        "faction_laws_begin",
        "faction_laws_end",
        "sod_law_max_active",
        "slot_faction_law_tax_peasants",
        "slot_faction_law_holy_modifier",
        "slot_faction_law_unrest",
        "slot_faction_sod_laws_migrated",
        "sod_law_block_conflict",
        "sod_law_ai_tag_economic",
    ]
    for const_name in required_constants:
        if const_name not in constants_raw:
            errors.append(f"SoD law framework missing constant: {const_name}")

    law_id_values = set(re.findall(r"(?m)^sod_law_[a-z0-9_]+\s*=\s*([0-9]+)\b", constants_raw))
    real_law_ids = {str(i) for i in range(1, 40)} - {"10", "20", "30"}
    missing_law_ids = sorted(real_law_ids - law_id_values, key=int)
    if missing_law_ids:
        errors.append("SoD law framework missing named law IDs: " + ", ".join(missing_law_ids))

    required_scripts = [
        "sod_law_is_active_for_faction",
        "sod_law_count_active_for_faction",
        "sod_law_find_empty_slot_for_faction",
        "sod_law_add_to_faction",
        "sod_law_remove_from_faction",
        "sod_law_compact_faction_laws",
        "sod_law_sync_player_legacy_slots",
        "sod_law_can_enact_for_faction",
        "sod_law_can_dismiss_for_faction",
        "sod_law_recalculate_faction_law_modifiers",
        "sod_law_sync_player_globals_from_faction",
        "sod_law_ai_process_all_factions",
        "sod_law_ai_score_law_for_faction",
        "sod_law_initialize_all_faction_defaults",
        "sod_law_describe_realm_law_report",
        "sod_law_store_block_reason_text",
        "sod_law_maybe_notify_foreign_change",
    ]
    for script_name in required_scripts:
        if f'"{script_name}"' not in script_raw:
            errors.append(f"SoD law framework missing script: {script_name}")

    for placeholder in ("sod_law_spacer_villagers", "sod_law_spacer_townspeople", "sod_law_spacer_clergy"):
        if placeholder not in script_raw:
            errors.append(f"SoD law framework does not explicitly reject placeholder law: {placeholder}")

    conflict_pairs = [
        ("sod_law_enfranchisement", "sod_law_serfdom"),
        ("sod_law_high_capitation", "sod_law_low_capitation"),
        ("sod_law_low_town_taxes", "sod_law_high_town_taxes"),
        ("sod_law_temple_supremacy", "sod_law_royal_supremacy"),
    ]
    for left, right in conflict_pairs:
        if left not in script_raw or right not in script_raw:
            errors.append(f"SoD law framework missing conflict tokens for {left} / {right}")

    if "script_sod_law_ai_process_all_factions" not in trigger_raw:
        errors.append("SoD law AI is not wired into weekly triggers")
    if "slot_faction_law_tax_townspeople" not in trigger_raw or "slot_faction_law_tax_peasants" not in trigger_raw:
        errors.append("Weekly economy triggers do not read faction law tax modifiers")
    if "script_sod_law_can_enact_for_faction" not in pres_raw:
        errors.append("SoD law presentation still bypasses central enactment rules")
    if "script_sod_law_store_block_reason_text" not in pres_raw:
        errors.append("SoD law presentation does not explain blocked enactment rules")
    if "script_sod_law_add_to_faction" not in pres_raw or "script_sod_law_remove_from_faction" not in pres_raw:
        errors.append("SoD law presentation still bypasses faction law add/remove APIs")
    if "mnu_realm_law_report" not in menu_raw or "script_sod_law_describe_realm_law_report" not in menu_raw:
        errors.append("SoD law framework is missing the realm/foreign law report menu")

    laws_with_effects = set(re.findall(r"eq,\s*\":law\",\s*(sod_law_[a-z0-9_]+)", script_raw))
    expected_effects = {
        name
        for name, value in re.findall(r"(?m)^(sod_law_[a-z0-9_]+)\s*=\s*([0-9]+)\b", constants_raw)
        if name
        not in {
            "sod_law_none",
            "sod_law_spacer_villagers",
            "sod_law_spacer_townspeople",
            "sod_law_spacer_clergy",
        }
        and not name.startswith("sod_law_ai_tag_")
        and not name.startswith("sod_law_block_")
        and not name.startswith("sod_law_category_")
        and not name.endswith("_min")
        and not name.endswith("_max")
        and name not in {"sod_law_max_active", "sod_laws_begin", "sod_laws_end"}
        and value not in {"0", "10", "20", "30"}
    }
    missing_effects = sorted(expected_effects - laws_with_effects)
    if missing_effects:
        warnings.append("SoD law framework has named laws without explicit effect branches: " + ", ".join(missing_effects[:20]))

    report_path = DOCS_REPORTS / "sod_law_audit_report.txt"
    report_lines = [
        "SoD Law Framework Audit",
        "",
        "Model: faction-owned active laws with player legacy trp_law mirror",
        "Definitions: module-script branch tables",
        "Active slots: faction_laws_begin..faction_laws_end",
        "Compatibility wrappers: law_is_active, activate_law, deactivate_law",
        "Modifier model: clear and recalculate from active laws",
        "NPC support: weekly AI scoring and cooldown processing for active kingdoms",
        "Presentation: calls central can/add/remove APIs",
        "Reports: in-game realm/foreign law report plus doctor artifacts",
        "",
        f"Named real laws expected: {len(real_law_ids)}",
        f"Effect branches found: {len(laws_with_effects)}",
        f"Law audit missing effect branches: {len(missing_effects)}",
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    snapshot_path = DOCS_REPORTS / "sod_law_faction_snapshot.json"
    snapshot = {
        "active_law_slots": [f"slot_faction_law_{i}" for i in range(1, 11)],
        "compatibility": {
            "legacy_player_troop": "trp_law",
            "legacy_scripts": ["law_is_active", "activate_law", "deactivate_law"],
        },
        "diagnostics": {
            "required_scripts": required_scripts,
            "required_constants": required_constants,
            "conflict_pairs": conflict_pairs,
            "missing_effect_branches": missing_effects,
        },
        "reports": {
            "text": report_path.relative_to(ROOT).as_posix(),
        },
    }
    snapshot_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _check_quest_authoring_dsl(errors: List[str], warnings: List[str]) -> None:
    try:
        from src.quests.quest_schema import (
            ambush_quest,
            delivery_quest,
            diplomacy_quest,
            escort_quest,
            hunt_quest,
            investigation_quest,
            quest_branch,
            quest_chain,
            quest_failure_bundle,
            quest_optional_stage,
            quest_repeatable_stage,
            quest_reward_bundle,
            quest_timed_stage,
            rescue_quest,
            siege_quest,
        )
    except Exception as exc:
        errors.append(f"Quest authoring DSL failed to import: {exc}")
        return

    try:
        rewards = quest_reward_bundle("dsl_smoke_rewards", gold=250, xp=150, renown=1)
        failures = quest_failure_bundle("dsl_smoke_failures", relation=-1, cooldown_days=3)
        optional = quest_optional_stage(
            "optional_clue",
            "Find an optional clue",
            "Search for an extra clue.",
            rewards=rewards[:1],
        )
        timed = quest_timed_stage(
            "timed_delivery",
            "Deliver before nightfall",
            "Complete the delivery before the deadline.",
            duration_hours=12,
            failures=failures[:1],
            transitions=(quest_branch("timeout", "failed", condition="timed_out"),),
        )
        repeatable = quest_repeatable_stage(
            "repeat_patrol",
            "Patrol the road",
            "Patrol the road until it is safe.",
            max_repeats=2,
            repeat_cooldown_days=1,
        )
        chain = quest_chain(
            "dsl_smoke_chain",
            "DSL Smoke Chain",
            quests=(
                delivery_quest("dsl_delivery_smoke", "dispatches", "the next town", rewards=rewards),
                hunt_quest("dsl_hunt_smoke", "road thieves"),
                escort_quest("dsl_escort_smoke", "the envoy", "the border post"),
                rescue_quest("dsl_rescue_smoke", "the captured scout"),
                siege_quest("dsl_siege_smoke", "Greywall", role="scouting"),
                diplomacy_quest("dsl_diplomacy_smoke", "Lord Harven"),
                ambush_quest("dsl_ambush_smoke", "the toll captain"),
                investigation_quest("dsl_investigation_smoke", "the missing ledgers"),
            ),
            metadata={
                "optional_stage": optional.to_snapshot(),
                "timed_stage": timed.to_snapshot(),
                "repeatable_stage": repeatable.to_snapshot(),
            },
        )
        chain.validate()
    except Exception as exc:
        errors.append(f"Quest authoring DSL smoke test failed: {exc}")


def _scan_quest_id_locations(quest_files: List[Path]) -> Dict[str, List[Tuple[Path, int, str]]]:
    locations: Dict[str, List[Tuple[Path, int, str]]] = {}
    patterns = [
        ("legacy_tuple", re.compile(r'^\s*\(\s*"([a-z][a-z0-9_]*)"\s*,')),
        ("template_spec", re.compile(r'\bquest_template_spec\(\s*"([a-z][a-z0-9_]*)"')),
        ("dsl_template", re.compile(r'\b(?:delivery_quest|hunt_quest|escort_quest|rescue_quest|siege_quest|diplomacy_quest|ambush_quest|investigation_quest|quest_blueprint|quest_template)\(\s*"([a-z][a-z0-9_]*)"')),
    ]
    for fp in quest_files:
        if "_preamble" in fp.parts:
            continue
        if fp.name.startswith("quest_"):
            continue
        raw = _read_text(fp)
        if "QUESTS" not in raw:
            continue
        for line_no, line in enumerate(raw.splitlines(), start=1):
            for source_kind, pattern in patterns:
                match = pattern.search(line)
                if not match:
                    continue
                quest_id = match.group(1)
                locations.setdefault(quest_id, []).append((fp, line_no, source_kind))
    return locations


def _write_quest_diagnostics_report(
    quest_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    report_path = DOCS_REPORTS / "quest_diagnostics_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)

    lines = [
        "Quest Diagnostics Report",
        "========================",
        "",
        "Purpose: Phase 8 validation surface for quest IDs, stage graphs, branches, DSL helpers, dynamic generation configs, and cross-fragment conflicts.",
        "",
    ]

    locations = _scan_quest_id_locations(quest_files)
    duplicate_locations = {
        quest_id: locs
        for quest_id, locs in locations.items()
        if len(locs) > 1
    }

    lines.extend(
        [
            "Source Line Map",
            "---------------",
            f"- Quest IDs with source locations: {len(locations)}",
            f"- Cross-fragment duplicate/conflict groups: {len(duplicate_locations)}",
            "",
        ]
    )
    for quest_id in sorted(locations):
        sample = "; ".join(
            f"{fp.relative_to(ROOT).as_posix()}:{line_no} ({kind})"
            for fp, line_no, kind in locations[quest_id][:8]
        )
        if len(locations[quest_id]) > 8:
            sample += f"; ... (+{len(locations[quest_id]) - 8})"
        lines.append(f"- {quest_id}: {sample}")

    lines.extend(["", "Conflict Report", "---------------"])
    if duplicate_locations:
        for quest_id, locs in sorted(duplicate_locations.items()):
            location_text = "; ".join(f"{fp.relative_to(ROOT).as_posix()}:{line_no}" for fp, line_no, _ in locs)
            message = f"[QUEST-DUP] Duplicate quest id {quest_id!r}: {location_text}"
            errors.append(message)
            lines.append(f"- ERROR {message}")
    else:
        lines.append("- No duplicate quest IDs found across quest fragments.")

    narrative_helpers = {
        "record_event": SRC_SCRIPTS / "ZG_quests" / "sod_quest_dialogue_record_event.py",
        "read_memory": SRC_SCRIPTS / "ZG_quests" / "sod_quest_dialogue_read_memory.py",
        "describe_stage": SRC_SCRIPTS / "ZG_quests" / "sod_quest_dialogue_describe_stage.py",
        "describe_reaction": SRC_SCRIPTS / "ZG_quests" / "sod_quest_dialogue_describe_reaction.py",
        "describe_battle_line": SRC_SCRIPTS / "ZG_quests" / "sod_quest_dialogue_describe_battle_line.py",
    }
    narrative_dialogues = {
        "lord_start": SRC_DIALOGS / "ZA01_startup_and_dispatch" / "anyone_lord_start_quest_memory.py",
        "member_chat": SRC_DIALOGS / "ZA01_startup_and_dispatch" / "anyone_member_chat_quest_memory.py",
        "battle_reason": SRC_DIALOGS / "ZD01_encounters_battles_and_prisoners" / "anyone_plyr_battle_reason_quest_memory.py",
    }
    lines.extend(["", "Narrative Surface", "-----------------"])
    missing_helpers = []
    for label, path in narrative_helpers.items():
        present = path.exists()
        lines.append(f"- helper {label}: {'present' if present else 'missing'} ({path.relative_to(ROOT).as_posix()})")
        if not present:
            missing_helpers.append(label)
    missing_dialogues = []
    for label, path in narrative_dialogues.items():
        present = path.exists()
        lines.append(f"- dialogue {label}: {'present' if present else 'missing'} ({path.relative_to(ROOT).as_posix()})")
        if not present:
            missing_dialogues.append(label)
    if missing_helpers:
        warnings.append(f"Quest narrative helper coverage is incomplete: {', '.join(sorted(missing_helpers))}")
        lines.append(f"- WARNING helper coverage incomplete: {', '.join(sorted(missing_helpers))}")
    if missing_dialogues:
        warnings.append(f"Quest narrative dialogue coverage is incomplete: {', '.join(sorted(missing_dialogues))}")
        lines.append(f"- WARNING dialogue coverage incomplete: {', '.join(sorted(missing_dialogues))}")

    try:
        from src.quests.quest_diagnostics import (
            QuestDiagnosticsReport,
            quest_graph_dot,
            quest_graph_mermaid,
            quest_graph_report_json,
            validate_dynamic_generation_templates,
            validate_quest_chain_graph,
        )
        from src.quests.quest_generation import DEFAULT_DYNAMIC_QUEST_TEMPLATES
        from src.quests.quest_schema import (
            delivery_quest,
            hunt_quest,
            quest_battle_objective,
            quest_branch,
            quest_chain,
            quest_optional_stage,
            quest_reward_bundle,
            quest_stage,
            quest_template,
            quest_timed_stage,
        )
    except Exception as exc:
        errors.append(f"Quest diagnostics failed to import validation helpers: {exc}")
        lines.extend(["", "Diagnostic Helper Import", "------------------------", f"- ERROR {exc}"])
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    diagnostics_report = QuestDiagnosticsReport()
    graph_items = []
    diagnostics_report.extend(
        validate_dynamic_generation_templates(
            DEFAULT_DYNAMIC_QUEST_TEMPLATES,
            source="src/quests/quest_generation.py",
        )
    )
    try:
        rewards = quest_reward_bundle("diagnostics_rewards", gold=100, xp=50)
        optional_stage = quest_optional_stage(
            "diagnostics_optional",
            "Optional clue",
            "Find an optional clue.",
            rewards=rewards,
        )
        timed_stage = quest_timed_stage(
            "diagnostics_timed",
            "Timed errand",
            "Finish before the timer expires.",
            duration_hours=8,
            transitions=(quest_branch("success", "completed"), quest_branch("late", "failed", condition="timed_out")),
        )
        chain = quest_chain(
            "diagnostics_chain",
            "Diagnostics Chain",
            quests=(
                delivery_quest(
                    "diagnostics_delivery",
                    "sealed orders",
                    "the watch post",
                    rewards=rewards,
                    metadata={"diagnostics_stage": optional_stage.to_snapshot()},
                ),
                quest_template(
                    "diagnostics_hunt",
                    "Hunt the road thieves",
                    0,
                    "Track down and defeat the road thieves.",
                    stages=(
                        quest_stage(
                            "diagnostics_hunt_stage_1",
                            "Track and defeat the target",
                            "Find and defeat the road thieves.",
                            battle_objective=quest_battle_objective(
                                "diagnostics_hunt_stage_1_objective",
                                "kill_target",
                                target_troop_id="trp_road_thief",
                            ),
                            metadata={"terminal": True},
                        ),
                    ),
                    metadata={"diagnostics_stage": timed_stage.to_snapshot()},
                ),
            ),
            branches={"main": ("diagnostics_delivery", "diagnostics_hunt")},
        )
        diagnostics_report.extend(
            validate_quest_chain_graph(
                chain,
                source="doctor:quest_diagnostics_smoke",
            )
        )
        graph_items.append(chain)
    except Exception as exc:
        diagnostics_report.add(
            __import__("src.quests.quest_diagnostics", fromlist=["QuestDiagnostic"]).QuestDiagnostic(
                severity="error",
                code="diagnostics_smoke",
                message=f"Quest diagnostics smoke chain failed: {exc}",
                source="doctor:quest_diagnostics_smoke",
            )
        )

    lines.extend(["", "Domain Validation", "-----------------"])
    lines.extend(diagnostics_report.to_lines())

    for diagnostic in diagnostics_report.errors:
        errors.append(f"[QUEST-DIAG] {diagnostic.format()}")
    for diagnostic in diagnostics_report.warnings:
        warnings.append(f"[QUEST-DIAG] {diagnostic.format()}")

    if graph_items:
        graph_json_path = DOCS_REPORTS / "quest_graph_report.json"
        graph_mmd_path = DOCS_REPORTS / "quest_graph_report.mmd"
        graph_dot_path = DOCS_REPORTS / "quest_graph_report.dot"
        graph_json_path.write_text(
            json.dumps(quest_graph_report_json(graph_items, diagnostics_report.diagnostics), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        graph_mmd_path.write_text("\n".join(quest_graph_mermaid(item).rstrip() for item in graph_items) + "\n", encoding="utf-8")
        graph_dot_path.write_text("\n".join(quest_graph_dot(item).rstrip() for item in graph_items) + "\n", encoding="utf-8")
        lines.extend(
            [
                "",
                "Graph Artifacts",
                "---------------",
                f"- JSON: {graph_json_path.relative_to(ROOT).as_posix()}",
                f"- Mermaid: {graph_mmd_path.relative_to(ROOT).as_posix()}",
                f"- Graphviz DOT: {graph_dot_path.relative_to(ROOT).as_posix()}",
            ]
        )

    lines.extend(
        [
            "",
            "Validation Layers Covered",
            "-------------------------",
            "- Identifier validation",
            "- Duplicate quest ID validation with source line mapping",
            "- Duplicate stage ID validation",
            "- Missing stage link and invalid transition validation",
            "- Unreachable stage warnings",
            "- Invalid reward/failure/condition/action expression diagnostics",
            "- Impossible dynamic generation config detection",
            "- Cross-fragment conflict report",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_quest_engine_integration(
    script_files: List[Path],
    trigger_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    scripts_by_name = {p.name for p in script_files}
    required_scripts = {
        "sod_quest_runtime_init_metadata.py",
        "sod_quest_runtime_accept.py",
        "sod_quest_runtime_update.py",
        "sod_quest_runtime_complete.py",
        "sod_quest_runtime_fail.py",
        "sod_quest_runtime_abort.py",
        "sod_quest_event_dispatch.py",
        "sod_quest_dispatch_active_event.py",
        "sod_quest_runtime_daily_update.py",
    }
    missing_scripts = sorted(required_scripts - scripts_by_name)
    for script_name in missing_scripts:
        errors.append(f"Quest engine integration missing script fragment: {script_name}")

    script_raw = "\n".join(_read_text(p) for p in script_files)
    required_calls = {
        "script_sod_quest_runtime_accept",
        "script_sod_quest_runtime_complete",
        "script_sod_quest_runtime_fail",
        "script_sod_quest_runtime_abort",
        "script_sod_quest_event_dispatch",
        "script_sod_quest_dispatch_active_event",
        "script_sod_quest_runtime_init_metadata",
    }
    for call_name in sorted(required_calls):
        if call_name not in script_raw:
            errors.append(f"Quest engine integration missing call/reference: {call_name}")

    trigger_raw = "\n".join(_read_text(p) for p in trigger_files)
    if "script_sod_quest_runtime_daily_update" not in trigger_raw:
        errors.append("Quest engine integration missing daily runtime update trigger")

    report_path = DOCS_REPORTS / "quest_engine_integration_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "Quest Engine Integration Report",
        "===============================",
        "",
        "Purpose: Phase 9 bridge from Python quest models into Warband script/slot/event behavior.",
        "",
        "Engine Adapter Scripts",
        "----------------------",
    ]
    for script_name in sorted(required_scripts):
        status = "OK" if script_name in scripts_by_name else "MISSING"
        lines.append(f"- {status}: {script_name}")
    lines.extend(
        [
            "",
            "Hook Coverage",
            "-------------",
            "- Acceptance: script_start_quest calls script_sod_quest_runtime_accept.",
            "- Completion: script_succeed_quest and script_end_quest call runtime completion adapters.",
            "- Failure/abort: script_fail_quest, script_abort_quest, and script_cancel_quest call runtime failure/abort adapters.",
            "- Battle hooks: game_event_battle_end dispatches sod_quest_event_battle.",
            "- Map encounter hooks: game_event_party_encounter dispatches sod_quest_event_map_encounter.",
            "- Center visit hooks: game_event_party_encounter dispatches sod_quest_event_center_visit for centers.",
            "- Trigger hooks: ST03_daily/entry_0152.py calls script_sod_quest_runtime_daily_update.",
            "",
            "Generated Runtime Metadata",
            "--------------------------",
            "- Quest tuples remain generated by build/build_quests.py.",
            "- Runtime state uses slot_quest_sod_runtime_* slots for state, stage, event, actor, party, center, day, progress, target, and metadata.",
            "- Event constants use sod_quest_event_* values for acceptance, update, completion, failure, dialogue, mission, trigger, battle, map encounter, center visit, movement, and time.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_modernization_tooling_guards(
    script_files: List[Path],
    dialog_files: List[Path],
    menu_files: List[Path],
    trigger_files: List[Path],
    presentation_files: List[Path],
    mission_template_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    """Pin the modernization-era safety checks in Doctor output.

    The focused static tests remain the detailed graph walker. Doctor owns the
    build-facing contract: key guard helpers, order-file coverage, unsafe exit
    patterns, callback compatibility, and high-frequency party-id hazards must
    stay visible during normal builds.
    """
    script_raw = "\n".join(_read_text(p) for p in script_files)
    dialog_raw = "\n".join(_read_text(p) for p in dialog_files)
    menu_raw = "\n".join(_read_text(p) for p in menu_files)
    trigger_raw = "\n".join(_read_text(p) for p in trigger_files)
    presentation_raw = "\n".join(_read_text(p) for p in presentation_files)
    mission_raw = "\n".join(_read_text(p) for p in mission_template_files)
    all_raw = "\n".join((script_raw, dialog_raw, menu_raw, trigger_raw, presentation_raw, mission_raw))

    required_tokens = {
        "dialogue graph safety static guard": "test_dialogue_outputs_have_matching_inputs_or_safe_terminals",
        "unsafe post-mission return static guard": "test_generic_continue_menus_do_not_only_change_screen_return",
        "high-frequency party safety static guard": "test_high_frequency_ai_scripts_do_not_use_unguarded_global_party_ops",
        "camp/report fallback static guard": "test_report_menus_call_description_scripts_and_use_fallbacks",
        "quest sentinel/order static guard": "test_quest_end_sentinel_is_isolated_and_last",
        "M&B 1.011 callback static guard": "test_warband_presentation_callbacks_are_absent_for_mb1011",
    }
    modernization_static_path = ROOT / "build" / "test_modernization_static.py"
    modernization_static = _read_text(modernization_static_path) if modernization_static_path.exists() else ""
    if not modernization_static:
        errors.append("[MODERNIZATION] Missing build/test_modernization_static.py top-level guard.")
    for label, token in required_tokens.items():
        if token not in modernization_static:
            errors.append(f"[MODERNIZATION] Missing {label}: {token}")

    required_runtime_tokens = {
        "safe encounter cleanup helper": "script_sod_safe_leave_encounter",
        "safe active party helper": "sod_party_is_safe_active_to_reg",
        "center fallback helper": "script_sod_store_center_name_or_fallback_to_s21",
        "company incident focus helper": "script_sod_company_dialogue_store_incident_focus",
        "trade route pressure helper": "script_sod_trade_network_get_route_pressure_to_regs",
    }
    for label, token in required_runtime_tokens.items():
        if token not in all_raw:
            errors.append(f"[MODERNIZATION] Missing {label}: {token}")

    presentations_order_path = ROOT / "src" / "presentations" / "_order_presentations.txt"
    presentations_order = _read_text(presentations_order_path) if presentations_order_path.exists() else ""
    presentation_ids_path = ROOT / "compile" / "ids" / "ID_presentations.py"
    presentation_ids = _read_text(presentation_ids_path) if presentation_ids_path.exists() else ""
    presentation_stub_rel = "9999_mb1011_game_presentation_stubs/game_presentation_stubs.py"
    presentation_stub_path = ROOT / "src" / "presentations" / presentation_stub_rel
    presentation_raw = "\n".join(_read_text(p) for p in presentation_files)
    if "0000_game_hardcoded_callbacks" in presentations_order:
        errors.append("[MODERNIZATION] M&B 1.011 should not register Warband-only game_start/game_escape presentation callbacks.")
    if presentation_stub_rel in presentations_order or presentation_stub_path.exists():
        errors.append("[MODERNIZATION] Remove the old inert prsnt_game_start/prsnt_game_escape tail stub; M&B 1.011 logs UNABLE TO MAP when these callbacks are exported.")
    if '"game_start"' in presentation_raw or '"game_escape"' in presentation_raw:
        errors.append("[MODERNIZATION] Warband-only prsnt_game_start/prsnt_game_escape callbacks must stay absent from M&B 1.011 presentations.")
    if presentation_ids and (
        "prsnt_game_credits = 0" not in presentation_ids
        or "prsnt_banner_selection = 1" not in presentation_ids
    ):
        warnings.append("[MODERNIZATION] Generated presentation IDs do not yet reflect Original SoD presentation order; rebuild export and run static callback tests.")
    if presentation_ids and (
        "prsnt_game_start" in presentation_ids
        or "prsnt_game_escape" in presentation_ids
        or "prsnt_game_credits = 0" not in presentation_ids
        or "prsnt_banner_selection = 1" not in presentation_ids
    ):
        errors.append("[MODERNIZATION] Original SoD presentation order must keep prsnt_game_credits = 0, prsnt_banner_selection = 1, and omit Warband-only game_start/game_escape callbacks.")

    if "game_check_party_sees_party" not in script_raw or "game_get_party_speed_multiplier" not in script_raw:
        errors.append("[MODERNIZATION] M&B 1.011 hardcoded game script compatibility fragments are missing.")

    unsafe_continue_menus: List[str] = []
    for path in menu_files:
        raw = _read_text(path)
        if (
            "change_screen_return" in raw
            and ("finish_mission" in raw or "start_mission" in raw)
            and "jump_to_menu" not in raw
            and "change_screen_map" not in raw
        ):
            unsafe_continue_menus.append(path.relative_to(ROOT).as_posix())
    if unsafe_continue_menus:
        errors.append(
            "[MODERNIZATION] Menu fragment(s) use change_screen_return without explicit menu/map exit: "
            + ", ".join(unsafe_continue_menus[:20])
        )

    party_hazard_tokens = (
        "store_distance_to_party_from_party",
        "store_faction_of_party",
        "$g_encountered_party",
        "$g_enemy_party",
        "$g_talk_troop_party",
    )
    if any(token in all_raw for token in party_hazard_tokens) and "sod_party_is_safe_active_to_reg" not in all_raw:
        errors.append("[MODERNIZATION] Party-id hazard operations exist without the safe active party helper.")

    report_path = DOCS_REPORTS / "builder_doctor_tooling_audit.md"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Builder, Doctor, And Tooling Audit",
        "",
        "## Doctor Coverage",
        "",
        "- Dialogue graph input/output validity is pinned through `build/test_modernization_static.py` and surfaced by Doctor as a required modernization guard.",
        "- Unsafe post-mission `change_screen_return` patterns are checked in static coverage and Doctor flags source menu fragments that rely on return without explicit menu/map exits.",
        "- High-frequency party operations are guarded by the shared active-party helper and static coverage.",
        "- M&B 1.011 hardcoded callback compatibility is pinned by Original SoD presentation order and static coverage.",
        "- Stale order-file entries remain hard Doctor errors through manifest completeness checks.",
        "- Duplicate top-level IDs and duplicate dialogue heads remain Doctor-owned checks.",
        "",
        "## Static Coverage",
        "",
    ]
    for label, token in required_tokens.items():
        status = "present" if token in modernization_static else "missing"
        lines.append(f"- {status}: {label} (`{token}`)")
    lines.extend(
        [
            "",
            "## Runtime Helper Coverage",
            "",
        ]
    )
    for label, token in required_runtime_tokens.items():
        status = "present" if token in all_raw else "missing"
        lines.append(f"- {status}: {label} (`{token}`)")
    lines.extend(
        [
            "",
            "## Manual QA",
            "",
            "- [ ] Run Doctor after deleting a listed order-file fragment and confirm the stale manifest error is clear.",
            "- [ ] Run Doctor after adding an unsafe `change_screen_return`-only menu fragment and confirm the modernization error is clear.",
            "- [ ] Run Doctor after registering `prsnt_game_start` or `prsnt_game_escape` and confirm M&B 1.011 callback coverage catches it.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_quest_battle_integration(
    script_files: List[Path],
    mission_template_files: List[Path],
    constant_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    scripts_by_name = {p.name for p in script_files}
    required_scripts = {
        "sod_quest_battle_action_set.py",
        "sod_quest_battle_message.py",
        "sod_quest_battle_advance_action.py",
        "sod_quest_battle_mission_start.py",
        "sod_quest_battle_agent_defeated.py",
        "sod_quest_battle_scan_agents.py",
        "sod_quest_battle_tick.py",
        "sod_quest_battle_note_prisoner_freed.py",
        "sod_quest_battle_note_target_captured.py",
    }
    for script_name in sorted(required_scripts - scripts_by_name):
        errors.append(f"Quest battle integration missing script fragment: {script_name}")

    constants_raw = "\n".join(_read_text(p) for p in constant_files)
    required_constants = {
        "sod_quest_battle_action_kill_target",
        "sod_quest_battle_action_capture_target",
        "sod_quest_battle_action_protect_target",
        "sod_quest_battle_action_survive_timer",
        "sod_quest_battle_action_break_siege_line",
        "sod_quest_battle_action_hold_position",
        "sod_quest_battle_action_destroy_force",
        "sod_quest_battle_action_escort_during_battle",
        "sod_quest_battle_action_free_prisoner",
        "sod_quest_battle_action_rescue_allied_captain",
        "sod_quest_battle_action_defeat_wave",
        "slot_quest_sod_battle_action",
        "slot_quest_sod_battle_progress",
        "slot_quest_sod_battle_timer_duration",
    }
    for const_name in sorted(required_constants):
        if const_name not in constants_raw:
            errors.append(f"Quest battle integration missing constant: {const_name}")

    mt_raw = "\n".join(_read_text(p) for p in mission_template_files)
    for token in (
        "quest_battle_agent_defeated",
        "quest_battle_tick",
        "script_sod_quest_battle_mission_start",
        "script_sod_quest_battle_scan_agents",
    ):
        if token not in mt_raw:
            errors.append(f"Quest battle integration missing mission-template hook: {token}")

    script_raw = "\n".join(_read_text(p) for p in script_files)
    for token in (
        "script_sod_quest_battle_note_prisoner_freed",
        "script_sod_quest_battle_note_target_captured",
        "script_sod_quest_battle_advance_action",
    ):
        if token not in script_raw:
            errors.append(f"Quest battle integration missing script call/reference: {token}")

    report_path = DOCS_REPORTS / "quest_battle_integration_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "Quest Battle Integration Report",
        "===============================",
        "",
        "Purpose: Phase 10 generalized battle-aware quest objective layer.",
        "",
        "Supported Actions",
        "-----------------",
        "- kill target",
        "- capture target",
        "- protect target",
        "- survive timer",
        "- break siege line",
        "- hold position",
        "- destroy force",
        "- escort during battle",
        "- free prisoner during mission",
        "- rescue allied captain",
        "- defeat wave objective",
        "",
        "Engine Hooks",
        "------------",
        "- lead_charge calls script_sod_quest_battle_mission_start at mission start.",
        "- lead_charge includes quest_battle_agent_defeated, a normal-M&B-safe scan trigger that detects defeated agents through slot_agent_is_alive_before_retreat.",
        "- lead_charge includes quest_battle_tick for timer, hold, escort, siege-line, and rescue-style objectives.",
        "- script_remove_troop_from_prison dispatches free-prisoner quest battle progress.",
        "- script_event_hero_taken_prisoner_by_player dispatches capture-target quest battle progress.",
        "",
        "Authoring Contract",
        "------------------",
        "- Call script_sod_quest_battle_action_set with quest, action type, target troop, required count, and timer duration.",
        "- Progress is stored in slot_quest_sod_battle_progress and mirrored into runtime event metadata.",
        "- Completion advances the runtime stage and emits sod_quest_event_mission.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_quest_journal_integration(
    script_files: List[Path],
    menu_files: List[Path],
    constant_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    scripts_by_name = {p.name for p in script_files}
    required_scripts = {
        "sod_quest_journal_set_flags.py",
        "sod_quest_journal_mark_pinned.py",
        "sod_quest_journal_update.py",
        "sod_quest_journal_describe_to_s2.py",
    }
    for script_name in sorted(required_scripts - scripts_by_name):
        errors.append(f"Quest journal integration missing script fragment: {script_name}")

    constants_raw = "\n".join(_read_text(p) for p in constant_files)
    for const_name in (
        "slot_quest_sod_journal_flags",
        "slot_quest_sod_journal_priority",
        "slot_quest_sod_journal_category",
        "sod_quest_journal_capacity_default",
        "sod_quest_journal_flag_pinned",
        "sod_quest_journal_flag_main",
        "sod_quest_journal_flag_side",
        "sod_quest_journal_flag_urgent",
    ):
        if const_name not in constants_raw:
            errors.append(f"Quest journal integration missing constant: {const_name}")

    quest_menu_path = SRC_MENUS / "reports" / "quest_journal_report.py"
    reports_menu_path = SRC_MENUS / "0000_hardcoded_mb1011" / "reports.py"
    update_path = SRC_SCRIPTS / "ZG_quests" / "sod_quest_journal_update.py"
    describe_path = SRC_SCRIPTS / "ZG_quests" / "sod_quest_journal_describe_to_s2.py"

    def _read_required(path: Path) -> str:
        if not path.exists():
            errors.append(f"Quest journal integration missing source file: {path.relative_to(ROOT).as_posix()}")
            return ""
        return _read_text(path)

    quest_menu_raw = _read_required(quest_menu_path)
    reports_menu_raw = _read_required(reports_menu_path)
    update_raw = _read_required(update_path)
    describe_raw = _read_required(describe_path)
    script_raw = "\n".join(_read_text(p) for p in script_files)

    check_results: List[Tuple[str, bool, Path, List[str]]] = []

    def record_check(label: str, path: Path, text: str, tokens: Tuple[str, ...]) -> None:
        missing = [token for token in tokens if token not in text]
        passed = not missing
        check_results.append((label, passed, path, list(tokens)))
        if missing:
            errors.append(
                f"Quest journal integration missing {label} token(s) in {path.relative_to(ROOT).as_posix()}: "
                + ", ".join(missing)
            )

    record_check(
        "camp report route",
        reports_menu_path,
        reports_menu_raw,
        ("view_quest_journal_report", "mnu_quest_journal_report"),
    )
    record_check(
        "journal shell route",
        quest_menu_path,
        quest_menu_raw,
        ("mnu_quest_journal_report",),
    )
    record_check(
        "journal shell refresh",
        quest_menu_path,
        quest_menu_raw,
        ("script_sod_quest_journal_update", "script_sod_quest_journal_describe_to_s2"),
    )
    record_check(
        "journal shell back option",
        quest_menu_path,
        quest_menu_raw,
        ("quest_journal_report_back",),
    )
    record_check(
        "presentation refresh call",
        describe_path,
        describe_raw,
        ('call_script, "script_sod_quest_journal_update"', "str_clear, s2"),
    )
    record_check(
        "presentation section headings",
        describe_path,
        describe_raw,
        ("Companion Personal Arcs", "Active Quests", "Completed Archive", "Failed Archive"),
    )
    record_check(
        "runtime summary refresh",
        update_path,
        update_raw,
        (
            "sod_quest_journal_capacity_default",
            "slot_quest_sod_runtime_state",
            "slot_quest_sod_runtime_stage",
            "slot_quest_sod_journal_chain_progress",
            "slot_quest_sod_journal_archive_day",
        ),
    )
    record_check(
        "runtime priority flags",
        update_path,
        update_raw,
        (
            "sod_quest_journal_flag_pinned",
            "sod_quest_journal_flag_main",
            "sod_quest_journal_flag_side",
            "sod_quest_journal_flag_urgent",
        ),
    )
    record_check(
        "default classification call",
        SRC_SCRIPTS / "ZG_quests" / "sod_quest_journal_set_flags.py",
        script_raw,
        ("script_sod_quest_journal_set_flags",),
    )
    record_check(
        "runtime output register",
        describe_path,
        describe_raw,
        ("str_store_string, s2",),
    )

    report_path = DOCS_REPORTS / "quest_journal_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)

    def _check_status(label: str) -> str:
        for recorded_label, passed, _, _ in check_results:
            if recorded_label == label:
                return "PASS" if passed else "FAIL"
        return "UNKNOWN"

    lines = [
        "Quest Journal Integration Report",
        "================================",
        "",
        "Purpose: Phase 11 quest journal and concurrency layer.",
        "",
        "Verified Chain",
        "--------------",
        "- Camp reports entry: view_quest_journal_report -> mnu_quest_journal_report",
        "- Journal screen shell: mnu_quest_journal_report -> script_sod_quest_journal_update -> script_sod_quest_journal_describe_to_s2",
        "- Back navigation: quest_journal_report_back -> mnu_camp_reports",
        "- Runtime summary source: slot_quest_sod_runtime_state/stage, slot_quest_sod_journal_chain_progress, slot_quest_sod_journal_archive_day",
        "",
        "Player-Facing Journal Presentation",
        "-----------------------------------",
        "- Active log section for tracked quests.",
        "- Priority markers for pinned, main, side, and urgent quests.",
        "- Visible stage and chain progress for each entry.",
        "- Archive sections for completed and failed quests.",
        "",
        "Source Evidence",
        "---------------",
        f"- camp report route: {_check_status('camp report route')}",
        f"- journal shell route: {_check_status('journal shell route')}",
        f"- journal shell refresh: {_check_status('journal shell refresh')}",
        f"- journal shell back option: {_check_status('journal shell back option')}",
        f"- presentation refresh call: {_check_status('presentation refresh call')}",
        f"- presentation section headings: {_check_status('presentation section headings')}",
        f"- runtime summary refresh: {_check_status('runtime summary refresh')}",
        f"- runtime priority flags: {_check_status('runtime priority flags')}",
        f"- default classification call: {_check_status('default classification call')}",
        f"- runtime output register: {_check_status('runtime output register')}",
        "",
        "Source Files",
        "------------",
        f"- {reports_menu_path.relative_to(ROOT).as_posix()}",
        f"- {quest_menu_path.relative_to(ROOT).as_posix()}",
        f"- {describe_path.relative_to(ROOT).as_posix()}",
        f"- {update_path.relative_to(ROOT).as_posix()}",
        "",
        "Journal Features",
        "----------------",
        "- Active quest count and recommended capacity.",
        "- Pinned quest marker support.",
        "- Main, side, and urgent quest category slots.",
        "- Completed and failed archive counters.",
        "- Expiration warning count.",
        "- Stage and chain progress slots for migrated quest chains.",
        "",
        "Engine Hooks",
        "------------",
        "- New accepted quests default to side quest classification.",
        "- Completion/failure adapters update archive category and archive day.",
        "- Journal update script refreshes counters from native quest state and structured runtime slots.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_quest_branching_integration(
    script_files: List[Path],
    constant_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    scripts_by_name = {p.name for p in script_files}
    required_scripts = {
        "sod_quest_chain_set.py",
        "sod_quest_chain_advance.py",
        "sod_quest_chain_apply_outcome.py",
        "sod_quest_chain_branch_success.py",
        "sod_quest_chain_branch_failure.py",
        "sod_quest_chain_branch_choice.py",
        "sod_quest_chain_branch_faction.py",
        "sod_quest_chain_alternate_ending.py",
        "sod_quest_chain_unlock_hidden.py",
        "sod_quest_chain_lock.py",
        "sod_quest_chain_reset.py",
        "sod_quest_chain_resume_due.py",
        "sod_quest_chain_describe_to_s2.py",
    }
    for script_name in sorted(required_scripts - scripts_by_name):
        errors.append(f"Quest branching integration missing script fragment: {script_name}")

    constants_raw = "\n".join(_read_text(p) for p in constant_files)
    required_constants = {
        "slot_quest_sod_chain_id",
        "slot_quest_sod_chain_step",
        "slot_quest_sod_chain_branch",
        "slot_quest_sod_chain_choice",
        "slot_quest_sod_chain_lock_state",
        "slot_quest_sod_chain_resume_day",
        "slot_quest_sod_chain_ending",
        "slot_quest_sod_chain_flags",
        "slot_quest_sod_chain_next_quest",
        "slot_quest_sod_chain_previous_quest",
        "sod_quest_chain_branch_success",
        "sod_quest_chain_branch_failure",
        "sod_quest_chain_branch_choice",
        "sod_quest_chain_branch_faction",
        "sod_quest_chain_branch_hidden",
        "sod_quest_chain_branch_alternate_ending",
        "sod_quest_chain_lock_resuming",
        "sod_quest_chain_flag_resume_pending",
    }
    for const_name in sorted(required_constants):
        if const_name not in constants_raw:
            errors.append(f"Quest branching integration missing constant: {const_name}")

    script_raw = "\n".join(_read_text(p) for p in script_files)
    for token in (
        "script_sod_quest_chain_apply_outcome",
        "script_sod_quest_chain_resume_due",
        "script_sod_quest_chain_describe_to_s2",
    ):
        if token not in script_raw:
            errors.append(f"Quest branching integration missing runtime hook/reference: {token}")

    report_path = DOCS_REPORTS / "quest_branching_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "Quest Branching Integration Report",
        "==================================",
        "",
        "Purpose: Phase 12 branching quest chain layer.",
        "",
        "Supported Chain Mechanics",
        "-------------------------",
        "- Linear chains through next-quest continuation.",
        "- Branch on success through script_sod_quest_chain_branch_success and runtime completion hooks.",
        "- Branch on failure through script_sod_quest_chain_branch_failure and runtime failure hooks.",
        "- Branch on player choice through script_sod_quest_chain_branch_choice.",
        "- Branch on faction alignment through script_sod_quest_chain_branch_faction.",
        "- Hidden branch unlocks through script_sod_quest_chain_unlock_hidden.",
        "- Alternate endings through branch/ending slots for authored content.",
        "- Chain resets through script_sod_quest_chain_reset when the resettable flag is present.",
        "- Chain lockouts through script_sod_quest_chain_lock.",
        "- Chain resume after delay through script_sod_quest_chain_resume_due.",
        "",
        "Runtime Slots",
        "-------------",
        "- slot_quest_sod_chain_id",
        "- slot_quest_sod_chain_step",
        "- slot_quest_sod_chain_branch",
        "- slot_quest_sod_chain_choice",
        "- slot_quest_sod_chain_lock_state",
        "- slot_quest_sod_chain_resume_day",
        "- slot_quest_sod_chain_ending",
        "- slot_quest_sod_chain_flags",
        "- slot_quest_sod_chain_next_quest",
        "- slot_quest_sod_chain_previous_quest",
        "",
        "Engine Hooks",
        "------------",
        "- script_sod_quest_runtime_complete applies success branch outcomes.",
        "- script_sod_quest_runtime_fail applies failure branch outcomes.",
        "- script_sod_quest_runtime_daily_update calls delayed chain resume processing.",
        "- script_sod_quest_journal_describe_to_s2 appends branch chain counters.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _check_quest_migration_strategy(
    quest_files: List[Path],
    errors: List[str],
    warnings: List[str],
) -> None:
    try:
        from src.quests.quest_migration import build_quest_migration_plan
    except Exception as exc:
        errors.append(f"Quest migration strategy failed to import: {exc}")
        return

    plan = build_quest_migration_plan(quest_files)
    report_path = DOCS_REPORTS / "quest_migration_report.txt"
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(plan.summary_lines()) + "\n", encoding="utf-8")
    if not plan.candidates:
        warnings.append("Quest migration strategy found no quest files to rank.")


def _extract_list_block(raw: str, var_name: str) -> str:
    """
    Return inner text of: VAR = [ ... ]  (handles strings + # comments)
    Raises ValueError if not found or unclosed.
    """
    # Prefer the actual list assignment line: ^VAR = [
    # This avoids false matches when var_name appears in imports/comments.
    import re
    m = re.search(rf"(?m)^\s*{re.escape(var_name)}\s*=\s*\[", raw)
    if m:
        lb = m.end() - 1
    else:
        idx = raw.find(var_name)
        if idx < 0:
            raise ValueError(f"Missing {var_name} in fragment.")
        lb = raw.find("[", idx)
        if lb < 0:
            raise ValueError(f"Missing '[' after {var_name}.")
    i = lb
    depth = 0
    in_str = False
    str_ch = ""
    esc = False
    in_comment = False

    while i < len(raw):
        ch = raw[i]

        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue

        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == str_ch:
                in_str = False
            i += 1
            continue

        if ch == "#":
            in_comment = True
            i += 1
            continue
        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            i += 1
            continue

        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return raw[lb + 1 : i].strip()
        i += 1

    raise ValueError(f"Unclosed list bracket for {var_name}.")

def _iter_top_level_tuple_ids(list_inner: str) -> List[str]:
    """Parse top-level records and return the first string element of each.

    Historically our fragments use tuples like:
        ("id", [...])

    But some classic compile/module_*.py lists (notably module_items.py) use lists like:
        ["id", "Name", ...]

    This parser supports BOTH by treating a top-level '(' OR '[' as a record start.
    It avoids false positives from nested tuples/lists (e.g., menu options "continue").
    """
    ids: List[str] = []
    i = 0
    paren_depth = 0
    bracket_depth = 0
    in_str = False
    str_ch = ""
    esc = False
    in_comment = False

    def skip_ws_and_comments(j: int) -> int:
        nonlocal in_comment
        while j < len(list_inner):
            ch2 = list_inner[j]
            if in_comment:
                if ch2 == "\n":
                    in_comment = False
                j += 1
                continue
            if ch2.isspace():
                j += 1
                continue
            if ch2 == "#":
                in_comment = True
                j += 1
                continue
            break
        return j

    while i < len(list_inner):
        ch = list_inner[i]

        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue

        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == str_ch:
                in_str = False
            i += 1
            continue

        if ch == "#":
            in_comment = True
            i += 1
            continue

        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            i += 1
            continue

        if ch in ("(", "["):
            if paren_depth == 0 and bracket_depth == 0:
                # Potential start of a top-level record -> parse first string element
                j = skip_ws_and_comments(i + 1)
                if j < len(list_inner) and list_inner[j] in ('"', "'"):
                    quote = list_inner[j]
                    j += 1
                    start_s = j
                    esc2 = False
                    while j < len(list_inner):
                        cj = list_inner[j]
                        if esc2:
                            esc2 = False
                        elif cj == "\\":
                            esc2 = True
                        elif cj == quote:
                            ids.append(list_inner[start_s:j])
                            break
                        j += 1
                # Continue scanning; we're now inside this record
            if ch == "(":
                paren_depth += 1
            else:
                bracket_depth += 1
            i += 1
            continue

        if ch == ")":
            if paren_depth > 0:
                paren_depth -= 1
            i += 1
            continue

        if ch == "]":
            if bracket_depth > 0:
                bracket_depth -= 1
            i += 1
            continue

        i += 1

    return ids


def _iter_top_level_records(list_inner: str) -> List[str]:
    """Return raw top-level tuple/list records from a list body."""
    out: List[str] = []
    start: int | None = None
    i = 0
    paren_depth = 0
    bracket_depth = 0
    in_str = False
    str_ch = ""
    esc = False
    in_comment = False

    while i < len(list_inner):
        ch = list_inner[i]

        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue

        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == str_ch:
                in_str = False
            i += 1
            continue

        if ch == "#":
            in_comment = True
            i += 1
            continue
        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            i += 1
            continue

        if ch in ("(", "["):
            if paren_depth == 0 and bracket_depth == 0:
                start = i
            if ch == "(":
                paren_depth += 1
            else:
                bracket_depth += 1
            i += 1
            continue

        if ch == ")" and paren_depth > 0:
            paren_depth -= 1
            if paren_depth == 0 and bracket_depth == 0 and start is not None:
                out.append(list_inner[start : i + 1].strip())
                start = None
            i += 1
            continue

        if ch == "]" and bracket_depth > 0:
            bracket_depth -= 1
            if paren_depth == 0 and bracket_depth == 0 and start is not None:
                out.append(list_inner[start : i + 1].strip())
                start = None
            i += 1
            continue

        i += 1

    return out


def _split_top_level_fields(record: str) -> List[str]:
    """Split a tuple/list record into top-level comma-separated fields."""
    s = record.strip()
    if len(s) < 2 or s[0] not in "([" or s[-1] not in ")]":
        return []
    s = s[1:-1]
    out: List[str] = []
    start = 0
    i = 0
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    in_str = False
    str_ch = ""
    esc = False
    in_comment = False

    while i < len(s):
        ch = s[i]
        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == str_ch:
                in_str = False
            i += 1
            continue
        if ch == "#":
            in_comment = True
            i += 1
            continue
        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            i += 1
            continue
        if ch == "(":
            paren_depth += 1
        elif ch == ")" and paren_depth > 0:
            paren_depth -= 1
        elif ch == "[":
            bracket_depth += 1
        elif ch == "]" and bracket_depth > 0:
            bracket_depth -= 1
        elif ch == "{":
            brace_depth += 1
        elif ch == "}" and brace_depth > 0:
            brace_depth -= 1
        elif ch == "," and paren_depth == 0 and bracket_depth == 0 and brace_depth == 0:
            out.append(s[start:i].strip())
            start = i + 1
        i += 1

    tail = s[start:].strip()
    if tail:
        out.append(tail)
    return out


def _record_has_only_comments_or_whitespace(text: str) -> bool:
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            return False
    return True


def _normalize_signal_hash(text: str) -> str:
    cleaned: List[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        cleaned.append(s)
    return hashlib.sha256("\n".join(cleaned).encode("utf-8", errors="replace")).hexdigest()[:12]


def _slice_list_payload(text: str) -> str:
    s = text.strip()
    if s.startswith("[") and s.endswith("]"):
        return s[1:-1]
    return s


def _is_comment_only_list(text: str) -> bool:
    return _record_has_only_comments_or_whitespace(_slice_list_payload(text))


def _record_line_no(raw: str, record: str) -> int | None:
    try:
        idx = raw.index(record)
    except ValueError:
        return None
    return raw.count("\n", 0, idx) + 1


def _check_stub_fragments(
    files: List[Path],
    export_name: str,
    warnings: List[str],
    errors: List[str],
    *,
    strict: bool,
    allowlist: List[re.Pattern] | None,
    max_examples: int = 50,
) -> None:
    """Detect fragments that export records but appear to contain placeholder logic."""
    hits: List[str] = []

    for fp in files:
        rel = fp.relative_to(ROOT).as_posix()
        if _path_is_allowlisted(rel, allowlist):
            continue
        raw = _read_text(fp)
        try:
            inner = _extract_list_block(raw, export_name)
        except Exception:
            continue

        records = _iter_top_level_records(inner)
        if not records:
            continue

        for idx, record in enumerate(records, start=1):
            fields = _split_top_level_fields(record)
            body = ""
            reason = ""
            line_no = _record_line_no(raw, record)

            if export_name == "SCRIPTS":
                ops = fields[1] if len(fields) >= 2 else ""
                body = ops
                if ops.strip() == "[]":
                    reason = "empty operation list"
                elif _is_comment_only_list(ops):
                    reason = "comment-only operation list"
                elif _STUB_MARKER_RE.search(record) and not re.search(r"\(\s*(call_script|assign|try_begin|try_for_range|store_)\b", record):
                    reason = "stub marker without meaningful operations"
            elif export_name == "SIMPLE_TRIGGERS":
                cond = fields[1] if len(fields) >= 2 else ""
                cons = fields[2] if len(fields) >= 3 else ""
                body = "\n".join([cond, cons])
                cond_empty = cond.strip() == "[]"
                cons_empty = cons.strip() == "[]"
                if cond_empty and cons_empty:
                    reason = "empty conditions and consequences"
                elif cons_empty and _is_comment_only_list(cond):
                    reason = "no effective trigger logic"
                elif _STUB_MARKER_RE.search(record) and cons_empty:
                    reason = "stub marker with empty consequences"
            elif export_name == "DIALOGS":
                cond = fields[2] if len(fields) >= 3 else ""
                cons = fields[5] if len(fields) >= 6 else ""
                body = "\n".join([cond, cons])
                cons_empty = cons.strip() == "[]"
                if _STUB_MARKER_RE.search(record) and (cons_empty or _is_comment_only_list(cons)):
                    reason = "stub marker with empty/no-op consequences"
            elif export_name == "MENUS":
                ops = fields[4] if len(fields) >= 5 else ""
                options = fields[5] if len(fields) >= 6 else ""
                body = "\n".join([ops, options])
                if ops.strip() == "[]" and options.strip() == "[]":
                    reason = "empty menu operations and options"
                elif _STUB_MARKER_RE.search(record) and (options.strip() == "[]" or _is_comment_only_list(options)):
                    reason = "stub marker with empty/no-op options"
            elif export_name == "PRESENTATIONS":
                triggers = fields[3] if len(fields) >= 4 else ""
                body = triggers
                if triggers.strip() == "[]":
                    reason = "empty trigger list"
                elif _is_comment_only_list(triggers):
                    reason = "comment-only trigger list"
                elif _STUB_MARKER_RE.search(record) and not re.search(r"\(\s*ti_", record):
                    reason = "stub marker without presentation triggers"
            elif export_name == "MISSION_TEMPLATES":
                triggers = fields[5] if len(fields) >= 6 else ""
                body = triggers
                if triggers.strip() == "[]":
                    reason = "empty trigger list"
                elif _is_comment_only_list(triggers):
                    reason = "comment-only trigger list"
                elif _STUB_MARKER_RE.search(record) and not re.search(r"\(\s*(ti_|0\s*,)", record):
                    reason = "stub marker without mission triggers"
            else:
                continue

            if not reason:
                continue

            signal = _normalize_signal_hash(body)
            loc = f":{line_no}" if line_no else ""
            hits.append(f"[STUB] {rel}{loc} [{export_name} #{idx}] {reason} (sig={signal})")
            if len(hits) >= max_examples:
                break
        if len(hits) >= max_examples:
            break

    if not hits:
        return

    target = errors if strict else warnings
    target.append(f"[STUB] Found {len(hits)} suspected stub/empty fragment record(s).")
    target.extend(hits)


def _check_exports(files: Iterable[Path], export_name: str, errors: List[str]) -> None:
    pat = _EXPORT_RE[export_name]
    for fp in files:
        raw = _read_text(fp)
        if not pat.search(raw):
            errors.append(f"[EXPORT] {export_name} missing or not assigned in: {fp}")

def _check_top_level_id_duplicates(
    files: Iterable[Path],
    export_name: str,
    errors: List[str],
    label: str,
    *,
    check_duplicates: bool = True,
    allowlist: List[re.Pattern] | None = None,
) -> int:
    """
    Extract top-level tuple ids (usually 1 per file) and check duplicates.
    Returns number of top-level entries found across all fragments.
    """
    seen: Dict[str, Path] = {}
    count = 0
    for fp in files:
        raw = _read_text(fp)
        if not _EXPORT_RE[export_name].search(raw):
            continue
        try:
            inner = _extract_list_block(raw, export_name)
        except Exception as e:
            errors.append(f"[PARSE] Failed to parse {export_name} list in {fp}: {e}")
            continue

        ids = _iter_top_level_tuple_ids(inner)
        if not ids:
            errors.append(f"[EMPTY] No top-level tuple found in {export_name} list for {fp}")
            continue

        count += len(ids)
        if check_duplicates:
            for _id in ids:
                allow_key = f"{label}:{_id}".lower()
                if allowlist and any(pat.match(allow_key) for pat in allowlist):
                    if _id not in seen:
                        seen[_id] = fp
                    continue
                if _id in seen:
                    errors.append(
                        f"[DUP] Duplicate {label} id '{_id}' in {export_name}:\n"
                        f"      first: {seen[_id]}\n"
                        f"      again: {fp}"
                    )
                else:
                    seen[_id] = fp
    return count

def _read_order_file(order_path: Path, base: Path, errors: List[str], allow_code_prefix: bool=False) -> List[str]:
    if not order_path.exists():
        errors.append(f"[ORDER] Missing order file: {order_path}")
        return []
    rels: List[str] = []
    seen: Set[str] = set()
    for ln in _read_text(order_path).splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if allow_code_prefix:
            parts = ln.split()
            rel = parts[-1]
        else:
            rel = ln
        rel = rel.replace("\\", "/")
        if rel in seen:
            errors.append(f"[ORDER] Duplicate entry in {order_path.name}: {rel}")
            continue
        seen.add(rel)
        rels.append(rel)
        p = base / rel
        if not p.exists():
            errors.append(f"[ORDER] Listed file missing: {p}")
    return rels

def _check_manifest_completeness(
    base: Path,
    files: List[Path],
    order_rels: List[str],
    errors: List[str],
    label: str
) -> None:
    existing: Set[str] = { _rel(p, base) for p in files }
    listed: Set[str] = set(order_rels)

    missing_in_manifest = sorted(existing - listed)
    extra_in_manifest = sorted(listed - existing)

    if missing_in_manifest:
        errors.append(f"[ORDER] {label}: {len(missing_in_manifest)} fragment(s) not listed in order file.")
        for m in missing_in_manifest[:25]:
            errors.append(f"        missing: {m}")
        if len(missing_in_manifest) > 25:
            errors.append(f"        ...and {len(missing_in_manifest) - 25} more")

    if extra_in_manifest:
        errors.append(f"[ORDER] {label}: {len(extra_in_manifest)} entry(s) in order file do not exist on disk.")
        for m in extra_in_manifest[:25]:
            errors.append(f"        extra: {m}")
        if len(extra_in_manifest) > 25:
            errors.append(f"        ...and {len(extra_in_manifest) - 25} more")

def _check_za_order_warning(all_scripts: List[Path], warnings: List[str], errors: List[str]) -> None:
    za_root = SRC_SCRIPTS / "ZA_hardcoded_game_scripts"
    if not za_root.exists():
        return
    za_files = [p for p in all_scripts if "ZA_hardcoded_game_scripts" in p.parts]
    if not za_files:
        return

    if not ORDER_ZA.exists():
        warnings.append("[ZA] _order_za_scripts.txt missing; ZA will follow folder+filename order.")
        return

    listed = _read_order_file(ORDER_ZA, SRC_SCRIPTS, errors, allow_code_prefix=False)
    if not listed:
        warnings.append("[ZA] _order_za_scripts.txt is empty; ZA will follow folder+filename order.")
        return

    existing = {_rel(p, SRC_SCRIPTS) for p in za_files}
    listed_set = set(listed)
    missing = sorted(existing - listed_set)
    if missing:
        warnings.append(f"[ZA] Order file does not cover {len(missing)} ZA fragment(s). They will be appended after listed entries.")
        for m in missing[:25]:
            warnings.append(f"      missing: {m}")
        if len(missing) > 25:
            warnings.append(f"      ...and {len(missing) - 25} more")


def _check_constants_order(base: Path, order_path: Path, warnings: List[str], errors: List[str]) -> List[str]:
    if not base.exists():
        return []
    rels = _read_order_file(order_path, base, errors, allow_code_prefix=False)
    existing = {
        _rel(p, base)
        for p in _iter_py_files(base)
        if "_preamble" not in p.parts
    }
    listed = set(rels)
    missing = sorted(existing - listed)
    extra = sorted(listed - existing)

    if missing:
        errors.append(f"[ORDER] Constants: {len(missing)} module(s) not listed in order file.")
        for item in missing[:25]:
            errors.append(f"        missing: {item}")
        if len(missing) > 25:
            errors.append(f"        ...and {len(missing) - 25} more")
    if extra:
        errors.append(f"[ORDER] Constants: {len(extra)} entry(s) in order file do not exist on disk.")
        for item in extra[:25]:
            errors.append(f"        extra: {item}")
        if len(extra) > 25:
            errors.append(f"        ...and {len(extra) - 25} more")
    return rels

def _check_orphan_src_python_files(
    loaded_fragment_files: Set[Path],
    warnings: List[str],
) -> None:
    """QoL: warn if a python file exists under src/ but won't be compiled into any module output."""
    orphan: List[Path] = []
    for fp in _iter_all_src_py_files():
        if fp in loaded_fragment_files:
            continue
        # If this file lives under an allowlisted top-level src folder, ignore.
        try:
            rel = fp.relative_to(SRC_ROOT)
        except Exception:
            continue
        if rel.parts and rel.parts[0] in _SRC_PY_ALLOWLIST:
            continue
        orphan.append(fp)

    if orphan:
        warnings.append(f"[ORPHAN] Found {len(orphan)} *.py file(s) under src/ that are not used by any builder.")
        for p in orphan[:40]:
            warnings.append(f"         {p.relative_to(ROOT).as_posix()}")
        if len(orphan) > 40:
            warnings.append(f"         ...and {len(orphan) - 40} more")



def _check_empty_src_folders(warnings: List[str]) -> None:
    """QoL: warn if there are empty folders under src/ (often indicates a typo or unused section)."""
    empty_dirs: List[Path] = []
    for d in SRC_ROOT.rglob("*"):
        if not d.is_dir():
            continue
        # Ignore allowlisted top-level folders
        rel = _rel(d, SRC_ROOT)
        top = rel.split("/", 1)[0] if rel else ""
        if top in _SRC_PY_ALLOWLIST:
            continue
        name = d.name
        if name == "__pycache__" or name.startswith("."):
            continue
        entries = [e for e in d.iterdir() if not e.name.startswith(".") and e.name != "__pycache__"]
        if len(entries) == 0:
            empty_dirs.append(d)

    if empty_dirs:
        warnings.append(f"[EMPTY] Found {len(empty_dirs)} empty folder(s) under src/ (possible typo or unused section).")
        for p in empty_dirs[:25]:
            warnings.append(f"  - src/{_rel(p, SRC_ROOT)}")
        if len(empty_dirs) > 25:
            warnings.append(f"  ... {len(empty_dirs) - 25} more")


def _check_global_var_collisions(
    files: List[Path],
    label: str,
    prefixes: Tuple[str, ...],
    warnings: List[str],
    allowlist: List[re.Pattern] | None = None,
    max_vars: int = 15,
    max_files_per_var: int = 8,
) -> None:
    """Warn when the same $g_* variable is used in many fragments.

    This is a *heuristic* check: it's not always wrong to reuse globals.
    But presentations and mission templates are notorious for subtle UI/state bugs
    when globals are shared without careful reset/prefix discipline.

    WARNING-ONLY by design.
    """
    usage: Dict[str, Set[Path]] = {}
    spellings: Dict[str, Set[str]] = {}

    def is_allowlisted(var_lower: str) -> bool:
        if not allowlist:
            return False
        return any(pat.match(var_lower) for pat in allowlist)

    for fp in files:
        raw = _read_text(fp)
        for m in _GLOBAL_VAR_RE.finditer(raw):
            gv = m.group(1)
            key = gv.lower()
            if prefixes and not any(key.startswith(p) for p in prefixes):
                continue
            if is_allowlisted(key):
                continue
            usage.setdefault(key, set()).add(fp)
            spellings.setdefault(key, set()).add(gv)

    collisions = [(k, v) for k, v in usage.items() if len(v) > 1]
    collisions.sort(key=lambda kv: (-len(kv[1]), kv[0]))

    if collisions:
        warnings.append(
            f"[{label}] Potential global-var collisions: {len(collisions)} variable(s) used across multiple fragments. "
            "Consider per-feature/presentation prefixes + explicit resets."
        )
        for key, fps in collisions[:max_vars]:
            pretty_var = next(iter(spellings.get(key, {key})))
            files_sorted = sorted([p.relative_to(ROOT).as_posix() for p in fps], key=str.lower)
            shown = files_sorted[:max_files_per_var]
            more = len(files_sorted) - len(shown)
            warnings.append(f"  - {pretty_var}  ({len(files_sorted)} files)")
            for sp in shown:
                warnings.append(f"      {sp}")
            if more > 0:
                warnings.append(f"      ...and {more} more")

    # Also warn when the *same* global var appears with multiple casings.
    # This is benign in vanilla, but becomes a hard bug if you later move to WRECK (case-insensitive globals).
    multi_case = [(k, s) for k, s in spellings.items() if len(s) > 1 and (not prefixes or any(k.startswith(p) for p in prefixes))]
    multi_case.sort(key=lambda kv: kv[0])
    if multi_case:
        warnings.append(f"[{label}] Case-mixed globals detected (future WRECK hazard): {len(multi_case)}")
        for key, s in multi_case[:max_vars]:
            warnings.append(f"  - {', '.join(sorted(s))}")


def _load_allowlist_patterns(path: Path) -> List[re.Pattern]:
    """Load wildcard patterns from a text file and compile to regex.

    Supports '*' wildcard. Matching is case-insensitive.
    """
    if not path.exists():
        return []
    pats: List[re.Pattern] = []
    for ln in _read_text(path).splitlines():
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        # normalize to lowercase for matching; we still compile case-insensitive
        expr = re.escape(ln.lower()).replace(r"\*", ".*")
        pats.append(re.compile(rf"^{expr}$", re.IGNORECASE))
    return pats


def _path_is_allowlisted(rel_path: str, allowlist: List[re.Pattern] | None) -> bool:
    if not allowlist:
        return False
    rp = rel_path.replace('\\', '/').lower()
    return any(p.match(rp) for p in allowlist)


def _check_missing_cost_headers(
    helper_files: List[Path],
    warnings: List[str],
    errors: List[str],
    *,
    strict: bool,
    allowlist: List[re.Pattern] | None,
    max_examples: int = 50,
) -> None:
    """Warn/error when a ZY helper script is missing a '# COST:' line near the top.

    Scope: helper scripts only (under src/scripts/ZY_helper_scripts).
    """
    missing: List[str] = []
    for fp in helper_files:
        rel = fp.relative_to(ROOT).as_posix()
        if _path_is_allowlisted(rel, allowlist):
            continue
        raw = _read_text(fp)
        head = "\n".join(raw.splitlines()[:80])
        if re.search(r"(?mi)^\s*#\s*COST\s*:\s*", head) is None:
            missing.append(f"[COST] Missing '# COST:' in {rel}")

    if not missing:
        return
    target = errors if strict else warnings
    target.append(f"[COST] {len(missing)} helper script(s) missing '# COST:' header line.")
    target.extend(missing[:max_examples])
    if len(missing) > max_examples:
        target.append(f"[COST] ...and {len(missing) - max_examples} more")


def _line_is_comment_or_blank(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith('#')


def _next_meaningful_line(lines: List[str], start_idx: int) -> tuple[int, str] | None:
    for idx in range(start_idx + 1, len(lines)):
        if not _line_is_comment_or_blank(lines[idx]):
            return idx + 1, lines[idx]
    return None


def _check_forbidden_code_patterns(
    files: List[Path],
    errors: List[str],
    *,
    allowlist: List[re.Pattern] | None,
    max_examples: int = 40,
) -> None:
    """Fail fast on known-bad patterns that look structurally valid but break builds/gameplay.

    This catches:
      - Invalid slot math like ":pool_begin" + 1
      - this_or_next chains that accidentally fall through into real actions

    Scope: all src/*.py (not build tools).
    """
    hits: List[str] = []

    for fp in files:
        rel = fp.relative_to(ROOT).as_posix()
        if _path_is_allowlisted(rel, allowlist):
            continue
        raw = _read_text(fp)
        lines = raw.splitlines()
        for idx, line in enumerate(lines):
            ln_no = idx + 1
            s = line.lstrip()
            if not s or s.startswith('#'):
                continue
            m = _FORBIDDEN_SLOT_MATH_RE.search(line)
            if m:
                hash_i = line.find('#')
                if hash_i == -1 or hash_i > m.start():
                    hits.append(f"[FORBID] slot-math {rel}:{ln_no}: {line.strip()}")
                    if len(hits) >= max_examples:
                        break
            if _THIS_OR_NEXT_RE.search(line):
                nxt = _next_meaningful_line(lines, idx)
                if nxt is not None:
                    nxt_ln, nxt_line = nxt
                    if _ACTION_AFTER_THIS_OR_NEXT_RE.search(nxt_line):
                        hits.append(
                            f"[FORBID] this-or-next-action {rel}:{ln_no}->{nxt_ln}: "
                            f"{line.strip()} / {nxt_line.strip()}"
                        )
                        if len(hits) >= max_examples:
                            break
        if len(hits) >= max_examples:
            break

    if hits:
        errors.append(f"[FORBID] Found forbidden code pattern(s): {len(hits)} example(s) shown.")
        errors.extend(hits)


def _check_non_ascii_in_build_and_bats(
    warnings: List[str],
    errors: List[str],
    *,
    strict: bool,
    allowlist: List[re.Pattern] | None,
    max_examples: int = 30,
) -> None:
    """Warn/error on non-ASCII characters in build scripts and batch files.

    This prevents console/banner garbling on Windows terminals.
    Scope: build/**/*.py and *.bat at repo root.
    """
    candidates: List[Path] = []
    build_dir = ROOT / 'build'
    if build_dir.exists():
        candidates.extend([p for p in build_dir.rglob('*.py') if p.is_file()])
    candidates.extend([p for p in ROOT.glob('*.bat') if p.is_file()])
    candidates.sort(key=lambda p: p.relative_to(ROOT).as_posix().lower())

    hits: List[str] = []
    for fp in candidates:
        rel = fp.relative_to(ROOT).as_posix()
        if _path_is_allowlisted(rel, allowlist):
            continue
        raw = _read_text(fp)
        for ln_no, line in enumerate(raw.splitlines(), start=1):
            bad = [ch for ch in line if ord(ch) > 127]
            if bad:
                uniq = ''.join(sorted(set(bad)))
                hits.append(f"[ASCII] {rel}:{ln_no}: non-ascii={uniq!r}")
                if len(hits) >= max_examples:
                    break
        if len(hits) >= max_examples:
            break

    if not hits:
        return
    target = errors if strict else warnings
    target.append(f"[ASCII] Non-ASCII characters found in build/bat files: {len(hits)} example(s) shown.")
    target.extend(hits)


def _iter_string_literals_with_linenos(raw: str) -> List[Tuple[str, int]]:
    """Extract simple single/double-quoted string literals with their starting line number.

    - Ignores comments (# ... end of line) when not inside a string.
    - Skips triple-quoted strings entirely (docstrings / large blocks).

    This is *not* a full Python parser. It's a fast, robust enough lexer for our fragments.
    """
    out: List[Tuple[str, int]] = []
    i = 0
    line = 1
    in_comment = False
    in_str = False
    quote = ""
    esc = False
    start_line = 1
    buf: List[str] = []

    while i < len(raw):
        ch = raw[i]

        # Track line numbers
        if ch == "\n":
            line += 1
            in_comment = False
            if in_str:
                # keep newlines inside strings (rare in fragments, but safe)
                buf.append(ch)
            i += 1
            continue

        if in_comment:
            i += 1
            continue

        if in_str:
            if esc:
                buf.append(ch)
                esc = False
                i += 1
                continue

            if ch == "\\":
                buf.append(ch)
                esc = True
                i += 1
                continue

            if ch == quote:
                out.append(("".join(buf), start_line))
                buf = []
                in_str = False
                quote = ""
                i += 1
                continue

            buf.append(ch)
            i += 1
            continue

        # Not in string
        if ch == "#":
            in_comment = True
            i += 1
            continue

        if ch in ("'", '"'):
            # Skip triple quotes (''' or """)
            if raw[i:i+3] == ch*3:
                end = raw.find(ch*3, i+3)
                if end == -1:
                    # unclosed triple quote; treat as rest-of-file
                    return out
                # advance, counting lines
                block = raw[i:end+3]
                line += block.count("\n")
                i = end + 3
                continue

            in_str = True
            quote = ch
            start_line = line
            buf = []
            i += 1
            continue

        i += 1

    return out


def _iter_identifier_tokens_with_linenos(raw: str) -> List[Tuple[str, int, int]]:
    """Extract identifier-like tokens with line numbers and start index.

    - Ignores comments (# ... end of line) when not inside a string.
    - Skips all quoted strings (single, double, and triple-quoted) entirely.

    Returns (token, line, start_index).

    Notes:
    - Tokens immediately preceded by '$' are suppressed (e.g. $qst_foo). Those are variables,
      not ID constants.
    """
    out: List[Tuple[str, int, int]] = []
    i = 0
    line = 1
    in_comment = False
    in_str = False
    quote = ''
    esc = False

    def is_ident_start(ch: str) -> bool:
        return ch.isalpha() or ch == '_'

    def is_ident_part(ch: str) -> bool:
        return ch.isalnum() or ch == '_'

    while i < len(raw):
        ch = raw[i]

        if ch == '\n':
            line += 1
            in_comment = False
            i += 1
            continue

        if in_comment:
            i += 1
            continue

        if in_str:
            if esc:
                esc = False
                i += 1
                continue
            if ch == '\\':
                esc = True
                i += 1
                continue
            if ch == quote:
                in_str = False
                quote = ''
                i += 1
                continue
            i += 1
            continue

        # Not in string
        if ch == '#':
            in_comment = True
            i += 1
            continue

        if ch in ("'", '"'):
            # Skip triple-quoted blocks
            if raw[i:i+3] == ch*3:
                end = raw.find(ch*3, i+3)
                if end == -1:
                    return out
                block = raw[i:end+3]
                line += block.count('\n')
                i = end + 3
                continue
            in_str = True
            quote = ch
            i += 1
            continue

        if is_ident_start(ch):
            start_i = i
            start_line = line
            j = i + 1
            while j < len(raw) and is_ident_part(raw[j]):
                j += 1
            tok = raw[start_i:j]

            # Suppress global-var names like $qst_foo (variables, not IDs)
            if start_i > 0 and raw[start_i - 1] == '$':
                i = j
                continue

            out.append((tok, start_line, start_i))
            i = j
            continue

        i += 1

    return out


def _build_known_id_sets(
    script_files: List[Path],
    menu_files: List[Path],
    pres_files: List[Path],
    mt_files: List[Path],
    errors: List[str],
) -> Tuple[Set[str], Set[str], Set[str], Set[str]]:
    """Return known ID constants for scripts/menus/presentations/mission templates."""
    def ids_from(files: List[Path], export: str) -> List[str]:
        out_ids: List[str] = []
        for fp in files:
            raw = _read_text(fp)
            if not _EXPORT_RE[export].search(raw):
                continue
            try:
                inner = _extract_list_block(raw, export)
            except Exception as e:
                errors.append(f"[PARSE] Failed to parse {export} list in {fp}: {e}")
                continue
            out_ids.extend(_iter_top_level_tuple_ids(inner))
        return out_ids

    scripts = {f"script_{i}" for i in ids_from(script_files, "SCRIPTS")}
    menus = {f"mnu_{i}" for i in ids_from(menu_files, "MENUS")}
    pres = {f"prsnt_{i}" for i in ids_from(pres_files, "PRESENTATIONS")}
    mts = {f"mt_{i}" for i in ids_from(mt_files, "MISSION_TEMPLATES")}

    return scripts, menus, pres, mts



def _build_known_id_sets_extended(errors: List[str]) -> Dict[str, Set[str]]:
    """Build known ID sets for non-modular domains from compile/ids/ID_*.py.

    The generated ID files are the most reliable source in this repo shape:
    they already include legacy append patterns and preserve the exact exported
    constant spellings that source fragments reference.
    """
    ids_dir = ROOT / "compile" / "ids"

    def ids_from_id_file(filename: str, prefix: str) -> Set[str]:
        path = ids_dir / filename
        if not path.exists():
            return set()
        raw = _read_text(path)
        pat = re.compile(rf"(?mi)^\s*({re.escape(prefix)}[A-Za-z0-9_]+)\s*=")
        return {m.group(1) for m in pat.finditer(raw)}

    out: Dict[str, Set[str]] = {}
    out["trp_"] = ids_from_id_file("ID_troops.py", "trp_")
    out["itm_"] = ids_from_id_file("ID_items.py", "itm_")
    out["fac_"] = ids_from_id_file("ID_factions.py", "fac_")
    out["p_"] = ids_from_id_file("ID_parties.py", "p_")
    out["pt_"] = ids_from_id_file("ID_party_templates.py", "pt_")
    out["qst_"] = ids_from_id_file("ID_quests.py", "qst_")
    out["scn_"] = ids_from_id_file("ID_scenes.py", "scn_")

    return out

def _check_missing_string_id_references(
    files: List[Path],
    known_scripts: Set[str],
    known_menus: Set[str],
    known_pres: Set[str],
    known_mts: Set[str],
    warnings: List[str],
    errors: List[str],
    *,
    strict: bool,
    max_examples: int = 40,
) -> None:
    """Validate references to IDs that are typically used as string literals.

    We scan string literals (ignoring comments) and flag missing targets for:
    - script_*
    - mnu_*
    - prsnt_*
    - mt_*

    If strict=False, findings are warnings (safer rollout).
    """
    missing: List[str] = []

    def check_token(tok: str) -> bool:
        if not tok.startswith(_REF_STRING_PREFIXES):
            return True
        if tok.startswith("script_"):
            return tok in known_scripts
        if tok.startswith("mnu_"):
            return tok in known_menus
        if tok.startswith("prsnt_"):
            return tok in known_pres
        if tok.startswith("mt_"):
            return tok in known_mts
        return True

    for fp in files:
        raw = _read_text(fp)
        for tok, ln in _iter_string_literals_with_linenos(raw):
            if not tok.startswith(_REF_STRING_PREFIXES):
                continue
            if not check_token(tok):
                missing.append(f"[REF] Missing reference '{tok}' in {fp} (line {ln})")

    if not missing:
        return

    header = f"[REF] Found {len(missing)} missing string-id reference(s)."
    target = errors if strict else warnings
    target.append(header)
    target.extend(missing[:max_examples])
    if len(missing) > max_examples:
        target.append(f"[REF] ...and {len(missing) - max_examples} more")


def _check_missing_identifier_id_references(
    files: List[Path],
    known_by_prefix: Dict[str, Set[str]],
    warnings: List[str],
    errors: List[str],
    *,
    strict: bool,
    max_examples: int = 60,
) -> None:
    """Validate references to IDs that are typically used as identifier constants.

    We scan identifier tokens outside of strings/comments and flag missing targets for:
    - trp_*, itm_*, fac_*, p_*, pt_*, qst_*, scn_*

    Heuristic to reduce noise:
    - ignore tokens that are directly assigned to (token followed by '=')

    If strict=False, findings are warnings (safer rollout).
    """
    missing: List[str] = []

    def should_ignore_assignment(raw: str, start_i: int, tok_len: int) -> bool:
        j = start_i + tok_len
        while j < len(raw) and raw[j].isspace():
            j += 1
        return (j < len(raw) and raw[j] == '=')

    prefixes = tuple(known_by_prefix.keys())

    for fp in files:
        raw = _read_text(fp)
        for tok, ln, start_i in _iter_identifier_tokens_with_linenos(raw):
            if not tok.startswith(prefixes):
                continue
            if should_ignore_assignment(raw, start_i, len(tok)):
                continue
            for pref in prefixes:
                if tok.startswith(pref):
                    known = known_by_prefix.get(pref, set())
                    if known and tok not in known:
                        missing.append(f"[REF] Missing reference '{tok}' in {fp} (line {ln})")
                    break

    if not missing:
        return

    header = f"[REF] Found {len(missing)} missing identifier-id reference(s)."
    target = errors if strict else warnings
    target.append(header)
    target.extend(missing[:max_examples])
    if len(missing) > max_examples:
        target.append(f"[REF] ...and {len(missing) - max_examples} more")


def _extract_dialog_route_key(inner: str) -> str:
    m = re.search(
        r'^\s*\[\s*([^,\]]+)\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([^"]+)"',
        inner,
        re.S,
    )
    if not m:
        return ""
    speaker = m.group(1).strip()
    input_state = m.group(2).strip()
    output_state = m.group(5).strip()
    return f"{speaker}::{input_state}->{output_state}"


def _extract_dialog_head_signature(inner: str, max_ops: int = 3) -> str:
    m = re.search(
        r'^\s*\[\s*([^,\]]+)\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([^"]+)"',
        inner,
        re.S,
    )
    if not m:
        return ""
    head = m.group(3)
    ops = [mm.group(1).strip() for mm in re.finditer(r'\(\s*([A-Za-z0-9_|]+)', head)]
    if not ops:
        return "no_conditions"
    return "|".join(ops[:max_ops])


def _extract_dialog_text_fingerprint(inner: str) -> str:
    m = re.search(
        r'^\s*\[\s*([^,\]]+)\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([^"]+)"',
        inner,
        re.S,
    )
    if not m:
        return ""
    text = m.group(4)
    text = text.replace("\\\n", " ")
    text = re.sub(r"\{[^}]+\}", "{var}", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    if not text:
        return "empty_text"
    if len(text) > 64:
        text = text[:64]
    return text


def _check_dialog_head_duplicates(
    files: List[Path],
    warnings: List[str],
    errors: List[str],
    *,
    strict: bool,
    allowlist: List[re.Pattern] | None,
    max_examples: int = 5,
) -> None:
    seen: Dict[str, Path] = {}
    dups: Dict[str, List[Path]] = {}

    def is_allowlisted(sig: str) -> bool:
        if not allowlist:
            return "$" in sig
        s = sig.lower()
        return any(p.match(s) for p in allowlist)

    for fp in files:
        raw = _read_text(fp)
        if not _EXPORT_RE["DIALOGS"].search(raw):
            continue
        try:
            inner = _extract_list_block(raw, "DIALOGS")
        except Exception:
            continue
        route_key = _extract_dialog_route_key(inner)
        head_sig = _extract_dialog_head_signature(inner)
        text_sig = _extract_dialog_text_fingerprint(inner)
        sig = f"{route_key} [{head_sig}] {{{text_sig}}}" if route_key and head_sig and text_sig else ""
        if not sig or is_allowlisted(sig):
            continue
        if sig in seen:
            dups.setdefault(sig, [seen[sig]]).append(fp)
        else:
            seen[sig] = fp

    if not dups:
        return

    items = sorted(dups.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))
    target = errors if strict else warnings
    target.append(
        f"[DIALOG-DUP] Found {len(items)} duplicate dialog head signature(s). "
        "See docs/reports/dialog_head_duplicates.txt for the full list."
    )
    for sig, paths in items[:max_examples]:
        rels = [p.relative_to(ROOT).as_posix() for p in paths]
        target.append(f"[DIALOG-DUP] {sig} ({len(rels)} fragments) first={rels[0]}")

    if len(items) > max_examples:
        target.append(f"[DIALOG-DUP] ...and {len(items) - max_examples} more signature(s)")


def _apply_baseline_filter(
    warnings: List[str],
    errors: List[str],
    baseline: List[re.Pattern] | None,
) -> Tuple[List[str], List[str], int]:
    if not baseline:
        return warnings, errors, 0

    def keep(msg: str) -> bool:
        lowered = msg.lower()
        return not any(p.match(lowered) for p in baseline)

    new_warnings = [w for w in warnings if keep(w)]
    new_errors = [e for e in errors if keep(e)]
    suppressed = (len(warnings) - len(new_warnings)) + (len(errors) - len(new_errors))
    return new_warnings, new_errors, suppressed


### (v81) additional Doctor checks are defined earlier in this file.
def run_doctor(
    *,
    check_duplicate_ids: bool = True,
    check_refs: bool = True,
    refs_strict: bool = False,
    check_cost: bool = True,
    cost_strict: bool = False,
    check_forbidden: bool = True,
    check_ascii: bool = True,
    ascii_strict: bool = False,
    check_stubs: bool = True,
    stubs_strict: bool = False,
    check_dialog_duplicates: bool = True,
    dialog_duplicates_strict: bool = False,
    check_feature_integrations: bool = True,
    check_generated_contract: bool = True,
    check_generated_ids: bool = True,
    strict_all: bool = False,
    new_only: bool = False,
) -> DoctorResult:
    errors: List[str] = []
    warnings: List[str] = []
    summary: List[str] = []
    timings_ms: Dict[str, int] = {}

    def run_timed(label: str, fn: Callable[[], None]) -> None:
        t0 = time.perf_counter()
        fn()
        timings_ms[label] = int((time.perf_counter() - t0) * 1000)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_EDIT.mkdir(parents=True, exist_ok=True)
    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    _check_compile_id_shadow_artifacts(errors)

    if check_generated_contract:
        def run_generated_contract() -> None:
            contract_errors, contract_warnings = check_generated_hardcoded_contract(check_ids=check_generated_ids)
            errors.extend(contract_errors)
            warnings.extend(contract_warnings)

        run_timed("mb1011_generated_hardcoded_contract", run_generated_contract)

    # Gather files (exclude _preamble folders from fragment validation)
    script_files_all = _iter_py_files(SRC_SCRIPTS)
    menu_files_all = _iter_py_files(SRC_MENUS)
    dialog_files_all = _iter_py_files(SRC_DIALOGS)
    trigger_files_all = _iter_py_files(SRC_TRIGGERS)
    pres_files_all = _iter_py_files(SRC_PRESENTATIONS)
    mt_files_all = _iter_py_files(SRC_MISSION_TEMPLATES)
    constant_files = _iter_py_files(SRC_CONSTANTS)
    quest_files_all = _iter_py_files(SRC_QUESTS)

    script_preamble_files = [p for p in script_files_all if "_preamble" in p.parts]
    menu_preamble_files = [p for p in menu_files_all if "_preamble" in p.parts]
    dialog_preamble_files = [p for p in dialog_files_all if "_preamble" in p.parts]
    trigger_preamble_files = [p for p in trigger_files_all if "_preamble" in p.parts]
    pres_preamble_files = [p for p in pres_files_all if "_preamble" in p.parts]
    mt_preamble_files = [p for p in mt_files_all if "_preamble" in p.parts]
    quest_preamble_files = [p for p in quest_files_all if "_preamble" in p.parts]

    script_files = [p for p in script_files_all if "_preamble" not in p.parts]
    menu_files = [p for p in menu_files_all if "_preamble" not in p.parts]
    dialog_files = [p for p in dialog_files_all if "_preamble" not in p.parts]
    trigger_files = [p for p in trigger_files_all if "_preamble" not in p.parts]
    pres_files = [p for p in pres_files_all if "_preamble" not in p.parts]
    mt_files = [p for p in mt_files_all if "_preamble" not in p.parts]
    quest_files = [p for p in quest_files_all if "_preamble" not in p.parts]

    # Exports present?
    _check_exports(script_files, "SCRIPTS", errors)
    _check_exports(menu_files, "MENUS", errors)
    _check_exports(dialog_files, "DIALOGS", errors)
    _check_exports(trigger_files, "SIMPLE_TRIGGERS", errors)
    _check_exports(pres_files, "PRESENTATIONS", errors)
    _check_exports(mt_files, "MISSION_TEMPLATES", errors)

    # Optional allowlist to keep inherited duplicate IDs explicit instead of
    # disabling duplicate checks wholesale.
    allow_duplicate_ids = _load_allowlist_patterns(ALLOWLIST_DUPLICATE_IDS_PATH)

    # Duplicate top-level IDs (and counts)
    n_scripts = _check_top_level_id_duplicates(
        script_files,
        "SCRIPTS",
        errors,
        label="script",
        check_duplicates=check_duplicate_ids,
        allowlist=allow_duplicate_ids,
    )
    n_menus = _check_top_level_id_duplicates(
        menu_files,
        "MENUS",
        errors,
        label="menu",
        check_duplicates=check_duplicate_ids,
        allowlist=allow_duplicate_ids,
    )
    n_pres = _check_top_level_id_duplicates(
        pres_files,
        "PRESENTATIONS",
        errors,
        label="presentation",
        check_duplicates=check_duplicate_ids,
        allowlist=allow_duplicate_ids,
    )
    n_mts = _check_top_level_id_duplicates(
        mt_files,
        "MISSION_TEMPLATES",
        errors,
        label="mission template",
        check_duplicates=check_duplicate_ids,
        allowlist=allow_duplicate_ids,
    )
    # Missing reference checks (warning by default; can be made strict)
    if check_refs:
        known_scripts, known_menus, known_pres, known_mts = _build_known_id_sets(
            script_files,
            menu_files,
            pres_files,
            mt_files,
            errors,
        )
        known_extended = _build_known_id_sets_extended(errors)
        scan_files = list({
            *script_files_all,
            *menu_files_all,
            *dialog_files_all,
            *trigger_files_all,
            *pres_files_all,
            *mt_files_all,
        })
        scan_files.sort(key=lambda p: p.relative_to(ROOT).as_posix().lower())
        _check_missing_string_id_references(
            scan_files,
            known_scripts,
            known_menus,
            known_pres,
            known_mts,
            warnings,
            errors,
            strict=refs_strict,
        )
        _check_missing_identifier_id_references(
            scan_files,
            known_extended,
            warnings,
            errors,
            strict=refs_strict,
        )

    # Strict manifests
    menu_order = _read_order_file(ORDER_MENUS, SRC_MENUS, errors, allow_code_prefix=False)
    dialog_order = _read_order_file(ORDER_DIALOGS, SRC_DIALOGS, errors, allow_code_prefix=True)
    trigger_order = _read_order_file(ORDER_TRIGGERS, SRC_TRIGGERS, errors, allow_code_prefix=False)
    presentation_order = _read_order_file(
        ORDER_PRESENTATIONS,
        SRC_PRESENTATIONS,
        errors,
        allow_code_prefix=False,
    )
    mission_template_order = _read_order_file(
        ORDER_MISSION_TEMPLATES,
        SRC_MISSION_TEMPLATES,
        errors,
        allow_code_prefix=False,
    )
    constant_order = _check_constants_order(SRC_CONSTANTS, ORDER_CONSTANTS, warnings, errors)

    _check_manifest_completeness(SRC_MENUS, menu_files, menu_order, errors, "Game Menus")
    _check_manifest_completeness(SRC_DIALOGS, dialog_files, dialog_order, errors, "Dialogs")
    _check_manifest_completeness(SRC_TRIGGERS, trigger_files, trigger_order, errors, "Simple Triggers")
    _check_manifest_completeness(
        SRC_PRESENTATIONS,
        pres_files,
        presentation_order,
        errors,
        "Presentations",
    )
    _check_manifest_completeness(
        SRC_MISSION_TEMPLATES,
        mt_files,
        mission_template_order,
        errors,
        "Mission Templates",
    )

    # ZA warnings only
    _check_za_order_warning(script_files, warnings, errors)

    # QoL: orphan *.py fragments under src/ that won't be compiled into any module output.
    loaded: Set[Path] = (
        set(script_files) | set(menu_files) | set(dialog_files) | set(trigger_files) | set(pres_files) | set(mt_files)
        | set(quest_files)
        | set(script_preamble_files) | set(menu_preamble_files) | set(pres_preamble_files) | set(mt_preamble_files)
        | set(quest_preamble_files)
        | set(dialog_preamble_files) | set(trigger_preamble_files)
    )
    # Only files referenced by strict manifests are actually compiled.
    loaded |= {SRC_MENUS / rel for rel in menu_order if (SRC_MENUS / rel).exists()}
    loaded |= {SRC_DIALOGS / rel for rel in dialog_order if (SRC_DIALOGS / rel).exists()}
    loaded |= {SRC_TRIGGERS / rel for rel in trigger_order if (SRC_TRIGGERS / rel).exists()}
    loaded |= {
        SRC_PRESENTATIONS / rel
        for rel in presentation_order
        if (SRC_PRESENTATIONS / rel).exists()
    }
    loaded |= {
        SRC_MISSION_TEMPLATES / rel
        for rel in mission_template_order
        if (SRC_MISSION_TEMPLATES / rel).exists()
    }
    loaded |= {
        SRC_CONSTANTS / rel
        for rel in constant_order
        if (SRC_CONSTANTS / rel).exists()
    }
    _check_orphan_src_python_files(loaded, warnings)
    _check_empty_src_folders(warnings)

    if check_feature_integrations:
        run_timed(
            "modernization_tooling_guards",
            lambda: _check_modernization_tooling_guards(
                script_files_all,
                dialog_files_all,
                menu_files_all,
                trigger_files_all,
                pres_files_all,
                mt_files_all,
                errors,
                warnings,
            ),
        )
        run_timed(
            "sod_doctrine_registry",
            lambda: _check_sod_doctrine_registry(script_files_all, constant_files, warnings, errors),
        )
        run_timed(
            "sod_threat_board_registry",
            lambda: _check_sod_threat_board_registry(
                script_files_all, menu_files, trigger_files, quest_files, constant_files, warnings, errors
            ),
        )
        run_timed(
            "sod_law_framework",
            lambda: _check_sod_law_framework(
                script_files_all, menu_files, trigger_files, pres_files, constant_files, errors, warnings
            ),
        )
    if check_feature_integrations:
        run_timed(
            "quest_generation_registry",
            lambda: _check_quest_generation_registry(errors, warnings),
        )
        run_timed(
            "quest_authoring_dsl",
            lambda: _check_quest_authoring_dsl(errors, warnings),
        )
        run_timed(
            "quest_diagnostics",
            lambda: _write_quest_diagnostics_report(quest_files_all, errors, warnings),
        )
    if check_feature_integrations:
        run_timed(
            "quest_engine_integration",
            lambda: _check_quest_engine_integration(script_files_all, trigger_files, errors, warnings),
        )
        run_timed(
            "quest_battle_integration",
            lambda: _check_quest_battle_integration(script_files_all, mt_files_all, constant_files, errors, warnings),
        )
        run_timed(
            "quest_journal_integration",
            lambda: _check_quest_journal_integration(script_files_all, menu_files, constant_files, errors, warnings),
        )
        run_timed(
            "quest_branching_integration",
            lambda: _check_quest_branching_integration(script_files_all, constant_files, errors, warnings),
        )
    if check_feature_integrations:
        run_timed(
            "quest_migration_strategy",
            lambda: _check_quest_migration_strategy(quest_files_all, errors, warnings),
        )
        run_timed(
            "building_registry",
            lambda: _check_building_registry_consistency(
                constant_files,
                list(
                    {
                        *script_files_all,
                        *menu_files_all,
                        *dialog_files_all,
                        *trigger_files_all,
                        *pres_files_all,
                        *mt_files_all,
                        *quest_files_all,
                    }
                ),
                warnings,
                errors,
            ),
        )
        run_timed(
            "quest_architecture_report",
            lambda: _write_quest_architecture_report(
                quest_files_all,
                script_files_all,
                dialog_files_all,
                menu_files_all,
                trigger_files_all,
                mt_files_all,
                constant_files,
            ),
        )

    # Optional allowlist to reduce noise from known-safe global reuse.
    allow_globals = _load_allowlist_patterns(ALLOWLIST_GLOBALS_PATH)

    # Optional allowlists for additional checks.
    allow_missing_cost = _load_allowlist_patterns(ALLOWLIST_COST_PATH)
    allow_non_ascii = _load_allowlist_patterns(ALLOWLIST_NONASCII_PATH)
    allow_forbidden = _load_allowlist_patterns(ALLOWLIST_FORBIDDEN_PATTERNS_PATH)
    allow_stubs = _load_allowlist_patterns(ALLOWLIST_STUBS_PATH)
    allow_dialog_dupes = _load_allowlist_patterns(ALLOWLIST_DIALOG_DUPES_PATH)
    baseline_patterns = _load_allowlist_patterns(BASELINE_FINDINGS_PATH) if new_only else []

    # QoL: potential state/overlay ID collisions in Presentations & Mission Templates.
    # (heuristic; warning-only)
    run_timed(
        "global_var_collisions_presentations",
        lambda: _check_global_var_collisions(
            pres_files,
            label="PRES-ID",
            prefixes=("$g_presentation",),
            warnings=warnings,
            allowlist=allow_globals,
        ),
    )
    run_timed(
        "global_var_collisions_mission_templates",
        lambda: _check_global_var_collisions(
            mt_files,
            label="MT-ID",
            prefixes=("$g_mt", "$g_mission", "$g_battle"),
            warnings=warnings,
            allowlist=allow_globals,
        ),
    )

    # (v81+) Additional sanity checks
    if check_cost:
        helper_files = [p for p in script_files_all if "ZY_helper_scripts" in p.parts]
        run_timed(
            "cost_headers",
            lambda: _check_missing_cost_headers(
                helper_files,
                warnings,
                errors,
                strict=cost_strict,
                allowlist=allow_missing_cost,
            ),
        )

    if check_forbidden:
        run_timed(
            "forbidden_patterns",
            lambda: _check_forbidden_code_patterns(
                _iter_all_src_py_files(),
                errors,
                allowlist=allow_forbidden,
            ),
        )

    if check_ascii:
        run_timed(
            "ascii_scan",
            lambda: _check_non_ascii_in_build_and_bats(
                warnings,
                errors,
                strict=ascii_strict,
                allowlist=allow_non_ascii,
            ),
        )

    if check_stubs:
        run_timed(
            "stub_detection_scripts",
            lambda: _check_stub_fragments(
                script_files,
                "SCRIPTS",
                warnings,
                errors,
                strict=stubs_strict,
                allowlist=allow_stubs,
            ),
        )
        run_timed(
            "stub_detection_triggers",
            lambda: _check_stub_fragments(
                trigger_files,
                "SIMPLE_TRIGGERS",
                warnings,
                errors,
                strict=stubs_strict,
                allowlist=allow_stubs,
            ),
        )
        run_timed(
            "stub_detection_dialogs",
            lambda: _check_stub_fragments(
                dialog_files,
                "DIALOGS",
                warnings,
                errors,
                strict=stubs_strict,
                allowlist=allow_stubs,
            ),
        )
        run_timed(
            "stub_detection_menus",
            lambda: _check_stub_fragments(
                menu_files,
                "MENUS",
                warnings,
                errors,
                strict=stubs_strict,
                allowlist=allow_stubs,
            ),
        )
        run_timed(
            "stub_detection_presentations",
            lambda: _check_stub_fragments(
                pres_files,
                "PRESENTATIONS",
                warnings,
                errors,
                strict=stubs_strict,
                allowlist=allow_stubs,
            ),
        )
        run_timed(
            "stub_detection_mission_templates",
            lambda: _check_stub_fragments(
                mt_files,
                "MISSION_TEMPLATES",
                warnings,
                errors,
                strict=stubs_strict,
                allowlist=allow_stubs,
            ),
        )

    if check_dialog_duplicates:
        run_timed(
            "dialog_duplicate_heads",
            lambda: _check_dialog_head_duplicates(
                dialog_files,
                warnings,
                errors,
                strict=dialog_duplicates_strict,
                allowlist=allow_dialog_dupes,
            ),
        )

    suppressed_by_baseline = 0
    if new_only:
        warnings, errors, suppressed_by_baseline = _apply_baseline_filter(
            warnings,
            errors,
            baseline_patterns,
        )

    if strict_all and warnings:
        errors.extend(warnings)
        warnings = []

    # Summary
    summary.append("Doctor Report (P1)")
    summary.append("")
    summary.append("Modes:")
    summary.append(f"Duplicate ID check: {'ENABLED (STRICT)' if check_duplicate_ids else 'DISABLED'}")
    summary.append(f"Reference checks:   {'ENABLED (STRICT)' if check_refs and refs_strict else ('ENABLED (WARN)' if check_refs else 'DISABLED')}")
    summary.append(f"COST headers:       {'ENABLED (STRICT)' if check_cost and cost_strict else ('ENABLED (WARN)' if check_cost else 'DISABLED')}")
    summary.append(f"Forbidden patterns: {'ENABLED (STRICT)' if check_forbidden else 'DISABLED'}")
    summary.append(f"ASCII build/bat:    {'ENABLED (STRICT)' if check_ascii and ascii_strict else ('ENABLED (WARN)' if check_ascii else 'DISABLED')}")
    summary.append(f"Stub detection:     {'ENABLED (STRICT)' if check_stubs and stubs_strict else ('ENABLED (WARN)' if check_stubs else 'DISABLED')}")
    summary.append(f"Dialog duplicates:  {'ENABLED (STRICT)' if check_dialog_duplicates and dialog_duplicates_strict else ('ENABLED (WARN)' if check_dialog_duplicates else 'DISABLED')}")
    if check_generated_contract:
        generated_mode = "ENABLED (STRICT)" if check_generated_ids else "ENABLED (STRICT, IDs deferred)"
    else:
        generated_mode = "DISABLED (checked after fragment assembly)"
    summary.append(f"M&B 1.011 generated hardcoded contract: {generated_mode}")
    summary.append("SoD doctrine:       ENABLED (STRICT)")
    summary.append("Threat board:       ENABLED (STRICT)")
    summary.append(f"Strict umbrella:    {'ENABLED' if strict_all else 'DISABLED'}")
    summary.append(f"New findings only:  {'ENABLED' if new_only else 'DISABLED'}")
    summary.append("")
    summary.append("Coverage:")
    summary.append(f"Scripts:           {len(script_files)} files, {n_scripts} top-level scripts")
    summary.append(f"Game Menus:        {len(menu_files)} files, manifest entries: {len(menu_order)}")
    summary.append(f"Game Menus IDs:    {n_menus} top-level menus")
    summary.append(f"Dialogs:           {len(dialog_files)} files, manifest entries: {len(dialog_order)}")
    summary.append(f"Simple Triggers:   {len(trigger_files)} files, manifest entries: {len(trigger_order)}")
    summary.append(
        f"Presentations:     {len(pres_files)} files, manifest entries: {len(presentation_order)}"
    )
    summary.append(f"Presentations IDs: {n_pres} top-level presentations")
    summary.append(
        f"Mission Templates: {len(mt_files)} files, manifest entries: {len(mission_template_order)}"
    )
    summary.append(f"Mission Templates IDs: {n_mts} top-level mission templates")
    summary.append(f"Constants:         {len(constant_files)} files, manifest entries: {len(constant_order)}")
    summary.append(f"Quests:            {len(quest_files)} files")
    summary.append("")
    if new_only:
        summary.append(f"Baseline filtered: {suppressed_by_baseline} finding(s) suppressed")
        summary.append("")
    summary.append("Timing (ms):")
    for key in sorted(timings_ms):
        summary.append(f"{key}: {timings_ms[key]}")
    summary.append("")
    summary.append(f"Outcome:           {len(errors)} error(s), {len(warnings)} warning(s)")
    summary.append("")

    if warnings:
        summary.append("Warnings:")
        summary.extend([f"  {w}" for w in warnings])
        summary.append("")
    if errors:
        summary.append("Errors:")
        summary.extend([f"  {e}" for e in errors])
        summary.append("")

    REPORT_PATH.write_text("\n".join(summary), encoding="utf-8", errors="replace")
    report_artifacts = _doctor_report_artifacts()
    slowest_timings = _slowest_timings(timings_ms)
    report_json = {
        "modes": {
            "check_duplicate_ids": check_duplicate_ids,
            "check_refs": check_refs,
            "refs_strict": refs_strict,
            "check_cost": check_cost,
            "cost_strict": cost_strict,
            "check_forbidden": check_forbidden,
            "check_ascii": check_ascii,
            "ascii_strict": ascii_strict,
            "check_stubs": check_stubs,
            "stubs_strict": stubs_strict,
            "check_dialog_duplicates": check_dialog_duplicates,
            "dialog_duplicates_strict": dialog_duplicates_strict,
            "check_feature_integrations": check_feature_integrations,
            "strict_all": strict_all,
            "new_only": new_only,
        },
        "counts": {
            "errors": len(errors),
            "warnings": len(warnings),
            "scripts_files": len(script_files),
            "scripts_top_level": n_scripts,
            "menus_files": len(menu_files),
            "menus_top_level": n_menus,
            "dialogs_files": len(dialog_files),
            "triggers_files": len(trigger_files),
            "presentations_files": len(pres_files),
            "presentations_top_level": n_pres,
            "mission_templates_files": len(mt_files),
            "mission_templates_top_level": n_mts,
            "constants_files": len(constant_files),
            "quests_files": len(quest_files),
            "baseline_suppressed": suppressed_by_baseline,
        },
        "timings_ms": timings_ms,
        "slowest_timings": slowest_timings,
        "warnings": warnings,
        "errors": errors,
        "report_path": REPORT_PATH.relative_to(ROOT).as_posix(),
        "report_artifacts": report_artifacts,
    }
    REPORT_JSON_PATH.write_text(json.dumps(report_json, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return DoctorResult(errors=errors, warnings=warnings, summary=summary, timings_ms=timings_ms)

def main(
    *,
    check_duplicate_ids: bool = True,
    check_refs: bool = True,
    refs_strict: bool = False,
    check_cost: bool = True,
    cost_strict: bool = False,
    check_forbidden: bool = True,
    check_ascii: bool = True,
    ascii_strict: bool = False,
    check_stubs: bool = True,
    stubs_strict: bool = False,
    check_dialog_duplicates: bool = True,
    dialog_duplicates_strict: bool = False,
    check_generated_contract: bool = True,
    check_generated_ids: bool = True,
    strict_all: bool = False,
    new_only: bool = False,
    argv: List[str] | None = None,
) -> None:
    """Run Doctor and exit non-zero on errors.

    Toggle duplicate-id detection:
      --doctor-no-dupes   disables duplicate-id checks
      --doctor-dupes      explicitly enables duplicate-id checks (default)

    Toggle additional checks:
      --doctor-no-cost            disable helper COST header check
      --doctor-cost              enable helper COST header check (default)
      --doctor-cost-strict        treat missing COST headers as errors

      --doctor-no-forbidden       disable forbidden slot-math string pattern check
      --doctor-forbidden          enable forbidden pattern check (default)

      --doctor-no-ascii           disable non-ASCII scan for build/*.py and *.bat
      --doctor-ascii              enable non-ASCII scan (default)
      --doctor-ascii-strict       treat non-ASCII findings as errors

      --doctor-no-stubs           disable stub/empty fragment detection
      --doctor-stubs              enable stub/empty fragment detection (default)
      --doctor-stubs-strict       treat stub/empty fragments as errors

      --doctor-no-dialog-dupes    disable duplicate dialog head detection
      --doctor-dialog-dupes       enable duplicate dialog head detection (default)
      --doctor-dialog-dupes-strict treat duplicate dialog heads as errors

      --doctor-no-generated-contract skip generated compile-layer hardcoded checks
      --doctor-prebuild-source-only defer generated ID checks until the process step
      --doctor-hardcoded-postprocess run only the M&B 1.011 generated ID/name contract

      --doctor-strict             promote all remaining warnings to errors
      --doctor-new-only           suppress findings matched by docs/edit/doctor_baseline_findings.txt
    """
    args = list(sys.argv if argv is None else argv)
    if '--doctor-hardcoded-postprocess' in args:
        contract_errors, contract_warnings = check_generated_hardcoded_contract(check_ids=True)
        for warning in contract_warnings:
            print(f"[doctor] WARNING: {warning}")
        if contract_errors:
            for error in contract_errors:
                print(f"[doctor] ERROR: {error}")
            print(f"[doctor] M&B 1.011 generated hardcoded contract failed: {len(contract_errors)} error(s), {len(contract_warnings)} warning(s).")
            raise SystemExit(1)
        print(f"[doctor] M&B 1.011 generated hardcoded contract OK: {len(contract_warnings)} warning(s).")
        return

    if '--doctor-prebuild-source-only' in args:
        check_generated_ids = False
    if '--doctor-no-generated-contract' in args:
        check_generated_contract = False

    if "--doctor-no-dupes" in args:
        check_duplicate_ids = False
    elif "--doctor-dupes" in args:
        check_duplicate_ids = True
    if '--doctor-no-refs' in args:
        check_refs = False
    elif '--doctor-refs' in args:
        check_refs = True

    if '--doctor-refs-strict' in args:
        refs_strict = True

    # COST headers
    if '--doctor-no-cost' in args:
        check_cost = False
    elif '--doctor-cost' in args:
        check_cost = True
    if '--doctor-cost-strict' in args:
        cost_strict = True

    # Forbidden patterns
    if '--doctor-no-forbidden' in args:
        check_forbidden = False
    elif '--doctor-forbidden' in args:
        check_forbidden = True

    # ASCII scan for build/bats
    if '--doctor-no-ascii' in args:
        check_ascii = False
    elif '--doctor-ascii' in args:
        check_ascii = True
    if '--doctor-ascii-strict' in args:
        ascii_strict = True

    if '--doctor-no-stubs' in args:
        check_stubs = False
    elif '--doctor-stubs' in args:
        check_stubs = True
    if '--doctor-stubs-strict' in args:
        stubs_strict = True

    if '--doctor-no-dialog-dupes' in args:
        check_dialog_duplicates = False
    elif '--doctor-dialog-dupes' in args:
        check_dialog_duplicates = True
    if '--doctor-dialog-dupes-strict' in args:
        dialog_duplicates_strict = True

    if '--doctor-strict' in args:
        strict_all = True
        refs_strict = True
        cost_strict = True
        ascii_strict = True
        stubs_strict = True
        dialog_duplicates_strict = True
    if '--doctor-new-only' in args:
        new_only = True

    res = run_doctor(
        check_duplicate_ids=check_duplicate_ids,
        check_refs=check_refs,
        refs_strict=refs_strict,
        check_cost=check_cost,
        cost_strict=cost_strict,
        check_forbidden=check_forbidden,
        check_ascii=check_ascii,
        ascii_strict=ascii_strict,
        check_stubs=check_stubs,
        stubs_strict=stubs_strict,
        check_dialog_duplicates=check_dialog_duplicates,
        dialog_duplicates_strict=dialog_duplicates_strict,
        check_generated_contract=check_generated_contract,
        check_generated_ids=check_generated_ids,
        strict_all=strict_all,
        new_only=new_only,
    )
    print(f"[doctor] Wrote {REPORT_PATH}")
    if res.errors:
        print(f"[doctor] FAIL: {len(res.errors)} error(s), {len(res.warnings)} warning(s).")
        raise SystemExit(1)
    print(f"[doctor] OK: {len(res.warnings)} warning(s).")

if __name__ == "__main__":
    main()
