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
        'slot_center_has_chapel, "chapel", "faith", ("castle",)',
        'slot_center_has_chapter, "chapter", "military", ("castle",)',
        '"faith_ascension_bonus_flat", 8, "chapel_military_vows"',
        '"garrison_recovery_flat", 4, "chapel_morale"',
        '"noble_recruitment_flat", 3, "chapter_homeland_nobles"',
        '"administration_flat", 8, "chapter_household_officers"',
        '"garrison_recovery_flat", 6, "chapter_retinue_mustering"',
        '"garrison_upkeep_pct", -5, "barracks_orderly_lodging"',
        '"raid_resistance_pct", 5, "practice_range_wall_coverage"',
        '"threat_reduction_flat", 10, "stables_route_screens"',
    ):
        assert_contains(registry, token)

    for token in (
        "castle",
        "Garrison Recovery",
        "Noble Recruitment",
        "Faith Ascension Bonus",
        "Raid Resistance %",
    ):
        assert_contains(audit, token)

    print("[castle_building_development] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
