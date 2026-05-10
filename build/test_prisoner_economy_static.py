# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_prisoner_economy_constants_exist() -> None:
    raw = read("src/constants/module_constants.py")
    for token in [
        "spt_prisoner_train     = 12",
        "slot_center_sod_common_prisoners",
        "slot_center_sod_military_prisoners",
        "slot_center_sod_bandit_prisoners",
        "slot_center_sod_slave_laborers",
        "slot_center_sod_prisoner_unrest_pressure",
        "slot_center_sod_prisoner_escape_pressure",
        "slot_center_sod_prisoner_capacity",
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_prisoner_demand",
        "slot_faction_sod_prisoner_labor_policy",
        "slot_faction_sod_prisoner_exchange_pressure",
        "slot_faction_sod_prisoner_abuse_heat",
        "slot_faction_sod_prisoner_mercy_reputation",
        "slot_faction_sod_active_prisoner_trains",
        "slot_party_sod_prisoner_origin",
        "slot_party_sod_prisoner_destination",
        "slot_party_sod_prisoner_purpose",
        "slot_party_sod_prisoner_value",
        "slot_party_sod_prisoner_guard_quality",
        "slot_party_sod_prisoner_total_count",
        "slot_party_sod_prisoner_military_count",
        "slot_party_sod_prisoner_bandit_count",
        "slot_party_sod_prisoner_civilian_count",
        "slot_party_sod_prisoner_created_day",
        "slot_party_sod_prisoner_expected_arrival_day",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_imprisonment",
        "sod_prisoner_train_purpose_labor",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_trial",
        "sod_prisoner_train_purpose_liberation",
        "sod_prisoner_train_status_traveling",
        "sod_prisoner_labor_policy_regulated",
        "sod_prisoner_train_fail_policy_blocked",
        "sod_prisoner_category_mercenary",
        "sod_prisoner_category_elite",
    ]:
        assert_contains(raw, token)


def test_prisoner_economy_helpers_exist() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        '"sod_classify_prisoner_troop"',
        '"sod_center_recalculate_prisoner_pressure"',
        '"sod_deposit_party_prisoners_to_center_pool"',
        '"sod_withdraw_prisoners_from_center_pool"',
        '"sod_estimate_prisoner_pool_value"',
        '"sod_estimate_prisoner_pool_danger"',
        '"sod_estimate_prisoner_pool_labor_potential"',
        '"sod_find_prisoner_train_destination"',
        '"sod_load_prisoner_train_from_party"',
        '"sod_load_prisoner_train_from_center_pool"',
        '"sod_add_prisoner_train_guards"',
        '"cf_sod_create_prisoner_train"',
        '"sod_maybe_create_prisoner_train_from_party"',
        '"sod_maybe_create_prisoner_train_from_center_overcapacity"',
        '"sod_process_center_prisoner_weekly_pressure"',
        '"sod_process_prisoner_weekly_pressure"',
        '"sod_prisoner_train_describe_to_s20"',
        '"sod_prisoner_train_purpose_to_s23"',
        '"sod_prisoner_train_status_to_s24"',
        '"sod_center_prisoner_report_to_s20"',
        '"sod_faction_prisoner_report_to_s20"',
        '"sod_prisoner_train_arrive"',
        '"sod_prisoner_train_destroyed"',
        '"sod_process_prisoner_trains"',
        "pt_prisoner_train_party",
        "pt_default_prisoners",
        "slot_faction_slaver_market_supply",
        "slot_faction_slaver_market_heat",
        "slot_center_has_prisoner_tower",
        "slot_center_sod_slave_laborers",
        "slot_center_ransom_broker",
        "slot_town_slavers",
        "slot_faction_diplomacy_decree_anti_slaver",
        "slot_faction_sod_prisoner_labor_policy",
        "sod_prisoner_labor_policy_liberation",
        "slot_faction_sod_prisoner_abuse_heat",
        "slot_center_sod_local_population",
        "slot_center_sod_local_prosperity",
        "slot_faction_law_unrest",
        "slot_center_sod_security_cache_contract_security",
        "slot_center_accumulated_tariffs",
        "slot_town_wealth",
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_prisoner_demand",
        "script_sod_change_center_local_prosperity",
        "neg|troop_is_hero",
        "mercenary_troops_begin",
        "mercenary_troops_end",
        "sod_doctrine_flag_mercenary",
        "script_sod_troop_get_elite_tier",
        "sod_elite_tier_elite",
        "sod_prisoner_category_mercenary",
        "sod_prisoner_category_elite",
    ]:
        assert_contains(raw, token)


def test_prisoner_train_outcomes_touch_economy_population_and_law() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        "sod_prisoner_train_purpose_ransom",
        "slot_center_accumulated_tariffs",
        "slot_town_wealth",
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_prisoner_demand",
        "sod_prisoner_train_purpose_exchange",
        "slot_faction_sod_prisoner_exchange_pressure",
        "sod_prisoner_train_purpose_labor",
        "slot_center_sod_slave_laborers",
        "slot_faction_sod_prisoner_abuse_heat",
        "sod_prisoner_train_purpose_trial",
        "slot_faction_law_unrest",
        "slot_center_sod_security_cache_contract_security",
        "sod_prisoner_train_purpose_liberation",
        "slot_center_sod_local_population",
        "slot_center_sod_local_prosperity",
        "script_get_closest_center",
    ]:
        assert_contains(raw, token)


def test_prisoner_train_purpose_layer_is_implemented() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    simulated = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    player_victory = read("src/scripts/ZC_parties/total_victory_distribute_leftovers.py")
    encounter = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_02.py")
    defeated = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "spawn_around_party, \":origin\", \"pt_prisoner_train_party\"",
        "slot_party_type, spt_prisoner_train",
        "slot_party_sod_support_type, spt_prisoner_train",
        "peak_prisoner_trains",
        "script_sod_load_prisoner_train_from_party",
        "script_sod_load_prisoner_train_from_center_pool",
        "script_sod_find_prisoner_train_destination",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_labor",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_liberation",
        "script_sod_prisoner_train_arrive",
        "script_sod_prisoner_train_destroyed",
    ]:
        assert_contains(helper, token)
    assert_contains(simulated, "script_sod_maybe_create_prisoner_train_from_party")
    assert_contains(player_victory, "script_sod_maybe_create_prisoner_train_from_party")
    assert_contains(encounter, "encounter_attack")
    assert_contains(defeated, "script_sod_prisoner_train_destroyed")
    for token in [
        "- [x] Implement prisoner trains as the physical logistics layer between battles, prisons, towns, slaver markets, prisoner exchanges, labor sites, and liberation outcomes.",
        "- [x] Make prisoner trains explain where non-hero captives go after battles instead of letting them vanish into party stacks or sale menus.",
        "- [x] Make prisoner trains valuable enough to protect, raid, escort, ransom, or liberate.",
        "- [x] Keep prisoner trains small enough that they enrich the campaign map without cluttering it.",
        "- [x] Treat prisoner trains as support parties, not lord parties.",
        "- [x] Preserve the old concept of prisoner trains while replacing the old raw spawn triggers with policy-aware creation logic.",
    ]:
        assert_contains(checklist, token)


