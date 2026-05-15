from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(source: str, needle: str, label: str) -> None:
    assert needle in source, f"{label}: missing {needle}"


def assert_order(source: str, first: str, second: str, label: str) -> None:
    assert first in source, f"{label}: missing {first}"
    assert second in source, f"{label}: missing {second}"
    assert source.index(first) < source.index(second), f"{label}: {first} must precede {second}"


def test_allied_siege_victory_routes_through_total_victory_before_capture_menu() -> None:
    allied_menu = read("src/menus/centers/castle/talk_to_siege_commander.py")
    menu_order = read("src/menus/_order_game_menus.txt")

    assert_contains(allied_menu, '"{s72} remains under siege.', "allied siege text")
    assert_contains(allied_menu, '(str_store_string, s72, "@The center")', "allied siege text")
    assert_contains(allied_menu, '(str_store_string, s73, "@the allied host")', "allied siege text")
    assert_contains(allied_menu, '(party_is_active, "$g_encountered_party")', "allied siege")
    assert_contains(allied_menu, '(party_is_active, "$g_encountered_party_2")', "allied siege")
    assert_contains(allied_menu, '(assign, "$g_enemy_party", "$g_encountered_party")', "allied siege")
    assert_contains(allied_menu, '(assign, "$g_ally_party", "$g_encountered_party_2")', "allied siege")
    assert_order(
        allied_menu,
        '(party_is_active, "$g_encountered_party")',
        '(assign, "$g_enemy_party", "$g_encountered_party")',
        "allied siege enemy guard",
    )
    assert_order(
        allied_menu,
        '(party_is_active, "$g_encountered_party_2")',
        '(assign, "$g_ally_party", "$g_encountered_party_2")',
        "allied siege ally guard",
    )
    assert_contains(allied_menu, '(party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy")', "allied siege")
    assert_contains(allied_menu, '(assign, "$g_next_menu", "mnu_castle_taken_by_friends")', "allied siege")
    assert_contains(allied_menu, '(jump_to_menu, "mnu_total_victory")', "allied siege")
    assert_order(
        allied_menu,
        '(party_is_active, "$g_enemy_party")',
        '(party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy")',
        "allied siege capture guard",
    )

    assert_contains(allied_menu, '("talk_to_siege_commander", [', "allied siege commander option")
    assert_contains(allied_menu, '(party_get_num_companion_stacks, ":num_siege_leader_stacks", "$g_encountered_party_2")', "allied siege commander option")
    assert_order(
        allied_menu,
        '(gt, ":num_siege_leader_stacks", 0)',
        '(party_stack_get_troop_id, ":siege_leader_id", "$g_encountered_party_2", 0)',
        "allied siege commander option",
    )

    assert_order(
        menu_order,
        "centers/castle/castle_taken_by_friends.py",
        "other/continue_17.py",
        "menu order",
    )


def test_player_siege_victory_preserves_center_context_for_total_victory() -> None:
    player_siege = read("src/menus/centers/castle/siege_request_meeting.py")
    finalize = read("src/scripts/ZC_parties/total_victory_finalize.py")

    for token in (
        '(call_script, "script_encounter_init_variables")',
        '(assign, "$g_enemy_party", "$g_encountered_party")',
        '(call_script, "script_encounter_calculate_fit")',
        '(assign, "$g_next_menu", "mnu_castle_taken")',
        '(jump_to_menu, "mnu_total_victory")',
    ):
        assert_contains(player_siege, token, "player siege")
    assert player_siege.count('(call_script, "script_encounter_init_variables")') >= 2, (
        "player siege must reset capture/loot state before both led and simulated assaults"
    )
    assert_order(
        player_siege,
        '(call_script, "script_encounter_init_variables")',
        '(set_party_battle_mode)',
        "player siege led assault state reset",
    )
    assert_order(
        player_siege,
        '(call_script, "script_encounter_init_variables")',
        '(jump_to_menu, "mnu_castle_attack_walls_simulate")',
        "player siege simulated assault state reset",
    )

    for token in (
        '(this_or_next|eq, "$g_next_menu", "mnu_castle_taken")',
        '(eq, "$g_next_menu", "mnu_castle_taken_by_friends")',
        '(is_between, "$g_player_besiege_town", walled_centers_begin, walled_centers_end)',
        '(assign, "$g_enemy_party", "$g_player_besiege_town")',
        '(assign, "$g_encountered_party", "$g_player_besiege_town")',
        '(is_between, "$current_town", walled_centers_begin, walled_centers_end)',
        '(assign, "$g_enemy_party", "$current_town")',
        '(assign, "$g_encountered_party", "$current_town")',
        '(call_script, "script_sod_battle_aftermath_validate_globals_to_regs")',
    ):
        assert_contains(finalize, token, "total victory capture restore")
    assert_order(
        finalize,
        '(this_or_next|eq, "$g_next_menu", "mnu_castle_taken")',
        '(call_script, "script_sod_battle_aftermath_validate_globals_to_regs")',
        "total victory capture restore",
    )


