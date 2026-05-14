# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_before(raw: str, first: str, second: str) -> None:
    assert first in raw, f"missing token: {first}"
    assert second in raw, f"missing token: {second}"
    assert raw.index(first) < raw.index(second), f"{first} should appear before {second}"


def iter_source_files(root: str) -> list[Path]:
    return [
        path
        for path in (ROOT / root).rglob("*.py")
        if "__pycache__" not in path.parts
    ]


def test_quest_terminal_sentinel_loads_last() -> None:
    order_lines = [
        line.strip()
        for line in read("src/quests/_order_quests.txt").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert order_lines[-1] == "9999_quests_end.py"

    sentinel = read("src/quests/9999_quests_end.py")
    assert_contains(sentinel, '"quests_end"')
    assert_contains(sentinel, '"sentinel": True')
    assert_contains(sentinel, "quest_terminal_sentinel")

    for fragment in (ROOT / "src" / "quests").glob("*.py"):
        if fragment.name == "9999_quests_end.py":
            continue
        raw = fragment.read_text(encoding="utf-8", errors="replace")
        assert 'quest_template_spec(\n    "quests_end"' not in raw, (
            f"quests_end definition must stay in 9999_quests_end.py, found in {fragment}"
        )


def test_quest_journal_archive_entries_are_not_duplicated() -> None:
    raw = read("src/scripts/ZG_quests/sod_quest_journal_describe_to_s2.py")
    assert_contains(raw, "if include_archive_day:")
    assert_contains(raw, "else:")
    assert raw.count('(str_store_string, s0, "@        Stage {reg0} | Chain {reg1} | State {reg2}"),') == 1
    assert raw.count('(str_store_string, s0, "@        Stage {reg0} | Chain {reg1} | State {reg2} | Archived day {reg3}"),') == 1


def test_quest_journal_surfaces_companion_personal_arcs() -> None:
    journal = read("src/scripts/ZG_quests/sod_quest_journal_describe_to_s2.py")
    menu = read("src/menus/reports/quest_journal_report.py")
    for token in (
        "Companion Personal Arcs",
        "[COMPANION] personal arc",
        "Borcha is ready to speak of old horde roads",
        "Marnid records profit made stable enough to trust",
        "Ymira records mercy protected under command",
        "Rolf records the grand claim preserved at the cost of belief",
        "Baheshtur records loyalty chosen freely",
        "Firentis records service turned toward restitution",
        "Deshavi records survivors hidden before the trail went cold",
        "Matheld records courage kept sharp and disciplined",
        "Alayen records duty placed before display",
        "Bunduk records soldiers defended by command instead of spent by it",
        "Katrin records the camp fed before speeches were made",
        "Jeremus records healing protected even under battlefield pressure",
        "Nizar records a charge dramatic enough to remember",
        "Lezalit records order strengthened without chains",
        "Artimenner records a design trusted before disaster",
        "Klethi records a choice kept in her own hands",
        "qst_companion_ymira_mercy_under_arms",
        "qst_companion_lezalit_discipline_without_chains",
        "qst_companion_klethi_knife_with_name",
    ):
        assert_contains(journal, token)
    assert_contains(menu, "Active Log and Companion Arcs")
    assert_contains(menu, "companion personal arcs")


def test_legacy_jester_and_formation_bugfixes() -> None:
    formations = read("src/mission_templates/_preamble/00_imports.py")
    formations_j = formations[formations.index("formations_j =") : formations.index("# K - wedge")]
    assert_contains(formations_j, "(key_clicked, key_j)")
    assert_contains(formations_j, "(neg|key_is_down, key_left_control)")
    assert_contains(formations_j, "(neg|key_is_down, key_right_control)")

    player_lead = read("src/dialogs/ZA02_sod_court_and_strategy/anyone_plyr_jester_skirmish4.py")
    jester_lead = read("src/dialogs/ZA02_sod_court_and_strategy/anyone_plyr_jester_skirmish4_02.py")
    assert '[(assign,' not in player_lead
    assert '[(assign,' not in jester_lead
    assert_contains(player_lead, '"I will lead an army myself.", "marshal_skirmish",[')
    assert_contains(player_lead, '(assign, "$sod_skirmish_playertroop", "trp_player")')
    assert_contains(jester_lead, '"I want you to lead an army.", "marshal_skirmish",[')
    assert_contains(jester_lead, '(assign, "$sod_skirmish_playertroop", "trp_sod_jester")')

    for path in (
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_jester_plyr_jester_cheat1.py",
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_jester_plyr_jester_cheatt1.py",
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_jester_plyr_jester_cheatc1_10.py",
    ):
        raw = read(path)
        assert_contains(raw, '"That trick is enough for now.", "close_window"')

    order = read("src/dialogs/_order_dialogs.txt")
    assert order.index("trp_sod_jester_plyr_jester_cheatc1_10.py") < order.index(
        "trp_sod_jester_jester_skirmish1.py"
    )

    for path in (
        "src/scripts/ZZ_common_array_processing/enter_court.py",
        "src/menus/kingdom/talk_council_marshal.py",
        "src/menus/kingdom/talk_council_rep_0.py",
    ):
        raw = read(path)
        assert_contains(raw, '(this_or_next|eq, "$cheat_mode", 1)')
        assert_contains(raw, '(eq, "$g_sod_cheat_mode", 1)')
        assert_contains(raw, '(set_visitor, 16, "trp_sod_jester")')
        assert_contains(raw, '(set_passage_menu, "mnu_town_castle_passages")')

    castle_menu = read("src/menus/centers/castle/castle_castle.py")
    passage_script = read("src/scripts/ZZ_common_array_processing/enter_town_center_from_passage.py")
    assert castle_menu.index('"join_tournament"') < castle_menu.index('"town_castle"')
    assert castle_menu.index('"town_castle"') < castle_menu.index('"review_regional_threats"')
    assert_contains(castle_menu, '"town_castle_passages"')
    assert_contains(castle_menu, "preserve SoD's visible door labels")
    assert_contains(castle_menu, '"castle_passage_dungeon_8"')
    assert_contains(castle_menu, '(call_script, "script_enter_town_center_from_passage")')
    assert_contains(castle_menu, '"Leave Area."')
    assert_contains(castle_menu, '"Door to the dungeon."')
    assert_contains(castle_menu, '(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")')
    passage_block = castle_menu[castle_menu.index('"town_castle_passages"'):]
    assert '(jump_to_menu, "mnu_town")' not in passage_block
    assert_contains(passage_script, '"enter_town_center_from_passage"')
    assert_contains(passage_script, '(party_slot_eq, "$current_town", slot_party_type, spt_castle)')
    assert_contains(passage_script, '(set_jump_mission, "mt_castle_visit")')
    assert_contains(passage_script, '(jump_to_scene, ":castle_exterior")')
    assert_contains(passage_script, '(set_jump_mission, "mt_town_center")')
    assert_contains(passage_script, '(jump_to_scene, ":town_scene")')

    for path in (
        "src/dialogs/ZA01_startup_and_dispatch/trp_sod_jester_start.py",
        "src/dialogs/ZA01_startup_and_dispatch/trp_sod_jester_start_02.py",
        "src/dialogs/ZA01_startup_and_dispatch/trp_sod_jester_start_03.py",
    ):
        raw = read(path)
        assert_contains(raw, '(this_or_next|eq, "$cheat_mode", 1)')
        assert_contains(raw, '(eq, "$g_sod_cheat_mode", 1)')

    disabled = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_jester_start_disabled.py")
    assert_contains(disabled, '(neq, "$cheat_mode", 1)')
    assert_contains(disabled, '(neq, "$g_sod_cheat_mode", 1)')
    assert_contains(disabled, "The bells on my cap are tied off")

    order = read("src/dialogs/_order_dialogs.txt")
    assert order.index("trp_sod_jester_start_03.py") < order.index("trp_sod_jester_start_disabled.py")
    assert order.index("trp_sod_jester_start_disabled.py") < order.index("trp_sod_jester_jester_else.py")


def test_legacy_honor_duel_and_jotnar_quest_bugfixes() -> None:
    duel = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_challenge_duel_for_lady_3.py")
    assert_contains(duel, '(set_jump_mission, "mt_arena_challenge_fight")')
    assert_contains(duel, '(jump_to_scene, ":arena_scene")')
    assert_contains(duel, '(jump_to_menu, "mnu_arena_duel_fight")')
    assert '(neq, "$talk_context", tc_court_talk)' not in duel

    village = read("src/menus/centers/village/recruit_volunteers.py")
    black_army_branch = village[village.index('(check_quest_active, "qst_black_army_aid_warband")'):]
    black_army_branch = black_army_branch[:black_army_branch.index('(check_quest_active, "qst_jotnar_clan_revenge")')]
    assert_contains(black_army_branch, '(val_min, ":plyr_lvl", 80)')
    assert_contains(black_army_branch, '(val_min, ":p_size", 80)')
    assert_contains(black_army_branch, '(val_max, ":p_size", ":plyr_lvl")')
    assert_contains(black_army_branch, '(val_add, ":p_size", 1)')
    assert_contains(black_army_branch, '(store_random_in_range, ":rand", ":plyr_lvl", ":p_size")')
    assert_contains(black_army_branch, '(val_min, reg8, 80)')

    jotnar_branch = village[village.index('(check_quest_active, "qst_jotnar_clan_revenge")'):]
    jotnar_branch = jotnar_branch[:jotnar_branch.index('(else_try),')]
    assert_contains(jotnar_branch, '(val_min, ":plyr_lvl", 80)')
    assert_contains(jotnar_branch, '(val_min, ":p_size", 80)')
    assert_contains(jotnar_branch, '(val_max, ":p_size", ":plyr_lvl")')
    assert_contains(jotnar_branch, '(val_add, ":p_size", 1)')
    assert_contains(jotnar_branch, '(store_random_in_range, ":rand", ":plyr_lvl", ":p_size")')

    guild_bandits = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_gm_troublesome_bandits_quest_brief.py")
    assert_contains(guild_bandits, '(val_min, ":plyr_lvl", 80)')
    assert_contains(guild_bandits, '(val_min, ":p_size", 80)')
    assert_contains(guild_bandits, '(val_max, ":p_size", ":plyr_lvl")')
    assert_contains(guild_bandits, '(val_add, ":p_size", 1)')
    assert_contains(guild_bandits, '(store_random_in_range, ":rand", ":plyr_lvl", ":p_size")')

    duel_mission = read("src/mission_templates/0039_arena_challenge_fight/arena_challenge_fight.py")
    assert_contains(duel_mission, '(call_script, "script_succeed_quest", "qst_duel_for_lady")')
    assert_before(duel_mission, '(jump_to_menu, "mnu_sod_continue_return")', "(finish_mission)")

    continue_menu = read("src/menus/other/sod_continue_return.py")
    assert_contains(continue_menu, "(change_screen_map)")
    assert "(change_screen_return)" not in continue_menu

    for path, target_menu in (
        ("src/mission_templates/0040_sod_arena_challenge_fight/sod_arena_challenge_fight.py", "mnu_sod_continue_return"),
        ("src/mission_templates/0041_sod_arena_duel_fight_honor/sod_arena_duel_fight_honor.py", "mnu_sod_continue_return"),
        ("src/mission_templates/0043_sod_arena_duel_fight/sod_arena_duel_fight.py", "mnu_sod_continue_return"),
        ("src/mission_templates/0042_jotnar_clan_arena/jotnar_clan_arena.py", "mnu_jotnar_clan_competition"),
    ):
        mission = read(path)
        assert_before(mission, f'(jump_to_menu, "{target_menu}")', "(finish_mission)")


def test_legacy_construction_and_conquered_court_bugfixes() -> None:
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    advance = construction[construction.index('("sod_advance_center_construction"'):]
    assert_contains(advance, '(gt, ":required", 0)')
    assert_contains(advance, '(ge, ":progress", ":required")')
    assert advance.index('(ge, ":progress", ":required")') < advance.index('(call_script, "script_sod_get_center_construction_workforce", ":center_no")')
    assert_contains(advance, '(call_script, "script_cf_sod_complete_center_construction", ":center_no")')

    center_transfer = read("src/scripts/ZD_centers/give_center_to_faction_aux.py")
    assert_contains(center_transfer, 'kingdom_ladies_begin')
    assert_contains(center_transfer, 'kingdom_ladies_end')
    assert_contains(center_transfer, '(troop_slot_eq, ":lady_no", slot_troop_cur_center, ":center_no")')
    assert_contains(center_transfer, '(neq, ":lady_faction", ":faction_no")')
    assert_contains(center_transfer, '(troop_set_slot, ":lady_no", slot_troop_cur_center, ":new_center")')
    assert_contains(center_transfer, 'slot_troop_spouse')
    assert_contains(center_transfer, 'slot_troop_father')


def test_legacy_message_feed_boar_toll_and_battle_count_bugfixes() -> None:
    message_guard = read("src/triggers/ST02_every_hour/entry_0164.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    assert_contains(message_guard, "set_show_messages")
    assert_contains(message_guard, "(set_show_messages, 1)")
    assert_contains(message_guard, "suppression leaks")
    assert_contains(trigger_order, "ST02_every_hour/entry_0164.py")

    boar_attack = read("src/dialogs/ZZ99_misc_dialogs/anyone_boar_clan_attack.py")
    assert_contains(boar_attack, '"boar_clan_attack"')
    assert_contains(boar_attack, "(encounter_attack)")

    debrief = read("src/menus/other/continue_05.py")
    assert_contains(debrief, "Enemy Casualties:{s9}")
    assert_contains(debrief, "Fit to continue: your side {reg10}, enemy side {reg11}.")


def test_legacy_enemy_reinforcement_auto_dismount_bugfix() -> None:
    formations = read("src/mission_templates/_preamble/00_imports.py")
    ai_dismount = formations[
        formations.index("formations_ai_dismount =") : formations.index("# stop moving units into formations")
    ]
    assert_contains(ai_dismount, "(team_give_order, reg0, grc_cavalry, mordr_mount)")
    assert "(team_give_order, reg0, grc_everyone, mordr_dismount)" not in ai_dismount


def test_legacy_diego_and_legion_dialogue_bugfixes() -> None:
    prison_break_mission = read("src/mission_templates/0024_prison_break/prison_break.py")
    assert_contains(prison_break_mission, '(assign, "$prison_break", 6)')
    assert_contains(prison_break_mission, '(call_script, "script_succeed_quest", "qst_slave_q3")')

    walkers = read("src/scripts/ZY_helper_scripts/init_mercenary_base_walkers.py")
    assert_contains(walkers, '(neq, "$prison_break", 5)')
    assert_contains(walkers, '(neq, "$prison_break", 6)')
    assert_contains(walkers, '(set_visitor, 20, "trp_slave_hero")')

    diego_start = read("src/dialogs/ZA01_startup_and_dispatch/trp_slave_hero_start.py")
    assert_contains(diego_start, '(eq, "$prison_break", 0)')
    assert_contains(diego_start, '(neg|check_quest_succeeded, "qst_slave_q3")')

    for path in (
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_capitalist_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_crusader_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_imperialist_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_liberator_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_nihilistic_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_racist_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_respectful_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_sane_6.py",
    ):
        assert_contains(read(path), "(encounter_attack)")


def test_legacy_party_encounter_invalid_party_bugfix() -> None:
    callback = read("src/scripts/ZA_hardcoded_game_scripts/game_event_party_encounter.py")
    assert_contains(callback, "invalid/reserved encounter ids")
    assert_contains(callback, '("game_event_party_encounter",')
    assert_contains(callback, '(store_script_param_1, "$g_encountered_party")')
    assert_contains(callback, '(gt, "$g_encountered_party", 0)')
    assert_contains(callback, '(party_is_active, "$g_encountered_party")')
    assert_contains(callback, '(jump_to_menu, "mnu_castle_outside")')
    assert_contains(callback, '(jump_to_menu, "mnu_village")')
    assert_contains(callback, '(jump_to_menu, "mnu_simple_encounter")')
    for token in (
        "start_map_conversation",
        "start_party_encounter",
    ):
        assert token not in callback


def test_legacy_party_size_helpers_reject_invalid_parties() -> None:
    attached = read("src/scripts/ZC_parties/get_troop_attached_party.py")
    assert_contains(attached, '(gt, ":party_no", 0)')
    assert_contains(attached, '(party_is_active, ":party_no")')
    assert_before(attached, '(party_is_active, ":party_no")', '(party_get_attached_to, ":attached_party_no", ":party_no")')

    count_fit = read("src/scripts/ZC_parties/party_count_fit_regulars.py")
    assert_contains(count_fit, '(assign, reg0, 0)')
    assert_contains(count_fit, '(gt, ":party", 0)')
    assert_contains(count_fit, '(party_is_active, ":party")')
    assert_before(count_fit, '(party_is_active, ":party")', '(party_get_num_companion_stacks, ":num_stacks", ":party")')

    ideal_size = read("src/scripts/ZC_parties/party_get_ideal_size.py")
    assert_contains(ideal_size, '(assign, ":faction_id", -1)')
    assert_contains(ideal_size, '(assign, ":party_leader", -1)')
    assert_contains(ideal_size, '(gt, ":party_no", 0)')
    assert_contains(ideal_size, '(party_is_active, ":party_no")')
    assert_before(ideal_size, '(party_is_active, ":party_no")', '(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party)')
    assert_contains(ideal_size, '(gt, ":faction_id", 0)')
    assert_contains(ideal_size, '(gt, ":party_leader", 0)')

    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    assert_contains(game_start, '(assign, ":lords_party", "$pout_party")')
    assert_contains(game_start, '(gt, ":lords_party", 0)')
    assert_contains(game_start, '(party_is_active, ":lords_party")')
    assert_before(game_start, '(party_is_active, ":lords_party")', '(party_attach_to_party, ":lords_party", ":center_no")')


def test_menu_fragments_are_not_empty_dead_ends() -> None:
    report = read("docs/reports/systems_tooling/menu_empty_fragment_audit.md")
    assert_contains(report, "# Empty Menu Fragment Audit")
    assert_contains(report, "No `src/menus` fragment has `MENUS = []`.")
    assert_contains(report, "Empty option menus are acceptable only when they are auto-routing menus.")

    routing_tokens = (
        "jump_to_menu",
        "change_screen_return",
        "change_screen_map",
        "change_screen_mission",
        "change_screen_map_conversation",
        "start_map_conversation",
        "leave_encounter",
    )
    generated_option_files = {
        "src/menus/camp/sod_upgrade_camp.py",
        "src/menus/other/sod_upgrade.py",
        "src/menus/other/sod_battle_commander_select.py",
    }
    offenders = []
    for path in iter_source_files("src/menus"):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if "/_preamble/" in rel or path.name.startswith("_"):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(raw, filename=rel)
        menu_values = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "MENUS":
                        menu_values.append(node.value)
        if not menu_values:
            offenders.append((rel, "missing MENUS assignment"))
            continue
        for menu_value in menu_values:
            if not isinstance(menu_value, ast.List):
                offenders.append((rel, "MENUS is not a list literal"))
                continue
            if not menu_value.elts:
                offenders.append((rel, "MENUS list is empty"))
                continue
            for menu in menu_value.elts:
                if not isinstance(menu, ast.Tuple) or len(menu.elts) < 6:
                    offenders.append((rel, "malformed menu tuple"))
                    continue
                menu_id = menu.elts[0].value if isinstance(menu.elts[0], ast.Constant) else "<nonliteral>"
                options = menu.elts[5]
                if isinstance(options, ast.List):
                    if not options.elts and not any(token in raw for token in routing_tokens):
                        offenders.append((rel, f"{menu_id}: empty options without routing op"))
                elif rel not in generated_option_files or not (
                    "generate_upgrade_options()" in raw
                    or "generate_sod_battle_commander_select_options()" in raw
                ):
                    offenders.append((rel, f"{menu_id}: nonliteral options without known generator"))
    assert not offenders, "empty or malformed menu fragments: " + repr(offenders[:30])


def test_legacy_unarmed_troop_prisoner_crash_bugfix() -> None:
    prisoner_sell = read("src/scripts/ZA_hardcoded_game_scripts/game_check_prisoner_can_be_sold.py")
    assert_contains(prisoner_sell, "(neg|troop_is_hero, \":troop_id\")")
    assert_contains(prisoner_sell, "(is_between, \":troop_id\", soldiers_begin, soldiers_end)")

    hourly_sanitizer = read("src/triggers/ST02_every_hour/entry_0163.py")
    assert_contains(hourly_sanitizer, '(call_script, "script_sod_sanitize_unique_hero_party_stacks")')

    for path in (
        "src/scripts/ZC_parties/party_prisoners_add_party_companions.py",
        "src/scripts/ZC_parties/party_prisoners_add_party_prisoners.py",
    ):
        raw = read(path)
        assert_contains(raw, "(is_between, \":stack_troop\", soldiers_begin, soldiers_end)")
        assert_contains(raw, "(party_add_prisoners, \":target_party\", \":stack_troop\", \":stack_size\")")

    camp_gate = read("src/menus/0000_hardcoded_mb1011/party_management.py")
    recruit_menu = read("src/menus/0000_hardcoded_mb1011/camp_recruit_prisoners.py")
    assert_contains(camp_gate, "(is_between, \":cur_troop_id\", soldiers_begin, soldiers_end)")
    assert recruit_menu.count("(is_between, \":cur_troop_id\", soldiers_begin, soldiers_end)") >= 3
    assert_contains(recruit_menu, "(party_add_members, \"p_main_party\", \"$g_prisoner_recruit_troop_id\", \"$g_prisoner_recruit_size\")")


def test_legacy_nearby_friend_strength_invalid_party_spam_bugfix() -> None:
    raw = read("src/scripts/ZC_parties/party_calculate_and_set_nearby_friend_strength.py")
    assert_contains(raw, "(le, \":party_no\", 0)")
    assert_contains(raw, "(neg|party_is_active, \":party_no\")")
    assert_contains(raw, "(val_max, \":num_enemy_factions\", 1)")
    assert_contains(raw, "(store_distance_to_party_from_party, \":distance\", \":party_no\", \":party_b\")")
    assert '(store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":party_b")' not in raw
    merc_block = raw[raw.index('(try_for_parties, ":party_b")'):]
    merc_block = merc_block[:merc_block.index('(party_set_slot, ":party_no", slot_party_follower_strength')]
    assert_contains(merc_block, "(party_is_active, \":party_b\")")
    assert_contains(merc_block, "(party_get_slot, \":str\", \":party_b\", slot_party_cached_strength)")


def test_legacy_neutral_town_siege_entry_bugfix() -> None:
    outside = read("src/menus/centers/common/approach_gates.py")
    town = read("src/menus/centers/castle/castle_castle.py")

    assert_contains(outside, "#MORDACHAI - allow sieges against what what a neutral or friendly faction")
    assert_contains(town, '"town_start_siege_from_inside"')
    assert_contains(town, "Neutral or friendly towns auto-enter this menu, unlike castles.")
    assert_contains(town, '(this_or_next|party_slot_eq, "$current_town", slot_center_is_besieged_by, -1)')
    assert_contains(town, '(neq, ":center_faction", "$players_kingdom")')
    assert_contains(town, '(jump_to_menu, "mnu_castle_siege_confirm")')
    assert_contains(town, '(assign, "$g_player_besiege_town", "$current_town")')
    assert_contains(town, '(call_script, "script_make_kingdom_hostile_to_player", ":center_faction", -10)')
    assert town.index('"town_start_siege_from_inside"') < town.index('"town_leave"')


def test_legacy_wilderness_camp_crash_guard() -> None:
    camp = read("src/menus/0000_hardcoded_mb1011/camp.py")
    camp_action = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    assert_contains(camp, "stale center or party ids")
    assert_contains(camp, '(gt, "$g_encountered_party", 0)')
    assert_contains(camp, '(neg|party_is_active, "$g_encountered_party")')
    assert_contains(camp, '(assign, "$g_encountered_party", -1)')
    assert_contains(camp, '(assign, "$g_encountered_party_2", -1)')
    assert_contains(camp, '(assign, "$current_town", -1)')
    assert_contains(camp_action, '("camp_strategy_advisor"')
    assert_contains(camp_action, '(main_party_has_troop, "trp_sod_strategy_advisor")')
    assert '(eq, "$g_sod_sa_in_court", 1)' not in camp_action


def test_legacy_mounted_lord_sidearms_bugfix() -> None:
    troops = read("compile/module_troops.py")
    for lord_id in (
        "reserved_knight_6",
        "reserved_knight_9",
        "reserved_knight_13",
        "reserved_knight_15",
    ):
        start = troops.index(f'["{lord_id}"')
        row = troops[start : troops.index("],", start) + 2]
        assert_contains(row, "itm_military_pick")

    aels = troops[troops.index('["reserved_knight_9"') : troops.index('["reserved_knight_10"')]
    assert_contains(aels, '"Aels"')
    assert_contains(aels, "itm_courser")
    assert_contains(aels, "itm_military_pick")
    assert_contains(aels, "itm_two_handed_battle_axe_2")


def test_legacy_ief_dying_centurion_dialogue_bugfix() -> None:
    death_narration = read("src/dialogs/ZZ99_misc_dialogs/anyone_cpdla_nihilistic_10.py")
    death_reply = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_2.py")
    mercy_refusal = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_4.py")
    confession_request = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_4_02.py")
    dialog_order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(death_reply, '"cpdla_nihilistic_2"')
    assert_contains(death_reply, '"close_window"')
    assert_contains(death_reply, 'script_kill_kingdom_hero')
    assert_contains(death_reply, 'script_sod_safe_leave_encounter')
    assert '"cpdla_nihilistic_3"' not in death_reply

    assert_contains(confession_request, '"cpdla_nihilistic_2"')
    assert_contains(confession_request, '"cpdla_nihilistic_3"')
    assert_contains(confession_request, '"cpdla_nihilistic_4"')
    assert_contains(confession_request, '"cpdla_nihilistic_5"')

    assert_contains(death_narration, '"cpdla_nihilistic_10"')
    assert_contains(death_narration, '"close_window"')
    assert_contains(death_narration, 'script_kill_kingdom_hero')
    assert_contains(death_narration, 'script_sod_safe_leave_encounter')
    assert '"cpdla_nihilistic_11"' not in death_narration
    assert "ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_11.py" not in dialog_order

    assert_contains(mercy_refusal, '"close_window"')
    assert_contains(mercy_refusal, 'script_kill_kingdom_hero')
    assert_contains(mercy_refusal, 'script_sod_safe_leave_encounter')


def test_legacy_gaius_marcus_lore_dialogue_bugfixes() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    about_self = read("src/dialogs/ZZ99_misc_dialogs/anyone_legate_sq_2_15.py")
    about_self_reply = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_legate_sq_2_16.py")
    imperialist_terminal = read("src/dialogs/ZA02_sod_court_and_strategy/anyone_cpsq_imperialist_13.py")
    captured_liberator = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_liberator_4.py")
    camp_nihilistic = read("src/dialogs/ZZ99_misc_dialogs/anyone_cp_nihilistic_5.py")
    camp_respectful = read("src/dialogs/ZZ99_misc_dialogs/anyone_cp_respectful_5.py")

    assert_contains(about_self, '"legate_sq_2_15"')
    assert_contains(about_self, '"legate_sq_2_16"')
    assert_contains(about_self_reply, '"legate_sq_2_16"')
    assert_contains(about_self_reply, '"legate_sq_2_17"')
    assert_contains(order, "ZZ99_misc_dialogs/anyone_plyr_legate_sq_2_16.py")
    assert "ZZ99_misc_dialogs/anyone_plyr_legate_sq_1_16.py" not in order

    assert_contains(imperialist_terminal, '"cpsq_imperialist_13"')
    assert_contains(imperialist_terminal, '"close_window"')
    assert_contains(imperialist_terminal, '(assign, "$g_leave_encounter", 1)')

    for source in (captured_liberator, camp_nihilistic, camp_respectful):
        assert_contains(source, "colleagues")
        assert "colleges" not in source


def test_legacy_relic_map_and_mercenary_lord_faction_cleanup_bugfixes() -> None:
    relics = read("src/presentations/0021_sod_royal_artifacts/sod_royal_artifacts.py")
    defeated_cleanup = read("src/triggers/ST03_daily/entry_0070.py")

    assert_contains(relics, "Jewel of the desert")
    assert "Jawel of the desert" not in relics

    assert_contains(defeated_cleanup, "spt_mercenary_lord_party")
    assert_contains(defeated_cleanup, "(party_stack_get_troop_id, \":merc_lord\", \":cur_party\", 0)")
    assert_contains(defeated_cleanup, "(troop_slot_eq, \":merc_lord\", slot_troop_occupation, slto_mercenary_lord)")
    assert_contains(defeated_cleanup, "(store_troop_faction, \":merc_guild\", \":merc_lord\")")
    assert_contains(defeated_cleanup, "(is_between, \":merc_guild\", guilds_begin, guilds_end)")
    assert_contains(defeated_cleanup, "(party_set_faction, \":cur_party\", \":merc_guild\")")
    assert_contains(defeated_cleanup, "(is_between, \":home_center\", centers_begin, centers_end)")


def test_legacy_antarian_javelinmen_have_multiwave_ammo() -> None:
    troops = read("compile/module_troops.py")

    javelinman = troops[troops.index('["sod_ant_javelinman"') : troops.index('["sod_ant_trained_javelinman"')]
    trained = troops[troops.index('["sod_ant_trained_javelinman"') : troops.index('["sod_ant_noble"')]

    assert javelinman.count("itm_jarid") >= 3
    assert trained.count("itm_ant_angon") >= 3


def test_legacy_formations_stale_scripted_order_bugfix() -> None:
    formations = read("src/mission_templates/_preamble/00_imports.py")
    formations_u = formations[formations.index("formations_u =") : formations.index("# stop moving ai units")]
    formations_0 = formations[formations.index("formations_0 =") : formations.index("# J - ranks")]

    assert_contains(formations_0, "(key_clicked, key_1)")
    assert_contains(formations_0, "(call_script, \"script_formation_end\")")
    assert_contains(formations_0, '(assign, "$infantryformationtype", 0)')
    assert_contains(formations_0, '(assign, "$archerformationtype", 0)')
    assert_contains(formations_0, '(assign, "$cavalryformationtype", 0)')
    assert '(call_script, "script_cf_formation")' not in formations_u

    for path in (
        "src/mission_templates/0005_bandits_at_night/bandits_at_night.py",
        "src/mission_templates/0010_lead_charge/lead_charge.py",
        "src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py",
        "src/mission_templates/0012_village_raid/village_raid.py",
        "src/mission_templates/0050_custom_battle/custom_battle.py",
    ):
        mission = read(path)
        assert mission.index("formations_0") < mission.index("formations_1")


def test_company_troop_dialogue_static_coverage_registered() -> None:
    raw = read("build/test_company_troop_dialogue_static.py")
    checklist = read("docs/company/COMPANY_TROOP_DIALOGUE_INCIDENTS_CHECKLIST.md")
    for token in (
        "test_company_troop_dialogue_static: OK",
        "sod_company_dialogue_schedule_spokesperson_incident",
        "sod_company_dialogue_process_faith_value_action",
        "sod_company_spokesperson_response_hazard_pay",
        "sod_company_spokesperson_response_victory_feast",
    ):
        assert_contains(raw, token)
    assert_contains(checklist, "- [x] Assert tests are referenced by broad feature audit if desired.")


def test_faction_campaign_director_static_coverage_registered() -> None:
    raw = read("build/test_faction_campaign_director_static.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    for token in (
        "test_faction_campaign_director_static: OK",
        "sod_faction_update_campaign_posture",
        "sod_faction_apply_posture_to_ai_thresholds",
        "sod_faction_apply_posture_to_lord_chances",
        "sod_faction_apply_posture_to_follow_chance",
        "test_raiding_posture_uses_marshal_style_and_target_value",
        "test_border_and_recovery_postures_improve_local_supply",
    ):
        assert_contains(raw, token)
    checklist_path = ROOT / "docs/reports/faction_campaign_director_marshal_planning_checklist.md"
    if checklist_path.exists():
        checklist = checklist_path.read_text(encoding="utf-8", errors="replace")
        for token in (
            "Faction Campaign Director and Marshal Planning Checklist",
            "- [x] Add `script_sod_faction_apply_posture_to_ai_thresholds`.",
            "- [x] Add `script_sod_faction_apply_posture_to_lord_chances`.",
            "- [x] Add `script_sod_faction_apply_posture_to_follow_chance`.",
        ):
            assert_contains(checklist, token)
    assert_contains(helper, "Campaign director")
    assert_contains(helper, "Followers {reg50}/{reg51}")
    assert_contains(notes, "script_sod_faction_describe_campaign_posture_to_s31")


def test_tax_courier_static_coverage_registered() -> None:
    raw = read("build/test_tax_courier_static.py")
    checklist = read("docs/reports/campaign_strategy/tax_courier_messenger_design.md")
    for token in (
        "test_tax_courier_static: OK",
        "test_tax_courier_constants_and_slots_exist",
        "test_processing_handles_delivery_expiry_and_loss_cleanup",
        "test_interception_dialog_and_battle_hooks_are_wired",
        "test_nonhostile_courier_coercion_has_reputation_consequences",
        "script_sod_tax_courier_resolve_defeated_by_party",
    ):
        assert_contains(raw, token)
    assert_contains(checklist, "- [x] Add or update a static validation test.")


def test_captivity_uses_systemic_outcome_inputs() -> None:
    wilderness = read("src/menus/captivity/captivity_wilderness_check.py")
    castle = read("src/menus/captivity/captivity_castle_check.py")
    ransom = read("src/menus/captivity/captivity_end_ransom_accept.py")
    for raw in (wilderness, castle):
        assert_contains(raw, "store_character_level")
        assert_contains(raw, "slot_troop_renown")
        assert_contains(raw, "$player_honor")
        assert_contains(raw, ":ransom_chance")
        assert_contains(raw, ":exchange_chance")
    assert_contains(wilderness, "fac_sod_merc_guild6")
    assert_contains(ransom, "(le, \"$player_ransom_amount\", 0)")
    assert_contains(ransom, "(assign, \"$player_ransom_amount\", 0)")


def test_invasion_arrival_and_report_surfaces_exist() -> None:
    arrival = read("src/menus/other/invaders_arrived.py")
    report = read("src/menus/reports/invasion_status_report.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    constants = read("src/constants/module_constants.py")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py") + read("src/menus/reports/report_submenus.py")
    order = read("src/menus/_order_game_menus.txt")
    for token in (
        "slot_faction_imperial_expedition_pressure",
        "slot_faction_imperial_expedition_supply",
        "slot_faction_imperial_expedition_front",
        "slot_faction_imperial_expedition_sabotage_until",
        "sod_imperial_expedition_action_delay_invasion",
    ):
        assert_contains(constants, token)
    assert_contains(arrival, "Review the invasion status")
    assert_contains(arrival, "slot_faction_num_armies")
    assert_contains(arrival, "script_sod_imperial_expedition_describe_status_to_s28")
    assert_contains(report, "Imperial Invasion Status")
    assert_contains(report, "slot_faction_current_power")
    assert_contains(report, "$g_sod_invasion_begin")
    assert_contains(report, "$g_sod_imperial_delay_total")
    assert_contains(report, "$g_sod_imperial_last_delay_day")
    assert_contains(report, "delay_imperial_invasion")
    assert_contains(report, "counter-intelligence")
    assert_contains(report, "Anti-Legion coalition")
    assert_contains(report, "Friendly realms")
    assert_contains(report, "Trusted mini-factions")
    assert_contains(report, "delay_imperial_invasion_needs_allies")
    assert_contains(report, "build an anti-Legion coalition first")
    assert_contains(report, "delay_imperial_invasion_no_gold")
    assert_contains(report, "sabotage_imperial_supply")
    assert_contains(report, "sod_imperial_expedition_action_sabotage_supply")
    assert_contains(report, "sod_imperial_expedition_action_delay_invasion")
    assert_contains(scripts, "sod_imperial_expedition_process_campaign")
    assert_contains(scripts, "sod_imperial_expedition_calculate_anti_legion_coalition")
    assert_contains(scripts, ":realm_allies")
    assert_contains(scripts, ":mini_faction_allies")
    assert_contains(scripts, ":coalition_score")
    assert_contains(scripts, "ge, \":coalition_score\", 30")
    assert_contains(scripts, "store_div, \":coalition_bonus\", \":coalition_score\", 20")
    assert_contains(scripts, 'val_add, "$g_sod_invasion_begin"')
    assert_contains(scripts, "$g_sod_imperial_delay_total")
    assert_contains(scripts, "Expeditionary doctrine")
    assert_contains(scripts, "accepts no outside mercenary pacts")
    assert_contains(scripts, "Bastard Brothers and Sons of Deer auxiliaries")
    assert_contains(scripts, "script_diplomacy_start_war_between_kingdoms")
    assert_contains(scripts, "living Centurions")
    assert_contains(read("src/triggers/ST03_daily/entry_0158.py"), "script_sod_imperial_expedition_process_campaign")
    assert_contains(read("src/triggers/ST03_daily/entry_0088.py"), "pt_legion_mercenaries")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    assert_contains(game_start, "$g_sod_imperial_delay_total")
    assert_contains(game_start, "$g_sod_imperial_last_delay_day")
    assert_contains(read("src/scripts/ZI_campaign_ai/ai_hire_mercenaries.py"), "script_sod_merc_market_weekly_pulse")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_merc_market_weekly_pulse.py"), '(neq, ":kingdom_faction", "fac_kingdom_6")')
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py"), '(neq, ":kingdom_faction", "fac_kingdom_6")')
    assert_contains(read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_plyr_chancellor_peace_2_06.py"), "(eq, 0, 1)")
    assert_contains(reports_menu, "mnu_invasion_status_report")
    assert_contains(order, "reports/invasion_status_report.py")


def test_only_imperial_heroes_can_die_in_battle() -> None:
    raw = read("src/scripts/ZE_encounters/cf_check_hero_can_die_in_battle.py")
    assert_contains(raw, '(eq, ":faction", "fac_kingdom_6")')
    assert_contains(raw, '":living_imperial_vassals"')
    assert_contains(raw, '(eq, ":living_imperial_vassals", 0)')
    assert_contains(raw, 'king_death_after_defeat_chance')
    assert_contains(raw, 'hero_death_after_defeat_chance')


def test_faction_notes_surface_realm_systems() -> None:
    raw = read("src/scripts/ZF_factions/update_faction_notes.py")
    assert_contains(raw, "script_sod_law_recalculate_faction_law_modifiers")
    assert_contains(raw, "script_sod_law_count_active_for_faction")
    assert_contains(raw, "slot_faction_law_militarization")
    assert_contains(raw, "slot_faction_law_centralization")
    assert_contains(raw, "slot_faction_law_legitimacy")
    assert_contains(raw, "slot_faction_law_unrest")
    assert_contains(raw, "slot_faction_current_power")
    assert_contains(raw, "Realm systems")
    assert_contains(raw, "Legion")


def test_slavers_black_market_web_exists() -> None:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    wilderness = read("src/menus/captivity/captivity_wilderness_check.py")
    castle = read("src/menus/captivity/captivity_castle_check.py")
    for token in (
        "slot_faction_slaver_market_demand",
        "slot_faction_slaver_market_supply",
        "slot_faction_slaver_market_heat",
        "slot_faction_slaver_market_bases",
        "slot_party_sod_slaver_web_activity",
        "sod_slaver_action_trade_prisoners",
        "sod_slaver_action_free_runaways",
        "sod_slaver_action_buy_slaves",
        "sod_slaver_action_carry_slaves",
    ):
        assert_contains(constants, token)
    for script_name in (
        '"sod_slavers_update_market_state"',
        '"sod_slavers_apply_player_action"',
        '"sod_slavers_spawn_world_activity"',
        '"sod_slavers_process_world_activity"',
        '"sod_slavers_process_player_slave_burden"',
        '"sod_slavers_store_slave_purchase_quote"',
        '"sod_slavers_buy_slaves_for_player"',
        '"sod_slavers_describe_status_to_s20"',
    ):
        assert_contains(scripts, script_name)
    assert_contains(scripts, "pt_slavers_caravan")
    assert_contains(scripts, "pt_slaves_with_jotnar_clansmen")
    assert_contains(weekly, "script_sod_slavers_spawn_world_activity")
    assert_contains(read("src/triggers/ST03_daily/entry_0156.py"), "script_sod_slavers_process_world_activity")
    assert_contains(read("src/triggers/ST03_daily/entry_0157.py"), "script_sod_slavers_process_player_slave_burden")
    assert_contains(read("src/triggers/_order_simple_triggers.txt"), "ST03_daily/entry_0156.py")
    assert_contains(read("src/triggers/_order_simple_triggers.txt"), "ST03_daily/entry_0157.py")
    assert_contains(scripts, "Slaver black market transport")
    assert_contains(scripts, "remove_party")
    assert_contains(scripts, "party_add_members, \"p_main_party\", \"trp_slave\"")
    assert (
        "troop_remove_gold" in scripts
        or "script_sod_player_charge_gold" in scripts
    ), "slaver slave purchase must charge the player"
    assert_contains(scripts, "Keeping slaves in your party damages your honor")
    assert_contains(notes, "script_sod_slavers_describe_status_to_s20")
    assert_contains(scripts, "Black market web")
    assert_contains(wilderness, "slot_faction_slaver_market_demand")
    assert_contains(castle, "slot_faction_slaver_market_heat")


def test_slaver_player_actions_feed_market_state() -> None:
    ramun = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_ramun_the_slave_trader_ramun_sell_prisoners.py")
    guild = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_gm_talk_sell_prisoners.py")
    escort = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start.py")
    returned = read("src/dialogs/ZZ99_misc_dialogs/party_tpl_pt_runaway_slaves_runaway_slave_go_back.py")
    freed = read("src/dialogs/ZZ99_misc_dialogs/anyone_runaway_slave_let_go.py")
    assert_contains(ramun, "sod_slaver_action_trade_prisoners")
    assert_contains(guild, "sod_slaver_action_trade_prisoners")
    assert_contains(escort, "sod_slaver_action_escort_caravan")
    assert_contains(returned, "sod_slaver_action_return_runaways")
    assert_contains(freed, "sod_slaver_action_free_runaways")


def test_player_can_buy_slaves_from_slaver_market() -> None:
    ramun = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_ramun_the_slave_trader_plyr_ramun_buy_slaves.py")
    guild = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_buy_slaves.py")
    quote = read("src/dialogs/ZZ99_misc_dialogs/anyone_sod_slaver_buy_slaves_quote.py")
    confirm = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sod_slaver_buy_slaves_confirm.py")
    order = read("src/dialogs/_order_dialogs.txt")
    assert_contains(ramun, "Show me the captives for sale, Ramun, and name your price.")
    assert_contains(guild, "slavers_guild_master")
    assert_contains(guild, "slavers_rep")
    assert_contains(quote, "script_sod_slavers_store_slave_purchase_quote")
    assert_contains(confirm, "script_sod_slavers_buy_slaves_for_player")
    assert_contains(order, "trp_ramun_the_slave_trader_plyr_ramun_buy_slaves.py")
    assert_contains(order, "anyone_plyr_gm_buy_slaves.py")
    assert_contains(order, "anyone_sod_slaver_buy_slaves_done.py")


def test_player_slave_ownership_has_consequences_and_release_path() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    camp_action = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    free_menu = read("src/menus/camp/free_slaves_confirm.py")
    menu_order = read("src/menus/_order_game_menus.txt")
    assert_contains(scripts, "sod_slaver_action_carry_slaves")
    assert_contains(scripts, "script_change_player_honor\", -1")
    assert_contains(camp_action, "mnu_free_slaves_confirm")
    assert_contains(free_menu, "party_remove_members, \"p_main_party\", \"trp_slave\"")
    assert_contains(free_menu, "party_remove_members, \"p_main_party\", \"trp_slave_female\"")
    assert_contains(free_menu, "script_change_player_honor")
    assert_contains(free_menu, "sod_slaver_action_free_runaways")
    assert_contains(menu_order, "camp/free_slaves_confirm.py")


def test_elephant_guard_sacred_warden_world_presence_exists() -> None:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    order = read("src/triggers/_order_simple_triggers.txt")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    dialogs_order = read("src/dialogs/_order_dialogs.txt")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py") + read("src/menus/reports/report_submenus.py")
    warden_report = read("src/menus/reports/elephant_guard_warden_report.py")
    party_templates = read("compile/module_party_templates.py")
    for token in (
        "slot_faction_elephant_guard_devotion",
        "slot_faction_elephant_guard_supplies",
        "slot_faction_elephant_guard_omens",
        "slot_faction_elephant_guard_slaver_alarm",
        "slot_party_sod_elephant_guard_activity",
        "sod_elephant_guard_activity_patrol",
        "sod_elephant_guard_activity_procession",
    ):
        assert_contains(constants, token)
    for script_name in (
        '"sod_elephant_guard_update_sacred_state"',
        '"sod_elephant_guard_spawn_world_activity"',
        '"sod_elephant_guard_process_world_activity"',
        '"sod_elephant_guard_apply_player_support"',
        '"sod_elephant_guard_grant_player_blessing"',
        '"sod_elephant_guard_grant_road_volunteers"',
        '"sod_elephant_guard_free_player_slaves"',
        '"sod_elephant_guard_describe_status_to_s21"',
    ):
        assert_contains(scripts, script_name)
    assert_contains(party_templates, "elephant_guard_sanctuary_patrol")
    assert_contains(party_templates, "elephant_guard_relic_procession")
    assert_contains(scripts, "script_get_center_threat_level")
    assert_contains(scripts, "script_change_center_prosperity")
    assert_contains(scripts, "Elephant Guard relic procession")
    assert_contains(weekly, "script_sod_elephant_guard_spawn_world_activity")
    assert_contains(daily, "script_sod_elephant_guard_process_world_activity")
    assert_contains(order, "ST03_daily/entry_0158.py")
    assert_contains(notes, "script_sod_elephant_guard_describe_status_to_s21")
    assert_contains(notes, "fac_sod_merc_guild3")
    assert_contains(dialogs_order, "party_tpl_pt_elephant_guard_sanctuary_patrol_start.py")
    assert_contains(dialogs_order, "party_tpl_pt_elephant_guard_relic_procession_start.py")
    assert_contains(dialogs_order, "anyone_plyr_elephant_guard_world_talk_03.py")
    assert_contains(dialogs_order, "anyone_plyr_elephant_guard_world_talk_06.py")
    assert_contains(dialogs_order, "anyone_plyr_elephant_guard_world_talk_07.py")
    assert_contains(dialogs_order, "anyone_elephant_guard_world_volunteers.py")
    assert_contains(dialogs_order, "anyone_elephant_guard_world_free_slaves.py")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_02.py"), "script_sod_elephant_guard_apply_player_support")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_03.py"), "script_sod_elephant_guard_grant_player_blessing")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_06.py"), "script_sod_elephant_guard_grant_road_volunteers")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_07.py"), "script_sod_elephant_guard_free_player_slaves")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_05.py"), "script_change_player_relation_with_faction")
    assert_contains(scripts, "trp_elephant_guard_tribesman")
    assert_contains(scripts, "trp_elephant_guard_fighter")
    assert_contains(scripts, "script_sod_slavers_apply_player_action")
    assert_contains(scripts, "sod_slaver_action_free_runaways")
    assert_contains(scripts, "slot_faction_slaver_market_heat")
    assert_contains(scripts, "slot_party_sod_slaver_web_activity")
    assert_contains(scripts, "slot_faction_elephant_guard_slaver_alarm")
    assert_contains(scripts, "ai_bhvr_attack_party")
    assert_contains(scripts, "sod_slaver_action_hostile")
    assert_contains(scripts, "Slaver alarm")
    assert_contains(reports_menu, "mnu_elephant_guard_warden_report")
    assert_contains(warden_report, "Elephant Guard Sacred Wardens")
    assert_contains(warden_report, "{s21}")
    assert_contains(warden_report, "slot_faction_elephant_guard_slaver_alarm")
    assert_contains(warden_report, "pt_elephant_guard_sanctuary_patrol")
    assert_contains(warden_report, "pt_elephant_guard_relic_procession")
    assert_contains(warden_report, "script_sod_elephant_guard_describe_status_to_s21")
    assert_contains(warden_report, "Send 500 denars to Elephant Guard relief stores")
    assert_contains(warden_report, "script_sod_elephant_guard_apply_player_support")
    assert_contains(warden_report, "$g_sod_elephant_guard_last_report_donation_day")
    assert (
        "troop_remove_gold" in warden_report
        or "script_sod_player_charge_gold" in warden_report
    ), "Elephant Guard relief donation must charge the player"
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/elephant_guard_warden_report.py")