def test_kingdom_party_factory_knows_prisoner_trains() -> None:
    create_raw = read("src/scripts/ZC_parties/cf_create_kingdom_party.py")
    limit_raw = read("src/scripts/ZC_parties/create_kingdom_party_if_below_limit.py")
    for token in [
        "spt_prisoner_train",
        "pt_prisoner_train_party",
        "script_sod_find_prisoner_train_destination",
        "script_sod_load_prisoner_train_from_center_pool",
        "script_sod_add_prisoner_train_guards",
        "slot_faction_sod_active_prisoner_trains",
    ]:
        assert_contains(create_raw, token)
    assert_contains(limit_raw, "peak_prisoner_trains")
    assert_contains(limit_raw, "spt_prisoner_train")


def test_prisoner_train_party_template_is_sane() -> None:
    raw = read("compile/module_party_templates.py")
    assert_contains(raw, '("prisoner_train_party","Prisoner Train"')
    for token in [
        "icon_mule",
        "carries_goods(12)",
        "pf_show_faction",
        "pf_default_behavior",
        "fac_commoners",
        "escorted_merchant_personality",
        "[]",
    ]:
        assert_contains(raw, token)


def test_prisoner_train_destination_uses_infrastructure_capacity_and_policy() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        "slot_center_ransom_broker",
        "slot_town_slavers",
        "slot_center_sod_prisoner_capacity",
        "script_sod_center_recalculate_prisoner_pressure",
        "towns_begin",
        "castles_begin",
        "villages_begin",
        "slot_faction_marshall",
        "slot_faction_diplomacy_decree_anti_slaver",
        "slot_faction_sod_prisoner_labor_policy",
        "sod_prisoner_labor_policy_none",
        "sod_prisoner_labor_policy_liberation",
        "script_sod_estimate_prisoner_pool_labor_potential",
        "sod_prisoner_train_fail_policy_blocked",
    ]:
        assert_contains(raw, token)


def test_prisoner_destination_uses_slavery_and_labor_policy_gates() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    destination_start = raw.index('("sod_find_prisoner_train_destination"')
    factory_start = raw.index('("cf_sod_create_prisoner_train"')
    destination = raw[destination_start:factory_start]
    for token in [
        "slot_faction_diplomacy_policy_slavery",
        "sod_diplomacy_policy_slavery_tolerated",
        "slot_faction_sod_prisoner_labor_policy",
        "sod_prisoner_labor_policy_penal",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_diplomacy_policy_slavery_banned",
        "slot_faction_diplomacy_decree_anti_slaver",
        "(assign, \":valid_destination\", 0)",
        "sod_prisoner_train_purpose_labor",
        "sod_prisoner_labor_policy_none",
        "sod_prisoner_labor_policy_liberation",
        "sod_diplomacy_policy_slavery_accepted",
        "sod_diplomacy_policy_slavery_regulated",
    ]:
        assert_contains(destination, token)


def test_prisoner_destination_prefers_safer_routes_with_marshal_logistics() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    destination_start = raw.index('("sod_find_prisoner_train_destination"')
    factory_start = raw.index('("cf_sod_create_prisoner_train"')
    destination = raw[destination_start:factory_start]
    for token in [
        "script_sod_marshal_get_planning_profile_to_regs",
        "slot_faction_sod_marshal_logistics_score",
        "assign, \":marshal_logistics\", reg2",
        "assign, \":valuable_prisoners\", 0",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_imprisonment",
        "script_get_center_threat_level",
        "assign, \":destination_threat\", reg0",
        "assign, \":threat_penalty\", \":destination_threat\"",
        "eq, \":valuable_prisoners\", 1",
        "store_div, \":valuable_threat_penalty\", \":destination_threat\", 2",
        "ge, \":marshal_logistics\", 65",
        "store_div, \":logistics_safety_penalty\", \":destination_threat\", 4",
        "lt, \":marshal_logistics\", 35",
        "store_div, \":poor_logistics_discount\", \":threat_penalty\", 3",
        "ge, \":destination_threat\", 70",
        "neq, \":purpose\", sod_prisoner_train_purpose_imprisonment",
        "val_add, \":threat_penalty\", 30",
        "val_sub, \":score\", \":threat_penalty\"",
    ]:
        assert_contains(destination, token)


def test_prisoner_train_factory_validates_origin_threat_and_speed_penalty_inputs() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    speed = read("src/scripts/ZA_hardcoded_game_scripts/game_get_party_speed_multiplier.py")
    for token in [
        "store_faction_of_party, \":origin_faction\", \":origin\"",
        "store_relation, \":origin_relation\", \":origin_faction\", \":faction_no\"",
        "lt, \":origin_relation\", 0",
        "sod_prisoner_train_fail_invalid_origin",
        "script_get_center_threat_level",
        "ge, \":route_threat\", 70",
        "le, \":minimum_guard_strength\", 1",
        "sod_prisoner_train_fail_no_guards",
        "slot_party_sod_trade_route_risk",
        "store_mul, \":guard_coverage\", \":guard_quality\", 20",
        "risk {reg9}",
    ]:
        assert_contains(helper, token)
    for token in [
        "party_slot_eq, \":party_no\", slot_party_type, spt_prisoner_train",
        "slot_party_sod_prisoner_total_count",
        "slot_party_sod_prisoner_guard_quality",
        "slot_party_sod_trade_route_risk",
        "store_div, \":load_penalty\", \":captives\", 8",
        "store_div, \":risk_penalty\", \":route_risk\", 12",
        "store_mul, \":guard_relief\", \":guard_quality\", 2",
        "val_clamp, \":speed_multiplier\", 55, 121",
    ]:
        assert_contains(speed, token)


def test_prisoner_train_guard_composition_is_purpose_aware() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    guard_start = raw.index('("sod_add_prisoner_train_guards"')
    factory_start = raw.index('("cf_sod_create_prisoner_train"')
    guard = raw[guard_start:factory_start]
    for token in [
        "slot_party_sod_prisoner_origin",
        "slot_party_sod_prisoner_destination",
        "slot_party_sod_prisoner_total_count",
        "slot_party_sod_prisoner_value",
        "script_get_center_threat_level",
        "slot_town_wealth",
        "slot_faction_marshall",
        "script_sod_marshal_get_planning_profile_to_regs",
        "slot_faction_tier_2_troop",
        "slot_faction_tier_3_troop",
        "slot_faction_diplomacy_policy_slavery",
        "party_get_num_companions, \":origin_garrison_size\", \":origin\"",
        "gt, \":origin_garrison_size\", 90",
        "store_sub, \":local_garrison_detail\", \":origin_garrison_size\", 80",
        "party_remove_members, \":origin\", \":stack_troop\", \":take\"",
        "party_add_members, \":train_party\", \":stack_troop\", \":take\"",
        "sod_prisoner_train_purpose_slaver_market",
        "trp_slave_hunter",
        "trp_manhunter",
        "trp_caravan_guard",
        "sod_prisoner_train_purpose_labor",
        "trp_watchman",
        "sod_prisoner_train_purpose_liberation",
        "trp_sword_sister",
        "trp_refugee",
        "sod_prisoner_train_purpose_trial",
        "sod_prisoner_train_purpose_exchange",
        "trp_mercenary_horseman",
        "store_distance_to_party_from_party, \":distance\", \":origin\", \":destination\"",
        "gt, \":distance\", 25",
        "gt, \":value\", 500",
        "store_div, \":count_bonus\", \":total_prisoners\", 12",
        "store_div, \":threat_bonus\", \":route_threat\", 10",
        "store_div, \":wealth_bonus\", \":origin_wealth\", 30000",
        "store_div, \":logistics_bonus\", \":marshal_logistics\", 20",
    ]:
        assert_contains(guard, token)