def test_capture_menus_only_mutate_resolved_walled_centers() -> None:
    friends_capture = read("src/menus/centers/castle/castle_taken_by_friends.py")
    player_capture = read("src/menus/other/continue_17.py")

    for label, source in (
        ("friends capture", friends_capture),
        ("player capture", player_capture),
    ):
        for token in (
            '(is_between, "$g_enemy_party", walled_centers_begin, walled_centers_end)',
            '(is_between, "$g_player_besiege_town", walled_centers_begin, walled_centers_end)',
            '(is_between, "$current_town", walled_centers_begin, walled_centers_end)',
            '(is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end)',
            '(assign, "$current_town", "$g_encountered_party")',
            '(store_faction_of_party, "$g_encountered_party_faction", "$g_encountered_party")',
            '(neq, "$g_encountered_party_faction", ":winner_faction")',
            '(party_clear, "$g_encountered_party")',
            '(call_script, "script_lift_siege", "$g_encountered_party", 0)',
            '(call_script, "script_give_center_to_faction"',
            '@Siege result warning: captured center could not be resolved.',
        ):
            assert_contains(source, token, label)
        assert_order(
            source,
            '(store_faction_of_party, "$g_encountered_party_faction", "$g_encountered_party")',
            '(party_clear, "$g_encountered_party")',
            label,
        )
        assert_order(
            source,
            '(neq, "$g_encountered_party_faction", ":winner_faction")',
            '(party_clear, "$g_encountered_party")',
            label,
        )

    assert_contains(player_capture, '(assign, "$auto_enter_town", -1)', "player capture continue guard")
    assert_contains(player_capture, '(assign, ":winner_faction", "$players_kingdom")', "player capture ownership")
    assert_contains(player_capture, '(assign, ":winner_faction", "fac_player_supporters_faction")', "player capture ownership")
    assert_contains(player_capture, '(jump_to_menu, "mnu_castle_taken_2")', "player vassal claim")
    assert_contains(friends_capture, 'logent_player_participated_in_siege', "friends capture log")
    for token in (
        '(assign, ":winner_faction", -1)',
        '(party_is_active, "$g_encountered_party_2")',
        '(store_faction_of_party, ":winner_faction", "$g_encountered_party_2")',
        '(assign, ":leader_troop", -1)',
        '(party_stack_get_troop_id, ":leader_troop", "$g_encountered_party_2", 0)',
        '(party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, ":leader_troop")',
        '(party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1)',
        '(call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", ":winner_faction")',
    ):
        assert_contains(friends_capture, token, "friends capture ownership")
    assert_order(
        friends_capture,
        '(store_faction_of_party, ":winner_faction", "$g_encountered_party_2")',
        '(assign, ":winner_faction", "$players_kingdom")',
        "friends capture winner fallback",
    )
    assert_order(
        friends_capture,
        '(assign, ":winner_faction", "$players_kingdom")',
        '(assign, ":winner_faction", "fac_player_supporters_faction")',
        "friends capture winner fallback",
    )


