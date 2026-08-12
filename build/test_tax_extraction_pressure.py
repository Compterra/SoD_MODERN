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
    profile = read("src/scripts/ZY_helper_scripts/sod_tax_extraction_profile.py")
    weekly_taxes = (
        read("src/triggers/ST04_weekly/entry_0038.py")
        + read("src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py")
    )
    weekly_wealth = read("src/triggers/ST04_weekly/entry_0016.py")
    town = read("src/scripts/ZY_helper_scripts/sod_town_market_profile.py")
    village = read("src/scripts/ZY_helper_scripts/sod_village_output_profile.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    regional = read("src/scripts/ZY_helper_scripts/sod_regional_economy_flow_profile.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    laws = read("src/scripts/ZZ_common_array_processing/sod_law_reports.py")
    town_report = read("src/menus/economy/town_market_report.py")
    regional_report = read("src/menus/economy/regional_economy_flow_report.py")
    notes = read("docs/reports/economy_settlements/tax_extraction_pressure_audit.md")

    for token in (
        '"sod_get_center_tax_extraction_profile"',
        "slot_faction_law_tax_peasants",
        "slot_faction_law_tax_townspeople",
        "slot_faction_law_tax_nobles",
        "slot_faction_law_merchant_happiness",
        "slot_faction_diplomacy_decree_war_taxes",
        "script_sod_law_calculate_trade_tax_policy",
        ":tax_revenue_pct",
        ":tax_pressure",
        ":merchant_happiness_delta",
        ":migration_retention_pct",
        ":liquidity_pct",
        ":recovery_pct",
        ":wealth_drift",
        "(val_clamp, \":tax_revenue_pct\", 60, 181)",
        "(val_clamp, \":tax_pressure\", 0, 101)",
        "(val_clamp, \":migration_retention_pct\", 45, 126)",
        "(val_clamp, \":liquidity_pct\", 45, 126)",
        "(val_clamp, \":recovery_pct\", 45, 126)",
        "(assign, reg0, \":tax_revenue_pct\")",
        "(assign, reg6, \":wealth_drift\")",
    ):
        assert_contains(profile, token)

    for raw in (weekly_taxes, weekly_wealth, town, village, population, regional):
        assert_contains(raw, "script_sod_get_center_tax_extraction_profile")

    for token in (
        ":tax_extraction_revenue_pct",
        ":tax_extraction_pressure",
        ":tax_wealth_drift",
        "script_sod_change_center_wealth",
        "script_sod_change_center_local_prosperity",
    ):
        assert_contains(weekly_taxes, token)

    for token in (
        ":tax_migration_retention_pct",
        ":tax_recovery_pct",
        ":tax_extraction_pressure",
    ):
        assert_contains(population, token)

    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68")

    assert_contains(laws, "Tax social pressure")
    assert_contains(laws, "High extraction raises immediate rents")
    assert_contains(town_report, "high extraction raises immediate revenue")
    assert_contains(regional_report, "tax extraction can fund rulers now")
    assert_contains(regional_report, "liquidity, retention, and recovery later")
    assert_contains(notes, "Tax Extraction Pressure Audit")
    assert_contains(notes, "Immediate revenue")
    assert_contains(notes, "Long-term pressure")

    print("[tax_extraction_pressure] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

