from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_ordered(path, tokens):
    raw = read(path)
    offset = 0
    for token in tokens:
        index = raw.find(token, offset)
        if index < 0:
            raise AssertionError(f"{path}: missing ordered token after {offset}: {token}")
        offset = index + len(token)


def test_spawned_persistent_parties_are_active_before_mutation():
    cases = (
        (
            "src/scripts/ZC_parties/change_party_template.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_name, ":new_party", s19)',
            ),
        ),
        (
            "src/scripts/ZC_parties/cf_create_kingdom_party.py",
            (
                '(assign, ":result", reg0)',
                '(gt, ":result", 0)',
                '(party_is_active, ":result")',
                '(party_set_faction, ":result", ":faction_no")',
            ),
        ),
        (
            "src/scripts/ZC_parties/create_kingdom_hero_party.py",
            (
                '(assign, "$pout_party", reg0)',
                '(gt, "$pout_party", 0)',
                '(party_is_active, "$pout_party")',
                '(party_set_faction, "$pout_party", ":troop_faction_no")',
            ),
        ),
        (
            "src/scripts/ZC_parties/create_village_farmer_party.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_get_slot, ":population", ":village_no", slot_center_sod_local_population)',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/cf_sod_create_castle_patrol.py",
            (
                '(assign, ":patrol_party", reg0)',
                '(gt, ":patrol_party", 0)',
                '(party_is_active, ":patrol_party")',
                '(party_set_faction, ":patrol_party", ":faction_no")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_merc_lord_try_spawn_for_troop.py",
            (
                '(assign, ":merc_lord_party", reg0)',
                '(gt, ":merc_lord_party", 0)',
                '(party_is_active, ":merc_lord_party")',
                '(party_set_faction, ":merc_lord_party", ":employer_faction")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_tax_couriers.py",
            (
                '(assign, ":courier_party", reg0)',
                '(gt, ":courier_party", 0)',
                '(party_is_active, ":courier_party")',
                '(party_set_faction, ":courier_party", ":origin_faction")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_center_public_health.py",
            (
                '(assign, ":relief_party", reg0)',
                '(gt, ":relief_party", 0)',
                '(party_is_active, ":relief_party")',
                '(party_set_faction, ":relief_party", ":origin_faction")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_diplomacy_system.py",
            (
                '(assign, ":envoy_party", reg0)',
                '(gt, ":envoy_party", 0)',
                '(party_is_active, ":envoy_party")',
                '(party_set_faction, ":envoy_party", "fac_player_supporters_faction")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py",
            (
                '(assign, ":mercs", reg0)',
                '(gt, ":mercs", 0)',
                '(party_is_active, ":mercs")',
                '(party_set_name, ":mercs", s60)',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py",
            (
                '(assign, ":mercs", reg0)',
                '(gt, ":mercs", 0)',
                '(party_is_active, ":mercs")',
                '(call_script, "script_party_add_party", ":mercs", "$g_encountered_party")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_company_accounts.py",
            (
                '(assign, ":deserter_party", reg0)',
                '(gt, ":deserter_party", 0)',
                '(party_is_active, ":deserter_party")',
                '(party_clear, ":deserter_party")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_company_accounts.py",
            (
                '(assign, ":mutiny_party", reg0)',
                '(gt, ":mutiny_party", 0)',
                '(party_is_active, ":mutiny_party")',
                '(party_set_name, ":mutiny_party", "@Company Mutineers")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_lord_party_morale.py",
            (
                '(assign, ":deserter_party", reg0)',
                '(gt, ":deserter_party", 0)',
                '(party_is_active, ":deserter_party")',
                '(party_clear, ":deserter_party")',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, ":boar_spawn_anchor", "pt_boar_clan_fighters")',
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild7")',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, "p_sod_merc_guild_7", "pt_boar_clan_fighters_desert")',
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild7")',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, ":spawn_point", "pt_bandits")',
                '(assign, ":spawned_party_id", reg0)',
                '(gt, ":spawned_party_id", 0)',
                '(party_is_active, ":spawned_party_id")',
                '(assign, ":spawned_from_village", 0)',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, ":party_no", "pt_deserters")',
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_remove_members, ":party_no", ":tier_1_troop", ":number_to_add")',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, ":center_no", "pt_sod_deserters")',
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(store_mul, ":population_delta", ":number_to_add", -1)',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, ":center_no", "pt_sod_merc_deserters")',
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(store_faction_of_party, ":faction_no", ":center_no")',
            ),
        ),
        (
            "src/scripts/ZZ_common_array_processing/spawn_bandits.py",
            (
                '(spawn_around_party, ":spawn_point", "pt_mercenaries")',
                '(assign, ":merc_party", reg0)',
                '(gt, ":merc_party", 0)',
                '(party_is_active, ":merc_party")',
                '(call_script, "script_cf_party_upgrade_with_xp", ":merc_party", 150000)',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py",
            (
                '(assign, ":looter_party", reg0)',
                '(gt, ":looter_party", 0)',
                '(party_is_active, ":looter_party")',
                '(party_clear, ":looter_party")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py",
            (
                '(assign, ":bandit_party", reg0)',
                '(gt, ":bandit_party", 0)',
                '(party_is_active, ":bandit_party")',
                '(party_set_slot, ":bandit_party", slot_party_sod_threat_type, sod_threat_type_faction_problem)',
            ),
        ),
        (
            "src/triggers/ST03_daily/entry_0088.py",
            (
                '(assign, ":merc_party", reg0)',
                '(gt, ":merc_party", 0)',
                '(party_is_active, ":merc_party")',
                '(party_add_template, ":merc_party", "pt_legion_mercenaries")',
            ),
        ),
        (
            "src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py",
            (
                '(assign, ":mercs", reg0)',
                '(gt, ":mercs", 0)',
                '(party_is_active, ":mercs")',
                '(party_set_slot, ":mercs", slot_party_starting_base, "p_sod_merc_guild_1")',
            ),
        ),
        (
            "src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py",
            (
                '(party_set_slot, ":mercs", slot_party_starting_base, -1)',
                '(try_end)',
                '(gt, ":mercs", 0)',
                '(party_is_active, ":mercs")',
                '(party_set_slot, ":mercs", slot_party_starting_size, ":starting_size")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild3")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild5")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild1")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild2")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py",
            (
                '(assign, ":new_party", reg0)',
                '(gt, ":new_party", 0)',
                '(party_is_active, ":new_party")',
                '(party_set_faction, ":new_party", "fac_sod_merc_guild4")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
            (
                '(assign, ":camp_party", reg0)',
                '(gt, ":camp_party", 0)',
                '(party_is_active, ":camp_party")',
                '(party_set_faction, ":camp_party", "fac_black_khergits")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
            (
                '(assign, ":guard_party", reg0)',
                '(gt, ":guard_party", 0)',
                '(party_is_active, ":guard_party")',
                '(party_set_faction, ":guard_party", "fac_black_khergits")',
            ),
        ),
        (
            "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
            (
                '(assign, ":raider_party", reg0)',
                '(gt, ":raider_party", 0)',
                '(party_is_active, ":raider_party")',
                '(party_set_faction, ":raider_party", "fac_black_khergits")',
            ),
        ),
    )
    for path, tokens in cases:
        assert_ordered(path, tokens)


def test_diplomatic_envoy_spawn_failure_keeps_player_informed():
    raw = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    if "could not place the envoy on the map" not in raw:
        raise AssertionError("diplomatic envoy spawn failure needs a player-facing message")


def test_mercenary_quote_uses_temp_party_not_world_spawn():
    raw = read("src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py")
    quote_start = raw.index('("merc_calculate_hire_quote"')
    spawn_start = raw.index('("merc_spawn_player_company"', quote_start)
    quote_script = raw[quote_start:spawn_start]
    if '(spawn_around_party, "p_main_party", "pt_player_mercenaries")' in quote_script:
        raise AssertionError("hire quote should not create a temporary world-map mercenary party")
    for token in (
        '(assign, ":preview_party", "p_temp_party")',
        '(call_script, "script_merc_build_preview_party", ":preview_party"',
        '(eq, ":preview_party", "p_temp_party")',
        '(party_clear, ":preview_party")',
    ):
        if token not in quote_script:
            raise AssertionError(f"hire quote missing temp-party token: {token}")


def test_boar_hire_charges_only_after_successful_conversion():
    dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_boar_clan_recruit_3.py")
    assert_ordered(
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_boar_clan_recruit_3.py",
        (
            '(call_script, "script_sod_boar_clan_convert_to_player_mercenaries")',
            '(eq, reg0, 1)',
            '(call_script, "script_sod_player_charge_gold", ":hire_cost")',
            '(call_script, "script_sod_boar_clan_apply_player_action", sod_boar_action_hire_band, ":hire_cost")',
        ),
    )
    for token in (
        "No silver changed hands",
        '(assign, reg0, ":converted")',
    ):
        raw = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")
        if token not in raw:
            raise AssertionError(f"boar conversion missing failure/success token: {token}")
    if dialog.index('(assign, "$g_sod_boar_hire_cost", 0)') < dialog.index('(try_end)'):
        raise AssertionError("boar hire cost should clear after the success gate closes")


def test_slaver_world_spawn_names_and_messages_are_guarded():
    path = "src/scripts/ZY_helper_scripts/sod_slavers_black_market.py"
    raw = read(path)
    if raw.count('(assign, ":web_party", reg0)') != 2:
        raise AssertionError("slaver world spawn should assign web_party in both recovery and caravan branches")
    if '(party_set_name, ":web_party", s0)' in raw:
        raise AssertionError("slaver world spawn should not name parties through s0")
    active = raw.index('(party_is_active, ":web_party")')
    name = raw.index('(party_set_name, ":web_party", s60)')
    faction = raw.index('(party_set_faction, ":web_party", "fac_sod_merc_guild6")')
    recovery_message = raw.index("Slaver recovery parties are moving")
    caravan_message = raw.index("Slaver caravans are expanding")
    if not (active < name < recovery_message < faction):
        raise AssertionError("slaver recovery spawn message/name should be behind the active-party guard")
    if not (active < caravan_message < faction):
        raise AssertionError("slaver caravan spawn message should be behind the active-party guard")
    last_assign = raw.rindex('(assign, ":web_party", reg0)')
    if not (last_assign < active):
        raise AssertionError("slaver caravan branch should be guarded before shared party setup")


def test_all_legion_auxiliary_waves_guard_spawn_results():
    raw = read("src/triggers/ST03_daily/entry_0088.py")
    spawn_count = raw.count('(spawn_around_party, ":cur_spawn_point", "pt_legion_mercenaries")')
    active_count = raw.count('(party_is_active, ":merc_party")')
    if spawn_count != 3:
        raise AssertionError("expected three Legion auxiliary spawn waves")
    if active_count < spawn_count:
        raise AssertionError("each Legion auxiliary spawn wave needs an active-party guard")


def test_ai_merc_spawn_branches_guard_spawn_results():
    raw = read("src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py")
    spawn_count = raw.count('(spawn_around_party')
    active_count = raw.count('(party_is_active, ":mercs")')
    if spawn_count != 6:
        raise AssertionError("expected six AI mercenary spawn branches")
    if active_count < spawn_count + 1:
        raise AssertionError("AI mercenary spawns need per-branch and final active-party guards")


def test_generic_party_helpers_guard_invalid_or_empty_parties():
    assert_ordered(
        "src/scripts/ZC_parties/cf_reinforce_party.py",
        (
            '(assign, ":party_type", -1)',
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(store_faction_of_party, ":party_faction", ":party_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/cf_reinforce_party.py",
        (
            '(eq, ":party_type", spt_kingdom_hero_party)',
            '(party_get_num_companion_stacks, ":num_stacks", ":party_no")',
            '(gt, ":num_stacks", 0)',
            '(party_stack_get_troop_id, ":leader", ":party_no", 0)',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/cf_reinforce_party.py",
        (
            '(gt, ":party_template", 0)',
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(party_add_template, ":party_no", ":party_template")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/party_get_ideal_size.py",
        (
            '(party_is_active, ":party_no")',
            '(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party)',
            '(party_get_num_companion_stacks, ":num_stacks", ":party_no")',
            '(gt, ":num_stacks", 0)',
            '(party_stack_get_troop_id, ":party_leader", ":party_no", 0)',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/get_nonempty_party_in_group.py",
        (
            '(assign, reg0, -1)',
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(party_get_num_companion_stacks, ":num_companion_stacks", ":party_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/get_nonempty_party_in_group.py",
        (
            '(party_is_active, ":party_no")',
            '(party_get_num_attached_parties, ":num_attached_parties", ":party_no")',
            '(party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/party_wound_all_members_aux.py",
        (
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(party_get_num_companion_stacks, ":num_stacks", ":party_no")',
            '(party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/party_wound_all_members_aux.py",
        (
            '(party_is_active, ":party_no")',
            '(party_get_num_attached_parties, ":num_attached_parties", ":party_no")',
            '(party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/collect_prisoners_from_empty_parties.py",
        (
            '(party_is_active, ":party_no")',
            '(party_is_active, ":collection_party")',
            '(party_get_num_companions, ":num_companions", ":party_no")',
            '(party_get_num_prisoner_stacks, ":num_stacks", ":party_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/collect_prisoners_from_empty_parties.py",
        (
            '(party_is_active, ":collection_party")',
            '(party_get_num_attached_parties, ":num_attached_parties", ":party_no")',
            '(party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/cf_party_remove_random_regular_troop.py",
        (
            '(assign, reg0, -1)',
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(party_get_num_companion_stacks, ":num_stacks", ":party_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZY_helper_scripts/sod_transfer_hostile_prisoners_to_player.py",
        (
            '(gt, ":source_party", 0)',
            '(party_is_active, ":source_party")',
            '(party_get_num_prisoner_stacks, ":num_stacks", ":source_party")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/event_player_captured_as_prisoner.py",
        (
            '(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party)',
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(party_slot_eq, ":party_no", slot_party_commander_party, "p_main_party")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/exchange_prisoners_between_factions.py",
        (
            '(try_for_parties, ":party_no")',
            '(party_is_active, ":party_no")',
            '(store_faction_of_party, ":party_faction", ":party_no")',
            '(party_get_num_prisoner_stacks, ":num_stacks", ":party_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/get_stack_with_rank.py",
        (
            '(assign, reg(0), -1)',
            '(gt, ":party", 0)',
            '(party_is_active, ":party")',
            '(ge, ":rank", 0)',
            '(party_get_num_companion_stacks, ":num_stacks", ":party")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/inflict_casualties_to_party.py",
        (
            '(gt, ":party", 0)',
            '(party_is_active, ":party")',
            '(call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank")',
            '(assign, ":attacked_stack", reg(0))',
            '(ge, ":attacked_stack", 0)',
            '(party_stack_get_troop_id,     ":attacked_troop", ":party", ":attacked_stack")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/write_fit_party_members_to_stack_selection.py",
        (
            '(assign, ":slot_index", 2)',
            '(assign, ":total_fit", 0)',
            '(gt, ":party_no", 0)',
            '(party_is_active, ":party_no")',
            '(party_get_num_companion_stacks, ":num_stacks", ":party_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/remove_fit_party_member_from_stack_selection.py",
        (
            '(assign, reg0, -1)',
            '(troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0)',
            '(is_between, ":slot_index", 0, ":num_slots")',
            '(gt, ":amount", 0)',
            '(assign, reg0, ":troop_no")',
        ),
    )
    assert_ordered(
        "src/scripts/ZC_parties/remove_random_fit_party_member_from_stack_selection.py",
        (
            '(assign, reg0, -1)',
            '(troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1)',
            '(gt, ":total_amount", 0)',
            '(store_random_in_range, ":random_troop", 0, ":total_amount")',
        ),
    )
    for path in (
        "src/scripts/ZC_parties/party_count_fit_for_battle.py",
        "src/scripts/ZC_parties/party_count_members_with_full_health.py",
        "src/scripts/ZC_parties/party_calculate_regular_strength.py",
        "src/scripts/ZC_parties/party_calculate_siege_or_not_strength.py",
        "src/scripts/ZF_factions/kt_party_calculate_strength.py",
        "src/scripts/ZF_factions/kt_count_viable_troops.py",
        "src/scripts/ZC_parties/sod_party_count_strength.py",
    ):
        assert_ordered(
            path,
            (
                '(gt, ":party", 0)',
                '(party_is_active, ":party")',
                '(party_get_num_companion_stacks, ":num_stacks"',
            ),
        )
    assert_ordered(
        "src/scripts/ZF_factions/kt_count_viable_troops_with_attachments.py",
        (
            '(assign, ":attached_count", 0)',
            '(gt, ":root_party", 0)',
            '(party_is_active, ":root_party")',
            '(party_get_num_attached_parties, ":attached_count", ":root_party")',
        ),
    )


if __name__ == "__main__":
    test_spawned_persistent_parties_are_active_before_mutation()
    test_diplomatic_envoy_spawn_failure_keeps_player_informed()
    test_mercenary_quote_uses_temp_party_not_world_spawn()
    test_boar_hire_charges_only_after_successful_conversion()
    test_slaver_world_spawn_names_and_messages_are_guarded()
    test_all_legion_auxiliary_waves_guard_spawn_results()
    test_ai_merc_spawn_branches_guard_spawn_results()
    test_generic_party_helpers_guard_invalid_or_empty_parties()
    print("test_spawn_active_guards_static: OK")
