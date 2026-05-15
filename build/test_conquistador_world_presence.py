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
    presence = read("src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    order = read("src/dialogs/_order_dialogs.txt")
    player_victory_event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")

    for token in (
        "slot_faction_conquistador_supply_stock",
        "slot_faction_conquistador_requisition_heat",
        "sod_conquistador_action_fund_supplies",
        "sod_conquistador_action_take_stores",
        "sod_conquistador_action_delivery_contract",
    ):
        assert_contains(constants, token)

    assert_contains(party_templates, '"conquistador_procurement_column"')
    assert_contains(party_templates, '"conquistador_expeditionary_camp"')
    assert_contains(party_templates, "trp_conquistador_lancer")
    assert_contains(party_templates, "trp_conquistador_tercio_pikeman")
    assert_contains(party_templates, "fac_sod_merc_guild2")

    assert_contains(presence, '("sod_conquistador_world_presence"')
    assert_contains(presence, "pt_conquistador_procurement_column")
    assert_contains(presence, "pt_conquistador_expeditionary_camp")
    assert_contains(presence, "fac_sod_merc_guild2")
    assert_contains(presence, "p_sod_merc_guild_2")
    assert_contains(presence, "slot_faction_merc_pact")
    assert_contains(presence, "slot_town_wealth")
    assert_contains(presence, "slot_center_sod_local_prosperity")
    assert_contains(presence, "script_center_get_food_store_limit")
    assert_contains(presence, "slot_party_food_store")
    assert_contains(presence, "food_store_limit")
    assert_contains(presence, "script_party_set_ai_state")
    assert_contains(presence, "spai_holding_center")
    assert_contains(presence, "slot_party_merc_contract")
    assert_contains(presence, '("sod_conquistador_apply_player_action"')
    assert_contains(presence, '("sod_conquistador_describe_status_to_s25"')
    assert_contains(presence, "slot_party_sod_slaver_web_activity")
    assert_contains(presence, "slot_party_sod_boar_frontier_activity")
    assert_contains(presence, "native_kingdoms_begin, native_kingdoms_end")
    if "try_for_range, \":cur_faction\", kingdoms_begin, kingdoms_end" in presence:
        raise AssertionError("Conquistador employer scans should use native kingdom range")

    assert_contains(spawns, 'call_script, "script_sod_conquistador_world_presence"')
    assert_contains(report, "script_sod_conquistador_describe_status_to_s25")
    assert_contains(report, "expeditionary supply machine active")
    assert_contains(notes, "script_sod_conquistador_describe_status_to_s25")
    assert_contains(order, "party_tpl_pt_conquistador_procurement_column_start.py")
    assert_contains(order, "party_tpl_pt_conquistador_expeditionary_camp_start.py")
    assert_contains(order, "anyone_plyr_conquistador_world_logistics_talk_04.py")
    assert_contains(order, "anyone_plyr_conquistador_world_logistics_talk_05.py")
    attack_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_conquistador_world_logistics_talk_03.py")
    assert_contains(attack_dialog, "encounter_attack")
    assert_not_contains(attack_dialog, "sod_conquistador_action_take_stores")
    assert_contains(player_victory_event, "pt_conquistador_procurement_column")
    assert_contains(player_victory_event, "pt_conquistador_expeditionary_camp")
    assert_contains(player_victory_event, "sod_conquistador_action_take_stores")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_conquistador_world_logistics_talk_04.py"), "sod_conquistador_action_fund_supplies")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_conquistador_world_logistics_talk_05.py"), "sod_conquistador_action_delivery_contract")
    assert_contains(read("src/menus/reports/conquistador_supply_report.py"), "Conquistador Expeditionary Supply")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/reports.py"), "mnu_mini_faction_reports")
    assert_contains(read("src/menus/reports/report_submenus.py"), "mnu_conquistador_supply_report")
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/conquistador_supply_report.py")

    column_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_conquistador_procurement_column_start.py")
    camp_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_conquistador_expeditionary_camp_start.py")
    about_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_conquistador_world_logistics_about.py")
    assert_contains(column_dialog, "pt_conquistador_procurement_column")
    assert_contains(camp_dialog, "pt_conquistador_expeditionary_camp")
    assert_contains(about_dialog, "slot_faction_merc_pact")
    assert_contains(about_dialog, "fac_sod_merc_guild2")
    assert_contains(about_dialog, "native_kingdoms_begin, native_kingdoms_end")

    if "party_set_faction, \":new_party\", \":employer_faction\"" in presence:
        raise AssertionError("Conquistador world parties must not inherit employer faction wars")

    print("[conquistador_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



