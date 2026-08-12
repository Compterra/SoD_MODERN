# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SAFE_DIALOGUE_TERMINALS = {
    "close_window",
    "close_window.",
    "close_window_1",
    "close_window_2",
    "close_window_3",
    "close_window_4",
    "close_window_5",
    "close_window_6",
    "close_window_7",
    "close_window_8",
    "close_window_9",
}
KNOWN_EXTERNAL_OR_LEGACY_STATES = {
    # Native/common companion and encounter states can be entered by engine
    # dialogue setup or legacy common-dialogue fragments that are not cleanly
    # represented as one-state-per-file modern fragments yet. Keep these
    # explicit so newly removed bespoke states still fail loudly.
    "companion_quitting",
    "companion_personalitymatch_b",
    "companion_recruit_backstory_a",
    "companion_recruit_backstory_b",
    "companion_recruit_signup",
    "companion_rehire_refused",
    "member_wilderness_talk",
    "member_inn_talk",
    "party_encounter_hostile_defender",
    "cpsq_0",
    "sh_spy_liberated_battle",
}


def parse_dialogue_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    dialog_re = re.compile(
        r"\[\s*([^,\]]+)\s*,\s*\"([^\"]+)\"\s*,\s*(\[[\s\S]*?\])\s*,\s*\"([\s\S]*?)\"\s*,\s*\"([^\"]+)\"\s*,\s*(\[[\s\S]*?\])\s*,",
        re.M,
    )
    for path in iter_source_files("src/dialogs"):
        if path.name.startswith("_"):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        for match in dialog_re.finditer(raw):
            speaker, state_in, conditions, text, state_out, consequences = match.groups()
            entries.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "speaker": speaker.strip(),
                    "state_in": state_in,
                    "conditions": conditions,
                    "text": text,
                    "state_out": state_out,
                    "consequences": consequences,
                    "raw": match.group(0),
                }
            )
    return entries


def is_player_speaker(speaker: str) -> bool:
    return "plyr" in speaker.split("|")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists() and path.startswith("docs/reports/"):
        matches = sorted((ROOT / "docs" / "reports").rglob(Path(path).name))
        if len(matches) == 1:
            target = matches[0]
    return target.read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    assert needle in raw, f"missing token: {needle}"


def assert_not_contains(raw: str, needle: str) -> None:
    assert needle not in raw, f"unexpected token: {needle}"


def iter_ordered_files(order_path: str) -> list[str]:
    lines = []
    for line in read(order_path).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    return lines


def iter_source_files(root: str) -> list[Path]:
    return [
        path
        for path in (ROOT / root).rglob("*.py")
        if "__pycache__" not in path.parts
    ]


def operation_hits(roots: tuple[str, ...], pattern: str) -> list[tuple[str, int, str]]:
    rx = re.compile(pattern)
    hits = []
    for root in roots:
        for path in iter_source_files(root):
            for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if rx.search(stripped):
                    hits.append((str(path.relative_to(ROOT)).replace("\\", "/"), line_no, stripped))
    return hits


def test_modernization_checklist_structure() -> None:
    raw = read("docs/tooling/MODULE_SYSTEM_MODERNIZATION_CHECKLIST.md")
    for heading in (
        "# Module System Modernization Checklist",
        "## Phase 1: Dialogue And Encounter Safety",
        "## Phase 2: Party, Troop, And Center ID Safety",
        "## Phase 3: Menus, Reports, And Presentation Safety",
        "## Phase 4: Campaign AI Modernization",
        "## Phase 5: Quest Framework Modernization",
        "## Phase 6: Companion And Incident Modernization",
        "## Phase 7: Mini-Faction Modernization",
        "## Phase 8: Economy, Trade, And Company Systems",
        "## Phase 9: Builder, Doctor, And Tooling",
        "## First Implementation Slice: Dialogue + Encounter Safety",
        "## Recently Fixed Old Bugs",
        "## Build Gate",
    ):
        assert_contains(raw, heading)


def test_modernization_checklist_tracks_known_bug_families() -> None:
    raw = read("docs/tooling/MODULE_SYSTEM_MODERNIZATION_CHECKLIST.md")
    for token in (
        "IEF dying Centurion",
        "Court lady honor duel",
        "invalid party `-1`",
        "Chancellor lord recruitment",
        "Jester cheat",
        "Formation reset",
        "game_event_party_encounter",
        "change_screen_return",
        "finish_mission",
        "cpdla_nihilistic_11",
    ):
        assert_contains(raw, token)


def test_first_slice_has_verification_gate() -> None:
    raw = read("docs/tooling/MODULE_SYSTEM_MODERNIZATION_CHECKLIST.md")
    first_slice = raw[raw.index("## First Implementation Slice: Dialogue + Encounter Safety"):]
    first_slice = first_slice[:first_slice.index("## Recently Fixed Old Bugs")]
    for token in (
        "build/test_modernization_static.py",
        "py build\\test_modernization_static.py",
        "py build\\test_feature_audit_static.py",
        "py build\\doctor.py --doctor-new-only",
        "cmd /c build_module.bat --no-cache",
    ):
        assert_contains(first_slice, token)


def test_dialogue_close_window_audit_report_exists() -> None:
    raw = read("docs/reports/dialogue_close_window_audit.md")
    for token in (
        "# Dialogue Close Window Audit",
        "Plain `close_window`, No Extra Action",
        "`$g_leave_encounter`",
        "`change_screen_map`",
        "`change_screen_return`",
        "`start_map_conversation` / `change_screen_map_conversation`",
        "Manual QA Still Needed",
    ):
        assert_contains(raw, token)


def test_dialogue_family_terminal_audit_report_exists() -> None:
    raw = read("docs/reports/dialogue_family_terminal_audit.md")
    for token in (
        "# Dialogue Family Terminal Audit",
        "`cpdla*` captured Centurion branches",
        "`pelha*` surrender/capture branches",
        "`legate_sq_*` Legion lore chains",
        "Lord recruitment, oath, pardon, and rebellion branches",
        "Companion direct-talk incident branches",
        "test_cpdla_captured_centurion_dialogue_family_is_safe",
        "Manual QA Still Needed",
    ):
        assert_contains(raw, token)


def test_dialogue_order_references_existing_files() -> None:
    for rel in iter_ordered_files("src/dialogs/_order_dialogs.txt"):
        assert (ROOT / "src" / "dialogs" / rel).exists(), f"missing ordered dialogue file: {rel}"
    assert "ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_11.py" not in iter_ordered_files("src/dialogs/_order_dialogs.txt")


def test_dialogue_outputs_have_matching_inputs_or_safe_terminals() -> None:
    input_states: set[str] = set()
    output_refs: list[tuple[str, str]] = []
    for entry in parse_dialogue_entries():
        input_states.add(str(entry["state_in"]))
        output_refs.append((str(entry["path"]), str(entry["state_out"])))

    missing = [
        (path, state)
        for path, state in output_refs
        if state not in SAFE_DIALOGUE_TERMINALS
        and state not in KNOWN_EXTERNAL_OR_LEGACY_STATES
        and state not in input_states
    ]
    assert not missing, "dialogue output states without matching inputs: " + repr(missing[:20])


def test_restored_dialogue_handoffs_start_and_close_cleanly() -> None:
    peace_acceptance = read(
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_quest_persuade_peace_9.py"
    )
    peace_acknowledgement = read(
        "src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_persuade_peace_10.py"
    )
    outlaw_completion = read(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_sell_prisoner_outlaws_finished.py"
    )
    assert_contains(peace_acceptance, '(setup_quest_text, "qst_persuade_lords_to_make_peace")')
    assert_contains(peace_acceptance, '(call_script, "script_start_quest", "qst_persuade_lords_to_make_peace", "$g_talk_troop")')
    assert_contains(peace_acknowledgement, '"merchant_quest_persuade_peace_10"')
    assert_contains(peace_acknowledgement, '"close_window"')
    assert_contains(outlaw_completion, '"sell_prisoner_outlaws_finished"')
    assert_contains(outlaw_completion, '"close_window"')


def test_dialogue_outputs_do_not_use_stale_removed_state_names() -> None:
    stale_exact = {
        "cpdla_nihilistic_11",
        "party_encounter_attack",
    }
    offenders = []
    input_states = {str(entry["state_in"]) for entry in parse_dialogue_entries()}
    for entry in parse_dialogue_entries():
        state = str(entry["state_out"])
        if state in SAFE_DIALOGUE_TERMINALS:
            continue
        if state in stale_exact:
            offenders.append((entry["path"], entry["state_in"], state))
        if state.endswith("_end") and state not in input_states:
            offenders.append((entry["path"], entry["state_in"], state))
        if re.search(r"(nihlistic|coll?eges|jawel)", state, re.I):
            offenders.append((entry["path"], entry["state_in"], state))
    assert not offenders, "dialogue outputs to stale removed/typo states: " + repr(offenders[:20])


def test_duplicate_player_options_do_not_shadow_later_branches() -> None:
    seen: dict[tuple[str, str, str], str] = {}
    offenders = []
    allowed_duplicate_text = {
        "Continue...",
        "Never mind.",
        "I must leave now.",
        "I have to leave.",
        "Go on.",
        "What can you tell me about this?",
    }
    normalize_ws = re.compile(r"\s+")
    for entry in parse_dialogue_entries():
        if not is_player_speaker(str(entry["speaker"])):
            continue
        text = normalize_ws.sub(" ", str(entry["text"]).strip())
        if text in allowed_duplicate_text:
            continue
        conditions = normalize_ws.sub(" ", str(entry["conditions"]).strip())
        key = (str(entry["state_in"]), conditions, text)
        prior = seen.get(key)
        if prior is not None:
            offenders.append((prior, entry["path"], entry["state_in"], text))
        else:
            seen[key] = str(entry["path"])
    assert not offenders, "duplicate player options can shadow later branches: " + repr(offenders[:20])


def test_terminal_post_battle_dialogues_leave_encounter_when_needed() -> None:
    death_or_capture_text = re.compile(
        r"(bleeding|wounds? are deep|finally.*end|execute)",
        re.I | re.S,
    )
    safe_tokens = (
        '$g_leave_encounter',
        "(change_screen_map)",
        "(change_screen_return)",
        "(start_map_conversation",
        "(change_screen_map_conversation",
        "(jump_to_menu",
        "(setup_party_meeting)",
    )
    offenders = []
    for entry in parse_dialogue_entries():
        path = str(entry["path"])
        raw = str(entry["raw"])
        state_out = str(entry["state_out"])
        if state_out not in SAFE_DIALOGUE_TERMINALS:
            continue
        if not any(token in path or token in str(entry["state_in"]) for token in ("cpdla", "pelha", "defeat_lord")):
            continue
        if not death_or_capture_text.search(str(entry["text"]) + " " + raw):
            continue
        if not any(token in raw for token in safe_tokens):
            offenders.append((path, entry["state_in"], state_out))
    assert not offenders, "post-battle terminal dialogues lack explicit encounter exit: " + repr(offenders[:20])


def test_legion_ief_capture_branches_terminate_safely() -> None:
    required_resolution_tokens = (
        "script_kill_kingdom_hero",
        "party_add_prisoners",
        "call_script, \"script_cf_sod_ief_release_captured_hero\"",
        "call_script, \"script_cf_sod_ief_recruit_captured_hero\"",
        '$g_leave_encounter',
        "(change_screen_map)",
        "(change_screen_return)",
    )
    offenders = []
    for entry in parse_dialogue_entries():
        path = str(entry["path"])
        state_in = str(entry["state_in"])
        raw = str(entry["raw"])
        if not any(token in path or token in state_in for token in ("cpdla_nihilistic", "centurion_death", "legate_execution")):
            continue
        if str(entry["state_out"]) not in SAFE_DIALOGUE_TERMINALS:
            continue
        if not any(token in raw for token in required_resolution_tokens):
            offenders.append((path, state_in, entry["state_out"]))
    assert not offenders, "Legion/IEF terminal capture branches lack death/capture/release/recruit exit: " + repr(offenders[:20])


def test_auto_proceed_branches_have_reachable_next_player_option() -> None:
    player_input_states = {
        str(entry["state_in"])
        for entry in parse_dialogue_entries()
        if is_player_speaker(str(entry["speaker"]))
    }
    offenders = []
    for entry in parse_dialogue_entries():
        if str(entry["speaker"]) != "anyone|auto_proceed":
            continue
        state_out = str(entry["state_out"])
        if state_out in SAFE_DIALOGUE_TERMINALS or state_out in KNOWN_EXTERNAL_OR_LEGACY_STATES:
            continue
        if state_out not in player_input_states:
            offenders.append((entry["path"], entry["state_in"], state_out))
    assert not offenders, "auto_proceed branches lead to states without player options: " + repr(offenders[:20])


