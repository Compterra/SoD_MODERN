# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    apply = read("src/scripts/ZY_helper_scripts/sod_apply_center_investment.py")
    target = read("src/scripts/ZY_helper_scripts/sod_find_investment_target.py")
    npc = read("src/scripts/ZY_helper_scripts/sod_npc_invest_in_centers.py")
    fief_menu = read("src/menus/0000_hardcoded_mb1011/fief_reports.py")
    trigger = read("src/triggers/ST04_weekly/entry_0153.py")
    order = read("src/triggers/_order_simple_triggers.txt")

    assert_contains(apply, "script_change_center_prosperity")
    assert_contains(apply, "script_change_center_health")
    assert_contains(apply, "script_sod_center_apply_population_delta")
    assert_contains(apply, "script_sod_change_center_local_prosperity")
    assert_contains(apply, "script_sod_change_center_wealth")
    assert_contains(apply, "script_sod_center_apply_cattle_delta")
    assert_contains(apply, "script_change_player_relation_with_center")

    assert_contains(target, "slot_town_lord")
    assert_contains(target, "slot_faction_leader")
    assert_contains(target, "slot_center_sod_local_health")
    assert_contains(target, "slot_town_prosperity")
    assert_contains(target, "slot_center_sod_local_population")
    assert_contains(target, "script_sod_get_center_regional_flow_profile")
    assert_contains(target, ":regional_weakness")

    assert_contains(npc, "kingdom_heroes_begin")
    assert_contains(npc, "slot_troop_wealth")
    assert_contains(npc, "script_sod_find_investment_target")
    assert_contains(npc, "script_sod_apply_center_investment")
    assert_contains(npc, "slot_faction_leader")
    assert_contains(npc, ":investment_mode")
    assert_contains(npc, ":regional_weakness")

    assert_contains(fief_menu, "invest_personal_relief")
    assert_contains(fief_menu, "invest_personal_trade")
    assert_contains(fief_menu, "invest_realm_relief")
    assert_contains(fief_menu, "mnu_regional_economy_flow_report")
    assert_contains(fief_menu, "script_sod_player_charge_gold")
    assert_contains(fief_menu, "$g_sod_weekly_construction")

    assert_contains(trigger, "script_sod_npc_invest_in_centers")
    assert_contains(order, "ST04_weekly/entry_0153.py")

    print("[center_investments] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
