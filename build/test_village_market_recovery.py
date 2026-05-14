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
    refresh = read("src/scripts/ZB_economy_and_trade/refresh_village_merchant_inventory.py")

    assert_contains(refresh, "slot_center_sod_local_population")
    assert_contains(refresh, "slot_center_sod_local_health")
    assert_contains(refresh, "slot_town_wealth")
    assert_contains(refresh, "recovery_factor")
    assert_contains(refresh, "merchandise_batches")
    assert_contains(refresh, "market_refresh_cost")
    assert_contains(refresh, "troop_add_merchandise")
    assert_contains(refresh, "script_sod_center_apply_wealth_delta")

    print("[village_market_recovery] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
