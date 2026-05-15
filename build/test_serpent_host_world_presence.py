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
    presence = read("src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    order = read("src/dialogs/_order_dialogs.txt")
    player_victory_event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")

    assert_contains(constants, "slot_faction_serpent_route_pressure")
    assert_contains(constants, "slot_faction_serpent_active_parties")
    assert_contains(constants, "slot_faction_serpent_target_center")
    assert_contains(constants, "slot_faction_serpent_intelligence")
    assert_contains(constants, "slot_faction_serpent_safe_passage")
    assert_contains(constants, "slot_party_sod_serpent_route_activity")
    assert_contains(constants, "sod_serpent_action_buy_intel")

    assert_contains(party_templates, '"serpent_host_route_screen"')
    assert_contains(party_templates, '"serpent_host_courier_lance"')
    assert_contains(party_templates, "trp_serpent_host_akinci")
    assert_contains(party_templates, "trp_serpent_host_sipahi")
    assert_contains(party_templates, "fac_sod_merc_guild5")

    assert_contains(presence, '("sod_serpent_host_world_presence"')
    assert_contains(presence, "pt_serpent_host_route_screen")
    assert_contains(presence, "pt_serpent_host_courier_lance")
    assert_contains(presence, "p_sod_merc_guild_5")
    assert_contains(presence, "fac_sod_merc_guild5")
    assert_contains(presence, "slot_faction_merc_pact")
    assert_contains(presence, "script_get_center_threat_level")
    assert_contains(presence, "slot_town_wealth")
    assert_contains(presence, "slot_center_sod_local_prosperity")
    assert_contains(presence, "slot_party_merc_contract")
    assert_contains(presence, "script_party_set_ai_state")
    assert_contains(presence, "spai_patrolling_around_center")
    assert_contains(presence, '("sod_serpent_host_apply_player_action"')
    assert_contains(presence, '("sod_serpent_host_describe_status_to_s26"')
    assert_contains(presence, "slot_party_sod_boar_frontier_activity")
    assert_contains(presence, "Serpent Host riders are shadowing Boar Clan toll roads")
    assert_contains(presence, "native_kingdoms_begin, native_kingdoms_end")
    if "try_for_range, \":cur_faction\", kingdoms_begin, kingdoms_end" in presence:
        raise AssertionError("Serpent Host employer scans should use native kingdom range")

    assert_contains(spawns, 'call_script, "script_sod_serpent_host_world_presence"')
    assert_contains(report, "script_sod_serpent_host_describe_status_to_s26")
    assert_contains(report, "route intelligence network active")
    assert_contains(notes, "script_sod_serpent_host_describe_status_to_s26")

    assert_contains(order, "party_tpl_pt_serpent_host_route_screen_start.py")
    assert_contains(order, "party_tpl_pt_serpent_host_courier_lance_start.py")
    assert_contains(order, "anyone_serpent_host_world_route_about.py")
    assert_contains(order, "anyone_plyr_serpent_host_world_route_talk_04.py")
    assert_contains(order, "anyone_plyr_serpent_host_world_route_talk_05.py")
    attack_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_serpent_host_world_route_talk_03.py")
    assert_contains(attack_dialog, "I will break your line.")
    assert_contains(attack_dialog, '"close_window"')
    assert_contains(attack_dialog, '(assign, "$g_enemy_party", "$g_encountered_party")')
    assert_contains(attack_dialog, 'script_let_nearby_parties_join_current_battle')
    assert_contains(attack_dialog, "(encounter_attack)")
    assert_not_contains(attack_dialog, "party_encounter_attack")
    assert_not_contains(attack_dialog, "I will break your screen.")
    assert_not_contains(attack_dialog, "sod_serpent_action_attack_screen")
    assert_contains(player_victory_event, "pt_serpent_host_route_screen")
    assert_contains(player_victory_event, "pt_serpent_host_courier_lance")
    assert_contains(player_victory_event, "sod_serpent_action_attack_screen")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_serpent_host_world_route_talk_04.py"), "sod_serpent_action_buy_intel")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_serpent_host_world_route_talk_05.py"), "sod_serpent_action_safe_passage")
    assert_contains(read("src/menus/reports/serpent_host_route_report.py"), "Serpent Host Route Intelligence")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/reports.py"), "mnu_mini_faction_reports")
    assert_contains(read("src/menus/reports/report_submenus.py"), "mnu_serpent_host_route_report")
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/serpent_host_route_report.py")

    screen_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_serpent_host_route_screen_start.py")
    lance_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_serpent_host_courier_lance_start.py")
    about_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_serpent_host_world_route_about.py")
    assert_contains(screen_dialog, "pt_serpent_host_route_screen")
    assert_contains(lance_dialog, "pt_serpent_host_courier_lance")
    assert_contains(about_dialog, "slot_faction_serpent_target_center")

    if "party_set_faction, \":new_party\", \":employer_faction\"" in presence:
        raise AssertionError("Serpent Host world parties must not inherit employer faction wars")

    print("[serpent_host_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



