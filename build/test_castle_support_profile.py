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
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    relative_value = read("src/scripts/ZD_centers/get_center_relative_value.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    castle_report = read("src/menus/economy/castle_support_report.py")
    garrison = read("src/triggers/ST03_daily/entry_0107.py")
    weekly_wealth = read("src/triggers/ST04_weekly/entry_0016.py")
    food_resupply = read("src/scripts/ZD_centers/sod_center_daily_maintenance.py")
    grant = read("src/menus/centers/common/give_center_to_player_accept.py")
    confirm = read("src/menus/other/continue_19.py")
    notes = read("docs/reports/economy_settlements/castle_support_profile_audit.md")

    for token in (
        '"sod_get_castle_support_profile"',
        "castles_begin",
        "party_get_num_companions",
        "slot_village_bound_center",
        "slot_center_sod_local_population",
        "script_sod_get_village_output_profile",
        ":village_food_output",
        ":village_labor_capacity",
        ":village_recruit_capacity",
        "script_sod_get_center_food_profile",
        "sod_center_modifier_administration_flat",
        "script_sod_get_center_security_profile",
        "slot_center_has_chapter",
        "(assign, reg0, \":support_score\")",
        "(assign, reg1, \":garrison\")",
        "(assign, reg2, \":bound_population\")",
        "(assign, reg3, \":bound_villages\")",
        "(assign, reg6, \":road_control\")",
        "(assign, reg7, \":noble_access\")",
        "(assign, reg8, \":military_power\")",
        "(assign, reg9, \":honor_value\")",
        "(assign, reg10, \":commander_quality\")",
        "(assign, reg11, \":siege_readiness\")",
        "(assign, reg12, \":garrison_recovery\")",
        "(assign, reg13, \":patrol_strength\")",
        "(assign, reg14, \":recruitment_quality\")",
        "(assign, reg15, \":tax_reliability\")",
        "(assign, reg16, \":village_protection\")",
        "slot_troop_renown",
        "slot_troop_wealth",
        "skl_leadership",
        "skl_tactics",
        "skl_trainer",
    ):
        assert_contains(profile, token)

    assert_contains(construction, "script_sod_get_castle_support_profile")
    assert_contains(construction, ":castle_support")
    assert_contains(construction, ":bound_population")
    assert_contains(relative_value, "script_sod_get_castle_support_profile")
    assert_contains(relative_value, ":castle_military_power")
    assert_contains(relative_value, ":castle_honor_value")
    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68")
    assert_contains(castle_report, "Castle Support Report")
    assert_contains(castle_report, "siege readiness")
    assert_contains(castle_report, "noble chapter")
    assert_contains(castle_report, "scutage is")
    assert_contains(garrison, "script_sod_get_center_garrison_policy")
    assert_contains(garrison, ":garrison_recovery")
    assert_contains(garrison, "script_sod_get_castle_support_profile")
    assert_contains(garrison, ":castle_support_pop_equivalent")
    assert_contains(weekly_wealth, "script_sod_get_castle_support_profile")
    assert_contains(weekly_wealth, ":castle_support")
    assert_contains(weekly_wealth, ":bound_population")
    assert_contains(weekly_wealth, ":road_control")
    assert_contains(weekly_wealth, ":noble_access")
    assert_contains(weekly_wealth, ":military_power")
    assert_contains(weekly_wealth, ":tax_reliability")
    assert_contains(food_resupply, "script_sod_get_castle_support_profile")
    assert_contains(food_resupply, ":garrison")
    assert_contains(food_resupply, ":road_control")
    assert_contains(food_resupply, "script_sod_change_center_wealth")
    assert_contains(grant, "A castle grant is a high honor")
    assert_contains(confirm, "high military honor")

    assert_contains(notes, "Castle Support Profile Audit")
    assert_contains(notes, "garrison")
    assert_contains(notes, "attached villages")
    assert_contains(notes, "Noble troops")
    assert_contains(notes, "Siege endurance")
    assert_contains(notes, "tax/scutage reliability")

    print("[castle_support_profile] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