def test_map_conversation_ops_are_only_used_in_safe_contexts() -> None:
    offenders = []
    safe_roots = (
        "src/menus/",
        "src/dialogs/",
        "src/mission_templates/",
    )
    safe_map_event_files = {
        "src/triggers/ST02_every_hour/entry_0045.py",
        "src/triggers/ST02_every_hour/entry_0086.py",
        "src/triggers/ST03_daily/entry_0046.py",
        "src/triggers/ST03_daily/entry_0158.py",
        "src/scripts/ZC_parties/setup_party_meeting.py",
        "src/scripts/ZE_encounters/post_battle_personality_clash_check.py",
        "src/scripts/ZH_heroes/setup_troop_meeting.py",
    }
    for root in ("src",):
        for path in iter_source_files(root):
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            raw = path.read_text(encoding="utf-8", errors="replace")
            if "(start_map_conversation" not in raw and "(change_screen_map_conversation" not in raw:
                continue
            if rel.startswith(safe_roots) or rel in safe_map_event_files:
                continue
            offenders.append(rel)
    assert not offenders, "map conversation ops outside safe menu/dialog/mission contexts: " + repr(offenders)


def entries_matching(*patterns: str) -> list[dict[str, object]]:
    compiled = [re.compile(pattern) for pattern in patterns]
    matches = []
    for entry in parse_dialogue_entries():
        haystack = " ".join(
            (
                str(entry["path"]),
                str(entry["state_in"]),
                str(entry["state_out"]),
            )
        )
        if any(pattern.search(haystack) for pattern in compiled):
            matches.append(entry)
    return matches


def assert_family_graph_is_closed(name: str, entries: list[dict[str, object]]) -> None:
    assert entries, f"{name} dialogue family not found"
    input_states = {str(entry["state_in"]) for entry in parse_dialogue_entries()}
    missing = []
    for entry in entries:
        state_out = str(entry["state_out"])
        if state_out in SAFE_DIALOGUE_TERMINALS or state_out in KNOWN_EXTERNAL_OR_LEGACY_STATES:
            continue
        if state_out not in input_states:
            missing.append((entry["path"], entry["state_in"], state_out))
    assert not missing, f"{name} dialogue family has unresolved outputs: {repr(missing[:20])}"


def assert_family_has_no_removed_suffixes(name: str, entries: list[dict[str, object]]) -> None:
    input_states = {str(entry["state_in"]) for entry in parse_dialogue_entries()}
    offenders = []
    for entry in entries:
        state_out = str(entry["state_out"])
        if state_out in SAFE_DIALOGUE_TERMINALS:
            continue
        if state_out.endswith("_end") and state_out not in input_states:
            offenders.append((entry["path"], entry["state_in"], state_out))
    assert not offenders, f"{name} dialogue family points at stale suffix states: {repr(offenders[:20])}"


def test_cpdla_captured_centurion_dialogue_family_is_safe() -> None:
    entries = entries_matching(r"\bcpdla")
    assert_family_graph_is_closed("cpdla captured Centurion", entries)
    assert_family_has_no_removed_suffixes("cpdla captured Centurion", entries)

    nihilistic_death = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_2.py")
    assert_contains(nihilistic_death, '"close_window"')
    assert_contains(nihilistic_death, '(call_script, "script_kill_kingdom_hero", "$g_talk_troop")')
    assert_contains(nihilistic_death, '(call_script, "script_sod_safe_leave_encounter")')


def test_pelha_surrender_capture_dialogue_family_is_safe() -> None:
    entries = entries_matching(r"\bpelha")
    assert_family_graph_is_closed("pelha surrender/capture", entries)
    assert_family_has_no_removed_suffixes("pelha surrender/capture", entries)

    terminal_states = [
        (entry["path"], entry["state_in"])
        for entry in entries
        if str(entry["state_out"]) in SAFE_DIALOGUE_TERMINALS
    ]
    assert terminal_states, "pelha surrender/capture family has no terminal branches"


def test_legate_sq_lore_chains_are_terminal_safe() -> None:
    entries = entries_matching(r"legate_sq_")
    assert_family_graph_is_closed("legate_sq lore", entries)
    assert_family_has_no_removed_suffixes("legate_sq lore", entries)

    terminal_entries = [
        entry
        for entry in entries
        if str(entry["state_out"]) in SAFE_DIALOGUE_TERMINALS
        or str(entry["state_out"]) in {"cpsq_0", "party_encounter_hostile_defender"}
    ]
    assert terminal_entries, "legate_sq lore chains have no safe terminals"
    unsafe = [
        (entry["path"], entry["state_in"], entry["state_out"])
        for entry in terminal_entries
        if str(entry["state_out"]) not in SAFE_DIALOGUE_TERMINALS
        and str(entry["state_out"]) not in {"cpsq_0", "party_encounter_hostile_defender"}
    ]
    assert not unsafe, "legate_sq lore chains use unsafe terminal state: " + repr(unsafe[:20])


def test_lord_politics_dialogue_families_are_graph_safe() -> None:
    entries = entries_matching(
        r"lord_recruit",
        r"chancellor_lord",
        r"swear_oath",
        r"ask_pardon",
        r"join_rebellion",
        r"rebellion",
        r"loa_",
        r"pardon",
    )
    assert_family_graph_is_closed("lord recruitment/oath/pardon/rebellion", entries)
    assert_family_has_no_removed_suffixes("lord recruitment/oath/pardon/rebellion", entries)

    risky_terminal = []
    for entry in entries:
        if str(entry["state_out"]) not in SAFE_DIALOGUE_TERMINALS:
            continue
        raw = str(entry["raw"])
        if any(token in raw for token in ("script_sod_chancellor_lord_recruitment", "script_cf_lord_can_join_faction")):
            if not any(token in raw for token in ("$g_leave_encounter", "(change_screen_map)", "(change_screen_return)", "(jump_to_menu")):
                risky_terminal.append((entry["path"], entry["state_in"], entry["state_out"]))
    assert not risky_terminal, "lord political terminal branches alter state without explicit exit: " + repr(risky_terminal[:20])


def test_companion_direct_talk_incidents_are_graph_safe() -> None:
    entries = entries_matching(
        r"member_chat",
        r"companion_",
        r"regular_member_companion",
        r"companion_depth",
        r"companion_(ymira|lezalit|bunduk|jeremus|firentis|marnid|borcha|deshavi|matheld|nizar|artimenner|rolf|alayen|klethi|baheshtur)",
    )
    assert_family_graph_is_closed("companion direct-talk incidents", entries)
    assert_family_has_no_removed_suffixes("companion direct-talk incidents", entries)


