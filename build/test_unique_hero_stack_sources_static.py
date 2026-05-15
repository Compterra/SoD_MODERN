from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mercenary_lord_spawn_uses_leader_stack():
    trigger = read("src/triggers/ST03_daily/entry_0129.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_merc_contract_daily.py")
    assert 'script_sod_merc_process_lord_market_pass' in trigger
    assert 'script_sod_merc_lord_try_spawn_for_troop' in helper
    text = read("src/scripts/ZY_helper_scripts/sod_merc_lord_try_spawn_for_troop.py")
    assert '(party_add_leader, ":merc_lord_party", ":troop_no")' in text
    assert '(party_add_members, ":merc_lord_party", ":troop_no", 1)' not in text


def test_attached_party_troop_transfer_rejects_heroes():
    trigger = read("src/triggers/ST02_every_hour/entry_0142.py")
    assert 'script_sod_hourly_lord_ai_maintenance' in trigger
    text = read("src/scripts/ZI_campaign_ai/sod_hourly_lord_ai_maintenance.py")
    troop_read = '(party_stack_get_troop_id, ":troop_id", ":attached_to", ":stack_no")'
    hero_guard = '(neg|troop_is_hero, ":troop_id")'
    add_members = '(party_add_members, ":kingdom_hero_party", ":troop_id", ":transfer")'
    assert troop_read in text
    assert hero_guard in text
    assert text.index(troop_read) < text.index(hero_guard) < text.index(add_members)


def test_prisoner_rescue_helper_never_turns_heroes_into_members():
    text = read("src/scripts/ZC_parties/party_add_party_prisoners.py")
    assert '(neg|troop_is_hero, ":stack_troop")' in text
    assert '(eq, "$g_move_heroes", 1)' not in text
    assert '(party_add_members, ":target_party", ":stack_troop", ":stack_size")' in text


def test_kingdom_hero_party_creation_rejects_invalid_unique_troops():
    text = read("src/scripts/ZC_parties/create_kingdom_hero_party.py")
    assert '(assign, "$pout_party", -1)' in text
    assert '(is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end)' in text
    assert '(neq, ":troop_no", "trp_player")' in text
    assert '(neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1)' in text
    assert '(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0)' in text


def test_ratio_member_transfer_rejects_heroes():
    text = read("src/scripts/ZZ_common_array_processing/move_members_with_ratio.py")
    troop_read = '(party_stack_get_troop_id,     ":stack_troop", ":source_party", ":stack_no")'
    hero_guard = '(neg|troop_is_hero, ":stack_troop")'
    add_members = '(party_add_members, ":target_party", ":stack_troop", ":number_moved")'
    assert text.index(troop_read) < text.index(hero_guard) < text.index(add_members)


def test_generic_party_size_fix_never_removes_heroes():
    text = read("src/scripts/ZC_parties/cf_fix_party_size_recursive.py")
    troop_read = '(party_stack_get_troop_id, ":cur_troop", ":cur_party", ":index")'
    hero_guard = '(neg|troop_is_hero, ":cur_troop")'
    remove_members = '(party_remove_members, ":cur_party", ":cur_troop", ":delta")'
    assert '(assign, ":to_del_stack", -1)' in text
    assert '(ge, ":to_del_stack", 0)' in text
    assert text.index(troop_read) < text.index(hero_guard) < text.index(remove_members)


def test_party_size_fix_resets_prisoner_hero_flag_per_stack():
    text = read("src/scripts/ZC_parties/cf_fix_party_size.py")
    loop = '(try_for_range_backwards, ":index", 0, ":num_stacks")'
    reset = '(assign, ":bool", 0)'
    prisoner_read = '(party_prisoner_stack_get_troop_id, ":cur_troop", ":cur_party", ":index")'
    remove_prisoners = '(party_remove_prisoners, ":cur_party", ":cur_troop", ":cur_size")'
    assert text.index(loop) < text.index(reset) < text.index(prisoner_read) < text.index(remove_prisoners)


