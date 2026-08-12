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
    normalize = read("src/scripts/ZY_helper_scripts/sod_normalize_center_population.py")
    volunteers = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")
    npc_volunteers = read("src/scripts/ZD_centers/update_npc_volunteer_troops_in_village.py")
    mercenaries = read("src/scripts/ZD_centers/update_mercenary_units_of_towns.py")
    defenders = read("src/scripts/ZD_centers/refresh_village_defenders.py")
    farmers = read("src/scripts/ZC_parties/create_village_farmer_party.py")
    recruit_cond = read("src/scripts/ZD_centers/cf_village_recruit_volunteers_cond.py")
    raid_attack = read("src/menus/centers/village/village_raid_attack.py")
    normalize_trigger = read("src/triggers/ST03_daily/entry_0154.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")

    assert_contains(population, "slot_center_sod_local_population")
    assert_contains(population, "slot_center_sod_local_health")
    assert_contains(population, "slot_center_sod_local_prosperity")
    assert_contains(population, "slot_town_prosperity")
    assert_contains(population, "slot_town_wealth")
    assert_contains(population, "script_sod_get_center_food_profile")
    assert_contains(population, ":food_security")
    assert_contains(population, ":food_pressure")
    assert_contains(population, "script_sod_normalize_center_population")
    assert_contains(population, "slot_faction_law_village_population_modifier")
    assert_contains(population, "slot_faction_law_town_population_modifier")
    assert_contains(population, "party_slot_eq, \":center_no\", slot_party_type, spt_village")
    assert_contains(population, "lt, \":health\", 20")
    assert_contains(population, "lt, \":town_prosperity\", 20")
    assert_contains(normalize, "sod_normalize_center_population")
    assert_contains(normalize, "sod_normalize_all_center_populations")
    assert_contains(normalize, "\":recovery_floor\"")
    assert_contains(normalize, "\":population_cap\"")
    assert_contains(normalize, "lt, \":population\", \":recovery_floor\"")
    assert_contains(normalize, "gt, \":population\", \":population_cap\"")
    assert_contains(normalize, "village_pop_min")
    assert_contains(normalize, "town_pop_min")
    assert_contains(normalize, "slot_center_sod_local_prosperity")
    assert_contains(normalize, "slot_town_wealth")
    assert_contains(normalize, "script_change_center_health")
    assert_contains(normalize_trigger, "script_sod_normalize_all_center_populations")
    assert_contains(trigger_order, "ST03_daily/entry_0154.py")

    assert_contains(volunteers, "slot_center_sod_local_population")
    assert_contains(volunteers, "village_pop_min")
    assert_contains(volunteers, "\":population_surplus\"")
    assert_contains(volunteers, "lt, \":population_surplus\", 80")
    assert_contains(volunteers, "ge, \":population_surplus\", 450")
    assert_contains(npc_volunteers, "slot_center_sod_local_population")
    assert_contains(npc_volunteers, "\":population_surplus\"")
    assert_contains(npc_volunteers, "slot_center_npc_volunteer_troop_amount")
    assert_contains(mercenaries, "slot_center_sod_local_population")
    assert_contains(mercenaries, "slot_center_sod_local_health")
    assert_contains(mercenaries, "slot_town_prosperity")
    assert_contains(mercenaries, "town_pop_min")
    assert_contains(mercenaries, "\":population_surplus\"")
    assert_contains(mercenaries, "ge, \":population_surplus\", 1500")
    assert_contains(mercenaries, "slot_center_mercenary_troop_amount")
    assert_contains(defenders, "slot_center_sod_local_population")
    assert_contains(defenders, "slot_center_sod_local_health")
    assert_contains(defenders, "slot_town_prosperity")
    assert_contains(defenders, "\":population_defense_bonus\"")
    assert_contains(defenders, "\":population_defense_cap\"")
    assert_contains(defenders, "pt_village_defenders")
    assert_contains(farmers, "slot_center_sod_local_population")
    assert_contains(farmers, "slot_center_sod_local_health")
    assert_contains(farmers, "slot_town_prosperity")
    assert_contains(farmers, "\":farmer_capacity\"")
    assert_contains(farmers, "party_remove_members")
    assert_contains(farmers, "remove_party")
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

