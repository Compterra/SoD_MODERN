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
    totals = read("src/scripts/ZI_campaign_ai/get_center_building_effect_totals.py")
    health = read("src/scripts/ZD_centers/get_center_ideal_health.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    audit = read("build/audit_building_system.py")
    report = read("docs/reports/building_system_audit.md")

    for token in (
        "population_capacity_bonus",
        "weekly_population_growth_bonus",
        "raid_recovery_bonus",
        "get_building_population_capacity_bonus",
        "get_building_weekly_population_growth_bonus",
        "get_building_raid_recovery_bonus",
        "SUPPORTED_BUILDING_ROLES",
        "BUILDING_ROLE_LABELS",
        "building_roles",
        "get_building_roles",
        "building_has_role",
        "get_buildings_with_role",
        "center_modifiers",
        "get_building_center_modifiers",
        "get_building_center_modifier_value",
        "LEGACY_BUILDING_SCRIPT_EFFECT_EXCEPTIONS",
        "BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER",
        "BUILDING_FIELD_TO_CENTER_MODIFIER",
        "must map to a center modifier before adding scripted behavior",
    ):
        assert_contains(registry, token)

    assert_contains(registry, "slot_center_has_hospital")
    assert_contains(registry, "population_capacity_bonus=340")
    assert_contains(registry, "slot_center_has_ambulatory")
    assert_contains(registry, "weekly_population_growth_bonus=2")
    assert_contains(registry, "slot_center_has_watch_tower")
    assert_contains(registry, "raid_recovery_bonus=1")
    assert_contains(registry, '"food_security"')
    assert_contains(registry, '"trade_liquidity"')
    assert_contains(registry, '"military_training"')
    assert_contains(registry, 'building_roles=("food_security", "production", "population_capacity", "trade_liquidity")')
    assert_contains(registry, '"construction_speed_pct", 18, "clayworks_local_materials"')

    assert_contains(totals, ":population_capacity_bonus")
    assert_contains(totals, "script_sod_get_center_modifier")
    assert_contains(totals, ":weekly_population_growth_bonus")
    assert_contains(totals, ":raid_recovery_bonus")
    assert_contains(totals, "(assign, reg11, \":population_capacity_bonus\")")
    assert_contains(totals, "(assign, reg12, \":weekly_population_growth_bonus\")")
    assert_contains(totals, "(assign, reg13, \":raid_recovery_bonus\")")

    assert_contains(health, ":building_health_bonus")
    assert_contains(health, "script_sod_get_center_population_capacity_profile")
    assert_contains(health, ":effective_pop_ideal")

    assert_contains(population, "script_sod_get_center_modifier_totals")
    assert_contains(population, ":building_population_growth_bonus")
    assert_contains(population, ":building_raid_recovery_bonus")
    assert_contains(population, ":building_population_capacity_bonus")
    assert_contains(population, "village_pop_max")
    assert_contains(population, "town_pop_max")

    assert_contains(audit, "Building System Audit")
    assert_contains(audit, "Building Role Matrix")
    assert_contains(audit, "Center Modifier Sources")
    assert_contains(audit, "Modifier Discipline")
    assert_contains(audit, "Unmapped effect tags")
    assert_contains(report, "Economy And Population Hooks")
    assert_contains(report, "Building Role Matrix")
    assert_contains(report, "Modifier Discipline")
    assert_contains(report, "Pop cap")
    assert_contains(report, "Raid recovery")

    print("[building_system_audit] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
