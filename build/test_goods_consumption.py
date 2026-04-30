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
    goods = read("src/scripts/ZY_helper_scripts/sod_consume_center_trade_goods.py")
    trigger = read("src/triggers/ST03_daily/entry_0155.py")
    order = read("src/triggers/_order_simple_triggers.txt")
    merchant_trade = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    price_update = read("src/scripts/ZB_economy_and_trade/update_trade_good_price_for_party.py")
    weekly_demand = read("src/triggers/ST04_weekly/entry_0019.py")

    assert_contains(goods, "sod_consume_center_trade_goods")
    assert_contains(goods, "sod_consume_all_center_trade_goods")
    assert_contains(goods, "slot_center_sod_local_population")
    assert_contains(goods, "slot_town_prosperity")
    assert_contains(goods, "slot_center_sod_local_health")
    assert_contains(goods, "slot_party_food_store")
    assert_contains(goods, "script_center_get_food_consumption")
    assert_contains(goods, "troop_remove_item")
    assert_contains(goods, "script_change_center_health")
    assert_contains(goods, "script_change_center_prosperity")
    assert_contains(goods, "itm_grain")
    assert_contains(goods, "itm_flour")
    assert_contains(goods, "itm_tools")
    assert_contains(goods, "food_begin")
    assert_contains(goods, "food_end")

    assert_contains(trigger, "script_sod_consume_all_center_trade_goods")
    assert_contains(order, "ST03_daily/entry_0155.py")

    assert_contains(merchant_trade, "troop_remove_item")
    assert_contains(price_update, "desired_stock")
    assert_contains(weekly_demand, "script_center_change_trade_good_production")

    print("[goods_consumption] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
