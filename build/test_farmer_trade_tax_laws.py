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
    farmer_trade = read("src/triggers/ST02_every_hour/entry_0050.py")

    assert_contains(farmer_trade, "script_sod_law_calculate_trade_tax_policy")
    assert_contains(farmer_trade, "home_trade_tax_modifier")
    assert_contains(farmer_trade, "home_trade_volume_modifier")
    assert_contains(farmer_trade, "home_tariff_modifier")
    assert_contains(farmer_trade, "market_trade_tax_modifier")
    assert_contains(farmer_trade, "market_trade_volume_modifier")
    assert_contains(farmer_trade, "market_merchant_happiness")
    assert_contains(farmer_trade, "market_tariff_modifier")
    assert_contains(farmer_trade, "farmer_trade_percent")
    assert_contains(farmer_trade, "val_mul, \":market_tariff_change\", \":market_tariff_modifier\"")
    assert_contains(farmer_trade, "val_mul, \":home_tariff_change\", \":home_tariff_modifier\"")
    assert_contains(farmer_trade, "val_mul, \":trade_food_import\", \":market_trade_volume_modifier\"")
    assert_contains(farmer_trade, "val_mul, \":market_gain_chance\", \":market_trade_volume_modifier\"")
    assert_contains(farmer_trade, "val_mul, \":village_gain_chance\", \":home_trade_volume_modifier\"")

    print("[farmer_trade_tax_laws] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
