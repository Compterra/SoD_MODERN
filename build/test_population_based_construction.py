# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError("Missing expected token: %s" % needle)


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError("Unexpected token remains: %s" % needle)


def main() -> int:
    constants = read("src/constants/module_constants.py")
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    hourly = read("src/triggers/ST02_every_hour/entry_0064.py")
    weekly = read("src/triggers/ST04_weekly/entry_0123.py")
    report_script = read("src/scripts/ZB_economy_and_trade/describe_current_project.py")
    available_report = read("src/menus/kingdom/fief_available_construction_report.py")
    presentation = read("src/presentations/0020_sod_fief_management/sod_fief_management.py")
    improve_payload = read("src/menus/other/improve_cont.py")

    for token in (
        "slot_center_construction_progress",
        "slot_center_construction_required",
        "slot_center_construction_weekly_workforce",
        "slot_center_construction_last_progress",
    ):
        assert_contains(constants, token)

    for token in (
        '"sod_get_center_construction_workforce"',
        '"sod_get_building_development_required"',
        '"sod_start_center_construction"',
        '"sod_ensure_center_construction_state"',
        '"sod_advance_center_construction"',
        '"cf_sod_complete_center_construction"',
        "slot_center_sod_local_population",
        "slot_center_sod_local_health",
        "slot_town_prosperity",
        "script_sod_get_center_food_profile",
        "script_sod_get_castle_support_profile",
        "script_sod_get_center_security_profile",
        "sod_center_modifier_construction_speed_pct",
        "party_get_num_companions",
        "(gt, \":population\", 0)",
        "(gt, \":weekly_workforce\", 0)",
        "slot_center_improvement_end_hour, 0",
    ):
        assert_contains(construction, token)

    assert_contains(hourly, "SIMPLE_TRIGGERS = []")
    assert_not_contains(hourly, "store_current_hours")
    assert_not_contains(hourly, "slot_center_improvement_end_hour")

    assert_contains(weekly, "script_sod_advance_center_construction")
    assert_contains(weekly, "script_sod_start_center_construction")
    assert_not_contains(weekly, "hours_takes")
    assert_not_contains(weekly, "store_current_hours")

    for token in (
        "slot_center_construction_progress",
        "slot_center_construction_required",
        "script_sod_get_center_construction_workforce",
        "labor per week",
        "Construction is stalled",
    ):
        assert_contains(report_script, token)

    assert_contains(available_report, "most advanced active project")
    assert_contains(available_report, "lack of usable labor")
    assert_contains(presentation, "script_sod_start_center_construction")
    assert_contains(presentation, "script_sod_get_building_development_required")
    assert_contains(presentation, "script_sod_get_center_construction_workforce")
    assert_contains(presentation, "labor per week")
    assert_not_contains(presentation, "hours_takes")
    assert_not_contains(presentation, "will take {reg10} days")

    assert_contains(improve_payload, "runtime development now advances from population/workforce")

    print("[population_based_construction] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