def test_jotnar_hearthbound_kin_world_presence_exists() -> None:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    dialogs_order = read("src/dialogs/_order_dialogs.txt")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py") + read("src/menus/reports/report_submenus.py")
    hearth_report = read("src/menus/reports/jotnar_hearth_report.py")
    slavers = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    party_templates = read("compile/module_party_templates.py")
    for token in (
        "slot_faction_jotnar_hearth_pressure",
        "slot_faction_jotnar_active_parties",
        "slot_faction_jotnar_target_center",
        "slot_faction_jotnar_slaver_pressure",
        "slot_party_sod_jotnar_hearth_activity",
    ):
        assert_contains(constants, token)
    for script_name in (
        '"sod_jotnar_update_hearth_state"',
        '"sod_jotnar_spawn_world_activity"',
        '"sod_jotnar_process_world_activity"',
        '"sod_jotnar_apply_player_support"',
        '"sod_jotnar_grant_hearth_volunteers"',
        '"sod_jotnar_free_player_captives"',
        '"sod_jotnar_describe_status_to_s22"',
    ):
        assert_contains(scripts, script_name)
    assert_contains(party_templates, "jotnar_hearth_guard")
    assert_contains(party_templates, "jotnar_wintering_camp")
    assert_contains(scripts, "script_get_center_threat_level")
    assert_contains(scripts, "script_change_center_prosperity")
    assert_contains(scripts, "script_sod_slavers_apply_player_action")
    assert_contains(scripts, "slot_party_sod_slaver_web_activity")
    assert_contains(scripts, "ai_bhvr_attack_party")
    assert_contains(scripts, "Jotnar hearth guards are shadowing Slaver traffic")
    assert_contains(scripts, "trp_jotnar_clan_armsman")
    assert_contains(scripts, "trp_jotnar_clan_volva")
    assert_contains(weekly, "script_sod_jotnar_spawn_world_activity")
    assert_contains(daily, "script_sod_jotnar_process_world_activity")
    assert_contains(notes, "script_sod_jotnar_describe_status_to_s22")
    assert_contains(notes, "fac_sod_merc_guild4")
    assert_contains(dialogs_order, "anyone_plyr_jotnar_world_hearth_talk_04.py")
    assert_contains(dialogs_order, "anyone_plyr_jotnar_world_hearth_talk_05.py")
    assert_contains(dialogs_order, "anyone_jotnar_world_hearth_volunteers.py")
    assert_contains(dialogs_order, "anyone_plyr_jotnar_world_hearth_talk_06.py")
    assert_contains(dialogs_order, "anyone_jotnar_world_hearth_free_captives.py")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_jotnar_world_hearth_talk_04.py"), "script_sod_jotnar_apply_player_support")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_jotnar_world_hearth_talk_05.py"), "script_sod_jotnar_grant_hearth_volunteers")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_jotnar_world_hearth_talk_06.py"), "script_sod_jotnar_free_player_captives")
    assert_contains(reports_menu, "mnu_jotnar_hearth_report")
    assert_contains(hearth_report, "Jotnar Hearthbound Kin")
    assert_contains(hearth_report, "slot_faction_jotnar_slaver_pressure")
    assert_contains(hearth_report, "pt_jotnar_hearth_guard")
    assert_contains(hearth_report, "pt_jotnar_wintering_camp")
    assert_contains(hearth_report, "script_sod_jotnar_describe_status_to_s22")
    assert_contains(hearth_report, "Send 400 denars to Jotnar hearth stores")
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/jotnar_hearth_report.py")
    assert_contains(slavers, "fac_sod_merc_guild4")
    assert_contains(slavers, "sod_slaver_action_buy_slaves")


