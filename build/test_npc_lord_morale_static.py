# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_constants_exist() -> None:
    raw = read("src/constants/module_constants.py")
    for token in [
        "slot_troop_sod_lord_party_morale",
        "slot_troop_sod_lord_pay_strain",
        "slot_troop_sod_lord_campaign_fatigue",
        "slot_troop_sod_lord_supply_confidence",
        "slot_troop_sod_lord_last_desertion_day",
        "slot_troop_sod_lord_last_battle_refusal_day",
        "slot_troop_sod_lord_last_morale_broken_event_day",
        "slot_troop_sod_lord_last_home_morale_event_day",
        "slot_troop_sod_lord_last_pay_strain_event_day",
        "slot_troop_sod_lord_last_exhaustion_event_day",
        "slot_troop_sod_lord_last_confident_campaign_event_day",
        "slot_troop_sod_lord_strategic_intent",
        "slot_troop_sod_lord_last_intent_day",
        "slot_troop_sod_lord_intent_target",
        "slot_troop_sod_lord_last_dangerous_target",
        "slot_troop_sod_lord_last_failed_siege_day",
        "slot_troop_sod_lord_last_profitable_raid_target",
        "slot_troop_sod_lord_last_profitable_raid_day",
        "slot_faction_sod_lord_morale_pressure",
        "slot_faction_sod_campaign_health",
        "slot_faction_sod_tired_lord_count",
        "slot_faction_sod_unpaid_lord_count",
        "slot_party_sod_morale_snapshot",
        "slot_party_sod_pay_strain_snapshot",
        "slot_party_sod_supply_confidence_snapshot",
        "sod_lord_morale_broken_max",
        "sod_lord_morale_confident_max",
        "sod_lord_intent_recovering",
        "sod_lord_intent_siege_ready",
    ]:
        assert_contains(raw, token)


def test_lord_morale_scripts_exist() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        '"sod_lord_estimate_party_wage"',
        '"sod_lord_get_party_composition_to_regs"',
        '"sod_lord_calculate_pay_strain"',
        '"sod_lord_apply_realm_pay_support"',
        '"sod_lord_calculate_supply_confidence"',
        '"sod_lord_get_campaign_pressure"',
        '"sod_lord_apply_campaign_pressure_to_ai_chances"',
        '"sod_lord_adjust_follow_marshal_chance"',
        '"sod_lord_update_strategic_intent"',
        '"sod_faction_update_campaign_health"',
        '"sod_lord_update_campaign_fatigue"',
        '"sod_lord_update_party_morale"',
        '"sod_lord_update_all_party_morale"',
        '"sod_lord_emit_morale_world_events"',
        '"sod_party_record_lord_battle_outcome"',
        '"sod_lord_try_spawn_deserter_party"',
        '"sod_party_get_lord_morale_context"',
        '"sod_lord_store_morale_report_text"',
        '"sod_lord_get_battle_willingness"',
        '"sod_battle_initialize_morale_context"',
    ]:
        assert_contains(raw, token)


def test_supply_confidence_reads_center_security_profile() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, "script_sod_get_center_security_profile")
    assert_contains(raw, ":supply_center")
    assert_contains(raw, ":recovery_security")
    assert_contains(raw, ":route_security")
    assert_contains(raw, ":contract_security")


def test_daily_update_is_wired() -> None:
    raw = read("src/triggers/ST03_daily/entry_0158.py")
    script_raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, "script_sod_lord_update_all_party_morale")
    assert_contains(script_raw, "script_sod_lord_try_spawn_deserter_party")
    assert_contains(script_raw, "script_sod_lord_emit_morale_world_events")
    assert_contains(script_raw, "script_sod_lord_update_strategic_intent")
    assert_contains(script_raw, "script_sod_lord_apply_realm_pay_support")
    assert_contains(script_raw, "slot_faction_economic_strength")
    assert_contains(script_raw, "slot_faction_sod_lord_morale_pressure")