def test_bulk_party_stack_helpers_guard_party_ids_before_stack_reads():
    remove_prisoners = read("src/scripts/ZC_parties/party_remove_all_prisoners.py")
    assert remove_prisoners.index('(party_is_active, ":party")') < remove_prisoners.index('(party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party")')

    remove_companions = read("src/scripts/ZC_parties/party_remove_all_companions.py")
    assert remove_companions.index('(party_is_active, ":party")') < remove_companions.index('(party_get_num_companion_stacks, ":num_companion_stacks", ":party")')

    add_prisoners = read("src/scripts/ZC_parties/party_add_party_prisoners.py")
    assert add_prisoners.index('(party_is_active, ":target_party")') < add_prisoners.index('(party_is_active, ":source_party")')
    assert add_prisoners.index('(party_is_active, ":source_party")') < add_prisoners.index('(party_get_num_prisoner_stacks, ":num_stacks", ":source_party")')

    add_companions = read("src/scripts/ZC_parties/party_add_party_companions.py")
    assert add_companions.index('(party_is_active, ":target_party")') < add_companions.index('(party_is_active, ":source_party")')
    assert add_companions.index('(party_is_active, ":source_party")') < add_companions.index('(party_get_num_companion_stacks, ":num_stacks", ":source_party")')

    prisoners_add_companions = read("src/scripts/ZC_parties/party_prisoners_add_party_companions.py")
    assert prisoners_add_companions.index('(party_is_active, ":target_party")') < prisoners_add_companions.index('(party_is_active, ":source_party")')
    assert prisoners_add_companions.index('(party_is_active, ":source_party")') < prisoners_add_companions.index('(party_get_num_companion_stacks, ":num_stacks", ":source_party")')

    prisoners_add_wounded = read("src/scripts/ZC_parties/party_prisoners_add_wounded_party_companions.py")
    assert prisoners_add_wounded.index('(party_is_active, ":target_party")') < prisoners_add_wounded.index('(party_is_active, ":source_party")')
    assert prisoners_add_wounded.index('(party_is_active, ":source_party")') < prisoners_add_wounded.index('(party_get_num_companion_stacks, ":num_stacks", ":source_party")')

    prisoners_add_prisoners = read("src/scripts/ZC_parties/party_prisoners_add_party_prisoners.py")
    assert prisoners_add_prisoners.index('(party_is_active, ":target_party")') < prisoners_add_prisoners.index('(party_is_active, ":source_party")')
    assert prisoners_add_prisoners.index('(party_is_active, ":source_party")') < prisoners_add_prisoners.index('(party_get_num_prisoner_stacks, ":num_stacks", ":source_party")')

    party_copy = read("src/scripts/ZC_parties/party_copy.py")
    assert party_copy.index('(party_is_active, ":target_party")') < party_copy.index('(party_is_active, ":source_party")')
    assert party_copy.index('(party_is_active, ":source_party")') < party_copy.index('(party_clear, ":target_party")')


def test_retreat_leave_behind_does_not_add_invalid_prisoner_troop():
    text = read("src/menus/prisoners/leave_behind.py")
    remove_call = '(call_script, "script_cf_party_remove_random_regular_troop", "p_main_party")'
    lost_assign = '(assign, ":lost_troop", reg0)'
    troop_guard = '(gt, ":lost_troop", 0)'
    party_guard = '(party_is_active, "$g_encountered_party")'
    add_prisoner = '(party_add_prisoners, "$g_encountered_party", ":lost_troop", 1)'
    assert text.index(remove_call) < text.index(lost_assign) < text.index(troop_guard)
    assert text.index(troop_guard) < text.index(party_guard) < text.index(add_prisoner)


def test_dynamic_divisions_guard_zero_edge_cases():
    report = read("src/menus/economy/to_price_and_productions.py")
    consumption_assign = '(assign, ":food_consumption", reg0)'
    consumption_guard = '(val_max, ":food_consumption", 1)'
    food_div = '(store_div, reg3, ":town_food_store", ":food_consumption")'
    assert report.index(consumption_assign) < report.index(consumption_guard) < report.index(food_div)

    retreat = read("src/scripts/ZZ_common_array_processing/simulate_retreat.py")
    casualty_guard = '(gt, ":total_casualties", 0)'
    ally_guard = '(gt, ":total_allies", 0)'
    morale_div = '(val_div, ":morale_adder", ":total_allies")'
    assert retreat.index(casualty_guard) < retreat.index(ally_guard) < retreat.index(morale_div)