def test_generic_continue_menus_do_not_only_change_screen_return() -> None:
    dangerous = []
    for path in iter_source_files("src/menus"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        # Random-event result menus often use a descriptive body and return to
        # the previous screen. The brittle class is a generic menu whose title
        # itself is only "Continue", as with old post-mission handoff screens.
        if not re.search(r'\(\s*\"[^\"]+\"\s*,\s*[^,]+,\s*\"Continue\.?\"', raw):
            continue
        if "(change_screen_return)" not in raw:
            continue
        if any(token in raw for token in ("(jump_to_menu", "(change_screen_map)", "(change_screen_mission)", "(start_presentation", "(start_map_conversation", "(change_screen_map_conversation")):
            continue
        dangerous.append(str(path.relative_to(ROOT)))
    assert not dangerous, "generic continue menus rely only on change_screen_return: " + repr(dangerous)


def test_mission_templates_jump_to_menu_before_finish_mission() -> None:
    offenders = []
    for path in iter_source_files("src/mission_templates"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "(finish_mission)" not in raw or "(jump_to_menu" not in raw:
            continue
        finish_pos = raw.index("(finish_mission)")
        jump_pos = raw.index("(jump_to_menu")
        if finish_pos < jump_pos:
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, "mission templates finish before jump_to_menu: " + repr(offenders)


def test_encounter_and_camp_safety_guards_remain() -> None:
    helper = read("src/scripts/ZE_encounters/sod_safe_leave_encounter.py")
    assert_contains(helper, '"sod_safe_leave_encounter"')
    assert_contains(helper, '(assign, "$g_leave_encounter", 1)')
    assert_contains(helper, '(lt, "$g_encountered_party", 0)')
    assert_contains(helper, '(neg|party_is_active, "$g_encountered_party")')

    encounter = read("src/scripts/ZA_hardcoded_game_scripts/game_event_party_encounter.py")
    assert_contains(encounter, "invalid/reserved encounter ids")
    assert_contains(encounter, '(gt, "$g_encountered_party", 0)')
    assert_contains(encounter, '(party_is_active, "$g_encountered_party")')
    assert_not_contains(encounter, "start_party_encounter")

    camp = read("src/menus/0000_hardcoded_mb1011/camp.py")
    assert_contains(camp, '(neg|party_is_active, "$g_encountered_party")')
    assert_contains(camp, '(assign, "$g_encountered_party", -1)')
    assert_contains(camp, '(assign, "$g_encountered_party_2", -1)')
    hourly_sanitizer = read("src/triggers/ST02_every_hour/entry_0163.py")
    assert_contains(hourly_sanitizer, '(call_script, "script_sod_sanitize_unique_hero_party_stacks")')


def test_game_event_party_encounter_keeps_mb1011_routing_with_guards() -> None:
    encounter = read("src/scripts/ZA_hardcoded_game_scripts/game_event_party_encounter.py")
    for token in (
        '(store_script_param_1, "$g_encountered_party")',
        '(gt, "$g_encountered_party", 0)',
        '(party_is_active, "$g_encountered_party")',
        '(store_faction_of_party, "$g_encountered_party_faction", "$g_encountered_party")',
        '(party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type)',
        '(party_get_template_id, "$g_encountered_party_template", "$g_encountered_party")',
        '(assign, "$new_encounter", 1)',
        '(jump_to_menu, "mnu_castle_outside")',
        '(jump_to_menu, "mnu_village")',
        '(jump_to_menu, "mnu_simple_encounter")',
    ):
        assert_contains(encounter, token)


def test_party_safe_active_guard_helper_exists() -> None:
    helper = read("src/scripts/ZC_parties/sod_party_is_safe_active_to_reg.py")
    assert_contains(helper, '"sod_party_is_safe_active_to_reg"')
    assert_contains(helper, "(store_script_param_1, \":party_no\")")
    assert_contains(helper, "(assign, reg0, 0)")
    assert_contains(helper, "(ge, \":party_no\", 0)")
    assert_contains(helper, "(party_is_active, \":party_no\")")
    assert_contains(helper, "(assign, reg0, 1)")


def test_party_id_safety_audit_report_exists() -> None:
    raw = read("docs/reports/party_id_safety_audit.md")
    for token in (
        "# Party ID Safety Audit",
        "script_sod_party_is_safe_active_to_reg",
        "store_distance_to_party_from_party",
        "store_faction_of_party",
        "$g_encountered_party",
        "$current_town",
        "$g_enemy_party",
        "High-frequency trigger distance calls",
    ):
        assert_contains(raw, token)


def test_troop_hero_movement_audit_report_exists() -> None:
    raw = read("docs/reports/troop_hero_movement_audit.md")
    for token in (
        "# Troop And Hero Movement Audit",
        "party_force_add_prisoners",
        "party_add_members",
        "script_event_hero_taken_prisoner_by_player",
        "script_sod_sanitize_unique_hero_party_stacks",
        "script_kill_kingdom_hero",
        "Manual QA Still Needed",
    ):
        assert_contains(raw, token)


def test_high_frequency_distance_calls_are_audited() -> None:
    hits = operation_hits(
        ("src/triggers/ST01_every_frame", "src/triggers/ST02_every_hour"),
        r"\(store_distance_to_party_from_party,",
    )
    current = {f"{path}:{line}" for path, line, _ in hits}
    audited = {
        "src/triggers/ST01_every_frame/entry_0078.py:10",
        "src/triggers/ST02_every_hour/entry_0073.py:5",
        "src/triggers/ST02_every_hour/entry_0077.py:18",
        "src/triggers/ST02_every_hour/entry_0082.py:8",
        "src/triggers/ST02_every_hour/entry_0082.py:16",
        "src/triggers/ST02_every_hour/entry_0082.py:24",
        "src/triggers/ST02_every_hour/entry_0086.py:69",
        "src/triggers/ST02_every_hour/entry_0087.py:39",
        "src/triggers/ST02_every_hour/entry_0178_incriminate_loyal_commander.py:20",
    }
    assert current == audited, "high-frequency distance-call inventory changed: " + repr(sorted(current ^ audited))


def test_runtime_log_invalid_party_zero_sources_are_guarded() -> None:
    closest_helpers = (
        "src/scripts/ZD_centers/get_closest_center.py",
        "src/scripts/ZD_centers/get_closest_town.py",
        "src/scripts/ZD_centers/get_closest_village.py",
        "src/scripts/ZD_centers/get_closest_walled_center.py",
        "src/scripts/ZD_centers/get_closest_center_of_faction.py",
        "src/scripts/ZD_centers/get_closest_town_of_faction.py",
        "src/scripts/ZD_centers/get_closest_walled_center_of_faction.py",
    )
    for path in closest_helpers:
        raw = read(path)
        assert "(assign, reg0, -1)" in raw or '(assign, ":result", -1)' in raw
        assert_contains(raw, '(gt, ":party_no", 0)')
        assert_contains(raw, '(party_is_active, ":party_no")')
        assert raw.index('(party_is_active, ":party_no")') < raw.index("(store_distance_to_party_from_party")

    prosperity = read("src/scripts/ZB_economy_and_trade/change_center_prosperity.py")
    health = read("src/scripts/ZD_centers/change_center_health.py")
    threat = read("src/scripts/ZY_helper_scripts/sod_threat_board_apply_economy_effect.py")
    music = read("src/scripts/ZC_parties/get_culture_with_party_faction_for_music.py")
    retreat = read("src/scripts/ZY_helper_scripts/sod_world_map_trigger_services.py")
    assert prosperity.index('(is_between, ":center_no", centers_begin, centers_end)') < prosperity.index("(party_get_slot")
    assert health.index('(is_between, ":center_no", centers_begin, centers_end)') < health.index("(party_get_slot")
    assert threat.index('(is_between, ":sponsor_center", centers_begin, centers_end)') < threat.index("script_change_center_prosperity")
    assert music.index('(party_is_active, ":party_no")') < music.index("(store_faction_of_party")
    lord_avoid_ai = retreat[retreat.index('"sod_world_map_process_lord_avoid_party_ai"') :]
    assert lord_avoid_ai.index('(neg|party_is_active, ":commander_party")') < lord_avoid_ai.index("(faction_get_slot")


def test_global_party_operations_are_audited_in_scripts_and_triggers() -> None:
    hits = operation_hits(
        ("src/scripts", "src/triggers"),
        r"\((?:[a-z_]+\|)*(party_get_slot|party_slot_eq|str_store_party_name),.*(\$g_encountered_party|\$current_town|\$g_enemy_party|\$g_talk_troop_party)",
    )
    current = set()
    for path, _line, line in hits:
        operation = re.search(r"\((?:[a-z_]+\|)*(party_get_slot|party_slot_eq|str_store_party_name),", line).group(1)
        global_name = re.search(r"(\$g_encountered_party|\$current_town|\$g_enemy_party|\$g_talk_troop_party)", line).group(1)
        current.add(f"{path}:{operation}:{global_name}")
    audited = {
        "src/scripts/ZA_hardcoded_game_scripts/game_event_buy_item.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZA_hardcoded_game_scripts/game_event_party_encounter.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZA_hardcoded_game_scripts/game_event_party_encounter.py:party_slot_eq:$g_encountered_party",
        "src/scripts/ZA_hardcoded_game_scripts/game_event_sell_item.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZA_hardcoded_game_scripts/game_get_item_buy_price_factor.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZA_hardcoded_game_scripts/game_get_item_sell_price_factor.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZB_economy_and_trade/get_trade_penalty.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZB_economy_and_trade/shield_item_set_banner.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZC_parties/event_player_defeated_enemy_party.py:party_get_slot:$g_enemy_party",
        "src/scripts/ZC_parties/event_player_defeated_enemy_party.py:party_slot_eq:$g_enemy_party",
        "src/scripts/ZC_parties/total_victory_finalize.py:party_get_slot:$g_enemy_party",
        "src/scripts/ZC_parties/total_victory_finalize.py:party_slot_eq:$g_enemy_party",
        "src/scripts/ZD_centers/agent_get_town_walker_details.py:party_get_slot:$current_town",
        "src/scripts/ZD_centers/center_ambiance_sounds.py:party_slot_eq:$g_encountered_party",
        "src/scripts/ZD_centers/cf_enter_center_location_bandit_check.py:party_get_slot:$current_town",
        "src/scripts/ZD_centers/cf_enter_center_location_bandit_check.py:party_slot_eq:$current_town",
        "src/scripts/ZD_centers/cf_village_recruit_volunteers_cond.py:party_get_slot:$current_town",
        "src/scripts/ZD_centers/cf_village_recruit_volunteers_cond.py:party_slot_eq:$current_town",
        "src/scripts/ZD_centers/init_town_walkers.py:party_get_slot:$current_town",
        "src/scripts/ZD_centers/village_recruit_volunteers_get_params.py:party_get_slot:$current_town",
        "src/scripts/ZE_encounters/select_battle_tactic_aux.py:party_slot_eq:$g_enemy_party",
        "src/scripts/ZE_encounters/sod_safe_leave_encounter.py:str_store_party_name:$current_town",
        "src/scripts/ZE_encounters/sod_safe_leave_encounter.py:str_store_party_name:$g_encountered_party",
        "src/scripts/ZE_encounters/sod_safe_leave_encounter.py:str_store_party_name:$g_enemy_party",
        "src/scripts/ZE_encounters/sod_safe_leave_encounter.py:str_store_party_name:$g_talk_troop_party",
        "src/scripts/ZG_quests/get_random_quest.py:party_slot_eq:$g_encountered_party",
        "src/scripts/ZY_helper_scripts/sod_banking.py:party_slot_eq:$current_town",
        "src/scripts/ZL_banners_and_profiles/change_banners_and_chest.py:party_get_slot:$g_encountered_party",
        "src/scripts/ZN_tournaments/get_random_tournament_team_amount_and_size.py:party_get_slot:$current_town",
        "src/scripts/ZN_tournaments/get_win_amount_for_tournament_bet.py:party_get_slot:$current_town",
        "src/scripts/ZZ_common_array_processing/enter_town_center_from_passage.py:party_get_slot:$current_town",
        "src/scripts/ZZ_common_array_processing/enter_town_center_from_passage.py:party_slot_eq:$current_town",
        "src/scripts/ZZ_common_array_processing/fgtq_end.py:party_get_slot:$g_encountered_party",
        "src/triggers/ST02_every_hour/entry_0084.py:party_get_slot:$g_encountered_party",
    }
    assert current == audited, "global party-operation inventory changed: " + repr(sorted(current ^ audited))


def test_party_force_add_prisoners_hero_paths_are_explicit() -> None:
    hits = operation_hits(("src/dialogs", "src/menus", "src/scripts", "src/triggers"), r"\(party_force_add_prisoners,")
    assert hits, "party_force_add_prisoners inventory is unexpectedly empty"
    offenders = []
    for path, _line, _text in hits:
        raw = read(path)
        if "sod_player_capture_hero_to_reg" in raw:
            for token in (
                "(is_between, \":troop_no\", heroes_begin, heroes_end)",
                "slot_troop_prisoner_of_party",
                "script_event_hero_taken_prisoner_by_player",
            ):
                if token not in raw:
                    offenders.append((path, f"shared hero capture helper missing {token}"))
            continue
        if '"$g_talk_troop"' not in raw:
            offenders.append((path, "non-talk-troop prisoner force-add needs review"))
            continue
        if "slot_troop_prisoner_of_party" not in raw:
            offenders.append((path, "missing prisoner ownership slot"))
        if "script_event_hero_taken_prisoner_by_player" not in raw:
            offenders.append((path, "missing hero prisoner event"))
    assert not offenders, "party_force_add_prisoners hero handling is not explicit: " + repr(offenders[:20])


def test_party_add_members_talk_troop_rejects_heroes_or_is_intended() -> None:
    hits = operation_hits(("src/dialogs", "src/menus", "src/scripts", "src/triggers"), r"\(party_add_members,.*\$g_talk_troop")
    offenders = []
    intended_exceptions = {
        # Escort/quest-spawn flow: the talked troop is moved into a newly
        # spawned quest party, not merged into a generic stack.
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sacrificed_messenger_3.py",
    }
    for path, _line, _text in hits:
        if path in intended_exceptions:
            continue
        raw = read(path)
        if '(neg|troop_is_hero, "$g_talk_troop")' not in raw and '(troop_is_hero, "$g_talk_troop")' not in raw:
            offenders.append(path)
    assert not offenders, "party_add_members with $g_talk_troop lacks explicit hero handling: " + repr(offenders)


def test_duplicate_unique_hero_stack_risks_are_blocked() -> None:
    sanitizer = read("src/scripts/ZC_parties/sod_sanitize_unique_hero_party_stacks.py")
    assert_contains(sanitizer, "kingdom_heroes_begin")
    assert_contains(sanitizer, "kingdom_heroes_end")
    assert_contains(sanitizer, "slot_troop_leaded_party")
    assert_contains(sanitizer, "(party_remove_members, \":party_no\", \":stack_troop\", \":stack_size\")")

    hits = operation_hits(("src/dialogs", "src/menus", "src/scripts", "src/triggers"), r"\(party_add_members,")
    risky_literals = []
    allowed_contexts = (
        "get_heroes_attached_to_center",
        "get_heroes_attached_to_center_as_prisoner_aux",
        "sod_royal_return_expedition_heroes",
        "sod_sanitize_unique_hero_party_stacks",
    )
    for path, _line, text in hits:
        if any(token in path for token in allowed_contexts):
            continue
        if re.search(r'"trp_kingdom_\d+_lord"|kingdom_heroes_begin|kingdom_heroes_end', text):
            risky_literals.append((path, text))
    assert not risky_literals, "unique kingdom hero party_add_members outside controlled contexts: " + repr(risky_literals[:20])


def test_lord_lifecycle_paths_are_audited() -> None:
    expected_tokens = {
        "death": "script_kill_kingdom_hero",
        "capture": "script_event_hero_taken_prisoner_by_player",
        "release": "remove_troops_from_prisoners",
        "recruit": "script_sod_chancellor_lord_recruitment",
        "oath": "lord_give_oath",
        "faction_change": "script_change_troop_faction",
    }
    corpus = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in iter_source_files("src"))
    missing = [label for label, token in expected_tokens.items() if token not in corpus]
    assert not missing, "lord lifecycle token(s) missing from audit corpus: " + repr(missing)


def test_ief_dying_centurion_default_branch_is_terminal() -> None:
    death_reply = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_2.py")
    assert_contains(death_reply, '"cpdla_nihilistic_2"')
    assert_contains(death_reply, '"close_window"')
    assert_contains(death_reply, '(call_script, "script_kill_kingdom_hero", "$g_talk_troop")')
    assert_contains(death_reply, '(call_script, "script_sod_safe_leave_encounter")')
    assert_not_contains(death_reply, '"cpdla_nihilistic_3"')


def test_center_validation_audit_report_exists() -> None:
    raw = read("docs/reports/center_validation_audit.md")
    for token in (
        "# Center Validation Audit",
        "Closest-Center Consumers",
        "Mini-Faction Report Fallbacks",
        "script_sod_store_center_name_or_fallback_to_s21",
        "Remaining Manual QA",
    ):
        assert_contains(raw, token)


def test_center_name_fallback_helper_validates_center_range() -> None:
    raw = read("src/scripts/ZD_centers/sod_store_center_name_or_fallback_to_s21.py")
    assert_contains(raw, '("sod_store_center_name_or_fallback_to_s21"')
    assert_contains(raw, '(is_between, ":center_no", centers_begin, centers_end)')
    assert_contains(raw, "(str_store_party_name_link, s21, \":center_no\")")
    assert_contains(raw, "(str_store_string, s21, \":fallback_string\")")


def test_closest_center_consumers_are_inventoried() -> None:
    hits = operation_hits(
        ("src/scripts",),
        r"\(call_script, \"script_get_closest_(?:center|village|walled_center|town)\"",
    )
    current = {f"{path}:{text}" for path, _line, text in hits}
    audited = {
        'src/scripts/ZC_parties/total_victory_finalize.py:(call_script, "script_get_closest_center", "p_main_party"),',
        'src/scripts/ZG_quests/sod_rtc_price_of_bread_bind_world.py:(call_script, "script_get_closest_village", "p_main_party"),',
        'src/scripts/ZE_encounters/get_information_about_troops_position.py:(call_script, "script_get_closest_center", ":party_no"),',
        'src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py:(call_script, "script_get_closest_walled_center", ":cur_party"),',
        'src/scripts/ZK_music/music_set_situation_with_culture.py:(call_script, "script_get_closest_center", "p_main_party"),',
        'src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py:(call_script, "script_get_closest_center", ":camp_party"),',
        'src/scripts/ZY_helper_scripts/sod_companion_depth.py:(call_script, "script_get_closest_town", "p_main_party"),',
        'src/scripts/ZY_helper_scripts/sod_companion_depth.py:(call_script, "script_get_closest_village", ":origin"),',
        'src/scripts/ZY_helper_scripts/sod_companion_depth.py:(call_script, "script_get_closest_village", "p_main_party"),',
        'src/scripts/ZY_helper_scripts/sod_company_accounts.py:(call_script, "script_get_closest_center", "p_main_party"),',
        'src/scripts/ZY_helper_scripts/sod_company_accounts.py:(call_script, "script_get_closest_walled_center", "p_main_party"),',
        'src/scripts/ZY_helper_scripts/sod_lord_party_morale.py:(call_script, "script_get_closest_center", ":party_no"),',
        'src/scripts/ZY_helper_scripts/sod_lord_party_morale.py:(call_script, "script_get_closest_walled_center", ":party_no"),',
        'src/scripts/ZY_helper_scripts/sod_prisoner_economy.py:(call_script, "script_get_closest_center", ":source_party"),',
        'src/scripts/ZY_helper_scripts/sod_prisoner_economy.py:(call_script, "script_get_closest_center", ":train_party"),',
        'src/scripts/ZY_helper_scripts/sod_threat_board_normalize_center.py:(call_script, "script_get_closest_center", "p_main_party"),',
        'src/scripts/ZY_helper_scripts/sod_trade_network.py:(call_script, "script_get_closest_center", ":party_no"),',
        'src/scripts/ZZ_common_array_processing/spawn_bandits.py:(call_script, "script_get_closest_walled_center", ":party_no"),',
    }
    assert current == audited, "closest-center consumer inventory changed: " + repr(sorted(current ^ audited))


def test_mini_faction_reports_use_center_fallback_helper() -> None:
    report_files = {
        "src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py": "no confirmed frontier village",
        "src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py": "no confirmed shrine-road",
        "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py": "no confirmed rich road",
        "src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py": "no confirmed frontier mark",
        "src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py": "no confirmed watched route",
        "src/scripts/ZY_helper_scripts/merc_describe_standing_report.py": "no confirmed frontier village",
        "src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py": "no confirmed center",
        "src/scripts/ZY_helper_scripts/sod_diplomacy_system.py": "no declared target",
    }
    for path, fallback in report_files.items():
        raw = read(path)
        assert_contains(raw, "script_sod_store_center_name_or_fallback_to_s21")
        assert_contains(raw, fallback)


def test_faction_target_center_names_are_range_guarded_or_fallbacked() -> None:
    target_tokens = (
        "slot_faction_jotnar_target_center",
        "slot_faction_elephant_guard_target_center",
        "slot_faction_black_khergit_target_center",
        "slot_faction_boar_target_center",
        "slot_faction_serpent_target_center",
    )
    offenders = []
    for path in iter_source_files("src/scripts"):
        raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for idx, line in enumerate(raw_lines):
            if not any(token in line for token in target_tokens):
                continue
            window = "\n".join(raw_lines[idx : idx + 8])
            if "str_store_party_name" not in window:
                continue
            if (
                "script_sod_store_center_name_or_fallback_to_s21" not in window
                and "is_between" not in window
                and "centers_begin" not in window
            ):
                offenders.append(f"{path.relative_to(ROOT)}:{idx + 1}")
    assert not offenders, "target-center party names without range/fallback guard: " + repr(offenders[:20])


def test_touched_closest_center_outputs_are_center_range_checked() -> None:
    troop_info = read("src/scripts/ZE_encounters/get_information_about_troops_position.py")
    assert_contains(troop_info, "(is_between, reg0, centers_begin, centers_end)")
    assert_contains(troop_info, "@unknown roads")
    assert_contains(troop_info, '(str_store_string, s68, "@is currently")')
    assert_contains(troop_info, '(str_store_string, s70, "@should be")')
    assert_contains(troop_info, '(str_store_string, s71, "@ at the moment")')
    assert_not_contains(troop_info, "{reg3?was:is")
    assert_not_contains(troop_info, "{reg3?was:should be")
    assert_not_contains(troop_info, "{reg3?was:has been")
    assert_not_contains(troop_info, "{reg4?she:he}")
    assert_not_contains(troop_info, "{reg4?her:his}")

    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    assert_contains(accounts, '(is_between, ":center", centers_begin, centers_end)')

    trade = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(trade, "sod_trade_network_validate_center_to_reg")
    assert_contains(trade, '(neg|is_between, reg0, centers_begin, centers_end)')
    assert_contains(trade, '(assign, reg0, "p_town_1")')

    horde = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    assert_contains(horde, '(is_between, ":target_center", centers_begin, centers_end)')


def test_phase3_audit_report_exists() -> None:
    raw = read("docs/reports/menu_report_presentation_safety_audit.md")
    for token in (
        "# Menu, Report, And Presentation Safety Audit",
        "Menu Export Reliability",
        "Report Safety",
        "Presentation Compatibility",
        "prsnt_game_credits",
        "prsnt_banner_selection",
    ):
        assert_contains(raw, token)


def test_menu_source_shape_is_export_friendly() -> None:
    offenders = []
    for path in iter_source_files("src/menus"):
        if "_preamble" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "MENUS = [" not in raw:
            offenders.append((str(path.relative_to(ROOT)), "missing MENUS list"))
        if not re.search(r'\(\s*"[^"]+"\s*,', raw):
            offenders.append((str(path.relative_to(ROOT)), "no recognizable menu tuple id"))
        if "\r\n\r\n\r\n" in raw:
            offenders.append((str(path.relative_to(ROOT)), "excess blank lines inside menu source"))
        if re.search(r'"\s*\n\s*"', raw):
            offenders.append((str(path.relative_to(ROOT)), "adjacent string literals split across lines"))
    assert not offenders, "menu source shape may export brittle records: " + repr(offenders[:20])


def test_menu_option_brackets_are_balanced_before_export() -> None:
    offenders = []
    for path in iter_source_files("src/menus"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if raw.count("[") != raw.count("]"):
            offenders.append((str(path.relative_to(ROOT)), raw.count("["), raw.count("]")))
    assert not offenders, "menu square-bracket balance failed: " + repr(offenders[:20])


def test_jump_to_menu_targets_exist() -> None:
    menu_ids = set()
    for path in iter_source_files("src/menus"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        menu_ids.update(re.findall(r'^\s*\("([^"]+)",\s*(?!\[)', raw, re.M))
    compiled = ROOT / "compile/module_game_menus.py"
    if compiled.exists():
        raw = compiled.read_text(encoding="utf-8", errors="replace")
        menu_ids.update(re.findall(r'^\s*\(?\s*"([^"]+)",\s*(?:mnf_|0|menu_text_color)', raw, re.M))
    refs = operation_hits(("src/menus", "src/dialogs", "src/scripts", "src/triggers", "src/mission_templates"), r'\(jump_to_menu,\s*"mnu_[^"]+"')
    missing = []
    for path, line, text in refs:
        match = re.search(r'"mnu_([^"]+)"', text)
        if match and match.group(1) not in menu_ids:
            missing.append(f"{path}:{line}:{match.group(0)}")
    assert not missing, "jump_to_menu target(s) missing from src/menus: " + repr(missing[:30])


def test_camp_report_option_conditions_do_not_call_high_risk_scripts() -> None:
    high_risk = (
        "game_event_party_encounter",
        "party_calculate_and_set_nearby_friend_strength",
        "sod_black_khergits_spawn_or_recover_camp",
        "sod_mini_faction_generate_incident",
        "sod_company_accounts_apply_pay_choice",
    )
    offenders = []
    for path in iter_source_files("src/menus/camp"):
        name = path.name
        if "report" not in name and name not in {"camp.py", "camp_action.py"}:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r'\("([^"]+)",\s*\[([\s\S]*?)\]\s*,\s*"[^"]*"\s*,\s*\[', raw):
            option_id, conditions = match.groups()
            if "(call_script" not in conditions:
                continue
            for token in high_risk:
                if token in conditions:
                    offenders.append((str(path.relative_to(ROOT)), option_id, token))
    assert not offenders, "camp/report menu option conditions call high-risk scripts: " + repr(offenders[:20])


def test_report_menus_call_description_scripts_and_use_fallbacks() -> None:
    report_files = [path for path in iter_source_files("src/menus/reports") if "report" in path.name]
    assert report_files, "no camp report files found"
    description_callers = []
    for path in report_files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "_describe_" in raw or "describe_status" in raw:
            description_callers.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    assert "src/menus/reports/boar_clan_frontier_report.py" in description_callers
    boar = read("src/menus/reports/boar_clan_frontier_report.py")
    assert_contains(boar, "script_sod_store_center_name_or_fallback_to_s21")
    assert_contains(boar, "no confirmed frontier mark")


def test_warband_presentation_callbacks_are_absent_for_mb1011() -> None:
    order = read("src/presentations/_order_presentations.txt")
    assert_contains(order, "0001_game_credits/game_credits.py")
    assert "0000_game_hardcoded_callbacks" not in order
    assert "9999_mb1011_game_presentation_stubs" not in order
    presentation_paths = [
        line.strip()
        for line in order.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    presentation_raw = "\n".join(read("src/presentations/" + line) for line in presentation_paths)
    assert '"game_start"' not in presentation_raw
    assert '"game_escape"' not in presentation_raw
    ids = read("compile/ids/ID_presentations.py")
    assert_contains(ids, "prsnt_game_credits = 0")
    assert_contains(ids, "prsnt_banner_selection = 1")
    assert "prsnt_game_start" not in ids
    assert "prsnt_game_escape" not in ids
    note = read("docs/reports/references_features/original_sod_game_start_flow_audit.md")
    assert_contains(note, "Mount&Blade 1.011")
    assert_contains(note, "Warband-only presentation callbacks")


def test_phase4_campaign_ai_audit_report_exists() -> None:
    raw = read("docs/reports/campaign_ai_modernization_audit.md")
    for token in (
        "# Campaign AI Modernization Audit",
        "AI Pulse Safety",
        "Lord AI And Diplomacy",
        "Battle And Formation AI",
        "script_sod_imperial_expedition_enforce_total_war",
    ):
        assert_contains(raw, token)


def test_campaign_ai_trigger_cadence_is_documented() -> None:
    seven_hour = read("src/triggers/ST02_every_hour/entry_0024.py")
    assert_contains(seven_hour, "Campaign AI cadence: every 7 hours")
    assert_contains(seven_hour, 'script_init_ai_calculation')
    assert_contains(seven_hour, 'script_decide_kingdom_party_ais')

    two_hour = read("src/triggers/ST02_every_hour/entry_0027.py")
    assert_contains(two_hour, "Campaign AI cadence: every 2 hours")
    assert_contains(two_hour, 'script_process_kingdom_parties_ai')

    daily = read("src/triggers/ST03_daily/entry_0158.py")
    assert_contains(daily, "Campaign modernization cadence: daily")
    for token in (
        "script_sod_imperial_expedition_process_campaign",
        "script_sod_diplomacy_update_realm_state",
        "script_sod_lord_update_all_party_morale",
    ):
        assert_contains(daily, token)


def test_high_frequency_ai_scripts_do_not_use_unguarded_global_party_ops() -> None:
    hot_files = (
        "src/triggers/ST02_every_hour/entry_0024.py",
        "src/triggers/ST02_every_hour/entry_0027.py",
        "src/triggers/ST03_daily/entry_0158.py",
        "src/scripts/ZY_helper_scripts/sod_imperial_expedition.py",
        "src/scripts/ZY_helper_scripts/sod_diplomacy_system.py",
    )
    dangerous_globals = ("$g_encountered_party", "$g_enemy_party", "$g_talk_troop_party")
    offenders = []
    for path in hot_files:
        raw = read(path)
        for token in dangerous_globals:
            if token in raw:
                offenders.append((path, token))
    assert not offenders, "high-frequency AI path uses volatile global party ids: " + repr(offenders)


def test_diplomacy_personality_memory_and_posture_are_centralized() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    assert_contains(raw, '("sod_diplomacy_get_faction_personality_to_regs"')
    assert_contains(raw, "slot_faction_diplomacy_temperament")
    assert_contains(raw, "sod_diplomacy_temperament_imperial_exception")
    assert_contains(raw, '("sod_diplomacy_apply_memory"')
    posture = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(posture, '("sod_faction_update_campaign_posture"')
    assert_contains(posture, "slot_faction_sod_campaign_posture")


def test_ief_total_war_and_auxiliary_rules_are_pinned() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    assert_contains(raw, '("sod_imperial_expedition_enforce_total_war"')
    assert_contains(raw, '(faction_set_slot, "fac_kingdom_6", slot_faction_merc_pact, 0)')
    assert_contains(raw, '(faction_set_slot, "fac_kingdom_6_mercenaries", slot_faction_state, sfs_active)')
    assert_contains(raw, 'script_diplomacy_start_war_between_kingdoms')
    assert_contains(raw, 'script_sod_diplomacy_note_war_reason')
    assert_contains(raw, 'script_sod_store_center_name_or_fallback_to_s21')

    diplomacy = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    assert_contains(diplomacy, '(this_or_next|eq, ":source_faction", "fac_kingdom_6")')
    assert_contains(diplomacy, '(assign, ":score", -100)')


def test_kingdom6_only_hero_death_rules_are_static_pinned() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    assert_contains(raw, '("sod_imperial_expedition_count_living_vassals"')
    assert_contains(raw, '(faction_get_slot, ":leader", "fac_kingdom_6", slot_faction_leader)')
    assert_contains(raw, '(neq, ":cur_troop", ":leader")')
    assert_contains(raw, '(eq, ":cur_faction", "fac_kingdom_6")')
    assert_contains(raw, "Gaius Marius cannot be slain while any Centurion command remains alive")


def test_major_battle_templates_keep_formation_and_morale_hooks() -> None:
    lead_charge = read("src/mission_templates/0010_lead_charge/lead_charge.py")
    for token in (
        "script_sod_battle_initialize_morale_context",
        "script_sod_company_dialogue_process_battle_start_morale",
        "formations_init",
        "formations_start_coherence",
        "formations_update_morale",
        "formations_update_route",
    ):
        assert_contains(lead_charge, token)

    siege_ladder = read("src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py")
    siege_belfry = read("src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py")
    for raw in (siege_ladder, siege_belfry):
        assert_contains(raw, "common_siege_refill_ammo")
        assert_contains(raw, "common_siege_attacker_morale_pressure")
        assert_contains(raw, "formations_start_coherence")


def test_phase5_quest_framework_audit_report_exists() -> None:
    raw = read("docs/reports/quest_framework_modernization_audit.md")
    for token in (
        "# Quest Framework Modernization Audit",
        "Registration",
        "Runtime And Journal",
        "Companion Personal Arcs",
        "Journal Text Standards",
    ):
        assert_contains(raw, token)


def test_quest_end_sentinel_is_isolated_and_last() -> None:
    order = [
        line.strip()
        for line in read("src/quests/_order_quests.txt").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert order[-1] == "9999_quests_end.py", "quest end sentinel must load last"
    sentinel = read("src/quests/9999_quests_end.py")
    assert_contains(sentinel, "Keep the terminal quest sentinel in its own final fragment")
    assert_contains(sentinel, '"quests_end"')
    offenders = []
    for path in iter_source_files("src/quests"):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel.endswith("9999_quests_end.py"):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        if 'quest_template_spec(\n    "quests_end"' in raw or 'quest_template_spec("quests_end"' in raw:
            offenders.append(rel)
    assert not offenders, "quests_end appears outside sentinel fragment: " + repr(offenders)


def test_legacy_quest_wrappers_route_to_runtime_helpers() -> None:
    start = read("src/scripts/ZG_quests/start_quest.py")
    succeed = read("src/scripts/ZG_quests/succeed_quest.py")
    fail = read("src/scripts/ZG_quests/fail_quest.py")
    end = read("src/scripts/ZG_quests/end_quest.py")
    assert_contains(start, 'script_sod_quest_runtime_accept')
    assert_contains(succeed, 'script_sod_quest_runtime_complete')
    assert_contains(fail, 'script_sod_quest_runtime_fail')
    assert_contains(end, 'script_sod_quest_runtime_fail')
    assert_contains(end, 'script_sod_quest_runtime_complete')


def test_quest_runtime_journal_memory_outcome_surfaces_exist() -> None:
    expected = {
        "src/scripts/ZG_quests/sod_quest_runtime_accept.py": "sod_quest_runtime_accept",
        "src/scripts/ZG_quests/sod_quest_runtime_update.py": "sod_quest_runtime_update",
        "src/scripts/ZG_quests/sod_quest_runtime_complete.py": "sod_quest_runtime_complete",
        "src/scripts/ZG_quests/sod_quest_runtime_fail.py": "sod_quest_runtime_fail",
        "src/scripts/ZG_quests/sod_quest_dialogue_record_event.py": "sod_quest_dialogue_record_event",
        "src/scripts/ZG_quests/sod_quest_journal_update.py": "sod_quest_journal_update",
        "src/scripts/ZG_quests/sod_quest_outcome_apply_consequences.py": "sod_quest_outcome_apply_consequences",
    }
    for path, token in expected.items():
        assert_contains(read(path), token)


def test_companion_personal_arcs_have_framework_ids_and_metadata() -> None:
    raw = read("src/quests/0012_companion_personal_quests.py")
    expected_ids = (
        "companion_borcha_road_keeps_own",
        "companion_marnid_honest_price",
        "companion_ymira_mercy_under_arms",
        "companion_lezalit_discipline_without_chains",
        "companion_bunduk_men_hold_line",
        "companion_jeremus_hands_triage",
        "companion_firentis_debt_restitution",
        "companion_rolf_name_worth_wearing",
        "companion_baheshtur_unbroken_saddle",
        "companion_deshavi_tracks_through_ash",
        "companion_matheld_no_backward_step",
        "companion_alayen_standard_self",
        "companion_katrin_last_coin",
        "companion_nizar_impossible_charge",
        "companion_artimenner_siege_that_should",
        "companion_klethi_knife_with_name",
    )
    for quest_id in expected_ids:
        assert_contains(raw, quest_id)
    assert raw.count('"category": "companion"') >= len(expected_ids)
    assert raw.count('"depth_layer": "dragon_age_style"') >= len(expected_ids)
    assert raw.count("quest_stage_spec(") >= len(expected_ids) * 3


def test_companion_quest_journal_text_separates_talk_from_world_incident() -> None:
    raw = read("src/quests/0012_companion_personal_quests.py")
    assert raw.count("Speak with") >= 8, "opening stages should direct companion conversation"
    world_hooks = (
        "Captives on the Road",
        "The Captured Drill",
        "A Grievance in the Ranks",
        "Triage After Battle",
        "Restraint Under Steel",
        "A Bad Road Chosen",
        "A Bargain Under Strain",
        "Survivors or Pursuit",
        "The Shield Still Faces Forward",
        "Design or Blame",
    )
    missing = [token for token in world_hooks if token not in raw]
    assert not missing, "companion field-test journal text missing world/adventure hooks: " + repr(missing)


def test_companion_quest_memory_and_outcome_hooks_are_present() -> None:
    companion = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    assert_contains(companion, "script_sod_quest_dialogue_record_event")
    assert_contains(companion, "script_sod_quest_journal_update")
    assert_contains(companion, "script_sod_quest_outcome_apply_consequences")
    assert_contains(companion, "script_sod_quest_runtime_accept")
    assert_contains(companion, "script_sod_quest_runtime_update")
    assert_contains(companion, "script_sod_quest_runtime_complete")
    assert_contains(companion, "script_sod_quest_runtime_fail")


def test_phase6_companion_incident_audit_report_exists() -> None:
    raw = read("docs/reports/companion_incident_modernization_audit.md")
    for token in (
        "# Companion And Incident Modernization Audit",
        "Direct Dialogue Surface",
        "Adventure Surface",
        "Shared Gameplay Hooks",
        "Static Coverage",
    ):
        assert_contains(raw, token)


def test_all_companions_have_direct_talk_pending_incident_files() -> None:
    companions = (
        "alayen",
        "artimenner",
        "baheshtur",
        "borcha",
        "bunduk",
        "deshavi",
        "firentis",
        "jeremus",
        "katrin",
        "klethi",
        "lezalit",
        "marnid",
        "matheld",
        "nizar",
        "rolf",
        "ymira",
    )
    base = ROOT / "src/dialogs/ZE01_companions_and_named_npcs"
    for companion in companions:
        assert (base / f"anyone_companion_depth_{companion}.py").exists(), f"missing NPC direct talk for {companion}"
        assert (base / f"anyone_plyr_companion_depth_{companion}.py").exists(), f"missing player direct talk for {companion}"
    order = read("src/dialogs/_order_dialogs.txt")
    for companion in companions:
        assert_contains(order, f"anyone_companion_depth_{companion}.py")
        assert_contains(order, f"anyone_plyr_companion_depth_{companion}.py")


def test_companion_incidents_store_focus_center_or_cause() -> None:
    companion = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    focus_tokens = (
        "$g_sod_lezalit_ief_discipline_focus_cause",
        "$g_sod_bunduk_line_cause",
        "$g_sod_jeremus_triage_focus_cause",
        "$g_sod_firentis_restitution_focus_center",
        "$g_sod_firentis_restitution_focus_cause",
        "$g_sod_ymira_refugee_focus_center",
        "$g_sod_katrin_last_coin_cause",
        "$g_sod_deshavi_trail_warning_cause",
        "$g_sod_deshavi_trail_focus_center",
        "$g_sod_klethi_old_job_cause",
        "$g_sod_rolf_name_challenge_focus_cause",
        "$g_sod_alayen_standard_cause",
        "$g_sod_nizar_charge_focus_cause",
        "$g_sod_baheshtur_saddle_cause",
        "$g_sod_matheld_no_backward_step_cause",
        "$g_sod_artimenner_siege_cause",
    )
    for token in focus_tokens:
        assert_contains(companion, token)
    assert_contains(companion, "script_sod_companion_select_focus_village")
    assert_contains(companion, "sod_companion_focus_restitution_village")


def test_companion_adventure_surfaces_are_documented_and_present() -> None:
    surfaces = (
        "src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_companion_marnid_market.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_ymira_refugees.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_firentis_restitution.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_companion_ymira_refugee.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_companion_rolf_name.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_companion_alayen_standard.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_slaver_world_caravan_companion_deshavi_pursuer.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_companion_baheshtur_rider.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_guard_companion_baheshtur_rider.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_companion_klethi_contact.py",
    )
    for surface in surfaces:
        assert (ROOT / surface).exists(), f"missing companion adventure surface: {surface}"
    audit = read("docs/reports/companion_incident_modernization_audit.md")
    assert_contains(audit, "camp menu is a fallback")
    assert_contains(audit, "focus village")


def test_major_systems_call_companion_reaction_hooks() -> None:
    all_src = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in iter_source_files("src"))
    companion = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    assert_contains(companion, "sod_companion_dispatch_player_action")
    assert_contains(companion, "script_sod_companion_apply_player_action")
    major_surfaces = {
        "slavery": (
            "src/scripts/ZY_helper_scripts/sod_slavers_black_market.py",
            ("script_sod_companion_dispatch_player_action", "sod_companion_action_carry_slaves"),
        ),
        "mercy_and_prisoners": (
            "src/scripts/ZY_helper_scripts/sod_prisoner_economy.py",
            ("script_sod_companion_dispatch_player_action", "sod_companion_action_free_captives"),
        ),
        "raids_and_mini_factions": (
            "src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py",
            ("script_sod_companion_dispatch_player_action", "sod_companion_action_jotnar_support"),
        ),
        "diplomacy": (
            "src/scripts/ZY_helper_scripts/sod_diplomacy_system.py",
            ("script_sod_companion_dispatch_player_action", "sod_companion_action_execute_lord"),
        ),
        "ief": (
            "src/scripts/ZY_helper_scripts/sod_companion_depth.py",
            ("sod_companion_try_lezalit_ief_discipline_incident", "sod_companion_action_defeat_imperials"),
        ),
        "black_khergit_tribute": (
            "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
            (
                "script_sod_companion_dispatch_player_action",
                "sod_companion_action_black_khergit_tribute",
                "sod_companion_action_black_khergit_bribe",
            ),
        ),
        "trade_contracts": (
            "src/scripts/ZY_helper_scripts/sod_trade_network.py",
            ("script_sod_companion_dispatch_player_action", "sod_companion_action_caravan_protection"),
        ),
        "company_morale": (
            "src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py",
            ("script_sod_companion_dispatch_player_action", "sod_companion_action_threatened_troops"),
        ),
    }
    for name, (path, tokens) in major_surfaces.items():
        raw = read(path)
        for token in tokens:
            assert_contains(raw, token)
        if path != "src/scripts/ZY_helper_scripts/sod_companion_depth.py":
            assert "script_sod_companion_apply_player_action" not in raw, f"{name} should use dispatch wrapper"
    assert all_src.count("script_sod_companion_apply_player_action") >= 40, "major gameplay hooks should feed companion reactions"


def test_warning_and_reconciliation_exist_before_departure_logic() -> None:
    companion = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "slot_troop_companion_warning_state",
        "sod_companion_warning_pending",
        "sod_companion_warning_acknowledged",
        "sod_companion_reconciliation_to_s0",
        "script_sod_companion_try_trigger_reaction",
    ):
        assert_contains(companion, token)
    dialogs = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in iter_source_files("src/dialogs/ZE01_companions_and_named_npcs"))
    assert_contains(dialogs, "companion_quitting")
    assert_contains(dialogs, "warning")
    assert_contains(dialogs, "reconciliation")


def test_phase7_mini_faction_modernization_audit_report_exists() -> None:
    raw = read("docs/reports/mini_faction_modernization_audit.md")
    for token in (
        "# Mini-Faction Modernization Audit",
        "Shared Pressure Vocabulary",
        "Countermeasure Cooldowns",
        "Cross-Faction Reactions",
        "Party Template Dialogue Coverage",
    ):
        assert_contains(raw, token)


def test_mini_faction_pressure_descriptors_and_cooldowns_are_centralized() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py")
    for token in (
        "sod_mini_faction_get_pressure_descriptor_to_s33",
        "calm",
        "watched",
        "active",
        "dangerous",
        "sod_mini_faction_get_countermeasure_cooldown_to_regs",
        "$g_sod_mini_faction_last_targeted_counterplay_day",
        "$g_sod_mini_faction_last_countermeasure_day",
        "script_sod_mini_faction_get_pressure_descriptor_to_s33",
        "script_sod_mini_faction_get_countermeasure_cooldown_to_regs",
    ):
        assert_contains(raw, token)


def test_mini_faction_party_templates_have_encounter_dialogue() -> None:
    templates = read("compile/module_party_templates.py")
    startup_dialogs = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in iter_source_files("src/dialogs/ZA01_startup_and_dispatch")
    )
    expected = {
        "slavers_caravan": "party_tpl|pt_slavers_caravan",
        "black_army_patrol": "party_tpl|pt_black_army_patrol",
        "black_army_contract_column": "party_tpl|pt_black_army_contract_column",
        "elephant_guard_sanctuary_patrol": "party_tpl|pt_elephant_guard_sanctuary_patrol",
        "elephant_guard_relic_procession": "party_tpl|pt_elephant_guard_relic_procession",
        "jotnar_hearth_guard": "party_tpl|pt_jotnar_hearth_guard",
        "jotnar_wintering_camp": "party_tpl|pt_jotnar_wintering_camp",
        "serpent_host_route_screen": "party_tpl|pt_serpent_host_route_screen",
        "serpent_host_courier_lance": "party_tpl|pt_serpent_host_courier_lance",
        "black_khergit_raiders": "party_tpl|pt_black_khergit_raiders",
        "black_khergit_horde_camp": "party_tpl|pt_black_khergit_horde_camp",
        "black_khergit_night_guard": "party_tpl|pt_black_khergit_night_guard",
    }
    for template_id, dialogue_state in expected.items():
        assert_contains(templates, f'("{template_id}"')
        assert_contains(startup_dialogs, dialogue_state)
    assert_contains(templates, '("boar_clan_fighters"')
    assert_contains(startup_dialogs, "boar_clan_meet")