def test_npc_lord_desertions_spawn_real_parties() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, '"sod_lord_try_spawn_deserter_party"')
    assert_contains(raw, "spawn_around_party")
    assert_contains(raw, '"pt_deserters"')
    assert_contains(raw, "party_clear")
    assert_contains(raw, "party_remove_members")
    assert_contains(raw, "party_add_members")
    assert_contains(raw, "slot_troop_sod_lord_last_desertion_day")
    assert_contains(raw, "slot_troop_sod_lord_pay_strain")
    assert_contains(raw, "slot_troop_sod_lord_campaign_fatigue")
    assert_contains(raw, "slot_troop_sod_lord_supply_confidence")


def test_battle_context_is_wired() -> None:
    raw = read("src/mission_templates/_preamble/00_imports.py")
    script_raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, "script_sod_battle_initialize_morale_context")
    assert_contains(script_raw, "$g_sod_battle_ally_lord_morale")
    assert_contains(script_raw, "$g_sod_battle_ally_supply_confidence")
    assert_contains(script_raw, "$g_sod_battle_enemy_supply_confidence")
    assert_contains(script_raw, "(assign, reg3, \":supply\")")
    assert_contains(raw, "formations_update_morale")
    assert_contains(raw, "formations_update_route")


def test_non_lord_battle_context_has_fallbacks() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, "fac_deserters")
    assert_contains(raw, "fac_outlaws")
    assert_contains(raw, "fac_mountain_bandits")
    assert_contains(raw, "fac_forest_bandits")
    assert_contains(raw, "spt_village_farmer")
    assert_contains(raw, "spt_cattle_herd")
    assert_contains(raw, "spt_ai_mercenaries")
    assert_contains(raw, "spt_kingdom_caravan")
    assert_contains(raw, "slot_party_sod_morale_snapshot")
    assert_contains(raw, "slot_party_sod_supply_confidence_snapshot")


def test_field_special_battles_initialize_morale_context() -> None:
    for path in [
        "src/mission_templates/0005_bandits_at_night/bandits_at_night.py",
        "src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py",
        "src/mission_templates/0012_village_raid/village_raid.py",
        "src/mission_templates/0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py",
    ]:
        raw = read(path)
        assert (
            "script_sod_battle_initialize_morale_context" in raw
            or "common_battle_mission_start" in raw
        ), f"missing morale context initializer in {path}"


def test_sally_battle_uses_morale_and_route_triggers() -> None:
    raw = read("src/mission_templates/0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py")
    assert_contains(raw, "script_sod_battle_initialize_morale_context")
    assert_contains(raw, "formations_start_coherence")
    assert_contains(raw, "formations_update_morale")
    assert_contains(raw, "formations_update_route")


def test_siege_wall_and_inner_battles_use_limited_morale() -> None:
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    assert_contains(preamble, "common_siege_attacker_morale_pressure")
    assert_contains(preamble, "script_flee_allies")
    assert "script_rout_check" not in preamble.split("common_siege_attacker_morale_pressure", 1)[1].split("##########Tactical triggers above", 1)[0]
    for path in [
        "src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py",
        "src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py",
    ]:
        raw = read(path)
        assert_contains(raw, "common_battle_mission_start")
        assert_contains(raw, "formations_start_coherence")
        assert_contains(raw, "common_siege_attacker_morale_pressure")
        assert "formations_update_route" not in raw
    for path in [
        "src/mission_templates/0013_besiege_inner_battle_castle/besiege_inner_battle_castle.py",
        "src/mission_templates/0014_besiege_inner_battle_town_center/besiege_inner_battle_town_center.py",
    ]:
        raw = read(path)
        assert_contains(raw, "script_sod_battle_initialize_morale_context")
        assert_contains(raw, "formations_start_coherence")
        assert "formations_update_route" not in raw


def test_coherence_reads_lord_morale_context() -> None:
    raw = read("src/scripts/ZZ_common_array_processing/coherence.py")
    assert_contains(raw, "$g_sod_battle_ally_lord_morale")
    assert_contains(raw, "$g_sod_battle_enemy_lord_morale")
    assert_contains(raw, "$g_sod_battle_ally_pay_strain")
    assert_contains(raw, "$g_sod_battle_enemy_fatigue")
    assert_contains(raw, "$g_sod_battle_ally_supply_confidence")
    assert_contains(raw, "$g_sod_battle_enemy_supply_confidence")
    assert_contains(raw, ":ally_supply_mod")
    assert_contains(raw, ":enemy_supply_mod")
    assert_contains(raw, "(val_max, \":num_allies\", 1)")
    assert_contains(raw, "(val_max, \":num_enemies\", 1)")


