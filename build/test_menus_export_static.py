from pathlib import Path
import importlib
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def _read_export_tokens() -> list[str]:
    raw = (ROOT / "_export" / "menus.txt").read_text(encoding="utf-8", errors="replace")
    return raw.split()


def _read_generated_menu_ids() -> list[str]:
    import_paths = [
        ROOT / "compile" / "ids",
        ROOT / "compile",
        ROOT / "compile" / "headers",
        ROOT / "compile" / "process",
        ROOT,
    ]
    for path in reversed(import_paths):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
    sys.modules.pop("module_game_menus", None)
    module_game_menus = importlib.import_module("module_game_menus")
    return [f"menu_{menu[0]}" for menu in module_game_menus.game_menus]


def _read_id_menu_assignments() -> dict[str, int]:
    raw = (ROOT / "compile" / "ids" / "ID_menus.py").read_text(
        encoding="utf-8", errors="replace"
    )
    pattern = re.compile(r"(?m)^(menu_[A-Za-z0-9_]+)\s*=\s*(\d+)\s*$")
    return {match.group(1): int(match.group(2)) for match in pattern.finditer(raw)}


def _read_int(tokens: list[str], index: int, context: str) -> tuple[int, int]:
    assert index < len(tokens), f"EOF while reading {context} at token {index}"
    token = tokens[index]
    try:
        return int(token), index + 1
    except ValueError as exc:
        raise AssertionError(
            f"expected integer for {context} at token {index}, got {token!r}"
        ) from exc


def _skip_ops(tokens: list[str], index: int, count: int, context: str) -> int:
    for op_index in range(count):
        _, index = _read_int(tokens, index, f"{context} op-code #{op_index}")
        argc, index = _read_int(tokens, index, f"{context} op-argc #{op_index}")
        assert 0 <= argc <= 1000, f"suspicious argc {argc} in {context} op #{op_index}"
        index += argc
        assert index <= len(tokens), f"EOF while reading {context} op #{op_index} args"
    return index


def test_exported_menus_txt_is_token_parseable() -> None:
    tokens = _read_export_tokens()
    assert tokens[:3] == ["menusfile", "version", "1"]
    index = 3
    declared_count, index = _read_int(tokens, index, "menu count")
    menu_ids: list[str] = []

    for menu_index in range(declared_count):
        assert index < len(tokens), f"EOF before menu #{menu_index}"
        menu_id = tokens[index]
        assert menu_id.startswith("menu_"), (
            f"expected menu id at token {index} after {menu_index} menus, got {menu_id!r}"
        )
        menu_ids.append(menu_id)
        index += 1
        _, index = _read_int(tokens, index, f"{menu_id} flags")
        index += 2  # text, mesh
        menu_ops, index = _read_int(tokens, index, f"{menu_id} operation count")
        index = _skip_ops(tokens, index, menu_ops, f"{menu_id} menu ops")
        option_count, index = _read_int(tokens, index, f"{menu_id} option count")

        for option_index in range(option_count):
            assert index < len(tokens), f"EOF before {menu_id} option #{option_index}"
            option_id = tokens[index]
            assert option_id.startswith("mno_"), (
                f"expected option id for {menu_id} option #{option_index} at token "
                f"{index}, got {option_id!r}"
            )
            index += 1
            condition_ops, index = _read_int(
                tokens, index, f"{menu_id}/{option_id} condition count"
            )
            index = _skip_ops(
                tokens, index, condition_ops, f"{menu_id}/{option_id} conditions"
            )
            index += 1  # option text
            consequence_ops, index = _read_int(
                tokens, index, f"{menu_id}/{option_id} consequence count"
            )
            index = _skip_ops(
                tokens, index, consequence_ops, f"{menu_id}/{option_id} consequences"
            )
            index += 1  # door text

    assert index == len(tokens), f"unparsed trailing menu tokens: {len(tokens) - index}"
    duplicates = sorted({menu_id for menu_id in menu_ids if menu_ids.count(menu_id) > 1})
    assert not duplicates, f"duplicate exported menu id(s): {duplicates}"


