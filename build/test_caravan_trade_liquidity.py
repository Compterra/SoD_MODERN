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
    trade = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")

    assert_contains(trade, "slot_center_sod_local_population")
    assert_contains(trade, "slot_party_food_store")
    assert_contains(trade, "slot_center_accumulated_tariffs")
    assert_contains(trade, "script_sod_change_center_wealth")
    assert_contains(trade, "market_liquidity")
    assert_contains(trade, "import_pressure")
    assert_contains(trade, "export_pressure")
    assert_contains(trade, "scarcity_score")
    assert_contains(trade, "abundance_score")
    assert_contains(trade, "script_sod_get_center_goods_market_profile")
    assert_contains(trade, "goods_liquidity_pressure")
    assert_contains(trade, "goods_scarcity_pressure")
    assert_contains(trade, "script_change_center_prosperity")

    print("[caravan_trade_liquidity] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