def test_mini_faction_cross_reaction_links_are_pinned() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py")
    constants = read("src/constants/module_constants.py")
    slaver_market = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    assert_contains(raw, "sod_mini_faction_dispatch_cross_reaction")
    cross_start = raw.index('("sod_mini_faction_dispatch_cross_reaction"')
    cross_end = raw.index('("sod_mini_faction_apply_incident_footprint"', cross_start)
    cross = raw[cross_start:cross_end]
    anti_slavery_tokens = (
        "sod_mini_faction_incident_slaver_heat",
        "script_sod_jotnar_spawn_world_activity",
        "script_sod_elephant_guard_spawn_world_activity",
        "script_sod_slavers_apply_market_delta",
        "slot_faction_jotnar_hearth_pressure",
        "slot_faction_elephant_guard_slaver_alarm",
        "sod_companion_action_free_captives",
    )
    road_pressure_tokens = (
        "sod_mini_faction_incident_black_khergit_raid",
        "sod_mini_faction_incident_boar_tolls",
        "sod_mini_faction_incident_serpent_warning",
        "sod_mini_faction_incident_black_army_contract",
        "fac_black_khergits",
        "fac_sod_merc_guild7",
        "fac_sod_merc_guild5",
        "fac_sod_merc_guild1",
        "slot_faction_black_khergit_pressure",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
        "sod_companion_action_black_army_security",
    )
    for token in anti_slavery_tokens + road_pressure_tokens:
        assert_contains(cross, token)
    # Incident cross-reactions now use the centralized market-delta script
    # rather than duplicating the faction-slot read/write pair locally.
    assert_contains(slaver_market, '("sod_slavers_apply_market_delta"')
    assert_contains(slaver_market, '(faction_get_slot, ":supply", "fac_sod_merc_guild6", slot_faction_slaver_market_supply)')
    assert_contains(slaver_market, '(faction_set_slot, "fac_sod_merc_guild6", slot_faction_slaver_market_supply, ":supply")')
    owned_pairs = (
        ('"fac_sod_merc_guild4"', "slot_faction_jotnar_hearth_pressure", "# Jotnar Clan hearth camps. Used by fac_sod_merc_guild4 only."),
        ('"fac_sod_merc_guild3"', "slot_faction_elephant_guard_slaver_alarm", "# Elephant Guard sacred wardens. Used by fac_sod_merc_guild3 only."),
        ('"fac_black_khergits"', "slot_faction_black_khergit_pressure", "# Black Khergit moving horde. Used by fac_black_khergits only."),
        ('"fac_sod_merc_guild7"', "slot_faction_boar_frontier_pressure", "# Boar Clan frontier toll bands. Used by fac_sod_merc_guild7 only."),
        ('"fac_sod_merc_guild5"', "slot_faction_serpent_route_pressure", "# Serpent Host route screens. Used by fac_sod_merc_guild5 only."),
        ('"fac_sod_merc_guild1"', "slot_faction_black_army_contract_heat", "# Black Army road-security contracts. Used by fac_sod_merc_guild1 only."),
    )
    for faction, slot, comment in owned_pairs:
        assert_contains(constants, comment)
        get_pattern = f"(faction_get_slot, "
        set_pattern = f"(faction_set_slot, {faction}, {slot},"
        assert_contains(cross, faction)
        assert_contains(cross, slot)
        assert_contains(cross, set_pattern)
        assert_contains(cross, get_pattern)
    assert cross.index("sod_mini_faction_incident_slaver_heat") < cross.index("script_sod_jotnar_spawn_world_activity")
    assert cross.index("sod_mini_faction_incident_black_khergit_raid") < cross.index("slot_faction_serpent_route_pressure")
    assert cross.index("sod_mini_faction_incident_boar_tolls") < cross.index("slot_faction_black_army_contract_heat")
    assert cross.index("sod_mini_faction_incident_black_army_contract") < cross.index("slot_faction_boar_frontier_pressure")


