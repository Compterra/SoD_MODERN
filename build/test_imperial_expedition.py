# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    report = read("src/menus/reports/invasion_status_report.py")
    arrival = read("src/menus/other/invaders_arrived.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")

    for token in (
        "slot_faction_imperial_expedition_pressure",
        "slot_faction_imperial_expedition_supply",
        "slot_faction_imperial_expedition_front",
        "slot_faction_imperial_expedition_enemy_realms",
        "slot_faction_imperial_expedition_last_update_day",
        "slot_faction_imperial_expedition_sabotage_until",
        "sod_imperial_expedition_action_sabotage_supply",
    ):
        assert_contains(constants, token)

    for token in (
        '"sod_imperial_expedition_enforce_total_war"',
        '"sod_imperial_expedition_update_campaign_state"',
        '"sod_imperial_expedition_process_campaign"',
        '"sod_imperial_expedition_apply_player_action"',
        '"sod_imperial_expedition_count_living_vassals"',
        '"sod_imperial_expedition_describe_status_to_s28"',
        "script_set_faction_offensive_objective",
        "slot_faction_current_power",
        "Expeditionary doctrine",
        "accepts no outside mercenary pacts",
        "Bastard Brothers and Sons of Deer auxiliaries",
        "remains at war with every active realm",
        "living Centurions",
        "Gaius Marius cannot be slain while any Centurion command remains alive",
    ):
        assert_contains(scripts, token)

    assert_contains(read("src/scripts/ZI_campaign_ai/ai_hire_mercenaries.py"), '(neq, ":troop_faction", "fac_kingdom_6")')
    assert_contains(scripts, "slot_faction_merc_pact")
    assert_contains(scripts, "fac_kingdom_6_mercenaries")
    assert_contains(scripts, "script_diplomacy_start_war_between_kingdoms")
    assert_contains(daily, "script_sod_imperial_expedition_process_campaign")
    arrival_trigger = read("src/triggers/ST03_daily/entry_0088.py")
    assert_contains(arrival_trigger, "pt_legion_mercenaries")
    assert_contains(arrival_trigger, "fac_kingdom_6_mercenaries")
    assert_contains(arrival_trigger, "sfs_active")
    assert_contains(read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_plyr_chancellor_peace_2_06.py"), "(eq, 0, 1)")
    assert_contains(report, "script_sod_imperial_expedition_describe_status_to_s28")
    assert_contains(report, "sabotage_imperial_supply")
    assert_contains(report, "sod_imperial_expedition_action_sabotage_supply")
    assert_contains(report, "$g_sod_imperial_last_sabotage_day")
    assert_contains(arrival, "script_sod_imperial_expedition_describe_status_to_s28")
    assert_contains(arrival, "sabotage Imperial supply lines")
    assert_contains(notes, "script_sod_imperial_expedition_describe_status_to_s28")

    print("[imperial_expedition] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

