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
    factions = read("compile/module_factions.py")
    party_templates = read("compile/module_party_templates.py")
    presence = read("src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    report = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    dialogue = read("src/dialogs/ZZ99_misc_dialogs/anyone_boar_clan_introduce.py")
    encounter = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")
    player_victory_event = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(constants, "slot_faction_boar_frontier_pressure")
    assert_contains(constants, "slot_faction_boar_pressure_relief")
    assert_contains(constants, "slot_faction_boar_pressure_relief_until")
    assert_contains(constants, "slot_faction_boar_active_parties")
    assert_contains(constants, "slot_faction_boar_target_center")
    assert_contains(constants, "slot_faction_boar_tribute_stock")
    assert_contains(constants, "slot_faction_boar_intimidation")
    assert_contains(constants, "slot_party_sod_boar_frontier_activity")
    assert_contains(constants, "sod_boar_action_pay_toll")
    assert_contains(constants, "sod_boar_action_hire_band")
    assert_contains(constants, "sod_boar_action_defy_toll")
    assert_contains(constants, "sod_boar_action_frontier_tribute")
    assert_contains(constants, "sod_boar_action_defeat_band")
    assert_contains(factions, '("sod_merc_guild7","The Boar Clan"')
    assert_contains(factions, '("commoners", 0.0)')
    assert_contains(factions, '("player_faction", 0.0)')
    assert_contains(factions, '("player_supporters_faction", 0.0)')
    assert_contains(factions, '("outlaws", -0.2)')
    assert_contains(factions, '("deserters", -0.2)')
    assert_contains(factions, '("sod_merc_guild7", 0.0)')

    assert_contains(party_templates, '"boar_clan_fighters"')
    assert_contains(party_templates, '"boar_clan_fighters_desert"')
    assert_contains(party_templates, "trp_boar_clan_tusk_rider")
    assert_contains(party_templates, "fac_sod_merc_guild7")
    assert_contains(party_templates, '"boar_clan_reinforcements","Boar Clan Fighters"')
    assert_contains(party_templates, "fac_sod_merc_guild7,soldier_personality")

    assert_contains(presence, '("sod_boar_clan_world_presence"')
    assert_contains(presence, "pt_boar_clan_fighters")
    assert_contains(presence, "pt_boar_clan_fighters_desert")
    assert_contains(presence, "p_sod_merc_guild_7")
    assert_contains(presence, "fac_sod_merc_guild7")
    assert_contains(presence, "script_get_center_threat_level")
    assert_contains(presence, "slot_center_sod_local_population")
    assert_contains(presence, "slot_town_wealth")
    assert_contains(presence, "slot_center_sod_local_prosperity")
    assert_contains(presence, "script_sod_get_village_output_profile")
    assert_contains(presence, "script_sod_change_center_wealth")
    assert_contains(presence, "script_sod_change_center_local_prosperity")
    assert_contains(presence, "village_pop_min")
    assert_contains(presence, "script_sod_center_apply_population_delta")
    assert_contains(presence, "slot_faction_boar_tribute_stock")
    assert_contains(presence, "slot_faction_boar_intimidation")
    assert_contains(presence, "val_clamp, \":tribute_stock\", 0, 2000")
    assert_contains(presence, "val_clamp, \":intimidation\", 0, 101")
    assert_contains(presence, "slot_party_merc_contract")
    assert_contains(presence, "slot_party_type, spt_ai_mercenaries")
    assert_contains(presence, "party_get_battle_opponent")
    assert_contains(presence, "slot_party_type, spt_player_mercenaries")
    assert_contains(presence, "script_party_set_ai_state")
    assert_contains(presence, "spai_patrolling_around_center")
    assert_contains(presence, "sod_boar_clan_apply_player_action")
    assert_contains(presence, "sod_boar_action_pay_toll")
    assert_contains(presence, "sod_boar_action_hire_band")
    assert_contains(presence, "sod_boar_action_defy_toll")
    assert_contains(presence, "sod_boar_action_frontier_tribute")
    assert_contains(presence, "sod_boar_action_defeat_band")
    assert_contains(presence, "slot_faction_boar_frontier_pressure")
    assert_contains(presence, "slot_faction_boar_pressure_relief")
    assert_contains(presence, "slot_faction_boar_pressure_relief_until")
    assert_contains(presence, 'store_add, ":relief_until", ":cur_day", 5')
    assert_contains(presence, "sod_companion_action_safe_roadcraft")
    assert_contains(player_victory_event, "pt_boar_clan_fighters")
    assert_contains(player_victory_event, "pt_boar_clan_fighters_desert")
    assert_contains(player_victory_event, "sod_boar_action_defeat_band")

    assert_contains(spawns, 'call_script, "script_sod_boar_clan_world_presence"')
    assert_contains(spawns, "slot_faction_boar_target_center")
    assert_contains(spawns, 'party_set_faction, ":new_party", "fac_sod_merc_guild7"')
    assert_contains(report, "toll-band network active")
    assert_contains(report, "tribute")
    assert_contains(report, "intimidation")
    assert_contains(notes, "fac_sod_merc_guild7")
    assert_contains(notes, "script_sod_boar_clan_describe_status_to_s23")
    assert_contains(dialogue, "script_sod_boar_clan_prepare_encounter")
    assert_contains(encounter, "frontier tribute")
    assert_contains(encounter, "Boar Clan warding")
    assert_contains(order, "party_tpl_pt_boar_clan_fighters_start.py")
    assert_contains(order, "party_tpl_pt_boar_clan_fighters_desert_start.py")

    if "party_set_faction, \":new_party\", \":employer_faction\"" in presence:
        raise AssertionError("Boar Clan world parties must not inherit employer faction wars")
    if "p_town_18" in spawns or "p_town_3" in spawns or "p_town_15" in spawns:
        raise AssertionError("Boar Clan field parties should spawn from their own frontier target/base, not fixed towns")
    if '"boar_clan_reinforcements","Boar Clan Fighters",icon_flagbearer_a|carries_goods(2),0,fac_outlaws' in party_templates:
        raise AssertionError("Boar Clan reinforcement template must not use fac_outlaws")

    print("[boar_clan_world_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
