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
    helpers = read("src/scripts/ZY_helper_scripts/sod_center_military_modifiers.py")
    player_recruits = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")
    npc_recruits = read("src/scripts/ZD_centers/update_npc_volunteer_troops_in_village.py")
    town_mercs = read("src/scripts/ZD_centers/update_mercenary_units_of_towns.py")
    daily = read("src/triggers/ST03_daily/entry_0107.py")
    faith_daily = read("src/triggers/ST03_daily/entry_0109.py")
    wages = read("src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py")
    upgrade_cost = read("src/scripts/ZY_helper_scripts/sod_troop_get_upgrade_cost.py")
    faith_center = read("src/scripts/ZY_helper_scripts/sod_troop_can_faith_ascend_at_center.py")
    nobles = read("src/scripts/ZY_helper_scripts/update_nobles_gather_at.py")

    for token in (
        '"sod_get_center_recruitment_policy"',
        '"sod_get_center_garrison_policy"',
        "sod_center_modifier_recruit_count_flat",
        "sod_center_modifier_recruit_tier_bonus_flat",
        "sod_center_modifier_noble_recruitment_flat",
        "sod_center_modifier_faith_troop_access_flat",
        "sod_center_modifier_faith_ascension_bonus_flat",
        "sod_center_modifier_troop_upgrade_cost_pct",
        "sod_center_modifier_garrison_recovery_flat",
        "sod_center_modifier_garrison_upkeep_pct",
    ):
        assert_contains(helpers, token)

    for raw in (player_recruits, npc_recruits):
        assert_contains(raw, "script_sod_get_center_recruitment_policy")
        assert_contains(raw, ":recruit_count_bonus")
        assert_contains(raw, ":recruit_tier_bonus")
        assert_contains(raw, "(val_add, \":upper_limit\", \":recruit_count_bonus\")")
        assert_contains(raw, "troop_get_upgrade_troop")

    assert_contains(town_mercs, "script_sod_get_center_recruitment_policy")
    assert_contains(town_mercs, "(val_add, \":amount\", reg0)")

    for token in (
        "script_sod_get_center_garrison_policy",
        ":garrison_recovery",
        ":recovery_bonus",
        ":noble_recruitment_bonus",
        ":extra_nobles",
    ):
        assert_contains(daily, token)

    assert_contains(wages, "script_sod_get_center_garrison_policy")
    assert_contains(wages, ":garrison_upkeep_pct")
    assert_contains(wages, "(val_mul, \":cur_wage\", \":garrison_upkeep_pct\")")
    assert_contains(upgrade_cost, "script_sod_get_center_recruitment_policy")
    assert_contains(upgrade_cost, ":troop_upgrade_cost_pct")
    assert_contains(faith_center, "script_sod_get_center_recruitment_policy")
    assert_contains(faith_center, "(val_add, \":effective_faith\", reg4)")
    assert_contains(faith_daily, ":faith_ascension_bonus")
    assert_contains(faith_daily, "script_sod_get_center_recruitment_policy")
    assert_contains(nobles, ":noble_recruitment_score")

    print("[recruitment_garrison_modifiers] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
