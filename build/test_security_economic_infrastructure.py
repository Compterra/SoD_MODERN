# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError("Missing expected token: %s" % needle)


def main() -> int:
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    town = read("src/scripts/ZY_helper_scripts/sod_town_market_profile.py")
    village = read("src/scripts/ZY_helper_scripts/sod_village_output_profile.py")
    caravan = read("src/scripts/ZB_economy_and_trade/cf_select_random_town_at_peace_with_faction_in_trade_route.py")
    bandits = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    town_report = read("src/menus/economy/town_market_report.py")
    regional_report = read("src/menus/economy/regional_economy_flow_report.py")
    notes = read("docs/reports/security_economic_infrastructure_audit.md")

    for token in (
        '"sod_get_center_security_economy_profile"',
        "script_sod_get_center_security_profile",
        "fac_sod_merc_guild1",
        "fac_sod_merc_guild5",
        ":contract_security",
        ":trade_security_pct",
        ":recovery_security_pct",
        ":bandit_pressure_pct",
        ":raid_damage_pct",
        ":merchant_confidence",
        ":route_security",
        "(assign, reg0, \":trade_security_pct\")",
        "(assign, reg6, \":contract_security\")",
    ):
        assert_contains(security, token)

    for raw in (town, village, caravan, bandits, recon, town_report, regional_report):
        assert_contains(raw, "script_sod_get_center_security_economy_profile")

    assert_contains(town, ":security_trade_pct")
    assert_contains(town, ":security_recovery_pct")
    assert_contains(village, ":bandit_pressure_pct")
    assert_contains(caravan, ":route_security")
    assert_contains(bandits, ":bandit_pressure_pct")
    assert_contains(recon, "Security infrastructure")
    assert_contains(town_report, "Security infrastructure")
    assert_contains(regional_report, "Security trade protection")

    assert_contains(notes, "Security Economic Infrastructure Audit")
    assert_contains(notes, "contracted Black Army and Serpent Host")
    assert_contains(notes, "trade volume")
    assert_contains(notes, "bandit pressure")

    print("[security_economic_infrastructure] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