def test_prisoner_economy_slot_ids_are_unique_within_new_slot_families() -> None:
    raw = read("src/constants/module_constants.py")
    families = [
        "slot_center_sod_prisoner_",
        "slot_center_sod_common_prisoners",
        "slot_center_sod_military_prisoners",
        "slot_center_sod_bandit_prisoners",
        "slot_center_sod_slave_laborers",
        "slot_faction_sod_prisoner_",
        "slot_faction_sod_active_prisoner_trains",
        "slot_party_sod_prisoner_",
    ]
    seen: dict[int, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^(slot_(?:center|faction|party)_sod_[A-Za-z0-9_]+)\s*=\s*(\d+)\b", line)
        if not match:
            continue
        name, value_text = match.groups()
        if not any(name.startswith(prefix) for prefix in families):
            continue
        value = int(value_text)
        assert value not in seen, f"duplicate prisoner economy slot id {value}: {seen[value]} and {name}"
        seen[value] = name
    for required in [
        "slot_center_sod_prisoner_capacity",
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_active_prisoner_trains",
        "slot_party_sod_prisoner_origin",
        "slot_party_sod_prisoner_expected_arrival_day",
    ]:
        assert any(name == required for name in seen.values()), f"missing prisoner slot in uniqueness scan: {required}"


def test_player_faction_wage_uses_prisoner_tower_explicitly_for_center_prisoner_upkeep() -> None:
    raw = read("src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py")
    for token in [
        "(this_or_next|party_slot_eq, \":party_no\", slot_party_type, spt_castle)",
        "(party_slot_eq, \":party_no\", slot_party_type, spt_town)",
        "(party_get_num_prisoners, \":num_prisoners\", \":party_no\"),",
        "(assign, \":prisoner_upkeep\", \":num_prisoners\"),",
        "(party_slot_ge, \":party_no\", slot_center_has_prisoner_tower, 1),",
        "(val_div, \":prisoner_upkeep\", 2),",
        "(val_add, \":upkeep\", \":prisoner_upkeep\"),",
    ]:
        assert_contains(raw, token)
    assert "slot_center_has_prisoner_tower, 0" not in raw
    assert "twan456 upkeep was reduced by garrison" not in raw


def test_center_holding_roles_are_distinct() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        ":castle_military_relief",
        ":town_military_strain",
        "is_between, \":center_no\", villages_begin, villages_end",
        "assign, \":capacity\", 0",
        "assign, \":max_count\", -1",
        "is_between, \":destination\", towns_begin, towns_end",
        "val_mul, \":ransom_income\", 125",
        ":town_exchange_bonus",
        "slot_center_ransom_broker",
        "slot_town_slavers",
    ]:
        assert_contains(raw, token)


def test_battle_aftermath_can_request_prisoner_trains() -> None:
    simulated = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    player_victory = read("src/scripts/ZC_parties/total_victory_distribute_leftovers.py")
    for raw in [simulated, player_victory]:
        assert_contains(raw, "script_sod_maybe_create_prisoner_train_from_party")
    assert_contains(simulated, "faction_receiving_prisoners")
    assert_contains(player_victory, "$g_ally_party")
    assert_contains(player_victory, "neq, \":ally_prisoner_carrier\", \"p_main_party\"")


def test_prisoner_train_creation_sources_are_policy_and_marshal_aware() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    simulated = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    for token in [
        '"sod_maybe_create_prisoner_train_from_center_policy_demand"',
        "slot_faction_sod_prisoner_demand",
        "slot_faction_sod_prisoner_exchange_pressure",
        "slot_center_ransom_broker",
        "slot_center_has_prisoner_tower",
        "slot_town_slavers",
        "sod_diplomacy_policy_slavery_accepted",
        "sod_diplomacy_policy_slavery_regulated",
        "slot_faction_diplomacy_decree_anti_slaver",
        "sod_prisoner_labor_policy_liberation",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_liberation",
        "sod_prisoner_train_purpose_trial",
        "slot_party_type, spt_patrol",
        "slot_party_type, spt_player_patrol",
        "script_sod_maybe_create_prisoner_train_from_party",
        "@Prisoner logistics demand created {reg5} center train(s) and {reg6} patrol trial train(s).",
    ]:
        assert_contains(helper, token)
    for token in [
        "slot_faction_marshall",
        "script_sod_marshal_get_planning_profile_to_regs",
        "\":marshal_logistics\"",
        "assign, \":prisoner_train_reason\", 28",
        "sod_prisoner_train_purpose_imprisonment",
    ]:
        assert_contains(simulated, token)


def test_player_defeating_prisoner_train_has_train_consequences() -> None:
    event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    finalize = read("src/scripts/ZC_parties/total_victory_finalize.py")
    assert_contains(event, "slot_party_type, spt_prisoner_train")
    assert_contains(event, "script_sod_prisoner_train_destroyed")
    assert_contains(event, "sod_companion_action_free_captives")
    assert_contains(finalize, ":enemy_was_prisoner_train")
    assert_contains(finalize, "eq, \":enemy_was_prisoner_train\", 0")
    assert_contains(finalize, "script_clear_party_group")


def test_prisoner_train_daily_processor_is_wired() -> None:
    order = read("src/triggers/_order_simple_triggers.txt")
    trigger = read("src/triggers/ST03_daily/entry_0161.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    assert_contains(order, "ST03_daily/entry_0161.py")
    assert_contains(trigger, "script_sod_process_prisoner_trains")
    assert_contains(helper, "script_sod_maybe_create_prisoner_train_from_center_overcapacity")
    assert_contains(helper, "walled_centers_begin")
    assert_contains(helper, "slot_center_sod_prisoner_capacity")


def test_prisoner_train_daily_processor_handles_invalid_destinations() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        '"sod_prisoner_train_disband"',
        "slot_faction_sod_active_prisoner_trains",
        "sod_prisoner_train_status_arrived",
        "sod_prisoner_train_status_intercepted",
        "sod_prisoner_train_status_disbanded",
        "slot_party_sod_prisoner_destination",
        "store_faction_of_party, \":destination_faction\", \":destination\"",
        "neq, \":destination_faction\", \":train_faction\"",
        "script_sod_find_prisoner_train_destination",
        "party_set_ai_behavior, \":party_no\", ai_bhvr_travel_to_party",
        "party_set_ai_object, \":party_no\", \":new_destination\"",
        "slot_center_is_besieged_by",
        "@Prisoner train logistics: {reg3} redirected, {reg4} disbanded.",
    ]:
        assert_contains(helper, token)


def test_prisoner_train_map_ai_handles_threat_refuge_and_escorts() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        '"sod_prisoner_train_update_map_ai"',
        "slot_party_sod_prisoner_value",
        "slot_party_sod_prisoner_guard_quality",
        "script_get_center_threat_level",
        "assign, \":nearest_enemy\"",
        "lt, \":nearby_relation\", 0",
        "lt, \":nearby_dist\", 10",
        "assign, \":threatened\", 1",
        "ge, \":destination_threat\", 75",
        "script_sod_find_prisoner_train_destination",
        "party_set_ai_behavior, \":train_party\", ai_bhvr_travel_to_party",
        "party_slot_eq, \":center_no\", slot_center_is_besieged_by, -1",
        "slot_faction_diplomacy_decree_anti_slaver",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_liberation",
        "fac_sod_merc_guild6",
        "slot_town_slavers",
        "party_set_ai_behavior, \":escort_party\", ai_bhvr_escort_party",
        "party_set_ai_object, \":escort_party\", \":train_party\"",
        "slot_faction_marshall",
        "slot_troop_leaded_party",
        "party_set_ai_behavior, \":marshal_party\", ai_bhvr_escort_party",
        "slot_party_sod_prisoner_expected_arrival_day",
        "gt, \":overdue_days\", 5",
        "script_sod_prisoner_train_disband",
        "script_sod_prisoner_train_update_map_ai",
        "@Prisoner train map AI adjusted {reg7} train(s).",
    ]:
        assert_contains(helper, token)