def test_siege_loot_fallback_survives_missing_enemy_global() -> None:
    loot = read("src/scripts/ZC_parties/party_calculate_loot.py")

    for token in (
        '(assign, ":loot_source_party", "$g_enemy_party")',
        '(assign, ":loot_source_valid", 0)',
        '(val_max, ":num_player_party_shares", 1)',
        '(assign, ":loot_source_party", "$g_encountered_party")',
        '(assign, ":loot_source_party", "$current_town")',
        '(assign, ":loot_source_party", "$g_player_besiege_town")',
        '(assign, ":loot_source_party", ":enemy_party")',
        '(eq, ":loot_source_valid", 1)',
        '(this_or_next|party_slot_eq, ":loot_source_party", slot_party_type, spt_town)',
        '(party_slot_eq, ":loot_source_party", slot_party_type, spt_castle)',
        '(this_or_next|eq, "$g_next_menu", "mnu_castle_taken")',
        '(is_between, "$current_town", walled_centers_begin, walled_centers_end)',
        '(eq, ":num_looted_items", 0)',
        '(eq, ":is_siege_center", 1)',
        '(try_for_range, ":cur_food", food_begin, food_end)',
        '(troop_add_merchandise, "trp_temp_troop", itp_type_goods, ":plunder_amount")',
        '(assign, ":troop_loot_party", ":enemy_party")',
        '(assign, ":troop_loot_party_valid", 0)',
        '(party_is_active, ":troop_loot_party")',
        '(eq, ":troop_loot_party_valid", 1)',
        '(party_get_num_companion_stacks, ":num_stacks", ":troop_loot_party")',
    ):
        assert_contains(loot, token, "siege loot fallback")

    assert_order(
        loot,
        '(assign, ":num_player_party_shares", reg0)',
        '(val_max, ":num_player_party_shares", 1)',
        "siege loot share clamp",
    )
    assert_order(
        loot,
        '(party_get_slot, ":cur_price", ":loot_source_party", ":cur_price_slot")',
        '(val_max, ":cur_price", 1)',
        "siege loot price clamp",
    )
    assert_order(
        loot,
        '(party_is_active, ":troop_loot_party")',
        '(party_get_num_companion_stacks, ":num_stacks", ":troop_loot_party")',
        "siege troop loot stale party guard",
    )

    for stale_token in (
        '(party_get_slot, ":item_no", "$g_enemy_party", ":cur_loot_slot")',
        '(party_set_slot, "$g_enemy_party", ":cur_loot_slot", 0)',
        '(party_get_slot, ":cur_price", "$g_enemy_party", ":cur_price_slot")',
        '(party_set_slot, "$g_enemy_party", slot_party_next_looted_item_slot, 0)',
        '(party_get_num_companion_stacks, ":num_stacks", ":enemy_party")',
    ):
        assert stale_token not in loot, f"siege loot fallback still has brittle direct enemy global read: {stale_token}"


