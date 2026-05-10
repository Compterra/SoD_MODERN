# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError("Missing expected token: %s" % needle)


def main() -> int:
    audit = read("build/audit_food_reference.py")
    report = read("docs/reports/food_reference_audit.md")
    food_profile = read("src/scripts/ZY_helper_scripts/sod_center_food_profile.py")
    consumption = read("src/scripts/ZD_centers/center_get_food_consumption.py")
    village = read("src/scripts/ZY_helper_scripts/sod_village_output_profile.py")
    town = read("src/scripts/ZY_helper_scripts/sod_town_market_profile.py")
    castle = read("src/scripts/ZY_helper_scripts/sod_castle_support_profile.py")
    trade = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    route = read("src/scripts/ZB_economy_and_trade/cf_select_random_town_at_peace_with_faction_in_trade_route.py")

    for token in (
        "Food Reference Audit",
        "Food is not just flavor",
        "Villages create the food base",
        "Towns are net consumers",
        "Castles are military consumers",
        "Caravans should see food scarcity",
        "Food Profile Outputs",
    ):
        assert_contains(report, token)

    for token in (
        "sod_get_center_food_profile",
        "center_get_food_consumption",
        "sod_consume_center_trade_goods.py",
        "sod_population_based_construction.py",
        "cf_select_random_town_at_peace_with_faction_in_trade_route.py",
    ):
        assert_contains(audit, token)

    for token in (
        "slot_party_food_store",
        "script_center_get_food_store_limit",
        "script_center_get_food_consumption",
        ":food_security",
        ":food_pressure",
        ":food_unrest_pressure",
    ):
        assert_contains(food_profile, token)

    assert_contains(consumption, "spt_town")
    assert_contains(consumption, "service_consumption")
    assert_contains(consumption, "sod_center_modifier_food_consumption_pct")
    assert_contains(village, ":food_output")
    assert_contains(village, ":cattle_output")
    assert_contains(town, ":consumption_pressure")
    assert_contains(town, ":import_demand")
    assert_contains(castle, ":food_security")
    assert_contains(trade, ":food_trade_pressure")
    assert_contains(route, ":food_security")

    print("[food_reference_audit] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
