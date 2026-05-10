# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def troop_entry(raw: str, troop_id: str) -> str:
    marker = f'["{troop_id}"'
    start = raw.find(marker)
    assert start >= 0, f"missing troop: trp_{troop_id}"
    end = raw.find("],", start)
    assert end >= 0, f"troop entry did not close: trp_{troop_id}"
    return raw[start:end]


def test_quest_foundation_is_registered() -> None:
    order = read("src/quests/_order_quests.txt")
    quests = read("src/quests/0013_seven_oaths_of_ash_quests.py")
    assert_contains(order, "0013_seven_oaths_of_ash_quests.py")
    assert_contains(quests, "campaign_seven_oaths_of_ash")
    for quest_id in (
        "seven_ash_ultimatum",
        "seven_ash_village_audit",
        "seven_ash_garric_ashbow",
        "seven_ash_oswin_ditchwright",
        "seven_ash_sir_aldrik_vane",
        "seven_ash_mirelle_voss",
        "seven_ash_tomas_reed",
        "seven_ash_beren_hardhand",
        "seven_ash_sister_elianor",
        "seven_ash_return_to_ashwick",
        "seven_ash_pressure_interlude",
        "seven_ash_oath_council",
        "seven_ash_outer_fields",
        "seven_ash_palisade",
        "seven_ash_breach",
        "seven_ash_inner_streets",
        "seven_ash_churchyard_stand",
        "seven_ash_aftermath",
    ):
        assert_contains(quests, f'"{quest_id}"')


def test_state_slots_and_defender_bits_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for slot in (
        "slot_quest_seven_ash_campaign_status",
        "slot_quest_seven_ash_active_stage",
        "slot_quest_seven_ash_act2_board_open",
        "slot_quest_seven_ash_act2_resolved_count",
        "slot_quest_seven_ash_act2_complete",
        "slot_quest_seven_ash_act3_pressure_started",
        "slot_quest_seven_ash_days_remaining",
        "slot_quest_seven_ash_act2_pacing_flags",
        "slot_quest_seven_ash_act2_last_tick_day",
        "slot_quest_seven_ash_sector_leader_bitmask",
        "slot_quest_seven_ash_memorial_bitmask",
        "slot_quest_seven_ash_ending_flags",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_player_strength_siege",
        "slot_quest_seven_ash_wulfred_host_strength",
        "slot_quest_seven_ash_recruited_bitmask",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_garric_status",
        "slot_quest_seven_ash_oswin_status",
        "slot_quest_seven_ash_garric_route",
        "slot_quest_seven_ash_oswin_route",
        "slot_quest_seven_ash_garric_evidence",
        "slot_quest_seven_ash_oswin_evidence",
        "slot_quest_seven_ash_garric_return_applied",
        "slot_quest_seven_ash_oswin_return_applied",
        "slot_quest_seven_ash_garric_trust",
        "slot_quest_seven_ash_garric_fear",
        "slot_quest_seven_ash_oswin_trust",
        "slot_quest_seven_ash_oswin_debt",
        "slot_quest_seven_ash_oswin_fear",
        "slot_quest_seven_ash_aldrik_route",
        "slot_quest_seven_ash_aldrik_evidence",
        "slot_quest_seven_ash_aldrik_return_applied",
        "slot_quest_seven_ash_aldrik_trust",
        "slot_quest_seven_ash_aldrik_pride",
        "slot_quest_seven_ash_aldrik_debt",
        "slot_quest_seven_ash_aldrik_fear",
        "slot_quest_seven_ash_mirelle_route",
        "slot_quest_seven_ash_mirelle_evidence",
        "slot_quest_seven_ash_mirelle_return_applied",
        "slot_quest_seven_ash_mirelle_trust",
        "slot_quest_seven_ash_mirelle_debt",
        "slot_quest_seven_ash_mirelle_fear",
        "slot_quest_seven_ash_mirelle_spy_support",
        "slot_quest_seven_ash_tomas_route",
        "slot_quest_seven_ash_tomas_evidence",
        "slot_quest_seven_ash_tomas_return_applied",
        "slot_quest_seven_ash_tomas_trust",
        "slot_quest_seven_ash_tomas_respect",
        "slot_quest_seven_ash_tomas_fear",
        "slot_quest_seven_ash_tomas_discipline_support",
        "slot_quest_seven_ash_beren_route",
        "slot_quest_seven_ash_beren_evidence",
        "slot_quest_seven_ash_beren_return_applied",
        "slot_quest_seven_ash_beren_trust",
        "slot_quest_seven_ash_beren_pride",
        "slot_quest_seven_ash_beren_fear",
        "slot_quest_seven_ash_beren_breach_support",
        "slot_quest_seven_ash_elianor_route",
        "slot_quest_seven_ash_elianor_evidence",
        "slot_quest_seven_ash_elianor_return_applied",
        "slot_quest_seven_ash_elianor_trust",
        "slot_quest_seven_ash_elianor_refugee_trust",
        "slot_quest_seven_ash_elianor_fear",
        "slot_quest_seven_ash_elianor_infirmary_support",
        "slot_quest_seven_ash_pressure_interlude_active",
        "slot_quest_seven_ash_pressure_interlude_resolved_bits",
        "slot_quest_seven_ash_sector_outer_fields",
        "slot_quest_seven_ash_sector_palisade",
        "slot_quest_seven_ash_sector_gate_reserve",
        "slot_quest_seven_ash_sector_inner_streets",
        "slot_quest_seven_ash_sector_churchyard",
        "slot_quest_seven_ash_sector_evacuation",
        "slot_quest_seven_ash_sector_commitment_locked",
        "slot_quest_seven_ash_siege_phase_active",
        "slot_quest_seven_ash_outer_wave_count",
        "slot_quest_seven_ash_outer_enemy_committed",
        "slot_quest_seven_ash_outer_result",
        "slot_quest_seven_ash_outer_casualty_pressure",
        "slot_quest_seven_ash_palisade_wave_count",
        "slot_quest_seven_ash_palisade_enemy_committed",
        "slot_quest_seven_ash_palisade_result",
        "slot_quest_seven_ash_palisade_breach_pressure",
        "slot_quest_seven_ash_breach_wave_count",
        "slot_quest_seven_ash_breach_enemy_committed",
        "slot_quest_seven_ash_breach_result",
        "slot_quest_seven_ash_breach_street_pressure",
        "slot_quest_seven_ash_inner_wave_count",
        "slot_quest_seven_ash_inner_enemy_committed",
        "slot_quest_seven_ash_inner_result",
        "slot_quest_seven_ash_inner_churchyard_pressure",
        "slot_quest_seven_ash_churchyard_wave_count",
        "slot_quest_seven_ash_churchyard_enemy_committed",
        "slot_quest_seven_ash_churchyard_result",
        "slot_quest_seven_ash_wulfred_outcome",
        "slot_quest_seven_ash_civilian_deaths",
        "slot_quest_seven_ash_burned_homes",
        "slot_quest_seven_ash_surviving_defender_count",
        "slot_quest_seven_ash_promises_kept",
        "slot_quest_seven_ash_prisoner_treatment",
        "slot_quest_seven_ash_settlement_outcome",
    ):
        assert_contains(constants, slot)
    for bit in (
        "sod_seven_ash_defender_garric = 1",
        "sod_seven_ash_defender_oswin = 2",
        "sod_seven_ash_defender_aldrik = 4",
        "sod_seven_ash_defender_mirelle = 8",
        "sod_seven_ash_defender_tomas = 16",
        "sod_seven_ash_defender_beren = 32",
        "sod_seven_ash_defender_elianor = 64",
        "sod_seven_ash_defender_all = 127",
        "sod_seven_ash_recruit_in_progress = 2",
        "sod_seven_ash_route_best = 1",
        "sod_seven_ash_evidence_public_truth = 3",
        "sod_seven_ash_interlude_burned_cow = 1",
        "sod_seven_ash_interlude_knife_marked_door = 2",
        "sod_seven_ash_interlude_grain_riot = 4",
        "sod_seven_ash_interlude_wulfred_offer = 8",
        "sod_seven_ash_interlude_first_funeral = 16",
        "sod_seven_ash_pacing_courier_10 = 1",
        "sod_seven_ash_pacing_scout_rumor_5 = 16",
        "sod_seven_ash_pacing_slow_warning = 32",
        "sod_seven_ash_pacing_emergency_return = 64",
        "sod_seven_ash_sector_outer_fields = 1",
        "sod_seven_ash_sector_evacuation = 6",
        "sod_seven_ash_siege_phase_outer_fields = 1",
        "sod_seven_ash_siege_phase_palisade = 2",
        "sod_seven_ash_siege_result_held = 1",
        "sod_seven_ash_siege_result_lost = 3",
        "sod_seven_ash_wulfred_killed = 1",
        "sod_seven_ash_wulfred_captured = 2",
        "sod_seven_ash_wulfred_escaped = 3",
        "sod_seven_ash_wulfred_wins = 4",
        "sod_seven_ash_prisoners_bound_for_trial = 1",
        "sod_seven_ash_settlement_refugee_camp = 3",
        "sod_seven_ash_settlement_ruined = 4",
        "sod_seven_ash_ending_seven_oaths_kept = 1",
        "sod_seven_ash_ending_ashwick_stands = 2",
        "sod_seven_ash_ending_wall_of_names = 4",
        "sod_seven_ash_ending_empty_houses = 8",
        "sod_seven_ash_ending_wulfred_broken = 16",
        "sod_seven_ash_ending_wulfred_escaped = 32",
        "sod_seven_ash_ending_bargain_brand = 64",
        "sod_seven_ash_ending_blood_for_ash = 128",
        "sod_seven_ash_ending_long_road_from_ashwick = 256",
        "sod_seven_ash_ending_palisade_grave = 512",
        "sod_seven_ash_ending_new_wolf = 1024",
        "sod_seven_ash_ending_common_bell = 2048",
    ):
        assert_contains(constants, bit)


