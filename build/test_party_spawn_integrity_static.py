from pathlib import Path
import ast
import re


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def empty_party_templates():
    raw = read("compile/module_party_templates.py")
    tree = ast.parse(raw)
    assignment = next(
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(getattr(target, "id", "") == "party_templates" for target in node.targets)
    )
    empty = set()
    for entry in assignment.value.elts:
        if len(entry.elts) < 7 or not isinstance(entry.elts[6], ast.List):
            continue
        if len(entry.elts[6].elts) == 0:
            empty.add(f"pt_{entry.elts[0].value}")
    return empty


def literal_spawn_templates():
    pattern = re.compile(r'\(spawn_around_party,\s*[^,\n]+,\s*"(?P<template>pt_[^"]+)"')
    spawns = []
    for path in (ROOT / "src").rglob("*.py"):
        raw = path.read_text(encoding="utf-8")
        for match in pattern.finditer(raw):
            spawns.append((path.relative_to(ROOT).as_posix(), match.group("template")))
    return spawns


def test_no_world_spawn_uses_pt_none():
    offenders = [
        path
        for path, template in literal_spawn_templates()
        if template == "pt_none"
    ]
    assert not offenders, f"pt_none must not be spawned onto the world map: {offenders}"


def test_empty_template_spawns_are_explicitly_audited():
    empty_templates = empty_party_templates()
    allowed_empty_spawns = {
        "pt_deserters",
        "pt_kingdom_hero_party",
        "pt_mercenary_lord_party",
        "pt_messenger_party",
        "pt_patrol_party",
        "pt_player_mercenaries",
        "pt_player_patrol",
        "pt_player_ship",
        "pt_prisoner_train_party",
        "pt_ravaging_bandits",
        "pt_sacrificed_messenger",
        "pt_sod_companion_retinue",
        "pt_sod_mercs",
    }
    offenders = sorted(
        {f"{path}:{template}" for path, template in literal_spawn_templates() if template in empty_templates}
        - {f"{path}:{template}" for path, template in literal_spawn_templates() if template in allowed_empty_spawns}
    )
    assert not offenders, f"new empty-template spawn needs explicit population/name audit: {offenders}"


def test_risky_spawns_validate_before_world_party_creation():
    kingdom_factory = read("src/scripts/ZC_parties/cf_create_kingdom_party.py")
    assert '(assign, ":party_template", -1)' in kingdom_factory
    assert kingdom_factory.index('(gt, ":party_template", 0)') < kingdom_factory.index("(spawn_around_party")

    ai_mercs = read("src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py")
    assert ai_mercs.index('script_sod_merc_guild_get_contract_roster') < ai_mercs.index("(spawn_around_party")
    for bit in [
        '(gt, ":starting_size", 0)',
        '(gt, ":t1_1", 0)',
        '(gt, ":t1_2", 0)',
        '(gt, ":noble", 0)',
        '(neq, ":noble", "trp_player")',
    ]:
        assert bit in ai_mercs

    merc_lord = read("src/scripts/ZY_helper_scripts/sod_merc_lord_try_spawn_for_troop.py")
    assert merc_lord.index('script_sod_merc_guild_get_roster') < merc_lord.index("(spawn_around_party")

    player_mercs = read("src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py")
    spawn_block = player_mercs[player_mercs.index('("merc_spawn_player_company"') :]
    assert spawn_block.index('script_sod_merc_guild_get_roster') < spawn_block.index("(spawn_around_party")
    assert '(party_get_num_companions, ":formed_size", ":mercs")' in spawn_block
    assert '(remove_party, ":mercs")' in spawn_block

    companion_patrol = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_check_leadership.py")
    assert companion_patrol.index("(party_count_members_of_type") < companion_patrol.index("(spawn_around_party")

    change_template = read("src/scripts/ZC_parties/change_party_template.py")
    assert change_template.index('(gt, ":source_companions", 0)') < change_template.index("(spawn_around_party")


def test_quest_variable_spawns_have_invalid_template_fallbacks():
    rtc = read("src/scripts/ZG_quests/sod_rtc_prepare_temporary_target.py")
    assert '(gt, ":template", 0)' in rtc
    assert "(spawn_around_party" in rtc
    assert rtc.index('(gt, ":template", 0)') < rtc.index("(spawn_around_party")

    threat_board = read("src/scripts/ZY_helper_scripts/sod_threat_board_spawn_target.py")
    assert '(le, ":party_template", 0)' in threat_board
    assert '(assign, ":party_template", "pt_bandits")' in threat_board
    assert threat_board.index('(assign, ":party_template", "pt_bandits")') < threat_board.index("(spawn_around_party")

    guild_bandits = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_gm_troublesome_bandits_quest_brief.py")
    assert guild_bandits.index('(gt, ":p_template", 0)') < guild_bandits.index("(spawn_around_party")
    assert guild_bandits.index('(gt, ":troops", 0)') < guild_bandits.index("(spawn_around_party")

    runaway_slaves = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_bring_back_runaway_slaves_accepted.py")
    assert runaway_slaves.index('(gt, ":quest_target_party_template", 0)') < runaway_slaves.index("(spawn_around_party")

    runaway_serfs = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_accepted.py")
    assert runaway_serfs.index('(gt, ":quest_target_party_template", 0)') < runaway_serfs.index("(spawn_around_party")


