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
    constants = read("src/constants/module_constants.py")
    slavers = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    daily_world = read("src/triggers/ST03_daily/entry_0156.py")
    daily_burden = read("src/triggers/ST03_daily/entry_0157.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    dialogs = read("src/dialogs/_order_dialogs.txt")

    assert_contains(constants, "slot_faction_slaver_market_demand")
    assert_contains(constants, "slot_faction_slaver_market_supply")
    assert_contains(constants, "slot_faction_slaver_market_heat")
    assert_contains(constants, "slot_party_sod_slaver_web_activity")
    assert_contains(constants, "sod_slaver_action_trade_prisoners")
    assert_contains(constants, "sod_slaver_action_buy_slaves")
    assert_contains(constants, "sod_slaver_action_free_runaways")

    assert_contains(slavers, '("sod_slavers_update_market_state"')
    assert_contains(slavers, '("sod_slavers_apply_player_action"')
    assert_contains(slavers, '("sod_slavers_spawn_world_activity"')
    assert_contains(slavers, '("sod_slavers_process_world_activity"')
    assert_contains(slavers, '("sod_slavers_process_player_slave_burden"')
    assert_contains(slavers, '("sod_slavers_describe_status_to_s20"')
    assert_contains(slavers, "pt_slavers_caravan")
    assert_contains(slavers, "pt_slaves_with_jotnar_clansmen")
    assert_contains(slavers, "slot_town_slavers")
    assert_contains(slavers, "party_set_faction, \":web_party\", \"fac_sod_merc_guild6\"")
    assert_contains(slavers, "slot_party_orginal_faction, \"fac_sod_merc_guild6\"")
    assert_contains(slavers, "slot_party_starting_base, \"p_sod_merc_guild_6\"")
    assert_contains(slavers, "slot_party_type, spt_ai_mercenaries")
    assert_contains(slavers, "slot_party_merc_contract")
    assert_contains(slavers, "val_clamp, \":heat\", 0, 101")

    assert_contains(weekly, "script_sod_slavers_spawn_world_activity")
    assert_contains(daily_world, "script_sod_slavers_process_world_activity")
    assert_contains(daily_burden, "script_sod_slavers_process_player_slave_burden")
    assert_contains(notes, "script_sod_slavers_describe_status_to_s20")
    assert_contains(report, "black-market web active")
    assert_contains(report, "Demand {reg20}, supply {reg21}, heat {reg22}")
    assert_contains(read("src/menus/reports/slaver_black_market_report.py"), "Slaver Black Market Web")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/reports.py"), "mnu_slaver_black_market_report")
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/slaver_black_market_report.py")
    assert_contains(dialogs, "party_tpl_pt_runaway_slaves_start.py")
    assert_contains(dialogs, "anyone_plyr_sod_slaver_buy_slaves_confirm.py")

    if "party_set_faction, \":web_party\", \":employer_faction\"" in slavers:
        raise AssertionError("Slaver web parties must not inherit employer faction wars")

    print("[slaver_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



