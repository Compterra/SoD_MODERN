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
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    volunteers = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")
    recruit_cond = read("src/scripts/ZD_centers/cf_village_recruit_volunteers_cond.py")
    raid_attack = read("src/menus/village/village_raid_attack.py")

    assert_contains(population, "slot_center_sod_local_population")
    assert_contains(population, "slot_center_sod_local_health")
    assert_contains(population, "slot_center_sod_local_prosperity")
    assert_contains(population, "slot_town_prosperity")
    assert_contains(population, "slot_town_wealth")
    assert_contains(population, "slot_faction_law_village_population_modifier")
    assert_contains(population, "slot_faction_law_town_population_modifier")
    assert_contains(population, "party_slot_eq, \":center_no\", slot_party_type, spt_village")
    assert_contains(population, "lt, \":health\", 20")
    assert_contains(population, "lt, \":town_prosperity\", 20")

    assert_contains(volunteers, "slot_center_sod_local_population")
    assert_contains(volunteers, "village_pop_min")
    assert_contains(recruit_cond, "slot_center_sod_local_population")
    assert_contains(recruit_cond, "slot_center_volunteer_troop_amount")
    assert_contains(raid_attack, "slot_center_sod_local_population")
    assert_contains(raid_attack, "village_pop_min")
    assert_contains(raid_attack, "\":population_resistance\"")
    assert_contains(raid_attack, "\":overawe_threshold\"")
    assert_contains(raid_attack, "val_add, \":villagers_party_size\", \":population_resistance\"")

    print("[population_reactivity] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
