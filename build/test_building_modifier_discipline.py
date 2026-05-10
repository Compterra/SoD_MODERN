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
    modifiers = read("src/constants/center_modifier_registry.py")
    totals = read("src/scripts/ZI_campaign_ai/get_center_building_effect_totals.py")
    audit = read("build/audit_building_system.py")
    doctor = read("build/doctor.py")

    for token in (
        "BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER",
        "BUILDING_FIELD_TO_CENTER_MODIFIER",
        "derive_building_center_modifiers(entry) + normalize_center_modifier_entries(center_modifiers)",
        "_merge_center_modifier_entries(center_modifiers)",
        "must map to a center modifier before adding scripted behavior",
        "LEGACY_BUILDING_SCRIPT_EFFECT_EXCEPTIONS",
    ):
        assert_contains(registry, token)

    for token in (
        '"weekly_relations": "relations_weekly_flat"',
        '"weekly_prosperity": "prosperity_growth_flat"',
        '"weekly_local_faith": "local_faith_growth_flat"',
        '"faith_troop_upgrade": "faith_troop_access_flat"',
        '("weekly_upkeep", "weekly_upkeep_flat")',
    ):
        assert_contains(modifiers, token)

    assert_contains(totals, "Compatibility wrapper for legacy building-effect totals")
    assert_contains(totals, "script_sod_get_center_modifier")
    assert_contains(audit, "Modifier Discipline")
    assert_contains(audit, "Script exception policy")
    assert_contains(doctor, "validate_building_registry")

    print("[building_modifier_discipline] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
