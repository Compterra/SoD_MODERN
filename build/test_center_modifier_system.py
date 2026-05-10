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
    constants = read("src/constants/module_constants.py")
    registry = read("src/constants/center_modifier_registry.py")
    buildings = read("src/constants/building_registry.py")
    scripts = read("src/scripts/ZI_campaign_ai/sod_center_modifiers.py")
    building_totals = read("src/scripts/ZI_campaign_ai/get_center_building_effect_totals.py")
    health = read("src/scripts/ZD_centers/get_center_ideal_health.py")
    prosperity = read("src/scripts/ZB_economy_and_trade/get_center_ideal_prosperity.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    food_limit = read("src/scripts/ZD_centers/center_get_food_store_limit.py")
    food_consumption = read("src/scripts/ZD_centers/center_get_food_consumption.py")
    recon_notes = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    caravan = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    audit = read("build/audit_center_modifier_system.py")

    for token in (
        "sod_center_modifier_trade_liquidity_flat",
        "sod_center_modifier_population_capacity_flat",
        "sod_center_modifier_raid_recovery_flat",
        "sod_center_modifier_cultural_assimilation_flat",
        "sod_center_modifier_begin",
        "sod_center_modifier_end",
    ):
        assert_contains(constants, token)

    for token in (
        "CENTER_MODIFIER_REGISTRY",
        "SUPPORTED_CENTER_MODIFIERS",
        "BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER",
        "BUILDING_FIELD_TO_CENTER_MODIFIER",
        "derive_building_center_modifiers",
        "validate_center_modifier_registry",
        "default %s is outside bounds",
        "bounds are too broad for safe runtime use",
        '"food_consumption_pct"',
        '"construction_speed_pct"',
        '"local_faith_growth_flat"',
        "0, -100, 500",
        "0, -25, 50",
        "0, 0, 10",
    ):
        assert_contains(registry, token)

    assert_contains(buildings, "center_modifiers")
    assert_contains(buildings, "modifiers")
    assert_contains(buildings, "get_building_center_modifiers")
    assert_contains(buildings, "get_building_center_modifier_value")
    assert_contains(buildings, "center modifier %s is not supported")

    assert_contains(scripts, '"sod_get_center_modifier"')
    assert_contains(scripts, '"sod_get_center_modifier_totals"')
    assert_contains(scripts, "CENTER_MODIFIER_REGISTRY")
    assert_contains(scripts, "party_slot_eq")
    assert_contains(scripts, "(gt, \":center_no\", 0)")
    assert_contains(scripts, "val_clamp")
    assert_contains(scripts, "(assign, reg0, \":population_capacity_flat\")")
    assert_contains(scripts, "(assign, reg13, \":trade_volume_pct\")")

    assert_contains(building_totals, "script_sod_get_center_modifier")
    assert_contains(building_totals, "sod_center_modifier_population_capacity_flat")
    assert_contains(building_totals, "(assign, reg11, \":population_capacity_bonus\")")

    assert_contains(health, "script_sod_get_center_modifier_totals")
    assert_contains(prosperity, "script_sod_get_center_modifier_totals")
    assert_contains(population, ":building_population_growth_pct")
    assert_contains(population, "script_sod_get_center_modifier_totals")
    assert_contains(food_limit, "sod_center_modifier_food_store_capacity_flat")
    assert_contains(food_consumption, "sod_center_modifier_food_consumption_pct")
    assert_contains(recon_notes, "script_sod_get_center_food_profile")
    assert_contains(caravan, ":center_trade_liquidity")
    assert_contains(caravan, ":center_trade_volume_pct")
    assert_contains(caravan, ":center_tariff_pct")
    assert_contains(caravan, ":center_prosperity_growth_pct")
    assert_contains(audit, "Center Modifier System Audit")

    print("[center_modifier_system] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
