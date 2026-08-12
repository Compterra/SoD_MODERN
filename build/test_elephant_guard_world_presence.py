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
    party_templates = read("compile/module_party_templates.py")
    presence = read("src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py")
    director = read("src/scripts/ZY_helper_scripts/sod_world_presence_director.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    order = read("src/dialogs/_order_dialogs.txt")
    defeat_event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")

    assert_contains(constants, "slot_faction_elephant_guard_devotion")
    assert_contains(constants, "slot_faction_elephant_guard_supplies")
    assert_contains(constants, "slot_faction_elephant_guard_omens")
    assert_contains(constants, "slot_party_sod_elephant_guard_activity")
    assert_contains(constants, "sod_elephant_guard_activity_patrol")
    assert_contains(constants, "sod_elephant_guard_activity_procession")
    assert_contains(constants, "sod_world_presence_activity_contract_days")

    assert_contains(party_templates, '"elephant_guard_sanctuary_patrol"')
    assert_contains(party_templates, '"elephant_guard_relic_procession"')
    assert_contains(party_templates, "trp_elephant_guard_battle_shaman")
    assert_contains(party_templates, "fac_sod_merc_guild3")

    assert_contains(presence, '("sod_elephant_guard_update_sacred_state"')
    assert_contains(presence, '("sod_elephant_guard_configure_activity_party"')
    assert_contains(presence, '("sod_elephant_guard_spawn_world_activity"')
    assert_contains(presence, '("sod_elephant_guard_process_world_activity"')
    assert_contains(presence, '("sod_elephant_guard_describe_status_to_s21"')
    assert_contains(presence, "script_get_center_threat_level")
    assert_contains(presence, "slot_center_sod_local_health")
    assert_contains(presence, "slot_center_sod_local_population")
    assert_contains(presence, "script_change_center_prosperity")
    assert_contains(presence, "script_sod_world_presence_configure_activity_party")
    assert_contains(presence, "sod_world_presence_activity_contract_days")
    assert_contains(director, '("sod_world_presence_configure_activity_party"')
    assert_contains(director, "slot_party_orginal_faction")
    assert_contains(director, "slot_party_type, spt_ai_mercenaries")
    assert_contains(director, "slot_party_merc_contract")
    assert_contains(director, "sod_world_presence_activity_contract_days")
    assert_contains(director, '(le, ":contract_days", 0)')

    assert_contains(weekly, "script_sod_elephant_guard_spawn_world_activity")
    assert_contains(daily, "script_sod_elephant_guard_process_world_activity")
    assert_contains(notes, "script_sod_elephant_guard_describe_status_to_s21")
    for token in (
        "The Elephant Guard has",
        "{reg10}",
        "sanctuary patrols",
        "{reg11}",
        "relic processions",
        "Devotion {reg21}",
        "supplies {reg22}",
        "omens {reg23}",
    ):
        assert_contains(report, token)

    assert_contains(order, "party_tpl_pt_elephant_guard_sanctuary_patrol_start.py")
    assert_contains(order, "party_tpl_pt_elephant_guard_relic_procession_start.py")
    assert_contains(order, "anyone_elephant_guard_world_rites_about.py")
    assert_contains(defeat_event, '"pt_elephant_guard_sanctuary_patrol"')
    assert_contains(defeat_event, '"pt_elephant_guard_relic_procession"')
    assert_contains(defeat_event, 'script_change_player_relation_with_faction", "fac_sod_merc_guild3", -3')

    patrol_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_elephant_guard_sanctuary_patrol_start.py")
    procession_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_elephant_guard_relic_procession_start.py")
    about_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_elephant_guard_world_rites_about.py")
    attack_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_elephant_guard_world_talk_05.py")
    assert_contains(patrol_dialog, "pt_elephant_guard_sanctuary_patrol")
    assert_contains(procession_dialog, "pt_elephant_guard_relic_procession")
    assert_contains(about_dialog, "script_sod_elephant_guard_describe_status_to_s21")

    if "party_set_faction, \":new_party\", \":employer_faction\"" in presence:
        raise AssertionError("Elephant Guard world parties must not inherit employer faction wars")
    if "script_change_player_relation_with_faction" in attack_dialog:
        raise AssertionError("Elephant Guard attack dialogue must not apply victory consequences before combat")

    process_start = presence.index('("sod_elephant_guard_process_world_activity"')
    process_end = presence.index('("sod_elephant_guard_apply_player_support"', process_start)
    process = presence[process_start:process_end]
    assert_contains(process, 'party_get_template_id, ":template", ":party_no"')
    assert_contains(process, 'script_sod_elephant_guard_configure_activity_party", ":party_no"')

    print("[elephant_guard_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
