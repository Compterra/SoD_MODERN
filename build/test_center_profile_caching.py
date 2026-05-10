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
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    backlog = read("docs/reports/optimization_backlog.md")

    for token in (
        "slot_center_sod_security_cache_day",
        "slot_center_sod_security_cache_effective_threat",
        "slot_center_sod_security_cache_security",
        "slot_center_sod_security_cache_threat_reduction",
        "slot_center_sod_security_cache_raid_resistance",
        "slot_center_sod_security_cache_vulnerability",
        "slot_center_sod_security_cache_contract_security",
    ):
        assert_contains(constants, token)

    for token in (
        "store_current_day",
        "slot_center_sod_security_cache_day",
        "party_slot_eq",
        "party_get_slot",
        "party_set_slot",
        "try_for_parties",
        "script_sod_get_center_food_profile",
        "script_sod_get_center_faith_profile",
    ):
        assert_contains(security, token)

    assert_contains(backlog, "Add cached center profile slots")
    assert_contains(backlog, "Optimization should preserve the modifier-driven model")

    print("[center_profile_caching] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
