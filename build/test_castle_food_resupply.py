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
    restock = read("src/triggers/ST03_daily/entry_0051.py")

    assert_contains(restock, "slot_party_food_store")
    assert_contains(restock, "script_center_get_food_consumption")
    assert_contains(restock, "slot_town_wealth")
    assert_contains(restock, "slot_village_bound_center")
    assert_contains(restock, "slot_center_sod_local_population")
    assert_contains(restock, "support_population")
    assert_contains(restock, "resupply_capacity")
    assert_contains(restock, "resupply_cost")
    assert_contains(restock, "party_set_slot, \":center_no\", slot_town_wealth")

    print("[castle_food_resupply] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