def test_post_battle_helpers_guard_stale_party_ids() -> None:
    finalize = read("src/scripts/ZC_parties/total_victory_finalize.py")
    ally_thanks = read("src/scripts/ZC_parties/total_victory_try_ally_thanks.py")
    capture_pool = read("src/scripts/ZC_parties/total_victory_prepare_capture_pool.py")
    leftovers = read("src/scripts/ZC_parties/total_victory_distribute_leftovers.py")
    total_defeat = read("src/menus/other/total_defeat.py")
    lord_morale = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    tactic = read("src/scripts/ZE_encounters/select_battle_tactic_aux.py")
    setup_meeting = read("src/scripts/ZC_parties/setup_party_meeting.py")

    assert_contains(
        finalize,
        '(party_get_num_companion_stacks, ":num_enemy_backup_stacks", "p_encountered_party_backup")',
        "total victory enemy leader guard",
    )
    assert (
        '(call_script, "script_post_battle_personality_clash_check"),\n\n'
        '        (try_begin),\n'
        '          (party_get_num_companion_stacks, ":num_enemy_backup_stacks", "p_encountered_party_backup")'
        in finalize
    ), "total victory enemy leader guard must be isolated in its own try block"
    assert (
        '          (try_end),\n'
        '        (try_end),\n\n'
        '        (val_add, "$g_total_victories", 1)'
        in finalize
    ), "total victory finalization must continue after optional enemy leader comment"
    assert_order(
        finalize,
        '(gt, ":num_enemy_backup_stacks", 0)',
        '(party_stack_get_troop_id, ":enemy_leader", "p_encountered_party_backup", 0)',
        "total victory enemy leader guard",
    )
    assert_order(
        finalize,
        '(party_stack_get_troop_id, ":enemy_leader", "p_encountered_party_backup", 0)',
        '(val_add, "$g_total_victories", 1)',
        "total victory enemy leader guard",
    )

    for label, source, later in (
        ("ally thanks", ally_thanks, '(party_get_num_companion_stacks, ":num_ally_stacks", "$g_ally_party")'),
        ("capture pool", capture_pool, '(distribute_party_among_party_group, "p_temp_party_2", "$g_ally_party")'),
        ("leftovers", leftovers, '(distribute_party_among_party_group, "p_temp_party", "$g_ally_party")'),
        ("total defeat", total_defeat, '(call_script, "script_party_wound_all_members", "$g_ally_party")'),
        ("lord morale", lord_morale, '(call_script, "script_sod_party_get_lord_morale_context", "$g_ally_party")'),
    ):
        assert_contains(source, '(party_is_active, "$g_ally_party")', label)
        assert_order(source, '(party_is_active, "$g_ally_party")', later, label)

    assert_order(
        leftovers,
        '(party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0)',
        '(party_is_active, ":helper_party")',
        "leftover helper party guard",
    )
    assert_order(
        leftovers,
        '(party_is_active, ":helper_party")',
        '(distribute_party_among_party_group, "p_temp_party", ":helper_party")',
        "leftover helper party guard",
    )

    assert_contains(ally_thanks, '(party_stack_get_troop_id, ":ally_leader", "$g_ally_party", 0)', "ally thanks")
    assert_contains(ally_thanks, '(party_stack_get_troop_dna, ":ally_leader_dna", "$g_ally_party", 0)', "ally thanks")

    assert_order(
        tactic,
        '(party_is_active, "$g_enemy_party")',
        '(party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_hero_party)',
        "battle tactic enemy party guard",
    )
    assert_order(
        tactic,
        '(party_is_active, "$g_ally_party")',
        '(party_slot_eq, "$g_ally_party", slot_party_type, spt_kingdom_hero_party)',
        "battle tactic ally party guard",
    )

    assert_contains(setup_meeting, '(assign, ":meeting_troop", -1)', "setup party meeting")
    assert_contains(setup_meeting, '(party_is_active, ":meeting_party")', "setup party meeting")
    assert_contains(setup_meeting, '(party_get_num_companion_stacks, ":num_meeting_stacks", ":meeting_party")', "setup party meeting")
    assert_order(
        setup_meeting,
        '(gt, ":num_meeting_stacks", 0)',
        '(party_stack_get_troop_id, ":meeting_troop", ":meeting_party", 0)',
        "setup party meeting",
    )


def test_party_group_cleanup_ignores_stale_party_ids() -> None:
    clear_party_group = read("src/scripts/ZC_parties/clear_party_group.py")

    for token in (
        '(gt, ":root_party", 0)',
        '(party_is_active, ":root_party")',
        '(party_clear, ":root_party")',
        '(party_get_num_attached_parties, ":num_attached_parties", ":root_party")',
        '(call_script, "script_clear_party_group", ":attached_party")',
    ):
        assert_contains(clear_party_group, token, "clear party group guard")
    assert_order(
        clear_party_group,
        '(party_is_active, ":root_party")',
        '(party_clear, ":root_party")',
        "clear party group guard",
    )


