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
    economy = read("src/scripts/ZY_helper_scripts/sod_center_economy_profile.py")
    caravan = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    threat = read("src/scripts/ZY_helper_scripts/sod_threat_board_apply_economy_effect.py")
    investment = read("src/scripts/ZY_helper_scripts/sod_apply_center_investment.py")
    village_state = read("src/scripts/ZD_centers/village_set_state.py")
    weekly_lords = read("src/triggers/ST04_weekly/entry_0039.py")
    weekly_centers = read("src/triggers/ST04_weekly/entry_0016.py")
    daily_garrison = read("src/triggers/ST03_daily/entry_0017.py")
    notes = read("docs/reports/wealth_prosperity_separation_audit.md")

    for token in (
        '"sod_get_center_economy_profile"',
        '"sod_change_center_wealth"',
        '"sod_change_center_local_prosperity"',
        "slot_town_wealth",
        "slot_town_prosperity",
        "slot_center_sod_local_prosperity",
        "sod_center_modifier_market_wealth_flat",
        "sod_center_modifier_market_wealth_pct",
        "script_sod_get_center_population_capacity_profile",
        "(assign, reg0, \":wealth\")",
        "(assign, reg1, \":prosperity\")",
        "(assign, reg2, \":local_prosperity\")",
        "(assign, reg3, \":liquidity_pct\")",
        "(assign, reg4, \":condition_pct\")",
        "val_clamp, \":new_wealth\", 0, 2000001",
        "val_clamp, \":new_local_prosperity\", 0, 101",
    ):
        assert_contains(economy, token)

    assert_contains(caravan, "script_sod_change_center_wealth")
    assert_contains(caravan, ":market_liquidity")
    assert_contains(caravan, "script_change_center_prosperity")

    assert_contains(threat, "script_sod_change_center_wealth")
    assert_contains(threat, "script_sod_change_center_local_prosperity")
    assert_contains(threat, "script_change_center_prosperity")

    assert_contains(investment, "script_sod_change_center_wealth")
    assert_contains(investment, "script_sod_change_center_local_prosperity")
    assert_contains(investment, "script_change_center_prosperity")

    assert_contains(village_state, ":wealth_loss")
    assert_contains(village_state, ":local_prosperity_loss")
    assert_contains(village_state, "script_sod_change_center_wealth")
    assert_contains(village_state, "script_sod_change_center_local_prosperity")
    assert_contains(village_state, "script_change_center_prosperity")

    assert_contains(weekly_lords, "script_sod_change_center_wealth")
    assert_contains(weekly_centers, ":net_wealth_change")
    assert_contains(weekly_centers, "script_sod_change_center_wealth")
    assert_contains(daily_garrison, "script_sod_get_center_economy_profile")
    assert_contains(daily_garrison, ":liquidity_pct")
    assert_contains(daily_garrison, "script_sod_get_castle_support_profile")
    assert_contains(daily_garrison, "script_sod_change_center_wealth")

    assert_contains(notes, "Wealth and Prosperity Separation Audit")
    assert_contains(notes, "liquid market capacity")
    assert_contains(notes, "long-term productivity")

    print("[wealth_prosperity_separation] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