def test_black_khergit_moving_horde_exists() -> None:
    constants = read("src/constants/module_constants.py")
    party_templates = read("compile/module_party_templates.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py") + read("src/menus/reports/report_submenus.py")
    dashboard = read("src/menus/reports/mercenary_world_activity_report.py")
    for token in (
        "slot_faction_black_khergit_pressure",
        "slot_faction_black_khergit_camp_party",
        "slot_faction_black_khergit_safe_passage_until",
        "slot_faction_black_khergit_camp_disrupted_until",
        "slot_faction_black_khergit_last_raid_report_day",
        "slot_faction_black_khergit_last_pressure_day",
        "slot_party_black_khergit_camp_activity",
        "sod_black_khergit_action_bribe_target",
        "sod_black_khergit_action_persuade_enemy",
        "sod_black_khergit_action_defeat_guards",
    ):
        assert_contains(constants, token)
    for token in (
        '"black_khergit_raiders"',
        '"black_khergit_horde_camp"',
        '"black_khergit_night_guard"',
    ):
        assert_contains(party_templates, token)
    for script_name in (
        '"sod_black_khergits_spawn_or_recover_camp"',
        '"sod_black_khergits_process_pressure_economy"',
        '"sod_black_khergits_process_day_cycle"',
        '"sod_black_khergits_spawn_raids"',
        '"sod_black_khergits_apply_safe_passage_to_party"',
        '"sod_black_khergits_refresh_active_parties"',
        '"sod_black_khergits_describe_status_to_s27"',
    ):
        assert_contains(scripts, script_name)
    assert_contains(scripts, "safe-passage hours")
    assert_contains(scripts, "camp disrupted until day")
    assert_contains(scripts, "days remaining")
    assert_contains(scripts, "last reported raid day")
    assert_contains(scripts, "road_dist")
    assert_contains(scripts, "script_sod_black_khergits_process_pressure_economy")
    assert_contains(scripts, "party_ignore_player")
    assert_contains(scripts, "script_sod_black_khergits_refresh_active_parties")
    assert_contains(read("src/triggers/ST02_every_hour/entry_0159.py"), "script_sod_black_khergits_process_day_cycle")
    assert_contains(read("src/triggers/_order_simple_triggers.txt"), "ST02_every_hour/entry_0159.py")
    assert_contains(read("src/triggers/ST03_daily/entry_0158.py"), "script_sod_black_khergits_spawn_raids")
    assert_contains(read("src/scripts/ZZ_common_array_processing/spawn_bandits.py"), "script_sod_black_khergits_spawn_raids")
    assert_contains(read("src/menus/reports/black_khergit_horde_report.py"), "sod_black_khergit_action_bribe_target")
    assert_contains(read("src/menus/reports/black_khergit_horde_report.py"), "sod_black_khergit_action_persuade_enemy")
    assert_contains(reports_menu, "mnu_black_khergit_horde_report")
    assert_contains(dashboard, "script_sod_black_khergits_describe_status_to_s27")
    assert_contains(read("src/dialogs/_order_dialogs.txt"), "party_tpl_pt_black_khergit_horde_camp_start.py")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_talk.py"), "sod_black_khergit_action_bribe_target")


