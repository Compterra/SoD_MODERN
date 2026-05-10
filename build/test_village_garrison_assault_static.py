from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_assault_constants_slots_and_design_are_pinned() -> None:
    constants = read("src/constants/module_constants.py")
    checklist = read("docs/settlements/VILLAGE_GARRISON_ASSAULT_CHECKLIST.md")

    for token in [
        "slot_party_sod_looter_raid_assault_resolved",
        "slot_center_sod_looter_last_assault_day",
        "slot_center_sod_looter_last_assault_result",
        "slot_center_sod_looter_garrison_losses_recent",
        "slot_center_sod_looter_militia_losses_recent",
        "sod_looter_raid_state_assaulting",
        "sod_village_assault_result_defender_rout",
        "sod_village_assault_result_defender_hold",
        "sod_village_assault_result_raider_costly",
        "sod_village_assault_result_raider_clean",
        "sod_village_assault_result_raider_overwhelming",
    ]:
        assert_contains(constants, token)

    assert_contains(checklist, "### Edge Cases")
    assert_contains(checklist, "- [x] Save/load occurs after arrival but before assault resolution.")
    assert_contains(checklist, "- [x] Existing village raid state `svs_being_raided` overlaps with looter raid pressure.")


def test_assault_resolution_uses_real_village_defenders() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")

    assert_contains(raids, '"sod_looter_resolve_village_garrison_assault"')
    assert_contains(raids, "party_get_template_id, \":party_template\", \":looter_party\"")
    assert_contains(raids, "eq, \":party_template\", \"pt_bandits\"")
    assert_contains(raids, "party_slot_eq, \":target_village\", slot_party_type, spt_village")
    assert_contains(raids, "party_slot_eq, \":target_village\", slot_village_state, 0")
    assert_contains(raids, "slot_party_sod_looter_raid_origin_region")
    assert_contains(raids, "neq, \":current_faction\", \":original_faction\"")
    assert_contains(raids, "party_get_num_companions, \":village_garrison\", \":target_village\"")
    assert_contains(raids, "slot_center_npc_volunteer_troop_amount")
    assert_contains(raids, "script_sod_get_center_security_profile")
    assert_contains(raids, "script_sod_get_center_garrison_policy")
    assert_contains(raids, "sod_center_modifier_health_recovery_flat")
    assert_contains(raids, "script_sod_get_center_food_profile")
    assert_contains(raids, ":garrison_recovery")
    assert_contains(raids, ":food_security")
    assert_contains(raids, ":health_recovery")
    assert_contains(raids, "slot_center_sod_looter_garrison_losses_recent")
    assert_contains(raids, "slot_center_sod_looter_militia_losses_recent")
    assert_contains(raids, "assign, reg0, \":result\"")
    assert_not_contains(raids, "party_get_num_companions, \":village_garrison\", \"p_main_party\"")


def test_assault_losses_are_safe_and_non_duplicate() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")

    assert_contains(raids, '"sod_apply_village_garrison_assault_losses"')
    assert_contains(raids, "neg|party_slot_ge, \":looter_party\", slot_party_sod_looter_raid_assault_resolved, 1")
    assert_contains(raids, "party_set_slot, \":looter_party\", slot_party_sod_looter_raid_assault_resolved, 1")
    assert_contains(raids, "neg|troop_is_hero, \":stack_troop\"")
    assert_contains(raids, "party_remove_members, \":target_village\", \":selected_troop\", \":take\"")
    assert_contains(raids, "party_remove_members, \":looter_party\", \":selected_troop\", \":take\"")
    assert_contains(raids, "val_min, \":actual_militia_losses\", \":current_militia\"")
    assert_contains(raids, "val_max, \":new_militia\", 0")
    assert_contains(raids, "lt, \":post_looter_size\", 25")
    assert_contains(raids, "script_sod_looter_resolve_village_raid\", \":looter_party\", 2")
    assert_not_contains(raids, "party_remove_members, \":target_village\", \"trp_player\"")


