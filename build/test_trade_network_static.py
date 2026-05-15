from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def local_var_count(raw: str) -> int:
    return len({match.group(1) for match in re.finditer(r'"(:[A-Za-z0-9_]+)"', raw)})


def test_trade_network_core_exists() -> None:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    for token in (
        "slot_party_sod_trade_origin",
        "slot_party_sod_trade_destination",
        "slot_party_sod_trade_cargo_focus",
        "slot_party_sod_trade_route_risk",
        "slot_party_sod_trade_last_result",
        "slot_party_sod_trade_contract",
        "slot_party_sod_trade_captain_seed",
        "slot_party_sod_trade_house_style",
        "slot_party_sod_trade_player_trust",
        "slot_party_sod_trade_route_reputation",
        "sod_trade_contract_guards",
        "sod_trade_contract_cargo_space",
        "sod_trade_contract_insurance",
        "sod_trade_contract_relief",
        "sod_trade_contract_profit",
        "sod_trade_route_toll",
        "sod_trade_route_raider",
        "sod_trade_result_shortage_supplied",
        "sod_trade_result_taxed",
        "sod_trade_result_raided",
        "sod_trade_result_exploited",
    ):
        assert_contains(constants, token)
    for token in (
        "sod_trade_network_initialize_caravan",
        "sod_trade_network_describe_caravan_to_s20",
        "sod_trade_network_describe_route_to_s22",
        "sod_trade_network_describe_center_identity_to_s23",
        "sod_trade_network_apply_player_contract",
        "sod_trade_network_process_caravan_arrival",
        "sod_trade_network_describe_report_to_s20",
        "sod_trade_network_get_contract_terms_to_regs",
        "cf_sod_trade_network_can_apply_strategy_action",
        "sod_trade_network_apply_strategy_action",
        "No player bargain is marked on this run",
        "Your funded guards are riding with this caravan",
        "(assign, reg0, 0)",
        "(neg|party_slot_ge, \":party_no\", slot_party_sod_trade_contract, 1)",
        "your cargo stake paid",
        "your insurance claim paid",
        "your relief cargo improved local stores",
        "We remember your guards",
        "Last run paid too much at the crossings",
        "Last run had raider shadows on it",
        "Last run earned hard coin from a hungry market",
        "slot_party_sod_trade_player_protection, 0",
        "slot_party_sod_trade_player_trust",
        "slot_party_sod_trade_captain_seed",
        "slot_party_sod_trade_house_style",
        "slot_party_sod_trade_route_reputation",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_black_khergit_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
        "slot_faction_slaver_market_heat",
        "slot_faction_jotnar_hearth_pressure",
        "slot_faction_elephant_guard_slaver_alarm",
        "sod_companion_action_caravan_protection",
        "sod_companion_action_trade_profit",
        "sod_companion_action_food_security",
        "sod_companion_action_dirty_profit",
        "skl_trade",
        "skl_pathfinding",
        "skl_spotting",
        "Your scouts would read the same signs",
        "You have the eye for ledgers",
        "No offense meant",
        "not yet a name every driver knows",
        "familiar-road truth",
        "slot_center_sod_looter_raid_pressure",
        "when those villages are raided",
        "iron and tool market",
        "cattle and butter market",
        "busy caravan hub",
        "thin-stored frontier market",
        "salt-road fortress market",
        "sod_trade_network_describe_town_roots_to_s20",
    ):
        assert_contains(scripts, token)


def test_merchant_town_trade_stays_under_mb1011_local_var_limit() -> None:
    raw = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    assert local_var_count(raw) <= 120
    assert_contains(raw, '"do_merchant_town_trade"')
    assert_contains(raw, ":stock_roll")


