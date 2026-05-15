from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_constants_slots_and_trigger_exist() -> None:
    constants = read("src/constants/module_constants.py")
    trigger = read("src/triggers/ST02_every_hour/entry_0168.py")
    design = read("docs/settlements/LOOTER_VILLAGE_RAIDS_DESIGN.md")

    for token in [
        "slot_party_sod_looter_raid_state",
        "slot_party_sod_looter_raid_target",
        "slot_party_sod_looter_raid_start_time",
        "slot_party_sod_looter_raid_last_tick",
        "slot_party_sod_looter_raid_origin_region",
        "slot_party_sod_looter_recently_checked",
        "slot_center_sod_looter_raid_cooldown_until",
        "slot_center_sod_looter_raid_pressure",
        "slot_center_sod_looter_last_raid_day",
        "slot_center_sod_looter_last_defense_day",
        "slot_center_sod_security_pressure",
        "slot_center_sod_looter_player_reward_cooldown_until",
        "sod_looter_raid_state_none",
        "sod_looter_raid_state_moving_to_target",
        "sod_looter_raid_state_plundering",
        "sod_looter_raid_grace_days = 30",
        "sod_looter_raid_min_party_size = 45",
        "sod_looter_raid_global_cap = 1",
        "sod_looter_raid_village_cooldown_days = 14",
        "sod_looter_raid_pressure_stage_low = 35",
        "sod_looter_raid_pressure_stage_mid = 65",
        "sod_looter_raid_pressure_stage_high = 90",
        "sod_looter_raid_player_reward_cooldown_days",
    ]:
        assert_contains(constants, token)

    assert_contains(trigger, "script_sod_process_looter_village_raids")
    assert_contains(design, "Audit source map:")
    assert_contains(design, "only `pt_bandits` counts as looters eligible for village raids")
    assert_contains(design, "Implemented first-pass thresholds:")
    assert_contains(design, "Raid-capable mob: 45 or more troops after campaign day 30.")
    assert_contains(design, "slot_center_sod_looter_player_reward_cooldown_until")
    assert_contains(design, "Implemented constants and slots:")


def test_eligibility_and_target_selection_guardrails() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    pressure_origin = read("src/scripts/ZY_helper_scripts/sod_select_bandit_pressure_origin.py")
    desperation = read("src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py")
    spawn_bandits = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")

    assert_contains(raids, '"cf_sod_looter_party_can_consider_village_raid"')
    assert_contains(raids, '"pt_bandits"')
    assert_contains(raids, "sod_looter_raid_min_party_size")
    assert_contains(raids, "sod_looter_raid_grace_days")
    assert_contains(raids, "slot_party_sod_threat_active_quest")
    assert_contains(raids, "slot_party_ai_state")
    assert_contains(raids, "spai_retreating_to_center")
    assert_contains(raids, "slot_party_retreat_flag")
    assert_contains(raids, "spai_holding_center")
    assert_contains(raids, "spai_patrolling_around_center")
    assert_contains(raids, "spai_raiding_around_center")
    assert_contains(raids, "party_get_battle_opponent")
    assert_contains(raids, "party_get_attached_to")
    assert_contains(raids, "slot_party_sod_looter_recently_checked")

    assert_contains(raids, '"sod_looter_find_village_raid_target"')
    assert_contains(raids, "slot_village_state, 0")
    assert_contains(raids, "slot_village_infested_by_bandits")
    assert_contains(raids, "party_get_num_companions, \":village_defender_count\", \":village_no\"")
    assert_contains(raids, "slot_center_npc_volunteer_troop_amount")
    assert_contains(raids, "gt, \":village_defender_count\", 0")
    assert_contains(raids, "slot_center_sod_looter_raid_cooldown_until")
    assert_contains(raids, "sod_looter_raid_target_radius")
    assert_contains(raids, ":faction_active_raids")
    assert_contains(raids, "sod_looter_raid_global_cap")
    assert_contains(raids, "script_cf_sod_looter_village_has_strong_defender")
    assert_contains(raids, "script_sod_get_center_security_profile")
    assert_contains(raids, ":patrol_response")
    assert_contains(raids, "slot_center_sod_looter_last_raid_day")
    assert_contains(raids, "slot_center_sod_looter_last_defense_day")
    assert_contains(raids, "assign, reg0, \":best_village\"")
    assert_contains(raids, "assign, \":best_village\", -1")
    assert_contains(desperation, "party_clear, \":looter_party\"")
    assert_contains(desperation, "party_add_members, \":looter_party\", \"trp_looter\", \":bandit_count\"")
    assert_contains(desperation, "walled_centers_begin, walled_centers_end")
    assert_contains(spawn_bandits, ":spawned_from_village")
    assert_contains(spawn_bandits, "party_clear, \":spawned_party_id\"")
    assert_contains(spawn_bandits, "party_add_members, \":spawned_party_id\", \"trp_looter\", \":population_loss\"")
    assert_contains(spawn_bandits, "pt_bandit_reinfocements")

    design = read("docs/settlements/LOOTER_VILLAGE_RAIDS_DESIGN.md")
    assert_contains(design, "- [x] Add `script_cf_sod_looter_party_can_consider_village_raid`.")
    assert_contains(design, "- [x] Add `script_sod_looter_find_village_raid_target`.")
    assert_contains(design, "Parties retreating to a center")
    assert_contains(design, "active looter raids against the same target faction")


