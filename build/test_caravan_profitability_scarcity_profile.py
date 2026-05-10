from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text, needle, path):
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main():
    helper_path = "src/scripts/ZY_helper_scripts/sod_center_trade_demand_profile.py"
    route_path = "src/scripts/ZB_economy_and_trade/cf_select_random_town_at_peace_with_faction_in_trade_route.py"
    trade_path = "src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py"

    helper = read(helper_path)
    route = read(route_path)
    trade = read(trade_path)

    for needle in [
        "# COST: O(bound villages for towns)",
        "sod_get_center_trade_demand_profile",
        "script_sod_get_center_food_profile",
        "script_sod_get_center_security_profile",
        "script_sod_get_center_security_economy_profile",
        "script_sod_get_center_tax_extraction_profile",
        "script_sod_get_town_market_profile",
        "script_sod_get_village_output_profile",
        "script_sod_get_castle_support_profile",
        "sod_center_modifier_goods_import_demand_pct",
        "sod_center_modifier_goods_export_supply_pct",
        "sod_center_modifier_trade_liquidity_flat",
        "sod_center_modifier_trade_volume_pct",
        "(assign, reg0, \":scarcity_pressure\")",
        "(assign, reg1, \":import_demand\")",
        "(assign, reg2, \":export_supply\")",
        "(assign, reg3, \":market_liquidity\")",
        "(assign, reg4, \":security_willingness\")",
        "(assign, reg5, \":tax_friction\")",
        "(assign, reg6, \":caravan_attractiveness\")",
        "(assign, reg7, \":effective_trade_volume\")",
    ]:
        assert_contains(helper, needle, helper_path)

    for needle in [
        "script_sod_get_center_trade_demand_profile",
        ":profile_caravan_attractiveness",
        ":profile_import_demand",
        ":profile_market_liquidity",
        ":profile_security_willingness",
        ":profile_tax_friction",
        ":profile_trade_volume",
        ":profile_trade_delta",
    ]:
        assert_contains(route, needle, route_path)

    for needle in [
        "script_sod_get_center_trade_demand_profile",
        ":profile_import_demand",
        ":profile_scarcity",
        ":profile_market_liquidity",
        ":profile_security_willingness",
        ":profile_tax_friction",
        ":profile_caravan_attractiveness",
        ":profile_trade_volume",
        ":profile_liquidity_bonus",
        ":profile_recovery_bonus",
        "script_sod_get_center_goods_market_profile",
        ":goods_food_balance",
        ":goods_strategic_balance",
        ":goods_scarcity_pressure",
        ":goods_trade_willingness",
        ":goods_liquidity_pressure",
        ":goods_luxury_flow",
        ":goods_prosperity_pressure",
    ]:
        assert_contains(trade, needle, trade_path)

    print("[caravan_profitability_scarcity_profile] OK")


if __name__ == "__main__":
    main()
