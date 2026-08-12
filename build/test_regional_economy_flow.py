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
    profile = read("src/scripts/ZY_helper_scripts/sod_regional_economy_flow_profile.py")
    target = read("src/scripts/ZY_helper_scripts/sod_find_investment_target.py")
    npc = read("src/scripts/ZY_helper_scripts/sod_npc_invest_in_centers.py")
    apply = read("src/scripts/ZY_helper_scripts/sod_apply_center_investment.py")
    fief_reports = read("src/menus/0000_hardcoded_mb1011/fief_reports.py")
    report = read("src/menus/economy/regional_economy_flow_report.py")
    order = read("src/menus/_order_game_menus.txt")
    notes = read("docs/reports/regional_economy_flow_audit.md")

    for token in (
        '"sod_get_center_regional_flow_profile"',
        "script_sod_get_village_output_profile",
        "script_sod_get_town_market_profile",
        "script_sod_get_castle_support_profile",
        "script_sod_get_center_security_profile",
        "script_sod_get_center_food_profile",
        "script_sod_get_center_tax_extraction_profile",
        ":tax_pressure",
        ":tax_recovery_pct",
        "villages_begin",
        "towns_begin",
        "castles_begin",
        ":weakness_score",
        ":recommended_mode",
        "(assign, reg0, \":flow_score\")",
        "(assign, reg7, \":weakness_score\")",
        "(assign, reg8, \":recommended_mode\")",
        "(assign, reg9, \":recovery_strength\")",
    ):
        assert_contains(profile, token)

    assert_contains(target, "script_sod_get_center_regional_flow_profile")
    assert_contains(target, ":regional_weakness")
    assert_contains(target, "(assign, \":best_score\", -1)")
    assert_contains(target, "(gt, \":score\", \":best_score\")")

    assert_contains(npc, "script_sod_refresh_all_center_investment_profiles")
    assert_contains(npc, "script_sod_find_cached_investment_target")
    assert_contains(npc, ":investment_mode")
    assert_contains(npc, "script_sod_apply_center_investment")

    assert_contains(apply, "eq, \":mode\", 3")
    assert_contains(apply, "castle support")
    assert_contains(apply, "script_sod_center_apply_food_delta")

    assert_contains(fief_reports, "mnu_regional_economy_flow_report")
    assert_contains(order, "economy/regional_economy_flow_report.py")
    assert_contains(report, "Regional Economy Flow Report")
    assert_contains(report, "Recommended investment")
    assert_contains(report, "tax extraction")

    assert_contains(notes, "Regional Economy Flow Audit")
    assert_contains(notes, "Investment targeting")
    assert_contains(notes, "Castle investments")

    print("[regional_economy_flow] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

