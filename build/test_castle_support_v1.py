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
    profile = read("src/scripts/ZY_helper_scripts/sod_castle_support_profile.py")
    military = read("src/scripts/ZY_helper_scripts/sod_center_military_modifiers.py")
    sieges = read("src/scripts/ZE_encounters/process_sieges.py")
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    fief_reports = read("src/menus/camp/fief_reports.py")
    castle_report = read("src/menus/economy/castle_support_report.py")
    order = read("src/menus/_order_game_menus.txt")
    notes = read("docs/reports/castle_support_profile_audit.md")

    for token in (
        ":commander_quality",
        ":siege_readiness",
        ":garrison_recovery",
        ":patrol_strength",
        ":recruitment_quality",
        ":tax_reliability",
        ":village_protection",
        "slot_town_lord",
        "skl_leadership",
        "skl_tactics",
        "skl_trainer",
        "(assign, reg16, \":village_protection\")",
    ):
        assert_contains(profile, token)

    for token in (
        "script_sod_get_castle_support_profile",
        ":castle_recruitment_quality",
        ":castle_recruit_count_bonus",
        ":castle_recruit_tier_bonus",
        ":castle_noble_bonus",
        "val_add, \":garrison_recovery_flat\", reg12",
    ):
        assert_contains(military, token)

    for token in (
        ":daily_siege_hardness_decay",
        ":castle_siege_readiness",
        ":consumption_reduction",
        ":starvation_wound_chance",
        "script_sod_get_castle_support_profile",
    ):
        assert_contains(sieges, token)

    for token in (
        ":bound_castle",
        ":castle_protection",
        ":castle_patrol_response",
        "(val_sub, \":base_threat\", \":castle_protection\")",
    ):
        assert_contains(security, token)

    assert_contains(fief_reports, "mnu_castle_support_report")
    assert_contains(order, "other/castle_support_report.py")
    assert_contains(castle_report, "Castle Support Report")
    assert_contains(castle_report, "commander quality")
    assert_contains(castle_report, "siege readiness")
    assert_contains(castle_report, "scutage reliability")
    assert_contains(castle_report, "village protection")

    assert_contains(notes, "Current Castle Economy/Support Audit")
    assert_contains(notes, "Siege endurance")
    assert_contains(notes, "Nearby village protection")

    print("[castle_support_v1] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

