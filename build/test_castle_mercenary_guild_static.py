from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text, needle):
    assert needle in text, f"Missing expected text: {needle}"


def assert_not_contains(text, needle):
    assert needle not in text, f"Unexpected text: {needle}"


def test_castle_building_slot_and_registry():
    constants = read("src/constants/module_constants.py")
    registry = read("src/constants/building_registry.py")

    assert_contains(constants, "slot_center_has_mercenary_guild_hall = 159")
    assert_contains(constants, "slot_center_sod_merc_hall_troop_type = 433")
    assert_contains(constants, "slot_center_sod_merc_hall_troop_amount = 434")
    assert_contains(constants, "slot_center_sod_merc_hall_guild = 435")
    assert_contains(constants, "slot_center_sod_merc_hall_last_refresh_day = 436")
    assert_contains(constants, "slot_center_sod_merc_hall_stock_quality = 437")
    assert_contains(constants, "castle_buildings = [")
    assert_contains(constants, "slot_center_has_prisoner_tower, slot_center_has_mercenary_guild_hall]")

    assert_contains(registry, 'slot_center_has_mercenary_guild_hall, "mercenary_guild_hall", "military", ("castle",)')
    assert_contains(registry, "Mercenary Guild Hall")
    assert_contains(registry, "prerequisite_any_buildings=(slot_center_has_barracks, slot_center_has_blacksmith)")
    assert_contains(registry, '("troop_upgrade_cost_pct", -5, "mercenary_guild_hall_outfitters")')
    assert_contains(registry, "affects_castle=True")
    assert_not_contains(registry, "affects_town=True, affects_castle=True, specialization=\"military\", tier=2, weekly_upkeep=25")


def test_castle_menu_surface_exists():
    castle = read("src/menus/centers/castle/castle_castle.py")
    menu = read("src/menus/centers/castle/castle_mercenary_guild_hall.py")
    order = read("src/menus/_order_game_menus.txt")

    assert_contains(castle, '"castle_mercenary_guild_hall"')
    assert_contains(castle, "slot_center_has_mercenary_guild_hall")
    assert_contains(castle, "mnu_castle_mercenary_guild_hall")
    assert_contains(order, "centers/castle/castle_mercenary_guild_hall.py")
    assert_contains(menu, "script_sod_center_refresh_mercenary_guild_hall_stock")
    assert_contains(menu, "script_sod_center_describe_mercenary_guild_hall_to_s20")
    assert_contains(menu, "script_cf_sod_center_can_hire_mercenary_hall_troops")
    assert_contains(menu, "script_game_get_join_cost")
    assert_contains(menu, "script_sod_player_charge_gold")
    assert_contains(menu, "script_sod_center_mercenary_guild_hall_consume_stock")
    assert_contains(menu, '"castle_mercenary_guild_hall_hire_select"')
    assert_contains(menu, "(party_clear, \"p_temp_party\")")
    assert_contains(menu, "(party_add_members, \"p_temp_party\", \":troop\", \":starting_amount\")")
    assert_contains(menu, "(set_mercenary_source_party, \"p_temp_party\")")
    assert_contains(menu, "(assign, \"$g_sod_merc_hall_buy_screen_active\", 1)")
    assert_contains(menu, "(change_screen_buy_mercenaries)")
    assert_contains(menu, "(assign, \"$g_sod_merc_hall_buy_screen_active\", 0)")
    assert_contains(menu, "(party_get_num_companions, \":remaining\", \"p_temp_party\")")
    assert_contains(menu, "(party_set_slot, \"$current_town\", slot_center_sod_merc_hall_troop_amount, \":remaining\")")
    assert_contains(menu, "(val_sub, \":manpower\", \":taken\")")
    assert_not_contains(menu, "(party_add_members, \"p_main_party\"")

    join_cost = read("src/scripts/ZA_hardcoded_game_scripts/game_get_join_cost.py")
    assert_contains(join_cost, "$g_sod_merc_hall_buy_screen_active")
    assert_contains(join_cost, "(val_mul, \":join_cost\", 115)")
    assert_contains(join_cost, "(val_div, \":join_cost\", 100)")