def test_flee_and_rout_read_context() -> None:
    for path, morale_token in [
        ("src/scripts/ZZ_common_array_processing/flee_allies.py", "$g_sod_battle_ally_lord_morale"),
        ("src/scripts/ZZ_common_array_processing/flee_enemies.py", "$g_sod_battle_enemy_lord_morale"),
        ("src/scripts/ZZ_common_array_processing/rout_allies.py", "$g_sod_battle_ally_lord_morale"),
        ("src/scripts/ZZ_common_array_processing/rout_enemies.py", "$g_sod_battle_enemy_lord_morale"),
    ]:
        raw = read(path)
        assert_contains(raw, morale_token)
        assert_contains(raw, "pay_panic")
        assert_contains(raw, "fatigue_panic")
        assert_contains(raw, "wounded_panic")
        assert_contains(raw, "troop_level_resistance")
        assert_contains(raw, "team_get_leader")
        assert_contains(raw, "neg|troop_is_hero")
        assert_contains(raw, "script_sod_troop_is_faith_elite")


def test_rally_respects_morale_and_leadership() -> None:
    raw = read("src/scripts/ZZ_common_array_processing/rally.py")
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    duel = read("src/scripts/ZY_helper_scripts/ponavosa_duel_resolve.py")
    assert_contains(raw, "$g_sod_battle_ally_lord_morale")
    assert_contains(raw, "$g_sod_battle_enemy_lord_morale")
    assert_contains(raw, "$g_sod_battle_ally_duel_momentum")
    assert_contains(raw, "$g_sod_battle_enemy_duel_momentum")
    assert_contains(raw, "skl_leadership")
    assert_contains(raw, "team_get_leader")
    assert_contains(raw, "sod_lord_morale_broken_max")
    assert_contains(raw, "sod_lord_morale_shaken_max")
    assert_contains(raw, ":rally_chance")
    assert_contains(preamble, "$g_sod_battle_ally_duel_momentum")
    assert_contains(duel, "$g_sod_battle_ally_duel_momentum")
    assert_contains(duel, "$g_sod_battle_enemy_duel_momentum")


def test_strategic_ai_uses_lord_morale() -> None:
    raw = read("src/scripts/ZF_factions/free_lords_estimate_their_situation.py")
    decide = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state.py")
    follow = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state_follow_or_not.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, "slot_troop_sod_lord_party_morale")
    assert_contains(raw, "slot_troop_sod_lord_pay_strain")
    assert_contains(raw, "slot_troop_sod_lord_campaign_fatigue")
    assert_contains(raw, "slot_troop_sod_lord_supply_confidence")
    assert_contains(raw, "slot_lord_self_confidence")
    assert_contains(raw, "slot_lord_raiding_factor")
    assert_contains(raw, "slot_troop_readiness_to_join_army")
    assert_contains(raw, ":readiness_bonus")
    assert_contains(raw, "slot_lord_interception_factor")
    assert_contains(raw, ":interception_factor")
    assert_contains(raw, "lrep_quarrelsome")
    assert_contains(raw, "(is_between, \":sod_lord_morale\", 20, 60)")
    assert_contains(raw, "(ge, \":sod_lord_morale\", 80)")
    assert_contains(raw, "lrep_cunning")
    assert_contains(helper, "script_sod_lord_get_battle_willingness")
    assert_contains(helper, "script_sod_lord_get_party_composition_to_regs")
    assert_contains(helper, "sod_doctrine_flag_mercenary")
    assert_contains(helper, "sod_doctrine_flag_noble")
    assert_contains(helper, "sod_doctrine_flag_faith")
    assert_contains(helper, "mercenary_troops_begin")
    assert_contains(helper, ":merc_pay_drag")
    assert_contains(helper, ":noble_defeat_drag")
    assert_contains(helper, ":faith_pay_resist")
    assert_contains(decide, "chance_besiege_enemy_center")
    assert_contains(decide, "chance_move_to_home_center")
    assert_contains(helper, "slot_troop_sod_lord_pay_strain")
    assert_contains(helper, "slot_troop_sod_lord_last_pay_day")
    assert_contains(helper, "lord_realm_pay_support")
    assert_contains(helper, "slot_faction_leader")
    assert_contains(helper, "slot_faction_marshall")
    assert_contains(helper, "slot_faction_economic_strength")
    assert_contains(decide, "script_sod_faction_apply_posture_to_lord_chances")
    assert_contains(helper, "script_sod_lord_apply_campaign_pressure_to_ai_chances")
    assert_contains(decide, "slot_faction_sod_campaign_health")
    assert_contains(decide, "script_sod_faction_update_campaign_health")
    assert_contains(helper, "slot_troop_sod_lord_strategic_intent")
    assert_contains(helper, "slot_troop_sod_lord_last_dangerous_target")
    assert_contains(helper, "slot_troop_sod_lord_last_failed_siege_day")
    assert_contains(helper, "slot_troop_sod_lord_last_profitable_raid_target")
    assert_contains(helper, "slot_faction_sod_campaign_health")
    assert_contains(helper, "slot_faction_sod_tired_lord_count")
    assert_contains(helper, "slot_faction_sod_unpaid_lord_count")
    assert_contains(helper, "lord_strategy_intent")
    assert_contains(helper, "slot_troop_sod_lord_recent_battle_confidence")
    assert_contains(decide, "chance_raid_around_center")
    assert_contains(decide, "chance_patrol_around_center")
    assert_contains(follow, "(ge, reg1, 55)")
    assert_contains(follow, "(ge, reg2, 75)")
    assert_contains(follow, "script_sod_faction_apply_posture_to_follow_chance")
    assert_contains(helper, "script_sod_lord_adjust_follow_marshal_chance")
    assert_contains(follow, "slot_faction_sod_campaign_health")
    assert_contains(follow, "chance_to_follow_other_party")
    assert_contains(raw, "slot_troop_sod_lord_supply_confidence")


