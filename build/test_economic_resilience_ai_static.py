from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def script_block(raw: str, name: str) -> str:
    start = raw.index(f'("{name}"')
    end = raw.find('\n("', start + 2)
    return raw[start:] if end < 0 else raw[start:end]


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_hourly_patrol_snapshot_prevents_per_kingdom_party_rescans() -> None:
    patrol = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_village_patrol_demand.py")
    prepare = script_block(patrol, "sod_merc_market_prepare_village_patrol_cache")
    demand = script_block(patrol, "sod_merc_market_calculate_village_patrol_demand")

    for token in (
        "store_current_hours",
        "$g_sod_merc_village_patrol_cache_initialized",
        "$g_sod_merc_village_patrol_cache_hour",
        "slot_center_sod_merc_nearby_patrol_cache",
        "try_for_parties",
        "party_is_active, \":patrol_party\"",
    ):
        assert_contains(prepare, token)
    assert_contains(demand, "script_sod_merc_market_prepare_village_patrol_cache")
    assert "try_for_parties" not in demand


def test_patrol_demand_accounts_for_food_health_and_population_crises() -> None:
    patrol = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_village_patrol_demand.py")
    demand = script_block(patrol, "sod_merc_market_calculate_village_patrol_demand")

    for token in (
        "slot_center_sod_local_health",
        "script_sod_get_center_population_capacity_profile",
        "script_sod_get_center_food_profile",
        ":critical_resilience_need",
        ":food_security_pressure",
        ":population_pressure",
        "Low-value villages still need protection",
    ):
        assert_contains(demand, token)


def test_kingdom_demand_caches_and_reports_settlement_resilience() -> None:
    constants = read("src/constants/module_constants.py")
    demand = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_demand.py")
    refresh = read("src/scripts/ZY_helper_scripts/sod_merc_market_refresh_kingdom_demands.py")
    report = read("src/scripts/ZY_helper_scripts/sod_merc_market_describe_kingdom_demand_to_s20.py")
    reassignment = read("src/scripts/ZC_parties/sod_merc_party_try_reassign_contract.py")

    for token in (
        "slot_faction_sod_merc_health_pressure",
        "slot_faction_sod_merc_food_pressure",
        "slot_faction_sod_merc_outbreak_pressure",
    ):
        assert_contains(constants, token)
        assert_contains(demand, token)
        assert_contains(refresh, token)
        assert_contains(report, token)

    assert_contains(demand, '"sod_merc_market_get_center_settlement_pressure"')
    assert_contains(demand, ":use_cached_settlement_pressure")
    assert_contains(demand, "sod_merc_contract_role_garrison_support")
    assert_contains(refresh, 'script_sod_merc_market_prepare_village_patrol_cache')
    assert_contains(refresh, 'party_is_active, ":cur_party"')
    assert_contains(demand, 'party_is_active, ":cur_party"')
    assert_contains(reassignment, 'party_is_active, ":other_party"')


def test_ai_investment_uses_shared_live_profile_and_weekly_cache() -> None:
    constants = read("src/constants/module_constants.py")
    target = read("src/scripts/ZY_helper_scripts/sod_find_investment_target.py")
    npc = read("src/scripts/ZY_helper_scripts/sod_npc_invest_in_centers.py")
    apply = read("src/scripts/ZY_helper_scripts/sod_apply_center_investment.py")

    for token in (
        "slot_center_sod_investment_need_cache",
        "slot_center_sod_investment_mode_cache",
    ):
        assert_contains(constants, token)
        assert_contains(target, token)

    for script in (
        '"sod_get_center_investment_need_profile"',
        '"sod_refresh_center_investment_profile"',
        '"sod_refresh_all_center_investment_profiles"',
        '"sod_find_cached_investment_target"',
    ):
        assert_contains(target, script)

    assert_contains(target, "script_sod_center_public_health_compute_causes")
    assert_contains(target, "script_sod_get_center_population_capacity_profile")
    assert_contains(target, "script_sod_get_center_regional_flow_profile")
    assert_contains(npc, "script_sod_refresh_all_center_investment_profiles")
    assert_contains(npc, "script_sod_find_cached_investment_target")
    assert_contains(npc, "script_sod_refresh_center_investment_profile")
    assert "script_sod_get_center_regional_flow_profile" not in npc
    assert_contains(apply, ":food_delta")
    assert_contains(apply, 'eq, ":mode", 1')
    assert_contains(apply, "script_sod_center_apply_food_delta")


