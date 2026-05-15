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
    helper = read("src/scripts/ZD_centers/sod_center_daily_maintenance.py")

    assert_contains(restock, "script_sod_center_process_daily_castle_food_resupply")
    assert "try_for_range" not in restock
    for token in [
        '"sod_center_process_daily_castle_food_resupply"',
        "castles_begin, castles_end",
        "slot_center_is_besieged_by, -1",
        "slot_party_food_store",
        "script_center_get_food_consumption",
        "slot_town_wealth",
        "script_sod_get_castle_support_profile",
        ":castle_support",
        ":garrison",
        ":road_control",
        "support_population",
        "resupply_capacity",
        "resupply_cost",
        "script_sod_change_center_wealth",
        "script_sod_center_apply_food_delta",
    ]:
        assert_contains(helper, token)

    print("[castle_food_resupply] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