def test_raid_tick_has_assault_state_recovery_and_no_direct_plunder_skip() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")

    assert_contains(raids, '"sod_looter_raid_tick"')
    assert_contains(raids, "eq, \":raid_state\", sod_looter_raid_state_assaulting")
    assert_contains(raids, "party_get_slot, \":assault_resolved\", \":looter_party\", slot_party_sod_looter_raid_assault_resolved")
    assert_contains(raids, "party_get_slot, \":assault_result\", \":target_village\", slot_center_sod_looter_last_assault_result")
    assert_contains(raids, "script_sod_looter_resolve_village_garrison_assault")
    assert_contains(raids, "script_sod_apply_village_garrison_assault_losses")
    assert_contains(raids, "sod_village_assault_result_defender_hold")
    assert_contains(raids, "sod_village_assault_result_raider_costly")
    assert_contains(raids, "slot_party_sod_looter_raid_state, sod_looter_raid_state_plundering")
    assert_contains(raids, "party_set_ai_behavior, \":looter_party\", ai_bhvr_patrol_location")
    assert_contains(raids, "neg|party_slot_eq, \":target_village\", slot_village_state, 0")
    assert_contains(raids, "slot_center_is_besieged_by")
    assert_contains(raids, "neq, \":current_faction\", \":original_faction\"")

    moving_branch = raids[raids.index("(eq, \":raid_state\", sod_looter_raid_state_moving_to_target)") :]
    moving_branch = moving_branch[: moving_branch.index("(else_try),\n      (eq, \":raid_state\", sod_looter_raid_state_plundering)")]
    assert_contains(moving_branch, "script_sod_looter_resolve_village_garrison_assault")
    assert_contains(moving_branch, "script_sod_apply_village_garrison_assault_losses")
    assert_contains(moving_branch, "slot_party_sod_looter_raid_state, sod_looter_raid_state_assaulting")
    assert_contains(moving_branch, "slot_party_sod_looter_raid_state, sod_looter_raid_state_plundering")


def test_battle_interruption_repair_and_reports_cover_edge_cases() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    defeated = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    autoresolve = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    total_defeat = read("src/menus/other/total_defeat.py")
    elder_reply = read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_looter_pressure.py")

    assert_contains(raids, '"sod_looter_handle_player_defeat_near_village_raid"')
    assert_contains(raids, "party_slot_eq, \":target_village\", slot_party_type, spt_village")
    assert_contains(raids, "party_slot_eq, \":target_village\", slot_village_state, 0")
    assert_contains(raids, "lt, \":besieged_by\", 0")
    assert_contains(raids, "eq, \":faction_ok\", 1")
    assert_contains(raids, '"sod_looter_raid_repair_state"')
    assert_contains(raids, "party_set_slot, \":party_no\", slot_party_sod_looter_raid_assault_resolved, 0")
    assert_contains(raids, "neg|party_slot_eq, \":target_village\", slot_party_type, spt_village")
    assert_contains(raids, "neg|party_slot_eq, \":target_village\", slot_village_state, 0")
    assert_contains(raids, "script_sod_looter_resolve_village_raid\", \":party_no\", 0")

    assert_contains(defeated, "slot_party_sod_looter_raid_assault_resolved")
    assert_contains(defeated, "saved before blood reached the lanes")
    assert_contains(defeated, "had already paid for the first assault")
    assert_contains(defeated, "script_sod_looter_resolve_village_raid")
    assert_contains(autoresolve, "slot_party_sod_looter_raid_state")
    assert_contains(autoresolve, "script_sod_looter_resolve_village_raid")
    assert_contains(total_defeat, "script_sod_looter_handle_player_defeat_near_village_raid")
    assert_contains(elder_reply, "The watch was raised in time")
    assert_contains(elder_reply, "There are fresh graves by the road")


def test_militia_armory_is_subtle_and_can_be_stolen() -> None:
    constants = read("src/constants/module_constants.py")
    registry = read("src/constants/building_registry.py")
    validation = read("src/scripts/ZI_campaign_ai/validate_construction_choice.py")
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    checklist = read("docs/settlements/VILLAGE_GARRISON_ASSAULT_CHECKLIST.md")

    assert_contains(constants, "slot_center_has_militia_armory")
    assert_contains(registry, "militia_armory")
    assert_contains(registry, "prerequisite_any_buildings=(slot_center_has_rustic_blacksmith, slot_center_has_manor)")
    assert_contains(registry, '"recruit_tier_bonus_flat", 1, "militia_armory_levy_gear"')
    assert_contains(registry, '"security_flat", 5, "militia_armory_stored_arms"')
    assert_contains(validation, "prerequisite_any_buildings")
    assert_contains(validation, ":any_prereq_ok")

    assert_contains(raids, "slot_center_has_militia_armory")
    assert_contains(raids, ":armory_theft_roll")
    assert_contains(raids, "sod_village_assault_result_raider_clean")
    assert_contains(raids, "sod_village_assault_result_raider_overwhelming")
    assert_contains(raids, "stolen arms may embolden local bandits for a time")
    assert_contains(checklist, "**Militia Armory:** local arms store.")
    assert_contains(checklist, "Requires Rustic Blacksmith or Manor.")


if __name__ == "__main__":
    test_assault_constants_slots_and_design_are_pinned()
    test_assault_resolution_uses_real_village_defenders()
    test_assault_losses_are_safe_and_non_duplicate()
    test_raid_tick_has_assault_state_recovery_and_no_direct_plunder_skip()
    test_battle_interruption_repair_and_reports_cover_edge_cases()
    test_militia_armory_is_subtle_and_can_be_stolen()
    print("test_village_garrison_assault_static: OK")
