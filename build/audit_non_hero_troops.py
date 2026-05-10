from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import statistics
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))

from header_items import (  # type: ignore
    blunt,
    get_body_armor,
    get_difficulty,
    get_head_armor,
    get_leg_armor,
    get_speed_rating,
    get_swing_damage,
    get_thrust_damage,
    get_weapon_length,
    iwf_damage_type_bits,
    itp_type_arrows,
    itp_type_body_armor,
    itp_type_bolts,
    itp_type_bow,
    itp_type_crossbow,
    itp_type_foot_armor,
    itp_type_hand_armor,
    itp_type_head_armor,
    itp_type_horse,
    itp_type_one_handed_wpn,
    itp_type_polearm,
    itp_type_shield,
    itp_type_thrown,
    itp_type_two_handed_wpn,
    pierce,
)
from header_skills import (  # type: ignore
    skl_athletics,
    skl_horse_archery,
    skl_ironflesh,
    skl_pathfinding,
    skl_power_draw,
    skl_power_strike,
    skl_power_throw,
    skl_riding,
    skl_shield,
    skl_spotting,
    skl_tactics,
    skl_trainer,
    skl_weapon_master,
)
from header_troops import (  # type: ignore
    tf_female,
    tf_guarantee_armor,
    tf_guarantee_boots,
    tf_guarantee_gloves,
    tf_guarantee_helmet,
    tf_guarantee_horse,
    tf_guarantee_ranged,
    tf_guarantee_shield,
    tf_hero,
    tf_inactive,
    tf_is_merchant,
    tf_mounted,
    tf_undead,
    tf_unmoveable_in_party_window,
)
import module_factions  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore
from module_constants import (  # type: ignore
    kt_troop_type_archer,
    kt_troop_type_cavalry,
    kt_troop_type_footsoldier,
    kt_troop_type_mtdarcher,
)


OUT_PATH = ROOT / "docs" / "reports" / "non_hero_troop_audit.md"
KT0_OUT_PATH = ROOT / "docs" / "reports" / "kt0_autoresolve_audit.md"

EXCLUDE_REASON_PATTERNS = [
    ("animal/non-troop party actor", re.compile(r"^cattle$")),
    ("scenario placeholder", re.compile(r"^farmer_from_bandit_village$")),
    ("script/log storage troop", re.compile(r"^log_array_")),
    ("range marker", re.compile(r"(^.*_begin$|^.*_end$)")),
    ("scene walker", re.compile(r"(^|_)walker(_|$)")),
    ("tutorial troop", re.compile(r"^tutorial_")),
    ("arena/training troop", re.compile(r"^(arena_|novice_fighter$|regular_fighter$|veteran_fighter$|champion_fighter$)")),
    ("prisoner placeholder", re.compile(r"_prisoner_")),
    ("hardcoded relative marker", re.compile(r"^relative_of_merchants")),
    ("multiplayer/quick battle troop", re.compile(r"^(multiplayer_|quick_battle_)")),
    ("temporary/code placeholder", re.compile(r"(^temp_|_temp$|placeholder)")),
]

ITEM_TYPE_TAGS = {
    itp_type_horse: "Horse",
    itp_type_one_handed_wpn: "1H",
    itp_type_two_handed_wpn: "2H",
    itp_type_polearm: "Pole",
    itp_type_arrows: "Arrows",
    itp_type_bolts: "Bolts",
    itp_type_shield: "Shield",
    itp_type_bow: "Bow",
    itp_type_crossbow: "Xbow",
    itp_type_thrown: "Throw",
    itp_type_head_armor: "Head",
    itp_type_body_armor: "Body",
    itp_type_foot_armor: "Foot",
    itp_type_hand_armor: "Hands",
}

FLAG_TAGS = [
    (tf_mounted, "tf_mounted"),
    (tf_guarantee_horse, "g_horse"),
    (tf_guarantee_shield, "g_shield"),
    (tf_guarantee_ranged, "g_ranged"),
    (tf_guarantee_armor, "g_armor"),
    (tf_guarantee_helmet, "g_helmet"),
    (tf_guarantee_boots, "g_boots"),
    (tf_guarantee_gloves, "g_gloves"),
    (tf_is_merchant, "merchant"),
    (tf_inactive, "inactive"),
    (tf_unmoveable_in_party_window, "unmoveable"),
    (tf_undead, "undead"),
    (tf_female, "female"),
]

PROF_NAMES = [
    ("1H", 0),
    ("2H", 10),
    ("Pole", 20),
    ("Arch", 30),
    ("Xbow", 40),
    ("Throw", 50),
    ("Fire", 60),
]

KEY_SKILLS = [
    ("IF", skl_ironflesh),
    ("PS", skl_power_strike),
    ("PD", skl_power_draw),
    ("PT", skl_power_throw),
    ("Ride", skl_riding),
    ("HA", skl_horse_archery),
    ("Ath", skl_athletics),
    ("Sh", skl_shield),
    ("WM", skl_weapon_master),
    ("Tac", skl_tactics),
    ("Path", skl_pathfinding),
    ("Spot", skl_spotting),
    ("Train", skl_trainer),
]

KT0_TYPE_LABELS = {
    kt_troop_type_footsoldier: "Foot",
    kt_troop_type_cavalry: "Cavalry",
    kt_troop_type_archer: "Archer",
    kt_troop_type_mtdarcher: "Mounted ranged",
}

PLAYER_SUBGROUPS = [
    ("Antarian", re.compile(r"^(sod_ant_|sod_peasant1)")),
    ("Marinian", re.compile(r"^(sod_mar_|sod_peasant2)")),
    ("Adenian", re.compile(r"^(sod_ade_|sod_peasant3)")),
    ("Villianese", re.compile(r"^(sod_vil_|sod_peasant4)")),
    ("Zerrikanian", re.compile(r"^(sod_zer_|sod_peasant5)")),
    ("Faith Orders", re.compile(r"^sod_faith")),
]

FAITH_SUBGROUPS = [
    ("Faith 1 - The One", re.compile(r"^sod_faith1_")),
    ("Faith 2 - Ancestors and Gods", re.compile(r"^sod_faith2_")),
    ("Faith 3 - The Void", re.compile(r"^sod_faith3_")),
    ("Faith 4 - The Boundless", re.compile(r"^sod_faith4_")),
    ("Faith 5 - Engineers and Specialists", re.compile(r"^sod_faith5_")),
]