def test_phase8_economy_trade_company_audit_report_exists() -> None:
    raw = read("docs/reports/economy_trade_company_modernization_audit.md")
    for token in (
        "# Economy, Trade, And Company Systems Modernization Audit",
        "Trade Network",
        "Company Accounts And Morale",
        "Static Coverage Targets",
        "Manual QA",
    ):
        assert_contains(raw, token)


def test_trade_network_validates_caravan_origin_destination_slots() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(raw, "sod_trade_network_validate_center_to_reg")
    assert raw.count("script_sod_trade_network_validate_center_to_reg") >= 7
    for token in (
        "(neg|is_between, reg0, centers_begin, centers_end)",
        '(call_script, "script_sod_trade_network_validate_center_to_reg", ":origin", ":destination")',
        '(call_script, "script_sod_trade_network_validate_center_to_reg", ":destination", ":origin")',
        '(is_between, ":center_no", centers_begin, centers_end)',
        '(is_between, "$g_sod_trade_network_last_result_center", centers_begin, centers_end)',
        '"@the next market"',
        '"@ordinary market"',
    ):
        assert_contains(raw, token)


def test_trade_network_dialogue_calls_description_helpers() -> None:
    dialogue_dir = ROOT / "src/dialogs/ZC01_centers_and_economy"
    description_files = (
        "anyone_plyr_merchant_talk_trade_avoid.py",
        "anyone_plyr_merchant_talk_trade_cargo.py",
        "anyone_plyr_merchant_talk_trade_destination.py",
        "anyone_plyr_merchant_talk_trade_goods.py",
        "anyone_plyr_merchant_talk_trade_origin.py",
        "anyone_plyr_merchant_talk_trade_protection.py",
        "anyone_plyr_merchant_talk_trade_roads.py",
        "anyone_plyr_merchant_talk_trade_summary.py",
    )
    contract_files = (
        "anyone_plyr_merchant_talk_trade_buy_space.py",
        "anyone_plyr_merchant_talk_trade_fund_guards.py",
        "anyone_plyr_merchant_talk_trade_insure.py",
        "anyone_plyr_merchant_talk_trade_profit.py",
        "anyone_plyr_merchant_talk_trade_relief.py",
    )
    for filename in description_files:
        assert_contains((dialogue_dir / filename).read_text(encoding="utf-8", errors="replace"), "script_sod_trade_network_describe_caravan_to_s20")
    for filename in contract_files:
        assert_contains((dialogue_dir / filename).read_text(encoding="utf-8", errors="replace"), "script_sod_trade_network_apply_player_contract")