def test_hourly_sanity_removes_old_empty_world_parties():
    helper = read("src/scripts/ZY_helper_scripts/sod_campaign_party_sanity.py")
    for bit in [
        '(party_get_num_companions, ":num_companions", ":party_no")',
        '(party_get_num_prisoners, ":num_prisoners", ":party_no")',
        '(neq, ":party_type", spt_ship)',
        '(neg|is_between, ":party_no", centers_begin, centers_end)',
        '(neg|is_between, ":party_no", spawn_points_begin, spawn_points_end)',
        '(remove_party, ":party_no")',
    ]:
        assert bit in helper


def test_clear_party_group_removes_cleared_mobile_roots():
    helper = read("src/scripts/ZC_parties/clear_party_group.py")
    for bit in [
        '(party_get_slot, ":root_party_type", ":root_party", slot_party_type)',
        '(party_clear, ":root_party")',
        '(try_for_range_backwards, ":attached_party_rank", 0, ":num_attached_parties")',
        '(neq, ":root_party_type", spt_town)',
        '(neq, ":root_party_type", spt_castle)',
        '(neq, ":root_party_type", spt_village)',
        '(neq, ":root_party_type", spt_ship)',
        '(neq, ":root_party_type", spt_cattle_herd)',
        '(neq, ":root_party_type", spt_merc_base)',
        '(neg|is_between, ":root_party", centers_begin, centers_end)',
        '(neg|is_between, ":root_party", spawn_points_begin, spawn_points_end)',
        '(neg|is_between, ":root_party", training_grounds_begin, training_grounds_end)',
        '(remove_party, ":root_party")',
    ]:
        assert bit in helper
    assert helper.index('(party_clear, ":root_party")') < helper.index('(remove_party, ":root_party")')


def test_encounter_callback_culls_empty_mobile_shells_before_menu_routing():
    callback = read("src/scripts/ZA_hardcoded_game_scripts/game_event_party_encounter.py")
    for bit in [
        '(party_get_num_companions, ":encounter_party_companions", "$g_encountered_party")',
        '(le, ":encounter_party_companions", 0)',
        '(party_get_num_prisoners, ":encounter_party_prisoners", "$g_encountered_party")',
        '(le, ":encounter_party_prisoners", 0)',
        '(neg|is_between, "$g_encountered_party", centers_begin, centers_end)',
        '(neg|is_between, "$g_encountered_party", spawn_points_begin, spawn_points_end)',
        '(neg|is_between, "$g_encountered_party", training_grounds_begin, training_grounds_end)',
        '(remove_party, "$g_encountered_party")',
        '(assign, "$g_encountered_party", -1)',
    ]:
        assert bit in callback
    assert callback.index('(remove_party, "$g_encountered_party")') < callback.index('(jump_to_menu, "mnu_simple_encounter")')


def test_zero_fit_enemies_cannot_start_empty_battle_missions():
    simple = read("src/menus/0000_hardcoded_mb1011/simple_encounter.py")
    join = read("src/menus/encounter/join_attack.py")

    for source in (simple, join):
        assert '(le, "$g_enemy_fit_for_battle", 0)' in source
        assert '(gt, "$g_friend_fit_for_battle", 0)' in source
        assert '(party_get_num_companions, ":enemy_total_companions", "p_collective_enemy")' in source
        assert '(assign, "$g_enemy_surrenders", 1)' in source
        assert '(gt, "$g_enemy_fit_for_battle", 0)' in source
        assert source.index('(assign, "$g_enemy_surrenders", 1)') < source.index('(jump_to_menu, "mnu_total_victory")')

    assert simple.index('(gt, "$g_enemy_fit_for_battle", 0)') < simple.index('(call_script, "script_cf_sod_battle_commander_can_start")')
    assert join.index('(gt, "$g_enemy_fit_for_battle", 0)') < join.index('(call_script, "script_cf_sod_battle_commander_can_start")')


if __name__ == "__main__":
    test_no_world_spawn_uses_pt_none()
    test_empty_template_spawns_are_explicitly_audited()
    test_risky_spawns_validate_before_world_party_creation()
    test_quest_variable_spawns_have_invalid_template_fallbacks()
    test_hourly_sanity_removes_old_empty_world_parties()
    test_clear_party_group_removes_cleared_mobile_roots()
    test_encounter_callback_culls_empty_mobile_shells_before_menu_routing()
    test_zero_fit_enemies_cannot_start_empty_battle_missions()
    print("party spawn integrity static checks passed")