def test_ai_public_health_relief_has_a_real_economic_cost() -> None:
    health = read("src/scripts/ZY_helper_scripts/sod_center_public_health.py")
    helper = script_block(health, "sod_center_public_health_get_owner_response_budget")
    response = script_block(health, "sod_center_public_health_try_owner_response")

    for token in (
        "slot_troop_wealth",
        ":available_wealth",
        ":response_budget",
        ":response_bonus",
    ):
        assert_contains(helper, token)
    assert_contains(response, "script_sod_center_public_health_get_owner_response_budget")
    assert_contains(response, "script_sod_apply_center_investment")
    assert_contains(response, 'troop_set_slot, ":lord_no", slot_troop_wealth')


def test_migration_uses_one_food_pressure_model_for_all_routes() -> None:
    migration = read("src/scripts/ZY_helper_scripts/sod_center_weekly_migration.py")

    assert_contains(migration, '"sod_center_weekly_get_food_migration_pressure"')
    assert migration.count('script_sod_center_weekly_get_food_migration_pressure') >= 2
    assert migration.count('script_sod_center_weekly_get_migration_food_adjusted_score') >= 6
    assert_contains(migration, ":src_pressure_hunger")
    assert_contains(migration, ":dest_food_capacity_ratio")


def test_ai_contract_roles_deploy_real_economic_responses() -> None:
    constants = read("src/constants/module_constants.py")
    deployment = read("src/scripts/ZY_helper_scripts/sod_merc_market_deploy_ai_contract.py")
    accept = read("src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py")
    renewal = read("src/scripts/ZC_parties/sod_merc_party_try_renew_contract.py")
    reassignment = read("src/scripts/ZC_parties/sod_merc_party_try_reassign_contract.py")
    follower_service = read("src/scripts/ZY_helper_scripts/sod_world_map_trigger_services.py")
    daily = read("src/scripts/ZY_helper_scripts/sod_merc_contract_daily.py")
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    demand = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_demand.py")

    assert_contains(constants, "slot_center_sod_merc_supply_relief_day")
    for script in (
        '"sod_merc_market_select_ai_contract_target"',
        '"sod_merc_market_deploy_ai_contract"',
        '"sod_merc_market_process_ai_contract_services"',
    ):
        assert_contains(deployment, script)
    for token in (
        "sod_merc_contract_role_patrol",
        "sod_merc_contract_role_garrison_support",
        "sod_merc_contract_role_supply_column",
        "spai_patrolling_around_center",
        "spai_holding_center",
        "script_sod_center_apply_food_delta",
        "slot_center_sod_merc_supply_relief_day",
        ":target_valid",
        ":previous_target",
    ):
        assert_contains(deployment, token)

    for caller in (accept, renewal, reassignment):
        assert_contains(caller, "script_sod_merc_market_deploy_ai_contract")
    assert_contains(reassignment, "sod_merc_market_calculate_renewal_price\", \":cur_party\", \":new_contract_role")
    assert_contains(follower_service, "Patrol, garrison, and supply contracts are independent")
    assert_contains(follower_service, "sod_merc_contract_role_special_world_activity")
    assert_contains(daily, "script_sod_merc_market_process_ai_contract_services")
    assert_contains(security, ":contract_employer")
    assert_contains(security, ":security_contribution")
    assert_contains(demand, "sod_merc_contract_role_supply_column")