def test_trade_route_risk_and_mini_faction_pressure_are_centralized() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(raw, "sod_trade_network_get_route_pressure_to_regs")
    eval_start = raw.index('("sod_trade_network_evaluate_route"')
    eval_end = raw.index('("sod_trade_network_describe_center_identity_to_s23"', eval_start)
    evaluate = raw[eval_start:eval_end]
    assert_contains(evaluate, "script_sod_trade_network_get_route_pressure_to_regs")
    for slot in (
        "slot_faction_boar_frontier_pressure",
        "slot_faction_black_khergit_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
    ):
        assert f"(faction_get_slot," not in evaluate or slot not in evaluate, f"{slot} should be read through the pressure helper"


def test_company_troop_dialogue_terminal_safety_and_focus() -> None:
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    dialogue = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    menu = read("src/menus/camp/company_spokesperson.py")
    for token in (
        "$g_sod_company_spokesperson_focus_party",
        "$g_sod_company_spokesperson_focus_center",
        "$g_sod_company_spokesperson_focus_cause",
        "$g_sod_company_spokesperson_focus_class",
        "$g_sod_company_spokesperson_focus_severity",
    ):
        assert_contains(accounts, token)
        assert_contains(dialogue, token)
    for token in (
        "sod_company_dialogue_store_incident_focus",
        "script_sod_company_dialogue_store_incident_focus",
        "Focus: this grievance",
    ):
        assert_contains(dialogue, token)
    assert menu.count('(jump_to_menu, "mnu_company_accounts")') >= 10
    for option in (
        "company_spokesperson_pay_now",
        "company_spokesperson_promise",
        "company_spokesperson_battle_promise",
        "company_spokesperson_rations",
        "company_spokesperson_wounded",
        "company_spokesperson_hazard_pay",
        "company_spokesperson_offering",
        "company_spokesperson_recreation",
        "company_spokesperson_persuade",
        "company_spokesperson_mediator",
        "company_spokesperson_threaten",
        "company_spokesperson_dismiss",
        "company_spokesperson_back",
    ):
        option_start = menu.index(f'("{option}"')
        next_option = menu.find('\n     ("company_spokesperson_', option_start + 1)
        option_block = menu[option_start: next_option if next_option != -1 else len(menu)]
        assert "jump_to_menu" in option_block, f"{option} lacks explicit terminal menu jump"
    assert "change_screen_return" not in menu


def test_company_mutiny_desertion_dialogue_closure_paths() -> None:
    raw = read("src/menus/camp/company_accounts.py")
    for menu_id in (
        "company_desertion_petition",
        "company_mutiny_warning",
        "company_mutiny_resolution",
        "company_spokesperson_incident",
    ):
        assert_contains(raw, menu_id)
    for target in (
        'jump_to_menu, "mnu_company_accounts"',
        'jump_to_menu, "mnu_company_mutiny_warning"',
        'jump_to_menu, "mnu_company_mutiny_resolution"',
        'jump_to_menu, "mnu_simple_encounter"',
    ):
        assert_contains(raw, target)
    assert_not_contains(raw, "company_accounts_desertion")
    assert_not_contains(raw, "company_accounts_mutiny")
    company_block = raw[raw.index('("company_desertion_petition"'):]
    assert "change_screen_return" not in company_block
    for option in (
        "company_desertion_paid",
        "company_desertion_persuade",
        "company_desertion_battle_promise",
        "company_desertion_unpaid",
        "company_desertion_forbid",
        "company_desertion_none",
        "company_desertion_spokesperson",
        "company_desertion_back",
        "company_mutiny_negotiate",
        "company_mutiny_pay_half",
        "company_mutiny_drill",
        "company_mutiny_threaten",
        "company_mutiny_resolution",
        "company_mutiny_none",
        "company_mutiny_spokesperson",
        "company_mutiny_back",
        "company_mutiny_resolve_settlement",
        "company_mutiny_resolve_expel",
        "company_mutiny_resolve_battle",
        "company_mutiny_resolve_defer",
        "company_mutiny_resolution_back",
    ):
        option_start = raw.index(f'("{option}"')
        next_option = raw.find('\n     ("company_', option_start + 1)
        option_block = raw[option_start: next_option if next_option != -1 else len(raw)]
        assert "jump_to_menu" in option_block, f"{option} lacks explicit terminal menu jump"


def test_in_battle_morale_hooks_are_present_in_high_risk_templates() -> None:
    lead_charge = read("src/mission_templates/0010_lead_charge/lead_charge.py")
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    belfry = read("src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py")
    ladder = read("src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py")
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    for token in (
        "script_sod_battle_initialize_morale_context",
        "script_sod_company_dialogue_process_battle_start_morale",
    ):
        assert_contains(lead_charge, token)
    for token in (
        "formations_update_morale",
        "formations_update_route",
        "common_battle_mission_start",
        "common_siege_attacker_morale_pressure",
    ):
        assert_contains(preamble, token)
    assert_contains(belfry, "common_siege_attacker_morale_pressure")
    assert_contains(ladder, "common_siege_attacker_morale_pressure")
    assert_contains(accounts, "script_sod_company_dialogue_process_post_battle_prompt")