NOBLE_FAITH_CONVERSIONS = {
    "sod_ant_honor_guard1": [
        "sod_faith1_foot",
        "sod_faith2_foot",
        "sod_faith3_foot",
        "sod_faith4_foot",
        "sod_faith5_foot",
    ],
    "sod_mar_condottieri1": [
        "sod_faith1_range_1",
        "sod_faith2_ranged_1",
        "sod_faith3_ranged_1",
        "sod_faith4_ranged_1",
        "sod_faith5_ranged_1",
    ],
    "sod_ade_magnate1": [
        "sod_faith1_mount",
        "sod_faith2_mount",
        "sod_faith3_mount",
        "sod_faith4_mount",
        "sod_faith5_mount",
    ],
    "sod_vil_high_chief1": [
        "sod_faith1_range_2",
        "sod_faith2_ranged_2",
        "sod_faith3_ranged_2",
        "sod_faith4_ranged_2",
        "sod_faith5_ranged_2",
    ],
    "sod_zer_3_noble1": [
        "sod_faith1_mount_range",
        "sod_faith2_mount_ranged",
        "sod_faith3_mount_ranged",
        "sod_faith4_mount_ranged",
        "sod_faith5_mount_ranged",
    ],
}


def md_escape(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def compact_list(values: list[str], empty: str = "-") -> str:
    return ", ".join(values) if values else empty


def compact_faith_targets(targets: list[str]) -> str:
    return ", ".join(target.replace("sod_", "") for target in targets)


def decode_attrs(attrs: int) -> dict[str, int]:
    return {
        "level": (attrs >> 32) & 0xFF,
        "str": attrs & 0xFF,
        "agi": (attrs >> 8) & 0xFF,
        "int": (attrs >> 16) & 0xFF,
        "cha": (attrs >> 24) & 0xFF,
    }


def decode_profs(profs: int) -> dict[str, int]:
    return {name: (profs >> bits) & 0x3FF for name, bits in PROF_NAMES}


def skill_value(skills: int, skill_id: int) -> int:
    return (skills >> (skill_id * 4)) & 0xF


def decode_skills(skills: int) -> dict[str, int]:
    return {name: skill_value(skills, skill_id) for name, skill_id in KEY_SKILLS}


def kt0_damage_value(raw_damage: int) -> float:
    pierce_flag = pierce << iwf_damage_type_bits
    blunt_flag = blunt << iwf_damage_type_bits
    if raw_damage & pierce_flag:
        return float(raw_damage & 0xFF) * 1.5
    if raw_damage & blunt_flag:
        return float(raw_damage & 0xFF) * 1.25
    return float(raw_damage & 0xFF)


def kt0_classify_type(flags: int, mw_value: float, rw_value: float, horse_value: float) -> int:
    guarantee_horse = bool(flags & tf_guarantee_horse)
    guarantee_ranged = bool(flags & tf_guarantee_ranged)
    if guarantee_horse and guarantee_ranged:
        return kt_troop_type_mtdarcher
    if guarantee_horse:
        return kt_troop_type_cavalry
    if guarantee_ranged:
        return kt_troop_type_archer
    if horse_value > 0 and rw_value > 0:
        return kt_troop_type_mtdarcher
    if horse_value > 0:
        return kt_troop_type_cavalry
    if rw_value > 0:
        return kt_troop_type_archer
    return kt_troop_type_footsoldier


def kt0_doctrine_multiplier(troop_id: str) -> tuple[int, int, list[str]]:
    notes: list[str] = []
    offense = 100
    defense = 100
    if troop_id.startswith("sod_faith"):
        offense = defense = 115
        notes.append("faith elite +15%")
    elif troop_id.startswith(("imperial_", "legion_")):
        offense = defense = 110
        notes.append("imperial endgame +10%")
    elif troop_id.startswith(
        (
            "black_army_",
            "conquistador_",
            "elephant_guard_",
            "jotnar_",
            "serpent_",
            "boar_",
            "slaver",
            "tormenter",
        )
    ):
        offense = defense = 105
        notes.append("mini-faction +5%")
    if troop_id.startswith(("slaver", "tormenter")):
        offense = int(offense * 95 / 100)
        notes.append("blunt capture -5% kill pressure")
    return offense, defense, notes


def kt0_context_values(offense: float, defense: float, horse: float, troop_type: int) -> dict[str, int]:
    def context(context_id: int) -> int:
        o_val = offense
        d_val = defense
        h_val = 0 if troop_type == kt_troop_type_mtdarcher else horse
        if context_id == 1:
            if troop_type == kt_troop_type_cavalry:
                o_val *= 3 / 5
                d_val *= 3 / 5
            elif troop_type == kt_troop_type_archer:
                o_val *= 4 / 3
                d_val *= 4 / 3
            elif troop_type == kt_troop_type_mtdarcher:
                o_val *= 6 / 5
                d_val *= 6 / 5
            else:
                o_val *= 6 / 5
                d_val *= 6 / 5
        elif context_id == 2:
            if troop_type == kt_troop_type_cavalry:
                o_val *= 4 / 5
                d_val *= 4 / 5
            elif troop_type == kt_troop_type_archer:
                o_val *= 6 / 5
                d_val *= 11 / 10
            elif troop_type == kt_troop_type_mtdarcher:
                o_val *= 5 / 4
                d_val *= 11 / 10
            else:
                o_val *= 11 / 10
                d_val *= 11 / 10
        else:
            if troop_type == kt_troop_type_cavalry:
                o_val *= 3 / 2
                d_val *= 3 / 2
            elif troop_type == kt_troop_type_archer:
                o_val *= 6 / 5
                d_val *= 11 / 10
            elif troop_type == kt_troop_type_mtdarcher:
                d_val *= 4 / 3
            else:
                o_val *= 11 / 10
                d_val *= 11 / 10
            o_val += h_val
        return max(0, int(round(o_val + d_val)))

    return {
        "open": context(0),
        "siege_attacker": context(2),
        "siege_defender": context(1),
    }


def kt0_band(value: int) -> str:
    if value >= 140:
        return "endgame"
    if value >= 100:
        return "elite"
    if value >= 70:
        return "veteran"
    if value >= 45:
        return "regular"
    if value > 0:
        return "low"
    return "zero"


def kt0_audit(troop_id: str, flags: int, inventory: list[int], attrs: dict[str, int], profs: dict[str, int], skills: dict[str, int]) -> dict[str, object]:
    mw_values: list[float] = []
    rw_values: list[float] = []
    head_values: list[float] = []
    body_values: list[float] = []
    foot_values: list[float] = []
    hand_values: list[float] = []
    shield_values: list[float] = []
    horse_values: list[float] = []

    for item_id in inventory:
        if not isinstance(item_id, int) or item_id < 0 or item_id >= len(module_items.items):
            continue
        item = module_items.items[item_id]
        item_type = item[3] & 0xFF
        stats = item[6]
        if item_type == itp_type_horse:
            horse_values.append(get_thrust_damage(stats) + ((get_body_armor(stats) + 5) / 10))
        elif item_type in (itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm):
            if item_type == itp_type_one_handed_wpn:
                prof = profs["1H"]
            elif item_type == itp_type_two_handed_wpn:
                prof = profs["2H"]
            else:
                prof = profs["Pole"]
            value = max(kt0_damage_value(get_swing_damage(stats)), kt0_damage_value(get_thrust_damage(stats)))
            value *= max(get_speed_rating(stats), 1)
            value *= max(prof, 1)
            value *= 100 + skills["PS"] * 8
            value /= 1000000
            mw_values.append(value)
        elif item_type in (itp_type_bow, itp_type_crossbow, itp_type_thrown):
            if item_type == itp_type_bow:
                prof = profs["Arch"]
                power_bonus = min(skills["PD"], get_difficulty(stats) + 4) * 14
            elif item_type == itp_type_crossbow:
                prof = profs["Xbow"]
                power_bonus = 0
            else:
                prof = profs["Throw"]
                power_bonus = skills["PT"] * 10
            value = kt0_damage_value(get_thrust_damage(stats))
            value *= max(get_leg_armor(stats), 100)
            value *= max(get_speed_rating(stats), 1)
            value *= max(prof, 1)
            value *= 100 + power_bonus
            value /= 100000000
            rw_values.append(value)
        elif item_type == itp_type_shield:
            shield_values.append(get_weapon_length(stats))
        elif item_type == itp_type_head_armor:
            head_values.append(get_head_armor(stats))
        elif item_type == itp_type_body_armor:
            body_values.append(get_body_armor(stats))
            foot_values.append(get_leg_armor(stats))
            head_values.append(get_head_armor(stats))
        elif item_type == itp_type_foot_armor:
            foot_values.append(get_leg_armor(stats))
        elif item_type == itp_type_hand_armor:
            hand_values.append(get_body_armor(stats))

    mw_value = statistics.mean(mw_values) if mw_values else 0
    rw_value = statistics.mean(rw_values) if rw_values else 0
    horse_value = statistics.mean(horse_values) if horse_values else 0
    shield_value = statistics.mean(shield_values) if shield_values else 0
    defense = (
        (statistics.mean(head_values) if head_values else 0)
        + (statistics.mean(body_values) if body_values else 0)
        + (statistics.mean(foot_values) if foot_values else 0)
        + (statistics.mean(hand_values) if hand_values else 0)
        + shield_value
    ) / 5
    defense += skills["IF"] * 2
    defense += attrs["str"]
    troop_type = kt0_classify_type(flags, mw_value, rw_value, horse_value)
    if troop_type in (kt_troop_type_mtdarcher, kt_troop_type_archer):
        offense = mw_value / 3 + rw_value
    else:
        offense = mw_value + rw_value / 4
    off_mult, def_mult, doctrine_notes = kt0_doctrine_multiplier(troop_id)
    offense = offense * off_mult / 100
    defense = defense * def_mult / 100
    values = kt0_context_values(offense, defense, horse_value, troop_type)
    warnings = list(doctrine_notes)
    if offense <= 0 and (mw_values or rw_values):
        warnings.append("zero offense despite weapons")
    elif offense <= 0 and troop_id not in {"player"}:
        warnings.append("zero combat offense")
    if defense <= 0 and (head_values or body_values or foot_values or hand_values):
        warnings.append("zero defense despite armor")
    if horse_value > 0 and troop_type not in (kt_troop_type_cavalry, kt_troop_type_mtdarcher):
        warnings.append("horse/type mismatch")
    if max(values.values()) >= 170:
        warnings.append("extreme autoresolve outlier")
    elif max(values.values()) >= 140:
        warnings.append("endgame autoresolve band")
    return {
        "type": KT0_TYPE_LABELS.get(troop_type, "Unknown"),
        "offense": int(round(offense)),
        "defense": int(round(defense)),
        "horse": int(round(horse_value)),
        "open": values["open"],
        "open_band": kt0_band(values["open"]),
        "siege_attacker": values["siege_attacker"],
        "siege_attacker_band": kt0_band(values["siege_attacker"]),
        "siege_defender": values["siege_defender"],
        "siege_defender_band": kt0_band(values["siege_defender"]),
        "warnings": warnings,
    }


def item_type_tags(inventory: list[int]) -> set[str]:
    tags: set[str] = set()
    for item_id in inventory:
        if not isinstance(item_id, int) or item_id < 0 or item_id >= len(module_items.items):
            continue
        item = module_items.items[item_id]
        flags = item[3]
        tag = ITEM_TYPE_TAGS.get(flags & 0xFF)
        if tag:
            tags.add(tag)
    return tags


def flag_tags(flags: int) -> list[str]:
    return [tag for mask, tag in FLAG_TAGS if flags & mask]


def classify_role(flags: int, gear: set[str], profs: dict[str, int]) -> str:
    mounted = bool(flags & (tf_mounted | tf_guarantee_horse)) or "Horse" in gear
    has_bow = "Bow" in gear or "Arrows" in gear
    has_xbow = "Xbow" in gear or "Bolts" in gear
    has_throw = "Throw" in gear
    has_ranged = bool(flags & tf_guarantee_ranged) or has_bow or has_xbow or has_throw
    has_melee = bool({"1H", "2H", "Pole"} & gear)

    if mounted and (has_bow or has_throw or has_xbow or profs["Arch"] >= 160):
        return "Mounted ranged"
    if mounted:
        return "Cavalry"
    if has_bow:
        return "Archer"
    if has_xbow:
        return "Crossbow"
    if has_throw:
        return "Skirmisher"
    if has_melee or has_ranged:
        return "Infantry"
    return "Noncombat/technical"


def parse_upgrades() -> dict[str, list[str]]:
    text = (COMPILE / "module_troops.py").read_text(encoding="utf-8", errors="replace")
    upgrades: dict[str, list[str]] = defaultdict(list)
    pattern = re.compile(
        r"upgrade2?\(troops,\s*\"([^\"]+)\",\s*\"([^\"]+)\"(?:,\s*\"([^\"]+)\")?\)"
    )
    for match in pattern.finditer(text):
        source, first, second = match.groups()
        upgrades[source].append(first)
        if second:
            upgrades[source].append(second)
    return upgrades


def exclusion_reason(troop_id: str) -> str | None:
    for reason, pattern in EXCLUDE_REASON_PATTERNS:
        if pattern.search(troop_id):
            return reason
    return None


def troop_note(
    troop_id: str,
    troop_name: str,
    role: str,
    attrs: dict[str, int],
    profs: dict[str, int],
    upgrades: list[str],
    faith_conversions: list[str],
) -> str:
    notes: list[str] = []
    is_equipment_variant = troop_name.endswith("*")
    if troop_id.endswith("_begin") or troop_id.endswith("_end") or "placeholder" in troop_id:
        notes.append("technical marker")
    if is_equipment_variant:
        notes.append("equipment-upgraded variant")
    if faith_conversions:
        notes.append("faith conversion candidate")
    if attrs["level"] >= 30:
        notes.append("elite level")
    if max(profs.values()) >= 300:
        notes.append("elite proficiency")
    if role == "Mounted ranged":
        notes.append("mobile ranged pressure")
    if len(upgrades) > 1:
        notes.append("split upgrade")
    elif not upgrades and not faith_conversions and not is_equipment_variant and role != "Noncombat/technical":
        notes.append("terminal")
    if role == "Noncombat/technical" and attrs["level"] > 10:
        notes.append("noncombat but leveled")
    return compact_list(notes)


def faction_name(faction_id: int) -> tuple[str, str]:
    if 0 <= faction_id < len(module_factions.factions):
        record = module_factions.factions[faction_id]
        return record[0], record[1]
    return f"unknown_{faction_id}", f"Unknown {faction_id}"


def player_subgroup(troop_id: str) -> str:
    for label, pattern in PLAYER_SUBGROUPS:
        if pattern.search(troop_id):
            return label
    return "Other Player Troops"


def faith_subgroup(troop_id: str) -> str:
    for label, pattern in FAITH_SUBGROUPS:
        if pattern.search(troop_id):
            return label
    return "Other Faith Troops"


def player_culture_line(troop_id: str, culture: str) -> str:
    noble_patterns = {
        "Antarian": re.compile(r"^sod_ant_(noble|guard|honor_guard)"),
        "Marinian": re.compile(r"^sod_mar_(mercenary|landsknecht|condottieri)"),
        "Adenian": re.compile(r"^sod_ade_(sqire|knight|magnate)"),
        "Villianese": re.compile(r"^sod_vil_(noble|chief|high_chief)"),
        "Zerrikanian": re.compile(r"^sod_zer_[123]_noble"),
    }
    pattern = noble_patterns.get(culture)
    if pattern and pattern.search(troop_id):
        return "Noble Troops"
    return "Normal Troops"


def assign_upgrade_tiers(rows: list[dict[str, object]]) -> None:
    base_rows = [row for row in rows if not row["equipment_variant"]]
    row_by_id = {str(row["id"]): row for row in base_rows}
    parent_ids = {
        child_id
        for row in base_rows
        for child_id in row["upgrades"]  # type: ignore[operator]
        if child_id in row_by_id
    }
    roots = [row for row in base_rows if str(row["id"]) not in parent_ids]
    for row in rows:
        row["tier"] = 0
        row["upgrade_depth"] = 0

    def walk(row: dict[str, object], tier: int, stack: set[str]) -> None:
        troop_id = str(row["id"])
        if troop_id in stack:
            return
        row["tier"] = max(int(row.get("tier", 0)), tier)
        for child_id in row["upgrades"]:  # type: ignore[operator]
            child = row_by_id.get(child_id)
            if child:
                walk(child, tier + 1, stack | {troop_id})

    for root in roots:
        walk(root, 1, set())

    child_depths: dict[str, int] = {}

    def depth(row: dict[str, object], stack: set[str]) -> int:
        troop_id = str(row["id"])
        if troop_id in child_depths:
            return child_depths[troop_id]
        if troop_id in stack:
            return 0
        children = [row_by_id[child_id] for child_id in row["upgrades"] if child_id in row_by_id]  # type: ignore[operator]
        value = 0 if not children else 1 + max(depth(child, stack | {troop_id}) for child in children)
        child_depths[troop_id] = value
        return value

    for row in base_rows:
        row["upgrade_depth"] = depth(row, set())

    base_by_id = {str(row["id"]): row for row in base_rows}
    for row in rows:
        if row["equipment_variant"]:
            base = base_by_id.get(str(row["base_troop_id"]))
            if base:
                row["tier"] = base["tier"]
                row["upgrade_depth"] = base["upgrade_depth"]


def build_rows() -> tuple[list[dict[str, object]], Counter[str]]:
    upgrades = parse_upgrades()
    troop_ids = {troop[0] for troop in module_troops.troops}
    rows: list[dict[str, object]] = []
    excluded: Counter[str] = Counter()
    for troop in module_troops.troops:
        troop_id, name, plural, flags, scene, reserved, faction_id, inventory, attrs_raw, profs_raw, skills_raw = troop[:11]
        if flags & tf_hero:
            continue
        reason = exclusion_reason(troop_id)
        if reason:
            excluded[reason] += 1
            continue
        attrs = decode_attrs(attrs_raw)
        profs = decode_profs(profs_raw)
        skills = decode_skills(skills_raw)
        gear = item_type_tags(inventory)
        role = classify_role(flags, gear, profs)
        is_equipment_variant = str(name).endswith("*")
        base_troop_id = troop_id[:-1] if is_equipment_variant and troop_id[:-1] in troop_ids else troop_id
        direct_upgrades = upgrades.get(troop_id, [])
        if is_equipment_variant and not direct_upgrades:
            direct_upgrades = upgrades.get(base_troop_id, [])
        faith_key = troop_id if is_equipment_variant else f"{troop_id}1"
        faith_conversions = NOBLE_FAITH_CONVERSIONS.get(faith_key, [])
        fac_id, fac_name = faction_name(faction_id)
        rows.append(
            {
                "id": troop_id,
                "name": name,
                "plural": plural,
                "flags": flags,
                "faction_idx": faction_id,
                "faction_id": fac_id,
                "faction_name": fac_name,
                "level": attrs["level"],
                "attrs": attrs,
                "profs": profs,
                "skills": skills,
                "gear": sorted(gear),
                "flag_tags": flag_tags(flags),
                "role": role,
                "kt0": kt0_audit(troop_id, flags, inventory, attrs, profs, skills),
                "equipment_variant": is_equipment_variant,
                "base_troop_id": base_troop_id,
                "tier": 0,
                "upgrade_depth": 0,
                "faith_conversions": faith_conversions,
                "upgrades": direct_upgrades,
                "notes": troop_note(troop_id, name, role, attrs, profs, direct_upgrades, faith_conversions),
            }
        )
    assign_upgrade_tiers(rows)
    return rows, excluded


def format_skill_summary(skills: dict[str, int]) -> str:
    visible = [f"{name}{value}" for name, value in skills.items() if value]
    return compact_list(visible)


def format_prof_summary(profs: dict[str, int]) -> str:
    return " ".join(f"{name}{value}" for name, value in profs.items() if name != "Fire" or value)


def append_faction_summary(lines: list[str], faction_rows: list[dict[str, object]]) -> None:
    faction_levels = [int(row["level"]) for row in faction_rows]
    faction_roles = Counter(str(row["role"]) for row in faction_rows)
    terminal_count = sum(
        1
        for row in faction_rows
        if not row["upgrades"]
        and not row["faith_conversions"]
        and row["role"] != "Noncombat/technical"
        and not row["equipment_variant"]
    )
    split_count = sum(1 for row in faction_rows if len(row["upgrades"]) > 1)
    lines.append(f"- Troops: {len(faction_rows)}")
    lines.append(
        f"- Level range: {min(faction_levels)}-{max(faction_levels)}; average level: {statistics.mean(faction_levels):.1f}"
    )
    lines.append("- Roles: " + compact_list([f"{role} {count}" for role, count in faction_roles.most_common()]))
    lines.append(f"- Direct upgrade terminals: {terminal_count}; split upgrades: {split_count}")


def append_troop_table(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append(
        "| Troop ID | Name | Tier | Lvl | Role | KT0 | Attrs | Profs | Skills | Gear/Flags | Direct upgrades | Notes |"
    )
    lines.append("|---|---|---:|---:|---|---|---|---|---|---|---|---|")
    for row in rows:
        attrs = row["attrs"]  # type: ignore[assignment]
        kt0 = row["kt0"]  # type: ignore[assignment]
        gear_flags = list(row["gear"]) + [f"[{tag}]" for tag in row["flag_tags"]]  # type: ignore[operator]
        lines.append(
            "| {id} | {name} | {tier} | {level} | {role} | {kt0} | {attrs} | {profs} | {skills} | {gear} | {upgrades} | {notes} |".format(
                id=md_escape(row["id"]),
                name=md_escape(row["name"]),
                tier=row["tier"],
                level=row["level"],
                role=md_escape(row["role"]),
                kt0=md_escape(
                    "{type} O{offense}/D{defense}/H{horse}; F {open} {open_band}; SA {siege_attacker} {siege_attacker_band}; SD {siege_defender} {siege_defender_band}".format(
                        **kt0  # type: ignore[arg-type]
                    )
                ),
                attrs=md_escape(
                    "STR{str} AGI{agi} INT{int} CHA{cha}".format(**attrs)  # type: ignore[arg-type]
                ),
                profs=md_escape(format_prof_summary(row["profs"])),  # type: ignore[arg-type]
                skills=md_escape(format_skill_summary(row["skills"])),  # type: ignore[arg-type]
                gear=md_escape(compact_list(gear_flags)),
                upgrades=md_escape(compact_list(row["upgrades"])),  # type: ignore[arg-type]
                notes=md_escape(row["notes"]),
            )
        )


def append_autoresolve_notes(lines: list[str], rows: list[dict[str, object]]) -> None:
    watched = [
        ("Imperial Expeditionary Force", lambda row: str(row["faction_id"]) == "kingdom_6" or str(row["id"]).startswith(("imperial_", "legion_"))),
        ("Faith Orders", lambda row: str(row["id"]).startswith("sod_faith")),
        ("Mercenary Mini-Factions", lambda row: str(row["faction_id"]).startswith("sod_merc_guild")),
        ("Black Khergits", lambda row: "black_khergit" in str(row["id"]) or str(row["faction_id"]) == "black_khergits"),
        ("Homeland Nobles", lambda row: "faith conversion candidate" in str(row["notes"]) or player_culture_line(str(row["id"]), player_subgroup(str(row["id"]))) == "Noble Troops"),
    ]

    all_warnings = [
        row for row in rows if row["kt0"]["warnings"]  # type: ignore[index]
    ]
    top_rows = sorted(
        rows,
        key=lambda row: max(
            int(row["kt0"]["open"]),  # type: ignore[index]
            int(row["kt0"]["siege_attacker"]),  # type: ignore[index]
            int(row["kt0"]["siege_defender"]),  # type: ignore[index]
        ),
        reverse=True,
    )[:30]

    lines.append("## Autoresolve Balance Notes")
    lines.append("")
    lines.append(
        "KT0 values are audit estimates matching the initialization model: offense/defense/horse slots, troop type, and open-field/siege context bands. "
        "They are meant to expose balance pressure, not replace in-game testing."
    )
    lines.append("")
    lines.append("| Watch area | Troops | Peak field | Peak siege attack | Peak siege defense | Notes |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for label, predicate in watched:
        subset = [row for row in rows if predicate(row)]
        if not subset:
            continue
        peak_open = max(int(row["kt0"]["open"]) for row in subset)  # type: ignore[index]
        peak_attack = max(int(row["kt0"]["siege_attacker"]) for row in subset)  # type: ignore[index]
        peak_defense = max(int(row["kt0"]["siege_defender"]) for row in subset)  # type: ignore[index]
        warnings = Counter(
            warning
            for row in subset
            for warning in row["kt0"]["warnings"]  # type: ignore[index]
        )
        lines.append(
            f"| {md_escape(label)} | {len(subset)} | {peak_open} | {peak_attack} | {peak_defense} | {md_escape(compact_list([f'{name} {count}' for name, count in warnings.most_common(3)]))} |"
        )
    lines.append("")
    lines.append("### KT0 Top Pressure")
    lines.append("")
    lines.append("| Troop | Faction | Type | Field | Siege attack | Siege defense | Warnings |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for row in top_rows:
        kt0 = row["kt0"]  # type: ignore[assignment]
        lines.append(
            "| {id} | {faction} | {type} | {field} | {attack} | {defense} | {warnings} |".format(
                id=md_escape(row["id"]),
                faction=md_escape(row["faction_name"]),
                type=md_escape(kt0["type"]),  # type: ignore[index]
                field=kt0["open"],  # type: ignore[index]
                attack=kt0["siege_attacker"],  # type: ignore[index]
                defense=kt0["siege_defender"],  # type: ignore[index]
                warnings=md_escape(compact_list(kt0["warnings"])),  # type: ignore[index]
            )
        )
    lines.append("")
    if all_warnings:
        lines.append("### KT0 Watchlist")
        lines.append("")

    structural_rows = [
        row
        for row in rows
        if any(
            warning in row["kt0"]["warnings"]  # type: ignore[index]
            for warning in ("zero offense despite weapons", "zero combat offense", "zero defense despite armor", "horse/type mismatch")
        )
    ]
    if structural_rows:
        lines.append("### KT0 Structural Issues")
        lines.append("")
        lines.append("| Troop | Faction | Role | Gear | KT0 | Issue |")
        lines.append("|---|---|---|---|---|---|")
        for row in sorted(structural_rows, key=lambda item: (str(item["faction_name"]), str(item["id"]))):
            kt0 = row["kt0"]  # type: ignore[assignment]
            issues = [
                warning
                for warning in kt0["warnings"]  # type: ignore[index]
                if warning in {"zero offense despite weapons", "zero combat offense", "zero defense despite armor", "horse/type mismatch"}
            ]
            lines.append(
                "| {id} | {faction} | {role} | {gear} | {kt0} | {issues} |".format(
                    id=md_escape(row["id"]),
                    faction=md_escape(row["faction_name"]),
                    role=md_escape(row["role"]),
                    gear=md_escape(compact_list(row["gear"])),  # type: ignore[arg-type]
                    kt0=md_escape(f"{kt0['type']} O{kt0['offense']}/D{kt0['defense']}/H{kt0['horse']}"),  # type: ignore[index]
                    issues=md_escape(compact_list(issues)),
                )
            )
        lines.append("")
        lines.append("| Troop | Faction | Type | Warning |")
        lines.append("|---|---|---|---|")
        for row in sorted(all_warnings, key=lambda item: (str(item["faction_name"]), str(item["id"]))):
            kt0 = row["kt0"]  # type: ignore[assignment]
            lines.append(
                f"| {md_escape(row['id'])} | {md_escape(row['faction_name'])} | {md_escape(kt0['type'])} | {md_escape(compact_list(kt0['warnings']))} |"  # type: ignore[index]
            )
        lines.append("")


def write_kt0_report(rows: list[dict[str, object]]) -> None:
    warning_rows = [row for row in rows if row["kt0"]["warnings"]]  # type: ignore[index]
    zero_offense = [
        row
        for row in rows
        if int(row["kt0"]["offense"]) == 0  # type: ignore[index]
        and str(row["role"]) != "Noncombat/technical"
        and any(warning in row["kt0"]["warnings"] for warning in ("zero offense despite weapons", "zero combat offense"))  # type: ignore[index]
    ]
    zero_defense = [
        row
        for row in rows
        if int(row["kt0"]["defense"]) == 0  # type: ignore[index]
        and ("Armor" in " ".join(row["gear"]) or "Shield" in row["gear"])  # type: ignore[operator]
    ]
    horse_mismatch = [
        row
        for row in rows
        if int(row["kt0"]["horse"]) > 0  # type: ignore[index]
        and row["kt0"]["type"] not in {"Cavalry", "Mounted ranged"}  # type: ignore[index]
    ]
    top_rows = sorted(
        rows,
        key=lambda row: max(
            int(row["kt0"]["open"]),  # type: ignore[index]
            int(row["kt0"]["siege_attacker"]),  # type: ignore[index]
            int(row["kt0"]["siege_defender"]),  # type: ignore[index]
        ),
        reverse=True,
    )[:75]

    lines: list[str] = []
    lines.append("# KT0 Autoresolve Audit")
    lines.append("")
    lines.append(
        "Generated alongside the non-hero troop audit. Values estimate KT0 slot outputs and context strength bands for balance review."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Audited non-hero troops: {len(rows)}")
    lines.append(f"- Rows with KT0 warnings: {len(warning_rows)}")
    lines.append(f"- Combat rows with zero offense: {len(zero_offense)}")
    lines.append(f"- Armored/shield rows with zero defense: {len(zero_defense)}")
    lines.append(f"- Horse/type mismatches: {len(horse_mismatch)}")
    lines.append("")
    lines.append("## Top KT0 Pressure")
    lines.append("")
    lines.append("| Troop | Faction | Type | O | D | H | Field | Siege attack | Siege defense | Warnings |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|")
    for row in top_rows:
        kt0 = row["kt0"]  # type: ignore[assignment]
        lines.append(
            "| {id} | {faction} | {type} | {offense} | {defense} | {horse} | {field} | {attack} | {defense_ctx} | {warnings} |".format(
                id=md_escape(row["id"]),
                faction=md_escape(row["faction_name"]),
                type=md_escape(kt0["type"]),  # type: ignore[index]
                offense=kt0["offense"],  # type: ignore[index]
                defense=kt0["defense"],  # type: ignore[index]
                horse=kt0["horse"],  # type: ignore[index]
                field=kt0["open"],  # type: ignore[index]
                attack=kt0["siege_attacker"],  # type: ignore[index]
                defense_ctx=kt0["siege_defender"],  # type: ignore[index]
                warnings=md_escape(compact_list(kt0["warnings"])),  # type: ignore[index]
            )
        )
    lines.append("")
    lines.append("## Warning Rows")
    lines.append("")
    lines.append("| Troop | Faction | Type | Field | Siege attack | Siege defense | Warnings |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for row in sorted(warning_rows, key=lambda item: (str(item["faction_name"]), str(item["id"]))):
        kt0 = row["kt0"]  # type: ignore[assignment]
        lines.append(
            "| {id} | {faction} | {type} | {field} | {attack} | {defense} | {warnings} |".format(
                id=md_escape(row["id"]),
                faction=md_escape(row["faction_name"]),
                type=md_escape(kt0["type"]),  # type: ignore[index]
                field=kt0["open"],  # type: ignore[index]
                attack=kt0["siege_attacker"],  # type: ignore[index]
                defense=kt0["siege_defender"],  # type: ignore[index]
                warnings=md_escape(compact_list(kt0["warnings"])),  # type: ignore[index]
            )
        )
    lines.append("")
    lines.append("## Balance Interpretation")
    lines.append("")
    lines.append("- `extreme autoresolve outlier` is a review flag, not an automatic bug; Imperial and faith elites are expected to appear here.")
    lines.append("- Zero offense/defense and horse/type mismatches are structural issues and should usually be fixed before balance tuning.")
    lines.append("- Mini-faction rows should cluster below Imperial/faith peaks unless their world role is explicitly endgame pressure.")
    lines.append("")

    KT0_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    KT0_OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def troop_tree_label(row: dict[str, object], variant_by_base: dict[str, dict[str, object]]) -> str:
    label = f"{row['id']} ({row['name']}, L{row['level']})"
    variant = variant_by_base.get(str(row["id"]))
    if variant:
        label += f" + {variant['id']} ({variant['name']}, equipment variant)"
        if variant["faith_conversions"]:
            label += " => faith variants"
    elif row["faith_conversions"]:
        label += " => faith variants"
    return label


def append_tree_node(
    lines: list[str],
    row: dict[str, object],
    row_by_id: dict[str, dict[str, object]],
    variant_by_base: dict[str, dict[str, object]],
    prefix: str = "",
    is_last: bool = True,
    stack: set[str] | None = None,
) -> None:
    stack = set() if stack is None else stack
    troop_id = str(row["id"])
    connector = "`-- " if is_last else "|-- "
    lines.append(prefix + connector + troop_tree_label(row, variant_by_base))
    if troop_id in stack:
        lines.append(prefix + ("    " if is_last else "|   ") + "`-- cycle stopped")
        return

    child_ids = [child_id for child_id in row["upgrades"] if child_id in row_by_id]  # type: ignore[operator]
    next_prefix = prefix + ("    " if is_last else "|   ")
    for index, child_id in enumerate(child_ids):
        append_tree_node(
            lines,
            row_by_id[child_id],
            row_by_id,
            variant_by_base,
            prefix=next_prefix,
            is_last=index == len(child_ids) - 1,
            stack=stack | {troop_id},
        )


def append_upgrade_trees(lines: list[str], rows: list[dict[str, object]]) -> None:
    base_rows = [row for row in rows if not row["equipment_variant"]]
    row_by_id = {str(row["id"]): row for row in base_rows}
    variant_by_base = {
        str(row["base_troop_id"]): row
        for row in rows
        if row["equipment_variant"] and str(row["base_troop_id"]) in row_by_id
    }
    parent_ids = {
        child_id
        for row in base_rows
        for child_id in row["upgrades"]  # type: ignore[operator]
        if child_id in row_by_id
    }
    roots = [row for row in base_rows if str(row["id"]) not in parent_ids]
    roots.sort(key=lambda row: (int(row["faction_idx"]), str(row["faction_name"]), int(row["level"]), str(row["id"])))

    roots_by_faction: dict[tuple[int, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in roots:
        key = (int(row["faction_idx"]), str(row["faction_id"]), str(row["faction_name"]))
        roots_by_faction[key].append(row)

    lines.append("## Upgrade Tree Visuals")
    lines.append("")
    lines.append(
        "Simple class-upgrade trees built from direct upgrade declarations. "
        "`*` rows are shown inline as equipment-upgraded variants of their base troop. "
        "Roots without class upgrades are collapsed into `Standalone` lists."
    )
    lines.append("")
    lines.append("Faith conversion note: top noble equipment variants are not standalone endpoints. They can convert into one faith-order variant based on the active player faith.")
    lines.append("")
    lines.append("| Noble equipment variant | Faith conversion options |")
    lines.append("|---|---|")
    for noble_id, targets in NOBLE_FAITH_CONVERSIONS.items():
        lines.append(f"| `{noble_id}` | {md_escape(compact_faith_targets(targets))} |")
    lines.append("")
    for faction_idx, faction_id, faction_name in sorted(roots_by_faction):
        faction_roots = roots_by_faction[(faction_idx, faction_id, faction_name)]
        tree_roots = [row for row in faction_roots if int(row["upgrade_depth"]) > 0]
        standalone_roots = [row for row in faction_roots if int(row["upgrade_depth"]) == 0]
        lines.append(f"### {md_escape(faction_name)} (`{faction_id}`)")
        lines.append("")
        if tree_roots:
            lines.append("```text")
            for root_index, root in enumerate(tree_roots):
                append_tree_node(
                    lines,
                    root,
                    row_by_id,
                    variant_by_base,
                    is_last=root_index == len(tree_roots) - 1,
                )
            lines.append("```")
            lines.append("")
        if standalone_roots:
            standalone = [
                troop_tree_label(row, variant_by_base)
                for row in sorted(standalone_roots, key=lambda item: (int(item["level"]), str(item["id"])))
            ]
            lines.append("Standalone: " + "; ".join(standalone))
        lines.append("")


def write_report(rows: list[dict[str, object]], excluded: Counter[str]) -> None:
    heroes = sum(1 for troop in module_troops.troops if troop[3] & tf_hero)
    excluded_count = sum(excluded.values())
    nonheroes = len(rows)
    levels = [int(row["level"]) for row in rows]
    roles = Counter(str(row["role"]) for row in rows)
    by_faction: dict[tuple[int, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        key = (int(row["faction_idx"]), str(row["faction_id"]), str(row["faction_name"]))
        by_faction[key].append(row)

    lines: list[str] = []
    lines.append("# Non-Hero Troop Audit")
    lines.append("")
    lines.append(
        "Generated from `compile/module_troops.py`, `compile/module_factions.py`, and `compile/module_items.py`. "
        "This file is intended as a balancing reference, so troops are grouped by faction first and then sorted by level and troop id."
    )
    lines.append("")
    lines.append("## Scope and Method")
    lines.append("")
    lines.append("- Includes compiled troops whose flags do not include `tf_hero` and that appear to represent real balance-relevant troops.")
    lines.append("- Excludes obvious code/storage, range-marker, tutorial, arena-training, prisoner-placeholder, multiplayer/quick-battle, temporary, and scene-walker entries.")
    lines.append("- Decodes level, attributes, weapon proficiencies, selected combat/party skills, equipment type tags, guarantee flags, and direct upgrade targets.")
    lines.append("- Derives `Tier` from upgrade-tree depth: root troops start at tier 1, and each class upgrade increases the tier by one.")
    lines.append("- Role labels are heuristic balance aids derived from equipment, guarantees, mounted flags, and ranged proficiencies.")
    lines.append("- Treats `*` troops as equipment-upgraded variants; their class upgrade targets are inherited from their base troop when generated that way.")
    lines.append("- Splits the Player Faction into its main culture subgroups, with Faith Orders further split into the five faith lines.")
    lines.append("- Within each Player Faction culture, separates the regular recruitment tree from the noble troop line.")
    if excluded:
        lines.append("- Excluded entries by reason: " + compact_list([f"{reason} {count}" for reason, count in excluded.most_common()]))
    lines.append("")
    lines.append("## Global Summary")
    lines.append("")
    lines.append(f"- Total compiled troops: {len(module_troops.troops)}")
    lines.append(f"- Non-hero troops audited: {nonheroes}")
    lines.append(f"- Obvious code/non-balancing entries excluded: {excluded_count}")
    lines.append(f"- Hero troops excluded: {heroes}")
    lines.append(f"- Factions represented: {len(by_faction)}")
    lines.append(f"- Level range: {min(levels)}-{max(levels)}; average level: {statistics.mean(levels):.1f}")
    lines.append("- Role counts: " + compact_list([f"{role} {count}" for role, count in roles.most_common()]))
    lines.append("")
    lines.append("## Global Balance Watchlist")
    lines.append("")
    elite_rows = sorted(
        rows,
        key=lambda row: (int(row["level"]), max(row["profs"].values())),  # type: ignore[index, union-attr]
        reverse=True,
    )[:25]
    lines.append("| Troop | Faction | Lvl | Role | Top prof | Notes |")
    lines.append("|---|---|---:|---|---:|---|")
    for row in elite_rows:
        profs = row["profs"]  # type: ignore[assignment]
        top_prof = max(profs.items(), key=lambda item: item[1])  # type: ignore[union-attr]
        lines.append(
            "| {id} | {faction} | {level} | {role} | {prof} | {notes} |".format(
                id=md_escape(row["id"]),
                faction=md_escape(row["faction_name"]),
                level=row["level"],
                role=md_escape(row["role"]),
                prof=md_escape(f"{top_prof[0]} {top_prof[1]}"),
                notes=md_escape(row["notes"]),
            )
        )
    lines.append("")

    append_autoresolve_notes(lines, rows)

    for (faction_idx, faction_id, display_name), faction_rows in sorted(by_faction.items()):
        faction_rows.sort(key=lambda row: (int(row["level"]), str(row["id"])))
        lines.append(f"## {md_escape(display_name)} (`{faction_id}`, index {faction_idx})")
        lines.append("")
        append_faction_summary(lines, faction_rows)
        lines.append("")
        if faction_id == "player_supporters_faction":
            subgroup_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
            for row in faction_rows:
                subgroup_rows[player_subgroup(str(row["id"]))].append(row)
            subgroup_order = [label for label, _pattern in PLAYER_SUBGROUPS] + ["Other Player Troops"]
            for subgroup in subgroup_order:
                rows_for_group = subgroup_rows.get(subgroup, [])
                if not rows_for_group:
                    continue
                lines.append(f"### {subgroup}")
                lines.append("")
                append_faction_summary(lines, rows_for_group)
                lines.append("")
                if subgroup in {"Antarian", "Marinian", "Adenian", "Villianese", "Zerrikanian"}:
                    culture_lines: dict[str, list[dict[str, object]]] = defaultdict(list)
                    for row in rows_for_group:
                        culture_lines[player_culture_line(str(row["id"]), subgroup)].append(row)
                    for culture_line in ["Normal Troops", "Noble Troops"]:
                        rows_for_line = culture_lines.get(culture_line, [])
                        if not rows_for_line:
                            continue
                        lines.append(f"#### {culture_line}")
                        lines.append("")
                        append_faction_summary(lines, rows_for_line)
                        lines.append("")
                        append_troop_table(lines, rows_for_line)
                        lines.append("")
                elif subgroup == "Faith Orders":
                    faith_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
                    for row in rows_for_group:
                        faith_rows[faith_subgroup(str(row["id"]))].append(row)
                    faith_order = [label for label, _pattern in FAITH_SUBGROUPS] + ["Other Faith Troops"]
                    for faith_group in faith_order:
                        rows_for_faith = faith_rows.get(faith_group, [])
                        if not rows_for_faith:
                            continue
                        lines.append(f"#### {faith_group}")
                        lines.append("")
                        append_faction_summary(lines, rows_for_faith)
                        lines.append("")
                        append_troop_table(lines, rows_for_faith)
                        lines.append("")
                else:
                    append_troop_table(lines, rows_for_group)
                lines.append("")
        else:
            append_troop_table(lines, faction_rows)
        lines.append("")

    append_upgrade_trees(lines, rows)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows, excluded = build_rows()
    write_report(rows, excluded)
    write_kt0_report(rows)
    print(
        f"Wrote {OUT_PATH.relative_to(ROOT)} "
        f"({len(rows)} non-hero troops, {sum(excluded.values())} obvious non-troop entries excluded)."
    )
    print(f"Wrote {KT0_OUT_PATH.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