def test_act2_gate_and_companion_foundation_are_explicit() -> None:
    quests = read("src/quests/0013_seven_oaths_of_ash_quests.py")
    mark_resolved = read("src/scripts/ZG_quests/sod_seven_ash_mark_defender_resolved.py")
    close_recruitment = read("src/scripts/ZG_quests/sod_seven_ash_close_recruitment.py")
    assert_contains(quests, "Act III pressure")
    assert_contains(quests, "set act2 complete")
    assert_contains(quests, "dlg_seven_ash_companion_offers")
    assert_contains(mark_resolved, "slot_quest_seven_ash_act2_resolved_count")
    assert_contains(mark_resolved, "ge, \":resolved_count\", 7")
    assert_contains(mark_resolved, "slot_quest_seven_ash_act2_complete, 1")
    assert_contains(mark_resolved, "sod_seven_ash_stage_return")
    assert_contains(close_recruitment, "ge, \":resolved\", 3")
    assert_contains(close_recruitment, "sod_seven_ash_recruit_abandoned")
    assert_contains(close_recruitment, "slot_quest_seven_ash_act2_complete, 1")
    assert_contains(close_recruitment, "sod_seven_ash_stage_return")


def test_campaign_state_repair_and_defender_bit_count_helpers_exist() -> None:
    menu = read("src/menus/start_game/seven_ash_ultimatum.py")
    count = read("src/scripts/ZG_quests/sod_seven_ash_count_defender_bits.py")
    repair = read("src/scripts/ZG_quests/sod_seven_ash_repair_campaign_state.py")
    checklist = read("docs/campaigns/the_seven_oaths_of_ash_implementation_checklist.md")
    assert_contains(menu, "script_sod_seven_ash_repair_campaign_state")
    assert_contains(menu, "script_party_count_fit_for_battle")
    assert_contains(menu, "slot_quest_seven_ash_player_strength_ultimatum")
    for token in (
        "sod_seven_ash_defender_garric",
        "sod_seven_ash_defender_oswin",
        "sod_seven_ash_defender_aldrik",
        "sod_seven_ash_defender_mirelle",
        "sod_seven_ash_defender_tomas",
        "sod_seven_ash_defender_beren",
        "sod_seven_ash_defender_elianor",
        "assign, reg0, \":count\"",
    ):
        assert_contains(count, token)
    for token in (
        "script_sod_seven_ash_count_defender_bits",
        "slot_quest_seven_ash_act2_resolved_count",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_sector_leader_bitmask",
        "sod_seven_ash_pacing_emergency_return",
        "sod_seven_ash_stage_return",
        "val_and, \":recruited\", sod_seven_ash_defender_all",
        "val_min, \":resolved\", 7",
    ):
        assert_contains(repair, token)
    assert_contains(checklist, "- [x] Bitmask helpers count recruited defenders correctly.")
    assert_contains(checklist, "- [x] Old saves or missing fields repair to safe defaults.")
    assert_contains(checklist, "- [x] Store player field strength at ultimatum.")