def test_phase9_builder_doctor_tooling_guard_exists() -> None:
    doctor = read("build/doctor.py")
    checklist = read("docs/tooling/MODULE_SYSTEM_MODERNIZATION_CHECKLIST.md")
    for token in (
        "_check_modernization_tooling_guards",
        "modernization_tooling_guards",
        "builder_doctor_tooling_audit.md",
        "test_dialogue_outputs_have_matching_inputs_or_safe_terminals",
        "test_generic_continue_menus_do_not_only_change_screen_return",
        "test_high_frequency_ai_scripts_do_not_use_unguarded_global_party_ops",
        "test_warband_presentation_callbacks_are_absent_for_mb1011",
        "sod_party_is_safe_active_to_reg",
        "script_sod_safe_leave_encounter",
    ):
        assert_contains(doctor, token)
    for row in (
        "- [x] Add doctor checks for dialogue graph input/output validity.",
        "- [x] Add doctor checks for unsafe post-mission `change_screen_return`.",
        "- [x] Add doctor checks for unguarded high-frequency party operations.",
        "- [x] Add doctor checks for missing M&B 1.011 hardcoded callback compatibility notes.",
        "- [x] Add doctor checks for stale files listed in `_order_*.txt`.",
        "- [x] Add doctor checks for duplicate menu/dialog IDs where unsafe.",
        "- [x] Add modernization test coverage for high-frequency AI party safety.",
        "- [x] Add modernization test coverage for camp/report invalid target fallbacks.",
        "- [x] Add modernization test coverage for quest sentinel/order safety.",
        "- [x] Add modernization test coverage for M&B 1.011 callback compatibility.",
    ):
        assert_contains(checklist, row)


def test_phase9_builder_doctor_tooling_audit_report_exists() -> None:
    raw = read("docs/reports/builder_doctor_tooling_audit.md")
    for token in (
        "# Builder, Doctor, And Tooling Audit",
        "Doctor Coverage",
        "Static Coverage",
        "Runtime Helper Coverage",
        "Manual QA",
        "Dialogue graph input/output validity",
        "M&B 1.011 hardcoded callback compatibility",
    ):
        assert_contains(raw, token)


def test_phase9_static_high_frequency_ai_party_safety() -> None:
    test_high_frequency_distance_calls_are_audited()
    test_global_party_operations_are_audited_in_scripts_and_triggers()
    test_high_frequency_ai_scripts_do_not_use_unguarded_global_party_ops()


def test_phase9_static_camp_report_invalid_target_fallbacks() -> None:
    test_center_name_fallback_helper_validates_center_range()
    test_mini_faction_reports_use_center_fallback_helper()
    test_faction_target_center_names_are_range_guarded_or_fallbacked()
    test_report_menus_call_description_scripts_and_use_fallbacks()


def test_phase9_static_quest_sentinel_order_safety() -> None:
    test_quest_end_sentinel_is_isolated_and_last()
    test_quest_runtime_journal_memory_outcome_surfaces_exist()


def test_phase9_static_mb1011_callback_compatibility() -> None:
    test_warband_presentation_callbacks_are_absent_for_mb1011()
    hardcoded_scripts = "\n".join(path.name for path in iter_source_files("src/scripts/ZA_hardcoded_game_scripts"))
    assert_contains(hardcoded_scripts, "game_check_party_sees_party.py")
    assert_contains(hardcoded_scripts, "game_get_party_speed_multiplier.py")


def test_runtime_regression_hardening_audit_exists() -> None:
    raw = read("docs/reports/runtime_regression_hardening_audit.md")
    for token in (
        "# Runtime Regression Hardening Audit",
        "Message-Log Spam Prevention",
        "Encounter State Cleanup",
        "Battle Aftermath Robustness",
        "script_sod_battle_aftermath_validate_globals_to_regs",
        "script_sod_sanitize_encounter_globals",
    ):
        assert_contains(raw, token)


def test_runtime_encounter_cleanup_sanitizes_all_high_risk_globals() -> None:
    raw = read("src/scripts/ZE_encounters/sod_safe_leave_encounter.py")
    for token in (
        '"sod_safe_leave_encounter"',
        '"sod_sanitize_encounter_globals"',
        'script_sod_sanitize_encounter_globals',
        '$g_encountered_party',
        '$g_encountered_party_2',
        '$g_enemy_party',
        '$g_talk_troop_party',
        '$current_town',
        '(assign, "$g_leave_encounter", 1)',
        '(neg|party_is_active, "$g_enemy_party")',
        '(neg|party_is_active, "$g_talk_troop_party")',
        '(neg|is_between, "$current_town", centers_begin, centers_end)',
        '(assign, "$current_town", -1)',
    ):
        assert_contains(raw, token)
    assert raw.index('(neg|is_between, "$current_town", centers_begin, centers_end)') < raw.index('(assign, "$current_town", -1)')


def test_runtime_battle_aftermath_validates_globals_before_party_ops() -> None:
    helper = read("src/scripts/ZE_encounters/sod_battle_aftermath_validate_globals_to_regs.py")
    total = read("src/scripts/ZC_parties/total_victory_finalize.py")
    defeated = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    captured = read("src/scripts/ZC_parties/event_hero_taken_prisoner_by_player.py")
    for token in (
        '"sod_battle_aftermath_validate_globals_to_regs"',
        '$g_enemy_party',
        '$g_ally_party',
        '$g_encountered_party',
        '(party_is_active, "$g_enemy_party")',
        '(party_is_active, "$g_ally_party")',
        '(party_is_active, "$g_encountered_party")',
    ):
        assert_contains(helper, token)
    validate_idx = total.index("script_sod_battle_aftermath_validate_globals_to_regs")
    threat_idx = total.index("script_sod_threat_board_note_party_defeated")
    clear_idx = total.index("script_clear_party_group")
    assert validate_idx < threat_idx < clear_idx
    assert_contains(total, "script_sod_safe_leave_encounter")
    assert_contains(defeated, "(store_script_param_1, \":defeated_party\")")
    assert_contains(defeated, "(party_is_active, \":defeated_party\")")
    assert_contains(defeated, '(assign, "$g_enemy_party", -1)')
    assert_contains(captured, "(is_between, \":troop_no\", heroes_begin, heroes_end)")
    assert captured.index('(is_between, ":troop_no", heroes_begin, heroes_end)') < captured.index("script_sod_quest_battle_note_target_captured")


def test_runtime_sanity_report_is_registered_and_scrubs_stale_state() -> None:
    helper = read("src/scripts/ZE_encounters/sod_safe_leave_encounter.py")
    menu = read("src/menus/reports/runtime_sanity_report.py")
    reports = read("src/menus/0000_hardcoded_mb1011/reports.py")
    order = read("src/menus/_order_game_menus.txt")
    audit = read("docs/reports/runtime_regression_hardening_audit.md")
    for token in (
        '"sod_describe_runtime_sanity_to_s20"',
        "Runtime Sanity Report",
        "$g_encountered_party",
        "$g_encountered_party_2",
        "$g_enemy_party",
        "$g_talk_troop_party",
        "$g_ally_party",
        "$current_town",
        "none or stale",
    ):
        assert_contains(helper, token)
    for token in (
        '"runtime_sanity_report"',
        "script_sod_describe_runtime_sanity_to_s20",
        "script_sod_sanitize_encounter_globals",
        '("runtime_sanity_scrub", [',
        '(this_or_next|eq, "$cheat_mode", 1)',
        '(eq, "$g_sod_cheat_mode", 1)',
        '(neq, "$cheat_mode", 1)',
        '(neq, "$g_sod_cheat_mode", 1)',
        'jump_to_menu, "mnu_runtime_sanity_report"',
        'jump_to_menu, "mnu_reports"',
    ):
        assert_contains(menu, token)
    assert_contains(reports, 'jump_to_menu, "mnu_runtime_sanity_report"')
    assert_contains(reports, '("view_runtime_sanity_report", [')
    assert_contains(reports, '(this_or_next|eq, "$cheat_mode", 1)')
    assert_contains(reports, '(eq, "$g_sod_cheat_mode", 1)')
    assert_contains(order, "reports/runtime_sanity_report.py")
    assert_contains(audit, "mnu_runtime_sanity_report")


def test_capture_prisoner_flow_validates_capturer_party() -> None:
    helper = read("src/scripts/ZE_encounters/sod_safe_leave_encounter.py")
    captured = read("src/scripts/ZC_parties/event_player_captured_as_prisoner.py")
    wilderness = read("src/menus/captivity/captivity_wilderness_check.py")
    castle = read("src/menus/captivity/captivity_castle_check.py")
    ransom = read("src/menus/captivity/captivity_end_ransom_accept.py")
    audit = read("docs/reports/runtime_regression_hardening_audit.md")
    for token in (
        '"sod_validate_capturer_party_to_reg"',
        '"sod_capture_set_capturer_from_encounter_to_reg"',
        '$capturer_party',
        '(neg|party_is_active, "$capturer_party")',
        '(assign, reg0, 1)',
    ):
        assert_contains(helper, token)
    assert captured.index("script_sod_validate_capturer_party_to_reg") < captured.index("store_faction_of_party")
    for raw in (wilderness, castle):
        validate_idx = raw.index("script_sod_validate_capturer_party_to_reg")
        store_idx = raw.index("store_faction_of_party")
        assert validate_idx < store_idx
        assert_contains(raw, '(assign, ":capturer_faction", "fac_outlaws")')
        assert_contains(raw, '(eq, reg0, 1)')
    assert ransom.index("script_sod_validate_capturer_party_to_reg") < ransom.index("party_relocate_near_party")
    assert_contains(ransom, "script_sod_sanitize_encounter_globals")
    for token in (
        "Capture And Prisoner Flow Guards",
        "script_sod_validate_capturer_party_to_reg",
        "script_sod_capture_set_capturer_from_encounter_to_reg",
        "$capturer_party",
    ):
        assert_contains(audit, token)


def test_captivity_start_menus_select_safe_capturer() -> None:
    start_files = (
        "src/menus/captivity/captivity_start_castle_defeat.py",
        "src/menus/captivity/captivity_start_castle_surrender.py",
        "src/menus/captivity/captivity_start_under_siege_defeat.py",
        "src/menus/captivity/captivity_start_wilderness.py",
        "src/menus/captivity/captivity_start_wilderness_defeat.py",
        "src/menus/captivity/captivity_start_wilderness_surrender.py",
    )
    for rel in start_files:
        raw = read(rel)
        assert_contains(raw, "script_sod_capture_set_capturer_from_encounter_to_reg")
        assert_not_contains(raw, '(assign, "$capturer_party", "$g_encountered_party")')


def test_runtime_sanity_report_includes_capture_fields() -> None:
    helper = read("src/scripts/ZE_encounters/sod_safe_leave_encounter.py")
    menu = read("src/menus/reports/runtime_sanity_report.py")
    for token in (
        "$capturer_party",
        "$g_sod_last_runtime_cleanup_day",
        "Capturer party",
        "Last cleanup day",
        "script_sod_sanitize_encounter_globals",
    ):
        assert_contains(helper, token)
    assert_contains(menu, "script_sod_sanitize_encounter_globals")


def test_runtime_trace_notes_cover_battle_capture_ransom_and_death() -> None:
    helper = read("src/scripts/ZE_encounters/sod_safe_leave_encounter.py")
    defeated = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    captured = read("src/scripts/ZC_parties/event_hero_taken_prisoner_by_player.py")
    ransom = read("src/menus/captivity/captivity_end_ransom_accept.py")
    death = read("src/scripts/ZC_parties/total_victory_try_enemy_hero_resolution.py")
    audit = read("docs/reports/runtime_regression_hardening_audit.md")
    for token in (
        '"sod_runtime_trace_event"',
        "$g_sod_last_runtime_trace_day",
        "$g_sod_last_runtime_trace_event",
        "$g_sod_last_runtime_trace_party",
        "$g_sod_last_runtime_trace_troop",
        "$g_sod_last_runtime_trace_menu",
        "$g_sod_last_runtime_trace_enemy_party",
        "$g_sod_last_runtime_trace_capturer_party",
        "$g_sod_last_defeated_party",
        "$g_sod_last_captured_hero",
        "Last runtime trace",
        "Trace party",
        "Trace troop",
        "Trace enemy party",
        "Trace capturer party",
        "Last defeated party",
        "Last captured hero",
    ):
        assert_contains(helper, token)
    assert_contains(defeated, '(call_script, "script_sod_runtime_trace_event", 1, ":defeated_party", -1)')
    assert_contains(captured, '(call_script, "script_sod_runtime_trace_event", 2, "p_main_party", ":troop_no")')
    assert_contains(ransom, '(call_script, "script_sod_runtime_trace_event", 4, "$capturer_party", "trp_player")')
    assert_contains(death, '(call_script, "script_sod_runtime_trace_event", 5, "$g_enemy_party", ":stack_troop")')
    for token in (
        "Runtime Trace Notes",
        "script_sod_runtime_trace_event",
        "defeated_enemy_party",
        "hero_taken_prisoner",
        "ransom acceptance",
        "hero death paths",
    ):
        assert_contains(audit, token)