def test_prisoner_train_interception_resolves_captive_outcomes() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    start = raw.index('("sod_prisoner_train_destroyed"')
    end = raw.index('("sod_process_prisoner_trains"', start)
    destroyed = raw[start:end]
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "(assign, \":captured\", 0)",
        "(assign, \":freed\", 0)",
        "(assign, \":scattered\", 0)",
        "(assign, \":bandit_recruits\", 0)",
        "(assign, \":returned\", 0)",
        "(assign, \":lost\", 0)",
        "fac_mountain_bandits",
        "fac_forest_bandits",
        "fac_black_khergits",
        "slot_faction_diplomacy_decree_anti_slaver",
        "slot_faction_diplomacy_policy_slavery",
        "sod_diplomacy_policy_slavery_accepted",
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_prisoner_exchange_pressure",
        "slot_faction_slaver_market_supply",
        "slot_faction_slaver_market_heat",
        "slot_faction_sod_prisoner_mercy_reputation",
        "script_change_player_relation_with_faction",
        "pt_runaway_slaves",
        "pt_runaway_serfs",
        "pt_bandits",
        "party_add_members, \":bandit_party\", \"trp_bandit\"",
        "script_party_remove_all_prisoners",
        "Prisoner train destroyed: total {reg20}, captured {reg21}, freed {reg22}, scattered {reg23}, bandit recruits {reg24}, returned {reg25}, lost {reg26}, value {reg27}.",
    ]:
        assert_contains(destroyed, token)
    for token in [
        "- [x] Determine whether captives are freed, recaptured, scattered as refugees, recruited by bandits, returned to original faction, or lost in chaos.",
        "- [x] Hostile military attackers should usually capture some prisoners.",
        "- [x] Bandit attackers should recruit some bandit/outlaw captives and scatter the rest.",
        "- [x] Anti-slaver attackers should reduce slaver market supply/heat and gain reputation.",
        "- [x] Apply relation consequences with train owner, prisoner origin factions, and anti-slaver/slaver factions.",
        "- [x] Optionally spawn refugee/fugitive parties if enough captives escape.",
    ]:
        assert_contains(checklist, token)


