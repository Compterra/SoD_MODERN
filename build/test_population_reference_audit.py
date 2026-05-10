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
    audit = read("build/audit_population_reference.py")
    report = read("docs/reports/population_reference_audit.md")
    capacity = read("src/scripts/ZY_helper_scripts/sod_center_population_capacity.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    volunteers = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")
    lord_party = read("src/scripts/ZC_parties/create_kingdom_hero_party.py")

    for token in (
        "village_pop_min                 = 80",
        "village_pop_max                 = 1000",
        "town_pop_min                    = 800",
        "town_pop_max                    = 6000",
        "sod_migration_max_per_week",
    ):
        assert_contains(constants, token)

    for token in (
        "Population Reference Audit",
        "Village upper band is currently",
        "Recruitment uses population surplus",
        "Lord party creation deducts troops",
        "Town upper band",
    ):
        assert_contains(report, token)

    for token in (
        "sod_get_center_population_capacity_profile",
        "update_center_population_supply",
        "get_center_recruitable_population",
        "spend_center_population_for_recruitment",
        "create_kingdom_hero_party",
        "sod_population_based_construction.py",
    ):
        assert_contains(audit, token)

    assert_contains(capacity, "productive_population")
    assert_contains(capacity, "population_capacity_bonus")
    assert_contains(population, "script_sod_get_center_tax_extraction_profile")
    assert_contains(population, "script_sod_get_center_security_economy_profile")
    assert_contains(volunteers, "population_surplus")
    assert_contains(lord_party, "troops_created")

    print("[population_reference_audit] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
