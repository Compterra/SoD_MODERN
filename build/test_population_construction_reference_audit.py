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
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    audit = read("build/audit_population_construction_reference.py")
    report = read("docs/reports/population_construction_reference_audit.md")

    for token in (
        "village_pop_min                 = 80",
        "village_pop_max                 = 1000",
        "town_pop_min                    = 800",
        "town_pop_max                    = 6000",
        "sod_village_construction_pop_divisor",
        "sod_town_construction_pop_divisor",
        "sod_castle_construction_bound_pop_divisor",
        "sod_castle_construction_garrison_divisor",
        "sod_castle_construction_min_garrison_labor",
    ):
        assert_contains(constants, token)

    for token in (
        "sod_village_construction_pop_divisor",
        "sod_town_construction_pop_divisor",
        "sod_castle_construction_bound_pop_divisor",
        "sod_castle_construction_support_divisor",
        "sod_castle_construction_garrison_divisor",
        "sod_castle_construction_min_garrison_labor",
        "sod_castle_construction_workforce_cap",
        "(gt, \":population\", 0)",
        "(gt, \":garrison\", 0)",
    ):
        assert_contains(construction, token)

    assert_contains(audit, "Medieval Demographics Made Easy")
    assert_contains(audit, "Fief")
    assert_contains(audit, "Zero-population villages and towns produce no construction labor")
    assert_contains(report, "Population And Construction Reference Audit")
    assert_contains(report, "Castle garrison")

    print("[population_construction_reference_audit] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