def test_player_prisoner_train_orders_are_wired() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    order = read("src/menus/_order_game_menus.txt")
    fief = read("src/menus/camp/fief_reports.py")
    menu = read("src/menus/prisoners/prisoner_train_orders.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        '"sod_player_prepare_prisoner_train_order"',
        '"cf_sod_player_commission_prisoner_train"',
        '"sod_player_consume_prisoner_train_food"',
        '"sod_player_cancel_forming_prisoner_train"',
        "slot_faction_leader, \"trp_player\"",
        "slot_faction_marshall, \"trp_player\"",
        "slot_faction_diplomacy_policy_slavery",
        "slot_faction_sod_prisoner_labor_policy",
        "slot_center_ransom_broker",
        "script_sod_find_prisoner_train_destination",
        "script_cf_sod_create_prisoner_train",
        "troop_remove_gold, \"trp_player\"",
        "itm_grain",
        "itm_bread",
        "itm_dried_meat",
        "main_party_has_troop, \"trp_npc3\"",
        "main_party_has_troop, \"trp_npc10\"",
        "main_party_has_troop, \"trp_npc12\"",
        "script_sod_companion_apply_player_action",
        "ai_bhvr_escort_party",
        "script_sod_prisoner_train_disband",
        "Neglected prisoner overcrowding",
        "slot_center_player_relation",
    ]:
        assert_contains(helper, token)
    assert_contains(order, "other/prisoner_train_orders.py")
    assert_contains(fief, "mnu_prisoner_train_orders")
    for token in [
        '("prisoner_train_orders"',
        '("prisoner_train_order_confirm"',
        "sod_prisoner_train_purpose_imprisonment",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_labor",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_liberation",
        "script_sod_player_prepare_prisoner_train_order",
        "script_cf_sod_player_commission_prisoner_train",
        "script_sod_player_cancel_forming_prisoner_train",
        "Confirm and have the train follow me as escort.",
        "Warning: anti-slavery companions object strongly to slave labor and slaver sales.",
    ]:
        assert_contains(menu, token)
    for token in [
        "- [x] Add ruler/marshal command to form a prisoner train from a fief.",
        "- [x] Let the player choose purpose: move to prison, ransom/exchange, labor, sell to slavers, or free/resettle captives.",
        "- [x] Gate each purpose by player status, faction policy, and center infrastructure.",
        "- [x] Charge denars/food/guards based on train size and distance.",
        "- [x] Warn player if companions strongly object.",
        "- [x] Let player cancel a forming train before it departs.",
        "- [x] Let player assign escort if they are near the origin.",
        "- [x] Add consequences if the player neglects over-capacity prisoner pools.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_train_failure_modes_are_handled() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "slot_party_sod_prisoner_origin",
        "store_faction_of_party, \":origin_faction\", \":origin\"",
        "A forming prisoner train at {s1} has been transferred to the new owner.",
        "script_sod_prisoner_train_disband",
        "slot_town_wealth",
        "guard wages are short, guard quality downgraded",
        "slot_party_sod_prisoner_expected_arrival_day",
        "ge, \":delay_days\", 3",
        "slot_center_sod_prisoner_unrest_pressure",
        "slot_center_sod_prisoner_escape_pressure",
        "sod_prisoner_train_fail_no_prisoners",
        "party_get_num_prisoner_stacks, \":representative_stacks\"",
        "pool-only arrival accounting",
        "peak_prisoner_trains",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_liberation",
        "script_sod_estimate_prisoner_pool_value",
        "slot_party_sod_prisoner_value",
    ]:
        assert_contains(raw, token)
    for token in [
        "- [x] If origin loses ownership before departure, cancel or convert the train to the new owner.",
        "- [x] If faction can no longer afford guards, delay or downgrade guard quality.",
        "- [x] If train is delayed too long, increase escape/unrest risk.",
        "- [x] If prison pool becomes empty before departure, cancel creation.",
        "- [x] If no representative prisoner stacks can be created, fallback to pool-only arrival accounting.",
        "- [x] If support-party cap is exceeded, prefer economy-critical or high-value trains.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_economy_integrates_labor_policy_and_road_security() -> None:
    prisoner = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "slot_center_sod_slave_laborers",
        "slot_faction_sod_prisoner_labor_policy",
        "sod_prisoner_labor_policy_penal",
        "sod_prisoner_labor_policy_regulated",
        "sod_prisoner_labor_policy_unrestricted",
        "prisoner_labor_bonus",
        "labor_cost_discount",
        "sod_center_modifier_construction_speed_pct",
        "sod_center_modifier_construction_cost_pct",
    ]:
        assert_contains(construction, token)
    for token in [
        "slot_center_sod_slave_laborers",
        "slot_faction_sod_prisoner_labor_policy",
        "sod_prisoner_labor_policy_regulated",
        "sod_prisoner_labor_policy_unrestricted",
        "slot_faction_sod_prisoner_abuse_heat",
        "script_sod_companion_apply_player_action",
        "script_change_player_relation_with_faction",
        "main_party_has_troop, \"trp_npc3\"",
        "main_party_has_troop, \"trp_npc10\"",
        "main_party_has_troop, \"trp_npc12\"",
        "slot_center_sod_security_cache_contract_security",
        "slot_center_sod_security_cache_threat_reduction",
        "bandit_threat_relief",
    ]:
        assert_contains(prisoner, token)
    for token in [
        "- [x] Let prisoner labor reduce construction time only under policies that allow it.",
        "- [x] Let prisoner labor reduce road/fortification repair cost only under policies that allow it.",
        "- [x] Let prisoner labor reduce honor/relation for humane companions or anti-slavery factions.",
        "- [x] Let regulated labor produce less unrest than unrestricted labor.",
        "- [x] Let bandit prisoners reduce road threat when successfully processed.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_population_integration_handles_mercy_volunteers_and_fugitives() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "slot_center_volunteer_troop_type",
        "slot_center_volunteer_troop_amount",
        "slot_faction_tier_1_troop",
        "freed_soldier_volunteers",
        "civilian_freed",
        "store_div, \":population_gain\", \":civilian_freed\", 4",
        "store_div, \":population_gain\", \":civilians\", 2",
        "pt_runaway_serfs",
        "military_fugitive_party",
        "party_set_faction, \":military_fugitive_party\", \":origin_faction\"",
        "slot_party_food_store",
        "food_pressure_loss",
        "slot_center_sod_security_cache_contract_security",
        "security_strain",
        "script_change_player_honor",
        "script_sod_companion_apply_player_action",
        "script_change_player_relation_with_faction",
    ]:
        assert_contains(raw, token)
    for token in [
        "- [x] Freed soldiers may become recruitable volunteers if culturally compatible.",
        "- [x] Released bandits should not become population by default.",
        "- [x] Escaped military prisoners can return to their faction or spawn small fugitive parties.",
        "- [x] Mass releases should affect local food pressure and security.",
        "- [x] Mercy-based release should improve honor/relations with some factions and companions.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_diplomacy_and_law_hooks_are_wired() -> None:
    prisoner = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    diplomacy = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    peace = read("src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py")
    ransom = read("src/scripts/ZH_heroes/calculate_ransom_amount_for_troop.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        '"sod_process_prisoner_exchange_between_factions"',
        "slot_faction_sod_prisoner_exchange_pressure",
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_prisoner_demand",
        "sod_diplomacy_treaty_truce",
        "sod_diplomacy_memory_captive_freed",
        "script_sod_diplomacy_apply_memory",
        "set_relation, \":faction_a\", \":faction_b\", \":relation\"",
    ]:
        assert_contains(prisoner, token)
    for token in [
        "sod_diplomacy_treaty_prisoner_exchange",
        "script_sod_process_prisoner_exchange_between_factions",
    ]:
        assert_contains(diplomacy, token)
    for token in [
        "sod_diplomacy_treaty_truce",
        "script_sod_process_prisoner_exchange_between_factions",
    ]:
        assert_contains(peace, token)
    for token in [
        "troop_is_hero",
        "script_sod_law_is_active_for_faction",
        "sod_law_noble_ransoms",
        "val_mul, \":ransom_amount\", 130",
    ]:
        assert_contains(ransom, token)
    for token in [
        "slot_faction_diplomacy_policy_slavery",
        "sod_diplomacy_policy_slavery_banned",
        "sod_diplomacy_policy_slavery_regulated",
        "sod_diplomacy_policy_slavery_accepted",
        "slot_faction_diplomacy_decree_anti_slaver",
        "sod_diplomacy_memory_anti_slaver_action",
        "sod_diplomacy_memory_slaver_cooperation",
        "script_change_player_relation_with_faction",
    ]:
        assert_contains(prisoner, token)
    destroyed = prisoner[prisoner.index('("sod_prisoner_train_destroyed"') : prisoner.index('("sod_process_prisoner_trains"')]
    for token in [
        "script_change_player_relation_with_faction",
        "slot_faction_slaver_market_heat",
        "script_sod_companion_apply_player_action",
        "slot_faction_sod_prisoner_mercy_reputation",
        "origin_faction",
    ]:
        assert_contains(destroyed, token)
    for token in [
        "- [x] Connect prisoner exchange treaty to faction prisoner pools.",
        "- [x] Let factions exchange military prisoners during peace or truce negotiations.",
        "- [x] Let noble ransom law affect hero prisoner ransom behavior without changing non-hero pools.",
        "- [x] Let factions condemn or approve player forced-labor policy based on their own stance.",
        "- [x] Add relation consequences for raiding prisoner trains:",
        "  - [x] enemy faction relation changes,",
        "  - [x] released prisoner faction relation changes,",
        "  - [x] companion reactions,",
        "  - [x] slaver market heat changes.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_weekly_pressure_processor_is_wired() -> None:
    order = read("src/triggers/_order_simple_triggers.txt")
    trigger = read("src/triggers/ST04_weekly/entry_0162.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    assert_contains(order, "ST04_weekly/entry_0162.py")
    assert_contains(trigger, "script_sod_process_prisoner_weekly_pressure")
    for token in [
        '"sod_process_center_prisoner_weekly_pressure"',
        '"sod_process_prisoner_weekly_pressure"',
        "slot_center_sod_prisoner_escape_pressure",
        "slot_center_sod_prisoner_unrest_pressure",
        "slot_center_sod_bandit_prisoners",
        "slot_center_sod_military_prisoners",
        "slot_center_sod_common_prisoners",
        "slot_center_sod_security_cache_contract_security",
        "script_sod_change_center_local_prosperity",
        "slot_faction_law_unrest",
    ]:
        assert_contains(helper, token)


def test_prisoner_train_encounter_dialog_is_wired() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    files = [
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_prisoner_train_party_start.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_sod_prisoner_train_about.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_04.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_05.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_06.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_07.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_08.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_02.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk_03.py",
    ]
    for path in files:
        rel = path.replace("src/dialogs/", "")
        assert_contains(order, rel)
    start = read(files[0])
    about = read(files[2])
    attack = read(files[3])
    leave = read(files[4])
    assert_contains(start, "party_tpl|pt_prisoner_train_party")
    assert_contains(start, "sod_prisoner_train_talk")
    assert_contains(about, "script_sod_prisoner_train_describe_to_s20")
    assert_contains(attack, "script_sod_prisoner_train_quote_buy_price")
    assert_contains(leave, "script_sod_player_negotiate_prisoner_train_ransom_exchange")
    assert_contains(read(files[5]), "script_sod_player_accept_prisoner_train_quest_hook")
    assert_contains(read(files[6]), "encounter_attack")
    assert_contains(read(files[7]), "sod_prisoner_train_purpose_slaver_market")
    assert_contains(read(files[8]), "encounter_attack")
    assert_contains(read(files[9]), "$g_leave_encounter")


def test_prisoner_economy_fief_report_is_wired() -> None:
    order = read("src/menus/_order_game_menus.txt")
    fief = read("src/menus/camp/fief_reports.py")
    report = read("src/menus/prisoners/prisoner_economy_report.py")
    assert_contains(order, "other/prisoner_economy_report.py")
    assert_contains(fief, "mnu_prisoner_economy_report")
    for token in [
        '("prisoner_economy_report"',
        "script_sod_center_prisoner_report_to_s20",
        "slot_center_sod_prisoner_unrest_pressure",
        "slot_center_sod_prisoner_escape_pressure",
        "slot_center_has_prisoner_tower",
        "script_sod_estimate_prisoner_pool_value",
        "script_sod_estimate_prisoner_pool_danger",
        "script_sod_estimate_prisoner_pool_labor_potential",
        "mnu_fief_reports",
    ]:
        assert_contains(report, token)


def test_prisoner_player_interaction_policy_and_hooks_are_wired() -> None:
    constants = read("src/constants/module_constants.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    menu = read("src/menus/prisoners/prisoner_train_orders.py")
    victory = read("src/scripts/ZC_parties/total_victory_distribute_leftovers.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "slot_center_sod_prisoner_holding_policy",
        "sod_prisoner_holding_policy_secure",
        "sod_prisoner_holding_policy_ransom",
        "sod_prisoner_holding_policy_labor",
        "sod_prisoner_holding_policy_liberation",
    ]:
        assert_contains(constants, token)
    for token in [
        '"sod_prisoner_train_quote_buy_price"',
        '"sod_player_buy_prisoners_from_train"',
        '"sod_player_negotiate_prisoner_train_ransom_exchange"',
        '"sod_player_accept_prisoner_train_quest_hook"',
        '"sod_prisoner_train_quest_status_to_s20"',
        '"sod_player_set_prisoner_labor_policy"',
        '"sod_player_set_local_prisoner_holding_policy"',
        '"sod_player_build_prisoner_tower_for_policy_target"',
        "$g_sod_prisoner_train_quest_party",
        "$g_sod_prisoner_train_quest_type",
        "$g_sod_prisoner_train_quest_destination",
        "$g_sod_prisoner_train_quest_reward",
        "Current prisoner train objective",
        "party_set_ai_behavior, \":train_party\", ai_bhvr_escort_party",
        "party_add_prisoners, \"p_main_party\"",
        "slot_center_has_prisoner_tower",
        "slot_center_sod_prisoner_holding_policy",
    ]:
        assert_contains(helper, token)
    for token in [
        '("prisoner_policy_orders"',
        '("prisoner_local_holding_orders"',
        "script_sod_player_set_prisoner_labor_policy",
        "script_sod_player_build_prisoner_tower_for_policy_target",
        "script_sod_player_set_local_prisoner_holding_policy",
        "script_sod_prisoner_train_quest_status_to_s20",
        "sod_prisoner_labor_policy_liberation",
        "sod_prisoner_holding_policy_secure",
    ]:
        assert_contains(menu, token)
    for token in [
        "script_sod_maybe_create_prisoner_train_from_party",
        "sod_prisoner_train_purpose_imprisonment",
    ]:
        assert_contains(victory, token)
    for token in [
        "- [x] Add bribe/buy-prisoners option for corrupt or slaver-aligned routes.",
        "- [x] Add ransom/exchange negotiation if train carries military captives.",
        "- [x] Add \"escort this prisoner train\" quest hook.",
        "- [x] Add \"intercept this prisoner train\" quest hook.",
        "- [x] Add \"free these captives\" quest hook.",
        "- [x] Let player rulers set broad prisoner policy.",
        "- [x] Let player marshals order prisoner trains after major victories.",
        "- [x] Let player fief owners build/upgrade Prison Towers and choose local holding policy.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_companion_morality_and_roles_are_wired() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        '"sod_prisoner_count_player_companion_role"',
        '"sod_prisoner_apply_companion_role_pressure_modifiers"',
        '"sod_prisoner_apply_companion_morality_for_outcome"',
        '"sod_prisoner_maybe_trigger_companion_incident"',
        "sod_companion_role_quartermaster",
        "sod_companion_role_surgeon",
        "sod_companion_role_envoy",
        "sod_companion_role_scout",
        "sod_companion_action_ymira_refugee_mercy",
        "sod_companion_action_ymira_refugee_expedience",
        "sod_companion_action_free_captives",
        "sod_companion_action_orderly_profit",
        "sod_companion_action_dirty_profit",
        "sod_companion_action_buy_slaves",
        "sod_companion_action_lezalit_ief_harsh",
        "sod_companion_action_strict_discipline",
        "sod_companion_action_scout_warning",
        "$g_sod_last_spotted_prisoner_train",
        "Your scouts spot {s20}",
        "script_sod_prisoner_apply_companion_role_pressure_modifiers",
        "script_sod_prisoner_apply_companion_morality_for_outcome",
        "script_sod_prisoner_maybe_trigger_companion_incident",
    ]:
        assert_contains(helper, token)
    for token in [
        "- [x] Apply companion/faction morality hooks if the player ordered the train.",
        "- [x] Ymira and mercy-oriented companions react positively to freeing captives.",
        "- [x] Harsh or pragmatic companions react positively to profitable ransoms or hard justice.",
        "- [x] Anti-slavery companions object to slave labor and slaver sales.",
        "- [x] Ruthless companions tolerate or support forced labor.",
        "- [x] Companion incidents can trigger when prisoner abuse heat is high.",
        "- [x] Companion incidents can trigger after freeing a major captive group.",
        "- [x] Companion party roles can modify prisoner handling:",
        "  - [x] quartermaster reduces prisoner escape,",
        "  - [x] surgeon reduces captive deaths,",
        "  - [x] negotiator improves ransom/exchange,",
        "  - [x] scout spots prisoner trains.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_train_ai_behavior_is_policy_and_morale_aware() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    simulated = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        '"sod_prisoner_find_lord_for_party"',
        '"sod_lord_choose_prisoner_train_purpose"',
        '"sod_lord_get_prisoner_train_escort_willingness"',
        "script_sod_lord_get_campaign_pressure",
        "slot_troop_sod_lord_party_morale",
        "slot_troop_sod_lord_pay_strain",
        "slot_troop_wealth",
        "slot_lord_reputation_type",
        "slot_troop_honorable",
        "lrep_upstanding",
        "lrep_goodnatured",
        "lrep_cunning",
        "lrep_selfrighteous",
        "lrep_debauched",
        "sod_prisoner_train_purpose_ransom",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_liberation",
        "sod_prisoner_train_purpose_labor",
        "sod_prisoner_train_purpose_slaver_market",
        "slot_faction_sod_prisoner_exchange_pressure",
        "assign, \":reason\", 39",
        "script_sod_lord_choose_prisoner_train_purpose",
        "script_sod_lord_get_prisoner_train_escort_willingness",
        "ai_bhvr_escort_party",
        "ai_bhvr_attack_party",
        "slot_faction_diplomacy_decree_anti_slaver",
        "fac_outlaws",
        "fac_mountain_bandits",
        "fac_forest_bandits",
        "fac_black_khergits",
        "slot_party_sod_prisoner_bandit_count",
    ]:
        assert_contains(helper, token)
    for token in [
        "script_sod_marshal_get_planning_profile_to_regs",
        "assign, \":prisoner_train_reason\", 28",
        "script_sod_maybe_create_prisoner_train_from_party",
    ]:
        assert_contains(simulated, token)
    for token in [
        "- [x] Low-morale lords are less willing to escort high-risk prisoner trains.",
        "- [x] Cash-strained lords prefer ransom/sale outcomes.",
        "- [x] Honorable lords prefer ransom/exchange/release over slaver sale.",
        "- [x] Ruthless lords prefer labor/slaver destinations if faction policy permits.",
        "- [x] Marshals create prisoner trains after campaign victories.",
        "- [x] Factions under pressure exchange prisoners more readily.",
        "- [x] Anti-slaver factions target slaver prisoner trains when militarily sensible.",
        "- [x] Bandit and outlaw parties may target prisoner trains for recruits or chaos.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_train_rumors_and_checklist_cleanup_are_wired() -> None:
    rumor = read("src/scripts/ZY_helper_scripts/get_rumor_to_s61.py")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "slot_party_type, spt_prisoner_train",
        "slot_party_sod_prisoner_destination",
        "slot_party_sod_prisoner_purpose",
        "slot_party_sod_prisoner_total_count",
        "sod_prisoner_train_purpose_slaver_market",
        "sod_prisoner_train_purpose_liberation",
        "sod_prisoner_train_purpose_exchange",
        "sod_prisoner_train_purpose_ransom",
        "A prisoner train is said to be moving toward {s62}",
    ]:
        assert_contains(rumor, token)
    for token in [
        "- [x] Treat non-hero prisoners as grouped resources, not individual actors.",
        "- [x] Keep hero prisoner logic separate from non-hero prisoner logistics.",
        "- [x] Preserve `change_screen_trade_prisoners` selling behavior.",
        "- [x] A player ruler or marshal can manually commission a prisoner train.",
        "- [x] Add optional traveler/rumor text for prisoner trains, escapes, and mass releases.",
        "- [x] Phase 1: audit and document the existing prisoner/slaver/ransom systems.",
        "- [x] Phase 2: add constants, slots, and static tests.",
        "- [x] Phase 3: add prisoner pool deposit/withdraw/classification helpers.",
        "- [x] Phase 4: connect Prison Tower capacity, escape, and unrest effects.",
        "- [x] Phase 5: revive prisoner trains as simple transfer parties.",
        "- [x] Phase 6: add player encounter dialogs for prisoner trains.",
        "- [x] Phase 9: add diplomacy/prisoner exchange consequences.",
    ]:
        assert_contains(checklist, token)


def test_prisoner_train_debug_and_faction_report_are_descriptive() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    for token in [
        '"sod_prisoner_train_purpose_to_s23"',
        '"sod_prisoner_train_status_to_s24"',
        "@slaver market",
        "@liberation/resettlement",
        "@traveling",
        "@Prisoner train created: {s1} -> {s2}; purpose {s23}; captives {reg5}; value {reg6}; guard {reg7}; risk {reg9}; reason {reg8}.",
        "slot_party_sod_prisoner_value",
        "slot_party_sod_prisoner_guard_quality",
        '"sod_faction_prisoner_report_to_s20"',
        "slot_faction_sod_prisoner_supply",
        "slot_faction_sod_prisoner_demand",
        "slot_faction_sod_prisoner_exchange_pressure",
        "slot_faction_sod_prisoner_abuse_heat",
        "slot_faction_sod_prisoner_mercy_reputation",
        "slot_faction_sod_active_prisoner_trains",
        "@{s22} prisoner economy: policy {s21}; active trains {reg25}.",
    ]:
        assert_contains(raw, token)


def test_checklist_reflects_started_implementation() -> None:
    raw = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "- [x] Add center prisoner pool slots:",
        "- [x] Add faction prisoner economy slots:",
        "- [x] Add support-party slots:",
        "- [x] Verify `pt_prisoner_train_party` exists and has sane flags, personality, and map icon behavior.",
        "- [x] Add or verify `spt_prisoner_train` support-party constant.",
        "- [x] Implement `script_cf_sod_create_prisoner_train`.",
        "- [x] Implement `script_sod_find_prisoner_train_destination`.",
        "- [x] Implement `script_sod_load_prisoner_train_from_party`.",
        "- [x] Implement `script_sod_load_prisoner_train_from_center_pool`.",
        "- [x] Add helper script to withdraw non-hero prisoners from a center pool into a party.",
        "- [x] Add helper script to estimate prisoner pool value.",
        "- [x] Add helper script to estimate prisoner pool danger.",
        "- [x] Add helper script to estimate prisoner pool labor potential.",
        "- [x] A center can request a train when its prisoner pool exceeds safe capacity.",
        "- [x] Battle aftermath can request a train when a marshal campaign captures many enemies.",
        "- [x] A town can request a train when it has ransom/exchange demand.",
        "- [x] A castle can request a train to move valuable prisoners to a safer fortress.",
        "- [x] A slavery-tolerant faction can request a train toward a slaver market or slave-processing town.",
        "- [x] An anti-slavery faction can request a liberation/resettlement train after freeing slaves.",
        "- [x] A patrol can request a trial/imprisonment train after capturing bandits.",
        "- [x] A marshal can request trains after major victories if logistics/planning skill is adequate.",
        "- [x] Increase escape pressure if guards are weak or security is low.",
        "- [x] Make castles better at holding military prisoners than towns.",
        "- [x] Make towns better at processing ransom, exchange, or market prisoners.",
        "- [x] Make villages unable to permanently hold prisoner pools except temporary labor/captive events.",
        "- [x] Add weekly prisoner escape rolls.",
        "- [x] Add weekly prisoner unrest/riot risk for overcrowded centers.",
        "- [x] Escaped bandit prisoners can increase local outlaw pressure.",
        "- [x] Convert ransom prisoners into faction/town income and prisoner demand reduction.",
        "- [x] Prefer towns with ransom broker/slaver infrastructure for ransom or market purpose.",
        "- [x] Prefer faction capitals or marshal muster towns for exchange purpose.",
        "- [x] Prefer labor-site centers only if policy allows labor and unrest is manageable.",
        "- [x] Prefer low-threat routes if prisoners are valuable.",
        "- [x] Avoid destinations already over capacity unless this is an emergency transfer.",
        "- [x] Avoid enemy-threatened destinations unless the train is part of a defensive evacuation.",
        "- [x] Let slavery policy affect what destinations prisoner trains choose.",
        "- [x] Let anti-slaver compact reduce slaver-market trains and increase liberation outcomes.",
        "- [x] Let good marshals/logisticians pick safer destinations; poor planning may choose closer but riskier targets.",
        "- [x] Let ransom/exchange processing create income without forced labor.",
        "- [x] Let military prisoners increase diplomatic exchange leverage.",
        "- [x] Implement `script_sod_add_prisoner_train_guards`.",
        "- [x] Determine guard makeup from creator faction, origin type, prisoner value/count, road threat, faction wealth, marshal logistics, and purpose.",
        "- [x] Slaver-market trains should use slaver/manhunter troops, mercenary guards, or faction troops depending on faction policy.",
        "- [x] Labor trains should use guards from local garrison or militia.",
        "- [x] Liberation trains should use escorts, healers, militia, or low-threat guard composition.",
        "- [x] Bandit-trial trains should use infantry-heavy guard composition.",
        "- [x] Add mounted outriders to valuable long-distance trains.",
        "- [x] Prevent guard generation from draining critical center garrisons below a safe threshold unless the train is an emergency evacuation.",
        "- [x] Optionally take some guards from origin garrison for stronger realism.",
        "- [x] Implement `script_sod_prisoner_train_arrive`.",
        "- [x] Implement `script_sod_prisoner_train_destroyed`.",
        "- [x] Add debug string constants for train purpose/status if this codebase uses debug reports.",
        "- [x] Add dev debug output for prisoner train creation:",
        "  - [x] origin,",
        "  - [x] destination,",
        "  - [x] purpose,",
        "  - [x] prisoner value,",
        "  - [x] guard quality,",
        "  - [x] policy reason.",
        "- [x] Add faction debug summary for prisoner economy state.",
        "- [x] If destination changes ownership, redirect to the nearest valid friendly destination.",
        "- [x] If destination is under siege, redirect unless the purpose is evacuation/reinforcement.",
        "- [x] Make trains avoid enemy centers and high-threat regions when possible.",
        "- [x] Make trains seek refuge at friendly towns/castles if threatened.",
        "- [x] Make trains request nearby patrol/marshal help if carrying high-value prisoners.",
        "- [x] Make low-guard trains flee hostile parties.",
        "- [x] Make slaver trains avoid anti-slaver factions and known hostile player parties.",
        "- [x] Make liberation trains avoid slaver faction territory.",
        "- [x] Make trains disband/reroute if stuck, destination is invalid, or faction is destroyed.",
        "- [x] Determine whether captives are freed, recaptured, scattered as refugees, recruited by bandits, returned to original faction, or lost in chaos.",
        "- [x] Hostile military attackers should usually capture some prisoners.",
        "- [x] Bandit attackers should recruit some bandit/outlaw captives and scatter the rest.",
        "- [x] Anti-slaver attackers should reduce slaver market supply/heat and gain reputation.",
        "- [x] Apply relation consequences with train owner, prisoner origin factions, and anti-slaver/slaver factions.",
        "- [x] Optionally spawn refugee/fugitive parties if enough captives escape.",
        "- [x] Add ruler/marshal command to form a prisoner train from a fief.",
        "- [x] Let the player choose purpose: move to prison, ransom/exchange, labor, sell to slavers, or free/resettle captives.",
        "- [x] Gate each purpose by player status, faction policy, and center infrastructure.",
        "- [x] Charge denars/food/guards based on train size and distance.",
        "- [x] Warn player if companions strongly object.",
        "- [x] Let player cancel a forming train before it departs.",
        "- [x] Let player assign escort if they are near the origin.",
        "- [x] Add consequences if the player neglects over-capacity prisoner pools.",
        "- [x] If origin loses ownership before departure, cancel or convert the train to the new owner.",
        "- [x] If faction can no longer afford guards, delay or downgrade guard quality.",
        "- [x] If train is delayed too long, increase escape/unrest risk.",
        "- [x] If prison pool becomes empty before departure, cancel creation.",
        "- [x] If no representative prisoner stacks can be created, fallback to pool-only arrival accounting.",
        "- [x] If support-party cap is exceeded, prefer economy-critical or high-value trains.",
        "- [x] Let prisoner labor reduce construction time only under policies that allow it.",
        "- [x] Let prisoner labor reduce road/fortification repair cost only under policies that allow it.",
        "- [x] Let prisoner labor reduce honor/relation for humane companions or anti-slavery factions.",
        "- [x] Let regulated labor produce less unrest than unrestricted labor.",
        "- [x] Let bandit prisoners reduce road threat when successfully processed.",
        "- [x] Freed soldiers may become recruitable volunteers if culturally compatible.",
        "- [x] Released bandits should not become population by default.",
        "- [x] Escaped military prisoners can return to their faction or spawn small fugitive parties.",
        "- [x] Mass releases should affect local food pressure and security.",
        "- [x] Mercy-based release should improve honor/relations with some factions and companions.",
        "- [x] Connect prisoner exchange treaty to faction prisoner pools.",
        "- [x] Let factions exchange military prisoners during peace or truce negotiations.",
        "- [x] Let noble ransom law affect hero prisoner ransom behavior without changing non-hero pools.",
        "- [x] Let factions condemn or approve player forced-labor policy based on their own stance.",
        "- [x] Add relation consequences for raiding prisoner trains:",
        "  - [x] enemy faction relation changes,",
        "  - [x] released prisoner faction relation changes,",
        "  - [x] companion reactions,",
        "  - [x] slaver market heat changes.",
        "- [x] Validate origin exists and belongs to the creating faction or allowed ally.",
        "- [x] Reject creation if road threat is too high and no guards can be assigned.",
        "- [x] Assign speed penalty based on prisoner count and guard quality.",
        "- [x] Add `build/test_prisoner_economy_static.py`.",
        "- [x] Verify faction slavery policy constants are used by prisoner train destination logic.",
        "- [x] Verify no new duplicate slot IDs are introduced.",
    ]:
        assert_contains(raw, token)


def test_prisoner_audit_report_exists_and_checklist_is_marked() -> None:
    audit = read("docs/reports/prisoner_system_audit.md")
    checklist = read("docs/reports/prisoner_economy_logistics_checklist.md")
    for token in [
        "# Prisoner, Slaver, Ransom, and Captive System Audit",
        "Selling Prisoners",
        "Ransom Broker Flows",
        "Ramun And Slaver Flows",
        "Prisoner Chat",
        "Noble Release, Keep, Ransom, And Treason",
        "Runaway Slaves",
        "Slaver Caravans",
        "Companion Mercy And Free-Captive Scenes",
        "Prisoner-Related Scripts",
        "`determine_prisoner_agreed`",
        "`calculate_ransom_amount_for_troop`",
        "`remove_troop_from_prison`",
        "`sod_slavers_apply_player_action`",
        "`sod_companion_apply_player_action`",
        "Prisoner Tower Logic",
        "`calculate_player_faction_wage.py`",
        "Dormant Or Legacy Prisoner Train References",
        "Party Templates",
        "`pt_prisoner_train_party`",
        "`pt_slavers_caravan`",
        "`pt_runaway_slaves`",
        "Faction Slavery Policy And Treaty Constants",
        "Non-Hero Prisoner Recruitment, Parole, And Treason",
    ]:
        assert_contains(audit, token)
    for token in [
        "- [x] Audit all active prisoner dialogs:",
        "  - [x] selling prisoners,",
        "  - [x] ransom broker flows,",
        "  - [x] Ramun/slaver flows,",
        "  - [x] prisoner chat,",
        "  - [x] noble release/ransom,",
        "  - [x] runaway slaves,",
        "  - [x] slaver caravans,",
        "  - [x] companion mercy/free-captive scenes.",
        "- [x] Audit prisoner-related scripts:",
        "  - [x] `determine_prisoner_agreed`,",
        "  - [x] `calculate_ransom_amount_for_troop`,",
        "  - [x] `remove_troop_from_prison`,",
        "  - [x] `sod_slavers_apply_player_action`,",
        "  - [x] `sod_companion_apply_player_action`,",
        "  - [x] captivity menus,",
        "  - [x] wage/upkeep scripts,",
        "  - [x] center modifier scripts.",
        "- [x] Audit existing prisoner tower logic for incorrect party/center slot usage.",
        "- [x] Audit dormant prisoner train references in old source/reference folders.",
        "- [x] Audit party templates for prisoner trains, slaver caravans, refugees, and runaway slaves.",
        "- [x] Audit faction slavery policy constants and treaty constants.",
        "- [x] Audit whether non-hero prisoner recruitment/parole/treason is fully implemented or only scaffolded.",
    ]:
        assert_contains(checklist, token)

