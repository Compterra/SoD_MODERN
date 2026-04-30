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
    fief_menu = read("src/menus/camp/fief_reports.py")
    trigger = read("src/triggers/ST04_weekly/entry_0153.py")
    order = read("src/triggers/_order_simple_triggers.txt")

    assert_contains(apply, "script_change_center_prosperity")
    assert_contains(apply, "script_change_center_health")
    assert_contains(apply, "slot_center_sod_local_population")
    assert_contains(apply, "slot_center_sod_local_prosperity")
    assert_contains(apply, "slot_town_wealth")
    assert_contains(apply, "slot_village_number_of_cattle")
    assert_contains(apply, "script_change_player_relation_with_center")

    assert_contains(target, "slot_town_lord")
    assert_contains(target, "slot_faction_leader")
    assert_contains(target, "slot_center_sod_local_health")
    assert_contains(target, "slot_town_prosperity")
    assert_contains(target, "slot_center_sod_local_population")

    assert_contains(npc, "kingdom_heroes_begin")
    assert_contains(npc, "slot_troop_wealth")
    assert_contains(npc, "script_sod_find_investment_target")
    assert_contains(npc, "script_sod_apply_center_investment")
    assert_contains(npc, "slot_faction_leader")

    assert_contains(fief_menu, "invest_personal_relief")
    assert_contains(fief_menu, "invest_personal_trade")
    assert_contains(fief_menu, "invest_realm_relief")
    assert_contains(fief_menu, "troop_remove_gold")
    assert_contains(fief_menu, "$g_sod_weekly_construction")

    assert_contains(trigger, "script_sod_npc_invest_in_centers")
    assert_contains(order, "ST04_weekly/entry_0153.py")

    print("[center_investments] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