def test_mini_faction_dashboard_links_reports() -> None:
    dashboard = read("src/menus/reports/mercenary_world_activity_report.py")
    for token in (
        "Mini-Faction World Activity",
        "Pressure read",
        "slot_faction_slaver_market_heat",
        "slot_faction_jotnar_hearth_pressure",
        "slot_faction_elephant_guard_slaver_alarm",
        "slot_faction_black_khergit_pressure",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
        "slot_faction_conquistador_requisition_heat",
        "$g_sod_mini_faction_last_incident_type",
        "$g_sod_mini_faction_last_countermeasure_day",
        "$g_sod_mini_faction_last_countermeasure_target",
        "$g_sod_mini_faction_last_countermeasure_score",
        "$g_sod_mini_faction_last_aftermath_day",
        "$g_sod_mini_faction_last_aftermath_type",
        "$g_sod_mini_faction_last_aftermath_score",
        "$g_sod_mini_faction_last_targeted_counterplay_day",
        "$g_sod_mini_faction_last_targeted_counterplay_target",
        "$g_sod_mini_faction_last_targeted_counterplay_strength",
        "$g_sod_mini_faction_last_footprint_day",
        "$g_sod_mini_faction_last_footprint_type",
        "$g_sod_mini_faction_last_footprint_center",
        "Recent incident",
        "Last countermeasure",
        "Last pressure shift",
        "Last targeted counterplay",
        "Last local footprint",
        "Dispatch countermeasures",
        "mini_faction_dispatch_countermeasures_cooldown",
        "mini_faction_dispatch_countermeasures_no_gold",
        "operations are still on cooldown",
        "you need 1000 denars",
        "script_sod_jotnar_apply_player_support",
        "script_sod_elephant_guard_apply_player_support",
        "sod_black_army_action_interdict_road_threats",
        "sod_black_army_action_hire_patrol",
        "sod_serpent_action_track_horde",
        "sod_serpent_action_buy_intel",
        "sod_conquistador_action_fund_supplies",
        "@dangerous",
        "Highest pressure",
        "mnu_conquistador_supply_report",
        "mnu_slaver_black_market_report",
        "mnu_jotnar_hearth_report",
        "mnu_elephant_guard_warden_report",
        "mnu_black_khergit_horde_report",
        "mnu_boar_clan_frontier_report",
        "mnu_serpent_host_route_report",
        "mnu_black_army_security_report",
        "pressure systems",
    ):
        assert_contains(dashboard, token)
    constants = read("src/constants/module_constants.py")
    assert_contains(constants, "sod_black_army_action_interdict_road_threats")
    assert_contains(constants, "sod_serpent_action_track_horde")
    assert_contains(constants, "sod_mini_faction_incident_black_khergit_raid")
    incidents = read("src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py")
    assert_contains(incidents, "sod_mini_faction_process_threshold_incidents")
    assert_contains(incidents, "sod_mini_faction_describe_recent_incident_to_s28")
    assert_contains(incidents, "sod_mini_faction_describe_recent_countermeasure_to_s30")
    assert_contains(incidents, "sod_mini_faction_describe_recommendation_to_s32")
    assert_contains(incidents, "sod_mini_faction_describe_standing_ledger_to_s34")
    assert_contains(incidents, "sod_mini_faction_apply_incident_aftermath")
    assert_contains(incidents, "sod_mini_faction_apply_incident_footprint")
    assert_contains(incidents, "sod_mini_faction_apply_report_counterplay")
    assert_contains(incidents, "Recent local incident")
    assert_contains(incidents, "Recent countermeasure")
    assert_contains(incidents, "Local recommendation")
    assert_contains(incidents, "Mini-faction reputation ledger")
    assert_contains(incidents, "script_sod_slavers_spawn_world_activity")
    assert_contains(incidents, "script_sod_jotnar_spawn_world_activity")
    assert_contains(incidents, "script_sod_elephant_guard_spawn_world_activity")
    assert_contains(incidents, "script_sod_black_khergits_spawn_raids")
    assert_contains(incidents, "$g_sod_mini_faction_last_world_response_day")
    assert_contains(incidents, "$g_sod_mini_faction_last_world_response_type")
    assert_contains(incidents, "$g_sod_mini_faction_last_aftermath_day")
    assert_contains(incidents, "$g_sod_mini_faction_last_aftermath_type")
    assert_contains(incidents, "$g_sod_mini_faction_last_aftermath_score")
    assert_contains(incidents, "$g_sod_mini_faction_last_targeted_counterplay_day")
    assert_contains(incidents, "$g_sod_mini_faction_last_footprint_center")
    assert_contains(incidents, "slot_town_wealth")
    assert_contains(incidents, "script_change_center_prosperity")
    assert_contains(incidents, "slot_faction_jotnar_slaver_pressure")
    assert_contains(incidents, "slot_faction_elephant_guard_slaver_alarm")
    assert_contains(incidents, "slot_faction_serpent_route_pressure")
    assert_contains(incidents, "slot_faction_black_army_contract_heat")
    assert_contains(incidents, "slot_faction_serpent_intelligence")
    assert_contains(incidents, "slot_faction_serpent_safe_passage")
    assert_contains(incidents, "slot_faction_conquistador_supply_stock")
    assert_contains(incidents, "val_sub, \":pressure\", 6")
    assert_contains(incidents, "val_clamp, \":pressure\", 0, 101")
    assert_contains(incidents, "script_sod_quest_event_dispatch")
    assert_contains(incidents, "script_sod_quest_dialogue_record_event")
    assert_contains(incidents, "script_sod_quest_journal_update")
    assert_contains(incidents, "sod_mini_faction_try_companion_triangle")
    assert_contains(incidents, "script_sod_companion_record_triangle_quest_event")
    assert_contains(incidents, "Ymira, Bunduk, and Lezalit argue the Slaver web")
    assert_contains(incidents, "Ymira sees shelter, Bunduk sees unpaid defense")
    assert_contains(incidents, "Ymira, Alayen, and Jeremus")
    assert_contains(incidents, "Borcha reads the theft")
    assert_contains(incidents, "Marnid calls it bad accounting")
    assert_contains(incidents, "Borcha, Deshavi, and Klethi")
    assert_contains(incidents, "Deshavi distrusts paid order")
    assert_contains(incidents, "Marnid sees coerced markets")
    assert_contains(incidents, "Ymira watches the Slaver reports")
    assert_contains(incidents, "Marnid notes")
    assert_contains(incidents, "$g_sod_mini_faction_last_incident_day")
    assert_contains(incidents, "$g_sod_mini_faction_last_countermeasure_target")
    assert_contains(incidents, "display_message")
    assert_contains(read("src/triggers/ST03_daily/entry_0158.py"), "script_sod_mini_faction_process_threshold_incidents")
    for path in (
        "src/menus/reports/slaver_black_market_report.py",
        "src/menus/reports/jotnar_hearth_report.py",
        "src/menus/reports/elephant_guard_warden_report.py",
        "src/menus/reports/black_khergit_horde_report.py",
        "src/menus/reports/boar_clan_frontier_report.py",
        "src/menus/reports/serpent_host_route_report.py",
        "src/menus/reports/black_army_security_report.py",
        "src/menus/reports/conquistador_supply_report.py",
    ):
        assert_contains(read(path), "mnu_mercenary_world_activity_report")
        assert_contains(read(path), "script_sod_mini_faction_describe_recent_incident_to_s28")
        assert_contains(read(path), "script_sod_mini_faction_describe_recent_countermeasure_to_s30")
        assert_contains(read(path), "script_sod_mini_faction_describe_recommendation_to_s32")
    slaver_report = read("src/menus/reports/slaver_black_market_report.py")
    assert_contains(slaver_report, "Slaver deals are still handled through Ramun")
    assert_contains(slaver_report, "Anti-Slaver disruption")
    assert_contains(slaver_report, "script_sod_mini_faction_apply_report_counterplay")
    for path in (
        "src/menus/reports/jotnar_hearth_report.py",
        "src/menus/reports/elephant_guard_warden_report.py",
        "src/menus/reports/boar_clan_frontier_report.py",
    ):
        assert_contains(read(path), "Your standing")
        assert_contains(read(path), "@trusted")
        assert_contains(read(path), "@hostile")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py"), "Your standing")
    for path in (
        "src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py",
        "src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py",
        "src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py",
        "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
    ):
        assert_contains(read(path), "your standing {s")
        assert_contains(read(path), "@trusted")
        assert_contains(read(path), "@hostile")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py"), "slot_faction_black_khergit_pressure")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py"), "sod_serpent_action_track_horde")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py"), "slot_faction_slaver_market_supply")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py"), "slot_faction_slaver_market_supply")
    assert_contains(read("src/menus/reports/black_army_security_report.py"), "road-threat interdiction")
    assert_contains(read("src/menus/reports/black_army_security_report.py"), "share one 7-day contract cooldown")
    assert_contains(read("src/menus/reports/serpent_host_route_report.py"), "Black Khergit horde tracking")
    assert_contains(read("src/menus/reports/serpent_host_route_report.py"), "share one 7-day scout cooldown")
    assert_contains(dashboard, "script_sod_mini_faction_describe_standing_ledger_to_s34")
    assert_contains(dashboard, "sod_companion_action_jotnar_support")
    assert_contains(dashboard, "sod_companion_action_elephant_guard_support")
    dialogs_order = read("src/dialogs/_order_dialogs.txt")
    for token in (
        "party_tpl_pt_slavers_caravan_start_03.py",
        "anyone_plyr_slaver_world_caravan_talk.py",
        "anyone_slaver_world_caravan_about.py",
        "anyone_plyr_black_khergit_raider_talk_03.py",
        "anyone_black_khergit_raider_about.py",
        "anyone_plyr_black_khergit_guard_talk_03.py",
        "anyone_black_khergit_guard_about.py",
        "anyone_plyr_jotnar_world_hearth_talk_07.py",
        "anyone_plyr_elephant_guard_world_talk_08.py",
        "anyone_plyr_serpent_host_world_route_talk_06.py",
        "anyone_plyr_boar_clan_meet_05.py",
    ):
        assert_contains(dialogs_order, token)
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_slaver_world_caravan_about.py"), "script_sod_slavers_describe_status_to_s20")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_slaver_world_caravan_talk_02.py"), "sod_companion_action_free_captives")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_raider_about.py"), "script_sod_black_khergits_describe_status_to_s27")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_jotnar_world_hearth_talk_07.py"), "sod_slaver_action_free_runaways")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_08.py"), "sod_slaver_action_hostile")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_serpent_host_world_route_talk_06.py"), "sod_serpent_action_track_horde")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_boar_clan_meet_05.py"), "sod_boar_action_hire_band")
    assert_contains(dashboard, "Last world response")
    for path in (
        "src/menus/reports/jotnar_hearth_report.py",
        "src/menus/reports/elephant_guard_warden_report.py",
        "src/menus/reports/black_khergit_horde_report.py",
        "src/menus/reports/boar_clan_frontier_report.py",
        "src/menus/reports/serpent_host_route_report.py",
        "src/menus/reports/black_army_security_report.py",
        "src/menus/reports/conquistador_supply_report.py",
    ):
        report = read(path)
        assert_contains(report, "Cooldown remaining")
        assert_contains(report, "unavailable")
        assert_contains(report, "need")
        assert "@neutral" not in report, f"{path} should not store a bare neutral label in shared string registers"
        assert "@uncommitted" not in report, f"{path} should not show an uncommitted standing label"
    for path in (
        "src/menus/reports/jotnar_hearth_report.py",
        "src/menus/reports/elephant_guard_warden_report.py",
        "src/menus/reports/boar_clan_frontier_report.py",
    ):
        assert_contains(read(path), "(str_clear, s3)")
    for path in (
        "src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py",
        "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
        "src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py",
        "src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py",
        "src/scripts/ZY_helper_scripts/sod_slavers_black_market.py",
    ):
        raw = read(path)
        assert "@neutral" not in raw, f"{path} should not store a bare neutral label in shared string registers"
        assert "@uncommitted" not in raw, f"{path} should not show an uncommitted standing label"
    for path, scratch_register in (
        ("src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py", "s22"),
        ("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py", "s22"),
        ("src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py", "s21"),
        ("src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py", "s22"),
        ("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py", "s21"),
    ):
        assert_contains(read(path), f"(str_clear, {scratch_register})")


