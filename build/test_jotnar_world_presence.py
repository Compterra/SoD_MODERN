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
    presence = read("src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    order = read("src/dialogs/_order_dialogs.txt")
    defeat_event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")

    assert_contains(constants, "slot_faction_jotnar_hearth_pressure")
    assert_contains(constants, "slot_faction_jotnar_active_parties")
    assert_contains(constants, "slot_faction_jotnar_target_center")
    assert_contains(constants, "slot_party_sod_jotnar_hearth_activity")

    assert_contains(party_templates, '"jotnar_hearth_guard"')
    assert_contains(party_templates, '"jotnar_wintering_camp"')
    assert_contains(party_templates, "trp_jotnar_clan_armsman")
    assert_contains(party_templates, "trp_jotnar_clan_volva")
    assert_contains(party_templates, "fac_sod_merc_guild4")

    assert_contains(presence, '("sod_jotnar_world_presence"')
    assert_contains(presence, "pt_jotnar_hearth_guard")
    assert_contains(presence, "pt_jotnar_wintering_camp")
    assert_contains(presence, "p_sod_merc_guild_4")
    assert_contains(presence, "fac_sod_merc_guild4")
    assert_contains(presence, "slot_faction_merc_pact")
    assert_contains(presence, "native_kingdoms_begin, native_kingdoms_end")
    assert_contains(presence, "slot_center_sod_local_population")
    assert_contains(presence, "village_pop_ideal")
    assert_contains(presence, "slot_center_sod_local_health")
    assert_contains(presence, "script_change_center_prosperity")
    assert_contains(presence, "slot_party_merc_contract")
    assert_contains(presence, "script_party_set_ai_state")
    assert_contains(presence, "spai_patrolling_around_center")

    assert_contains(spawns, 'call_script, "script_sod_jotnar_world_presence"')
    assert_contains(report, "hearth guards active")
    assert_contains(report, "wintering camps active")
    assert_contains(notes, "Hearth status")

    assert_contains(order, "party_tpl_pt_jotnar_hearth_guard_start.py")
    assert_contains(order, "party_tpl_pt_jotnar_wintering_camp_start.py")
    assert_contains(order, "anyone_jotnar_world_hearth_about.py")
    assert_contains(defeat_event, '"pt_jotnar_hearth_guard"')
    assert_contains(defeat_event, '"pt_jotnar_wintering_camp"')
    assert_contains(defeat_event, 'script_change_player_relation_with_faction", "fac_sod_merc_guild4", -3')

    guard_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_jotnar_hearth_guard_start.py")
    camp_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_jotnar_wintering_camp_start.py")
    about_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_jotnar_world_hearth_about.py")
    assert_contains(guard_dialog, "pt_jotnar_hearth_guard")
    assert_contains(camp_dialog, "pt_jotnar_wintering_camp")
    assert_contains(about_dialog, "slot_faction_jotnar_target_center")

    if "party_set_faction, \":new_party\", \":employer_faction\"" in presence:
        raise AssertionError("Jotnar world parties must not inherit employer faction wars")
    if "try_for_range, \":cur_faction\", kingdoms_begin, kingdoms_end" in presence:
        raise AssertionError("Jotnar employer search must stay on native kingdoms only")

    print("[jotnar_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
