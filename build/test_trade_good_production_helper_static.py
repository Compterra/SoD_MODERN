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
    helper = read("src/scripts/ZB_economy_and_trade/center_change_trade_good_production.py")
    normalizer = read("src/scripts/ZB_economy_and_trade/normalize_trade_good_productions.py")
    averager = read("src/scripts/ZB_economy_and_trade/average_trade_good_productions.py")

    assert_contains(helper, '"center_change_trade_good_production"')
    assert_contains(helper, "(is_between, \":center_no\", centers_begin, centers_end)")
    assert_contains(helper, "(party_is_active, \":center_no\")")
    assert_contains(helper, "(is_between, \":item_no\", trade_goods_begin, trade_goods_end)")
    assert_contains(helper, "(val_max, \":randomness\", 0)")
    assert_contains(helper, "(val_clamp, \":production_rate\", -10000, 10001)")
    assert_contains(helper, "(assign, reg0, \":production_rate\")")

    assert_contains(normalizer, "(val_clamp, \":center_production\", -10000, 10001)")

    assert_contains(averager, '"average_trade_good_productions"')
    assert_contains(averager, "(store_distance_to_party_from_party, \":cur_distance\", \":center_no\", \":other_center\")")
    assert_contains(averager, "(store_sub, \":dist_factor\", 110, \":cur_distance\")")
    assert_contains(averager, "(val_mul , \":prod_dif_change\", \":dist_factor\")")
    assert_contains(averager, "(party_set_slot, \":other_center\", \":cur_good_slot\", \":other_center_production\")")
    stale_needles = [
        "##              (is_between, \":center_no\", towns_begin, towns_end)",
        "##              (is_between, \":other_center\", towns_begin, towns_end)",
        "##              (val_mul, \":cur_distance\", 2)",
    ]
    for needle in stale_needles:
        if needle in averager:
            raise AssertionError("Stale average production distance block remains: %s" % needle)

    print("[trade_good_production_helper_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
