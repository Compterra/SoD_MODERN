# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    report = read("src/menus/reports/diplomacy_report.py")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    war_start = read("src/scripts/ZF_factions/diplomacy_start_war_between_kingdoms.py")
    peace_start = read("src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py")
    decide_ai = read("src/scripts/ZF_factions/decide_faction_ai.py")
    choose_war = read("src/scripts/ZF_factions/faction_chose_an_opponent_and_declare_war.py")
    badboy_change = read("src/scripts/ZF_factions/change_badboy_rating.py")
    badboy_decay = read("src/scripts/ZF_factions/calculate_badboy_decay.py")
    activate_player_faction = read("src/scripts/ZF_factions/activate_deactivate_player_faction.py")
    kingdom_hero_ai = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state.py")
    propose_peace = read("src/scripts/ZF_factions/faction_propose_peace.py")
    slavers = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    black_khergits = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    imperial = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    village_loot = read("src/menus/centers/village/village_loot.py")
    total_defeat = read("src/menus/other/total_defeat.py")
    total_victory = read("src/scripts/ZC_parties/total_victory_finalize.py")
    enemy_hero_resolution = read("src/scripts/ZC_parties/total_victory_try_enemy_hero_resolution.py")
    freed_hero = read("src/scripts/ZC_parties/total_victory_try_freed_hero.py")
    defeated_enemy_party = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    defeated_lord_dialog = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_defeat_lord_answer_06.py")
    executed_lord_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_execute.py")
    simulated_battle = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    party_templates = read("compile/module_party_templates.py")
    checklist = read("docs/systems/DIPLOMACY_SYSTEM_DESIGN.md")
    lord_diplomacy_view = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_talk_diplomacy_view.py")

    for token in (
        "slot_faction_diplomacy_temperament",
        "slot_faction_diplomacy_legitimacy",
        "slot_faction_diplomacy_fear",
        "slot_faction_diplomacy_grievance",
        "slot_faction_diplomacy_war_weariness",
        "slot_faction_diplomacy_trade_interest",
        "slot_faction_diplomacy_honor_stance",
        "slot_faction_diplomacy_slavery_stance",
        "slot_faction_diplomacy_border_stance",
        "slot_faction_diplomacy_current_crisis",
        "slot_faction_diplomacy_policy_culture",
        "slot_faction_diplomacy_policy_border",
        "slot_faction_diplomacy_policy_slavery",
        "slot_faction_diplomacy_policy_military_service",
        "slot_faction_diplomacy_policy_justice",
        "slot_faction_diplomacy_policy_reconstruction",
        "slot_faction_diplomacy_decree_war_taxes",
        "slot_faction_diplomacy_decree_reconstruction",
        "slot_faction_diplomacy_decree_anti_slaver",
        "slot_faction_diplomacy_decree_road_patrol",
        "slot_faction_diplomacy_decree_emergency_conscription",
        "slot_faction_diplomacy_decree_imperial_defense",
        "slot_faction_diplomacy_decree_caravan_protection",
        "slot_faction_treaty_partner_1",
        "slot_faction_diplomacy_memory_player_trust",
        "slot_faction_diplomacy_war_reason",
        "slot_faction_diplomacy_internal_discontent",
        "slot_faction_diplomacy_lord_war_support",
        "slot_faction_diplomacy_last_incident_day",
        "slot_faction_diplomacy_telemetry_incidents",
        "slot_faction_diplomacy_telemetry_treaty_effects",
        "slot_faction_diplomacy_telemetry_tribute_pressure",
        "slot_faction_diplomacy_telemetry_imperial_coordination",
        "slot_faction_diplomacy_telemetry_discontent_delta",
        "slot_faction_diplomacy_telemetry_support_delta",
        "slot_party_sod_diplomacy_envoy_activity",
        "spt_diplomatic_envoy",
        "sod_diplomacy_temperament_imperial_exception",
        "sod_diplomacy_treaty_anti_imperial_league",
        "sod_diplomacy_treaty_demand_tribute",
        "sod_diplomacy_treaty_non_aggression",
        "sod_diplomacy_treaty_military_access",
        "sod_diplomacy_treaty_defensive_pact",
        "sod_diplomacy_treaty_prisoner_exchange",
        "sod_diplomacy_treaty_anti_slaver_compact",
        "sod_diplomacy_treaty_border_security_pact",
        "sod_diplomacy_memory_broken_truce",
        "sod_diplomacy_memory_slaver_cooperation",
        "sod_diplomacy_memory_released_lord",
        "sod_diplomacy_memory_executed_lord",
        "sod_diplomacy_memory_border_raid",
        "sod_diplomacy_memory_caravan_attack",
        "sod_diplomacy_memory_captive_freed",
        "sod_diplomacy_memory_shared_enemy",
        "sod_diplomacy_war_reason_broken_treaty",
    ):
        assert_contains(constants, token)

    for token in (
        '"sod_diplomacy_initialize"',
        '"sod_diplomacy_update_realm_state"',
        '"sod_diplomacy_update_war_weariness"',
        '"sod_diplomacy_recalculate_policy_effects"',
        '"sod_diplomacy_apply_policy_change"',
        '"sod_diplomacy_apply_decree"',
        '"sod_diplomacy_repeal_decree"',
        "at least three days",
        '"sod_diplomacy_process_decrees"',
        '"sod_diplomacy_apply_memory"',
        '"sod_diplomacy_get_memory_score"',
        '"sod_diplomacy_record_event"',
        '"sod_diplomacy_decay_memories"',
        '"sod_diplomacy_note_war_reason"',
        '"sod_diplomacy_describe_war_reason_to_s39"',
        '"sod_diplomacy_describe_memory_to_s41"',
        '"sod_diplomacy_find_treaty_slot"',
        '"sod_diplomacy_apply_treaty"',
        '"sod_diplomacy_break_treaty"',
        '"sod_diplomacy_expire_treaties"',
        '"sod_diplomacy_describe_treaty_to_s37"',
        '"sod_diplomacy_describe_score_band_to_s48"',
        '"sod_diplomacy_score_treaty"',
        '"sod_diplomacy_spawn_envoy_party"',
        '"sod_diplomacy_process_envoy_parties"',
        '"sod_diplomacy_describe_envoys_to_s46"',
        '"sod_diplomacy_send_envoy"',
        '"sod_diplomacy_resolve_envoy"',
        '"sod_diplomacy_describe_treaties_to_s36"',
        "days remaining",
        '"sod_diplomacy_describe_policy_to_s42"',
        '"sod_diplomacy_describe_decree_to_s45"',
        '"sod_diplomacy_describe_governance_to_s30"',
        '"sod_diplomacy_describe_diplomatic_report_to_s30"',
        '"sod_diplomacy_describe_crisis_report_to_s30"',
        '"sod_diplomacy_ai_consider_treaties"',
        '"sod_diplomacy_process_defensive_pacts_on_war"',
        '"sod_diplomacy_ai_weekly_pulse"',
        '"sod_diplomacy_describe_status_to_s30"',
        '"sod_diplomacy_describe_player_report_to_s30"',
        "fac_kingdom_6",
        "Imperial conquest doctrine",
        "script_diplomacy_start_peace_between_kingdoms",
        "script_sod_slavers_apply_market_delta",
        "slot_faction_black_khergit_pressure",
        "slot_faction_black_army_security_fund",
        "Slaver",
        "Black Khergit",
    ):
        assert_contains(scripts, token)

    player_report_start = scripts.index('("sod_diplomacy_describe_player_report_to_s30"')
    player_report_end = scripts.index('("sod_diplomacy_ai_consider_treaties"', player_report_start)
    player_report_block = scripts[player_report_start:player_report_end]
    assert_contains(player_report_block, '(str_store_string, s29, "@{s30}")')
    assert_contains(player_report_block, "Realm Diplomacy: {s35}^^{s29}^^Active treaties:")
    if "Realm Diplomacy: {s35}^^{s30}^^Active treaties:" in player_report_block:
        raise AssertionError("player diplomacy report must not self-reference s30 in its final Realm Diplomacy string")

    assert_contains(game_start, "script_sod_diplomacy_initialize")
    assert_contains(daily, "script_sod_diplomacy_update_realm_state")
    assert_contains(daily, "script_sod_diplomacy_process_decrees")
    assert_contains(daily, "script_sod_diplomacy_process_envoy_parties")
    assert_contains(scripts, "script_sod_diplomacy_expire_treaties")
    assert_contains(report, "sod_diplomacy_report")
    assert_contains(report, "sod_realm_governance_report")
    assert_contains(report, "sod_diplomatic_report")
    assert_contains(report, "sod_crisis_diplomacy_report")
    assert_contains(report, "script_sod_diplomacy_describe_player_report_to_s30")
    assert_contains(report, "script_sod_diplomacy_describe_governance_to_s30")
    assert_contains(report, "script_sod_diplomacy_describe_diplomatic_report_to_s30")
    assert_contains(report, "script_sod_diplomacy_describe_crisis_report_to_s30")
    assert_contains(report, "sod_diplomacy_envoy_targets")
    assert_contains(report, "sod_diplomacy_envoy_actions")
    assert_contains(report, "sod_diplomacy_policy_management")
    assert_contains(report, "sod_diplomacy_decree_management")
    assert_contains(report, "script_sod_diplomacy_apply_policy_change")
    assert_contains(report, "script_sod_diplomacy_apply_decree")
    assert_contains(report, "script_sod_diplomacy_describe_decree_to_s45")
    assert_contains(report, "script_sod_diplomacy_resolve_envoy")
    assert_contains(report, "script_diplomacy_start_war_between_kingdoms")
    assert_contains(report, "sod_diplomacy_declare_formal_war")
    assert_contains(report, "sod_diplomacy_treaty_trade_accord")
    assert_contains(report, "sod_diplomacy_treaty_anti_imperial_league")
    assert_contains(report, "sod_diplomacy_treaty_demand_tribute")
    assert_contains(report, "sod_diplomacy_demand_tribute")
    assert_contains(report, "sod_diplomacy_treaty_non_aggression")
    assert_contains(report, "sod_diplomacy_treaty_military_access")
    assert_contains(report, "script_sod_diplomacy_describe_score_band_to_s48")
    assert_contains(report, "Military access: {reg8}")
    assert_contains(report, "Anti-Slaver compact: {reg11}")
    assert_contains(report, "sod_diplomacy_treaty_defensive_pact")
    assert_contains(report, "sod_diplomacy_treaty_prisoner_exchange")
    assert_contains(report, "sod_diplomacy_treaty_anti_slaver_compact")
    assert_contains(report, "sod_diplomacy_treaty_border_security_pact")
    assert_contains(report, "slot_faction_diplomacy_policy_military_service")
    assert_contains(report, "slot_faction_diplomacy_policy_justice")
    assert_contains(report, "slot_faction_diplomacy_policy_reconstruction")
    assert_contains(report, "slot_faction_diplomacy_decree_emergency_conscription")
    assert_contains(report, "script_sod_diplomacy_repeal_decree")
    assert_contains(report, "mnu_sod_ai_diplomacy_tuning_report")
    assert_contains(report, "script_sod_diplomacy_describe_ai_tuning_report_to_s30")
    assert_contains(report, "mnu_sod_diplomacy_telemetry_report")
    assert_contains(report, "mnu_sod_diplomacy_notifications")
    assert_contains(report, "script_sod_diplomacy_describe_telemetry_report_to_s30")
    assert_contains(report, "script_sod_diplomacy_normalize_state")
    assert_contains(report, "$g_sod_diplomacy_notification_level")
    assert_contains(reports_menu, "mnu_sod_diplomacy_report")
    assert_contains(notes, "script_sod_diplomacy_describe_status_to_s30")
    assert_contains(war_start, "script_sod_diplomacy_note_war_reason")
    assert_contains(war_start, "script_sod_diplomacy_describe_war_reason_to_s39")
    assert_contains(war_start, "script_sod_diplomacy_break_treaty")
    assert_contains(war_start, "script_sod_diplomacy_process_defensive_pacts_on_war")
    assert_contains(war_start, "sod_diplomacy_memory_broken_truce")
    assert_contains(war_start, "Diplomatic dispatch")
    assert_contains(peace_start, "slot_faction_diplomacy_war_weariness")
    assert_contains(peace_start, "script_sod_diplomacy_find_treaty_slot")
    assert_contains(peace_start, "sod_diplomacy_treaty_truce")
    assert_contains(peace_start, "slot_faction_diplomacy_war_reason_target")
    assert_contains(peace_start, "A truce is expected to hold for {reg39} days")
    assert_contains(peace_start, "Imperial front remains unstable")
    assert_contains(decide_ai, "slot_faction_diplomacy_war_weariness")
    assert_contains(decide_ai, "slot_faction_diplomacy_internal_discontent")
    assert_contains(decide_ai, "slot_faction_diplomacy_lord_war_support")
    assert_contains(choose_war, "slot_faction_diplomacy_war_weariness")
    assert_contains(choose_war, "sod_diplomacy_treaty_non_aggression")
    assert_contains(choose_war, "sod_diplomacy_treaty_defensive_pact")
    assert_contains(choose_war, "script_sod_diplomacy_find_treaty_slot")
    assert_contains(choose_war, "script_sod_diplomacy_note_war_reason")
    assert_contains(choose_war, "sod_diplomacy_war_reason_trade_route_conflict")
    assert_contains(choose_war, "sod_diplomacy_war_reason_conquest")
    assert_contains(choose_war, "sod_diplomacy_war_reason_retaliation")
    assert_contains(propose_peace, "slot_faction_diplomacy_war_weariness")
    assert_contains(propose_peace, "script_sod_diplomacy_score_treaty")
    assert_contains(propose_peace, "sod_diplomacy_treaty_truce")
    assert_contains(propose_peace, "truce_acceptance_score")
    assert_contains(scripts, "script_sod_slavers_apply_market_delta")
    assert_contains(scripts, "slot_faction_black_khergit_pressure")
    assert_contains(slavers, "sod_diplomacy_memory_slaver_cooperation")
    assert_contains(slavers, "sod_diplomacy_memory_anti_slaver_action")
    assert_contains(weekly, "script_sod_diplomacy_ai_weekly_pulse")
    assert_contains(weekly, "script_sod_diplomacy_process_treaty_effects")
    assert_contains(weekly, "script_sod_diplomacy_process_incident_events")
    assert_contains(village_loot, "sod_diplomacy_memory_border_raid")
    assert_contains(total_defeat, "slot_faction_diplomacy_war_weariness")
    assert_contains(total_victory, "slot_faction_diplomacy_war_weariness")
    assert_contains(enemy_hero_resolution, "slot_faction_diplomacy_war_weariness")
    assert_contains(freed_hero, "sod_diplomacy_memory_captive_freed")
    assert_contains(defeated_enemy_party, "sod_diplomacy_memory_caravan_attack")
    assert_contains(defeated_lord_dialog, "sod_diplomacy_memory_released_lord")
    assert_contains(executed_lord_dialog, "sod_diplomacy_memory_executed_lord")
    assert_contains(simulated_battle, "slot_faction_diplomacy_war_weariness")
    assert_contains(scripts, "slot_troop_player_relation")
    assert_contains(scripts, "skl_persuasion")
    assert_contains(scripts, "envoy was insulted")
    assert_contains(scripts, "envoy was detained")
    assert_contains(scripts, "detention risk")
    assert_contains(scripts, "possible")
    assert_contains(scripts, "pt_sod_diplomatic_envoy")
    assert_contains(scripts, "slot_party_sod_diplomacy_envoy_target")
    assert_contains(scripts, "too many envoys")
    assert_contains(scripts, "has vanished from the road")
    assert_contains(scripts, "Active envoys")
    assert_contains(scripts, "Active decrees: War Taxes")
    assert_contains(scripts, "Caravan Protection Charter")
    assert_contains(scripts, "current target: {s21}")
    assert_contains(scripts, "no declared target")
    assert_contains(scripts, "script_sod_report_record_faction_event")
    assert_contains(scripts, "sod_report_reason_realm_treaty")
    assert_contains(scripts, "sod_report_reason_realm_war")
    assert_contains(scripts, "honors its pact")
    assert_contains(scripts, "sod_diplomacy_treaty_defensive_pact")
    assert_contains(scripts, "sod_diplomacy_treaty_border_security_pact")
    assert_contains(scripts, "slot_faction_diplomacy_decree_road_patrol")
    assert_contains(scripts, "slot_faction_diplomacy_decree_anti_slaver")
    assert_contains(scripts, "slot_faction_diplomacy_decree_imperial_defense")
    assert_contains(scripts, "sod_diplomacy_policy_reconstruction_relief")
    assert_contains(scripts, '":ai_faction"')
    assert_contains(scripts, "(le, \":black_khergit_pressure\", 25)")
    assert_contains(scripts, "(le, \":slaver_heat\", 25)")
    assert_contains(scripts, "slot_faction_diplomacy_decree_reconstruction, 0")
    assert_contains(scripts, "slot_faction_black_army_security_fund")
    assert_contains(scripts, "slot_faction_imperial_expedition_supply")
    assert_contains(scripts, "sod_diplomacy_process_treaty_effects")
    assert_contains(scripts, "sod_diplomacy_ai_predatory_tribute_pressure")
    assert_contains(scripts, "sod_diplomacy_describe_ai_tuning_report_to_s30")
    assert_contains(scripts, "sod_diplomacy_process_internal_politics")
    assert_contains(scripts, "sod_diplomacy_apply_marshal_personality_bias")
    assert_contains(scripts, "sod_diplomacy_process_incident_events")
    assert_contains(scripts, "sod_diplomacy_describe_lord_view_to_s30")
    assert_contains(scripts, "sod_diplomacy_describe_telemetry_report_to_s30")
    assert_contains(scripts, "sod_diplomacy_normalize_state")
    assert_contains(scripts, "Notification filter")
    assert_contains(scripts, "the counting-house crown")
    assert_contains(scripts, "the wolf court")
    assert_contains(scripts, "the shuttered realm")
    assert_contains(scripts, "slot_troop_readiness_to_join_army")
    assert_contains(scripts, "slot_troop_morality_penalties")
    assert_contains(scripts, "Diplomatic incident")
    assert_contains(scripts, "Anti-Imperial league coordination strains Imperial supply lines")
    assert_contains(scripts, "has extracted tribute")
    assert_contains(scripts, "rallies toward the threatened front")
    assert_contains(scripts, "Imperial conquest doctrine")
    assert_contains(scripts, "sod_diplomacy_policy_justice_terror")
    assert_contains(scripts, "sod_diplomacy_temperament_predatory")
    assert_contains(scripts, '":source_temperament"')
    assert_contains(scripts, '":peace_threshold"')
    assert_contains(scripts, '":war_appetite_threshold"')
    assert_contains(scripts, "sod_diplomacy_treaty_demand_tribute")
    assert_contains(scripts, "sod_diplomacy_treaty_prisoner_exchange")
    assert_contains(scripts, "Doctrine: protects roads")
    assert_contains(scripts, "Doctrine: hunts exhausted realms")
    assert_contains(scripts, "Doctrine: seals borders")
    assert_contains(scripts, "Doctrine: conquest without normal diplomacy")
    assert_contains(scripts, "at least three days")
    assert_contains(party_templates, '"sod_diplomatic_envoy"')
    assert_contains(black_khergits, "sod_black_khergit_action_bribe_target")
    assert_contains(black_khergits, "sod_diplomacy_memory_border_raid")
    assert_contains(imperial, "script_sod_diplomacy_note_war_reason")
    assert_contains(imperial, "lt, \":enemy_realms\", 3")
    assert_contains(imperial, "script_faction_chose_an_opponent_and_declare_war")
    assert_contains(choose_war, '":temperament"')
    assert_contains(choose_war, '":war_commitment_threshold"')
    assert_contains(choose_war, '":predatory_weariness_bonus"')
    assert_contains(choose_war, "sod_diplomacy_war_reason_trade_route_conflict")
    assert_contains(choose_war, "sod_diplomacy_war_reason_slaver_outrage")
    assert_contains(choose_war, "(ge, \":badboy\", 35)")
    assert_contains(scripts, "(store_div, \":badboy_penalty\", \":badboy\", 3)")
    assert_contains(scripts, "(store_div, \":badboy_fear\", \":badboy\", 6)")
    assert_contains(scripts, "(ge, \":badboy\", 35)")
    assert_contains(badboy_change, "(ge, \":old_badboy\", 24)")
    assert_contains(badboy_change, "(store_div, \":badboy_pressure_bonus\", \":old_badboy\", 20)")
    assert_contains(badboy_change, "(lt, \":badboy_recency_bonus\", 10)")
    assert_contains(badboy_change, "(val_min, \":effective_badboy_change\", 6)")
    assert_contains(badboy_decay, "(val_div, \":badboy_decay\", 18)")
    assert_contains(badboy_decay, "(val_max, \":badboy_decay\", 2)")
    assert_contains(badboy_decay, "(assign, \":badboy_decay\", 10)")
    assert_contains(activate_player_faction, "(val_mul, \":missing_kingdoms\", 2)")
    assert_contains(activate_player_faction, "(val_min, \":total_badboy_effect\", 24)")
    assert_contains(kingdom_hero_ai, "(val_div, \":badboy\", 2)")
    assert_contains(propose_peace, '":peace_commitment_threshold"')
    assert_contains(propose_peace, "sod_diplomacy_temperament_isolationist")
    assert_contains(propose_peace, "sod_diplomacy_temperament_predatory")
    assert_contains(lord_diplomacy_view, "How fares your realm's politics?")
    assert_contains(lord_diplomacy_view, "script_sod_diplomacy_describe_lord_view_to_s30")
    assert_contains(checklist, "Ponavosa Diplomacy System Checklist")

    print("[diplomacy_system_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



