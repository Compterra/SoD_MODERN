# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_campaign_director_constants_exist() -> None:
    raw = read("src/constants/module_constants.py")
    for token in [
        "slot_faction_sod_campaign_posture",
        "slot_faction_sod_campaign_posture_target",
        "slot_faction_sod_campaign_posture_day",
        "slot_faction_sod_campaign_posture_confidence",
        "slot_faction_sod_campaign_posture_reason",
        "slot_faction_sod_marshal_planning_score",
        "slot_faction_sod_marshal_coordination_score",
        "slot_faction_sod_marshal_logistics_score",
        "slot_faction_sod_marshal_aggression_score",
        "slot_faction_sod_marshal_caution_score",
        "slot_faction_sod_last_failed_siege_target",
        "slot_faction_sod_last_failed_siege_day",
        "slot_faction_sod_failed_siege_avoidance",
        "slot_faction_sod_marshal_current_followers",
        "slot_faction_sod_marshal_desired_followers",
        "slot_faction_sod_marshal_offensive_readiness",
        "sod_campaign_posture_offensive_siege",
        "sod_campaign_posture_defensive_rally",
        "sod_campaign_posture_recovery",
        "sod_campaign_posture_raiding",
        "sod_campaign_posture_hunting",
        "sod_campaign_posture_border_patrol",
        "sod_campaign_posture_gathering",
        "sod_campaign_reason_threatened_center",
        "sod_campaign_reason_low_health",
        "sod_campaign_reason_marshal_opportunity",
    ]:
        assert_contains(raw, token)


def test_campaign_director_helpers_exist() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        '"sod_marshal_get_planning_profile_to_regs"',
        '"sod_faction_update_campaign_posture"',
        '"sod_faction_get_posture_target_score"',
        '"sod_faction_should_hold_posture"',
        '"sod_faction_apply_posture_to_ai_thresholds"',
        '"sod_faction_apply_posture_to_lord_chances"',
        '"sod_faction_apply_posture_to_follow_chance"',
        '"sod_faction_describe_campaign_posture_to_s31"',
        "skl_tactics",
        "skl_leadership",
        "skl_trainer",
        "skl_pathfinding",
        "skl_spotting",
        "skl_tracking",
        "slot_lord_self_confidence",
        "slot_lord_initiative",
        "faction_campaign_posture",
        "slot_faction_sod_campaign_health",
        "slot_faction_sod_tired_lord_count",
        "slot_faction_sod_unpaid_lord_count",
        "Campaign director",
        "Target:",
        "Reason:",
        "Marshal profile",
        "failed-siege avoidance",
        "sod_campaign_reason_recent_failed_siege",
    ]:
        assert_contains(raw, token)


