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
    audit = read("docs/reports/building_system_audit.md")

    for token in (
        "_merge_center_modifier_entries",
        "slot_center_has_temple",
        "slot_center_has_barracks",
        "slot_center_has_range",
        "slot_center_has_stables",
        "slot_center_has_blacksmith",
        "slot_center_has_messenger_post",
        "slot_center_has_prisoner_tower",
        "slot_center_has_guild",
        "slot_center_has_university",
        "slot_center_has_canalization",
        "slot_center_has_hospital",
        "slot_center_has_bank",
        "slot_center_has_manufacture",
    ):
        assert_contains(registry, token)

    for token in (
        '"faith_stability_flat", 12, "temple_civic_rites"',
        '"garrison_recovery_flat", 10, "barracks_mustering"',
        '"recruit_tier_bonus_flat", 1, "practice_range_basic_drill"',
        '"trade_volume_pct", 5, "stables_pack_animals"',
        '"construction_speed_pct", 14, "blacksmith_tools"',
        '"law_compliance_flat", 8, "prisoner_tower_courts"',
        '"trade_liquidity_flat", 80, "guild_market_network"',
        '"merchant_happiness_flat", 12, "guild_representation"',
        '"construction_speed_pct", 10, "university_engineers"',
        '"disease_resistance_pct", 10, "canalization_waste_control"',
        '"health_recovery_flat", 8, "hospital_physicians"',
        '"construction_cost_pct", -5, "bank_project_financing"',
        '"production_output_pct", 25, "manufacture_workshops"',
        '"market_wealth_flat", 1500, "manufacture_wages"',
    ):
        assert_contains(registry, token)

    for token in (
        "Center Modifier Sources",
        "Trade Liquidity",
        "Construction Speed %",
        "Merchant Happiness",
    ):
        assert_contains(audit, token)

    print("[town_building_development] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
