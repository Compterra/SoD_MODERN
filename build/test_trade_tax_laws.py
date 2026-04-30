# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    effects = read("src/scripts/ZZ_common_array_processing/sod_law_effects.py")
    trade = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    report = read("src/scripts/ZZ_common_array_processing/sod_law_reports.py")

    assert_contains(effects, "sod_law_calculate_trade_tax_policy")
    assert_contains(effects, "slot_faction_law_tax_townspeople")
    assert_contains(effects, "slot_faction_law_merchant_happiness")
    assert_contains(effects, "sod_law_low_town_taxes")
    assert_contains(effects, "sod_law_high_town_taxes")
    assert_contains(effects, "sod_law_free_cities")
    assert_contains(effects, "sod_law_mercantilism")
    assert_contains(effects, "sod_law_economic_regulations")
    assert_contains(effects, "trade_volume_modifier")
    assert_contains(effects, "tariff_modifier")

    assert_contains(trade, "script_sod_law_calculate_trade_tax_policy")
    assert_contains(trade, "trade_tax_faction")
    assert_contains(trade, "trade_tax_modifier")
    assert_contains(trade, "trade_volume_modifier")
    assert_contains(trade, "tariff_modifier")
    assert_contains(trade, "merchant_happiness_modifier")
    assert_contains(trade, "val_mul, \":trade_percent\", \":trade_volume_modifier\"")
    assert_contains(trade, "val_mul, \":tax_gain\", \":tariff_modifier\"")
    assert_contains(trade, "val_mul, \":market_liquidity\", \":trade_volume_modifier\"")
    assert_contains(trade, "val_mul, \":prosperity_chance\", \":trade_volume_modifier\"")
    assert_contains(trade, "val_mul, \":health_chance\", \":trade_volume_modifier\"")

    assert_contains(report, "script_sod_law_calculate_trade_tax_policy")
    assert_contains(report, "active_law_count")
    assert_contains(report, "Trade tax policy")
    assert_contains(report, "Tax pressure")
    assert_contains(report, "Trade volume")
    assert_contains(report, "Tariff capture")

    print("[trade_tax_laws] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