def test_battle_outcomes_feed_lord_confidence() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    simulate = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    victory = read("src/scripts/ZC_parties/total_victory_finalize.py")
    assert_contains(helper, '"sod_party_record_lord_battle_outcome"')
    assert_contains(helper, "slot_troop_sod_lord_last_victory_day")
    assert_contains(helper, "slot_troop_sod_lord_last_defeat_day")
    assert_contains(helper, "slot_troop_sod_lord_recent_battle_confidence")
    assert_contains(helper, "lrep_upstanding")
    assert_contains(simulate, "script_sod_party_record_lord_battle_outcome")
    assert_contains(victory, "script_sod_party_record_lord_battle_outcome")


def test_reports_and_notes_expose_lord_morale() -> None:
    readiness = read("src/menus/kingdom/lord_readiness_report.py")
    notes = read("src/scripts/ZH_heroes/update_troop_notes.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(readiness, "script_sod_lord_store_morale_report_text")
    assert_contains(readiness, "script_store_troop_name\", s68")
    assert_contains(readiness, "Battle readiness report for {s68}")
    assert_not_contains(readiness, "@{s2} is a prisoner")
    assert_not_contains(readiness, "@{s2} has no troops")
    assert_contains(notes, "Household morale")
    assert_contains(notes, "script_sod_lord_store_morale_report_text")
    assert_contains(helper, "Morale: {s61}")
    assert_contains(helper, "pay strain")
    assert_contains(helper, "campaign fatigue")


def test_lord_morale_rumors_are_wired() -> None:
    raw = read("src/scripts/ZY_helper_scripts/get_rumor_to_s61.py")
    assert_contains(raw, "slot_troop_sod_lord_party_morale")
    assert_contains(raw, "slot_troop_sod_lord_pay_strain")
    assert_contains(raw, "slot_troop_sod_lord_campaign_fatigue")
    assert_contains(raw, "slot_troop_sod_lord_supply_confidence")
    assert_contains(raw, "slot_troop_sod_lord_last_battle_refusal_day")
    assert_contains(raw, "slot_troop_sod_lord_last_morale_broken_event_day")
    assert_contains(raw, "slot_troop_sod_lord_last_home_morale_event_day")
    assert_contains(raw, "slot_troop_sod_lord_last_pay_strain_event_day")
    assert_contains(raw, "slot_troop_sod_lord_last_exhaustion_event_day")
    assert_contains(raw, "slot_troop_sod_lord_last_confident_campaign_event_day")
    assert_contains(raw, "counting their pay")
    assert_contains(raw, "host is exhausted")
    assert_contains(raw, "refused a fight recently")
    assert_contains(raw, "fed, paid, and marching")


def test_lord_morale_world_event_memory_is_wired() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, '"sod_lord_emit_morale_world_events"')
    assert_contains(raw, "lord_party_morale_broken")
    assert_contains(raw, "lord_returns_home_morale")
    assert_contains(raw, "lord_party_pay_strain")
    assert_contains(raw, "lord_campaign_fatigue")
    assert_contains(raw, "lord_confident_campaign")
    assert_contains(raw, "faction_lord_morale_pressure")
    assert_contains(raw, "slot_troop_sod_lord_last_morale_broken_event_day")
    assert_contains(raw, "slot_troop_sod_lord_last_pay_strain_event_day")
    assert_contains(raw, "slot_faction_sod_lord_morale_pressure")