def test_trade_network_dialogue_and_reports_exist() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    reports = read("src/menus/reports/report_submenus.py")
    menu_order = read("src/menus/_order_game_menus.txt")
    for token in (
        "anyone_plyr_merchant_talk_trade_summary.py",
        "anyone_plyr_merchant_talk_trade_route.py",
        "anyone_merchant_trade_route_intro.py",
        "anyone_plyr_merchant_talk_trade_cargo.py",
        "anyone_plyr_merchant_talk_trade_origin.py",
        "anyone_plyr_merchant_talk_trade_destination.py",
        "anyone_plyr_merchant_talk_trade_roads.py",
        "anyone_plyr_merchant_talk_trade_goods.py",
        "anyone_plyr_merchant_talk_trade_avoid.py",
        "anyone_plyr_merchant_talk_trade_protection.py",
        "anyone_plyr_merchant_trade_route_back.py",
        "anyone_plyr_merchant_talk_trade_market.py",
        "anyone_merchant_trade_market_intro.py",
        "anyone_plyr_merchant_trade_market_back.py",
        "anyone_plyr_merchant_talk_trade_contract_same_faction.py",
        "anyone_merchant_trade_contract_intro.py",
        "anyone_plyr_merchant_talk_trade_contract_foreign.py",
        "anyone_merchant_trade_contract_refused.py",
        "anyone_plyr_merchant_talk_trade_contract_busy.py",
        "anyone_plyr_merchant_talk_trade_contract_no_gold.py",
        "anyone_plyr_merchant_talk_trade_fund_guards.py",
        "anyone_plyr_merchant_talk_trade_buy_space.py",
        "anyone_plyr_merchant_talk_trade_insure.py",
        "anyone_plyr_merchant_talk_trade_relief.py",
        "anyone_plyr_merchant_talk_trade_profit.py",
        "anyone_plyr_merchant_trade_contract_back.py",
        "anyone_merchant_trade_network_answer.py",
        "anyone_plyr_goods_merchant_trade_rumor.py",
        "anyone_goods_merchant_trade_rumor.py",
        "anyone_plyr_village_elder_market_root.py",
        "anyone_village_elder_market_root.py",
        "anyone_plyr_mayor_info_trade_roots.py",
        "anyone_mayor_info_trade_roots.py",
    ):
        assert_contains(order, token)
    for path, token in (
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_summary.py", "What news travels with these wagons?"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_route.py", "Tell me about the road ahead."),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_market.py", "What are merchants saying about prices?"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_same_faction.py", "Can my company take a share in this run?"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_foreign.py", "Could my company take a share in this run?"),
    ):
        assert_contains(read(path), token)
    for path, state in (
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_origin.py", "merchant_trade_route_options"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_destination.py", "merchant_trade_route_options"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_roads.py", "merchant_trade_route_options"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_avoid.py", "merchant_trade_route_options"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_protection.py", "merchant_trade_route_options"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_cargo.py", "merchant_trade_market_options"),
        ("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_goods.py", "merchant_trade_market_options"),
    ):
        raw = read(path)
        assert_contains(raw, state)
        assert '"merchant_talk"' not in raw, f"{path} should live behind a compact submenu"
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_same_faction.py"), '(eq, "$g_encountered_party_faction", "$players_kingdom")')
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_foreign.py"), '(neg|eq, "$g_encountered_party_faction", "$players_kingdom")')
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_merchant_trade_contract_refused.py"), "I will not sell a foreign sword a place in our ledger")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_market_root.py"), "What does this village send to market?")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_market_root.py"), "script_sod_trade_network_describe_village_root_to_s20")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_trade_network.py"), "sod_trade_network_describe_village_root_to_s20")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_mayor_info_trade_roots.py"), "Which villages feed this market?")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_info_trade_roots.py"), "script_sod_trade_network_describe_town_roots_to_s20")
    for path in (
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_cargo.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_roads.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_goods.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_relief.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_profit.py",
    ):
        assert_contains(read(path), "script_sod_trade_network")
    for path in (
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_fund_guards.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_buy_space.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_insure.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_relief.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_profit.py",
    ):
        assert_contains(read(path), "slot_party_sod_trade_contract")
        assert_contains(read(path), "neg|party_slot_ge")
        assert_contains(read(path), "script_sod_trade_network_get_contract_terms_to_regs")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_busy.py"), "We already have your mark on this run")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_no_gold.py"), "script_sod_trade_network_get_contract_terms_to_regs")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_no_gold.py"), "starts near {reg0} denars")
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_80.py"), "script_sod_trade_network_initialize_caravan")
    assert_contains(read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py"), "script_sod_trade_network_process_caravan_arrival")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "script_sod_trade_network_describe_report_to_s20")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "script_sod_trade_network_apply_strategy_action")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "Fund road patrols")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "Challenge Boar toll pressure")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "Subsidize relief")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "familiar caravan route")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "script_cf_sod_trade_network_can_apply_strategy_action")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "Road orders are already moving today.")
    trade_report = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(trade_report, "$g_sod_trade_network_last_strategy_day")
    assert_contains(trade_report, 'neq, "$g_sod_trade_network_last_strategy_day", ":cur_day"')
    assert_contains(trade_report, 'store_current_day, "$g_sod_trade_network_last_strategy_day"')
    assert_contains(trade_report, "Road pressure snapshot:")
    assert_contains(trade_report, "Road recommendation:")
    assert_contains(trade_report, "Highest hostile pressure {reg28}")
    assert_contains(trade_report, "Black Khergit pressure is high")
    assert_contains(trade_report, "Boar toll pressure is high")
    assert_contains(trade_report, "captive traffic is heating the roads")
    assert_contains(read("src/menus/centers/common/center_goods_market_report.py"), "script_sod_trade_network_describe_center_identity_to_s23")
    assert_contains(read("src/menus/centers/common/center_goods_market_report.py"), "locally known as a {s23}")
    assert_contains(read("src/menus/reports/report_submenus.py"), "Read caravan road notes.")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_trade_rumor.py"), "slot_center_sod_local_health")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_trade_rumor.py"), "sickness talk")
    assert_contains(reports, "mnu_trade_network_report")
    assert_contains(menu_order, "reports/trade_network_report.py")