def test_faction_ai_uses_campaign_posture() -> None:
    raw = read("src/scripts/ZF_factions/decide_faction_ai.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, "script_sod_faction_update_campaign_posture")
    assert_contains(raw, "script_sod_faction_apply_posture_to_ai_thresholds")
    assert_contains(helper, "sod_campaign_posture_recovery")
    assert_contains(helper, "sod_campaign_posture_defensive_rally")
    assert_contains(helper, "sod_campaign_posture_offensive_siege")
    assert_contains(helper, "sod_campaign_posture_hunting")
    assert_contains(raw, ":sod_posture_confidence")
    assert_contains(raw, ":war_threshold")
    assert_contains(raw, ":peace_threshold")


def test_marshal_context_stores_planning_profile() -> None:
    raw = read("src/scripts/ZF_factions/decide_faction_ai_collect_marshall_context.py")
    assert_contains(raw, "script_sod_marshal_get_planning_profile_to_regs")
    assert_contains(raw, "slot_faction_sod_marshal_planning_score")
    assert_contains(raw, "slot_faction_sod_marshal_coordination_score")
    assert_contains(raw, "slot_faction_sod_marshal_logistics_score")
    assert_contains(raw, "slot_faction_sod_marshal_current_followers")
    assert_contains(raw, "slot_faction_sod_marshal_desired_followers")
    assert_contains(raw, "slot_faction_sod_marshal_offensive_readiness")
    assert_contains(raw, ":coordination_bonus")
    assert_contains(raw, ":offensive_rating_bonus")


def test_lord_ai_and_follow_read_posture() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    world = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state.py")
    follow = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state_follow_or_not.py")
    assert_contains(raw, "slot_faction_sod_campaign_posture")
    assert_contains(raw, "sod_campaign_posture_recovery")
    assert_contains(raw, "sod_campaign_posture_raiding")
    assert_contains(raw, "sod_campaign_posture_hunting")
    assert_contains(raw, "sod_campaign_posture_gathering")
    assert_contains(raw, "slot_faction_sod_marshal_coordination_score")
    assert_contains(raw, ":chance_to_follow")
    assert_contains(raw, ":chance_besiege")
    assert_contains(raw, ":chance_raid")
    assert_contains(raw, ":chance_patrol")
    assert_contains(world, "script_sod_faction_apply_posture_to_lord_chances")
    assert_contains(follow, "script_sod_faction_apply_posture_to_follow_chance")


def test_faction_notes_show_campaign_director() -> None:
    raw = read("src/scripts/ZF_factions/update_faction_notes.py")
    assert_contains(raw, "script_sod_faction_describe_campaign_posture_to_s31")
    assert_contains(raw, "add_faction_note_from_sreg")
    assert_contains(raw, "s31")


def test_failed_siege_memory_shapes_objectives() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    objective = read("src/scripts/ZF_factions/set_faction_offensive_objective.py")
    assert_contains(helper, "slot_faction_sod_last_failed_siege_target")
    assert_contains(helper, "slot_faction_sod_last_failed_siege_day")
    assert_contains(helper, "slot_faction_sod_failed_siege_avoidance")
    assert_contains(helper, "sod_campaign_reason_recent_failed_siege")
    assert_contains(objective, "script_sod_faction_get_posture_target_score")
    assert_contains(objective, ":failed_siege_avoidance")
    assert_contains(objective, ":avoidance_penalty")


def test_marshal_logistics_shapes_campaign_fatigue() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(raw, '"sod_lord_update_campaign_fatigue"')
    assert_contains(raw, ":following_marshal")
    assert_contains(raw, ":marshal_logistics")
    assert_contains(raw, "slot_faction_sod_marshal_logistics_score")
    assert_contains(raw, "slot_party_commander_party")


def test_marshal_planning_tiers_shape_posture() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        ":recovery_health_threshold",
        ":recovery_tired_threshold",
        ":siege_health_threshold",
        ":siege_coordination_threshold",
        ":hunting_opportunity_threshold",
        ":gathering_coordination_threshold",
        ":failed_siege_avoidance_threshold",
        "slot_faction_ai_state",
        "sfai_attacking_center",
        "sfai_raiding_village",
        "sfai_attacking_enemy_army",
        "sfai_gathering_army",
    ]:
        assert_contains(raw, token)


def test_marshal_context_is_called_before_posture() -> None:
    raw = read("src/scripts/ZF_factions/decide_faction_ai.py")
    context_index = raw.index("script_decide_faction_ai_collect_marshall_context")
    posture_index = raw.index("script_sod_faction_update_campaign_posture")
    assert context_index < posture_index
    assert_contains(raw, "slot_faction_ambition")


def test_posture_hysteresis_uses_shared_helper() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    update_start = raw.index('("sod_faction_update_campaign_posture"')
    hold_start = raw.index('("sod_faction_should_hold_posture"')
    update_body = raw[update_start:hold_start]
    hold_body = raw[hold_start:raw.index('("sod_faction_apply_posture_to_ai_thresholds"')]
    assert_contains(update_body, "script_sod_faction_should_hold_posture")
    assert_contains(update_body, ":hold_posture")
    assert_contains(hold_body, ":center_threat")
    assert_contains(hold_body, ":campaign_health")
    assert_contains(hold_body, "lt, \":center_threat\", 3")
    assert_contains(hold_body, "lt, \":campaign_health\", 85")
    assert_contains(hold_body, "gt, \":campaign_health\", 20")


def test_posture_requires_followers_for_siege() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        ":marshal_followers",
        ":desired_followers",
        ":offensive_readiness",
        "Followers {reg50}/{reg51}",
        "readiness {reg52}",
    ]:
        assert_contains(raw, token)


def test_defensive_rally_scores_threatened_centers() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        ":best_defense_score",
        ":defense_score",
        "script_get_center_relative_value",
        ":value_score",
        ":defensive_objective",
        "sod_campaign_posture_defensive_rally",
    ]:
        assert_contains(raw, token)


