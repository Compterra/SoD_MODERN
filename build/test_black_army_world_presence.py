# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    party_templates = read("compile/module_party_templates.py")
    presence = read("src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    faction_notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    order = read("src/dialogs/_order_dialogs.txt")
    player_victory_event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")

    for token in (
        "slot_faction_black_army_security_fund",
        "slot_faction_black_army_contract_heat",
        "sod_black_army_action_security_contract",
        "sod_black_army_action_hire_patrol",
        "sod_black_army_action_attack_patrol",
    ):
        assert_contains(constants, token)

    assert_contains(party_templates, '"black_army_patrol"')
    assert_contains(party_templates, '"black_army_contract_column"')
    assert_contains(party_templates, "fac_sod_merc_guild1")
    assert_contains(party_templates, "trp_black_army_raven_captain")
    assert_contains(party_templates, "trp_black_army_line_supporter")
    assert_contains(party_templates, "trp_black_army_line_crusher")

    assert_contains(presence, '("sod_black_army_world_presence"')
    assert_contains(presence, "pt_black_army_patrol")
    assert_contains(presence, "pt_black_army_contract_column")
    assert_contains(presence, "fac_sod_merc_guild1")
    assert_contains(presence, "p_sod_merc_guild_1")
    assert_contains(presence, "slot_faction_merc_pact")
    assert_contains(presence, "slot_party_orginal_faction")
    assert_contains(presence, "spt_ai_mercenaries")
    assert_contains(presence, "party_get_template_id")
    assert_contains(presence, "script_party_set_ai_state")
    assert_contains(presence, "spai_patrolling_around_center")
    assert_contains(presence, "slot_party_merc_contract")
    assert_contains(presence, "script_get_center_threat_level")
    assert_contains(presence, "centers_begin, centers_end")
    assert_contains(presence, "slot_village_state")
    assert_contains(presence, "svs_looted")
    assert_contains(presence, "svs_deserted")
    assert_contains(presence, "slot_center_sod_local_population")
    assert_contains(presence, "slot_center_sod_local_health")
    assert_contains(presence, "slot_town_prosperity")
    assert_contains(presence, "slot_town_wealth")
    assert_contains(presence, "village_pop_min")
    assert_contains(presence, "town_pop_min")
    assert_contains(presence, "val_clamp, \":target_limit\", 2, 5")
    assert_contains(presence, '("sod_black_army_apply_player_action"')
    assert_contains(presence, '("sod_black_army_describe_status_to_s24"')
    assert_contains(presence, "slot_party_sod_slaver_web_activity")
    assert_contains(presence, "slot_party_sod_boar_frontier_activity")
    assert_contains(presence, "native_kingdoms_begin, native_kingdoms_end")
    if "try_for_range, \":cur_faction\", kingdoms_begin, kingdoms_end" in presence:
        raise AssertionError("Black Army employer scans should use native kingdom range")

    assert_contains(spawns, 'call_script, "script_sod_black_army_world_presence"')
    assert_contains(report, "script_sod_black_army_describe_status_to_s24")
    assert_contains(report, "road-security network active")
    assert_contains(faction_notes, "script_sod_black_army_describe_status_to_s24")
    assert_contains(faction_notes, "fac_sod_merc_guild1")
    assert_contains(order, "party_tpl_pt_black_army_patrol_start.py")
    assert_contains(order, "party_tpl_pt_black_army_contract_column_start.py")
    assert_contains(order, "anyone_plyr_black_army_world_patrol_talk_04.py")
    assert_contains(order, "anyone_plyr_black_army_world_patrol_talk_05.py")
    attack_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_army_world_patrol_talk_03.py")
    assert_contains(attack_dialog, "encounter_attack")
    assert_not_contains(attack_dialog, "sod_black_army_action_attack_patrol")
    assert_contains(player_victory_event, "pt_black_army_patrol")
    assert_contains(player_victory_event, "pt_black_army_contract_column")
    assert_contains(player_victory_event, "sod_black_army_action_attack_patrol")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_army_world_patrol_talk_04.py"), "sod_black_army_action_security_contract")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_army_world_patrol_talk_05.py"), "sod_black_army_action_hire_patrol")
    assert_contains(read("src/menus/reports/black_army_security_report.py"), "Black Army Contract Security")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/reports.py"), "mnu_mini_faction_reports")
    assert_contains(read("src/menus/reports/report_submenus.py"), "mnu_black_army_security_report")
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/black_army_security_report.py")

    patrol_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_army_patrol_start.py")
    column_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_army_contract_column_start.py")
    about_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_army_world_patrol_about.py")
    assert_contains(patrol_dialog, "pt_black_army_patrol")
    assert_contains(column_dialog, "pt_black_army_contract_column")
    assert_contains(about_dialog, "slot_faction_merc_pact")
    assert_contains(about_dialog, "fac_sod_merc_guild1")
    assert_contains(about_dialog, "native_kingdoms_begin, native_kingdoms_end")

    if "party_set_faction, \":new_party\", \":employer_faction\"" in presence:
        raise AssertionError("Black Army world parties must not inherit employer faction wars")

    print("[black_army_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



