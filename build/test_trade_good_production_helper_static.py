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

    assert_contains(helper, '"center_change_trade_good_production"')
    assert_contains(helper, "(is_between, \":center_no\", centers_begin, centers_end)")
    assert_contains(helper, "(party_is_active, \":center_no\")")
    assert_contains(helper, "(is_between, \":item_no\", trade_goods_begin, trade_goods_end)")
    assert_contains(helper, "(val_max, \":randomness\", 0)")
    assert_contains(helper, "(val_clamp, \":production_rate\", -10000, 10001)")
    assert_contains(helper, "(assign, reg0, \":production_rate\")")

    assert_contains(normalizer, "(val_clamp, \":center_production\", -10000, 10001)")

    print("[trade_good_production_helper_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