def test_battle_willingness_helper_scores_core_factors() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, '"sod_lord_get_battle_willingness"')
    assert_contains(raw, "slot_lord_self_confidence")
    assert_contains(raw, "slot_party_cached_strength")
    assert_contains(raw, "sod_lord_morale_broken_max")
    assert_contains(raw, "slot_troop_sod_lord_pay_strain")
    assert_contains(raw, "slot_troop_sod_lord_campaign_fatigue")
    assert_contains(raw, "script_get_closest_center")
    assert_contains(raw, "spai_besieging_center")
    assert_contains(raw, "slot_party_commander_party")
    assert_contains(raw, ":commander_party")
    assert_contains(raw, ":quality_pressure")
    assert_contains(raw, "lrep_cunning")
    assert_contains(raw, "walled_centers_begin")
    assert_contains(raw, "villages_begin")
    assert_contains(raw, "slot_town_lord")
    assert_contains(raw, "try_for_parties")
    assert_contains(raw, "script_party_count_fit_regulars")


def test_debug_displays_cover_coherence_and_rout() -> None:
    coherence = read("src/scripts/ZZ_common_array_processing/coherence.py")
    rout = read("src/scripts/ZZ_common_array_processing/rout_check.py")
    assert_contains(coherence, "Ally/company battle morale context")
    assert_contains(coherence, "Enemy lord morale context")
    assert_contains(rout, "Enemy rout check fired")
    assert_contains(rout, "Ally rout check fired")


def test_player_lord_attack_orders_respect_willingness() -> None:
    party = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_suggest_attack_enemy_party3.py")
    castle = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_suggets_attack_enemy_castle3.py")
    assert_contains(party, "script_sod_lord_get_battle_willingness")
    assert_contains(party, "Not with my men in this state")
    assert_contains(party, "slot_troop_sod_lord_last_battle_refusal_day")
    assert_contains(party, "spai_engaging_army")
    assert_contains(castle, "script_sod_lord_get_battle_willingness")
    assert_contains(castle, "too strained")
    assert_contains(castle, "slot_troop_sod_lord_last_battle_refusal_day")
    assert_contains(castle, "spai_besieging_center")


if __name__ == "__main__":
    test_constants_exist()
    test_lord_morale_scripts_exist()
    test_supply_confidence_reads_center_security_profile()
    test_daily_update_is_wired()
    test_npc_lord_desertions_spawn_real_parties()
    test_battle_context_is_wired()
    test_non_lord_battle_context_has_fallbacks()
    test_field_special_battles_initialize_morale_context()
    test_sally_battle_uses_morale_and_route_triggers()
    test_siege_wall_and_inner_battles_use_limited_morale()
    test_coherence_reads_lord_morale_context()
    test_flee_and_rout_read_context()
    test_rally_respects_morale_and_leadership()
    test_strategic_ai_uses_lord_morale()
    test_battle_outcomes_feed_lord_confidence()
    test_reports_and_notes_expose_lord_morale()
    test_lord_morale_rumors_are_wired()
    test_lord_morale_world_event_memory_is_wired()
    test_battle_willingness_helper_scores_core_factors()
    test_debug_displays_cover_coherence_and_rout()
    test_player_lord_attack_orders_respect_willingness()
    print("test_npc_lord_morale_static: OK")