def test_post_defeat_spectator_follow_camera_is_shared() -> None:
    constants = read("src/constants/module_constants.py")
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    spectator = read("src/scripts/ZE_encounters/sod_post_defeat_spectator.py")
    company_report = read("src/scripts/ZY_helper_scripts/companion_describe_company_report.py")
    depth_report = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    doc = read("docs/combat/POST_DEFEAT_SPECTATOR_HERO_SWITCHING.md")

    assert_contains(constants, "slot_agent_sod_post_defeat_focus_index")
    assert_contains(constants, "slot_troop_sod_times_took_command")
    assert_contains(constants, "slot_troop_sod_post_fall_victories")
    assert_contains(constants, "slot_troop_sod_post_fall_failures")
    assert_contains(constants, "slot_troop_sod_last_took_command_hours")
    for token in (
        '"sod_post_defeat_init"',
        '"sod_post_defeat_rebuild_watch_list"',
        '"sod_post_defeat_choose_second_in_command"',
        '"sod_post_defeat_on_player_fallen"',
        '"sod_post_defeat_record_aftermath"',
        '"sod_post_defeat_count_casualties_once"',
        '"sod_post_defeat_describe_command_memory_to_s35"',
        '"sod_post_defeat_select_next_agent"',
        '"sod_post_defeat_focus_camera"',
        '"cf_sod_post_defeat_agent_is_watchable_base"',
        '"cf_sod_post_defeat_agent_is_watchable_hero"',
        '"cf_sod_post_defeat_agent_is_watchable_officer"',
        "slot_agent_sod_post_defeat_focus_index",
        "(agent_is_ally, \":agent_no\")",
        "(agent_slot_eq, \":agent_no\", slot_agent_is_hard_routed, 0)",
        "(store_skill_level, \":leadership\", \"skl_leadership\", \":troop_no\")",
        "(store_skill_level, \":tactics\", \"skl_tactics\", \":troop_no\")",
        "(neg|troop_is_hero, \":troop_no\")",
        "(ge, \":level\", 15)",
        "slot_troop_sod_times_took_command",
        "slot_troop_sod_post_fall_victories",
        "slot_troop_sod_post_fall_failures",
        "slot_troop_sod_last_took_command_hours",
        "Command continuity:",
        "$sod_post_defeat_next_rebuild_time",
        "$sod_post_defeat_casualties_counted",
        "$sod_post_defeat_aftermath_recorded",
        "The company stands victorious after you fall",
        "The company breaks after you fall",
        "no surviving officer held the line",
        "script_count_mission_casualties_from_agents",
        "(store_mission_timer_a, \":mission_time\")",
        "No surviving ally remains to follow. Free camera.",
        "script_sod_battle_apply_courage_pressure",
    ):
        assert_contains(spectator, token)
    assert_contains(company_report, "script_sod_post_defeat_describe_command_memory_to_s35")
    assert_contains(company_report, "{s35}")
    assert_contains(depth_report, "script_sod_post_defeat_describe_command_memory_to_s35")
    assert_contains(depth_report, "{s35}")

    shared_camera_templates = (
        "src/mission_templates/0005_bandits_at_night/bandits_at_night.py",
        "src/mission_templates/0010_lead_charge/lead_charge.py",
        "src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py",
        "src/mission_templates/0012_village_raid/village_raid.py",
        "src/mission_templates/0013_besiege_inner_battle_castle/besiege_inner_battle_castle.py",
        "src/mission_templates/0014_besiege_inner_battle_town_center/besiege_inner_battle_town_center.py",
        "src/mission_templates/0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py",
        "src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py",
        "src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py",
        "src/mission_templates/0050_custom_battle/custom_battle.py",
    )
    for path in shared_camera_templates:
        template = read(path)
        assert_contains(template, "camera_trigger_1")
        assert_contains(template, "camera_trigger_8")
    assert_contains(doc, "## Mission Classification Snapshot")
    assert_contains(doc, "## Player-Agent And Fall-Defeat Audit")
    assert_contains(doc, "`0005_bandits_at_night/bandits_at_night.py`")
    assert_contains(doc, "`0050_custom_battle/custom_battle.py`")
    assert_contains(doc, "No mission is currently classified as safe takeover.")
    assert_contains(doc, "Formation command triggers in `_preamble/00_imports.py`")
    assert_contains(doc, "`main_hero_fallen` force-defeat assumptions found:")

    assert_contains(preamble, '(call_script, "script_sod_post_defeat_init")')
    assert_contains(preamble, '(call_script, "script_sod_post_defeat_on_player_fallen")')
    assert_contains(preamble, '(call_script, "script_sod_post_defeat_record_aftermath", 1)')
    assert_contains(preamble, '(call_script, "script_sod_post_defeat_record_aftermath", -1)')
    assert_contains(preamble, '(call_script, "script_sod_post_defeat_count_casualties_once")')
    active_preamble = "\n".join(
        line for line in preamble.splitlines() if not line.lstrip().startswith("#")
    )
    assert active_preamble.count('(call_script, "script_count_mission_casualties_from_agents")') == 0
    safe_battle_templates = (
        "src/mission_templates/0010_lead_charge/lead_charge.py",
        "src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py",
        "src/mission_templates/0012_village_raid/village_raid.py",
        "src/mission_templates/0013_besiege_inner_battle_castle/besiege_inner_battle_castle.py",
        "src/mission_templates/0014_besiege_inner_battle_town_center/besiege_inner_battle_town_center.py",
        "src/mission_templates/0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py",
        "src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py",
        "src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py",
        "src/mission_templates/0050_custom_battle/custom_battle.py",
    )
    for path in safe_battle_templates:
        template = read(path)
        active_template = "\n".join(
            line for line in template.splitlines() if not line.lstrip().startswith("#")
        )
        for trigger_name in (
            "camera_trigger_1",
            "camera_trigger_2",
            "camera_trigger_3",
            "camera_trigger_4",
            "camera_trigger_5",
            "camera_trigger_6",
        ):
            assert_contains(template, trigger_name)
        assert active_template.count('(call_script, "script_count_mission_casualties_from_agents")') == 0
    excluded_takeover_templates = (
        "src/mission_templates/0024_prison_break/prison_break.py",
        "src/mission_templates/0044_tutorial_1/tutorial_1.py",
        "src/mission_templates/0045_tutorial_2/tutorial_2.py",
        "src/mission_templates/0046_tutorial_3/tutorial_3.py",
        "src/mission_templates/0047_tutorial_3_2/tutorial_3_2.py",
        "src/mission_templates/0048_tutorial_4/tutorial_4.py",
        "src/mission_templates/0049_tutorial_5/tutorial_5.py",
        "src/mission_templates/0060_companion_deshavi_trail_rescue/companion_deshavi_trail_rescue.py",
        "src/mission_templates/0064_companion_jeremus_infirmary/companion_jeremus_infirmary.py",
        "src/mission_templates/0065_companion_lezalit_drill_trial/companion_lezalit_drill_trial.py",
        "src/mission_templates/0066_companion_artimenner_repair_watch/companion_artimenner_repair_watch.py",
    )
    for path in excluded_takeover_templates:
        template = read(path)
        for forbidden in (
            "$sod_post_defeat_mission_allows_takeover",
            "script_sod_post_defeat_agent_is_controllable",
            "set_player_troop",
            "spawn_agent",
        ):
            assert forbidden not in template, f"{path} must not wire post-defeat takeover"
    for forbidden in (
        "choose_fighter_in_battle",
        "prsnt_choose_fighter_in_battle",
        "set_player_troop",
        "spawn_agent",
    ):
        assert forbidden not in spectator, "post-defeat spectator must not paste 108-WB takeover blocks"
        assert forbidden not in preamble, "mission preamble must not paste 108-WB takeover blocks"
    assert_contains(preamble, '(call_script, "script_sod_post_defeat_rebuild_watch_list")')
    assert_contains(preamble, '(call_script, "script_sod_post_defeat_focus_camera")')
    for trigger_name in (
        "formations_1",
        "formations_2",
        "formations_3",
        "formations_0",
        "formations_j",
        "formations_p",
        "formations_k",
        "formations_u",
        "formations_end",
        "formations_dismount",
        "formations_move_infantry",
        "formations_move_archers",
        "formations_move_cavalry",
        "formations_update_ally_infantry",
        "formations_update_ally_archers",
        "formations_update_ally_cavalry",
        "formations_update_kill_count",
    ):
        block = preamble[preamble.index(f"{trigger_name} =") :]
        block = block[: block.index("\n\n")]
        assert_contains(block, "(neg|main_hero_fallen)")
    for path in (
        "src/mission_templates/0010_lead_charge/lead_charge.py",
        "src/mission_templates/0012_village_raid/village_raid.py",
    ):
        template = read(path)
        for entry_no in ("0", "3"):
            reinforce = template[template.index(f"(add_reinforcements_to_entry, {entry_no},") :]
            reinforce = reinforce[: reinforce.index(")]")]
            assert "main_hero_fallen" not in reinforce
            assert_contains(reinforce, "val_add")
    for trigger_name in (
        "common_siege_defender_reinforcement_check",
        "common_siege_attacker_reinforcement_check",
    ):
        reinforce = preamble[preamble.index(f"{trigger_name} =") :]
        reinforce = reinforce[: reinforce.index("\n\n")]
        assert "main_hero_fallen" not in reinforce
        assert_contains(reinforce, "add_reinforcements_to_entry")
        assert_contains(reinforce, "val_add")
    focus_camera = spectator[spectator.index('("sod_post_defeat_focus_camera"') :]
    focus_camera = focus_camera[: focus_camera.index('("sod_post_defeat_describe_command_memory_to_s35"')]
    assert_contains(focus_camera, "$sod_post_defeat_next_rebuild_time")
    assert_contains(focus_camera, '(call_script, "script_sod_post_defeat_rebuild_watch_list")')
    assert_contains(preamble, '(key_clicked, key_right_mouse_button)')
    assert_contains(preamble, '(key_clicked, key_left_mouse_button)')
    assert_contains(preamble, '"$camera_mode", 2')
    custom_defeat = preamble[preamble.index("custom_battle_check_defeat_condition =") :]
    custom_defeat = custom_defeat[: custom_defeat.index("common_battle_victory_display =")]
    assert_contains(custom_defeat, "(num_active_teams_le, 1)")
    assert_contains(custom_defeat, "(neg|all_enemies_defeated, 2)")
    assert "(main_hero_fallen)" not in custom_defeat
    assert custom_defeat.count('(call_script, "script_sod_post_defeat_clear")') == 1
    assert preamble.count('(call_script, "script_sod_post_defeat_clear")') >= 5
    assert_contains(doc, "- [x] List every mission template that currently includes `camera_trigger_1` through `camera_trigger_8`.")
    assert_contains(doc, "- [x] Classify each mission as safe spectator, safe command continuity, safe takeover, or excluded.")
    assert_contains(doc, "- [x] Confirm which missions currently end immediately on `main_hero_fallen`.")
    assert_contains(doc, "- [x] Confirm which missions intentionally continue after player fall.")
    assert_contains(doc, "- [x] Identify all scripts that assume the original player agent remains the active player agent.")
    assert_contains(doc, "- [x] Identify all scripts that force defeat when `main_hero_fallen` is true.")
    assert_contains(doc, "- [x] Reserve or define safe agent/troop slots for post-defeat focus tracking.")
    assert_contains(doc, "- [x] Add static checks so new post-defeat globals are initialized and cleared.")
    assert_contains(doc, "- [x] Add a follow-camera mode that tracks `$sod_post_defeat_focus_agent`.")
    assert_contains(doc, "- [x] Treat alive allied captains/officers as second-priority watch targets.")
    assert_contains(doc, "- [x] Rebuild the focus list when reinforcements arrive after player fall.")
    assert_contains(doc, "- [x] Ensure casualty counting runs once and only once.")
    assert_contains(doc, "- [x] Verify battle continuation does not break reinforcement triggers.")
    assert_contains(doc, "- [x] Verify formation/order scripts do not spam orders after player fall.")
    assert_contains(doc, "- [x] Add a static test that safe battle templates initialize post-defeat state.")
    assert_contains(doc, "- [x] Add a static test that excluded mission templates do not include takeover triggers.")
    assert_contains(doc, "- [x] Add a static test that no broad pasted 108-WB trigger block was copied into multiple templates.")
    assert_contains(doc, "- [x] Add post-battle summary text for who took command.")
    assert_contains(doc, "- [x] Add event text for no surviving officer.")
    assert_contains(doc, "- [x] Add event text for victory after the captain fell.")
    assert_contains(doc, "- [x] Add event text for collapse after the captain fell.")
    assert_contains(doc, "- [x] Add `$sod_post_defeat_second_in_command`.")
    assert_contains(doc, "- [x] Feed the result into battle ranking or company memory.")
    assert_contains(doc, "### Phase 6: Pre-Battle Acting Commander")
    assert_contains(doc, "- [x] Preserve the stricter post-defeat takeover idea as a design note, not an active implementation checklist.")