def test_assignment_tick_and_resolution_are_separate_from_lord_raids() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    patrol_target = read("src/scripts/ZY_helper_scripts/sod_find_castle_patrol_threat_target.py")

    assert_contains(raids, '"sod_looter_assign_village_raid"')
    assert_contains(raids, "slot_party_sod_looter_raid_state")
    assert_contains(raids, "slot_party_sod_looter_raid_target")
    assert_contains(raids, "ai_bhvr_travel_to_party")
    assert_contains(raids, "val_add, \"$g_sod_active_looter_raids\"")
    assert_contains(raids, "gt, \"$g_sod_active_looter_raids\", sod_looter_raid_global_cap")
    assert_contains(raids, "party_get_template_id, \":party_template\", \":looter_party\"")
    assert_contains(raids, "eq, \":party_template\", \"pt_bandits\"")
    assert_contains(raids, "party_get_num_companions, \":village_defender_count\", \":target_village\"")
    assert_contains(raids, "gt, \":village_defender_count\", 0")
    assert_contains(raids, "neq, \":party_type\", spt_kingdom_hero_party")
    assert_contains(raids, "neq, \":party_type\", spt_player_patrol")
    assert_contains(raids, "neq, \":party_type\", spt_player_mercenaries")
    assert_contains(raids, "slot_party_sod_threat_active_quest")
    assert_contains(raids, "slot_party_retreat_flag")

    assert_contains(raids, '"sod_looter_raid_tick"')
    assert_contains(raids, "sod_looter_raid_state_plundering")
    assert_contains(raids, "slot_center_sod_looter_raid_pressure")
    assert_contains(raids, "sod_looter_raid_success_pressure")
    assert_contains(raids, "script_sod_looter_resolve_village_raid")
    assert_contains(raids, "sod_looter_raid_pressure_stage_low")
    assert_contains(raids, "sod_looter_raid_pressure_stage_mid")
    assert_contains(raids, "sod_looter_raid_pressure_stage_high")
    assert_contains(raids, "script_sod_get_center_food_profile")
    assert_contains(raids, "script_sod_center_apply_food_delta")
    assert_contains(raids, "store_mul, \":food_loss\", \":stage_damage\", 18")
    assert_contains(raids, "slot_center_volunteer_troop_amount")
    assert_contains(raids, "script_sod_center_apply_local_prosperity_delta")

    assert_contains(raids, '"sod_looter_resolve_village_raid"')
    assert_contains(raids, "slot_town_prosperity")
    assert_contains(raids, "script_sod_center_apply_local_prosperity_delta")
    assert_contains(raids, "slot_center_volunteer_troop_amount")
    assert_contains(raids, "slot_center_sod_security_pressure")
    assert_contains(raids, "sod_looter_raid_defense_cooldown_days")
    assert_contains(raids, ":scatter_roll")
    assert_contains(raids, ":extra_scatter_losses")
    assert_contains(raids, "val_sub, \":security_pressure\", 4")
    assert_contains(raids, "val_add, \":security_pressure\", 2")
    assert_contains(raids, "slot_party_sod_looter_raid_state, sod_looter_raid_state_none")
    assert_not_contains(raids, "script_village_set_state")
    assert_not_contains(raids, "svs_looted")

    assert_contains(raids, '"sod_looter_raid_call_nearby_defenders"')
    assert_contains(raids, "spt_kingdom_hero_party")
    assert_contains(raids, "spt_player_patrol")
    assert_contains(raids, ":can_redirect_patrol")
    assert_contains(raids, "slot_party_sod_patrol_origin_castle")
    assert_contains(raids, "slot_party_sod_patrol_radius")
    assert_contains(raids, "gt, \":patrol_origin\", 0")
    assert_contains(raids, "spai_engaging_army")
    assert_contains(raids, "slot_party_sod_support_target")
    assert_contains(raids, ":militia_roll")
    assert_contains(raids, ":militia_chance")
    assert_contains(patrol_target, "slot_party_sod_looter_raid_state")
    assert_contains(patrol_target, "sod_looter_raid_state_moving_to_target")
    assert_contains(patrol_target, "val_sub, \":score\", 45")

    assert_contains(raids, '"sod_looter_raid_repair_state"')
    assert_contains(raids, "script_sod_looter_raid_repair_state")
    assert_contains(raids, '"sod_looter_raid_decay_village_pressure"')
    assert_contains(raids, "script_sod_looter_raid_decay_village_pressure")
    assert_contains(raids, "slot_center_sod_security_pressure")
    assert_contains(raids, "val_clamp, \":pressure\", 0, 121")
    assert_contains(raids, "val_clamp, \":security_pressure\", 0, 101")
    assert_contains(raids, "assign, \":pressure_gain\", 12")
    assert_contains(raids, "assign, \":raid_resistance\", reg3")

    design = read("docs/settlements/LOOTER_VILLAGE_RAIDS_DESIGN.md")
    assert_contains(design, "- [x] Add `script_sod_looter_assign_village_raid`.")
    assert_contains(design, "- [x] Add `script_sod_looter_raid_tick`.")
    assert_contains(design, "- [x] Add `script_sod_looter_resolve_village_raid`.")
    assert_contains(design, "- [x] Let player-owned external patrols respond if their patrol radius includes the village.")
    assert_contains(design, "Only `pt_bandits` in an idle looter-compatible AI state can be assigned.")
    assert_contains(design, "Crossing pressure stages damages the village gradually")
    assert_contains(design, "Player mercenary follower companies are not automatically redirected")