def test_mb1011_hardcoded_start_menus_keep_native_indices() -> None:
    ids = (ROOT / "compile" / "ids" / "ID_menus.py").read_text(
        encoding="utf-8", errors="replace"
    )
    expected = {
        "menu_start_game_1": 0,
        "menu_start_phase_2": 1,
    }
    for menu_id, expected_index in expected.items():
        token = f"{menu_id} = {expected_index}"
        assert token in ids

    lines = (ROOT / "_export" / "menus.txt").read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()
    assert lines[2].startswith("menu_start_game_1 ")
    assert lines[4].startswith("menu_start_phase_2 ")


def test_generated_menu_ids_match_generated_menu_module_order() -> None:
    menu_ids = _read_generated_menu_ids()
    id_assignments = _read_id_menu_assignments()

    assert menu_ids, "compile/module_game_menus.py did not yield any menu ids"
    assert id_assignments, "compile/ids/ID_menus.py did not yield any menu ids"
    assert len(menu_ids) == len(id_assignments), (
        f"generated menu count mismatch: module has {len(menu_ids)}, "
        f"ID_menus.py has {len(id_assignments)}"
    )

    expected_assignments = {menu_id: index for index, menu_id in enumerate(menu_ids)}
    assert id_assignments == expected_assignments


def test_literal_menu_references_point_to_existing_generated_menus() -> None:
    id_assignments = _read_id_menu_assignments()
    missing: list[str] = []
    for base in (ROOT / "src" / "menus", ROOT / "src" / "dialogs", ROOT / "src" / "scripts"):
        for path in base.rglob("*.py"):
            raw = path.read_text(encoding="utf-8", errors="replace")
            for match in re.finditer(r'"(mnu_[A-Za-z0-9_]+)"', raw):
                menu_id = f"menu_{match.group(1)[4:]}"
                if menu_id not in id_assignments:
                    line = raw.count("\n", 0, match.start()) + 1
                    rel = path.relative_to(ROOT).as_posix()
                    missing.append(f"{rel}:{line}: {match.group(1)}")

    assert not missing, "missing literal menu target(s):\n" + "\n".join(missing[:50])


def test_menu_fragments_do_not_reuse_option_ids() -> None:
    offenders: list[str] = []
    option_pattern = re.compile(r'\(\s*"([A-Za-z0-9_]+)"\s*,\s*\[')
    menu_pattern = re.compile(r'(?m)^\(\s*"([A-Za-z0-9_]+)"\s*,\s*(?:mnf_[A-Za-z0-9_]+|0)\s*,')
    for path in sorted((ROOT / "src" / "menus").rglob("*.py")):
        raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        raw = "\n".join(line for line in raw_lines if not line.lstrip().startswith("#"))
        menu_matches = list(menu_pattern.finditer(raw))
        for idx, menu_match in enumerate(menu_matches):
            segment_end = menu_matches[idx + 1].start() if idx + 1 < len(menu_matches) else len(raw)
            segment = raw[menu_match.end():segment_end]
            option_ids = option_pattern.findall(segment)
            duplicates = sorted({option_id for option_id in option_ids if option_ids.count(option_id) > 1})
            if duplicates:
                rel = path.relative_to(ROOT).as_posix()
                offenders.append(f"{rel}/{menu_match.group(1)}: {', '.join(duplicates)}")

    assert not offenders, "duplicate menu option id(s):\n" + "\n".join(offenders[:50])