def test_hall_scripts_are_pact_aware_and_castle_only():
    get_guild = read("src/scripts/ZY_helper_scripts/sod_center_get_mercenary_guild_for_hall.py")
    selector = read("src/scripts/ZY_helper_scripts/sod_center_select_mercenary_hall_troop.py")
    refresh = read("src/scripts/ZY_helper_scripts/sod_center_refresh_mercenary_guild_hall_stock.py")
    can_hire = read("src/scripts/ZY_helper_scripts/cf_sod_center_can_hire_mercenary_hall_troops.py")
    supports = read("src/scripts/ZY_helper_scripts/cf_sod_center_mercenary_guild_hall_supports_troop.py")

    for text in (get_guild, refresh, can_hire, supports):
        assert_contains(text, "slot_center_has_mercenary_guild_hall")
        assert_contains(text, "castles_begin, castles_end")

    assert_contains(get_guild, "slot_faction_merc_pact")
    assert_contains(get_guild, "script_cf_sod_faction_is_merc_guild")
    assert_contains(selector, "script_sod_merc_guild_get_roster")
    assert_contains(selector, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(selector, '"trp_watchman"')
    assert_contains(selector, '"trp_caravan_guard"')
    assert_contains(selector, '"trp_mercenary_crossbowman"')
    assert_contains(selector, '"trp_mercenary_swordsman"')
    assert_contains(selector, '"trp_mercenary_horseman"')
    assert_not_contains(selector, '"trp_hired_blade"')
    assert_contains(refresh, "slot_center_sod_merc_hall_last_refresh_day")
    assert_contains(refresh, "slot_center_sod_merc_hall_stock_quality")
    assert_contains(refresh, "script_sod_get_center_security_profile")
    assert_contains(refresh, "slot_center_sod_local_health")
    assert_contains(refresh, "slot_center_is_besieged_by")
    assert_contains(refresh, "player_debt_to_faction")
    assert_contains(refresh, '":stored_guild"')
    assert_contains(supports, "slot_faction_merc_pact")
    assert_contains(supports, '(eq, ":pact_guild", ":troop_faction")')
    assert_contains(supports, "slot_center_is_besieged_by")
    assert_contains(supports, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(supports, "sod_merc_refusal_none")
    assert_contains(can_hire, "slot_center_is_besieged_by")


def test_upgrade_permission_uses_hall_exception_for_pact_guilds():
    upgrade = read("src/scripts/ZY_helper_scripts/sod_troop_can_upgrade_at_center.py")

    assert_contains(upgrade, "script_cf_sod_center_mercenary_guild_hall_supports_troop")
    assert_contains(upgrade, 'script_cf_sod_faction_is_merc_guild", ":troop_faction"')
    assert_contains(upgrade, '":merc_hall_supports_troop"')
    assert_contains(upgrade, 'sod_upgrade_fail_wrong_faction')


def test_hiring_drains_pact_manpower_and_reports_surface_halls():
    consume = read("src/scripts/ZY_helper_scripts/sod_center_mercenary_guild_hall_consume_stock.py")
    market = read("src/scripts/ZY_helper_scripts/sod_merc_market_describe_overview_to_s20.py")
    ledger = read("src/scripts/ZY_helper_scripts/sod_merc_guild_describe_ledger_to_s20.py")
    fiefs = read("src/menus/0000_hardcoded_mb1011/fief_reports.py")
    supply = read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_guild_supply.py")

    assert_contains(consume, "script_cf_sod_center_can_hire_mercenary_hall_troops")
    assert_contains(consume, "party_add_members")
    assert_contains(consume, "slot_faction_sod_merc_manpower")
    assert_contains(consume, "(val_sub, \":manpower\", \":taken\")")
    assert_contains(consume, "(val_max, \":manpower\", 0)")
    assert_contains(market, "Castle mercenary guild halls")
    assert_contains(market, "script_sod_count_mercenary_guild_halls_for_faction")
    assert_contains(ledger, "Castle halls backing this guild")
    assert_contains(ledger, "script_sod_count_mercenary_guild_halls_for_guild")
    assert_contains(fiefs, "script_sod_describe_player_mercenary_guild_halls_to_s20")
    assert_contains(fiefs, "Mercenary Guild Halls")
    assert_contains(supply, "script_sod_count_mercenary_guild_halls_for_guild")
    assert_contains(supply, '":hall_capacity_bonus"')


def test_ai_lord_hall_reinforcement_is_local_and_stock_limited():
    helper = read("src/scripts/ZY_helper_scripts/sod_lord_try_reinforce_from_mercenary_guild_hall.py")
    reinforce = read("src/scripts/ZC_parties/cf_reinforce_party.py")
    playtest = read("docs/CASTLE_MERCENARY_GUILD_PLAYTEST_CHECKLIST.md")

    assert_contains(helper, "party_get_attached_to")
    assert_contains(helper, "slot_center_has_mercenary_guild_hall")
    assert_contains(helper, "slot_center_is_besieged_by")
    assert_contains(helper, "(eq, \":lord_faction\", \":center_faction\")")
    assert_contains(helper, "script_sod_center_refresh_mercenary_guild_hall_stock")
    assert_contains(helper, "slot_center_sod_merc_hall_troop_amount")
    assert_contains(helper, "script_sod_center_mercenary_guild_hall_consume_stock")
    assert_not_contains(helper, "party_add_members")
    assert_contains(helper, "(val_min, \":need\", 3)")
    assert_contains(reinforce, "script_sod_lord_try_reinforce_from_mercenary_guild_hall")
    assert_contains(reinforce, "script_sod_merc_market_calculate_guild_supply")
    assert_contains(reinforce, "sod_merc_refusal_none")
    assert_contains(playtest, "AI Behavior")
    assert_contains(playtest, "Castle Mercenary Guild Hall Playtest Checklist")


def test_status_text_covers_siege_shutdown():
    describe = read("src/scripts/ZY_helper_scripts/sod_center_describe_mercenary_guild_hall_to_s20.py")

    assert_contains(describe, "slot_center_is_besieged_by")
    assert_contains(describe, "shuttered while the castle is under siege")


if __name__ == "__main__":
    test_castle_building_slot_and_registry()
    test_castle_menu_surface_exists()
    test_hall_scripts_are_pact_aware_and_castle_only()
    test_upgrade_permission_uses_hall_exception_for_pact_guilds()
    test_hiring_drains_pact_manpower_and_reports_surface_halls()
    test_ai_lord_hall_reinforcement_is_local_and_stock_limited()
    test_status_text_covers_siege_shutdown()
    print("castle mercenary guild hall static checks passed")