def test_battle_commander_selection_uses_custom_commander_style_flow() -> None:
    script = read("src/scripts/ZE_encounters/sod_battle_commander.py")
    menu_preamble = read("src/menus/_preamble/00_imports.py")
    selector = read("src/menus/other/sod_battle_commander_select.py")
    debrief = read("src/menus/other/continue_05.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    reset_trigger = read("src/triggers/ST01_every_frame/entry_0175_sod_battle_commander_reset.py")
    mission_preamble = read("src/mission_templates/_preamble/00_imports.py")
    doc = read("docs/combat/POST_DEFEAT_SPECTATOR_HERO_SWITCHING.md")

    for token in (
        '"cf_sod_battle_commander_troop_available"',
        '"cf_sod_battle_commander_party_has_available_commander"',
        '"sod_battle_commander_normalize"',
        '"cf_sod_battle_commander_can_start"',
        '"sod_battle_commander_apply_before_mission"',
        '"sod_battle_commander_spawn_player_ally"',
        '"sod_battle_commander_restore_player_health"',
        '"sod_battle_commander_reset"',
        "(set_player_troop, \":commander\")",
        "(set_player_troop, \"trp_player\")",
        "(str_store_troop_name, s7, \":commander\")",
        "(spawn_agent, \"trp_player\")",
        "(troop_set_inventory_slot, \"trp_player\", ek_horse, -1)",
        "slot_troop_sod_times_took_command",
        "slot_troop_sod_last_took_command_hours",
    ):
        assert_contains(script, token)
    assert_contains(menu_preamble, "build_sod_battle_commander_change_option")
    assert_contains(menu_preamble, "generate_sod_battle_commander_select_options")
    assert_contains(selector, '"sod_battle_commander_select"')
    assert_contains(selector, "If you cannot fight, select a fit companion.")
    assert_contains(debrief, '(call_script, "script_sod_battle_commander_restore_player_health")')
    assert_contains(trigger_order, "entry_0175_sod_battle_commander_reset.py")
    assert_contains(reset_trigger, "(map_free)")
    assert_contains(reset_trigger, '(call_script, "script_sod_battle_commander_reset")')
    assert_contains(mission_preamble, "sod_battle_commander_spawn_player_ally =")
    assert_contains(mission_preamble, "sod_battle_commander_spawn_player_ally_dismounted =")

    for path, trigger_name in (
        ("src/mission_templates/0010_lead_charge/lead_charge.py", "sod_battle_commander_spawn_player_ally"),
        ("src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py", "sod_battle_commander_spawn_player_ally"),
        ("src/mission_templates/0012_village_raid/village_raid.py", "sod_battle_commander_spawn_player_ally_dismounted"),
        ("src/mission_templates/0013_besiege_inner_battle_castle/besiege_inner_battle_castle.py", "sod_battle_commander_spawn_player_ally_dismounted"),
        ("src/mission_templates/0014_besiege_inner_battle_town_center/besiege_inner_battle_town_center.py", "sod_battle_commander_spawn_player_ally_dismounted"),
        ("src/mission_templates/0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py", "sod_battle_commander_spawn_player_ally_dismounted"),
        ("src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py", "sod_battle_commander_spawn_player_ally_dismounted"),
        ("src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py", "sod_battle_commander_spawn_player_ally_dismounted"),
    ):
        assert_contains(read(path), trigger_name)

    for path in (
        "src/menus/0000_hardcoded_mb1011/simple_encounter.py",
        "src/menus/encounter/join_attack.py",
        "src/menus/centers/castle/siege_request_meeting.py",
        "src/menus/centers/castle/talk_to_siege_commander.py",
        "src/menus/centers/castle/siege_defender_join_battle.py",
        "src/menus/centers/village/recruit_volunteers.py",
        "src/menus/centers/village/village_raid_attack.py",
        "src/menus/encounter/peasants_against_bandits_attack_resist.py",
    ):
        raw = read(path)
        assert_contains(raw, "build_sod_battle_commander_change_option")
        assert_contains(raw, "script_cf_sod_battle_commander_can_start")
        assert_contains(raw, "script_sod_battle_commander_apply_before_mission")
        assert_contains(raw, "({s7} leads")
    assert_contains(doc, "Custom Commander-style pre-battle acting commander")
    assert_contains(doc, "- [x] Add a pre-battle acting commander selector")
    assert_contains(doc, "- [x] Show the acting commander's name on battle-entry options, including wounded-player companion-led fights.")
    assert_contains(doc, "- [x] Add a static test that original player troop restore logic exists.")


if __name__ == "__main__":
    test_quest_journal_archive_entries_are_not_duplicated()
    test_quest_journal_surfaces_companion_personal_arcs()
    test_legacy_jester_and_formation_bugfixes()
    test_legacy_honor_duel_and_jotnar_quest_bugfixes()
    test_legacy_construction_and_conquered_court_bugfixes()
    test_legacy_message_feed_boar_toll_and_battle_count_bugfixes()
    test_legacy_enemy_reinforcement_auto_dismount_bugfix()
    test_legacy_diego_and_legion_dialogue_bugfixes()
    test_legacy_party_encounter_invalid_party_bugfix()
    test_legacy_party_size_helpers_reject_invalid_parties()
    test_menu_fragments_are_not_empty_dead_ends()
    test_legacy_unarmed_troop_prisoner_crash_bugfix()
    test_legacy_nearby_friend_strength_invalid_party_spam_bugfix()
    test_legacy_neutral_town_siege_entry_bugfix()
    test_legacy_wilderness_camp_crash_guard()
    test_legacy_mounted_lord_sidearms_bugfix()
    test_legacy_ief_dying_centurion_dialogue_bugfix()
    test_legacy_gaius_marcus_lore_dialogue_bugfixes()
    test_legacy_relic_map_and_mercenary_lord_faction_cleanup_bugfixes()
    test_legacy_antarian_javelinmen_have_multiwave_ammo()
    test_legacy_formations_stale_scripted_order_bugfix()
    test_company_troop_dialogue_static_coverage_registered()
    test_faction_campaign_director_static_coverage_registered()
    test_tax_courier_static_coverage_registered()
    test_captivity_uses_systemic_outcome_inputs()
    test_invasion_arrival_and_report_surfaces_exist()
    test_only_imperial_heroes_can_die_in_battle()
    test_faction_notes_surface_realm_systems()
    test_slavers_black_market_web_exists()
    test_slaver_player_actions_feed_market_state()
    test_player_can_buy_slaves_from_slaver_market()
    test_player_slave_ownership_has_consequences_and_release_path()
    test_elephant_guard_sacred_warden_world_presence_exists()
    test_jotnar_hearthbound_kin_world_presence_exists()
    test_black_khergit_moving_horde_exists()
    test_mini_faction_dashboard_links_reports()
    test_post_defeat_spectator_follow_camera_is_shared()
    test_battle_commander_selection_uses_custom_commander_style_flow()
    print("test_feature_audit_static: OK")






