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
    profile = read("src/scripts/ZY_helper_scripts/sod_town_market_profile.py")
    trade = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    weekly_taxes = (
        read("src/triggers/ST04_weekly/entry_0038.py")
        + read("src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py")
    )
    weekly_wealth = read("src/triggers/ST04_weekly/entry_0016.py")
    relative_value = read("src/scripts/ZD_centers/get_center_relative_value.py")
    food_consumption = read("src/scripts/ZD_centers/center_get_food_consumption.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    recon_brief = read("src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py")
    fief_reports = read("src/menus/0000_hardcoded_mb1011/fief_reports.py")
    town_report = read("src/menus/economy/town_market_report.py")
    order = read("src/menus/_order_game_menus.txt")
    notes = read("docs/reports/economy_settlements/town_market_profile_audit.md")

    for token in (
        '"sod_get_town_market_profile"',
        "towns_begin",
        "slot_center_sod_local_population",
        "slot_center_sod_local_health",
        "slot_town_prosperity",
        "slot_center_sod_local_prosperity",
        "slot_town_wealth",
        "script_sod_get_center_food_profile",
        "script_sod_get_center_security_profile",
        "script_sod_get_village_output_profile",
        "slot_village_bound_center",
        "sod_center_modifier_trade_liquidity_flat",
        "sod_center_modifier_trade_volume_pct",
        "sod_center_modifier_tariff_income_pct",
        "sod_center_modifier_goods_import_demand_pct",
        "sod_center_modifier_goods_export_supply_pct",
        "sod_center_modifier_market_wealth_flat",
        "sod_center_modifier_market_wealth_pct",
        "sod_center_modifier_tax_efficiency_pct",
        "script_sod_get_center_tax_extraction_profile",
        ":tax_extraction_pressure",
        ":tax_liquidity_pct",
        ":tax_recovery_pct",
        "(assign, reg0, \":market_score\")",
        "(assign, reg1, \":rural_surplus\")",
        "(assign, reg2, \":consumption_pressure\")",
        "(assign, reg3, \":import_demand\")",
        "(assign, reg4, \":services\")",
        "(assign, reg5, \":recovery_rate\")",
        "(assign, reg6, \":liquidity\")",
        "(assign, reg7, \":trade_volume\")",
        "(assign, reg8, \":tariff_capture\")",
        "(assign, reg9, \":tax_reliability\")",
    ):
        assert_contains(profile, token)

    for token in (
        "script_sod_get_town_market_profile",
        ":town_import_demand",
        ":town_consumption_pressure",
        ":town_services",
        ":town_recovery_rate",
        ":town_liquidity",
        ":town_trade_volume",
        ":town_tariff_capture",
        ":town_tax_reliability",
    ):
        assert_contains(trade, token)

    assert_contains(weekly_taxes, "script_sod_get_town_market_profile")
    assert_contains(weekly_taxes, ":town_services")
    assert_contains(weekly_taxes, ":town_liquidity")
    assert_contains(weekly_taxes, ":town_tax_reliability")
    assert_contains(weekly_taxes, "script_sod_change_center_wealth")

    assert_contains(weekly_wealth, "script_sod_get_town_market_profile")
    assert_contains(weekly_wealth, ":town_rural_surplus")
    assert_contains(weekly_wealth, ":town_market_score")
    assert_contains(weekly_wealth, ":town_tax_reliability")

    assert_contains(relative_value, "script_sod_get_town_market_profile")
    assert_contains(relative_value, ":town_market_value")
    assert_contains(food_consumption, "Towns are market engines")
    assert_contains(food_consumption, ":service_consumption")
    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68")
    assert_contains(recon_brief, "script_sod_get_center_goods_market_profile")
    assert_contains(recon_brief, "Trade is steady.")

    assert_contains(fief_reports, "mnu_town_market_report")
    assert_contains(order, "economy/town_market_report.py")
    assert_contains(town_report, "Town Market Report")
    assert_contains(town_report, "market engines")
    assert_contains(town_report, "high extraction raises immediate revenue")
    assert_contains(notes, "Town Market Profile Audit")
    assert_contains(notes, "Rural surplus")
    assert_contains(notes, "Caravan trade")

    print("[town_market_profile] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