def test_dynamic_random_ranges_are_clamped_before_tax_collection_rolls():
    text = read("src/menus/start_game/start_collecting.py")
    total_guard = '(val_max, "$qst_collect_taxes_total_hours", 24)'
    hourly_income = '(store_div, "$qst_collect_taxes_hourly_income", ":tax_quest_expected_revenue", "$qst_collect_taxes_total_hours")'
    menu_end_guard = '(val_max, ":menu_end_time", 2)'
    menu_begin_sub = '(val_sub, ":menu_begin_time", 1)'
    menu_roll = '(store_random_in_range, "$qst_collect_taxes_menu_counter", ":menu_begin_time", ":menu_end_time")'
    unrest_min = '(store_add, ":min_unrest_end_time", ":unrest_begin_time", 1)'
    unrest_roll = '(store_random_in_range, "$qst_collect_taxes_unrest_counter", ":unrest_begin_time", ":unrest_end_time")'
    assert text.index(total_guard) < text.index(hourly_income)
    assert text.index(menu_end_guard) < text.index(menu_begin_sub) < text.index(menu_roll)
    assert text.index(unrest_min) < text.index(unrest_roll)


def test_ai_center_construction_skips_empty_improvement_lists_before_random_roll():
    text = read("src/triggers/ST04_weekly/entry_0123.py")
    for troop in ("trp_village", "trp_town", "trp_castle"):
        count_read = f'(troop_get_slot, ":count", "{troop}", 0)'
        guard = '(gt, ":count", 0)'
        count_add = '(val_add, ":count", 1)'
        roll = '(store_random_in_range, ":rand", 1, ":count")'
        block_start = text.index(count_read)
        assert block_start < text.index(guard, block_start) < text.index(count_add, block_start) < text.index(roll, block_start)


def test_spawned_party_cleanup_rejects_heroes_before_stack_removal():
    farmer = read("src/scripts/ZC_parties/create_village_farmer_party.py")
    farmer_read = '(party_stack_get_troop_id, ":stack_troop", ":new_party", ":stack_no")'
    farmer_guard = '(neg|troop_is_hero, ":stack_troop")'
    farmer_remove = '(party_remove_members, ":new_party", ":stack_troop", ":remove_count")'
    assert farmer.index(farmer_read) < farmer.index(farmer_guard) < farmer.index(farmer_remove)

    desperation = read("src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py")
    desperation_read = '(party_stack_get_troop_id, ":tid", ":bandit_party", ":i")'
    desperation_guard = '(neg|troop_is_hero, ":tid")'
    desperation_remove = '(party_remove_members, ":bandit_party", ":tid", 1)'
    assert desperation.index(desperation_read) < desperation.index(desperation_guard) < desperation.index(desperation_remove)

    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    raid_read = '(party_stack_get_troop_id, ":looter_troop", ":looter_party", 0)'
    raid_guard = '(neg|troop_is_hero, ":looter_troop")'
    raid_remove = '(party_remove_members, ":looter_party", ":looter_troop", ":losses")'
    assert raids.index(raid_read) < raids.index(raid_guard) < raids.index(raid_remove)


def test_world_party_bloat_trim_is_single_scan_and_hero_safe():
    trigger = read("src/triggers/ST03_daily/entry_0149.py")
    text = read("src/scripts/ZY_helper_scripts/sod_trim_bloated_parties.py")
    assert '(call_script, "script_sod_trim_bloated_world_parties")' in trigger
    assert "try_for_parties" not in trigger
    assert text.count('(try_for_parties, ":party_no")') == 1
    for token in [
        '"sod_trim_bloated_world_parties"',
        "spt_kingdom_hero_party",
        "script_party_get_ideal_size",
        "sod_bandit_party_bloat_max",
        "script_cf_sod_party_is_hostile_economy_party",
        '(neg|troop_is_hero, ":stack_troop")',
        '(party_remove_members, ":party_no", ":stack_troop", ":removed_count")',
    ]:
        assert token in text
    assert text.count('(neg|troop_is_hero, ":stack_troop")') >= 3
    remove_token = '(party_remove_members, ":party_no", ":stack_troop", ":removed_count")'
    search_from = 0
    while True:
        remove_at = text.find(remove_token, search_from)
        if remove_at == -1:
            break
        previous_guard = text.rfind('(neg|troop_is_hero, ":stack_troop")', 0, remove_at)
        previous_read = text.rfind('(party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no")', 0, remove_at)
        assert previous_read != -1
        assert previous_guard > previous_read
        search_from = remove_at + len(remove_token)