def test_defensive_rally_biases_local_lord_behavior() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        ":posture_target",
        "slot_faction_sod_campaign_posture_target",
        ":target_home",
        ":home_center",
        "slot_troop_home",
        ":target_distance",
        "store_distance_to_party_from_party",
    ]:
        assert_contains(raw, token)


def test_recovery_posture_sheds_exhausted_followers() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        "lord_recovery_detach",
        "party_set_slot, \":party_no\", slot_party_commander_party, -1",
        "slot_faction_sod_campaign_posture, sod_campaign_posture_recovery",
        ":following_marshal",
        "val_div, \":chance_besiege\", 8",
        "val_mul, \":chance_home\", 3",
    ]:
        assert_contains(raw, token)


def test_raiding_posture_uses_marshal_style_and_target_value() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    lord_ai = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state.py")
    for token in [
        ":sod_campaign_posture",
        ":sod_marshal_planning",
        ":sod_marshal_aggression",
        ":value_bonus",
        ":deep_raid_penalty",
        ":deep_raid_bonus",
    ]:
        assert_contains(lord_ai, token)
    for token in [
        "ge, \":aggression\", 65",
        "lt, \":economic_strength\", 130",
        "sod_campaign_posture_raiding",
        "val_div, \":chance_raid\", 2",
    ]:
        assert_contains(helper, token)


def test_border_and_recovery_postures_improve_local_supply() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    for token in [
        '"sod_lord_calculate_supply_confidence"',
        ":sod_posture",
        ":near_friendly_center",
        "sod_campaign_posture_recovery",
        "sod_campaign_posture_border_patrol",
        "slot_faction_sod_campaign_posture",
    ]:
        assert_contains(raw, token)


def test_mobile_support_parties_are_strength_cached() -> None:
    raw = read("src/scripts/ZI_campaign_ai/init_ai_calculation.py")
    party_loop = raw[raw.index("(try_for_parties, \":party_no\")"):raw.index("(try_for_range, \":cur_troop\"")]
    assert_contains(party_loop, "(party_is_active, \":party_no\")")
    for token in [
        "spt_ai_mercenaries",
        "spt_player_mercenaries",
        "spt_kingdom_caravan",
        "spt_player_patrol",
    ]:
        assert_contains(party_loop, token)
    assert party_loop.count("spt_kingdom_caravan") == 1, "kingdom caravan should not duplicate the final party-type condition"
    assert "(this_or_next|party_slot_eq, \":party_no\", slot_party_type, spt_player_patrol)" not in party_loop
    assert_contains(party_loop, "(party_slot_eq, \":party_no\", slot_party_type, spt_player_patrol)")

    hero_loop = raw[raw.index("(try_for_range, \":cur_troop\", heroes_begin, heroes_end)"):raw.index("(try_for_range, \":cur_center\"")]
    assert_contains(hero_loop, "(party_is_active, \":cur_troop_party\")")
    assert hero_loop.index("(party_is_active, \":cur_troop_party\")") < hero_loop.index('(call_script, "script_party_calculate_strength", ":cur_troop_party", 0)')

    center_loop = raw[raw.index("(try_for_range, \":cur_center\", walled_centers_begin, walled_centers_end)"):]
    center_loop = center_loop[:center_loop.index('(assign, "$g_calculating_ais", 0)')]
    assert_contains(center_loop, "(party_is_active, \":cur_center\")")
    assert center_loop.index("(party_is_active, \":cur_center\")") < center_loop.index('(call_script, "script_party_calculate_strength", ":cur_center", 0)')


if __name__ == "__main__":
    test_campaign_director_constants_exist()
    test_campaign_director_helpers_exist()
    test_faction_ai_uses_campaign_posture()
    test_marshal_context_stores_planning_profile()
    test_lord_ai_and_follow_read_posture()
    test_faction_notes_show_campaign_director()
    test_failed_siege_memory_shapes_objectives()
    test_marshal_logistics_shapes_campaign_fatigue()
    test_marshal_planning_tiers_shape_posture()
    test_marshal_context_is_called_before_posture()
    test_posture_hysteresis_uses_shared_helper()
    test_posture_requires_followers_for_siege()
    test_defensive_rally_scores_threatened_centers()
    test_defensive_rally_biases_local_lord_behavior()
    test_recovery_posture_sheds_exhausted_followers()
    test_raiding_posture_uses_marshal_style_and_target_value()
    test_border_and_recovery_postures_improve_local_supply()
    test_mobile_support_parties_are_strength_cached()
    print("test_faction_campaign_director_static: OK")
