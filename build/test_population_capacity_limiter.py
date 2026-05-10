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
    profile = read("src/scripts/ZY_helper_scripts/sod_center_population_capacity.py")
    taxes = read("src/triggers/ST04_weekly/entry_0038.py")
    collect = read("src/menus/start_game/start_collecting.py")
    food = read("src/scripts/ZD_centers/center_get_food_consumption.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    garrison = read("src/triggers/ST03_daily/entry_0107.py")
    volunteers = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")

    for token in (
        '"sod_get_center_population_capacity_profile"',
        "slot_center_sod_local_population",
        "sod_center_modifier_population_capacity_flat",
        "village_pop_min",
        "village_pop_ideal",
        "town_pop_min",
        "town_pop_ideal",
        "slot_village_bound_center",
        "party_get_num_companions",
        "(assign, reg0, \":population\")",
        "(assign, reg1, \":population_surplus\")",
        "(assign, reg2, \":capacity_pct\")",
        "(assign, reg3, \":tax_base_pct\")",
        "(assign, reg4, \":labor_base_pct\")",
        "(assign, reg5, \":recovery_base_pct\")",
        "(assign, reg9, \":productive_population\")",
        "val_clamp, \":tax_base_pct\", 0, 126",
        "val_clamp, \":labor_base_pct\", 0, 126",
        "val_clamp, \":recovery_base_pct\", 0, 116",
    ):
        assert_contains(profile, token)

    assert_contains(taxes, "script_sod_get_center_population_capacity_profile")
    assert_contains(taxes, ":tax_capacity_pct")
    assert_contains(taxes, ":ideal_population")
    assert_contains(taxes, ":overcrowding_tax_drag")
    assert_contains(taxes, "val_mul, \":cur_rents\", \":tax_capacity_pct\"")

    assert_contains(collect, "script_sod_get_center_population_capacity_profile")
    assert_contains(collect, ":tax_capacity_pct")
    assert_contains(collect, ":productive_population")
    assert_contains(collect, "val_mul, \":tax_quest_expected_revenue\", \":tax_capacity_pct\"")
    assert_contains(collect, ":tax_capacity_drag")

    assert_contains(food, "script_sod_get_center_population_capacity_profile")
    assert_contains(food, "(assign, \":civilians\", reg9)")
    assert_contains(food, "sod_center_modifier_food_consumption_pct")

    assert_contains(population, "script_sod_get_center_population_capacity_profile")
    assert_contains(population, ":population_recovery_capacity_pct")
    assert_contains(population, "val_mul, \":population_change\", \":population_recovery_capacity_pct\"")

    assert_contains(construction, "script_sod_get_center_population_capacity_profile")
    assert_contains(construction, ":labor_base_pct")
    assert_contains(construction, "val_mul, \":workforce\", \":labor_base_pct\"")

    assert_contains(garrison, "slot_center_sod_local_population")
    assert_contains(garrison, "town_pop_min")
    assert_contains(garrison, "village_pop_min")
    assert_contains(volunteers, "slot_center_sod_local_population")
    assert_contains(volunteers, ":population_surplus")

    print("[population_capacity_limiter] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
