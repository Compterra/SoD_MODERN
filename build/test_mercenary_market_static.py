from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_mercenary_ledger_slots_and_constants_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for token in [
        "slot_faction_sod_merc_treasury",
        "slot_faction_sod_merc_manpower",
        "slot_faction_sod_merc_veterans",
        "slot_faction_sod_merc_elite_stock",
        "slot_faction_sod_merc_contract_load",
        "slot_faction_sod_merc_support_capacity",
        "slot_faction_sod_merc_active_contracts",
        "slot_faction_sod_merc_recovery_rate",
        "slot_faction_sod_merc_risk_tolerance",
        "slot_faction_sod_merc_market_reputation",
        "slot_faction_sod_merc_price_pressure",
        "slot_faction_sod_merc_demand_score",
        "slot_faction_sod_merc_budget",
        "slot_faction_sod_merc_max_bid",
        "slot_faction_sod_merc_village_patrol_demand",
        "slot_faction_sod_merc_village_patrol_budget",
        "slot_faction_sod_merc_village_patrol_target",
        "slot_faction_sod_merc_village_patrol_urgency",
        "slot_faction_sod_merc_world_activity_pressure",
        "slot_party_sod_merc_contract_employer",
        "slot_party_sod_merc_contract_guild",
        "slot_party_sod_merc_contract_value",
        "slot_party_sod_merc_contract_wage_rate",
        "slot_party_sod_merc_contract_term_end",
        "slot_party_sod_merc_contract_role",
        "slot_party_sod_merc_contract_start_day",
        "slot_party_sod_merc_contract_initial_size",
        "slot_party_sod_merc_contract_loss_score",
        "sod_merc_contract_role_field_company",
        "sod_merc_contract_role_mercenary_lord",
        "sod_merc_refusal_no_capacity",
        "sod_merc_refusal_low_manpower",
        "sod_merc_refusal_loss_shock",
        "sod_merc_buyer_player",
        "sod_merc_buyer_ai_kingdom",
        "sod_merc_access_trusted",
    ]:
        assert_contains(constants, token)