def test_player_hero_capture_lifecycle_uses_shared_helper() -> None:
    helper = read("src/scripts/ZC_parties/sod_player_capture_hero_to_reg.py")
    defeated_hero = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_defeat_hero_answer.py")
    defeated_lord = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_defeat_lord_answer_02.py")
    freed_lord = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_freed_lord_answer.py")
    audit = read("docs/reports/runtime_regression_hardening_audit.md")
    for token in (
        '"sod_player_capture_hero_to_reg"',
        "(is_between, \":troop_no\", heroes_begin, heroes_end)",
        "script_remove_troop_from_prison",
        "slot_troop_prisoner_of_party",
        "party_count_prisoners_of_type",
        "party_force_add_prisoners",
        "script_event_hero_taken_prisoner_by_player",
        "script_sod_runtime_trace_event",
        "$g_sod_last_captured_hero",
    ):
        assert_contains(helper, token)
    for raw in (defeated_hero, defeated_lord, freed_lord):
        assert_contains(raw, "script_sod_player_capture_hero_to_reg")
    assert_not_contains(defeated_hero, '(party_add_prisoners, "p_main_party", "$g_talk_troop", 1)')
    assert_contains(audit, "Lord And Hero Prisoner Lifecycle")


def test_ief_hero_death_branches_record_runtime_trace() -> None:
    death_files = (
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_4.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpdla_nihilistic_10.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_legate_execution_7.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_execute.py",
    )
    for rel in death_files:
        raw = read(rel)
        assert raw.index("script_sod_runtime_trace_event") < raw.index("script_kill_kingdom_hero")
    safe_death = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_4.py")
    assert_contains(safe_death, "script_sod_safe_leave_encounter")
    assert_not_contains(safe_death, '(assign, "$g_leave_encounter", 1)')


def test_hero_prisoner_release_clears_slot_and_stack() -> None:
    remove = read("src/scripts/ZH_heroes/remove_troop_from_prison.py")
    ransom = read("src/menus/captivity/ransom_accept.py")
    lord_sale = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_buy_prisoner_accept.py")
    for token in (
        "slot_troop_prisoner_of_party",
        '(troop_get_slot, ":prisoner_of_party", ":troop_no", slot_troop_prisoner_of_party)',
        '(party_is_active, ":prisoner_of_party")',
        "party_count_prisoners_of_type",
        "party_remove_prisoners",
        '(troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1)',
        '(call_script, "script_sod_runtime_trace_event", 6, -1, ":troop_no")',
    ):
        assert_contains(remove, token)
    assert ransom.index('(party_is_active, "$g_ransom_offer_party")') < ransom.index('(party_remove_prisoners, "$g_ransom_offer_party", "$g_ransom_offer_troop", 1)')
    assert_contains(ransom, '(call_script, "script_remove_troop_from_prison", "$g_ransom_offer_troop")')
    assert_contains(lord_sale, '(call_script, "script_remove_troop_from_prison", "$prisoner_lord_to_buy")')
    assert lord_sale.index('(party_is_active, "$g_encountered_party")') < lord_sale.index('(party_add_prisoners, "$g_encountered_party", "$prisoner_lord_to_buy", 1)')
    assert_contains(lord_sale, '(call_script, "script_sod_runtime_trace_event", 7, "$g_encountered_party", "$prisoner_lord_to_buy")')


def test_hero_death_clears_prisoner_ownership_first() -> None:
    kill = read("src/scripts/ZF_factions/kill_kingdom_hero.py")
    assert kill.index("script_remove_troop_from_prison") < kill.index("slot_troop_occupation, slto_dead")
    assert kill.index("script_sod_runtime_trace_event") < kill.index("slot_troop_occupation, slto_dead")


def test_note_from_sreg_calls_do_not_use_literal_strings() -> None:
    offenders = []
    pattern = re.compile(
        r"\((add_(?:troop|party|faction|quest)_note_from_sreg),\s*([^,\n]+),\s*([^,\n]+),\s*(?:@\"|\"@)"
    )
    for root in ("src/dialogs", "src/menus", "src/scripts", "src/triggers"):
        for path in iter_source_files(root):
            raw = path.read_text(encoding="utf-8", errors="replace")
            for match in pattern.finditer(raw):
                offenders.append((str(path.relative_to(ROOT)).replace("\\", "/"), match.group(1)))
    assert not offenders, "literal quick strings passed to *_note_from_sreg can leak stale sregs: " + repr(offenders[:20])


def test_weekly_population_news_is_gated_against_census_spam() -> None:
    town = read("src/triggers/ST04_weekly/entry_0101.py")
    village = read("src/triggers/ST04_weekly/entry_0102.py")
    for raw, threshold in ((town, 'ge, ":abs_growth", 20'), (village, 'ge, ":abs_growth", 8')):
        assert_contains(raw, ":should_report_population_change")
        assert_contains(raw, 'slot_town_lord, "trp_player"')
        assert_contains(raw, '"$players_kingdom"')
        assert_contains(raw, threshold)
        assert_contains(raw, '(eq, ":should_report_population_change", 1)')
        assert raw.index('(eq, ":should_report_population_change", 1)') < raw.index("Word reaches you from")


def test_world_map_trigger_service_scripts_do_not_fail_as_plain_helpers() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_world_map_trigger_services.py")

    for script_name in (
        "sod_world_map_process_player_spotted_center_warnings",
        "sod_refresh_player_map_icon_if_dirty",
        "sod_battle_commander_reset_if_dirty",
    ):
        start = raw.index(f'("{script_name}",')
        end = raw.index(" ]),", start)
        body = raw[start:end]
        assert body.index("(try_begin)") < body.index("(map_free)"), script_name

    spotted = raw[raw.index('"sod_world_map_process_player_spotted_center_warnings"') :]
    center_loop = spotted.index('(try_for_range, ":cur_center", centers_begin, centers_end)')
    center_filter = spotted.index('(store_faction_of_party, ":cur_faction", ":cur_center")')
    assert center_loop < spotted.rfind("(try_begin)", 0, center_filter) < center_filter
    refresh = raw[raw.index('"sod_refresh_player_map_icon_if_dirty"') :]
    refresh_map_free = refresh.index("(map_free)")
    refresh_check = refresh.index('(eq, ":needs_refresh", 1)')
    assert refresh.rfind("(try_begin)", 0, refresh_map_free) < refresh_map_free < refresh_check
    assert refresh.rfind("(try_begin)", 0, refresh_check) < refresh_check
    commander = raw[raw.index('"sod_battle_commander_reset_if_dirty"') :]
    commander_map_free = commander.index("(map_free)")
    commander_reset = commander.index('(call_script, "script_sod_battle_commander_reset")')
    assert commander.rfind("(try_begin)", 0, commander_map_free) < commander_map_free < commander_reset


if __name__ == "__main__":
    test_modernization_checklist_structure()
    test_modernization_checklist_tracks_known_bug_families()
    test_first_slice_has_verification_gate()
    test_dialogue_close_window_audit_report_exists()
    test_dialogue_family_terminal_audit_report_exists()
    test_dialogue_order_references_existing_files()
    test_dialogue_outputs_have_matching_inputs_or_safe_terminals()
    test_restored_dialogue_handoffs_start_and_close_cleanly()
    test_dialogue_outputs_do_not_use_stale_removed_state_names()
    test_duplicate_player_options_do_not_shadow_later_branches()
    test_terminal_post_battle_dialogues_leave_encounter_when_needed()
    test_legion_ief_capture_branches_terminate_safely()
    test_auto_proceed_branches_have_reachable_next_player_option()
    test_map_conversation_ops_are_only_used_in_safe_contexts()
    test_cpdla_captured_centurion_dialogue_family_is_safe()
    test_pelha_surrender_capture_dialogue_family_is_safe()
    test_legate_sq_lore_chains_are_terminal_safe()
    test_lord_politics_dialogue_families_are_graph_safe()
    test_companion_direct_talk_incidents_are_graph_safe()
    test_generic_continue_menus_do_not_only_change_screen_return()
    test_mission_templates_jump_to_menu_before_finish_mission()
    test_encounter_and_camp_safety_guards_remain()
    test_game_event_party_encounter_keeps_mb1011_routing_with_guards()
    test_party_safe_active_guard_helper_exists()
    test_party_id_safety_audit_report_exists()
    test_troop_hero_movement_audit_report_exists()
    test_high_frequency_distance_calls_are_audited()
    test_global_party_operations_are_audited_in_scripts_and_triggers()
    test_party_force_add_prisoners_hero_paths_are_explicit()
    test_party_add_members_talk_troop_rejects_heroes_or_is_intended()
    test_duplicate_unique_hero_stack_risks_are_blocked()
    test_lord_lifecycle_paths_are_audited()
    test_ief_dying_centurion_default_branch_is_terminal()
    test_center_validation_audit_report_exists()
    test_center_name_fallback_helper_validates_center_range()
    test_closest_center_consumers_are_inventoried()
    test_mini_faction_reports_use_center_fallback_helper()
    test_faction_target_center_names_are_range_guarded_or_fallbacked()
    test_touched_closest_center_outputs_are_center_range_checked()
    test_phase3_audit_report_exists()
    test_menu_source_shape_is_export_friendly()
    test_menu_option_brackets_are_balanced_before_export()
    test_jump_to_menu_targets_exist()
    test_camp_report_option_conditions_do_not_call_high_risk_scripts()
    test_report_menus_call_description_scripts_and_use_fallbacks()
    test_warband_presentation_callbacks_are_absent_for_mb1011()
    test_phase4_campaign_ai_audit_report_exists()
    test_campaign_ai_trigger_cadence_is_documented()
    test_high_frequency_ai_scripts_do_not_use_unguarded_global_party_ops()
    test_diplomacy_personality_memory_and_posture_are_centralized()
    test_ief_total_war_and_auxiliary_rules_are_pinned()
    test_kingdom6_only_hero_death_rules_are_static_pinned()
    test_major_battle_templates_keep_formation_and_morale_hooks()
    test_phase5_quest_framework_audit_report_exists()
    test_quest_end_sentinel_is_isolated_and_last()
    test_legacy_quest_wrappers_route_to_runtime_helpers()
    test_quest_runtime_journal_memory_outcome_surfaces_exist()
    test_companion_personal_arcs_have_framework_ids_and_metadata()
    test_companion_quest_journal_text_separates_talk_from_world_incident()
    test_companion_quest_memory_and_outcome_hooks_are_present()
    test_phase6_companion_incident_audit_report_exists()
    test_all_companions_have_direct_talk_pending_incident_files()
    test_companion_incidents_store_focus_center_or_cause()
    test_companion_adventure_surfaces_are_documented_and_present()
    test_major_systems_call_companion_reaction_hooks()
    test_warning_and_reconciliation_exist_before_departure_logic()
    test_phase7_mini_faction_modernization_audit_report_exists()
    test_mini_faction_pressure_descriptors_and_cooldowns_are_centralized()
    test_mini_faction_party_templates_have_encounter_dialogue()
    test_mini_faction_cross_reaction_links_are_pinned()
    test_phase8_economy_trade_company_audit_report_exists()
    test_trade_network_validates_caravan_origin_destination_slots()
    test_trade_network_dialogue_calls_description_helpers()
    test_trade_route_risk_and_mini_faction_pressure_are_centralized()
    test_company_troop_dialogue_terminal_safety_and_focus()
    test_company_mutiny_desertion_dialogue_closure_paths()
    test_in_battle_morale_hooks_are_present_in_high_risk_templates()
    test_phase9_builder_doctor_tooling_guard_exists()
    test_phase9_builder_doctor_tooling_audit_report_exists()
    test_phase9_static_high_frequency_ai_party_safety()
    test_phase9_static_camp_report_invalid_target_fallbacks()
    test_phase9_static_quest_sentinel_order_safety()
    test_phase9_static_mb1011_callback_compatibility()
    test_runtime_regression_hardening_audit_exists()
    test_runtime_encounter_cleanup_sanitizes_all_high_risk_globals()
    test_runtime_battle_aftermath_validates_globals_before_party_ops()
    test_runtime_sanity_report_is_registered_and_scrubs_stale_state()
    test_capture_prisoner_flow_validates_capturer_party()
    test_captivity_start_menus_select_safe_capturer()
    test_runtime_sanity_report_includes_capture_fields()
    test_runtime_trace_notes_cover_battle_capture_ransom_and_death()
    test_player_hero_capture_lifecycle_uses_shared_helper()
    test_ief_hero_death_branches_record_runtime_trace()
    test_hero_prisoner_release_clears_slot_and_stack()
    test_hero_death_clears_prisoner_ownership_first()
    test_note_from_sreg_calls_do_not_use_literal_strings()
    test_weekly_population_news_is_gated_against_census_spam()
    test_world_map_trigger_service_scripts_do_not_fail_as_plain_helpers()
    print("test_modernization_static: OK")