def test_player_interruption_and_elder_feedback_exist() -> None:
    defeated = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    autoresolve = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    order = read("src/dialogs/_order_dialogs.txt")
    elder_option = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_looter_pressure.py")
    elder_reply = read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_looter_pressure.py")
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    design = read("docs/settlements/LOOTER_VILLAGE_RAIDS_DESIGN.md")

    assert_contains(defeated, "slot_party_sod_looter_raid_state")
    assert_contains(defeated, "script_sod_looter_resolve_village_raid")
    assert_contains(defeated, "script_change_player_relation_with_center")
    assert_contains(defeated, "script_change_troop_renown")
    assert_contains(defeated, "script_change_player_honor")
    assert_contains(defeated, "sod_companion_action_help_village")
    assert_contains(defeated, "sod_companion_action_safe_roadcraft")
    assert_contains(defeated, "sod_companion_action_food_security")
    assert_contains(defeated, "sod_companion_action_build_security")
    assert_contains(defeated, "sod_companion_action_orderly_profit")
    assert_contains(defeated, "Ymira watches the village road")
    assert_contains(defeated, "Bunduk counts the scattered looters")
    assert_contains(defeated, "Marnid looks toward the grain carts")
    assert_contains(defeated, "slot_center_sod_looter_player_reward_cooldown_until")
    assert_contains(defeated, "sod_looter_raid_player_reward_cooldown_days")
    assert_contains(defeated, "assign, \":reward_allowed\", 0")

    assert_contains(order, "anyone_plyr_village_elder_looter_pressure.py")
    assert_contains(order, "anyone_village_elder_looter_pressure.py")
    assert_contains(elder_option, "slot_center_sod_looter_raid_pressure")
    assert_contains(elder_option, ":recent_window")
    assert_contains(elder_option, ":raid_age")
    assert_contains(elder_option, ":defense_age")
    assert_contains(elder_reply, "Not a lord's raid")
    assert_contains(elder_reply, "outer farms")
    assert_contains(elder_reply, ":recent_window")
    assert_contains(elder_reply, ":raid_age")
    assert_contains(elder_reply, ":defense_age")

    assert_contains(raids, "neg|party_slot_eq, \":target_village\", slot_village_state, 0")
    assert_contains(raids, "assign, \":result\", 0")
    assert_contains(raids, "lt, \":raid_state\", sod_looter_raid_state_plundering")
    assert_contains(raids, "le, \":village_defender_count\", 0")
    assert_contains(raids, "slot_center_is_besieged_by")
    assert_contains(raids, "slot_party_sod_looter_raid_origin_region")
    assert_contains(raids, "neq, \":current_faction\", \":original_faction\"")
    assert_contains(raids, "neq, \":target_faction\", \":original_faction\"")
    assert_contains(raids, "party_get_slot, \":stale_target\"")
    assert_contains(raids, "party_set_slot, \":party_no\", slot_party_sod_looter_raid_target, -1")
    assert_contains(raids, "call_script, \"script_sod_looter_resolve_village_raid\", \":party_no\", 0")
    assert_contains(raids, "script_sod_get_center_food_profile")
    assert_contains(raids, "script_sod_center_apply_food_delta")
    assert_contains(raids, "script_change_center_prosperity")
    assert_contains(raids, "script_sod_center_apply_local_prosperity_delta")
    assert_contains(raids, "val_sub, \":volunteers\", 2")
    assert_contains(raids, "val_add, \":security_pressure\", 12")
    assert_not_contains(raids, "party_add_members, \"p_main_party\"")
    assert_not_contains(raids, "party_add_prisoners")

    assert_contains(autoresolve, "slot_party_sod_looter_raid_state")
    assert_contains(autoresolve, "script_sod_looter_resolve_village_raid")
    assert_contains(autoresolve, "script_clear_party_group")

    assert_contains(design, "- [x] Add companion comment hooks for mercy, discipline, trade, and security personalities.")
    assert_contains(design, "- [x] Prevent looter raids from stacking too much with war raids.")
    assert_contains(design, "- [x] Looter target village becomes looted by a lord before looters arrive.")
    assert_contains(design, "- [x] Prevent active raid hosts from ignoring battle outcomes.")
    assert_contains(design, "Player interruption resolves as defense, grants a small village relation, renown, and honor reward")
    assert_contains(design, "If a village enters a non-normal state from war or another system before resolution")
    assert_contains(design, "Save/load repair clears stale old-save slots")
    assert_contains(design, "never add troops, prisoners, loot, or recruits")


if __name__ == "__main__":
    test_constants_slots_and_trigger_exist()
    test_eligibility_and_target_selection_guardrails()
    test_assignment_tick_and_resolution_are_separate_from_lord_raids()
    test_player_interruption_and_elder_feedback_exist()
    print("test_looter_village_raids_static: OK")