def test_all_seven_guilds_have_ledger_initialization() -> None:
    init = read("src/scripts/ZY_helper_scripts/sod_merc_guild_initialize_ledger.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    for guild in range(1, 8):
        assert_contains(init, f'"fac_sod_merc_guild{guild}"')

    assert_contains(game_start, "script_sod_merc_guild_initialize_ledger")
    assert_contains(game_start, "script_sod_merc_guild_repair_ledgers")


def test_profile_and_predicate_helpers_cover_market_identity() -> None:
    profile = read("src/scripts/ZY_helper_scripts/sod_merc_guild_get_profile.py")
    roster = read("src/scripts/ZY_helper_scripts/sod_merc_guild_get_roster.py")
    access = read("src/scripts/ZY_helper_scripts/sod_merc_guild_get_access_level.py")
    classic = read("src/scripts/ZY_helper_scripts/cf_sod_merc_guild_uses_classic_employer_rotation.py")
    world = read("src/scripts/ZY_helper_scripts/cf_sod_merc_guild_uses_world_presence.py")

    assert_contains(profile, "slot_guild_base")
    assert_contains(profile, "slot_guild_master")
    assert_contains(profile, "slot_guild_representative")
    assert_contains(profile, "script_merc_get_guild_price_factor")
    assert_contains(profile, "script_merc_get_elite_relation_requirement")
    assert_contains(roster, "slot_guild_tier_1_unit_1")
    assert_contains(roster, "slot_guild_tier_1_unit_2")
    assert_contains(roster, "slot_guild_noble")
    assert_contains(access, "sod_merc_access_trusted")
    assert_contains(classic, '"fac_sod_merc_guild6"')
    assert_contains(world, "script_cf_sod_faction_is_merc_guild")


def test_weekly_rotation_uses_explicit_classic_guild_predicate() -> None:
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")

    assert_contains(weekly, "script_sod_merc_market_weekly_pulse")
    assert_contains(weekly, "script_cf_sod_merc_guild_uses_classic_employer_rotation")
    assert_contains(weekly, "guilds_begin, guilds_end")
    assert_not_contains(weekly, 'guilds_begin, "fac_sod_merc_guild6"')


def test_ledger_repair_tags_active_contract_parties() -> None:
    repair = read("src/scripts/ZY_helper_scripts/sod_merc_guild_repair_ledgers.py")
    for token in [
        "spt_ai_mercenaries",
        "spt_player_mercenaries",
        "spt_mercenary_lord_party",
        "slot_party_sod_merc_contract_guild",
        "slot_party_sod_merc_contract_employer",
        "slot_party_sod_merc_contract_role",
        "slot_party_sod_merc_contract_start_day",
        "slot_party_sod_merc_contract_initial_size",
        "slot_party_sod_merc_contract_loss_score",
        "sod_merc_contract_role_field_company",
        "sod_merc_contract_role_mercenary_lord",
        "slot_faction_sod_merc_active_contracts",
    ]:
        assert_contains(repair, token)


def test_supply_demand_and_report_helpers_exist() -> None:
    demand = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_demand.py")
    budget = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_budget.py")
    village_patrol = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_village_patrol_demand.py")
    guild_weight = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_guild_weight.py")
    preferred_guild = read("src/scripts/ZY_helper_scripts/sod_merc_market_select_preferred_guild.py")
    refresh = read("src/scripts/ZY_helper_scripts/sod_merc_market_refresh_kingdom_demands.py")
    demand_report = read("src/scripts/ZY_helper_scripts/sod_merc_market_describe_kingdom_demand_to_s20.py")
    market_overview = read("src/scripts/ZY_helper_scripts/sod_merc_market_describe_overview_to_s20.py")
    world_pressure = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_world_activity_pressure.py")
    world_ledger = read("src/scripts/ZY_helper_scripts/sod_merc_market_apply_world_activity_ledger.py")
    guardrails = read("src/scripts/ZY_helper_scripts/sod_merc_market_apply_guardrails.py")
    supply = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_guild_supply.py")
    recovery = read("src/scripts/ZY_helper_scripts/sod_merc_market_weekly_recover_guilds.py")
    player_quote = read("src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py")
    player_replenish = read("src/scripts/ZY_helper_scripts/sod_merc_player_company_try_replenish.py")
    daily_replenish = read("src/triggers/ST03_daily/entry_0122.py")
    player_wage = read("src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py")
    hire_dialog = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_hire8.py")
    hire_accept = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_hire9.py")
    weekly_payment = read("src/menus/kingdom/mercenaries_weekly_payment.py")
    pact_status = read("src/scripts/ZY_helper_scripts/merc_describe_pact_status.py")
    missed_payment = read("src/scripts/ZY_helper_scripts/sod_merc_note_missed_payment.py")
    end_pact = read("src/scripts/ZY_helper_scripts/merc_player_end_guild_pact.py")
    cancel_pact = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_pact_cancel4.py")
    cancel_warning = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_pact_cancel1.py")
    debt_pay = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_debt_1.py")
    unpaid_pay = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_unpaid.py")
    unpaid_cancel = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_unpaid2.py")
    debt_service = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_debt_service.py")
    bid = read("src/scripts/ZY_helper_scripts/sod_merc_market_generate_bid.py")
    accept = read("src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py")
    pulse = read("src/scripts/ZY_helper_scripts/sod_merc_market_weekly_pulse.py")
    ai_hire = read("src/scripts/ZI_campaign_ai/ai_hire_mercenaries.py")
    spawn = read("src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py")
    renewal_price = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_renewal_price.py")
    change_state = read("src/scripts/ZC_parties/merc_party_change_state.py")
    renew_contract = read("src/scripts/ZC_parties/sod_merc_party_try_renew_contract.py")
    reassign_contract = read("src/scripts/ZC_parties/sod_merc_party_try_reassign_contract.py")
    return_contract = read("src/scripts/ZC_parties/sod_merc_party_return_to_guild_or_disband.py")
    merc_lord_spawn = read("src/scripts/ZY_helper_scripts/sod_merc_lord_try_spawn_for_troop.py")
    merc_lord_outcome = read("src/scripts/ZY_helper_scripts/sod_merc_lord_note_battle_outcome.py")
    merc_lord_trigger = read("src/triggers/ST03_daily/entry_0129.py")
    player_victory = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    simulate_battle = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    report = read("src/scripts/ZY_helper_scripts/sod_merc_guild_describe_ledger_to_s20.py")
    guild_report = read("src/menus/0000_hardcoded_mb1011/guilds_relations_report.py")
    market_report = read("src/menus/reports/mercenary_market_report.py")
    report_submenus = read("src/menus/reports/report_submenus.py")
    status_report = read("src/menus/other/mercenary_status_report.py")
    gm_market_option = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_28.py")
    gm_market_report = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_market_report.py")
    gm_standing_report = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_standing_report.py")
    dialog_order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(demand, "slot_faction_sod_merc_demand_score")
    assert_contains(demand, "slot_faction_sod_merc_budget")
    assert_contains(demand, "slot_faction_sod_merc_max_bid")
    assert_contains(demand, "slot_faction_sod_merc_contract_urgency")
    assert_contains(demand, "script_get_number_of_factions_at_war_with_faction")
    assert_contains(demand, "slot_faction_sod_marshal_desired_followers")
    assert_contains(demand, "slot_faction_sod_marshal_current_followers")
    assert_contains(demand, "slot_faction_sod_unpaid_lord_count")
    assert_contains(demand, "spt_ai_mercenaries")
    assert_contains(demand, "spt_mercenary_lord_party")
    assert_contains(demand, "sod_merc_contract_role_field_company")
    assert_contains(demand, "sod_merc_contract_role_patrol")
    assert_contains(demand, "sod_merc_contract_role_escort")
    assert_contains(demand, "sod_merc_contract_role_garrison_support")
    assert_contains(demand, '"fac_kingdom_6"')
    assert_contains(demand, "script_sod_merc_market_calculate_village_patrol_demand")
    assert_contains(demand, "script_sod_merc_market_calculate_world_activity_pressure")
    assert_contains(demand, "sod_merc_contract_role_special_world_activity")
    assert_contains(demand, "script_sod_merc_market_select_preferred_guild")
    assert_contains(budget, "slot_troop_wealth")
    assert_contains(budget, "slot_faction_economic_strength")
    assert_contains(budget, "slot_faction_leader")
    assert_contains(budget, "desperate_cap")
    assert_contains(village_patrol, "slot_town_wealth")
    assert_contains(village_patrol, "slot_town_prosperity")
    assert_contains(village_patrol, "slot_center_sod_looter_raid_pressure")
    assert_contains(village_patrol, "slot_center_sod_looter_garrison_losses_recent")
    assert_contains(village_patrol, "script_sod_get_center_security_profile")
    assert_contains(village_patrol, "slot_party_sod_support_type")
    assert_contains(village_patrol, "sod_support_type_castle_patrol")
    assert_contains(village_patrol, "slot_faction_sod_merc_village_patrol_target")
    assert_contains(guild_weight, "store_relation")
    assert_contains(guild_weight, "slot_party_sod_merc_contract_start_day")
    assert_contains(guild_weight, "slot_party_sod_merc_contract_value")
    assert_contains(guild_weight, "slot_party_sod_merc_contract_loss_score")
    assert_contains(guild_weight, "service_days")
    assert_contains(guild_weight, "loss_penalty")
    assert_contains(preferred_guild, "script_sod_merc_market_calculate_kingdom_guild_weight")
    assert_contains(refresh, "script_sod_merc_market_calculate_kingdom_demand")
    assert_contains(refresh, '"fac_kingdom_6"')
    assert_contains(demand_report, "script_sod_merc_market_calculate_kingdom_demand")
    assert_contains(demand_report, "Village patrol pressure")
    assert_contains(demand_report, "Favored guild")
    assert_contains(market_overview, "script_sod_merc_market_refresh_kingdom_demands")
    assert_contains(market_overview, "script_sod_merc_market_describe_kingdom_demand_to_s20")
    assert_contains(market_overview, "script_sod_merc_guild_describe_ledger_to_s20")
    assert_contains(market_overview, "slot_faction_sod_merc_last_hired_guild")
    assert_contains(market_overview, "Last accepted guild")
    assert_contains(world_pressure, "slot_quest_sod_threat_sponsor_faction")
    assert_contains(world_pressure, "sod_diplomacy_memory_caravan_attack")
    assert_contains(world_pressure, "$g_sod_mini_faction_last_incident_score")
    assert_contains(world_pressure, "slot_center_sod_looter_raid_pressure")
    assert_contains(world_pressure, "slot_faction_sod_merc_world_activity_pressure")
    assert_contains(world_pressure, "slot_faction_black_army_contract_heat")
    assert_contains(world_ledger, "slot_faction_black_army_security_fund")
    assert_contains(world_ledger, "slot_faction_black_army_contract_heat")
    assert_contains(world_ledger, "slot_faction_conquistador_supply_stock")
    assert_contains(world_ledger, "slot_faction_conquistador_requisition_heat")
    assert_contains(world_ledger, "slot_faction_elephant_guard_devotion")
    assert_contains(world_ledger, "slot_faction_elephant_guard_slaver_alarm")
    assert_contains(world_ledger, "slot_faction_jotnar_hearth_pressure")
    assert_contains(world_ledger, "slot_faction_serpent_intelligence")
    assert_contains(world_ledger, "slot_faction_serpent_safe_passage")
    assert_contains(world_ledger, "slot_faction_slaver_market_demand")
    assert_contains(world_ledger, "slot_faction_slaver_market_supply")
    assert_contains(world_ledger, "slot_faction_slaver_market_heat")
    assert_contains(world_ledger, "slot_faction_boar_tribute_stock")
    assert_contains(world_ledger, "slot_faction_boar_intimidation")
    assert_contains(world_ledger, "slot_faction_sod_merc_market_reputation")
    assert_contains(world_ledger, "slot_faction_sod_merc_price_pressure")
    assert_contains(guardrails, "treasury_cap")
    assert_contains(guardrails, "manpower_cap")
    assert_contains(guardrails, "slot_faction_sod_merc_support_capacity")
    assert_contains(guardrails, "slot_faction_sod_merc_active_contracts")
    assert_contains(guardrails, "player_debt_to_faction")
    assert_contains(guardrails, "$g_sod_merc_weekly_paiment_not_paid_in_a_row")
    assert_contains(guardrails, "slot_faction_slaver_market_supply")
    assert_contains(guardrails, "slot_faction_boar_tribute_stock")
    assert_contains(supply, "slot_faction_sod_merc_support_capacity")
    assert_contains(supply, "slot_faction_sod_merc_active_contracts")
    assert_contains(supply, "slot_faction_sod_merc_price_pressure")
    assert_contains(supply, "slot_faction_sod_merc_treasury")
    assert_contains(supply, "slot_faction_sod_merc_manpower")
    assert_contains(supply, "slot_faction_sod_merc_veterans")
    assert_contains(supply, "slot_faction_sod_merc_elite_stock")
    assert_contains(supply, "slot_faction_sod_merc_risk_tolerance")
    assert_contains(supply, "slot_faction_sod_merc_market_reputation")
    assert_contains(supply, "store_relation")
    assert_contains(supply, "slot_party_sod_merc_contract_loss_score")
    assert_contains(supply, "script_sod_merc_market_calculate_world_activity_pressure")
    assert_contains(supply, "slot_faction_elephant_guard_active_parties")
    assert_contains(supply, "slot_faction_jotnar_hearth_pressure")
    assert_contains(supply, "slot_faction_serpent_route_pressure")
    assert_contains(supply, "slot_faction_serpent_safe_passage")
    assert_contains(supply, "long_contract_willingness")
    assert_contains(supply, "danger_willingness")
    assert_contains(supply, "sod_merc_refusal_low_manpower")
    assert_contains(supply, "fac_player_faction")
    assert_contains(supply, "slot_faction_merc_pact")
    assert_contains(recovery, "slot_faction_sod_merc_recovery_rate")
    assert_contains(recovery, "weekly_contract_income")
    assert_contains(recovery, "slot_faction_sod_merc_manpower")
    assert_contains(recovery, "slot_faction_sod_merc_veterans")
    assert_contains(recovery, "slot_faction_sod_merc_elite_stock")
    assert_contains(recovery, "slot_faction_sod_merc_treasury")
    assert_contains(recovery, "script_sod_merc_market_apply_world_activity_ledger")
    assert_contains(recovery, "script_sod_merc_market_apply_guardrails")
    assert_contains(recovery, "world_activity_treasury_drain")
    assert_contains(recovery, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(player_quote, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(player_quote, "slot_party_sod_merc_contract_employer")
    assert_contains(player_quote, "slot_party_sod_merc_contract_wage_rate")
    assert_contains(player_quote, "$g_sod_merc_player_hire_blocked")
    assert_contains(player_quote, "Estimated weekly wages")
    assert_contains(player_quote, "retainer does not cover payroll")
    assert_contains(player_quote, "Replenishment")
    assert_contains(player_quote, "Availability")
    assert_contains(player_quote, "script_sod_merc_market_calculate_kingdom_guild_weight")
    assert_contains(player_quote, "queue premium")
    assert_contains(player_quote, "slot_faction_sod_merc_active_contracts")
    assert_contains(player_quote, "slot_faction_sod_merc_support_capacity")
    assert_contains(player_quote, "script_sod_merc_market_apply_guardrails")
    assert_contains(player_quote, "too weak to jump the queue")
    assert_contains(player_quote, "slot_faction_sod_merc_demand_score")
    assert_contains(player_quote, "player_debt_to_faction")
    assert_contains(player_quote, "missed pact payments")
    assert_contains(player_quote, "paid pact reserves attention")
    assert_contains(player_replenish, "spt_player_mercenaries")
    assert_contains(player_replenish, "slot_faction_sod_merc_manpower")
    assert_contains(player_replenish, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(player_replenish, "sod_merc_refusal_none")
    assert_contains(player_replenish, "player_debt_to_faction")
    assert_contains(player_replenish, "$g_sod_merc_weekly_paiment_not_paid_in_a_row")
    assert_contains(player_replenish, "store_relation")
    assert_contains(daily_replenish, "script_sod_merc_player_company_try_replenish")
    assert_contains(daily_replenish, "neg|party_slot_eq, \":cur_party\", slot_party_type, spt_player_mercenaries")
    assert_contains(player_wage, "spt_player_mercenaries")
    assert_contains(hire_dialog, "The retainer")
    assert_contains(hire_dialog, "{s54}^{s55}^{s56}^{s57}^{s58}")
    assert_contains(hire_accept, "$g_sod_merc_player_hire_blocked")
    assert_contains(hire_accept, "denar retainer")
    assert_contains(weekly_payment, "script_change_player_relation_with_faction")
    assert_contains(weekly_payment, "script_sod_merc_note_missed_payment")
    assert_contains(weekly_payment, "script_sod_merc_player_try_settle_debt")
    assert_contains(weekly_payment, "pact has collapsed")
    assert_contains(missed_payment, "sod_merc_note_missed_payment")
    assert_contains(missed_payment, "sod_merc_player_try_settle_debt")
    assert_contains(missed_payment, "player_debt_to_faction")
    assert_contains(missed_payment, "$g_sod_merc_weekly_paiment_not_paid_in_a_row")
    assert_contains(missed_payment, "script_sod_merc_market_apply_guardrails")
    assert_not_contains(end_pact, "faction_set_slot, \":guild_no\", player_debt_to_faction, 0")
    assert_contains(cancel_warning, "Any debt remains")
    assert_contains(cancel_pact, "player_debt_to_faction")
    assert_contains(cancel_pact, "script_merc_player_end_guild_pact")
    assert_contains(debt_pay, "script_sod_merc_player_try_settle_debt")
    assert_contains(unpaid_pay, "script_sod_merc_player_try_settle_debt")
    assert_contains(unpaid_cancel, "script_merc_player_end_guild_pact")
    assert_contains(unpaid_cancel, "script_change_player_relation_with_faction")
    assert_contains(debt_service, "Dangerous service")
    assert_contains(pact_status, "Debt outstanding")
    assert_contains(pact_status, "Heavy debt outstanding")
    assert_contains(pact_status, "Severe arrears")
    assert_contains(pact_status, "weakens priority")
    assert_contains(bid, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(bid, "slot_faction_sod_merc_max_bid")
    assert_contains(bid, "price_pressure")
    assert_contains(bid, "hostility")
    assert_contains(bid, "$g_sod_merc_weekly_paiment_paid_in_a_row")
    assert_contains(bid, "script_sod_merc_market_calculate_kingdom_guild_weight")
    assert_contains(bid, "sod_merc_contract_role_supply_column")
    assert_contains(bid, "role_fit_score")
    assert_contains(bid, "slot_faction_black_army_contract_heat")
    assert_contains(bid, "slot_faction_conquistador_supply_stock")
    assert_contains(bid, "slot_faction_elephant_guard_slaver_alarm")
    assert_contains(bid, "slot_faction_serpent_intelligence")
    assert_contains(bid, "slot_faction_serpent_safe_passage")
    assert_contains(bid, "slot_faction_slaver_market_heat")
    assert_contains(bid, "slot_faction_boar_frontier_pressure")
    assert_contains(guild_weight, "slot_faction_economic_strength")
    assert_contains(guild_weight, "slot_faction_diplomacy_policy_slavery")
    assert_contains(guild_weight, "sod_diplomacy_policy_slavery_banned")
    assert_contains(guild_weight, "sod_diplomacy_policy_slavery_accepted")
    assert_contains(accept, "script_cf_spawn_ai_mercs")
    assert_contains(accept, "budget_reserve")
    assert_contains(accept, "budget_after_bid")
    assert_contains(accept, "slot_party_sod_merc_contract_employer")
    assert_contains(accept, "slot_party_orginal_faction")
    assert_contains(accept, "slot_party_sod_merc_contract_value")
    assert_contains(accept, "slot_faction_sod_merc_last_hired_guild")
    assert_contains(accept, "script_sod_merc_market_apply_guardrails")
    assert_contains(pulse, "script_sod_merc_guild_repair_ledgers")
    assert_contains(pulse, "script_sod_merc_market_weekly_recover_guilds")
    assert_contains(pulse, "script_sod_merc_market_refresh_kingdom_demands")
    assert_contains(pulse, "script_sod_merc_market_generate_bid")
    assert_contains(pulse, "script_sod_merc_market_try_accept_bid")
    assert_contains(pulse, "$g_sod_merc_market_last_pulse_day")
    assert_contains(ai_hire, "script_sod_merc_market_weekly_pulse")
    assert_not_contains(ai_hire, "script_cf_spawn_ai_mercs")
    assert_contains(spawn, "script_sod_merc_guild_get_roster")
    assert_contains(spawn, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(spawn, "(assign, reg0, \":mercs\")")
    assert_contains(renewal_price, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(renewal_price, "price_pressure")
    assert_contains(renewal_price, "sod_merc_refusal_overextended")
    assert_contains(change_state, "script_sod_merc_party_try_renew_contract")
    assert_contains(change_state, "script_sod_merc_party_try_reassign_contract")
    assert_contains(change_state, "script_sod_merc_party_return_to_guild_or_disband")
    assert_contains(renew_contract, "script_sod_merc_market_calculate_renewal_price")
    assert_contains(renew_contract, "slot_faction_sod_merc_budget")
    assert_contains(renew_contract, "slot_faction_sod_merc_treasury")
    assert_contains(reassign_contract, "script_sod_merc_market_calculate_kingdom_demand")
    assert_contains(reassign_contract, "script_sod_merc_market_calculate_renewal_price")
    assert_contains(return_contract, "slot_party_commander_party")
    assert_contains(return_contract, "ai_bhvr_patrol_party")
    assert_contains(return_contract, "script_sod_merc_lord_note_battle_outcome")
    assert_contains(merc_lord_trigger, "script_sod_merc_lord_try_spawn_for_troop")
    assert_contains(merc_lord_trigger, "script_sod_merc_guild_repair_ledgers")
    assert_contains(merc_lord_spawn, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(merc_lord_spawn, "slot_faction_sod_merc_support_capacity")
    assert_contains(merc_lord_spawn, "slot_faction_sod_merc_treasury")
    assert_contains(merc_lord_spawn, "slot_faction_sod_merc_veterans")
    assert_contains(merc_lord_spawn, "slot_faction_sod_merc_elite_stock")
    assert_contains(merc_lord_spawn, "slot_party_sod_merc_contract_employer")
    assert_contains(merc_lord_spawn, "sod_merc_contract_role_mercenary_lord")
    assert_contains(merc_lord_spawn, "script_sod_merc_market_calculate_kingdom_demand")
    assert_contains(merc_lord_spawn, "script_sod_merc_guild_get_roster")
    assert_contains(merc_lord_outcome, "spt_mercenary_lord_party")
    assert_contains(merc_lord_outcome, "spt_ai_mercenaries")
    assert_contains(merc_lord_outcome, "spt_player_mercenaries")
    assert_contains(merc_lord_outcome, "slot_faction_sod_merc_market_reputation")
    assert_contains(merc_lord_outcome, "slot_faction_sod_merc_manpower")
    assert_contains(merc_lord_outcome, "slot_party_sod_merc_contract_loss_score")
    assert_contains(merc_lord_outcome, "script_sod_merc_market_apply_guardrails")
    assert_contains(player_victory, "script_sod_merc_lord_note_battle_outcome")
    assert_contains(player_victory, "spt_ai_mercenaries")
    assert_contains(simulate_battle, "script_sod_merc_lord_note_battle_outcome")
    assert_contains(report, "script_sod_merc_guild_repair_ledgers")
    assert_contains(report, "Treasury {reg20}; manpower {reg21}")
    assert_contains(report, "road pressure")
    assert_contains(report, "named leaders active")
    assert_contains(report, "Top employer")
    assert_contains(report, "Player standing")
    assert_contains(report, "debt")
    assert_contains(report, "Refusing work")
    assert_contains(report, "priority")
    assert_contains(guild_report, "script_sod_merc_guild_describe_ledger_to_s20")
    assert_contains(market_report, "script_sod_merc_market_describe_overview_to_s20")
    assert_contains(market_report, "mnu_mercenary_status_report")
    assert_contains(market_report, "mnu_mercenary_world_activity_report")
    assert_contains(report_submenus, "mnu_mercenary_market_report")
    assert_contains(status_report, "mnu_mercenary_market_report")
    assert_contains(gm_market_option, "How does the contract market look")
    assert_contains(gm_market_report, "script_sod_merc_guild_describe_ledger_to_s20")
    assert_contains(gm_market_report, "player_debt_to_faction")
    assert_contains(gm_market_report, "preferential")
    assert_contains(gm_market_report, "transactional")
    assert_contains(gm_standing_report, "Market note")
    assert_contains(dialog_order, "ZZ99_misc_dialogs/anyone_plyr_gm_talk_28.py")
    assert_contains(dialog_order, "ZZ99_misc_dialogs/anyone_gm_market_report.py")


if __name__ == "__main__":
    test_mercenary_ledger_slots_and_constants_exist()
    test_all_seven_guilds_have_ledger_initialization()
    test_profile_and_predicate_helpers_cover_market_identity()
    test_weekly_rotation_uses_explicit_classic_guild_predicate()
    test_ledger_repair_tags_active_contract_parties()
    test_supply_demand_and_report_helpers_exist()
    print("test_mercenary_market_static: OK")
