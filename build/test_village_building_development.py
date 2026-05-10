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
    registry = read("src/constants/building_registry.py")
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    validation = read("src/scripts/ZI_campaign_ai/validate_construction_choice.py")

    for token in (
        "derive_building_center_modifiers(entry) + normalize_center_modifier_entries(center_modifiers)",
        "_merge_center_modifier_entries(center_modifiers)",
        "slot_center_has_manor",
        "slot_center_has_mill",
        "slot_center_has_watch_tower",
        "slot_center_has_inn",
        "slot_center_has_shrine",
        "slot_center_has_monastery",
        "slot_center_has_messenger_post",
        "slot_center_has_water_supply",
        "slot_center_has_ambulatory",
        "slot_center_has_clayworks",
        "slot_center_has_rustic_blacksmith",
        "slot_center_has_militia_yard",
        "slot_center_has_beacon_hill",
        "slot_center_has_granary",
        "slot_center_has_militia_armory",
    ):
        assert_contains(registry, token)

    for token in (
        '"construction_speed_pct", 10, "manor_work_coordination"',
        '"food_security_flat", 30, "mill_food_processing"',
        '"food_store_capacity_flat", 120, "mill_storage"',
        '"security_flat", 15, "watch_tower_alarm_network"',
        '"trade_liquidity_flat", 25, "inn_travel_trade"',
        '"migration_attraction_flat", 8, "inn_returning_families"',
        '"faith_stability_flat", 8, "shrine_local_rites"',
        '"population_recovery_flat", 2, "monastery_refuge"',
        '"construction_speed_pct", 6, "messenger_post_work_orders"',
        '"disease_resistance_pct", 8, "water_supply_clean_water"',
        '"health_recovery_flat", 6, "ambulatory_treatment"',
        '"construction_speed_pct", 18, "clayworks_local_materials"',
        '"construction_speed_pct", 12, "rustic_blacksmith_tools"',
        '"garrison_recovery_flat", 10, "militia_yard_muster_rolls"',
        '"recruit_count_flat", 1, "militia_yard_drill_call"',
        '"warning_range_flat", 1, "beacon_hill_signal_fire"',
        '"patrol_response_pct", 12, "beacon_hill_runner_paths"',
        '"food_store_capacity_flat", 180, "granary_reserve_bins"',
        '"food_security_flat", 25, "granary_seed_reserve"',
        '"recruit_tier_bonus_flat", 1, "militia_armory_levy_gear"',
        '"garrison_recovery_flat", 4, "militia_armory_repair_tools"',
        "prerequisite_any_buildings=(slot_center_has_rustic_blacksmith, slot_center_has_manor)",
    ):
        assert_contains(registry, token)

    for token in (
        "sod_center_modifier_construction_speed_pct",
        "slot_center_sod_local_population",
        "slot_center_sod_local_health",
        "slot_town_prosperity",
        "sod_center_modifier_security_flat",
    ):
        assert_contains(construction, token)

    for token in (
        "prerequisite_any_buildings",
        ":any_prereq_ok",
        "BUILDING_VALIDATION_MISSING_PREREQUISITE",
    ):
        assert_contains(validation, token)

    print("[village_building_development] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
