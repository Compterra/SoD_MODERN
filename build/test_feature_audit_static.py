# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_quest_journal_archive_entries_are_not_duplicated() -> None:
    raw = read("src/scripts/ZG_quests/sod_quest_journal_describe_to_s2.py")
    assert_contains(raw, "if include_archive_day:")
    assert_contains(raw, "else:")
    assert raw.count('(str_store_string, s0, "@        Stage {reg0} | Chain {reg1} | State {reg2}"),') == 1
    assert raw.count('(str_store_string, s0, "@        Stage {reg0} | Chain {reg1} | State {reg2} | Archived day {reg3}"),') == 1


def test_captivity_uses_systemic_outcome_inputs() -> None:
    wilderness = read("src/menus/other/captivity_wilderness_check.py")
    castle = read("src/menus/other/captivity_castle_check.py")
    ransom = read("src/menus/other/captivity_end_ransom_accept.py")
    for raw in (wilderness, castle):
        assert_contains(raw, "store_character_level")
        assert_contains(raw, "slot_troop_renown")
        assert_contains(raw, "$player_honor")
        assert_contains(raw, ":ransom_chance")
        assert_contains(raw, ":exchange_chance")
    assert_contains(wilderness, "fac_sod_merc_guild6")
    assert_contains(ransom, "(le, \"$player_ransom_amount\", 0)")
    assert_contains(ransom, "(assign, \"$player_ransom_amount\", 0)")


def test_invasion_arrival_and_report_surfaces_exist() -> None:
    arrival = read("src/menus/other/invaders_arrived.py")
    report = read("src/menus/camp/invasion_status_report.py")
    reports_menu = read("src/menus/camp/reports.py")
    order = read("src/menus/_order_game_menus.txt")
    assert_contains(arrival, "Review the invasion status")
    assert_contains(arrival, "slot_faction_num_armies")
    assert_contains(report, "Imperial Invasion Status")
    assert_contains(report, "slot_faction_current_power")
    assert_contains(report, "$g_sod_invasion_begin")
    assert_contains(reports_menu, "mnu_invasion_status_report")
    assert_contains(order, "camp/invasion_status_report.py")


def test_faction_notes_surface_realm_systems() -> None:
    raw = read("src/scripts/ZF_factions/update_faction_notes.py")
    assert_contains(raw, "script_sod_law_recalculate_faction_law_modifiers")
    assert_contains(raw, "script_sod_law_count_active_for_faction")
    assert_contains(raw, "slot_faction_law_militarization")
    assert_contains(raw, "slot_faction_law_centralization")
    assert_contains(raw, "slot_faction_law_legitimacy")
    assert_contains(raw, "slot_faction_law_unrest")
    assert_contains(raw, "slot_faction_current_power")
    assert_contains(raw, "Realm systems")
    assert_contains(raw, "Legion")


if __name__ == "__main__":
    test_quest_journal_archive_entries_are_not_duplicated()
    test_captivity_uses_systemic_outcome_inputs()
    test_invasion_arrival_and_report_surfaces_exist()
    test_faction_notes_surface_realm_systems()
    print("test_feature_audit_static: OK")
