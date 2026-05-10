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
        "sod_trade_contract_guards",
        "sod_trade_contract_cargo_space",
        "sod_trade_contract_insurance",
        "sod_trade_contract_relief",
        "sod_trade_contract_profit",
        "sod_trade_route_toll",
        "sod_trade_route_raider",
        "sod_trade_result_shortage_supplied",
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
        "No player bargain is marked on this run",
        "Your funded guards are riding with this caravan",
        "(assign, reg0, 0)",
        "(neg|party_slot_ge, \":party_no\", slot_party_sod_trade_contract, 1)",
        "your cargo stake paid",
        "your insurance claim paid",
        "your relief cargo improved local stores",
        "slot_party_sod_trade_player_protection, 0",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_black_khergit_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
        "sod_companion_action_caravan_protection",
        "sod_companion_action_trade_profit",
        "sod_companion_action_food_security",
        "sod_companion_action_dirty_profit",
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
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_busy.py"), "We already have your mark on this run")
    assert_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_trade_contract_no_gold.py"), "Insurance starts at 250 denars")
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_80.py"), "script_sod_trade_network_initialize_caravan")
    assert_contains(read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py"), "script_sod_trade_network_process_caravan_arrival")
    assert_contains(read("src/menus/reports/trade_network_report.py"), "script_sod_trade_network_describe_report_to_s20")
    assert_contains(reports, "mnu_trade_network_report")
    assert_contains(menu_order, "reports/trade_network_report.py")


if __name__ == "__main__":
    test_trade_network_core_exists()
    test_trade_network_dialogue_and_reports_exist()
    print("test_trade_network_static: OK")