def test_event_menu_visible_text_has_no_embarassing_typo() -> None:
    offenders = []
    for path in sorted((ROOT / "src" / "menus" / "events").rglob("*.py")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        stale_tokens = (
            "embarassing",
            "catched",
            "guilties",
            "enlightnment",
            "This can't be",
            "Pacta sunt servanda",
            "As if I care",
            "deserted :",
            "magnificency",
            "fulminatng",
            "assasinated",
            "of an indigestion",
            "M'lord",
            "amongst",
            "=1500=",
            "Beatus qui",
            "Release the hounds",
            "nanny for God's sake",
            "accidentaly",
            "suspenders",
            "oldest job",
            "opposite rumors",
            "house and properties",
            "Old Golds",
            "supersticion",
            "bannish",
            "alwo",
            "A majesty don't",
            "will probably don't",
            "exactions",
            "How embarrassing",
            "Embarrassing",
            "Your kingdom",
            "whole kingdom",
            "vine and beer",
            "calradian subject",
            "disciples request",
            "professionnal",
            "sermon your men",
            "not good enough I guess",
        )
        if any(token in raw for token in stale_tokens):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert not offenders, "stale visible event text remains in: " + ", ".join(offenders[:50])


def test_random_owned_center_events_require_valid_target_center() -> None:
    for rel_path in (
        "src/menus/events/choice_06_1.py",
        "src/menus/events/choice_07_1.py",
        "src/menus/events/choice_08_1.py",
        "src/menus/events/choice_09_1.py",
        "src/menus/events/choice_10_1.py",
        "src/menus/events/choice_12_1.py",
        "src/menus/events/choice_13_1.py",
        "src/menus/events/choice_14_1.py",
        "src/menus/events/choice_16_1.py",
    ):
        raw = (ROOT / rel_path).read_text(encoding="utf-8", errors="replace")
        assert '(assign, "$temp", -1)' in raw, rel_path
        assert '(str_store_string, s68, "@one of your fiefs")' in raw, rel_path
        assert "(str_store_string_reg, s1, s68)" in raw, rel_path
        assert "(neg|is_between, \"$temp\", centers_begin, centers_end)" in raw, rel_path
        assert '(is_between, "$temp", centers_begin, centers_end)' in raw, rel_path


def test_global_population_boom_does_not_use_stale_random_center() -> None:
    raw = (ROOT / "src/menus/events/choice_17_1.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert "$temp" not in raw
    assert "store_random_party_in_range" not in raw
    assert raw.count('(val_add, "$g_sod_global_health", 1)') == 1
    assert "(gt, \":affected_count\", 0)" in raw


def test_realm_wide_harvest_and_pandemic_count_affected_fiefs() -> None:
    harvest = (ROOT / "src/menus/events/choice_11_1.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert '(assign, ":affected_count", 0)' in harvest
    assert '(val_add, ":affected_count", 1)' in harvest
    assert "(gt, \":affected_count\", 0)" in harvest
    assert "No affected fief could be found" in harvest

    pandemic = (ROOT / "src/menus/events/choice_15_1.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert pandemic.count('(assign, ":affected_count", 0)') == 2
    assert pandemic.count('(val_add, ":affected_count", 1)') == 2
    assert pandemic.count('(val_sub, "$g_sod_global_health", 2)') == 1
    assert "No affected fief could be found" in pandemic


def test_holy_ascension_choice_stays_visible_and_reports_failures() -> None:
    raw = (ROOT / "src/menus/events/choice_event_holy_1.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert '("choice_event_holy_1", [],' in raw
    assert "(store_troop_gold, \":gold\", \"trp_player\")" in raw
    assert raw.count('(party_count_members_of_type, ":noble_count", "p_main_party", "$g_sod_last_noble")') >= 2
    assert '(gt, ":noble_count", 0)' in raw
    assert "(call_script, \"script_sod_troop_get_effective_faith\")" in raw
    assert "don't have enough gold to sponsor the ascension" in raw
    assert "lacks the faith needed for such an ascension" in raw
    assert "noble veteran is no longer with your party" in raw


def test_event_menus_do_not_repeat_identical_global_faith_clamps() -> None:
    duplicate_locations: list[str] = []
    clamp = '(val_clamp, "$g_sod_global_faith", -2000, 2001),'
    for path in sorted((ROOT / "src" / "menus" / "events").rglob("*.py")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        previous_was_clamp = False
        for line_no, line in enumerate(lines, start=1):
            current_is_clamp = line.strip() == clamp
            if current_is_clamp and previous_was_clamp:
                duplicate_locations.append(f"{path.relative_to(ROOT).as_posix()}:{line_no}")
            previous_was_clamp = current_is_clamp

    assert not duplicate_locations, (
        "duplicate adjacent global faith clamp(s):\n" + "\n".join(duplicate_locations)
    )


def test_deserter_event_removes_troops_only_after_player_response() -> None:
    raw = (ROOT / "src" / "menus" / "events" / "choice_22_1.py").read_text(
        encoding="utf-8", errors="replace"
    )
    menu_setup, options = raw.split("    ],\n    [", 1)
    removal = '(party_remove_members, "p_main_party", reg2, reg3)'
    assert removal not in menu_setup
    assert options.count(removal) == 3


def test_investment_report_pays_only_after_player_collects() -> None:
    raw = (ROOT / "src" / "menus" / "events" / "choice_investment_report.py").read_text(
        encoding="utf-8", errors="replace"
    )
    menu_setup, options = raw.split("    ],\n    [", 1)
    payout = '(troop_add_gold, "trp_player", "$g_sod_invested_gold")'
    assert payout not in menu_setup
    assert options.count(payout) == 1
    assert "Collect {reg6} denars and leave." in options


def test_quest_journal_report_uses_caret_breaks_not_literal_newlines() -> None:
    raw = (ROOT / "src" / "menus" / "reports" / "quest_journal_report.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert "Quest Journal^^[Active Log and Companion Arcs]" in raw
    assert "\\n" not in raw


def test_new_economy_reports_use_high_string_scratch_and_validate_centers() -> None:
    for rel_path in (
        "src/menus/economy/town_market_report.py",
        "src/menus/economy/regional_economy_flow_report.py",
        "src/menus/economy/castle_support_report.py",
    ):
        raw = (ROOT / rel_path).read_text(encoding="utf-8", errors="replace")
        assert not re.search(r"\bs(?:[0-9]|1[0-9])\b", raw), rel_path
        assert "(str_store_party_name, s68," in raw, rel_path
        assert "(str_store_string_reg, s97, s98)" in raw, rel_path

    regional = (ROOT / "src/menus/economy/regional_economy_flow_report.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assign_center = '(assign, ":cur_center", reg0)'
    validate_center = '(is_between, ":cur_center", centers_begin, centers_end)'
    count_center = '(val_add, ":center_count", 1)'
    assert assign_center in regional
    assert validate_center in regional
    assert count_center in regional
    assert regional.index(assign_center) < regional.index(validate_center) < regional.index(count_center)


def test_night_bandit_result_screens_are_idempotent() -> None:
    failed = (ROOT / "src/menus/other/continue_28.py").read_text(
        encoding="utf-8", errors="replace"
    )
    succeeded = (ROOT / "src/menus/other/continue_29.py").read_text(
        encoding="utf-8", errors="replace"
    )

    assert "assasins" not in failed
    assert '(party_slot_eq, "$current_town", slot_center_has_bandits, 1)' in failed
    assert failed.index('(party_slot_eq, "$current_town", slot_center_has_bandits, 1)') < failed.index(
        '(call_script, "script_sod_player_charge_gold", ":gold_loss")'
    )
    assert failed.index('(call_script, "script_sod_player_charge_gold", ":gold_loss")') < failed.index(
        '(party_set_slot, "$current_town", slot_center_has_bandits, 0)'
    )

    assert '(party_slot_eq, "$current_town", slot_center_has_bandits, 1)' in succeeded
    assert succeeded.index('(party_slot_eq, "$current_town", slot_center_has_bandits, 1)') < succeeded.index(
        '(call_script, "script_troop_add_gold", "trp_player", ":gold_reward")'
    )
    assert succeeded.index('(party_set_slot, "$current_town", slot_center_has_bandits, 0)') < succeeded.index(
        '(call_script, "script_troop_add_gold", "trp_player", ":gold_reward")'
    )


def test_wilderness_captivity_validates_encounter_and_capturer_parties() -> None:
    raw = (ROOT / "src/menus/other/continue_48.py").read_text(
        encoding="utf-8", errors="replace"
    )

    assert '(assign, ":victorious_faction", "fac_commoners")' in raw
    assert '(party_is_active, "$g_encountered_party")' in raw
    assert '(party_is_active, "$capturer_party")' in raw
    assert raw.index('(party_is_active, "$g_encountered_party")') < raw.index(
        '(store_faction_of_party, ":victorious_faction", "$g_encountered_party")'
    )
    assert raw.index('(party_is_active, "$capturer_party")') < raw.index(
        '(store_faction_of_party, ":victorious_faction", "$capturer_party")'
    )
    assert raw.index('(party_is_active, "$capturer_party")') < raw.index(
        '(set_camera_follow_party, "$capturer_party")'
    )


def test_tournament_victory_rewards_are_idempotent() -> None:
    raw = (ROOT / "src/menus/other/continue_35.py").read_text(
        encoding="utf-8", errors="replace"
    )
    reward_guard = '(eq, "$g_tournament_player_team_won", 1)'
    assert reward_guard in raw
    for token in (
        '(call_script, "script_change_troop_renown", "trp_player", 20)',
        '(add_xp_to_troop, 250, "trp_player")',
        '(troop_add_gold, "trp_player", reg9)',
        '(troop_add_gold, "trp_player", ":total_win")',
        '(party_set_slot, "$current_town", slot_town_player_odds, ":player_odds")',
    ):
        assert token in raw
        assert raw.index(reward_guard) < raw.index(token)
    for token in (
        '(assign, "$g_tournament_bet_placed", 0)',
        '(assign, "$g_tournament_bet_win_amount", 0)',
        '(assign, "$tournament_high_bet", 0)',
        '(assign, "$g_tournament_player_team_won", 2)',
    ):
        assert token in raw
        assert raw.index('(troop_add_gold, "trp_player", ":total_win")') < raw.index(token)


def test_tournament_non_player_winner_renown_is_idempotent() -> None:
    raw = (ROOT / "src/menus/other/continue_36.py").read_text(
        encoding="utf-8", errors="replace"
    )
    guard = '(neq, "$g_tournament_player_team_won", 2)'
    renown = '(call_script, "script_change_troop_renown", ":winner_troop", 20)'
    consume = '(assign, "$g_tournament_player_team_won", 2)'
    assert guard in raw
    assert renown in raw
    assert consume in raw
    assert raw.index(guard) < raw.index(renown) < raw.index(consume)


def test_village_loot_completion_consumes_raid_complete_once() -> None:
    village_menu = (ROOT / "src/menus/centers/village/recruit_volunteers.py").read_text(
        encoding="utf-8", errors="replace"
    )
    result = (ROOT / "src/menus/other/continue_31.py").read_text(
        encoding="utf-8", errors="replace"
    )

    raid_complete_block = village_menu[village_menu.index('(eq, "$g_player_raid_complete", 1)'):]
    raid_complete_block = raid_complete_block[: raid_complete_block.index('(else_try),')]
    assert '(assign, "$g_player_raid_complete", 0)' not in raid_complete_block
    assert '(jump_to_menu, "mnu_village_loot_complete")' in raid_complete_block

    assert '(assign, reg1, 0)' in result
    assert '(eq, "$g_player_raid_complete", 1)' in result
    assert result.index('(eq, "$g_player_raid_complete", 1)') < result.index(
        '(call_script, "script_troop_add_gold", "trp_player", reg1)'
    )
    assert result.index('(call_script, "script_troop_add_gold", "trp_player", reg1)') < result.index(
        '(assign, "$g_player_raid_complete", 2)'
    )
    assert result.index('(eq, "$g_player_raid_complete", 2)') < result.index(
        '(call_script, "script_sod_center_apply_cattle_delta", "$current_town", ":cattle_delta")'
    )
    assert result.index('(call_script, "script_sod_center_apply_cattle_delta", "$current_town", ":cattle_delta")') < result.index(
        '(assign, "$g_player_raid_complete", 0)'
    )


def test_steal_cattle_result_consumes_attempt_once() -> None:
    raw = (ROOT / "src/menus/other/continue_30.py").read_text(
        encoding="utf-8", errors="replace"
    )
    guard = '(party_slot_eq, "$current_town", slot_village_player_can_not_steal_cattle, 0)'
    consume = '(party_set_slot, "$current_town", slot_village_player_can_not_steal_cattle, 1)'
    cattle_delta = '(call_script, "script_sod_center_apply_cattle_delta", "$current_town", ":cattle_delta")'
    center_relation = '(call_script, "script_change_player_relation_with_center", "$current_town", -5)'
    herd = '(call_script, "script_create_cattle_herd", "$current_town", ":actual_stolen")'

    assert guard in raw
    assert consume in raw
    assert "There are no more loose animals to drive off today." in raw
    for token in (consume, cattle_delta, center_relation, herd):
        assert token in raw
        assert raw.index(guard) < raw.index(token)
    assert raw.index(consume) < raw.index(cattle_delta)


def test_collect_taxes_completion_only_succeeds_active_unsucceeded_quest_once() -> None:
    raw = (ROOT / "src/menus/other/continue_37.py").read_text(
        encoding="utf-8", errors="replace"
    )
    active = '(check_quest_active, "qst_collect_taxes")'
    unsucceeded = '(neg|check_quest_succeeded, "qst_collect_taxes")'
    relation = '(call_script, "script_change_player_relation_with_center", "$current_town", -2)'
    succeed = '(call_script, "script_succeed_quest", "qst_collect_taxes")'

    for token in (active, unsucceeded, relation, succeed):
        assert token in raw
    assert raw.index(active) < raw.index(unsucceeded) < raw.index(relation)
    assert raw.index(unsucceeded) < raw.index(succeed)


def test_follow_army_failure_only_penalizes_active_quest_once() -> None:
    raw = (ROOT / "src/menus/other/continue_57.py").read_text(
        encoding="utf-8", errors="replace"
    )
    active = '(check_quest_active, "qst_follow_army")'
    abort = '(call_script, "script_abort_quest", "qst_follow_army", 1)'
    relation = '(call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3)'

    for token in (active, abort, relation):
        assert token in raw
    assert raw.index(active) < raw.index(abort) < raw.index(relation)


def test_collect_taxes_failure_only_fails_active_unfailed_quest_once() -> None:
    raw = (ROOT / "src/menus/other/continue_39.py").read_text(
        encoding="utf-8", errors="replace"
    )
    active = '(check_quest_active, "qst_collect_taxes")'
    unfailed = '(neg|check_quest_failed, "qst_collect_taxes")'
    fail = '(call_script, "script_fail_quest", "qst_collect_taxes")'
    state = '(quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 4)'

    for token in (active, unfailed, fail, state):
        assert token in raw
    assert raw.index(active) < raw.index(unfailed) < raw.index(fail) < raw.index(state)


def test_train_peasants_result_only_applies_terminal_quest_state_once() -> None:
    raw = (ROOT / "src/menus/other/continue_42.py").read_text(
        encoding="utf-8", errors="replace"
    )
    active = '(check_quest_active, "qst_train_peasants_against_bandits")'
    unsucceeded = '(neg|check_quest_succeeded, "qst_train_peasants_against_bandits")'
    succeed = '(call_script, "script_succeed_quest", "qst_train_peasants_against_bandits")'
    unfailed = '(neg|check_quest_failed, "qst_train_peasants_against_bandits")'
    fail = '(call_script, "script_fail_quest", "qst_train_peasants_against_bandits")'
    failed = '(check_quest_failed, "qst_train_peasants_against_bandits")'
    loot = '(call_script, "script_village_set_state", "$current_town", svs_looted)'

    for token in (active, unsucceeded, succeed, unfailed, fail, failed, loot):
        assert token in raw
    assert raw.index(active) < raw.index(unsucceeded) < raw.index(succeed)
    assert raw.index(unfailed) < raw.index(fail)
    assert raw.index(failed) < raw.index(loot)


def test_train_peasants_training_result_consumes_pending_training_once() -> None:
    raw = (ROOT / "src/menus/other/continue_41.py").read_text(
        encoding="utf-8", errors="replace"
    )
    inactive_guard = '(this_or_next|neg|check_quest_active, "qst_train_peasants_against_bandits")'
    active_continue = '(check_quest_active, "qst_train_peasants_against_bandits")'
    pending = '(neq, "$qst_train_peasants_against_bandits_currently_training", 1)'
    cap = '(val_min, ":quest_current_state", ":quest_target_amount")'
    progress = '(quest_set_slot, "qst_train_peasants_against_bandits", slot_quest_current_state, ":quest_current_state")'
    consume = '(assign, "$qst_train_peasants_against_bandits_currently_training", 0)'
    clear_count = '(assign, "$g_train_peasants_against_bandits_num_peasants", 0)'
    stale = "no active village training order"

    for token in (inactive_guard, active_continue, pending, cap, progress, consume, clear_count, stale):
        assert token in raw
    assert raw.index(inactive_guard) < raw.index(progress)
    assert raw.index(pending) < raw.index(progress)
    assert raw.index(cap) < raw.index(progress) < raw.index(consume) < raw.index(clear_count)
    assert raw.index(active_continue) > raw.index(consume)


def test_train_peasants_ready_menu_does_not_write_volatile_s0() -> None:
    raw = (ROOT / "src/menus/start_game/peasant_start_practice.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert '(str_store_troop_name_by_count, s68, "trp_trainee_peasant", ":random_number")' in raw
    assert "str_store_troop_name_by_count, s0" not in raw