def test_farmer_trade_guards_home_center() -> None:
    trigger = read("src/triggers/ST02_every_hour/entry_0050.py")
    raw = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(trigger, "script_sod_trade_network_process_farmer_arrival_tick")
    assert_contains(raw, "(party_get_slot, \":home_center\", \":party_no\", slot_party_home_center)")
    assert_contains(raw, "(is_between, \":home_center\", villages_begin, villages_end)")
    assert_contains(raw, "(is_between, \":cur_center\", centers_begin, centers_end)")
    assert_contains(raw, "(is_between, \":cur_ai_object\", towns_begin, towns_end)")
    assert_contains(raw, '(call_script, "script_sod_trade_network_send_party_to_center", ":party_no", ":home_center", 0)')


def test_farmer_encounter_names_are_guarded() -> None:
    raw = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_village_farmers_start.py")
    assert_contains(raw, "(is_between, \":home_center\", villages_begin, villages_end)")
    assert_contains(raw, "(is_between, \":market_town\", towns_begin, towns_end)")
    assert_contains(raw, "a village whose road has gone wrong")
    assert_contains(raw, "the nearest market")


def test_caravan_route_risk_affects_ai_departure() -> None:
    trigger = read("src/triggers/ST02_every_hour/entry_0049.py")
    raw = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(trigger, "script_sod_trade_network_process_caravan_arrival_tick")
    assert_contains(raw, "script_sod_trade_network_evaluate_route")
    assert_contains(raw, "slot_party_sod_trade_route_risk")
    assert_contains(raw, "slot_party_sod_trade_recent_trouble")
    assert_contains(raw, ":route_departure_chance")
    assert_contains(raw, "sod_trade_result_delayed")
    assert_contains(raw, "slot_party_sod_trade_player_protection")


def test_daily_caravan_spawn_pulse_is_extracted() -> None:
    trigger = read("src/triggers/ST03_daily/entry_0165.py")
    raw = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(trigger, "script_sod_trade_network_process_daily_caravan_spawn_pulse")
    assert "try_for_range" not in trigger
    for token in [
        '"sod_trade_network_process_daily_caravan_spawn_pulse"',
        "kingdoms_begin, kingdoms_end",
        "slot_faction_state, sfs_active",
        "slot_faction_num_towns",
        "script_create_kingdom_party_if_below_limit",
        "spt_kingdom_caravan",
    ]:
        assert_contains(raw, token)


def test_daily_village_farmer_spawn_pulse_is_extracted() -> None:
    trigger = read("src/triggers/ST03_daily/entry_0047.py")
    raw = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    assert_contains(trigger, "script_sod_trade_network_process_daily_village_farmer_spawn_pulse")
    assert "try_for_range" not in trigger
    for token in [
        '"sod_trade_network_process_daily_village_farmer_spawn_pulse"',
        "villages_begin, villages_end",
        "slot_village_state, svs_normal",
        "slot_village_farmer_party",
        "neg|party_is_active",
        "(lt, \":random_no\", 30)",
        "script_create_village_farmer_party",
        "party_set_slot, \":village_no\", slot_village_farmer_party, reg0",
    ]:
        assert_contains(raw, token)


if __name__ == "__main__":
    test_trade_network_core_exists()
    test_merchant_town_trade_stays_under_mb1011_local_var_limit()
    test_trade_network_dialogue_and_reports_exist()
    test_farmer_trade_guards_home_center()
    test_farmer_encounter_names_are_guarded()
    test_caravan_route_risk_affects_ai_departure()
    test_daily_caravan_spawn_pulse_is_extracted()
    test_daily_village_farmer_spawn_pulse_is_extracted()
    print("test_trade_network_static: OK")



