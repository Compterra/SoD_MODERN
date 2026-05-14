# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    boar = read("src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py")
    horde = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    incidents = read("src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py")
    boar_report = read("src/menus/reports/boar_clan_frontier_report.py")
    horde_report = read("src/menus/reports/black_khergit_horde_report.py")

    for token in (
        "slot_party_sod_boar_frontier_activity",
        "slot_party_sod_boar_frontier_origin",
        "slot_party_sod_boar_frontier_destination",
        "slot_party_black_khergit_camp_activity",
        "slot_party_black_khergit_origin",
        "slot_party_black_khergit_target",
        "slot_party_black_khergit_role",
        "slot_party_black_khergit_response_until",
        "slot_party_black_khergit_response_target",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_black_khergit_pressure",
    ):
        assert_contains(constants, token)

    for token in (
        '(party_set_slot, ":cur_party", slot_party_black_khergit_camp_activity, 0)',
        '(party_set_slot, ":cur_party", slot_party_black_khergit_origin, 0)',
        '(party_set_slot, ":cur_party", slot_party_black_khergit_target, 0)',
        '(party_set_slot, ":cur_party", slot_party_black_khergit_role, 0)',
        '(party_set_slot, ":cur_party", slot_party_black_khergit_response_target, 0)',
        '(party_set_slot, ":cur_party", slot_party_black_khergit_response_until, 0)',
        '(neq, ":cur_template", "pt_boar_clan_fighters")',
        '(neq, ":cur_template", "pt_boar_clan_fighters_desert")',
        '(party_set_slot, ":cur_party", slot_party_sod_boar_frontier_activity, 0)',
    ):
        assert_contains(boar, token)

    for token in (
        '"cf_sod_black_khergits_valid_target_center"',
        '"cf_sod_black_khergits_party_is_horde_camp"',
        '"cf_sod_black_khergits_party_is_raider"',
        '"cf_sod_black_khergits_party_is_horde_force"',
        '(store_faction_of_party, ":center_faction", ":center_no")',
        '(eq, ":center_faction", "fac_sod_merc_guild7")',
        '(store_faction_of_party, ":party_faction", ":party_no")',
        '(eq, ":party_faction", "fac_black_khergits")',
        '(assign, ":camp_valid", 0)',
        '(faction_set_slot, "fac_black_khergits", slot_faction_black_khergit_camp_party, 0)',
        '(faction_get_slot, ":boar_target", "fac_sod_merc_guild7", slot_faction_boar_target_center)',
        '(party_get_slot, ":boar_destination", ":boar_party", slot_party_sod_boar_frontier_destination)',
        '(call_script, "script_cf_sod_black_khergits_valid_target_center", ":center_no")',
        '(call_script, "script_cf_sod_black_khergits_valid_target_center", ":stored_target")',
        '(call_script, "script_cf_sod_black_khergits_party_is_horde_camp", ":camp_party")',
        '(call_script, "script_cf_sod_black_khergits_party_is_raider", ":raider_party")',
        '(call_script, "script_cf_sod_black_khergits_party_is_horde_force", ":threat_party")',
        'The Black Khergits are rumored to have invaded Calradia.',
        'The Black Khergit horde packs its tents and rides toward another rich trade road.',
        'Black Khergit raiders are stripping wealth from nearby villages.',
        'Black Khergit riders have found a caravan to harry on the trade roads.',
        '(party_set_slot, ":party_no", slot_party_sod_boar_frontier_activity, 0)',
        '(party_set_slot, ":party_no", slot_party_sod_boar_frontier_origin, 0)',
        '(party_set_slot, ":party_no", slot_party_sod_boar_frontier_destination, 0)',
        '(neq, ":template", "pt_black_khergit_horde_camp")',
        '(neq, ":template", "pt_black_khergit_raiders")',
        '(neq, ":template", "pt_black_khergit_night_guard")',
        '(party_set_slot, ":party_no", slot_party_black_khergit_camp_activity, 0)',
        '(party_set_slot, ":party_no", slot_party_black_khergit_origin, 0)',
        '(party_set_slot, ":party_no", slot_party_black_khergit_target, 0)',
        '(party_set_slot, ":party_no", slot_party_black_khergit_role, 0)',
    ):
        assert_contains(horde, token)

    assert_contains(incidents, '(faction_get_slot, ":horde_pressure", "fac_black_khergits", slot_faction_black_khergit_pressure)')
    assert_contains(incidents, '(faction_get_slot, ":boar_pressure", "fac_sod_merc_guild7", slot_faction_boar_frontier_pressure)')
    assert_contains(incidents, "sod_mini_faction_incident_black_khergit_raid")
    assert_contains(incidents, "sod_mini_faction_incident_boar_tolls")
    assert_contains(boar_report, "script_sod_mini_faction_describe_recent_incident_to_s28\", sod_mini_faction_incident_boar_tolls")
    assert_contains(horde_report, "script_sod_mini_faction_describe_recent_incident_to_s28\", sod_mini_faction_incident_black_khergit_raid")
    if horde.index("The Black Khergits are rumored to have invaded Calradia.") > horde.index("The Black Khergit horde packs its tents and rides toward another rich trade road."):
        raise AssertionError("Initial Black Khergit invasion rumor should be the first public horde message")
    if horde.index('(assign, ":camp_party", ":party_no")') > horde.index('(party_get_position, pos1, ":camp_party")'):
        raise AssertionError("Camp position reads must occur after a valid horde camp party is assigned")
    for stale in (
        "The Black Khergit horde camp {s21} is moving toward",
        "The Black Khergit horde is moving toward the rich roads around {s60}.",
        "Black Khergit raiders are stripping wealth from the villages around {s60}.",
        "Black Khergit riders have found a caravan to harry near {s60}.",
        "Black Khergit raiders are stripping wealth from the villages around {s22}.",
        "Black Khergit riders have found a caravan to harry near {s22}.",
    ):
        if stale in horde:
            raise AssertionError(f"Black Khergit public message still uses stale/shared text: {stale}")
    live_public_message = re.search(r'\(display_message,\s*"@[^"\n]*\{s[0-9]+\}', horde)
    if live_public_message:
        raise AssertionError(f"Black Khergit public message still has a live s-register placeholder: {live_public_message.group(0)}")
    deferred_public_message = re.search(r'\(display_message,\s*s[0-9]+', horde)
    if deferred_public_message:
        raise AssertionError(f"Black Khergit public message still displays a string register: {deferred_public_message.group(0)}")

    print("[black_khergit_boar_separation_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
