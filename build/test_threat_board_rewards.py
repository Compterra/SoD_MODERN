# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_first(*paths: str) -> str:
    for rel in paths:
        candidate = ROOT / rel
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    raise AssertionError(f"Unable to read regional threat board menu from expected paths: {paths}")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected token present: {needle}")


def main() -> int:
    reward = read("src/scripts/ZY_helper_scripts/sod_threat_board_calculate_reward.py")
    describe = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_offer.py")
    accept = read("src/scripts/ZY_helper_scripts/sod_threat_board_accept_contract.py")
    clear_link = read("src/scripts/ZY_helper_scripts/sod_threat_board_clear_target_party_link.py")
    spawn = read("src/scripts/ZY_helper_scripts/sod_threat_board_spawn_target.py")
    active = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_active_contract.py")
    complete = read("src/scripts/ZY_helper_scripts/sod_threat_board_complete_contract.py")
    fail = read("src/scripts/ZY_helper_scripts/sod_threat_board_fail_contract.py")
    defeated = read("src/scripts/ZY_helper_scripts/sod_threat_board_note_party_defeated.py")
    economy = read("src/scripts/ZY_helper_scripts/sod_threat_board_apply_economy_effect.py")
    pressure = read("src/scripts/ZY_helper_scripts/sod_threat_board_apply_regional_pressure.py")
    stakes = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_center_stakes.py")
    init_registry = read("src/scripts/ZY_helper_scripts/sod_threat_board_init_registry.py")
    get_archetype = read("src/scripts/ZY_helper_scripts/sod_threat_board_get_archetype.py")
    generate = read("src/scripts/ZY_helper_scripts/sod_threat_board_generate_offers.py")
    board_menu = read_first(
        "src/menus/reports/regional_threat_board.py",
        "src/menus/camp/regional_threat_board.py",
        "src/menus/other/regional_threat_board.py",
    )
    party_templates = read("compile/module_party_templates.py")
    castle_menu = read("src/menus/centers/castle/castle_castle.py")
    village_menu = read("src/menus/centers/village/recruit_volunteers.py")
    finalize = read("src/scripts/ZC_parties/total_victory_finalize.py")

    assert_contains(reward, "sod_threat_board_calculate_reward")
    assert_contains(reward, "store_sub, \":urgency\", 12, \":deadline_days\"")
    assert_contains(reward, "sod_threat_type_faction_problem")
    assert_contains(reward, "assign, reg(0), \":reward_gold\"")
    assert_contains(reward, "assign, reg(1), \":reward_xp\"")

    assert_contains(describe, "script_sod_threat_board_calculate_reward")
    assert_contains(describe, "{reg4} XP")
    assert_contains(accept, "script_sod_threat_board_calculate_reward")
    assert_contains(accept, "eq, \":offer_index\", 1")
    assert_contains(accept, "That contract option is not available.")
    assert_contains(accept, "slot_quest_sod_threat_offer_1")
    assert_contains(accept, "Target: {s1}. Sponsor: {s2}.")
    assert_contains(accept, "add_quest_note_from_sreg, \"qst_regional_threat_contract\", 4")
    assert_contains(accept, "script_sod_threat_board_spawn_target")
    assert_contains(accept, "That contract could not be issued right now.")
    assert_contains(complete, "call_script, \"script_sod_threat_board_clear_target_party_link\"")
    assert_contains(fail, "call_script, \"script_sod_threat_board_clear_target_party_link\"")
    assert_contains(fail, "slot_party_sod_threat_active_quest")
    assert_contains(fail, "eq, \":active_quest\", \"qst_regional_threat_contract\"")
    assert_contains(clear_link, "slot_party_sod_threat_active_quest, 0")
    assert_contains(defeated, "call_script, \"script_sod_threat_board_clear_target_party_link\", \":party_no\"")
    assert_contains(init_registry, "party_slot_eq, \":threat_party\", slot_party_sod_threat_active_quest, \"qst_regional_threat_contract\"")
    assert_contains(init_registry, "party_set_slot, \":threat_party\", slot_party_sod_threat_active_quest, 0")
    assert_contains(get_archetype, "neg|is_between, \":archetype\", sod_threat_archetypes_begin, sod_threat_archetypes_end")
    assert_contains(get_archetype, "(assign, \":archetype\", sod_threat_archetype_river_pirates)")
    assert_contains(spawn, "spawn_around_party, \":sponsor_center\", \":party_template\"")
    assert_contains(spawn, "party_is_active, \":target_party\"")
    assert_contains(spawn, "party_get_num_companions, \":target_size\", \":target_party\"")
    assert_contains(spawn, "lt, \":target_size\", 1")
    assert_contains(spawn, "eq, \":archetype\", sod_threat_archetype_noble_deserters")
    assert_contains(spawn, "party_add_members, \":target_party\", \"trp_mercenary_swordsman\", 8")
    assert_contains(spawn, "party_add_members, \":target_party\", \"trp_hired_blade\", 4")
    assert_contains(spawn, "str_store_string, s60, \"@Broken Banner Deserters\"")
    assert_contains(spawn, "party_set_name, \":target_party\", s60")
    assert_not_contains(spawn, "party_set_name, \":target_party\", \"@")
    assert_contains(spawn, "party_set_slot, \":target_party\"")
    assert_contains(spawn, "(try_begin)")
    assert_contains(spawn, "assign, reg(0), \":target_party\"")
    assert_contains(party_templates, '("sod_merc_deserters","Deserters"')
    assert_not_contains(party_templates, '("sod_merc_deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[])')
    assert_contains(party_templates, "(trp_mercenary_swordsman,6,12)")
    assert_contains(party_templates, "(trp_hired_blade,1,3)")
    assert_contains(active, "slot_quest_sod_threat_reward_xp")
    assert_contains(active, "{reg6} XP")
    assert_contains(complete, "{reg2} XP")
    assert_contains(complete, "script_sod_threat_board_apply_economy_effect\", \":threat_type\", \":sponsor_center\", 1")
    assert_contains(defeated, "Target defeated: {s5}.")
    assert_contains(defeated, "add_quest_note_from_sreg, \"qst_regional_threat_contract\", 5")
    assert_contains(defeated, "gt, \":party_no\", 0")
    assert_contains(defeated, "party_is_active, \":party_no\"")
    assert_contains(economy, "slot_center_sod_local_population")
    assert_contains(economy, "script_sod_change_center_local_prosperity")
    assert_contains(economy, "script_sod_change_center_wealth")
    assert_contains(economy, "slot_village_number_of_cattle")
    assert_contains(economy, "script_change_center_prosperity")
    assert_contains(economy, "script_change_center_health")
    assert_contains(pressure, "script_sod_threat_board_apply_economy_effect\", \":threat_type\", \":sponsor_center\", -1")
    assert_contains(pressure, "call_script, \"script_sod_threat_board_normalize_center\", \":sponsor_center\"")
    assert_contains(pressure, "assign, \":sponsor_center\", reg0")
    assert_contains(pressure, "script_change_player_relation_with_center")
    assert_contains(stakes, "slot_center_sod_local_population")
    assert_contains(stakes, "slot_center_sod_local_health")
    assert_contains(stakes, "slot_town_prosperity")
    assert_contains(stakes, "slot_center_sod_local_prosperity")
    assert_contains(stakes, "slot_town_wealth")
    assert_contains(stakes, "slot_village_number_of_cattle")
    assert_contains(stakes, "Local:")
    assert_contains(stakes, "No valid center selected.")
    assert_contains(stakes, '(neg|is_between, ":center_no", centers_begin, centers_end)')
    assert_contains(active, "script_sod_threat_board_describe_center_stakes")
    assert_contains(active, "Job Board Contract")
    assert_not_contains(active, "Regional Threat Contract")
    assert_contains(board_menu, "script_sod_threat_board_describe_center_stakes")
    assert_contains(board_menu, "Job Board - {s2}")
    assert_not_contains(board_menu, "Regional Threat Board")
    assert_contains(board_menu, "call_script, \"script_sod_threat_board_normalize_center\", \"$g_sod_threat_board_context_center\"")
    assert_contains(board_menu, '(assign, "$g_sod_threat_board_context_center", reg0)')
    assert_not_contains(board_menu, "script_get_closest_center")
    assert_contains(castle_menu, "call_script, \"script_sod_threat_board_normalize_center\", \"$current_town\"")
    assert_contains(castle_menu, '(assign, "$g_sod_threat_board_context_center", reg0)')
    assert_contains(village_menu, "call_script, \"script_sod_threat_board_normalize_center\", \"$current_town\"")
    assert_contains(village_menu, '(assign, "$g_sod_threat_board_context_center", reg0)')
    assert_contains(generate, "call_script, \"script_sod_threat_board_normalize_center\", \":center_no\"")
    assert_contains(generate, '(assign, ":center_no", reg0)')
    assert_contains(generate, "slot_center_sod_local_population")
    assert_contains(generate, "slot_center_sod_local_health")
    assert_contains(generate, "slot_town_prosperity")
    assert_contains(generate, "slot_center_sod_local_prosperity")
    assert_contains(generate, "slot_town_wealth")
    assert_contains(generate, "slot_village_number_of_cattle")
    assert_contains(generate, "sod_threat_archetype_cattle_raiders")
    assert_contains(generate, "sod_threat_archetype_river_pirates")
    assert_contains(generate, "sod_threat_archetype_army_deserters")
    assert_contains(generate, "sod_threat_archetype_invader_scouts")
    assert_contains(finalize, "script_sod_threat_board_note_party_defeated")
    assert_contains(finalize, "party_is_active, \"$g_enemy_party\"")
    assert_contains(finalize, "party_get_slot, \":sod_threat_active_quest\", \"$g_enemy_party\", slot_party_sod_threat_active_quest")
    assert_contains(finalize, "eq, \":sod_threat_active_quest\", \"qst_regional_threat_contract\"")

    print("[threat_board_rewards] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

