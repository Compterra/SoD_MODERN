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
    defenders = read("src/scripts/ZD_centers/refresh_village_defenders.py")
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    player_volunteers = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")
    npc_volunteers = read("src/scripts/ZD_centers/update_npc_volunteer_troops_in_village.py")
    raid_attack = read("src/menus/centers/village/village_raid_attack.py")
    faction_power = read("src/scripts/ZF_factions/calculate_faction_power.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    notes = read("docs/reports/village_economic_root_audit.md")

    for token in (
        "script_sod_get_village_output_profile",
        ":village_recruit_capacity",
        ":village_labor_capacity",
        ":village_fragility",
        ":village_reliability",
        ":population_defense_bonus",
        ":population_defense_cap",
        "pt_village_defenders",
        "slot_center_sod_local_population",
    ):
        assert_contains(defenders, token)

    for token in (
        "(party_get_num_companions, \":village_garrison\", \":center_no\")",
        "slot_center_npc_volunteer_troop_amount",
        "(val_add, \":village_militia\", \":village_garrison\")",
    ):
        assert_contains(security, token)
        assert_contains(faction_power, token)

    for raw in (player_volunteers, npc_volunteers):
        assert_contains(raw, "script_sod_get_village_output_profile")
        assert_contains(raw, ":village_recruit_capacity")
        assert_contains(raw, ":village_fragility")
        assert_contains(raw, ":village_reliability")
        assert_contains(raw, "(val_min, \":upper_limit\", \":village_recruit_capacity\")")
        assert_contains(raw, "(assign, \":amount\", 0)")
        assert_contains(raw, "(gt, \":upper_limit\", 0)")

    assert_contains(raid_attack, "script_sod_get_village_output_profile")
    assert_contains(raid_attack, ":village_fragility")
    assert_contains(raid_attack, ":village_reliability")
    assert_contains(raid_attack, ":population_resistance")

    assert_contains(recon, "Village garrison")
    assert_contains(recon, "NPC militia pool")
    assert_contains(recon, "player recruit pool")
    assert_contains(recon, "party_get_num_companions, reg17")

    assert_contains(notes, "Village garrison")
    assert_contains(notes, "actual village defenders")

    print("[village_garrison_unification] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