def test_act2_pacing_has_couriers_scouts_late_route_pressure_and_emergency_return() -> None:
    constants = read("src/constants/module_constants.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    audit = read("src/scripts/ZG_quests/sod_seven_ash_choose_audit_priority.py")
    pacing = read("src/scripts/ZG_quests/sod_seven_ash_act2_daily_pacing.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_first_defender_road.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    trigger = read("src/triggers/ST03_daily/entry_0166.py")
    for token in (
        "slot_quest_seven_ash_act2_pacing_flags",
        "slot_quest_seven_ash_act2_last_tick_day",
        "sod_seven_ash_pacing_courier_10",
        "sod_seven_ash_pacing_courier_6",
        "sod_seven_ash_pacing_courier_3",
        "sod_seven_ash_pacing_scout_rumor_9",
        "sod_seven_ash_pacing_scout_rumor_5",
        "sod_seven_ash_pacing_slow_warning",
        "sod_seven_ash_pacing_emergency_return",
    ):
        assert_contains(constants, token)
    for token in (
        "slot_quest_seven_ash_days_remaining, 100",
        "slot_quest_seven_ash_act2_pacing_flags, 0",
        "slot_quest_seven_ash_act2_last_tick_day, -1",
    ):
        assert_contains(init, token)
    for token in (
        "slot_quest_seven_ash_days_remaining, 14",
        "slot_quest_seven_ash_act2_pacing_flags, 0",
        "store_current_day, \":cur_day\"",
        "slot_quest_seven_ash_act2_last_tick_day",
    ):
        assert_contains(audit, token)
    for token in (
        "sod_seven_ash_act2_daily_pacing",
        "slot_quest_seven_ash_active_stage, sod_seven_ash_stage_recruitment",
        "store_current_day",
        "val_sub, \":days\", \":elapsed\"",
        "A light courier from Ashwick",
        "Wulfred's scouts",
        "Mother Hilda's last light courier",
        "slot_quest_seven_ash_act2_complete, 1",
        "sod_seven_ash_stage_return",
        "sod_seven_ash_recruit_abandoned",
        "emergency return",
    ):
        assert_contains(pacing, token)
    for token in (
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_hard",
        "le, \":days\", 3",
        "sod_seven_ash_pacing_slow_warning",
        "Wulfred's scouts made the delay costly",
    ):
        assert_contains(resolve, token)
    assert_contains(trigger_order, "ST03_daily/entry_0166.py")
    assert_contains(trigger, "script_sod_seven_ash_act2_daily_pacing")


def test_host_scaling_foundation_matches_design_range() -> None:
    script = read("src/scripts/ZG_quests/sod_seven_ash_compute_host_strength.py")
    menu = read("src/menus/start_game/seven_ash_siege_warning.py")
    ultimatum = read("src/menus/start_game/seven_ash_ultimatum.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_nell_harrow_siege_warning.py")
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    assert_contains(script, "base 140 + twice the visible player field strength")
    assert_contains(script, "val_add, \":host_strength\", \":scaled_player_strength\"")
    assert_contains(script, "val_max, \":host_strength\", 180")
    assert_contains(script, "val_min, \":host_strength\", 420")
    assert_contains(script, "slot_quest_seven_ash_wulfred_host_strength")
    assert_contains(script, "slot_quest_seven_ash_wulfred_elite_core")
    assert_contains(order, "start_game/seven_ash_siege_warning.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_nell_harrow_siege_warning.py")
    assert_contains(menu, "script_party_count_fit_for_battle")
    assert_contains(menu, "script_sod_seven_ash_compute_host_strength")
    assert_contains(menu, "Maud Ledger")
    assert_contains(menu, "Rafe")
    assert_contains(menu, "brigands")
    assert_contains(dialog, "slot_quest_seven_ash_player_strength_siege")
    assert_contains(dialog, "slot_quest_seven_ash_wulfred_host_strength")
    assert_contains(dialog, "slot_quest_seven_ash_wulfred_elite_core")
    assert_contains(dialog, "Maud Ledger")
    assert_contains(dialog, "Rafe Carrick")
    assert_contains(dialog, "brigands")
    assert_contains(dialog, "deserters")
    assert_contains(dialog, "script_sod_quest_chain_branch_success")
    assert_contains(ultimatum, "slot_quest_seven_ash_player_strength_ultimatum")
    for player_strength, expected_host in ((50, 240), (85, 310)):
        host_strength = max(180, min(420, 140 + player_strength * 2))
        assert host_strength == expected_host


def test_dialogue_first_metadata_is_present() -> None:
    quests = read("src/quests/0013_seven_oaths_of_ash_quests.py")
    for dialogue in (
        "dlg_seven_ash_rafe_ultimatum",
        "dlg_seven_ash_mother_hilda_audit",
        "dlg_seven_ash_garric_recruit",
        "dlg_seven_ash_oswin_recruit",
        "dlg_seven_ash_return_home",
        "dlg_seven_ash_oath_council",
        "dlg_seven_ash_aftermath",
        "dlg_seven_ash_companion_offers",
    ):
        assert_contains(quests, dialogue)
    assert_contains(quests, "menu_confirms_after_dialogue")


def test_act_i_menus_are_registered_and_dialogue_first() -> None:
    order = read("src/menus/_order_game_menus.txt")
    ultimatum = read("src/menus/start_game/seven_ash_ultimatum.py")
    audit = read("src/menus/start_game/seven_ash_village_audit.py")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    for menu_path in (
        "start_game/seven_ash_ultimatum.py",
        "start_game/seven_ash_village_audit.py",
        "start_game/seven_ash_recruitment_map.py",
    ):
        assert_contains(order, menu_path)
    assert_contains(ultimatum, "Rafe Carrick throws a sack")
    assert_contains(ultimatum, "Mother Hilda asks whether surety means hostage")
    assert_contains(ultimatum, "slot_quest_seven_ash_campaign_status")
    assert_contains(ultimatum, "sod_seven_ash_status_inactive")
    assert_contains(ultimatum, "script_sod_seven_ash_initialize_campaign_state")
    assert_contains(ultimatum, "The ultimatum has already been answered")
    assert_contains(ultimatum, "slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum")
    assert_contains(ultimatum, "Continue the Seven Oaths campaign")
    assert_contains(ultimatum, "mnu_seven_ash_recruitment_map")
    assert_contains(ultimatum, "mnu_seven_ash_return_to_ashwick")
    assert_contains(ultimatum, "script_sod_seven_ash_choose_posture")
    assert_contains(ultimatum, "sod_seven_ash_posture_find_defenders")
    assert_contains(audit, "At the palisade")
    assert_contains(audit, "At the mill bridge")
    assert_contains(audit, "dry cellars")
    assert_contains(audit, "mnu_seven_ash_village_audit_witnesses")
    assert_contains(audit, "Mother Hilda starts with people")
    assert_contains(audit, "Reeve Martin holds up the granary key")
    assert_contains(audit, "Piers Wainwright names carts")
    assert_contains(audit, "Nell of Little Harrow points past the ditch")
    assert_contains(audit, "Hear the village witnesses before choosing the first priority")
    assert_contains(audit, "Walk the village once more before deciding")
    assert_contains(audit, "script_sod_seven_ash_choose_audit_priority")
    assert_contains(audit, "sod_seven_ash_priority_scout_road")
    assert_contains(board, "No mark on it wins a defender")
    assert_contains(board, "where the next conversation waits")
    assert_contains(board, "final pressure until the oaths and returns are settled")
    assert_contains(board, "Days before emergency return")
    assert_contains(board, "Travel targets")
    assert_contains(board, "Road tallies")
    assert_contains(board, "Marks: 1 lead open, 2 road begun, 3 won, 4 refused, 5 present but bitter, 6 lost, 7 abandoned")
    assert_contains(board, "still need their Ashwick return")
    assert_contains(board, "slot_quest_seven_ash_days_remaining")


def test_act_i_resolvers_set_pressure_readiness_and_chain_state() -> None:
    posture = read("src/scripts/ZG_quests/sod_seven_ash_choose_posture.py")
    audit = read("src/scripts/ZG_quests/sod_seven_ash_choose_audit_priority.py")
    constants = read("src/constants/module_constants.py")
    for token in (
        "sod_seven_ash_posture_prepare_alone",
        "sod_seven_ash_posture_find_defenders",
        "sod_seven_ash_posture_kill_messengers",
        "sod_seven_ash_priority_repair_palisade",
        "sod_seven_ash_priority_scout_road",
    ):
        assert_contains(constants, token)
    assert_contains(posture, "slot_quest_seven_ash_wulfred_pressure")
    assert_contains(posture, "val_add, \":pressure\", 25")
    assert_contains(posture, "script_sod_quest_chain_branch_choice")
    assert_contains(audit, "slot_quest_seven_ash_fortification")
    assert_contains(audit, "slot_quest_seven_ash_food")
    assert_contains(audit, "slot_quest_seven_ash_training")
    assert_contains(audit, "slot_quest_seven_ash_civilian_safety")
    assert_contains(audit, "slot_quest_seven_ash_intelligence")
    assert_contains(audit, "slot_quest_seven_ash_act2_board_open, 1")
    assert_contains(audit, "script_sod_quest_chain_branch_success")


def test_act2_status_scripts_prevent_double_resolution() -> None:
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    audit = read("src/scripts/ZG_quests/sod_seven_ash_choose_audit_priority.py")
    set_status = read("src/scripts/ZG_quests/sod_seven_ash_set_defender_status.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_first_defender_road.py")
    for token in (
        "slot_quest_seven_ash_garric_status",
        "slot_quest_seven_ash_oswin_status",
        "sod_seven_ash_recruit_unknown",
    ):
        assert_contains(init, token)
    assert_contains(audit, "sod_seven_ash_recruit_available")
    begin = read("src/scripts/ZG_quests/sod_seven_ash_begin_defender_road.py")
    assert_contains(begin, "qst_seven_ash_garric_ashbow")
    assert_contains(begin, "p_town_6")
    assert_contains(begin, "qst_seven_ash_oswin_ditchwright")
    assert_contains(begin, "p_village_4")
    assert_contains(begin, "qst_seven_ash_sir_aldrik_vane")
    assert_contains(begin, "p_village_5")
    assert_contains(begin, "qst_seven_ash_mirelle_voss")
    assert_contains(begin, "p_town_5")
    assert_contains(begin, "qst_seven_ash_tomas_reed")
    assert_contains(begin, "p_town_3")
    assert_contains(begin, "qst_seven_ash_beren_hardhand")
    assert_contains(begin, "p_town_2")
    assert_contains(begin, "qst_seven_ash_sister_elianor")
    assert_contains(begin, "p_village_7")
    assert_contains(set_status, ":already_terminal")
    assert_contains(set_status, "(eq, \":already_terminal\", 0)")
    assert_contains(set_status, "script_sod_seven_ash_mark_defender_resolved")
    assert_contains(resolve, "slot_quest_seven_ash_garric_evidence")
    assert_contains(resolve, "slot_quest_seven_ash_oswin_evidence")
    assert_contains(resolve, "slot_quest_seven_ash_garric_trust")
    assert_contains(resolve, "slot_quest_seven_ash_garric_fear")
    assert_contains(resolve, "slot_quest_seven_ash_oswin_trust")
    assert_contains(resolve, "slot_quest_seven_ash_oswin_debt")
    assert_contains(resolve, "slot_quest_seven_ash_oswin_fear")
    assert_contains(resolve, "slot_quest_seven_ash_defender_bond_flags")
    assert_contains(resolve, "slot_quest_seven_ash_mirelle_route")
    assert_contains(resolve, "slot_quest_seven_ash_mirelle_evidence")
    assert_contains(resolve, "slot_quest_seven_ash_mirelle_trust")
    assert_contains(resolve, "slot_quest_seven_ash_mirelle_spy_support")
    assert_contains(resolve, "slot_quest_seven_ash_tomas_route")
    assert_contains(resolve, "slot_quest_seven_ash_tomas_evidence")
    assert_contains(resolve, "slot_quest_seven_ash_tomas_trust")
    assert_contains(resolve, "slot_quest_seven_ash_tomas_discipline_support")
    assert_contains(resolve, "slot_quest_seven_ash_beren_route")
    assert_contains(resolve, "slot_quest_seven_ash_beren_evidence")
    assert_contains(resolve, "slot_quest_seven_ash_beren_trust")
    assert_contains(resolve, "slot_quest_seven_ash_beren_breach_support")
    assert_contains(resolve, "slot_quest_seven_ash_elianor_route")
    assert_contains(resolve, "slot_quest_seven_ash_elianor_evidence")
    assert_contains(resolve, "slot_quest_seven_ash_elianor_trust")
    assert_contains(resolve, "slot_quest_seven_ash_elianor_infirmary_support")
    assert_contains(resolve, "slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none")
    return_script = read("src/scripts/ZG_quests/sod_seven_ash_apply_first_defender_return.py")
    assert_contains(return_script, "slot_quest_seven_ash_garric_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_oswin_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_training")
    assert_contains(return_script, "slot_quest_seven_ash_fortification")
    assert_contains(return_script, "slot_quest_seven_ash_companion_unlock_bitmask")
    assert_contains(return_script, "sod_seven_ash_defender_garric")
    assert_contains(return_script, "sod_seven_ash_defender_oswin")
    assert_contains(return_script, "slot_quest_seven_ash_aldrik_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_aldrik_route")
    assert_contains(return_script, "sod_seven_ash_defender_aldrik")
    assert_contains(return_script, "slot_quest_seven_ash_mirelle_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_mirelle_route")
    assert_contains(return_script, "sod_seven_ash_defender_mirelle")
    assert_contains(return_script, "slot_quest_seven_ash_tomas_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_tomas_route")
    assert_contains(return_script, "sod_seven_ash_defender_tomas")
    assert_contains(return_script, "slot_quest_seven_ash_beren_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_beren_route")
    assert_contains(return_script, "sod_seven_ash_defender_beren")
    assert_contains(return_script, "slot_quest_seven_ash_elianor_return_applied")
    assert_contains(return_script, "slot_quest_seven_ash_elianor_route")
    assert_contains(return_script, "sod_seven_ash_defender_elianor")


def test_first_defender_scene_menus_are_registered_and_dialogue_framed() -> None:
    order = read("src/menus/_order_game_menus.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    garric = read("src/menus/start_game/seven_ash_garric_split_hart.py")
    oswin = read("src/menus/start_game/seven_ash_oswin_quarry.py")
    for menu_path in (
        "start_game/seven_ash_garric_split_hart.py",
        "start_game/seven_ash_oswin_quarry.py",
    ):
        assert_contains(order, menu_path)
    assert_contains(board, "slot_quest_seven_ash_garric_status")
    assert_contains(board, "script_sod_seven_ash_begin_defender_road")
    assert_contains(board, "mnu_seven_ash_garric_split_hart")
    assert_contains(board, "mnu_seven_ash_oswin_quarry")
    assert_contains(board, "mnu_seven_ash_garric_watch_platform")
    assert_contains(board, "mnu_seven_ash_oswin_palisade")
    assert_contains(board, "mnu_seven_ash_aldrik_chapel")
    assert_contains(board, "mnu_seven_ash_aldrik_gate")
    assert_contains(board, "mnu_seven_ash_mirelle_low_lantern")
    assert_contains(board, "mnu_seven_ash_mirelle_evacuation_routes")
    assert_contains(board, "mnu_seven_ash_tomas_almshouse")
    assert_contains(board, "mnu_seven_ash_tomas_militia_yard")
    assert_contains(board, "mnu_seven_ash_beren_pit")
    assert_contains(board, "mnu_seven_ash_beren_gate")
    assert_contains(board, "mnu_seven_ash_elianor_refugee_camp")
    assert_contains(board, "mnu_seven_ash_elianor_infirmary")
    assert_contains(board, "mnu_seven_ash_end_recruitment_confirm")
    assert_contains(garric, "The Split Hart tavern goes quiet around Garric Ashbow")
    assert_contains(garric, "Eda Flint")
    assert_contains(garric, "the recruitment choice belongs to dialogue")
    assert_contains(garric, "(eq, \"$current_town\", \"p_town_6\")")
    assert_contains(garric, "Travel to {s11}; Garric is not here.")
    assert_contains(garric, "start_map_conversation, \"trp_seven_ash_garric_ashbow\"")
    assert_not_contains(garric, "script_sod_seven_ash_resolve_first_defender_road")
    assert_contains(oswin, "Harrowcut Quarry smells of wet lime")
    assert_contains(oswin, "broken bridge")
    assert_contains(oswin, "(eq, \"$current_town\", \"p_village_4\")")
    assert_contains(oswin, "Travel to {s11}; Oswin is not here.")
    assert_contains(oswin, "start_map_conversation, \"trp_seven_ash_oswin_ditchwright\"")
    assert_not_contains(oswin, "script_sod_seven_ash_resolve_first_defender_road")


def test_aldrik_recruitment_road_is_dialogue_driven() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    chapel = read("src/menus/start_game/seven_ash_aldrik_chapel.py")
    gate = read("src/menus/start_game/seven_ash_aldrik_gate.py")
    recruit = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_recruit.py")
    ret = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_return.py")
    assert_contains(order, "start_game/seven_ash_aldrik_chapel.py")
    assert_contains(order, "start_game/seven_ash_aldrik_gate.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_recruit.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_return.py")
    assert_contains(board, "slot_quest_seven_ash_aldrik_status")
    assert_contains(board, "sod_seven_ash_defender_aldrik")
    assert_contains(chapel, "Saint Cuthbert's Wayside Chapel")
    assert_contains(chapel, "Mara of the Bridge")
    assert_contains(chapel, "(eq, \"$current_town\", \"p_village_5\")")
    assert_contains(chapel, "start_map_conversation, \"trp_seven_ash_sir_aldrik_vane\"")
    assert_not_contains(chapel, "script_sod_seven_ash_resolve_first_defender_road")
    assert_contains(gate, "Aldrik stands before Ashwick's gate")
    assert_contains(gate, "start_map_conversation, \"trp_seven_ash_sir_aldrik_vane\"")
    for token in (
        "Mara has said her part",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_forced_service",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(recruit, token)
    assert_contains(ret, "slot_quest_seven_ash_aldrik_return_applied")
    assert_contains(ret, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(ret, "Hope without formation is only noise")


def test_mirelle_recruitment_road_is_dialogue_driven() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    tavern = read("src/menus/start_game/seven_ash_mirelle_low_lantern.py")
    routes = read("src/menus/start_game/seven_ash_mirelle_evacuation_routes.py")
    recruit = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_recruit.py")
    ret = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_return.py")
    assert_contains(order, "start_game/seven_ash_mirelle_low_lantern.py")
    assert_contains(order, "start_game/seven_ash_mirelle_evacuation_routes.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_recruit.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_return.py")
    assert_contains(board, "slot_quest_seven_ash_mirelle_status")
    assert_contains(board, "sod_seven_ash_defender_mirelle")
    assert_contains(tavern, "Low Lantern tavern")
    assert_contains(tavern, "Tib")
    assert_contains(tavern, "(eq, \"$current_town\", \"p_town_5\")")
    assert_contains(tavern, "Travel to {s11}; Mirelle is not here.")
    assert_contains(tavern, "start_map_conversation, \"trp_seven_ash_mirelle_voss\"")
    assert_not_contains(tavern, "script_sod_seven_ash_resolve_first_defender_road")
    assert_contains(routes, "chalk, thread, and three women")
    assert_contains(routes, "start_map_conversation, \"trp_seven_ash_mirelle_voss\"")
    for token in (
        "Tib thinks he is selling errands",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_blackmail",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(recruit, token)
    assert_contains(ret, "slot_quest_seven_ash_mirelle_return_applied")
    assert_contains(ret, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(ret, "A good exit is a lie told to panic before panic arrives")


def test_tomas_recruitment_road_is_dialogue_driven() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    almshouse = read("src/menus/start_game/seven_ash_tomas_almshouse.py")
    yard = read("src/menus/start_game/seven_ash_tomas_militia_yard.py")
    recruit = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_recruit.py")
    ret = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_return.py")
    assert_contains(order, "start_game/seven_ash_tomas_almshouse.py")
    assert_contains(order, "start_game/seven_ash_tomas_militia_yard.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_recruit.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_return.py")
    assert_contains(board, "slot_quest_seven_ash_tomas_status")
    assert_contains(board, "sod_seven_ash_defender_tomas")
    assert_contains(almshouse, "Red Crutch almshouse")
    assert_contains(almshouse, "Old Jory")
    assert_contains(almshouse, "Matteo")
    assert_contains(almshouse, "(eq, \"$current_town\", \"p_town_3\")")
    assert_contains(almshouse, "Travel to {s11}; Tomas is not here.")
    assert_contains(almshouse, "start_map_conversation, \"trp_seven_ash_tomas_reed\"")
    assert_not_contains(almshouse, "script_sod_seven_ash_resolve_first_defender_road")
    assert_contains(yard, "hold spears like broom handles")
    assert_contains(yard, "start_map_conversation, \"trp_seven_ash_tomas_reed\"")
    for token in (
        "Old Jory told you I saved men",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_forced_service",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(recruit, token)
    assert_contains(ret, "slot_quest_seven_ash_tomas_return_applied")
    assert_contains(ret, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(ret, "feet first, breath second, points third")


def test_beren_recruitment_road_is_dialogue_driven() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    pit = read("src/menus/start_game/seven_ash_beren_pit.py")
    gate = read("src/menus/start_game/seven_ash_beren_gate.py")
    recruit = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_recruit.py")
    ret = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_return.py")
    assert_contains(order, "start_game/seven_ash_beren_pit.py")
    assert_contains(order, "start_game/seven_ash_beren_gate.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_recruit.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_return.py")
    assert_contains(board, "slot_quest_seven_ash_beren_status")
    assert_contains(board, "sod_seven_ash_defender_beren")
    assert_contains(pit, "mill-yard pit")
    assert_contains(pit, "Ansel Miller")
    assert_contains(pit, "(eq, \"$current_town\", \"p_town_2\")")
    assert_contains(pit, "Travel to {s11}; Beren is not here.")
    assert_contains(pit, "start_map_conversation, \"trp_seven_ash_beren_hardhand\"")
    assert_not_contains(pit, "script_sod_seven_ash_resolve_first_defender_road")
    assert_contains(gate, "tests the beam with his shoulder")
    assert_contains(gate, "start_map_conversation, \"trp_seven_ash_beren_hardhand\"")
    for token in (
        "Ansel still telling folk I was not empty",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_forced_service",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(recruit, token)
    assert_contains(ret, "slot_quest_seven_ash_beren_return_applied")
    assert_contains(ret, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(ret, "Mother Hilda names the stop")


def test_elianor_recruitment_road_is_dialogue_driven() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    camp = read("src/menus/start_game/seven_ash_elianor_refugee_camp.py")
    infirmary = read("src/menus/start_game/seven_ash_elianor_infirmary.py")
    recruit = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_recruit.py")
    ret = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_return.py")
    assert_contains(order, "start_game/seven_ash_elianor_refugee_camp.py")
    assert_contains(order, "start_game/seven_ash_elianor_infirmary.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_recruit.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_return.py")
    assert_contains(board, "slot_quest_seven_ash_elianor_status")
    assert_contains(board, "sod_seven_ash_defender_elianor")
    assert_contains(camp, "Saint Ormond's refugee camp")
    assert_contains(camp, "wounded cannot march")
    assert_contains(camp, "(eq, \"$current_town\", \"p_village_7\")")
    assert_contains(camp, "Travel to {s11}; Sister Elianor is not here.")
    assert_contains(camp, "start_map_conversation, \"trp_seven_ash_sister_elianor\"")
    assert_not_contains(camp, "script_sod_seven_ash_resolve_first_defender_road")
    assert_contains(infirmary, "granary tally")
    assert_contains(infirmary, "start_map_conversation, \"trp_seven_ash_sister_elianor\"")
    for token in (
        "If you want blessings, go to a bishop",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_forced_service",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(recruit, token)
    assert_contains(ret, "slot_quest_seven_ash_elianor_return_applied")
    assert_contains(ret, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(ret, "Mercy is slower when it has to clear furniture first")


def test_act2_manual_close_marks_unresolved_roads_abandoned() -> None:
    order = read("src/menus/_order_game_menus.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    confirm = read("src/menus/start_game/seven_ash_end_recruitment_confirm.py")
    close_recruitment = read("src/scripts/ZG_quests/sod_seven_ash_close_recruitment.py")
    assert_contains(order, "start_game/seven_ash_end_recruitment_confirm.py")
    assert_contains(board, "slot_quest_seven_ash_act2_resolved_count")
    assert_contains(board, "(ge, \":resolved\", 3)")
    assert_contains(board, "End the search and return to Ashwick.")
    assert_contains(confirm, "Closing the search will mark every unresolved defender road as abandoned")
    assert_contains(confirm, "script_sod_seven_ash_close_recruitment")
    for defender in (
        "sod_seven_ash_defender_garric",
        "sod_seven_ash_defender_oswin",
        "sod_seven_ash_defender_aldrik",
        "sod_seven_ash_defender_mirelle",
        "sod_seven_ash_defender_tomas",
        "sod_seven_ash_defender_beren",
        "sod_seven_ash_defender_elianor",
    ):
        assert_contains(close_recruitment, defender)
    assert_contains(close_recruitment, "slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none")
    assert_contains(close_recruitment, "qst_seven_ash_return_to_ashwick")


def test_return_to_ashwick_starts_act3_through_dialogue() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    confirm = read("src/menus/start_game/seven_ash_end_recruitment_confirm.py")
    menu = read("src/menus/start_game/seven_ash_return_to_ashwick.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_return.py")
    script = read("src/scripts/ZG_quests/sod_seven_ash_begin_act3_return.py")
    assert_contains(order, "start_game/seven_ash_return_to_ashwick.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_return.py")
    assert_contains(board, "mnu_seven_ash_return_to_ashwick")
    assert_contains(confirm, "mnu_seven_ash_return_to_ashwick")
    assert_contains(menu, "Mother Hilda asks how many beds to prepare")
    assert_contains(menu, "Reeve Martin has the granary tally")
    assert_contains(menu, "Nell does not ask anything")
    assert_contains(menu, "start_map_conversation, \"trp_seven_ash_mother_hilda\"")
    assert_not_contains(menu, "script_sod_seven_ash_begin_act3_return")
    assert_contains(dialog, "I need beds for the ones you brought")
    assert_contains(dialog, "script_sod_seven_ash_begin_act3_return")
    assert_contains(script, "slot_quest_seven_ash_act3_pressure_started, 1")
    assert_contains(script, "sod_seven_ash_stage_pressure")
    assert_contains(script, "qst_seven_ash_pressure_interlude")


def test_act3_pressure_interludes_are_dialogue_driven_and_stateful() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_pressure_board.py")
    resolver = read("src/scripts/ZG_quests/sod_seven_ash_resolve_pressure_interlude.py")
    cow = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_burned_cow.py")
    door = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_nell_harrow_knife_marked_door.py")
    grain = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_reeve_martin_grain_riot.py")
    offer = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_rafe_carrick_wulfred_offer.py")
    funeral = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_first_funeral.py")
    assert_contains(order, "start_game/seven_ash_pressure_board.py")
    for dialog_path in (
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_burned_cow.py",
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_nell_harrow_knife_marked_door.py",
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_reeve_martin_grain_riot.py",
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_rafe_carrick_wulfred_offer.py",
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_first_funeral.py",
    ):
        assert_contains(dialog_order, dialog_path)
    for token in (
        "sod_seven_ash_interlude_burned_cow",
        "sod_seven_ash_interlude_knife_marked_door",
        "sod_seven_ash_interlude_grain_riot",
        "sod_seven_ash_interlude_wulfred_offer",
        "sod_seven_ash_interlude_first_funeral",
        "slot_quest_seven_ash_pressure_interlude_active",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    assert_not_contains(menu, "script_sod_seven_ash_resolve_pressure_interlude")
    for token in (
        "slot_quest_seven_ash_pressure_interlude_resolved_bits",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_intelligence",
        "slot_quest_seven_ash_civilian_safety",
        "slot_quest_seven_ash_food",
        "slot_quest_seven_ash_defender_bond_flags",
        "qst_seven_ash_pressure_interlude",
    ):
        assert_contains(resolver, token)
    for token in (
        "Piers wants riders sent",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_forced_service",
        "script_sod_seven_ash_resolve_pressure_interlude",
    ):
        assert_contains(cow, token)
    for token in (
        "Mirelle would say use quiet",
        "Aldrik would say quiet",
        "Elianor would ask",
        "sod_seven_ash_route_legal_promise",
        "script_sod_seven_ash_resolve_pressure_interlude",
    ):
        assert_contains(door, token)
    for token in (
        "Tomas calls this disorder",
        "Elianor calls it hunger",
        "Reeve Martin",
        "sod_seven_ash_route_forced_service",
        "script_sod_seven_ash_resolve_pressure_interlude",
    ):
        assert_contains(grain, token)
    for token in (
        "One offer, written seven ways",
        "a clean name",
        "safe passage",
        "refugees spared",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_forced_service",
        "script_sod_seven_ash_resolve_pressure_interlude",
    ):
        assert_contains(offer, token)
    for token in (
        "burying someone before the siege",
        "Tell the truth",
        "Promise victory",
        "Blame is a fast shovel",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_forced_service",
        "script_sod_seven_ash_resolve_pressure_interlude",
    ):
        assert_contains(funeral, token)


def test_oath_council_is_dialogue_first_and_sets_final_plan() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    pressure_board = read("src/menus/start_game/seven_ash_pressure_board.py")
    council_menu = read("src/menus/start_game/seven_ash_oath_council.py")
    council_dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_oath_council.py")
    resolver = read("src/scripts/ZG_quests/sod_seven_ash_resolve_oath_council_plan.py")
    assert_contains(order, "start_game/seven_ash_oath_council.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_oath_council.py")
    assert_contains(pressure_board, "mnu_seven_ash_oath_council")
    assert_contains(council_menu, "rough map of Ashwick")
    assert_contains(council_menu, "Missing roads leave blank places")
    assert_contains(council_menu, "Garric draws patient sightlines")
    assert_contains(council_menu, "Oswin marks failure points")
    assert_contains(council_menu, "Aldrik objects to dishonor")
    assert_contains(council_menu, "Mirelle supports dirty work")
    assert_contains(council_menu, "Tomas supports discipline")
    assert_contains(council_menu, "Beren supports force")
    assert_contains(council_menu, "Elianor supports any plan that counts wounded before pride")
    assert_contains(council_menu, "start_map_conversation, \"trp_seven_ash_mother_hilda\"")
    assert_not_contains(council_menu, "script_sod_seven_ash_resolve_oath_council_plan")
    for token in (
        "Seven questions before one oath",
        "where civilians go",
        "what happens to prisoners",
        "Hold the palisade",
        "Fight in depth",
        "Counterstroke",
        "Cut the head",
        "Empty the village",
        "script_sod_seven_ash_resolve_oath_council_plan",
        "mnu_seven_ash_sector_commitment",
    ):
        assert_contains(council_dialog, token)
    for token in (
        "slot_quest_seven_ash_final_plan",
        "sod_seven_ash_stage_siege",
        "sod_seven_ash_plan_hold_palisade",
        "sod_seven_ash_plan_defense_in_depth",
        "sod_seven_ash_plan_counterstroke",
        "sod_seven_ash_plan_cut_head",
        "sod_seven_ash_plan_empty_village",
        "qst_seven_ash_outer_fields",
    ):
        assert_contains(resolver, token)


def test_sector_commitment_focus_is_stored_for_siege() -> None:
    order = read("src/menus/_order_game_menus.txt")
    menu = read("src/menus/start_game/seven_ash_sector_commitment.py")
    script = read("src/scripts/ZG_quests/sod_seven_ash_commit_sector_focus.py")
    assert_contains(order, "start_game/seven_ash_sector_commitment.py")
    for token in (
        "outer fields",
        "ditch and palisade",
        "gate reserve",
        "inner streets",
        "churchyard fallback",
        "evacuation escort",
        "Garric leads if present",
        "Oswin leads if present",
        "Aldrik and Beren lead if present",
        "Mirelle and Elianor lead if present",
        "Tomas and Elianor lead if present",
        "script_sod_seven_ash_commit_sector_focus",
        "mnu_seven_ash_siege_warning",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_sector_commitment_locked",
        "slot_quest_seven_ash_sector_leader_bitmask",
        "slot_quest_seven_ash_sector_outer_fields",
        "slot_quest_seven_ash_sector_palisade",
        "slot_quest_seven_ash_sector_gate_reserve",
        "slot_quest_seven_ash_sector_inner_streets",
        "slot_quest_seven_ash_sector_churchyard",
        "slot_quest_seven_ash_sector_evacuation",
        "slot_quest_seven_ash_intelligence",
        "slot_quest_seven_ash_fortification",
        "slot_quest_seven_ash_civilian_safety",
        "assign, \":leaders\", 0",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_garric",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_oswin",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_aldrik",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_beren",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_mirelle",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_elianor",
        "store_and, \":bit\", \":recruited\", sod_seven_ash_defender_tomas",
        "val_or, \":leaders\", \":bit\"",
        "qst_seven_ash_oath_council",
    ):
        assert_contains(script, token)


def test_outer_fields_siege_phase_is_executable_and_stateful() -> None:
    menu_order = read("src/menus/_order_game_menus.txt")
    mission_order = read("src/mission_templates/_order_mission_templates.txt")
    warning = read("src/menus/start_game/seven_ash_siege_warning.py")
    scout_dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_nell_harrow_siege_warning.py")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    mission = read("src/mission_templates/0073_seven_ash_outer_fields/seven_ash_outer_fields.py")
    prepare = read("src/scripts/ZG_quests/sod_seven_ash_prepare_outer_fields.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_outer_fields.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    assert_contains(menu_order, "start_game/seven_ash_outer_fields.py")
    assert_contains(mission_order, "0073_seven_ash_outer_fields/seven_ash_outer_fields.py")
    assert_contains(warning, "mnu_seven_ash_outer_fields")
    assert_contains(scout_dialog, "mnu_seven_ash_outer_fields")
    for token in (
        "script_sod_seven_ash_prepare_outer_fields",
        "mt_seven_ash_outer_fields",
        "trp_seven_ash_garric_ashbow",
        "trp_seven_ash_tomas_reed",
        "trp_seven_ash_sibert_crow_eye",
        "script_sod_seven_ash_resolve_outer_fields",
        "mnu_seven_ash_palisade_staging",
    ):
        assert_contains(menu, token)
    for token in (
        '"seven_ash_outer_fields"',
        "mtef_team_0",
        "mtef_team_1",
        "first wave in the ditches",
        "stored Wulfred commitment",
        "mnu_seven_ash_outer_fields_held",
        "mnu_seven_ash_outer_fields_bloodied",
        "script_cf_troop_agent_is_alive",
    ):
        assert_contains(mission, token)
    for token in (
        "slot_quest_seven_ash_siege_phase_active",
        "sod_seven_ash_siege_phase_outer_fields",
        "slot_quest_seven_ash_wulfred_host_strength",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_intelligence",
        "slot_quest_seven_ash_sector_outer_fields",
        "val_max, \":enemy_committed\", 24",
        "val_min, \":enemy_committed\", 80",
        "slot_quest_seven_ash_outer_wave_count",
    ):
        assert_contains(prepare, token)
    for token in (
        "slot_quest_seven_ash_outer_result",
        "sod_seven_ash_siege_result_held",
        "sod_seven_ash_siege_result_bloodied",
        "sod_seven_ash_siege_result_lost",
        "slot_quest_seven_ash_civilian_safety",
        "sod_seven_ash_siege_phase_palisade",
        "qst_seven_ash_palisade",
    ):
        assert_contains(resolve, token)
    assert_contains(init, "slot_quest_seven_ash_outer_result, sod_seven_ash_siege_result_unresolved")


def test_palisade_siege_phase_uses_preparation_and_hands_to_breach() -> None:
    mission_order = read("src/mission_templates/_order_mission_templates.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    mission = read("src/mission_templates/0074_seven_ash_palisade/seven_ash_palisade.py")
    prepare = read("src/scripts/ZG_quests/sod_seven_ash_prepare_palisade.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_palisade.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    assert_contains(mission_order, "0074_seven_ash_palisade/seven_ash_palisade.py")
    for token in (
        "script_sod_seven_ash_prepare_palisade",
        "mt_seven_ash_palisade",
        "trp_seven_ash_oswin_ditchwright",
        "trp_seven_ash_tomas_reed",
        "trp_seven_ash_halvorn_pike",
        "script_sod_seven_ash_resolve_palisade",
        "mnu_seven_ash_breach_staging",
    ):
        assert_contains(menu, token)
    for token in (
        '"seven_ash_palisade"',
        "mtef_team_0",
        "mtef_team_1",
        "Oswin's works",
        "Tomas's discipline",
        "mnu_seven_ash_palisade_held",
        "mnu_seven_ash_palisade_bloodied",
        "script_cf_troop_agent_is_alive",
    ):
        assert_contains(mission, token)
    for token in (
        "slot_quest_seven_ash_siege_phase_active",
        "sod_seven_ash_siege_phase_palisade",
        "slot_quest_seven_ash_wulfred_host_strength",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_fortification",
        "slot_quest_seven_ash_training",
        "slot_quest_seven_ash_outer_casualty_pressure",
        "slot_quest_seven_ash_sector_palisade",
        "slot_quest_seven_ash_oswin_return_applied",
        "slot_quest_seven_ash_tomas_return_applied",
        "val_max, \":enemy_committed\", 36",
        "val_min, \":enemy_committed\", 120",
        "slot_quest_seven_ash_palisade_wave_count",
    ):
        assert_contains(prepare, token)
    for token in (
        "slot_quest_seven_ash_palisade_result",
        "sod_seven_ash_siege_result_held",
        "sod_seven_ash_siege_result_bloodied",
        "sod_seven_ash_siege_result_lost",
        "slot_quest_seven_ash_fortification",
        "sod_seven_ash_siege_phase_breach",
        "qst_seven_ash_breach",
    ):
        assert_contains(resolve, token)
    assert_contains(init, "slot_quest_seven_ash_palisade_result, sod_seven_ash_siege_result_unresolved")


def test_breach_siege_phase_uses_elite_core_and_hands_to_streets() -> None:
    mission_order = read("src/mission_templates/_order_mission_templates.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    mission = read("src/mission_templates/0075_seven_ash_breach/seven_ash_breach.py")
    prepare = read("src/scripts/ZG_quests/sod_seven_ash_prepare_breach.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_breach.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    assert_contains(mission_order, "0075_seven_ash_breach/seven_ash_breach.py")
    for token in (
        "script_sod_seven_ash_prepare_breach",
        "mt_seven_ash_breach",
        "trp_seven_ash_sir_aldrik_vane",
        "trp_seven_ash_beren_hardhand",
        "trp_seven_ash_halvorn_pike",
        "script_sod_seven_ash_resolve_breach",
        "mnu_seven_ash_inner_streets_staging",
    ):
        assert_contains(menu, token)
    for token in (
        '"seven_ash_breach"',
        "mtef_team_0",
        "mtef_team_1",
        "Halvorn's elite core",
        "Aldrik's oath",
        "Beren's violence",
        "mnu_seven_ash_breach_held",
        "mnu_seven_ash_breach_bloodied",
        "script_cf_troop_agent_is_alive",
    ):
        assert_contains(mission, token)
    for token in (
        "slot_quest_seven_ash_siege_phase_active",
        "sod_seven_ash_siege_phase_breach",
        "slot_quest_seven_ash_wulfred_elite_core",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_palisade_breach_pressure",
        "slot_quest_seven_ash_sector_gate_reserve",
        "slot_quest_seven_ash_aldrik_return_applied",
        "slot_quest_seven_ash_beren_return_applied",
        "slot_quest_seven_ash_beren_breach_support",
        "val_max, \":enemy_committed\", 24",
        "val_min, \":enemy_committed\", 90",
        "slot_quest_seven_ash_breach_wave_count",
    ):
        assert_contains(prepare, token)
    for token in (
        "slot_quest_seven_ash_breach_result",
        "sod_seven_ash_siege_result_held",
        "sod_seven_ash_siege_result_bloodied",
        "sod_seven_ash_siege_result_lost",
        "slot_quest_seven_ash_civilian_safety",
        "sod_seven_ash_siege_phase_inner_streets",
        "qst_seven_ash_inner_streets",
    ):
        assert_contains(resolve, token)
    assert_contains(init, "slot_quest_seven_ash_breach_result, sod_seven_ash_siege_result_unresolved")


def test_inner_streets_siege_phase_uses_civilian_safety_and_hands_to_churchyard() -> None:
    mission_order = read("src/mission_templates/_order_mission_templates.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    mission = read("src/mission_templates/0076_seven_ash_inner_streets/seven_ash_inner_streets.py")
    prepare = read("src/scripts/ZG_quests/sod_seven_ash_prepare_inner_streets.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_inner_streets.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    assert_contains(mission_order, "0076_seven_ash_inner_streets/seven_ash_inner_streets.py")
    for token in (
        "script_sod_seven_ash_prepare_inner_streets",
        "mt_seven_ash_inner_streets",
        "trp_seven_ash_mirelle_voss",
        "trp_seven_ash_sister_elianor",
        "trp_seven_ash_maud_ledger",
        "script_sod_seven_ash_resolve_inner_streets",
        "mnu_seven_ash_churchyard_staging",
    ):
        assert_contains(menu, token)
    for token in (
        '"seven_ash_inner_streets"',
        "mtef_team_0",
        "mtef_team_1",
        "Mirelle's exits",
        "Elianor's shelter",
        "civilian safety",
        "mnu_seven_ash_inner_streets_held",
        "mnu_seven_ash_inner_streets_bloodied",
        "script_cf_troop_agent_is_alive",
    ):
        assert_contains(mission, token)
    for token in (
        "slot_quest_seven_ash_siege_phase_active",
        "sod_seven_ash_siege_phase_inner_streets",
        "slot_quest_seven_ash_wulfred_host_strength",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_civilian_safety",
        "slot_quest_seven_ash_breach_street_pressure",
        "slot_quest_seven_ash_sector_inner_streets",
        "slot_quest_seven_ash_sector_evacuation",
        "slot_quest_seven_ash_mirelle_return_applied",
        "slot_quest_seven_ash_mirelle_spy_support",
        "slot_quest_seven_ash_elianor_return_applied",
        "slot_quest_seven_ash_elianor_infirmary_support",
        "val_max, \":enemy_committed\", 20",
        "val_min, \":enemy_committed\", 85",
        "slot_quest_seven_ash_inner_wave_count",
    ):
        assert_contains(prepare, token)
    for token in (
        "slot_quest_seven_ash_inner_result",
        "sod_seven_ash_siege_result_held",
        "sod_seven_ash_siege_result_bloodied",
        "sod_seven_ash_siege_result_lost",
        "slot_quest_seven_ash_civilian_safety",
        "sod_seven_ash_siege_phase_churchyard",
        "qst_seven_ash_churchyard_stand",
    ):
        assert_contains(resolve, token)
    assert_contains(init, "slot_quest_seven_ash_inner_result, sod_seven_ash_siege_result_unresolved")


def test_churchyard_siege_phase_resolves_wulfred_and_aftermath() -> None:
    mission_order = read("src/mission_templates/_order_mission_templates.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    mission = read("src/mission_templates/0077_seven_ash_churchyard/seven_ash_churchyard.py")
    prepare = read("src/scripts/ZG_quests/sod_seven_ash_prepare_churchyard.py")
    resolve = read("src/scripts/ZG_quests/sod_seven_ash_resolve_churchyard.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    assert_contains(mission_order, "0077_seven_ash_churchyard/seven_ash_churchyard.py")
    for token in (
        "script_sod_seven_ash_prepare_churchyard",
        "mt_seven_ash_churchyard",
        "trp_seven_ash_wulfred_carr",
        "trp_seven_ash_mother_hilda",
        "script_sod_seven_ash_resolve_churchyard",
        "sod_seven_ash_wulfred_captured",
        "sod_seven_ash_wulfred_killed",
        "sod_seven_ash_wulfred_escaped",
        "sod_seven_ash_wulfred_wins",
        "mnu_seven_ash_aftermath_staging",
    ):
        assert_contains(menu, token)
    for token in (
        '"seven_ash_churchyard"',
        "mtef_team_0",
        "mtef_team_1",
        "Wulfred's fate",
        "trp_seven_ash_wulfred_carr",
        "mnu_seven_ash_churchyard_wulfred_captured",
        "mnu_seven_ash_churchyard_wulfred_killed",
        "mnu_seven_ash_churchyard_wulfred_escaped",
        "script_cf_troop_agent_is_alive",
    ):
        assert_contains(mission, token)
    for token in (
        "slot_quest_seven_ash_siege_phase_active",
        "sod_seven_ash_siege_phase_churchyard",
        "slot_quest_seven_ash_wulfred_elite_core",
        "slot_quest_seven_ash_wulfred_pressure",
        "slot_quest_seven_ash_morale",
        "slot_quest_seven_ash_inner_churchyard_pressure",
        "slot_quest_seven_ash_sector_churchyard",
        "slot_quest_seven_ash_final_plan",
        "sod_seven_ash_plan_cut_head",
        "sod_seven_ash_defender_all",
        "val_max, \":enemy_committed\", 18",
        "val_min, \":enemy_committed\", 75",
        "slot_quest_seven_ash_churchyard_wave_count",
    ):
        assert_contains(prepare, token)
    for token in (
        "slot_quest_seven_ash_churchyard_result",
        "slot_quest_seven_ash_wulfred_outcome",
        "slot_quest_seven_ash_final_plan",
        "sod_seven_ash_plan_empty_village",
        "sod_seven_ash_result_bargain",
        "sod_seven_ash_wulfred_captured",
        "sod_seven_ash_wulfred_killed",
        "sod_seven_ash_wulfred_escaped",
        "sod_seven_ash_wulfred_wins",
        "slot_quest_seven_ash_result_grade",
        "sod_seven_ash_result_clean_victory",
        "sod_seven_ash_result_pyrrhic",
        "sod_seven_ash_result_failed",
        "sod_seven_ash_stage_aftermath",
        "qst_seven_ash_aftermath",
    ):
        assert_contains(resolve, token)
    assert_contains(init, "slot_quest_seven_ash_wulfred_outcome, sod_seven_ash_wulfred_unresolved")


def test_immediate_aftermath_counts_costs_and_records_first_count() -> None:
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    script = read("src/scripts/ZG_quests/sod_seven_ash_apply_immediate_aftermath.py")
    init = read("src/scripts/ZG_quests/sod_seven_ash_initialize_campaign_state.py")
    for token in (
        "script_sod_seven_ash_apply_immediate_aftermath",
        "civilian dead",
        "burned homes",
        "surviving defenders",
        "Wulfred's fate",
        "prisoner treatment",
        "promises kept",
        "Ashwick's future",
        "qst_seven_ash_aftermath",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_civilian_deaths",
        "slot_quest_seven_ash_burned_homes",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_surviving_defender_count",
        "slot_quest_seven_ash_promises_kept",
        "slot_quest_seven_ash_prisoner_treatment",
        "slot_quest_seven_ash_settlement_outcome",
        "slot_quest_seven_ash_outer_casualty_pressure",
        "slot_quest_seven_ash_palisade_breach_pressure",
        "slot_quest_seven_ash_breach_street_pressure",
        "slot_quest_seven_ash_inner_churchyard_pressure",
        "sod_seven_ash_prisoners_bound_for_trial",
        "sod_seven_ash_prisoners_executed",
        "sod_seven_ash_prisoners_scattered",
        "sod_seven_ash_settlement_village",
        "sod_seven_ash_settlement_fortified",
        "sod_seven_ash_settlement_refugee_camp",
        "sod_seven_ash_settlement_ruined",
        "sod_seven_ash_defender_garric",
        "sod_seven_ash_defender_elianor",
    ):
        assert_contains(script, token)
    for token in (
        "slot_quest_seven_ash_civilian_deaths, 0",
        "slot_quest_seven_ash_burned_homes, 0",
        "slot_quest_seven_ash_surviving_defender_count, 0",
        "slot_quest_seven_ash_prisoner_treatment, sod_seven_ash_prisoners_none",
        "slot_quest_seven_ash_companion_joined_bitmask, 0",
        "slot_quest_seven_ash_companion_stayed_bitmask, 0",
        "slot_quest_seven_ash_sector_leader_bitmask, 0",
        "slot_quest_seven_ash_memorial_bitmask, 0",
        "slot_quest_seven_ash_ending_flags, 0",
    ):
        assert_contains(init, token)
    assert_contains(script, "script_sod_seven_ash_archive_aftermath_endings")


def test_aftermath_archives_memorials_and_compact_ending_flags() -> None:
    script = read("src/scripts/ZG_quests/sod_seven_ash_archive_aftermath_endings.py")
    aftermath = read("src/scripts/ZG_quests/sod_seven_ash_apply_immediate_aftermath.py")
    checklist = read("docs/campaigns/the_seven_oaths_of_ash_implementation_checklist.md")
    assert_contains(aftermath, "script_sod_seven_ash_archive_aftermath_endings")
    for token in (
        "slot_quest_seven_ash_memorial_bitmask",
        "slot_quest_seven_ash_ending_flags",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "sod_seven_ash_defender_garric",
        "sod_seven_ash_defender_oswin",
        "sod_seven_ash_defender_aldrik",
        "sod_seven_ash_defender_mirelle",
        "sod_seven_ash_defender_tomas",
        "sod_seven_ash_defender_beren",
        "sod_seven_ash_defender_elianor",
        "sod_seven_ash_ending_seven_oaths_kept",
        "sod_seven_ash_ending_ashwick_stands",
        "sod_seven_ash_ending_wall_of_names",
        "sod_seven_ash_ending_empty_houses",
        "sod_seven_ash_ending_wulfred_broken",
        "sod_seven_ash_ending_wulfred_escaped",
        "sod_seven_ash_ending_bargain_brand",
        "sod_seven_ash_ending_blood_for_ash",
        "sod_seven_ash_ending_long_road_from_ashwick",
        "sod_seven_ash_ending_palisade_grave",
        "sod_seven_ash_ending_new_wolf",
        "sod_seven_ash_ending_common_bell",
        "Memorial roll",
        "craft and relationship",
        "sightlines",
        "timber",
        "oath",
        "doors",
        "drill",
        "breach",
        "water",
        "compact ending flags",
    ):
        assert_contains(script, token)
    for token in (
        "- [x] Memorialize dead defenders by craft and relationship.",
        "- [x] Implement Seven Oaths Kept.",
        "- [x] Implement Ashwick Stands.",
        "- [x] Implement Wall of Names.",
        "- [x] Implement Empty Houses.",
        "- [x] Implement Wulfred Broken.",
        "- [x] Implement Wulfred Escaped.",
        "- [x] Implement Bargain Brand.",
        "- [x] Implement Blood for Ash.",
        "- [x] Implement Long Road From Ashwick.",
        "- [x] Implement Palisade Grave.",
        "- [x] Implement New Wolf.",
        "- [x] Implement Common Bell.",
    ):
        assert_contains(checklist, token)


def test_garric_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_garric_ashbow",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "Eda Flint",
        "watch platform",
        "sightlines",
        "range",
        "waste",
        "Garric stayed in Ashwick as watch captain",
        "Garric refused to join because his trust condition was not met",
    ):
        assert_contains(dialog, token)


def test_oswin_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_oswin_ditchwright",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "Piers apologized to a gate",
        "failure points",
        "timber",
        "ditch",
        "mortar",
        "Oswin stayed in Ashwick as works master",
        "Oswin refused to join because his authority and trust conditions were not met",
    ):
        assert_contains(dialog, token)


def test_aldrik_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_sir_aldrik_vane",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "Mara stood before the gate",
        "shield hangs",
        "oath is a task",
        "witness",
        "lawful duty",
        "Aldrik stayed in Ashwick as shield captain",
        "Aldrik refused to join because his oath was not restored",
    ):
        assert_contains(dialog, token)


def test_mirelle_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_mirelle_voss",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "Tib is alive",
        "chalk",
        "doors",
        "shutter",
        "exits",
        "Mirelle stayed in Ashwick as keeper of hidden routes",
        "Mirelle refused to join because her trust condition was not met",
    ):
        assert_contains(dialog, token)


def test_tomas_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_tomas_reed",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "Old Jory",
        "Matteo",
        "discipline",
        "cruelty",
        "watches",
        "Tomas stayed in Ashwick as militia drillmaster",
        "Tomas refused to join because his discipline condition was not met",
    ):
        assert_contains(dialog, token)


def test_beren_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_beren_hardhand",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "Ansel saw me stop",
        "Mother Hilda",
        "Halvorn",
        "violence",
        "bounded force",
        "Beren stayed in Ashwick as breach warden",
        "Beren refused to join because his boundary condition was not met",
    ):
        assert_contains(dialog, token)


def test_elianor_aftermath_companion_offer_is_survival_and_unlock_gated() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    menu = read("src/menus/start_game/seven_ash_outer_fields.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_aftermath.py")
    assert_contains(dialog_order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_aftermath.py")
    for token in (
        "mnu_seven_ash_aftermath_defenders",
        "trp_seven_ash_sister_elianor",
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "start_map_conversation",
    ):
        assert_contains(menu, token)
    for token in (
        "slot_quest_seven_ash_active_stage",
        "sod_seven_ash_stage_aftermath",
        "slot_quest_seven_ash_survival_bitmask",
        "slot_quest_seven_ash_companion_unlock_bitmask",
        "slot_quest_seven_ash_companion_joined_bitmask",
        "slot_quest_seven_ash_companion_stayed_bitmask",
        "slot_quest_seven_ash_companion_refusal_bitmask",
        "party_add_members",
        "wounded",
        "water",
        "refugees",
        "sanctuary",
        "guarded labor",
        "Elianor stayed in Ashwick as infirmary keeper",
        "Elianor refused to join because her sanctuary condition was not met",
    ):
        assert_contains(dialog, token)


def test_first_defender_return_scenes_change_ashwick_readiness() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    garric_menu = read("src/menus/start_game/seven_ash_garric_watch_platform.py")
    oswin_menu = read("src/menus/start_game/seven_ash_oswin_palisade.py")
    garric_dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_return.py")
    oswin_dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_return.py")
    for menu_path in (
        "start_game/seven_ash_garric_watch_platform.py",
        "start_game/seven_ash_oswin_palisade.py",
    ):
        assert_contains(order, menu_path)
    for dialog_path in (
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_return.py",
        "ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_return.py",
    ):
        assert_contains(dialog_order, dialog_path)
    assert_contains(garric_menu, "Ashwick's old watch platform")
    assert_contains(garric_menu, "start_map_conversation, \"trp_seven_ash_garric_ashbow\"")
    assert_contains(oswin_menu, "walks Ashwick's palisade")
    assert_contains(oswin_menu, "start_map_conversation, \"trp_seven_ash_oswin_ditchwright\"")
    assert_contains(garric_dialog, "slot_quest_seven_ash_garric_return_applied")
    assert_contains(garric_dialog, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(garric_dialog, "courage and wasting arrows")
    assert_contains(oswin_dialog, "slot_quest_seven_ash_oswin_return_applied")
    assert_contains(oswin_dialog, "script_sod_seven_ash_apply_first_defender_return")
    assert_contains(oswin_dialog, "pretty wood can carve grave markers")


def test_first_defender_choices_live_in_dialogue_files() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    ids = read("compile/ids/ID_troops.py")
    garric = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_recruit.py")
    oswin = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_recruit.py")
    for token in (
        "trp_seven_ash_garric_ashbow =",
        "trp_seven_ash_oswin_ditchwright =",
        "trp_seven_ash_sibert_crow_eye =",
    ):
        assert_contains(ids, token)
    assert_contains(order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_recruit.py")
    assert_contains(order, "ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_recruit.py")
    for token in (
        "trp_seven_ash_garric_ashbow",
        "Eda still keeps the cellar loose",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_blackmail",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(garric, token)
    for token in (
        "trp_seven_ash_oswin_ditchwright",
        "The bridge failed at the pins",
        "sod_seven_ash_route_best",
        "sod_seven_ash_route_hard",
        "sod_seven_ash_route_legal_promise",
        "sod_seven_ash_route_forced_service",
        "sod_seven_ash_route_refusal",
        "script_sod_seven_ash_resolve_first_defender_road",
    ):
        assert_contains(oswin, token)


def test_seven_oaths_unique_troop_anchors_exist() -> None:
    troops = read("compile/module_troops.py")
    for troop_id in (
        "seven_ash_wulfred_carr",
        "seven_ash_rafe_carrick",
        "seven_ash_mother_hilda",
        "seven_ash_reeve_martin",
        "seven_ash_piers_wainwright",
        "seven_ash_nell_harrow",
        "seven_ash_garric_ashbow",
        "seven_ash_oswin_ditchwright",
        "seven_ash_sir_aldrik_vane",
        "seven_ash_mirelle_voss",
        "seven_ash_tomas_reed",
        "seven_ash_beren_hardhand",
        "seven_ash_sister_elianor",
        "seven_ash_halvorn_pike",
        "seven_ash_maud_ledger",
        "seven_ash_sibert_crow_eye",
    ):
        entry = troop_entry(troops, troop_id)
        assert_contains(entry, "tf_hero")
        assert_contains(entry, "no_scene")


def test_seven_defenders_keep_role_gear_and_two_handed_swords() -> None:
    troops = read("compile/module_troops.py")
    role_requirements = {
        "seven_ash_garric_ashbow": ("itm_sword_two_handed_a", "itm_long_bow", "itm_arrows"),
        "seven_ash_oswin_ditchwright": ("itm_sword_two_handed_a", "itm_tools", "itm_tab_shield_round_b"),
        "seven_ash_sir_aldrik_vane": ("itm_sword_two_handed_b", "itm_lance", "itm_hunter", "itm_tab_shield_heater_c"),
        "seven_ash_mirelle_voss": ("itm_sword_two_handed_a", "itm_knife", "itm_dagger", "itm_sword_medieval_a"),
        "seven_ash_tomas_reed": ("itm_sword_two_handed_a", "itm_spear", "itm_tab_shield_round_c"),
        "seven_ash_beren_hardhand": ("itm_sword_two_handed_b", "itm_battle_axe"),
        "seven_ash_sister_elianor": ("itm_sword_two_handed_a", "itm_staff", "itm_robe"),
    }
    for troop_id, required_items in role_requirements.items():
        entry = troop_entry(troops, troop_id)
        for item_id in required_items:
            assert_contains(entry, item_id)


def test_checklist_tracks_unique_troop_slice() -> None:
    checklist = read("docs/campaigns/the_seven_oaths_of_ash_implementation_checklist.md")
    assert_contains(checklist, "- [x] First unique NPC troop anchors are implemented.")
    assert_contains(checklist, "- [x] Locate troop definition sources for unique NPCs.")
    assert_contains(checklist, "- [x] Troop source file: `compile/module_troops.py`")
    assert_contains(checklist, "- [x] Give every defender a two-handed sword sidearm.")
    assert_contains(checklist, "- [x] Add Garric epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Add Oswin epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Add Aldrik epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Add Mirelle epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Add Tomas epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Add Beren epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Add Elianor epilogue and companion offer/refusal.")
    assert_contains(checklist, "- [x] Let qualifying survivors join as companions.")
    assert_contains(checklist, "- [x] Let qualifying survivors stay in Ashwick as trainers/contacts.")
    assert_contains(checklist, "- [x] Let non-qualifying survivors refuse with personal reasons.")
    assert_contains(checklist, "- [x] Let every recruited defender mark the map in their voice.")
    assert_contains(checklist, "- [x] Include defender objections and support.")
    assert_contains(checklist, "- [x] Let player assign companions or defenders as sector leaders.")
    assert_contains(checklist, "- [x] Memorialize dead defenders by craft and relationship.")
    assert_contains(checklist, "- [x] Verify endings store compact flags.")
    assert_contains(checklist, "Implementation status: **complete and build-verified**")
    assert_contains(checklist, "- [x] Implementation checklist separates code-complete items from manual playtest-only items.")
    assert_contains(checklist, "- [x] Menus remain structural: travel, staging, confirmation, and outcome summary.")
    assert_contains(checklist, "- [x] Dialogue remains the primary surface for persuasion, moral choice, companion trust, and refusal.")
    assert_contains(checklist, "- [x] Static tests now guard implementation completeness, dialogue craft, aftermath flags, and build surfaces.")
    assert_contains(checklist, "- [ ] Manual playtest pass remains the only non-static completion gate.")


if __name__ == "__main__":
    test_quest_foundation_is_registered()
    test_state_slots_and_defender_bits_exist()
    test_act2_gate_and_companion_foundation_are_explicit()
    test_campaign_state_repair_and_defender_bit_count_helpers_exist()
    test_act2_pacing_has_couriers_scouts_late_route_pressure_and_emergency_return()
    test_host_scaling_foundation_matches_design_range()
    test_dialogue_first_metadata_is_present()
    test_act_i_menus_are_registered_and_dialogue_first()
    test_act_i_resolvers_set_pressure_readiness_and_chain_state()
    test_act2_status_scripts_prevent_double_resolution()
    test_first_defender_scene_menus_are_registered_and_dialogue_framed()
    test_aldrik_recruitment_road_is_dialogue_driven()
    test_mirelle_recruitment_road_is_dialogue_driven()
    test_tomas_recruitment_road_is_dialogue_driven()
    test_beren_recruitment_road_is_dialogue_driven()
    test_elianor_recruitment_road_is_dialogue_driven()
    test_act2_manual_close_marks_unresolved_roads_abandoned()
    test_return_to_ashwick_starts_act3_through_dialogue()
    test_act3_pressure_interludes_are_dialogue_driven_and_stateful()
    test_oath_council_is_dialogue_first_and_sets_final_plan()
    test_sector_commitment_focus_is_stored_for_siege()
    test_outer_fields_siege_phase_is_executable_and_stateful()
    test_palisade_siege_phase_uses_preparation_and_hands_to_breach()
    test_breach_siege_phase_uses_elite_core_and_hands_to_streets()
    test_inner_streets_siege_phase_uses_civilian_safety_and_hands_to_churchyard()
    test_churchyard_siege_phase_resolves_wulfred_and_aftermath()
    test_immediate_aftermath_counts_costs_and_records_first_count()
    test_aftermath_archives_memorials_and_compact_ending_flags()
    test_garric_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_oswin_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_aldrik_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_mirelle_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_tomas_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_beren_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_elianor_aftermath_companion_offer_is_survival_and_unlock_gated()
    test_first_defender_return_scenes_change_ashwick_readiness()
    test_first_defender_choices_live_in_dialogue_files()
    test_seven_oaths_unique_troop_anchors_exist()
    test_seven_defenders_keep_role_gear_and_two_handed_swords()
    test_checklist_tracks_unique_troop_slice()
    print("test_seven_oaths_static: OK")