def test_claim_menu_uses_town_or_castle_wording() -> None:
    claim_menu = read("src/menus/centers/castle/castle_taken_claim.py")

    assert_contains(
        claim_menu,
        "full control of the {reg8?town:castle}",
        "claim menu town wording",
    )
    assert_contains(claim_menu, '(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town)', "claim menu")
    assert_contains(claim_menu, '(assign, reg8, 1)', "claim menu")


def test_player_supporter_center_assignment_is_not_overwritten_by_stale_players_kingdom() -> None:
    give_lord = read("src/scripts/ZD_centers/give_center_to_lord.py")

    for token in (
        '(store_faction_of_party, ":center_faction_before_lord", ":center_no")',
        '(eq, ":lord_troop_id", "trp_player")',
        '(eq, ":center_faction_before_lord", "fac_player_supporters_faction")',
        '(party_set_faction, ":center_no", "fac_player_supporters_faction")',
        '(gt, "$players_kingdom", 0)',
        '(party_set_faction, ":center_no", "$players_kingdom")',
    ):
        assert_contains(give_lord, token, "player supporter center ownership")

    assert_order(
        give_lord,
        '(eq, ":center_faction_before_lord", "fac_player_supporters_faction")',
        '(gt, "$players_kingdom", 0)',
        "player supporter center ownership",
    )


def test_center_faction_change_updates_bound_villages_farmers_and_market_links() -> None:
    give_faction = read("src/scripts/ZD_centers/give_center_to_faction.py")
    give_aux = read("src/scripts/ZD_centers/give_center_to_faction_aux.py")

    for token in (
        '(store_faction_of_party, ":old_faction", ":center_no")',
        '(call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no")',
        '(call_script, "script_sod_handle_center_faction_change_castle_patrols", ":center_no", ":old_faction", ":faction_no")',
        '(call_script, "script_update_village_market_towns")',
        '(eq, ":faction_no", "fac_player_supporters_faction")',
        '(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player")',
        '(call_script, "script_give_center_to_lord", ":center_no", "trp_player", 0)',
    ):
        assert_contains(give_faction, token, "center faction assignment")
    assert_order(
        give_faction,
        '(call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no")',
        '(call_script, "script_sod_handle_center_faction_change_castle_patrols", ":center_no", ":old_faction", ":faction_no")',
        "center faction assignment",
    )

    for token in (
        '(party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction")',
        '(party_set_faction, ":center_no", ":faction_no")',
        '(party_slot_eq, ":center_no", slot_party_type, spt_village)',
        '(party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party)',
        '(party_is_active, ":farmer_party")',
        '(party_set_faction, ":farmer_party", ":faction_no")',
        '(party_slot_eq, ":other_center", slot_village_bound_center, ":center_no")',
        '(call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no")',
    ):
        assert_contains(give_aux, token, "bound village faction assignment")
    assert_order(
        give_aux,
        '(party_is_active, ":farmer_party")',
        '(party_set_faction, ":farmer_party", ":faction_no")',
        "farmer faction update",
    )


def main() -> None:
    test_allied_siege_victory_routes_through_total_victory_before_capture_menu()
    test_player_siege_victory_preserves_center_context_for_total_victory()
    test_capture_menus_only_mutate_resolved_walled_centers()
    test_siege_loot_fallback_survives_missing_enemy_global()
    test_post_battle_helpers_guard_stale_party_ids()
    test_party_group_cleanup_ignores_stale_party_ids()
    test_claim_menu_uses_town_or_castle_wording()
    test_player_supporter_center_assignment_is_not_overwritten_by_stale_players_kingdom()
    test_center_faction_change_updates_bound_villages_farmers_and_market_links()
    print("test_siege_capture_resolution_static: OK")


if __name__ == "__main__":
    main()
