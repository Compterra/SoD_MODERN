# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected stale token: {needle}")


def assert_script_has_membership_guard(raw: str, script_name: str) -> None:
    marker = f'("{script_name}",'
    start = raw.find(marker)
    if start < 0:
        raise AssertionError(f"Missing script: {script_name}")
    next_start = raw.find('\n("', start + len(marker))
    body = raw[start:] if next_start < 0 else raw[start:next_start]
    assert_contains(body, "(is_between, \":companion\", companions_begin, companions_end)")
    assert_contains(body, "(main_party_has_troop, \":companion\")")


def assert_role_reader_has_party_guard(path: str) -> None:
    raw = read(path)
    if "slot_troop_companion_role" not in raw:
        raise AssertionError(f"Expected companion role reader in {path}")
    assert_contains(raw, "main_party_has_troop")


def assert_cleanup_after_removal(path: str) -> None:
    raw = read(path)
    if "remove_member_from_party" not in raw and "party_remove_members" not in raw:
        raise AssertionError(f"Expected removal operation in {path}")
    assert_contains(raw, "script_sod_companion_cleanup_departed_companion")


def assert_companion_depth_player_entries_are_party_guarded() -> None:
    for path in (ROOT / "src/dialogs/ZE01_companions_and_named_npcs").glob("anyone_plyr_companion_depth_*.py"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if '"member_talk"' not in raw:
            continue
        assert_contains(raw, "main_party_has_troop")


def assert_companion_setup_call_is_party_guarded(path: str) -> None:
    raw = read(path)
    assert_contains(raw, "script_setup_talk_info_companions")
    assert_contains(raw, '(is_between, "$g_talk_troop", companions_begin, companions_end)')
    assert_contains(raw, '(main_party_has_troop, "$g_talk_troop")')


def main() -> int:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    camp_action = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    town_menu = read("src/menus/centers/castle/castle_castle.py")
    mission_order = read("src/mission_templates/_order_mission_templates.txt")
    klethi_alley_mission = read("src/mission_templates/0057_companion_klethi_alley/companion_klethi_alley.py")
    ymira_refugee_mission = read("src/mission_templates/0058_companion_ymira_refugee_defense/companion_ymira_refugee_defense.py")
    firentis_restitution_mission = read("src/mission_templates/0059_companion_firentis_restitution_defense/companion_firentis_restitution_defense.py")
    deshavi_trail_mission = read("src/mission_templates/0060_companion_deshavi_trail_rescue/companion_deshavi_trail_rescue.py")
    borcha_road_mission = read("src/mission_templates/0061_companion_borcha_counter_ambush/companion_borcha_counter_ambush.py")
    marnid_warehouse_mission = read("src/mission_templates/0062_companion_marnid_warehouse/companion_marnid_warehouse.py")
    bunduk_line_mission = read("src/mission_templates/0063_companion_bunduk_line_test/companion_bunduk_line_test.py")
    jeremus_infirmary_mission = read("src/mission_templates/0064_companion_jeremus_infirmary/companion_jeremus_infirmary.py")
    lezalit_drill_mission = read("src/mission_templates/0065_companion_lezalit_drill_trial/companion_lezalit_drill_trial.py")
    artimenner_repair_mission = read("src/mission_templates/0066_companion_artimenner_repair_watch/companion_artimenner_repair_watch.py")
    alayen_standard_mission = read("src/mission_templates/0067_companion_alayen_standard_test/companion_alayen_standard_test.py")
    rolf_public_mission = read("src/mission_templates/0068_companion_rolf_public_proof/companion_rolf_public_proof.py")
    baheshtur_oath_mission = read("src/mission_templates/0069_companion_baheshtur_rider_oath/companion_baheshtur_rider_oath.py")
    matheld_line_mission = read("src/mission_templates/0070_companion_matheld_shield_line/companion_matheld_shield_line.py")
    katrin_supply_mission = read("src/mission_templates/0071_companion_katrin_supply_watch/companion_katrin_supply_watch.py")
    nizar_lane_mission = read("src/mission_templates/0072_companion_nizar_charge_lane/companion_nizar_charge_lane.py")
    campfire = read("src/menus/camp/companion_campfire.py")
    ymira_mercy_menu = read("src/menus/camp/ymira_mercy_under_arms.py")
    lezalit_discipline_menu = read("src/menus/camp/lezalit_discipline_without_chains.py")
    bunduk_line_menu = read("src/menus/camp/bunduk_men_hold_line.py")
    jeremus_triage_menu = read("src/menus/camp/jeremus_hands_triage.py")
    firentis_restitution_menu = read("src/menus/camp/firentis_debt_restitution.py")
    katrin_last_coin_menu = read("src/menus/camp/katrin_last_coin.py")
    companion_qa_menu = read("src/menus/camp/companion_interactive_quest_qa.py")
    borcha_road_menu = read("src/menus/camp/borcha_road_keeps_own.py")
    marnid_price_menu = read("src/menus/camp/marnid_honest_price.py")
    deshavi_tracks_menu = read("src/menus/camp/deshavi_tracks_through_ash.py")
    klethi_knife_menu = read("src/menus/camp/klethi_knife_with_name.py")
    rolf_name_menu = read("src/menus/camp/rolf_name_worth_wearing.py")
    alayen_standard_menu = read("src/menus/camp/alayen_standard_self.py")
    nizar_charge_menu = read("src/menus/camp/nizar_impossible_charge.py")
    baheshtur_saddle_menu = read("src/menus/camp/baheshtur_unbroken_saddle.py")
    matheld_step_menu = read("src/menus/camp/matheld_no_backward_step.py")
    artimenner_siege_menu = read("src/menus/camp/artimenner_siege_that_should.py")
    depth_report = read("src/menus/camp/companion_depth_report.py")
    company_report = read("src/scripts/ZY_helper_scripts/companion_describe_company_report.py")
    quitting_yes = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_yes.py")
    quitting_no_confirmed = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_no_confirmed.py")
    quitting_persuasion = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_persuasion_02.py")
    menu_order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    companion_bible = read("docs/COMPANION_DEPTH_BIBLE.md")
    companion_checklist = read("docs/COMPANION_OVERHAUL_CHECKLIST.md")
    interactive_quest_checklist = read("docs/COMPANION_INTERACTIVE_QUEST_CHECKLIST.md")
    interactive_quest_playtest = read("docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md")
    interactive_quest_qa_commands = read("docs/COMPANION_INTERACTIVE_QUEST_QA_COMMANDS.md")
    companion_quests = read("src/quests/0012_companion_personal_quests.py")

    assert_not_contains(companion_quests, "    qf_random_quest,")
    assert_contains(companion_quests, "deliberately dormant at game start")
    assert_contains(companion_quests, "script_sod_companion_sync_personal_quest_framework")
    assert_contains(scripts, '"sod_companion_sync_personal_quest_framework"')
    assert_contains(scripts, "script_sod_quest_runtime_accept")
    assert_contains(scripts, "sod_companion_quest_trust_unlocked")
    for guarded_script in (
        "sod_companion_shift_approval",
        "sod_companion_shift_core_value_proof",
        "sod_companion_try_trigger_reaction",
        "sod_companion_advance_personal_quest",
    ):
        assert_script_has_membership_guard(scripts, guarded_script)
    assert_contains(scripts, 'script_sod_companion_cleanup_departed_companion", ":companion"')
    assert_contains(scripts, '(assign, "$g_sod_ymira_refugee_focus_center", 0)')
    assert_contains(scripts, '(assign, "$g_sod_klethi_old_job_contacted", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_contacted", 0)')
    assert_contains(scripts, "(troop_set_slot, \":companion\", slot_troop_companion_role, sod_companion_role_none)")
    assert_contains(scripts, "(neq, \":warning_state\", sod_companion_warning_broken)")
    assert_contains(scripts, "(troop_set_slot, \":companion\", slot_troop_companion_warning_state, sod_companion_warning_none)")
    assert_contains(scripts, "(is_between, \":role\", sod_companion_role_none, sod_companion_role_spymaster + 1)")
    assert_contains(scripts, '(eq, "$npc_with_grievance", ":companion")')
    assert_contains(scripts, '(assign, "$npc_with_grievance", 0)')
    assert_contains(scripts, '(eq, "$npc_with_personality_clash", ":companion")')
    assert_contains(scripts, '(assign, "$npc_with_personality_clash", 0)')
    assert_contains(scripts, '(eq, "$npc_with_personality_clash_2", ":companion")')
    assert_contains(scripts, '(assign, "$npc_with_personality_clash_2", 0)')
    assert_contains(scripts, '(eq, "$npc_with_personality_match", ":companion")')
    assert_contains(scripts, '(assign, "$npc_with_personality_match", 0)')
    assert_contains(scripts, '(eq, "$g_companion_banter_pair_a", ":companion")')
    assert_contains(scripts, '(assign, "$g_companion_banter_pair_a", -1)')
    assert_contains(scripts, '(assign, "$g_companion_banter_pair_b", -1)')
    assert_contains(scripts, '(eq, "$g_companion_banter_last_pair_a", ":companion")')
    reduce_clash = read("src/scripts/ZH_heroes/reduce_companion_morale_for_clash.py")
    assert_contains(reduce_clash, '(is_between, ":companion_1", companions_begin, companions_end)')
    assert_contains(reduce_clash, '(is_between, ":companion_2", companions_begin, companions_end)')
    assert_contains(reduce_clash, '(main_party_has_troop, ":companion_1")')
    assert_contains(reduce_clash, '(main_party_has_troop, ":companion_2")')
    post_battle_clash = read("src/scripts/ZE_encounters/post_battle_personality_clash_check.py")
    assert_contains(post_battle_clash, '(main_party_has_troop, "$npc_with_personality_clash_2")')
    assert_contains(post_battle_clash, '(main_party_has_troop, "$npc_with_personality_match")')
    assert_contains(post_battle_clash, '(assign, "$npc_with_personality_clash_2", 0)')
    assert_contains(post_battle_clash, '(assign, "$npc_with_personality_match", 0)')
    personality_match_entry = read("src/dialogs/ZA01_startup_and_dispatch/anyone_event_triggered_08.py")
    assert_contains(personality_match_entry, '(main_party_has_troop, "$map_talk_troop")')
    assert_contains(personality_match_entry, '(main_party_has_troop, ":object")')
    morality_grievance_entry = read("src/dialogs/ZA01_startup_and_dispatch/anyone_event_triggered_05.py")
    assert_contains(morality_grievance_entry, '(main_party_has_troop, "$map_talk_troop")')
    home_intro_entry = read("src/dialogs/ZA01_startup_and_dispatch/anyone_event_triggered_09.py")
    assert_contains(home_intro_entry, '(main_party_has_troop, "$map_talk_troop")')
    personality_clash_entry = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_personalityclash_b.py")
    assert_contains(personality_clash_entry, '(eq, "$npc_map_talk_context", slot_troop_personalityclash_state)')
    assert_contains(personality_clash_entry, '(main_party_has_troop, "$map_talk_troop")')
    assert_contains(personality_clash_entry, '(main_party_has_troop, ":object")')
    assert_contains(personality_clash_entry, '(assign, "$npc_with_personality_clash", 0)')
    personality_clash_2_entry = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_personalityclash2_b.py")
    assert_contains(personality_clash_2_entry, '(eq, "$npc_map_talk_context", slot_troop_personalityclash2_state)')
    assert_contains(personality_clash_2_entry, '(main_party_has_troop, "$map_talk_troop")')
    assert_contains(personality_clash_2_entry, '(main_party_has_troop, ":object")')
    assert_contains(personality_clash_2_entry, '(assign, "$npc_with_personality_clash_2", 0)')
    personality_match_b_entry = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_personalitymatch_b.py")
    assert_contains(personality_match_b_entry, '(eq, "$npc_map_talk_context", slot_troop_personalitymatch_state)')
    assert_contains(personality_match_b_entry, '(main_party_has_troop, "$map_talk_troop")')
    assert_contains(personality_match_b_entry, '(main_party_has_troop, ":object")')
    assert_contains(personality_match_b_entry, '(assign, "$npc_with_personality_match", 0)')
    assert_companion_depth_player_entries_are_party_guarded()
    assert_companion_setup_call_is_party_guarded("src/dialogs/ZA01_startup_and_dispatch/anyone_member_chat.py")
    assert_companion_setup_call_is_party_guarded("src/dialogs/ZA01_startup_and_dispatch/anyone_event_triggered.py")
    for removal_path in (
        "src/scripts/ZH_heroes/retire_companion.py",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_yes.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_member_separate_yes.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_mission_lend_companion_accepted.py",
        "src/scripts/ZC_parties/party_remove_all_companions.py",
        "src/menus/other/continue_48.py",
    ):
        assert_cleanup_after_removal(removal_path)
    assert_contains(read("src/triggers/ST02_every_hour/entry_0086.py"), "script_sod_companion_cleanup_departed_companion")
    for role_reader in (
        "src/scripts/ZY_helper_scripts/sod_prisoner_economy.py",
        "src/scripts/ZY_helper_scripts/sod_get_companion_patrol_role_bonus.py",
        "src/scripts/ZY_helper_scripts/sod_company_accounts.py",
        "src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py",
        "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
        "src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py",
    ):
        assert_role_reader_has_party_guard(role_reader)

    for token in (
        "slot_troop_companion_approval",
        "slot_troop_companion_trust_tier",
        "slot_troop_companion_personal_quest_stage",
        "slot_troop_companion_role",
        "slot_troop_companion_last_reaction_day",
        "slot_troop_companion_warning_state",
        "slot_troop_companion_core_value_proof",
        "sod_companion_approval_devoted",
        "sod_companion_warning_final",
        "sod_companion_role_surgeon",
        "sod_companion_role_captain",
        "sod_companion_focus_refugee_shelter",
        "sod_companion_focus_trail_pressure",
        "sod_companion_focus_restitution_village",
        "sod_companion_action_free_captives",
        "sod_companion_action_buy_slaves",
        "sod_companion_action_execute_lord",
        "sod_companion_action_defeat_imperials",
        "sod_companion_action_safe_roadcraft",
        "sod_companion_action_costly_battle",
        "sod_companion_action_orderly_profit",
        "sod_companion_action_dirty_profit",
        "sod_companion_action_food_security",
        "sod_companion_action_hunger",
        "sod_companion_action_stealth_success",
        "sod_companion_action_betray_autonomy",
        "sod_companion_action_hard_victory",
        "sod_companion_action_cowardice",
        "sod_companion_action_trade_profit",
        "sod_companion_action_caravan_protection",
        "sod_companion_action_unpaid_wages",
        "sod_companion_action_honorable_peace",
        "sod_companion_action_diplomacy_betrayal",
        "sod_companion_action_siege_preparation",
        "sod_companion_action_scout_warning",
        "sod_companion_action_black_khergit_camp_defeat",
        "sod_companion_action_build_healing",
        "sod_companion_action_build_market",
        "sod_companion_action_black_army_security",
        "sod_companion_action_tournament_glory",
        "sod_companion_action_build_security",
        "sod_companion_action_efficient_construction",
        "sod_companion_action_ymira_refugee_mercy",
        "sod_companion_action_ymira_refugee_expedience",
        "sod_companion_action_lezalit_ief_reform",
        "sod_companion_action_lezalit_ief_harsh",
    ):
        assert_contains(constants, token)

    for script_name in (
        '"sod_companion_initialize_depth"',
        '"sod_companion_apply_player_action"',
        '"sod_companion_get_approval_band"',
        '"sod_companion_warning_to_s0"',
        '"sod_companion_reconciliation_to_s0"',
        '"sod_companion_warning_state_to_s3"',
        '"sod_companion_quest_stage_to_s5"',
        '"sod_companion_role_bonus_to_s6"',
        '"sod_companion_role_status_to_s7"',
        '"sod_companion_role_inactive_to_s6"',
        '"sod_companion_report_line_to_s0"',
        '"sod_companion_describe_triangles_to_s27"',
        '"sod_companion_describe_banter_seeds_to_s28"',
        '"sod_companion_describe_late_reflections_to_s29"',
        '"sod_companion_describe_world_followups_to_s32"',
        '"sod_companion_describe_framework_aftermath_to_s33"',
        '"sod_companion_describe_depth_report_to_s1"',
        '"sod_companion_describe_company_depth_to_s30"',
        '"sod_companion_describe_role_offices_to_s31"',
        '"sod_companion_process_departure_risk"',
        '"sod_companion_process_daily_depth"',
        '"sod_companion_cleanup_absent_state"',
        '"sod_companion_cleanup_departed_companion"',
        '"sod_companion_try_trigger_reaction"',
        '"sod_companion_try_action_followup_message"',
        '"sod_companion_try_triangle_incident"',
        '"sod_companion_record_triangle_quest_event"',
        '"sod_companion_shift_core_value_proof"',
        '"sod_companion_assign_role"',
        '"sod_companion_apply_role_effects"',
        '"sod_companion_advance_personal_quest"',
        '"sod_companion_sync_personal_quest_framework"',
        '"sod_companion_apply_hard_compromise_payoff"',
        '"sod_companion_select_focus_village"',
        '"sod_companion_try_ymira_refugee_incident"',
        '"sod_companion_try_ymira_refugee_expedience"',
        '"sod_companion_ymira_apply_mercy_payoff"',
        '"sod_companion_try_lezalit_ief_discipline_incident"',
        '"sod_companion_lezalit_apply_discipline_payoff"',
        '"sod_companion_try_bunduk_line_incident"',
        '"sod_companion_bunduk_apply_line_payoff"',
        '"sod_companion_try_jeremus_triage_incident"',
        '"sod_companion_jeremus_apply_triage_payoff"',
        '"sod_companion_try_firentis_restitution_incident"',
        '"sod_companion_firentis_apply_restitution_payoff"',
        '"sod_companion_try_katrin_last_coin_incident"',
        '"sod_companion_katrin_apply_last_coin_payoff"',
        '"sod_companion_try_deshavi_trail_warning_incident"',
        '"sod_companion_deshavi_apply_trail_payoff"',
        '"sod_companion_try_klethi_old_job_incident"',
        '"sod_companion_klethi_apply_old_job_payoff"',
        '"sod_companion_try_rolf_name_challenge_incident"',
        '"sod_companion_rolf_apply_name_payoff"',
        '"sod_companion_try_alayen_standard_incident"',
        '"sod_companion_alayen_apply_standard_payoff"',
        '"sod_companion_try_nizar_charge_incident"',
        '"sod_companion_nizar_apply_charge_payoff"',
        '"sod_companion_try_baheshtur_saddle_incident"',
        '"sod_companion_baheshtur_apply_saddle_payoff"',
        '"sod_companion_try_matheld_no_backward_step_incident"',
        '"sod_companion_matheld_apply_step_payoff"',
        '"sod_companion_try_artimenner_siege_incident"',
        '"sod_companion_artimenner_apply_siege_payoff"',
        '"sod_companion_borcha_describe_to_s11"',
        '"sod_companion_marnid_describe_to_s12"',
        '"sod_companion_ymira_describe_to_s13"',
        '"sod_companion_rolf_describe_to_s23"',
        '"sod_companion_baheshtur_describe_to_s25"',
        '"sod_companion_firentis_describe_to_s17"',
        '"sod_companion_jeremus_describe_to_s18"',
        '"sod_companion_katrin_describe_to_s20"',
        '"sod_companion_matheld_describe_to_s21"',
        '"sod_companion_alayen_describe_to_s22"',
        '"sod_companion_nizar_describe_to_s24"',
        '"sod_companion_lezalit_describe_to_s14"',
        '"sod_companion_artimenner_describe_to_s26"',
        '"sod_companion_deshavi_describe_to_s15"',
        '"sod_companion_bunduk_describe_to_s19"',
        '"sod_companion_klethi_describe_to_s16"',
    ):
        assert_contains(scripts, script_name)

    assert_contains(scripts, "trp_npc1")
    assert_contains(scripts, "trp_npc2")
    assert_contains(scripts, "trp_npc3")
    assert_contains(scripts, "trp_npc4")
    assert_contains(scripts, "trp_npc5")
    assert_contains(scripts, "trp_npc6")
    assert_contains(scripts, "trp_npc7")
    assert_contains(scripts, "trp_npc8")
    assert_contains(scripts, "trp_npc9")
    assert_contains(scripts, "trp_npc10")
    assert_contains(scripts, "trp_npc11")
    assert_contains(scripts, "trp_npc12")
    assert_contains(scripts, "trp_npc13")
    assert_contains(scripts, "trp_npc14")
    assert_contains(scripts, "trp_npc15")
    assert_contains(scripts, "trp_npc16")
    assert_contains(campfire, "The Road Keeps Its Own")
    assert_contains(campfire, "The Honest Price")
    assert_contains(campfire, "sod_companion_action_safe_roadcraft")
    assert_contains(campfire, "sod_companion_action_orderly_profit")
    assert_contains(campfire, "companion_campfire_ymira_mercy_spare")
    assert_contains(campfire, "companion_campfire_ymira_mercy_hard")
    assert_contains(campfire, "Mercy Under Arms")
    assert_contains(campfire, "A Name Worth Wearing")
    assert_contains(campfire, "companion_campfire_rolf_name_earn")
    assert_contains(campfire, "companion_campfire_rolf_name_hard")
    assert_contains(campfire, "The Unbroken Saddle")
    assert_contains(campfire, "companion_campfire_baheshtur_saddle_free")
    assert_contains(campfire, "companion_campfire_baheshtur_saddle_hard")
    assert_contains(campfire, "Debt of the Sword")
    assert_contains(campfire, "companion_campfire_firentis_debt_restitution")
    assert_contains(campfire, "companion_campfire_firentis_debt_hard")
    assert_contains(campfire, "Hands That Will Not Harden")
    assert_contains(campfire, "companion_campfire_jeremus_hands_civilians")
    assert_contains(campfire, "companion_campfire_jeremus_hands_hard")
    assert_contains(campfire, "companion_campfire_lezalit_discipline_reform")
    assert_contains(campfire, "companion_campfire_lezalit_discipline_hard")
    assert_contains(campfire, "Discipline Without Chains")
    assert_contains(campfire, "The Siege That Should Have Worked")
    assert_contains(campfire, "companion_campfire_artimenner_siege_prepare")
    assert_contains(campfire, "companion_campfire_artimenner_siege_hard")
    assert_contains(campfire, "Tracks Through Ash")
    assert_contains(campfire, "companion_campfire_deshavi_tracks_rescue")
    assert_contains(campfire, "companion_campfire_deshavi_tracks_hard")
    assert_contains(campfire, "The Men Who Hold the Line")
    assert_contains(campfire, "companion_campfire_bunduk_line_advocate")
    assert_contains(campfire, "companion_campfire_bunduk_line_hard")
    assert_contains(campfire, "The Last Coin in Camp")
    assert_contains(campfire, "companion_campfire_katrin_coin_stores")
    assert_contains(campfire, "companion_campfire_katrin_coin_hard")
    assert_contains(campfire, "No Backward Step")
    assert_contains(campfire, "companion_campfire_matheld_step_stand")
    assert_contains(campfire, "companion_campfire_matheld_step_hard")
    assert_contains(campfire, "The Standard and the Self")
    assert_contains(campfire, "companion_campfire_alayen_standard_duty")
    assert_contains(campfire, "companion_campfire_alayen_standard_hard")
    assert_contains(campfire, "The Impossible Charge")
    assert_contains(campfire, "companion_campfire_nizar_charge_daring")
    assert_contains(campfire, "companion_campfire_nizar_charge_hard")
    assert_contains(campfire, "A Knife With a Name")
    assert_contains(campfire, "companion_campfire_klethi_knife_protect")
    assert_contains(campfire, "companion_campfire_klethi_knife_hard")
    assert_contains(game_start, "script_sod_companion_initialize_depth")
    assert_contains(daily, "script_sod_companion_process_daily_depth")
    assert_contains(camp_action, "mnu_companion_campfire")
    assert_contains(camp_action, "mnu_companion_depth_report")
    assert_contains(camp_action, "mnu_borcha_road_keeps_own")
    assert_contains(camp_action, "Speak with Borcha about the hidden road")
    assert_contains(camp_action, "mnu_marnid_honest_price")
    assert_contains(camp_action, "Speak with Marnid about the suspect contract")
    assert_contains(camp_action, "mnu_ymira_mercy_under_arms")
    assert_contains(camp_action, "Speak with Ymira about the captives")
    assert_contains(camp_action, "mnu_lezalit_discipline_without_chains")
    assert_contains(camp_action, "Speak with Lezalit about the captured Imperial drill")
    assert_contains(camp_action, "mnu_bunduk_men_hold_line")
    assert_contains(camp_action, "Speak with Bunduk about the line's grievance")
    assert_contains(camp_action, "mnu_jeremus_hands_triage")
    assert_contains(camp_action, "Speak with Jeremus among the wounded")
    assert_contains(camp_action, "mnu_firentis_debt_restitution")
    assert_contains(camp_action, "Speak with Firentis about restitution")
    assert_contains(camp_action, "mnu_katrin_last_coin")
    assert_contains(camp_action, "Speak with Katrin about the last coin")
    assert_contains(camp_action, "mnu_deshavi_tracks_through_ash")
    assert_contains(camp_action, "Speak with Deshavi about the trail warning")
    assert_contains(camp_action, "mnu_klethi_knife_with_name")
    assert_contains(camp_action, "Speak with Klethi about the old job")
    assert_contains(camp_action, "mnu_rolf_name_worth_wearing")
    assert_contains(camp_action, "Speak with Rolf about the public challenge")
    assert_contains(camp_action, "mnu_alayen_standard_self")
    assert_contains(camp_action, "Speak with Alayen about the standard oath")
    assert_contains(camp_action, "mnu_nizar_impossible_charge")
    assert_contains(camp_action, "Speak with Nizar about the impossible charge")
    assert_contains(camp_action, "mnu_baheshtur_unbroken_saddle")
    assert_contains(camp_action, "Speak with Baheshtur about the saddle oath")
    assert_contains(camp_action, "mnu_matheld_no_backward_step")
    assert_contains(camp_action, "Speak with Matheld about the shield challenge")
    assert_contains(camp_action, "mnu_artimenner_siege_that_should")
    assert_contains(camp_action, "Speak with Artimenner about the siege design")
    assert_contains(camp_action, "camp_companion_depth_debug")
    assert_contains(camp_action, "camp_companion_interactive_quest_qa")
    assert_contains(camp_action, "DEBUG: Companion interactive quest QA.")
    assert_contains(menu_order, "camp/companion_interactive_quest_qa.py")
    assert_contains(companion_qa_menu, '"companion_interactive_quest_qa"')
    assert_contains(companion_qa_menu, '(neq, "$g_sod_debug", 1)')
    assert_contains(companion_qa_menu, "script_sod_companion_qa_recruit_roster")
    assert_contains(companion_qa_menu, "script_sod_companion_qa_prime_interactive_quest")
    assert_contains(companion_qa_menu, "ready for road climax")
    assert_contains(companion_qa_menu, "ready for charge-lane test")
    assert_contains(companion_qa_menu, "ready for aftermath")
    assert_contains(companion_qa_menu, "trp_npc16")
    assert_contains(scripts, '"sod_companion_qa_recruit_roster"')
    assert_contains(scripts, '"sod_companion_qa_prime_interactive_quest"')
    assert_contains(scripts, '(eq, "$g_sod_debug", 1)')
    assert_contains(scripts, "QA: companion roster recruited")
    assert_contains(scripts, "QA: {s1} is primed for the live interactive quest climax.")
    assert_contains(scripts, "QA: {s1} is primed for final interactive quest aftermath.")
    assert_contains(camp_action, "DEBUG: Inspect companion approval bands.")
    assert_contains(read("src/menus/camp/company_accounts.py"), "company_accounts_katrin_petition")
    assert_contains(read("src/menus/camp/company_accounts.py"), "$g_sod_katrin_last_coin_witnessed")
    assert_contains(read("src/menus/camp/company_accounts.py"), "$g_sod_katrin_last_coin_witnessed")
    for pending_global in (
        "$g_sod_borcha_road_pending",
        "$g_sod_marnid_market_pending",
        "$g_sod_lezalit_ief_discipline_pending",
        "$g_sod_bunduk_line_pending",
        "$g_sod_jeremus_triage_pending",
        "$g_sod_firentis_restitution_pending",
        "$g_sod_katrin_last_coin_pending",
        "$g_sod_deshavi_trail_warning_pending",
        "$g_sod_klethi_old_job_pending",
        "$g_sod_rolf_name_challenge_pending",
        "$g_sod_alayen_standard_pending",
        "$g_sod_nizar_charge_pending",
        "$g_sod_baheshtur_saddle_pending",
        "$g_sod_matheld_no_backward_step_pending",
        "$g_sod_artimenner_siege_pending",
    ):
        assert_contains(scripts, f'(assign, "{pending_global}", 0)')
    for focus_global in (
        "$g_sod_ymira_refugee_focus_center",
        "$g_sod_deshavi_trail_focus_center",
        "$g_sod_firentis_restitution_focus_center",
    ):
        assert_contains(scripts, f'(assign, "{focus_global}", 0)')
    for witness_global in (
        "$g_sod_ymira_refugee_witnessed",
        "$g_sod_deshavi_trail_witnessed",
        "$g_sod_firentis_restitution_witnessed",
    ):
        assert_contains(scripts, f'(assign, "{witness_global}", 0)')
    assert_contains(scripts, '(assign, "$g_sod_klethi_old_job_contacted", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_contacted", 0)')
    assert_contains(scripts, '(assign, "$g_sod_lezalit_ief_discipline_witnessed", 0)')
    assert_contains(scripts, '(assign, "$g_sod_bunduk_line_witnessed", 0)')
    assert_contains(scripts, '(assign, "$g_sod_jeremus_triage_witnessed", 0)')
    assert_contains(scripts, '(assign, "$g_sod_baheshtur_saddle_witnessed", 0)')
    assert_contains(scripts, '(assign, "$g_sod_katrin_last_coin_witnessed", 0)')
    assert_contains(scripts, '(assign, "$g_sod_deshavi_trail_confronted", 0)')
    assert_contains(scripts, '(assign, "$g_sod_deshavi_trail_result_grade", 0)')
    assert_contains(scripts, '(assign, "$g_sod_borcha_road_origin_center", 0)')
    assert_contains(scripts, '(assign, "$g_sod_borcha_road_destination_center", 0)')
    assert_contains(scripts, '(assign, "$g_sod_borcha_road_witnessed", 0)')
    assert_contains(scripts, '(assign, "$g_sod_borcha_road_confronted", 0)')
    assert_contains(scripts, '(assign, "$g_sod_borcha_road_result_grade", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_pending", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_focus_center", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_evidence", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_confronted", 0)')
    assert_contains(scripts, '(assign, "$g_sod_marnid_market_result_grade", 0)')

    for incident_menu in (
        borcha_road_menu,
        marnid_price_menu,
        ymira_mercy_menu,
        lezalit_discipline_menu,
        bunduk_line_menu,
        jeremus_triage_menu,
        firentis_restitution_menu,
        katrin_last_coin_menu,
        deshavi_tracks_menu,
        klethi_knife_menu,
        rolf_name_menu,
        alayen_standard_menu,
        nizar_charge_menu,
        baheshtur_saddle_menu,
        matheld_step_menu,
        artimenner_siege_menu,
    ):
        assert_contains(incident_menu, '(jump_to_menu, "mnu_camp_action")')

    for companion_guard in (
        (borcha_road_menu, '"trp_npc1"'),
        (marnid_price_menu, '"trp_npc2"'),
        (ymira_mercy_menu, '"trp_npc3"'),
        (lezalit_discipline_menu, '"trp_npc14"'),
        (bunduk_line_menu, '"trp_npc10"'),
        (jeremus_triage_menu, '"trp_npc12"'),
        (firentis_restitution_menu, '"trp_npc6"'),
        (katrin_last_coin_menu, '"trp_npc11"'),
        (deshavi_tracks_menu, '"trp_npc7"'),
        (klethi_knife_menu, '"trp_npc16"'),
        (rolf_name_menu, '"trp_npc4"'),
        (alayen_standard_menu, '"trp_npc9"'),
        (nizar_charge_menu, '"trp_npc13"'),
        (baheshtur_saddle_menu, '"trp_npc5"'),
        (matheld_step_menu, '"trp_npc8"'),
        (artimenner_siege_menu, '"trp_npc15"'),
    ):
        assert_contains(companion_guard[0], f"main_party_has_troop, {companion_guard[1]}")

    assert_contains(scripts, "Companion Campfire")
    assert_contains(depth_report, "script_sod_companion_describe_depth_report_to_s1")
    assert_contains(depth_report, "mnu_companion_campfire")
    assert_contains(scripts, "Companion Depth Report")
    assert_contains(scripts, "Banter seeds:")
    assert_contains(scripts, "Late reflections:")
    assert_contains(scripts, "slot_troop_companion_core_value_proof")
    assert_contains(scripts, "Repeated value - Ymira")
    assert_contains(scripts, "Repeated value - Lezalit")
    assert_contains(scripts, "Repeated value - Klethi")
    assert_contains(scripts, "Repeated break - Ymira")
    assert_contains(scripts, "Repeated break - Bunduk")
    assert_contains(scripts, "Repeated break - Artimenner")
    assert_contains(scripts, "World follow-ups:")
    assert_contains(scripts, "Quest-framework aftermath:")
    assert_contains(scripts, "personal matter active")
    assert_contains(scripts, "resolved well")
    assert_contains(scripts, "Road and ledger synergy")
    assert_contains(scripts, "road safety and Black Khergit pressure")
    assert_contains(scripts, "engineering discipline and fewer bad works")
    assert_contains(scripts, "office inactive until trust returns")
    assert_contains(scripts, "Borcha keeps the road notes folded until trust returns")
    assert_contains(scripts, "Marnid closes the ledger until trust returns")
    assert_contains(scripts, "Ymira tends wounds but no longer steadies the company")
    assert_contains(scripts, "Rolf's public office becomes ceremony without trust")
    assert_contains(scripts, "Baheshtur keeps the reins short until trust returns")
    assert_contains(scripts, "Firentis keeps discipline quiet until trust returns")
    assert_contains(scripts, "Deshavi withholds under-road warnings until trust returns")
    assert_contains(scripts, "Matheld's shield-line office goes hard and quiet until trust returns")
    assert_contains(scripts, "Alayen's envoy honor cools until trust returns")
    assert_contains(scripts, "Bunduk keeps soldier complaints to himself until trust returns")
    assert_contains(scripts, "Katrin counts stores without spending warmth until trust returns")
    assert_contains(scripts, "Jeremus heals bodies but not morale until trust returns")
    assert_contains(scripts, "Nizar's daring loses its lift until trust returns")
    assert_contains(scripts, "Lezalit drills obedience without inspiration until trust returns")
    assert_contains(scripts, "Artimenner gives measurements, not confidence, until trust returns")
    assert_contains(scripts, "Klethi keeps the useful doors to herself until trust returns")
    assert_contains(scripts, "Marnid keeps extra oats after Borcha predicts bad ground")
    assert_contains(scripts, "Ymira and Bunduk: Ymira names the wounded")
    assert_contains(scripts, "Lezalit praises order, and Bunduk asks how many ordinary men it is allowed to cost")
    assert_contains(scripts, "Firentis keeps guard near the wounded without being asked")
    assert_contains(scripts, "Matheld calls wounds proof; Jeremus asks whether fewer proofs might serve")
    assert_contains(scripts, "Rolf wants applause to remember rank; Nizar wants it to remember timing")
    assert_contains(scripts, "Baheshtur says horses need freedom; Katrin says they also need oats")
    assert_contains(scripts, "Artimenner says a road without measures is waste")
    assert_contains(scripts, "Deshavi hides food for hungry children; Klethi finds it")
    assert_contains(scripts, "Katrin calls theft a leak in the roof")
    assert_contains(scripts, "Ymira: She has seen mercy survive under guard")
    assert_contains(scripts, "Lezalit: He has learned that discipline can hold without chains")
    assert_contains(scripts, "Bunduk: He has started saying the men will hold")
    assert_contains(scripts, "Jeremus: He has not become less sorrowful")
    assert_contains(scripts, "Firentis: Service has become less like punishment")
    assert_contains(scripts, "Rolf: He has begun chasing a name that can survive witnesses")
    assert_contains(scripts, "Alayen: Honor has become labor in his mouth")
    assert_contains(scripts, "Nizar: He has discovered that survival improves a song")
    assert_contains(scripts, "Baheshtur: Chosen loyalty has steadied him")
    assert_contains(scripts, "Matheld: She has seen courage stand without wasting itself")
    assert_contains(scripts, "Artimenner: He no longer expects every plan to be ignored")
    assert_contains(scripts, "Katrin: Practical care has become camp law by habit")
    assert_contains(scripts, "Deshavi: The forgotten have become harder to overlook")
    assert_contains(scripts, "Klethi: Chosen belonging has made her no less sharp")
    assert_contains(scripts, "Borcha's scout office has gone quiet")
    assert_contains(scripts, "old horde trails in past tense")
    assert_contains(scripts, "Borcha reads Black Khergit tracks early")
    assert_contains(scripts, "Marnid keeps the accounts")
    assert_contains(scripts, "trade stability like a promise kept")
    assert_contains(scripts, "Marnid's Honest Price has turned ledgers")
    assert_contains(scripts, "script_sod_companion_describe_role_offices_to_s31")
    assert_contains(scripts, "Company triangles")
    assert_contains(scripts, "Stage banter - Ymira and Lezalit")
    assert_contains(scripts, "Approval banter - Firentis and Jeremus")
    assert_contains(scripts, "Ymira, Bunduk, and Lezalit argue over captives")
    assert_contains(scripts, "Rolf, Alayen, and Nizar nearly turn praise into a duel")
    assert_contains(scripts, "script_sod_companion_record_triangle_quest_event")
    assert_contains(scripts, 'script_sod_companion_record_triangle_quest_event", "trp_npc3", "trp_npc10", "trp_npc14"')
    assert_contains(scripts, 'script_sod_companion_record_triangle_quest_event", "trp_npc4", "trp_npc9", "trp_npc13"')
    assert_contains(scripts, "Slaver Web: Ymira names the captives")
    assert_contains(scripts, "Black Khergits: Borcha listens for old hoofbeats")
    assert_contains(scripts, "Imperial Expedition: Lezalit studies their order for flaws")
    assert_contains(scripts, "Protective Orders: Bunduk respects the hearth guards")
    assert_contains(scripts, "hard compromise steadies the line through fear and discipline")
    assert_contains(scripts, "qst_companion_ymira_mercy_under_arms")
    assert_contains(scripts, "qst_companion_lezalit_discipline_without_chains")
    assert_contains(scripts, "qst_companion_bunduk_men_hold_line")
    assert_contains(scripts, "qst_companion_jeremus_hands_triage")
    assert_contains(scripts, "qst_companion_firentis_debt_restitution")
    for qid in (
        "qst_companion_borcha_road_keeps_own",
        "qst_companion_marnid_honest_price",
        "qst_companion_rolf_name_worth_wearing",
        "qst_companion_baheshtur_unbroken_saddle",
        "qst_companion_deshavi_tracks_through_ash",
        "qst_companion_matheld_no_backward_step",
        "qst_companion_alayen_standard_self",
        "qst_companion_katrin_last_coin",
        "qst_companion_nizar_impossible_charge",
        "qst_companion_artimenner_siege_that_should",
        "qst_companion_klethi_knife_with_name",
    ):
        assert_contains(scripts, qid)
    assert_contains(scripts, "script_sod_quest_runtime_accept")
    assert_contains(scripts, "script_sod_quest_runtime_update")
    assert_contains(scripts, "script_sod_quest_runtime_complete")
    assert_contains(scripts, "script_sod_quest_runtime_fail")
    assert_contains(scripts, "script_sod_quest_dialogue_record_event")
    assert_contains(scripts, "script_sod_quest_journal_update")
    assert_contains(scripts, "script_sod_quest_outcome_apply_consequences")
    assert_contains(scripts, "script_sod_quest_event_dispatch")
    assert_contains(scripts, "Quest journal - Ymira")
    assert_contains(scripts, "Quest journal - Lezalit")
    assert_contains(scripts, "Quest journal - Bunduk")
    assert_contains(scripts, "Quest journal - Jeremus")
    assert_contains(scripts, "Quest journal - Firentis")
    for name in (
        "Quest journal - Borcha",
        "Quest journal - Marnid",
        "Quest journal - Rolf",
        "Quest journal - Baheshtur",
        "Quest journal - Deshavi",
        "Quest journal - Matheld",
        "Quest journal - Alayen",
        "Quest journal - Katrin",
        "Quest journal - Nizar",
        "Quest journal - Artimenner",
        "Quest journal - Klethi",
    ):
        assert_contains(scripts, name)
    assert_contains(scripts, "Ymira and Lezalit")
    assert_contains(scripts, "Alayen and Nizar")
    assert_contains(scripts, "Katrin and Artimenner")
    assert_contains(scripts, "Borcha and Rolf")
    assert_contains(scripts, "Ymira, Lezalit, and Bunduk")
    assert_contains(scripts, "Marnid and Alayen")
    assert_contains(scripts, "Marnid and Baheshtur")
    assert_contains(scripts, "Ymira and Bunduk")
    assert_contains(scripts, "Rolf and Nizar")
    assert_contains(scripts, "Baheshtur and Katrin")
    assert_contains(scripts, "Deshavi and Katrin")
    assert_contains(scripts, "Katrin and Klethi")
    assert_contains(scripts, "Firentis and Matheld")
    assert_contains(scripts, "Matheld and Jeremus")
    assert_contains(scripts, "final warning")
    assert_contains(scripts, "near leaving the company")
    assert_contains(scripts, "$npc_is_quitting")
    assert_contains(scripts, "will confront you about leaving the company")
    assert_contains(scripts, "script_sod_companion_try_trigger_reaction")
    assert_contains(scripts, "has grown troubled by your command")
    assert_contains(scripts, "seems ready to trust you with a deeper truth")
    assert_contains(quitting_yes, "remove_member_from_party")
    assert_contains(quitting_yes, "pp_history_quit")
    assert_contains(quitting_yes, "slot_troop_cur_center")
    assert_contains(quitting_yes, "sod_companion_role_none")
    assert_contains(quitting_no_confirmed, "sod_companion_warning_acknowledged")
    assert_contains(quitting_persuasion, "sod_companion_warning_acknowledged")
    assert_contains(campfire, "script_sod_companion_assign_role")
    assert_contains(campfire, "script_sod_companion_advance_personal_quest")
    assert_contains(campfire, "script_sod_companion_warning_to_s0")
    assert_contains(campfire, "script_sod_companion_reconciliation_to_s0")
    assert_contains(campfire, "companion_campfire_repair_acknowledged_warnings")
    assert_contains(campfire, ":has_pending_warning")
    assert_contains(campfire, ":has_named_warning")
    assert_contains(company_report, "script_sod_companion_describe_company_depth_to_s30")
    assert_contains(menu_order, "camp/companion_campfire.py")
    assert_contains(menu_order, "camp/companion_depth_report.py")
    assert_contains(menu_order, "camp/borcha_road_keeps_own.py")
    assert_contains(menu_order, "camp/marnid_honest_price.py")
    assert_contains(menu_order, "camp/ymira_mercy_under_arms.py")
    assert_contains(menu_order, "camp/lezalit_discipline_without_chains.py")
    assert_contains(menu_order, "camp/bunduk_men_hold_line.py")
    assert_contains(menu_order, "camp/jeremus_hands_triage.py")
    assert_contains(menu_order, "camp/firentis_debt_restitution.py")
    assert_contains(menu_order, "camp/katrin_last_coin.py")
    assert_contains(menu_order, "camp/deshavi_tracks_through_ash.py")
    assert_contains(menu_order, "camp/klethi_knife_with_name.py")
    assert_contains(menu_order, "camp/rolf_name_worth_wearing.py")
    assert_contains(menu_order, "camp/alayen_standard_self.py")
    assert_contains(menu_order, "camp/nizar_impossible_charge.py")
    assert_contains(menu_order, "camp/baheshtur_unbroken_saddle.py")
    assert_contains(menu_order, "camp/matheld_no_backward_step.py")
    assert_contains(menu_order, "camp/artimenner_siege_that_should.py")
    assert_contains(read("src/quests/_order_quests.txt"), "0012_companion_personal_quests.py")
    assert_contains(companion_quests, "companion_ymira_mercy_under_arms")
    assert_contains(companion_quests, "Ymira: Mercy Under Arms")
    assert_contains(companion_quests, "companion_lezalit_discipline_without_chains")
    assert_contains(companion_quests, "Lezalit: Discipline Without Chains")
    assert_contains(companion_quests, "companion_bunduk_men_hold_line")
    assert_contains(companion_quests, "Bunduk: The Men Who Hold the Line")
    assert_contains(companion_quests, "companion_jeremus_hands_triage")
    assert_contains(companion_quests, "Jeremus: Hands That Will Not Harden")
    assert_contains(companion_quests, "companion_firentis_debt_restitution")
    assert_contains(companion_quests, "Firentis: Debt of the Sword")
    for token in (
        "companion_borcha_road_keeps_own",
        "Borcha: The Road Keeps Its Own",
        "companion_marnid_honest_price",
        "Marnid: The Honest Price",
        "companion_rolf_name_worth_wearing",
        "Rolf: A Name Worth Wearing",
        "companion_baheshtur_unbroken_saddle",
        "Baheshtur: The Unbroken Saddle",
        "companion_deshavi_tracks_through_ash",
        "Deshavi: Tracks Through Ash",
        "companion_matheld_no_backward_step",
        "Matheld: No Backward Step",
        "companion_alayen_standard_self",
        "Alayen: The Standard and the Self",
        "companion_katrin_last_coin",
        "Katrin: The Last Coin in Camp",
        "companion_nizar_impossible_charge",
        "Nizar: The Impossible Charge",
        "companion_artimenner_siege_that_should",
        "Artimenner: The Siege That Should Have Worked",
        "companion_klethi_knife_with_name",
        "Klethi: A Knife With a Name",
    ):
        assert_contains(companion_quests, token)
    assert_contains(companion_quests, "slot_troop_companion_personal_quest_stage")
    assert_contains(companion_quests, "dragon_age_style")

    companion_dialog_names = (
        "borcha",
        "marnid",
        "ymira",
        "rolf",
        "baheshtur",
        "firentis",
        "deshavi",
        "matheld",
        "alayen",
        "bunduk",
        "katrin",
        "jeremus",
        "nizar",
        "lezalit",
        "artimenner",
        "klethi",
    )
    for name in companion_dialog_names:
        player_dialog = f"anyone_plyr_companion_depth_{name}.py"
        response_dialog = f"anyone_companion_depth_{name}.py"
        assert_contains(dialog_order, player_dialog)
        assert_contains(dialog_order, response_dialog)
        assert_contains(read(f"src/dialogs/ZE01_companions_and_named_npcs/{player_dialog}"), '"member_talk"')
        assert_contains(read(f"src/dialogs/ZE01_companions_and_named_npcs/{player_dialog}"), f'"companion_depth_{name}"')
        assert_contains(read(f"src/dialogs/ZE01_companions_and_named_npcs/{response_dialog}"), f'"companion_depth_{name}"')
        assert_contains(read(f"src/dialogs/ZE01_companions_and_named_npcs/{response_dialog}"), '"member_talk"')

    for rel in (
        "ZC01_centers_and_economy/anyone_plyr_village_elder_companion_ymira_refugees.py",
        "ZC01_centers_and_economy/anyone_village_elder_companion_ymira_refugees.py",
        "ZC01_centers_and_economy/anyone_plyr_village_elder_companion_deshavi_tracks.py",
        "ZC01_centers_and_economy/anyone_village_elder_companion_deshavi_tracks.py",
        "ZC01_centers_and_economy/anyone_plyr_village_elder_companion_firentis_restitution.py",
        "ZC01_centers_and_economy/anyone_village_elder_companion_firentis_restitution.py",
        "ZC01_centers_and_economy/anyone_plyr_village_elder_companion_alayen_standard.py",
        "ZC01_centers_and_economy/anyone_village_elder_companion_alayen_standard.py",
        "ZC01_centers_and_economy/anyone_plyr_town_dweller_companion_ymira_refugee.py",
        "ZC01_centers_and_economy/anyone_town_dweller_companion_ymira_refugee.py",
        "ZC01_centers_and_economy/anyone_plyr_town_dweller_companion_deshavi_survivor.py",
        "ZC01_centers_and_economy/anyone_town_dweller_companion_deshavi_survivor.py",
        "ZC01_centers_and_economy/anyone_plyr_town_dweller_companion_rolf_name.py",
        "ZC01_centers_and_economy/anyone_town_dweller_companion_rolf_name.py",
        "ZB01_lords_politics_and_family/anyone_plyr_lord_companion_alayen_standard.py",
        "ZB01_lords_politics_and_family/anyone_lord_companion_alayen_standard.py",
        "ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_companion_klethi_contact.py",
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_companion_klethi_contact.py",
        "ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_companion_borcha_road.py",
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_companion_borcha_road.py",
        "ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_lezalit_drill.py",
        "ZZ99_misc_dialogs/anyone_regular_member_companion_lezalit_drill.py",
        "ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_bunduk_line.py",
        "ZZ99_misc_dialogs/anyone_regular_member_companion_bunduk_line.py",
        "ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_jeremus_wounded.py",
        "ZZ99_misc_dialogs/anyone_regular_member_companion_jeremus_wounded.py",
        "ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_ymira_captive.py",
        "ZZ99_misc_dialogs/anyone_regular_member_companion_ymira_captive.py",
        "ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_matheld_line.py",
        "ZZ99_misc_dialogs/anyone_regular_member_companion_matheld_line.py",
        "ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_katrin_ledger.py",
        "ZZ99_misc_dialogs/anyone_regular_member_companion_katrin_ledger.py",
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_companion_nizar_charge.py",
        "ZD01_encounters_battles_and_prisoners/anyone_battle_reason_companion_nizar_charge.py",
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_companion_baheshtur_rider.py",
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_guard_companion_baheshtur_rider.py",
        "ZD01_encounters_battles_and_prisoners/anyone_black_khergit_companion_baheshtur_rider.py",
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_slaver_world_caravan_companion_deshavi_pursuer.py",
        "ZD01_encounters_battles_and_prisoners/anyone_slaver_world_caravan_companion_deshavi_pursuer.py",
    ):
        assert_contains(dialog_order, rel)

    for rel in (
        "src/menus/camp/free_slaves_confirm.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sod_slaver_buy_slaves_confirm.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_execute.py",
        "src/menus/centers/village/village_loot.py",
        "src/scripts/ZY_helper_scripts/sod_diplomacy_system.py",
        "src/scripts/ZC_parties/total_victory_finalize.py",
        "src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py",
        "src/menus/other/continue_05.py",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_02.py",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_army_caravan_start.py",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start.py",
        "src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py",
        "src/scripts/ZF_factions/diplomacy_start_war_between_kingdoms.py",
        "src/menus/centers/common/build_ladders_cont.py",
        "src/menus/centers/castle/build_siege_tower_cont.py",
        "src/scripts/ZY_helper_scripts/sod_population_based_construction.py",
        "src/menus/0000_hardcoded_mb1011/pay_day.py",
        "src/triggers/ST03_daily/entry_0054.py",
        "src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py",
        "src/menus/other/continue_35.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lady_qst_duel_for_lady_succeeded_2.py",
        "src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_02.py",
    ):
        raw = read(rel)
        if "script_sod_companion_dispatch_player_action" not in raw:
            assert_contains(raw, "script_sod_companion_apply_player_action")

    assert_contains(read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py"), "script_sod_black_khergits_apply_player_action")
    assert_contains(read("src/menus/camp/free_slaves_confirm.py"), "script_sod_companion_try_ymira_refugee_incident")
    assert_contains(read("src/menus/camp/free_slaves_confirm.py"), "script_sod_companion_try_ymira_refugee_expedience")
    assert_contains(read("src/menus/camp/free_slaves_confirm.py"), "script_sod_companion_ymira_apply_mercy_payoff")
    assert_contains(read("src/scripts/ZC_parties/total_victory_finalize.py"), "script_sod_companion_try_lezalit_ief_discipline_incident")
    assert_contains(read("src/menus/centers/village/village_bandits_defeated_accept.py"), "script_sod_companion_try_firentis_restitution_incident")
    assert_contains(read("src/triggers/ST03_daily/entry_0054.py"), "script_sod_companion_try_katrin_last_coin_incident")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/pay_day.py"), "script_sod_companion_try_katrin_last_coin_incident")
    assert_contains(read("src/triggers/ST03_daily/entry_0054.py"), "script_sod_companion_try_deshavi_trail_warning_incident")
    assert_contains(read("src/menus/camp/free_slaves_confirm.py"), "script_sod_companion_try_deshavi_trail_warning_incident")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py"), "script_sod_companion_try_klethi_old_job_incident")
    assert_contains(read("src/menus/camp/free_slaves_confirm.py"), "script_sod_companion_try_klethi_old_job_incident")
    assert_contains(read("src/menus/other/continue_35.py"), "script_sod_companion_try_rolf_name_challenge_incident")
    assert_contains(read("src/menus/centers/village/village_bandits_defeated_accept.py"), "script_sod_companion_try_alayen_standard_incident")
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_02.py"), "script_sod_companion_try_alayen_standard_incident")
    assert_contains(read("src/menus/other/continue_35.py"), "script_sod_companion_try_nizar_charge_incident")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py"), "script_sod_companion_try_baheshtur_saddle_incident")
    assert_contains(read("src/menus/other/continue_05.py"), "script_sod_companion_try_matheld_no_backward_step_incident")
    assert_contains(read("src/menus/centers/common/build_ladders_cont.py"), "script_sod_companion_try_artimenner_siege_incident")
    assert_contains(read("src/menus/centers/castle/build_siege_tower_cont.py"), "script_sod_companion_try_artimenner_siege_incident")
    assert_contains(scripts, "Mercy Under Arms has found its field test")
    assert_contains(scripts, "$g_sod_ymira_refugee_focus_center")
    assert_contains(scripts, "script_sod_companion_select_focus_village")
    assert_contains(scripts, "script_sod_get_center_security_profile")
    assert_contains(scripts, "slot_village_infested_by_bandits")
    assert_contains(scripts, "slot_faction_slaver_market_heat")
    assert_contains(scripts, "slot_faction_jotnar_target_center")
    assert_contains(scripts, "slot_faction_elephant_guard_target_center")
    assert_contains(scripts, "slot_faction_black_khergit_target_center")
    assert_contains(scripts, "Her warning waits at the campfire")
    assert_contains(scripts, "orderly refuge column")
    assert_contains(ymira_mercy_menu, "ymira_mercy_under_arms_protect")
    assert_contains(ymira_mercy_menu, "ymira_mercy_under_arms_ransom")
    assert_contains(ymira_mercy_menu, "ymira_mercy_under_arms_expedience")
    assert_contains(ymira_mercy_menu, "ymira_refugee_standoff")
    assert_contains(ymira_mercy_menu, "ymira_refugee_standoff_stand")
    assert_contains(ymira_mercy_menu, "ymira_refugee_standoff_pay")
    assert_contains(ymira_mercy_menu, "ymira_refugee_standoff_betray")
    assert_contains(ymira_mercy_menu, "mt_companion_ymira_refugee_defense")
    assert_contains(ymira_mercy_menu, "Mercy needs guards now")
    assert_contains(ymira_mercy_menu, "Mercy Under Arms remembers expedience")
    assert_contains(scripts, "Discipline Without Chains has found its field test")
    assert_contains(scripts, "$g_sod_lezalit_ief_discipline_pending")
    assert_contains(scripts, "captured Imperial drill into hard standards")
    assert_contains(scripts, "$g_sod_lezalit_ief_discipline_confronted")
    assert_contains(scripts, "$g_sod_lezalit_ief_discipline_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc14", sod_companion_campaign_mode_travel')
    assert_contains(lezalit_discipline_menu, "lezalit_discipline_reform")
    assert_contains(lezalit_discipline_menu, "lezalit_discipline_harsh")
    assert_contains(lezalit_discipline_menu, "lezalit_discipline_refuse")
    assert_contains(lezalit_discipline_menu, "lezalit_drill_trial")
    assert_contains(lezalit_discipline_menu, "mt_companion_lezalit_drill_trial")
    assert_contains(lezalit_discipline_menu, "$g_sod_lezalit_ief_discipline_confronted")
    assert_contains(lezalit_discipline_menu, "captured Imperial drill")
    assert_contains(lezalit_discipline_menu, "Lezalit breaks the captured Imperial drill")
    assert_contains(camp_action, "camp_lezalit_drill_trial")
    assert_contains(camp_action, "Run Lezalit's captured drill trial")
    assert_contains(mission_order, "0065_companion_lezalit_drill_trial/companion_lezalit_drill_trial.py")
    assert_contains(lezalit_drill_mission, '"companion_lezalit_drill_trial"')
    assert_contains(lezalit_drill_mission, "mnu_lezalit_drill_trial_succeeded")
    assert_contains(lezalit_drill_mission, "mnu_lezalit_drill_trial_failed")
    assert_contains(scripts, "$g_sod_bunduk_line_pending")
    assert_contains(scripts, "Bunduk counts the missing men")
    assert_contains(scripts, "orders the line can respect")
    assert_contains(scripts, "$g_sod_bunduk_line_confronted")
    assert_contains(scripts, "$g_sod_bunduk_line_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc10", sod_companion_campaign_mode_travel')
    assert_contains(bunduk_line_menu, "bunduk_line_advocate")
    assert_contains(bunduk_line_menu, "bunduk_line_compromise")
    assert_contains(bunduk_line_menu, "bunduk_line_crackdown")
    assert_contains(bunduk_line_menu, "bunduk_line_test")
    assert_contains(bunduk_line_menu, "mt_companion_bunduk_line_test")
    assert_contains(bunduk_line_menu, "$g_sod_bunduk_line_confronted")
    assert_contains(bunduk_line_menu, "The line gets better watches")
    assert_contains(camp_action, "camp_bunduk_line_test")
    assert_contains(camp_action, "Run Bunduk's watch-line test")
    assert_contains(mission_order, "0063_companion_bunduk_line_test/companion_bunduk_line_test.py")
    assert_contains(bunduk_line_mission, '"companion_bunduk_line_test"')
    assert_contains(bunduk_line_mission, "mnu_bunduk_line_test_succeeded")
    assert_contains(bunduk_line_mission, "mnu_bunduk_line_test_failed")
    assert_contains(scripts, "$g_sod_jeremus_triage_pending")
    assert_contains(scripts, "Jeremus runs out of clean cloth")
    assert_contains(scripts, "triage into calm order")
    assert_contains(scripts, "$g_sod_jeremus_triage_confronted")
    assert_contains(scripts, "$g_sod_jeremus_triage_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc12", sod_companion_campaign_mode_travel')
    assert_contains(jeremus_triage_menu, "jeremus_triage_mercy")
    assert_contains(jeremus_triage_menu, "jeremus_triage_hard")
    assert_contains(jeremus_triage_menu, "jeremus_triage_company")
    assert_contains(jeremus_triage_menu, "jeremus_triage_infirmary")
    assert_contains(jeremus_triage_menu, "mt_companion_jeremus_infirmary")
    assert_contains(jeremus_triage_menu, "$g_sod_jeremus_triage_confronted")
    assert_contains(jeremus_triage_menu, "too many wounded and too little time")
    assert_contains(camp_action, "camp_jeremus_infirmary_crisis")
    assert_contains(camp_action, "Face Jeremus' infirmary crisis")
    assert_contains(mission_order, "0064_companion_jeremus_infirmary/companion_jeremus_infirmary.py")
    assert_contains(jeremus_infirmary_mission, '"companion_jeremus_infirmary"')
    assert_contains(jeremus_infirmary_mission, "mnu_jeremus_infirmary_succeeded")
    assert_contains(jeremus_infirmary_mission, "mnu_jeremus_infirmary_failed")
    assert_contains(scripts, "$g_sod_firentis_restitution_pending")
    assert_contains(scripts, "Firentis sees the living cost of old violence")
    assert_contains(scripts, "penance into discipline")
    assert_contains(scripts, "$g_sod_firentis_restitution_confronted")
    assert_contains(scripts, "$g_sod_firentis_restitution_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc6", sod_companion_campaign_mode_travel')
    assert_contains(scripts, 'quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_target_center')
    assert_contains(firentis_restitution_menu, "firentis_restitution_protect")
    assert_contains(firentis_restitution_menu, "firentis_restitution_confess")
    assert_contains(firentis_restitution_menu, "firentis_restitution_silence")
    assert_contains(firentis_restitution_menu, "firentis_restitution_hearing")
    assert_contains(firentis_restitution_menu, "firentis_hearing_defend")
    assert_contains(firentis_restitution_menu, "firentis_hearing_confess")
    assert_contains(firentis_restitution_menu, "firentis_hearing_silence")
    assert_contains(firentis_restitution_menu, "mt_companion_firentis_restitution_defense")
    assert_contains(firentis_restitution_menu, "$g_sod_firentis_restitution_confronted")
    assert_contains(firentis_restitution_menu, "Debt of the Sword remembers restitution")
    assert_contains(read("src/menus/centers/village/recruit_volunteers.py"), "village_firentis_restitution_hearing")
    assert_contains(read("src/menus/centers/village/recruit_volunteers.py"), "Stand with Firentis at the restitution hearing")
    assert_contains(mission_order, "0059_companion_firentis_restitution_defense/companion_firentis_restitution_defense.py")
    assert_contains(firentis_restitution_mission, '"companion_firentis_restitution_defense"')
    assert_contains(firentis_restitution_mission, "mnu_firentis_restitution_defense_succeeded")
    assert_contains(firentis_restitution_mission, "mnu_firentis_restitution_defense_failed")
    assert_contains(scripts, "$g_sod_katrin_last_coin_pending")
    assert_contains(scripts, "Katrin finds empty food sacks")
    assert_contains(scripts, "lean stores into order")
    assert_contains(scripts, "$g_sod_katrin_last_coin_confronted")
    assert_contains(scripts, "$g_sod_katrin_last_coin_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc11", sod_companion_campaign_mode_travel')
    assert_contains(katrin_last_coin_menu, "katrin_last_coin_stores")
    assert_contains(katrin_last_coin_menu, "katrin_last_coin_ration")
    assert_contains(katrin_last_coin_menu, "katrin_last_coin_glory")
    assert_contains(katrin_last_coin_menu, "katrin_supply_watch")
    assert_contains(katrin_last_coin_menu, "mt_companion_katrin_supply_watch")
    assert_contains(katrin_last_coin_menu, "$g_sod_katrin_last_coin_confronted")
    assert_contains(katrin_last_coin_menu, "The Last Coin in Camp remembers practical care")
    assert_contains(camp_action, "camp_katrin_supply_watch")
    assert_contains(camp_action, "Run Katrin's supply watch")
    assert_contains(mission_order, "0071_companion_katrin_supply_watch/companion_katrin_supply_watch.py")
    assert_contains(katrin_supply_mission, '"companion_katrin_supply_watch"')
    assert_contains(katrin_supply_mission, "mnu_katrin_supply_watch_succeeded")
    assert_contains(katrin_supply_mission, "mnu_katrin_supply_watch_failed")
    assert_contains(scripts, "$g_sod_deshavi_trail_warning_pending")
    assert_contains(scripts, "Deshavi finds hunger signs")
    assert_contains(scripts, "false tracks")
    assert_contains(scripts, "$g_sod_deshavi_trail_confronted")
    assert_contains(scripts, "$g_sod_deshavi_trail_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc7", sod_companion_campaign_mode_travel')
    assert_contains(scripts, 'quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_target_center')
    assert_contains(deshavi_tracks_menu, "deshavi_tracks_shelter")
    assert_contains(deshavi_tracks_menu, "deshavi_tracks_ambush")
    assert_contains(deshavi_tracks_menu, "deshavi_tracks_hunt_only")
    assert_contains(deshavi_tracks_menu, "deshavi_tracks_trail_climax")
    assert_contains(deshavi_tracks_menu, "deshavi_trail_rescue")
    assert_contains(deshavi_tracks_menu, "deshavi_trail_reverse_ambush")
    assert_contains(deshavi_tracks_menu, "deshavi_trail_hunt_first")
    assert_contains(deshavi_tracks_menu, "mt_companion_deshavi_trail_rescue")
    assert_contains(deshavi_tracks_menu, "$g_sod_deshavi_trail_confronted")
    assert_contains(deshavi_tracks_menu, "Tracks Through Ash remembers shelter")
    assert_contains(scripts, "$g_sod_deshavi_trail_focus_center")
    assert_contains(read("src/menus/centers/village/recruit_volunteers.py"), "village_deshavi_follow_trail")
    assert_contains(read("src/menus/centers/village/recruit_volunteers.py"), "Follow Deshavi's trail beyond the village")
    assert_contains(mission_order, "0060_companion_deshavi_trail_rescue/companion_deshavi_trail_rescue.py")
    assert_contains(deshavi_trail_mission, '"companion_deshavi_trail_rescue"')
    assert_contains(deshavi_trail_mission, "mnu_deshavi_tracks_rescue_succeeded")
    assert_contains(deshavi_trail_mission, "mnu_deshavi_tracks_rescue_failed")
    assert_contains(scripts, "$g_sod_borcha_road_pending")
    assert_contains(scripts, "$g_sod_borcha_road_origin_center")
    assert_contains(scripts, "$g_sod_borcha_road_destination_center")
    assert_contains(scripts, "$g_sod_borcha_road_witnessed")
    assert_contains(scripts, "$g_sod_borcha_road_confronted")
    assert_contains(scripts, "$g_sod_borcha_road_result_grade")
    assert_contains(scripts, '"sod_companion_start_borcha_road_incident"')
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc1", sod_companion_campaign_mode_travel')
    assert_contains(scripts, 'quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_target_center')
    assert_contains(borcha_road_menu, "borcha_road_counter_ambush")
    assert_contains(borcha_road_menu, "borcha_counter_ambush_fight")
    assert_contains(borcha_road_menu, "borcha_counter_ambush_bypass")
    assert_contains(borcha_road_menu, "borcha_counter_ambush_sell_route")
    assert_contains(borcha_road_menu, "mt_companion_borcha_counter_ambush")
    assert_contains(borcha_road_menu, "The hidden route is marked")
    assert_contains(town_menu, "town_borcha_counter_ambush")
    assert_contains(town_menu, "Ride Borcha's side road before the ambush closes")
    assert_contains(town_menu, '"script_cf_sod_companion_campaign_available", "trp_npc1", sod_companion_campaign_mode_scene')
    assert_contains(mission_order, "0061_companion_borcha_counter_ambush/companion_borcha_counter_ambush.py")
    assert_contains(borcha_road_mission, '"companion_borcha_counter_ambush"')
    assert_contains(borcha_road_mission, "mnu_borcha_road_ambush_succeeded")
    assert_contains(borcha_road_mission, "mnu_borcha_road_ambush_failed")
    assert_contains(scripts, "$g_sod_marnid_market_pending")
    assert_contains(scripts, "$g_sod_marnid_market_focus_center")
    assert_contains(scripts, "$g_sod_marnid_market_evidence")
    assert_contains(scripts, "$g_sod_marnid_market_confronted")
    assert_contains(scripts, "$g_sod_marnid_market_result_grade")
    assert_contains(scripts, '"sod_companion_start_marnid_market_incident"')
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc2", sod_companion_campaign_mode_travel')
    assert_contains(scripts, 'quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_target_center')
    assert_contains(marnid_price_menu, "marnid_price_warehouse")
    assert_contains(marnid_price_menu, "marnid_warehouse_force")
    assert_contains(marnid_price_menu, "marnid_warehouse_audit")
    assert_contains(marnid_price_menu, "marnid_warehouse_blackmail")
    assert_contains(marnid_price_menu, "mt_companion_marnid_warehouse")
    assert_contains(marnid_price_menu, "profit that does not need hiding")
    assert_contains(town_menu, "town_marnid_warehouse")
    assert_contains(town_menu, "Inspect Marnid's suspect warehouse")
    assert_contains(town_menu, '"script_cf_sod_companion_campaign_available", "trp_npc2", sod_companion_campaign_mode_scene')
    assert_contains(mission_order, "0062_companion_marnid_warehouse/companion_marnid_warehouse.py")
    assert_contains(marnid_warehouse_mission, '"companion_marnid_warehouse"')
    assert_contains(marnid_warehouse_mission, "mnu_marnid_warehouse_succeeded")
    assert_contains(marnid_warehouse_mission, "mnu_marnid_warehouse_failed")
    assert_contains(scripts, "$g_sod_klethi_old_job_pending")
    assert_contains(scripts, "$g_sod_klethi_old_job_focus_center")
    assert_contains(scripts, "$g_sod_klethi_old_job_clue_bits")
    assert_contains(scripts, "$g_sod_klethi_old_job_result_grade")
    assert_contains(scripts, "$g_sod_klethi_old_job_confronted")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc16", sod_companion_campaign_mode_travel')
    assert_contains(scripts, 'quest_set_slot, "qst_companion_klethi_knife_with_name", slot_quest_target_center')
    assert_contains(scripts, "Klethi recognizes an old route")
    assert_contains(scripts, "old job into new doors")
    assert_contains(klethi_knife_menu, "klethi_knife_choose")
    assert_contains(klethi_knife_menu, "klethi_knife_protect")
    assert_contains(klethi_knife_menu, "klethi_knife_sellout")
    assert_contains(klethi_knife_menu, "klethi_knife_find_witness")
    assert_contains(klethi_knife_menu, "klethi_knife_follow_mark")
    assert_contains(klethi_knife_menu, "klethi_knife_alley_confront")
    assert_contains(klethi_knife_menu, "mt_companion_klethi_alley")
    assert_contains(klethi_knife_menu, "$g_sod_klethi_old_job_confronted")
    assert_contains(klethi_knife_menu, '(assign, "$g_sod_klethi_old_job_contacted", 0)')
    assert_contains(klethi_knife_menu, '(call_script, "script_get_closest_town", "p_main_party")')
    assert_contains(klethi_knife_menu, '(eq, "$current_town", "$g_sod_klethi_old_job_focus_center")')
    assert_contains(town_menu, "town_klethi_follow_old_mark")
    assert_contains(town_menu, "Follow Klethi's old mark into the alley")
    assert_contains(town_menu, "$g_sod_klethi_old_job_focus_center")
    assert_contains(town_menu, '"script_cf_sod_companion_campaign_available", "trp_npc16", sod_companion_campaign_mode_scene')
    assert_contains(mission_order, "0057_companion_klethi_alley/companion_klethi_alley.py")
    assert_contains(klethi_alley_mission, '"companion_klethi_alley"')
    assert_contains(klethi_alley_mission, "mnu_klethi_knife_alley_succeeded")
    assert_contains(klethi_alley_mission, "mnu_klethi_knife_alley_failed")
    assert_contains(klethi_knife_menu, "A Knife With a Name remembers chosen belonging")
    assert_contains(scripts, "$g_sod_ymira_refugee_captive_count")
    assert_contains(scripts, "$g_sod_ymira_refugee_confronted")
    assert_contains(scripts, "$g_sod_ymira_refugee_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc3", sod_companion_campaign_mode_travel')
    assert_contains(scripts, 'quest_set_slot, "qst_companion_ymira_mercy_under_arms", slot_quest_target_center')
    assert_contains(read("src/menus/centers/village/recruit_volunteers.py"), "village_ymira_refugee_standoff")
    assert_contains(read("src/menus/centers/village/recruit_volunteers.py"), "Stand watch with Ymira's refugees")
    assert_contains(mission_order, "0058_companion_ymira_refugee_defense/companion_ymira_refugee_defense.py")
    assert_contains(ymira_refugee_mission, '"companion_ymira_refugee_defense"')
    assert_contains(ymira_refugee_mission, "mnu_ymira_refugee_defense_succeeded")
    assert_contains(ymira_refugee_mission, "mnu_ymira_refugee_defense_failed")
    assert_contains(scripts, "$g_sod_rolf_name_challenge_pending")
    assert_contains(scripts, "Rolf hears his name cheered")
    assert_contains(scripts, "public dignity into useful ceremony")
    assert_contains(scripts, "$g_sod_rolf_name_challenge_focus_center")
    assert_contains(scripts, "$g_sod_rolf_name_challenge_confronted")
    assert_contains(scripts, "$g_sod_rolf_name_challenge_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc4", sod_companion_campaign_mode_travel')
    assert_contains(rolf_name_menu, "rolf_name_earn")
    assert_contains(rolf_name_menu, "rolf_name_defend")
    assert_contains(rolf_name_menu, "rolf_name_expose")
    assert_contains(rolf_name_menu, "rolf_public_proof")
    assert_contains(rolf_name_menu, "mt_companion_rolf_public_proof")
    assert_contains(rolf_name_menu, "$g_sod_rolf_name_challenge_confronted")
    assert_contains(rolf_name_menu, "A Name Worth Wearing remembers earned dignity")
    assert_contains(camp_action, "camp_rolf_public_proof")
    assert_contains(camp_action, "Stage Rolf's public proof")
    assert_contains(mission_order, "0068_companion_rolf_public_proof/companion_rolf_public_proof.py")
    assert_contains(rolf_public_mission, '"companion_rolf_public_proof"')
    assert_contains(rolf_public_mission, "mnu_rolf_public_proof_succeeded")
    assert_contains(rolf_public_mission, "mnu_rolf_public_proof_failed")
    assert_contains(scripts, "$g_sod_alayen_standard_pending")
    assert_contains(scripts, "Alayen sees the standard raised")
    assert_contains(scripts, "standard into obligation")
    assert_contains(scripts, "$g_sod_alayen_standard_focus_center")
    assert_contains(scripts, "$g_sod_alayen_standard_confronted")
    assert_contains(scripts, "$g_sod_alayen_standard_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc9", sod_companion_campaign_mode_travel')
    assert_contains(alayen_standard_menu, "alayen_standard_duty")
    assert_contains(alayen_standard_menu, "alayen_standard_oath")
    assert_contains(alayen_standard_menu, "alayen_standard_pride")
    assert_contains(alayen_standard_menu, "alayen_standard_test")
    assert_contains(alayen_standard_menu, "mt_companion_alayen_standard_test")
    assert_contains(alayen_standard_menu, "$g_sod_alayen_standard_confronted")
    assert_contains(alayen_standard_menu, "The Standard and the Self remembers duty")
    assert_contains(camp_action, "camp_alayen_standard_test")
    assert_contains(camp_action, "Stand Alayen's public standard test")
    assert_contains(mission_order, "0067_companion_alayen_standard_test/companion_alayen_standard_test.py")
    assert_contains(alayen_standard_mission, '"companion_alayen_standard_test"')
    assert_contains(alayen_standard_mission, "mnu_alayen_standard_test_succeeded")
    assert_contains(alayen_standard_mission, "mnu_alayen_standard_test_failed")
    assert_contains(scripts, "$g_sod_nizar_charge_pending")
    assert_contains(scripts, "Nizar hears the crowd")
    assert_contains(scripts, "daring into pursuit discipline")
    assert_contains(scripts, "$g_sod_nizar_charge_confronted")
    assert_contains(scripts, "$g_sod_nizar_charge_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc13", sod_companion_campaign_mode_travel')
    assert_contains(nizar_charge_menu, "nizar_charge_responsible")
    assert_contains(nizar_charge_menu, "nizar_charge_daring")
    assert_contains(nizar_charge_menu, "nizar_charge_blood_legend")
    assert_contains(nizar_charge_menu, "nizar_charge_lane_test")
    assert_contains(nizar_charge_menu, "mt_companion_nizar_charge_lane")
    assert_contains(nizar_charge_menu, "$g_sod_nizar_charge_confronted")
    assert_contains(nizar_charge_menu, "The Impossible Charge remembers glory with survivors")
    assert_contains(camp_action, "camp_nizar_charge_lane_test")
    assert_contains(camp_action, "Run Nizar's charge-lane test")
    assert_contains(mission_order, "0072_companion_nizar_charge_lane/companion_nizar_charge_lane.py")
    assert_contains(nizar_lane_mission, '"companion_nizar_charge_lane"')
    assert_contains(nizar_lane_mission, "mnu_nizar_charge_lane_succeeded")
    assert_contains(nizar_lane_mission, "mnu_nizar_charge_lane_failed")
    assert_contains(scripts, "$g_sod_baheshtur_saddle_pending")
    assert_contains(scripts, "Baheshtur sees broken horde riders")
    assert_contains(scripts, "broken pursuit into chosen riders")
    assert_contains(scripts, "$g_sod_baheshtur_saddle_focus_party")
    assert_contains(scripts, "$g_sod_baheshtur_saddle_confronted")
    assert_contains(scripts, "$g_sod_baheshtur_saddle_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc5", sod_companion_campaign_mode_travel')
    assert_contains(baheshtur_saddle_menu, "baheshtur_saddle_free")
    assert_contains(baheshtur_saddle_menu, "baheshtur_saddle_pursuit")
    assert_contains(baheshtur_saddle_menu, "baheshtur_saddle_submission")
    assert_contains(baheshtur_saddle_menu, "baheshtur_rider_oath_trial")
    assert_contains(baheshtur_saddle_menu, "mt_companion_baheshtur_rider_oath")
    assert_contains(baheshtur_saddle_menu, "$g_sod_baheshtur_saddle_confronted")
    assert_contains(baheshtur_saddle_menu, "The Unbroken Saddle remembers chosen loyalty")
    assert_contains(camp_action, "camp_baheshtur_rider_oath_trial")
    assert_contains(camp_action, "Run Baheshtur's rider-oath trial")
    assert_contains(mission_order, "0069_companion_baheshtur_rider_oath/companion_baheshtur_rider_oath.py")
    assert_contains(baheshtur_oath_mission, '"companion_baheshtur_rider_oath"')
    assert_contains(baheshtur_oath_mission, "mnu_baheshtur_rider_oath_succeeded")
    assert_contains(baheshtur_oath_mission, "mnu_baheshtur_rider_oath_failed")
    assert_contains(scripts, "$g_sod_matheld_no_backward_step_pending")
    assert_contains(scripts, "Matheld counts the dead")
    assert_contains(scripts, "courage into a shield wall")
    assert_contains(scripts, "$g_sod_matheld_no_backward_step_focus_party")
    assert_contains(scripts, "$g_sod_matheld_no_backward_step_confronted")
    assert_contains(scripts, "$g_sod_matheld_no_backward_step_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc8", sod_companion_campaign_mode_travel')
    assert_contains(matheld_step_menu, "matheld_step_temper")
    assert_contains(matheld_step_menu, "matheld_step_stand")
    assert_contains(matheld_step_menu, "matheld_step_blood_price")
    assert_contains(matheld_step_menu, "matheld_shield_line_test")
    assert_contains(matheld_step_menu, "mt_companion_matheld_shield_line")
    assert_contains(matheld_step_menu, "$g_sod_matheld_no_backward_step_confronted")
    assert_contains(matheld_step_menu, "No Backward Step remembers courage with teeth")
    assert_contains(camp_action, "camp_matheld_shield_line_test")
    assert_contains(camp_action, "Run Matheld's shield-line test")
    assert_contains(mission_order, "0070_companion_matheld_shield_line/companion_matheld_shield_line.py")
    assert_contains(matheld_line_mission, '"companion_matheld_shield_line"')
    assert_contains(matheld_line_mission, "mnu_matheld_shield_line_succeeded")
    assert_contains(matheld_line_mission, "mnu_matheld_shield_line_failed")
    assert_contains(scripts, "$g_sod_artimenner_siege_pending")
    assert_contains(scripts, "Artimenner studies the siege tower plans")
    assert_contains(scripts, "respected design")
    assert_contains(scripts, "$g_sod_artimenner_siege_focus_center")
    assert_contains(scripts, "$g_sod_artimenner_siege_confronted")
    assert_contains(scripts, "$g_sod_artimenner_siege_result_grade")
    assert_contains(scripts, '"script_cf_sod_companion_campaign_available", "trp_npc15", sod_companion_campaign_mode_travel')
    assert_contains(artimenner_siege_menu, "artimenner_siege_rebuild")
    assert_contains(artimenner_siege_menu, "artimenner_siege_improvise")
    assert_contains(artimenner_siege_menu, "artimenner_siege_blame")
    assert_contains(artimenner_siege_menu, "artimenner_repair_watch")
    assert_contains(artimenner_siege_menu, "mt_companion_artimenner_repair_watch")
    assert_contains(artimenner_siege_menu, "$g_sod_artimenner_siege_confronted")
    assert_contains(artimenner_siege_menu, "The Siege That Should Have Worked remembers respected design")
    assert_contains(camp_action, "camp_artimenner_repair_watch")
    assert_contains(camp_action, "Guard Artimenner's repair watch")
    assert_contains(mission_order, "0066_companion_artimenner_repair_watch/companion_artimenner_repair_watch.py")
    assert_contains(artimenner_repair_mission, '"companion_artimenner_repair_watch"')
    assert_contains(artimenner_repair_mission, "mnu_artimenner_repair_watch_succeeded")
    assert_contains(artimenner_repair_mission, "mnu_artimenner_repair_watch_failed")
    ymira_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_ymira.py")
    lezalit_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_lezalit.py")
    bunduk_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_bunduk.py")
    jeremus_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_jeremus.py")
    firentis_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_firentis.py")
    katrin_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_katrin.py")
    borcha_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_borcha.py")
    deshavi_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_deshavi.py")
    klethi_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_klethi.py")
    rolf_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_rolf.py")
    alayen_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_alayen.py")
    nizar_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_nizar.py")
    baheshtur_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_baheshtur.py")
    matheld_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_matheld.py")
    artimenner_dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_artimenner.py")
    assert_contains(ymira_dialog, "keeping a bowl steady while a man died")
    assert_contains(ymira_dialog, "Necessary should leave a mark")
    assert_contains(ymira_dialog, "put guards around mercy")
    assert_contains(lezalit_dialog, "The captured Imperial drill is waiting")
    assert_contains(lezalit_dialog, "They no longer need chains")
    assert_contains(lezalit_dialog, "Do not confuse that with loyalty")
    assert_contains(bunduk_dialog, "The men are listening for your answer")
    assert_contains(bunduk_dialog, "instead of ammunition")
    assert_contains(bunduk_dialog, "being led and being used")
    assert_contains(jeremus_dialog, "too many wounded and too little time")
    assert_contains(jeremus_dialog, "rank or usefulness")
    assert_contains(jeremus_dialog, "left waiting were only numbers")
    assert_contains(firentis_dialog, "Restitution did not raise the dead")
    assert_contains(firentis_dialog, "village is saved")
    assert_contains(firentis_dialog, "changed hands or merely changed banners")
    assert_contains(borcha_dialog, "Road says")
    assert_contains(borcha_dialog, "road witness")
    assert_contains(borcha_dialog, "ambush show its teeth")
    for rel, tokens in (
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_companion_ymira_refugees.py",
            ("Ymira says some captives may find shelter here", "$g_sod_ymira_refugee_focus_center", "$current_town"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_goods_merchant_companion_marnid_market.py",
            ("Marnid wants a merchant's plain account", "$g_sod_marnid_market_contacted", "$g_sod_marnid_market_focus_center", "script_cf_sod_companion_campaign_available", "script_sod_trade_network_describe_center_identity_to_s23"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_companion_marnid_market.py",
            ("warehouse lead", "$g_sod_marnid_market_contacted", "$g_sod_marnid_market_evidence", "market contact", "script_sod_companion_apply_player_action", "script_sod_companion_shift_core_value_proof", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_ymira_refugees.py",
            ("village_elder_companion_ymira_refugees_choice", "Slaver riders ask questions with ropes", "mnu_ymira_refugee_standoff", "script_sod_player_charge_gold", "$g_sod_ymira_refugee_witnessed"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_companion_deshavi_tracks.py",
            ("Deshavi followed signs here", "$g_sod_deshavi_trail_focus_center", "$current_town", "script_cf_sod_companion_campaign_available", "$g_sod_deshavi_trail_confronted"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_deshavi_tracks.py",
            ("g_sod_deshavi_trail_witnessed", "Tracks Through Ash now has witnesses", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_companion_firentis_restitution.py",
            ("village_elder_companion_firentis_restitution", "$g_sod_firentis_restitution_focus_center", "What would restitution mean here"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_firentis_restitution.py",
            ("$g_sod_firentis_restitution_witnessed", "living witness", "village_elder_companion_firentis_restitution_choice", "Leave guards, coin, and supplies", "mnu_firentis_restitution_hearing", "$g_sod_firentis_restitution_confronted"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_companion_alayen_standard.py",
            ("village_elder_companion_alayen_standard", "$g_sod_alayen_standard_pending", "standard was raised over people needing protection"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_alayen_standard.py",
            ("armed cloth", "$g_sod_alayen_standard_witnessed", "protected-people witness", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_dweller_companion_ymira_refugee.py",
            ("town_dweller_companion_ymira_refugee", "$g_sod_ymira_refugee_focus_center", "There are freed captives outside", "trp_slave_female"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_companion_ymira_refugee.py",
            ("one bowl", "$g_sod_ymira_refugee_witnessed", "human witness", "script_sod_companion_apply_player_action"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_ymira_captive.py",
            ("regular_member_companion_ymira_captive", "$g_sod_ymira_refugee_witnessed", "Bring me one of the captives", "trp_slave_female"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_ymira_captive.py",
            ("chains teach a person", "$g_sod_ymira_refugee_witnessed", "direct witness", "script_sod_companion_apply_player_action"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_dweller_companion_deshavi_survivor.py",
            ("town_dweller_companion_deshavi_survivor", "$g_sod_deshavi_trail_focus_center", "Deshavi found signs near here", "script_cf_sod_companion_campaign_available"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_companion_deshavi_survivor.py",
            ("Your tracker looked", "$g_sod_deshavi_trail_witnessed", "living witness", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_dweller_companion_rolf_name.py",
            ("town_dweller_companion_rolf_name", "$g_sod_rolf_name_challenge_pending", "Rolf's name in the street"),
        ),
        (
            "src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_companion_rolf_name.py",
            ("tall tale warms a tavern", "$g_sod_rolf_name_challenge_witnessed", "public matter", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_slaver_world_caravan_companion_deshavi_pursuer.py",
            ("slaver_world_caravan_companion_deshavi_pursuer", "$g_sod_deshavi_trail_warning_cause", "Were those yours", "script_cf_sod_companion_campaign_available"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_slaver_world_caravan_companion_deshavi_pursuer.py",
            ("A good hunter knows", "$g_sod_deshavi_trail_witnessed", "hunter witness", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_companion_klethi_contact.py",
            ("tavernkeeper_companion_klethi_contact", "$g_sod_klethi_old_job_pending", "$g_sod_klethi_old_job_focus_center", "$current_town", "Who has been asking after Klethi"),
        ),
        (
            "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_companion_klethi_contact.py",
            ("$g_sod_klethi_old_job_contacted", "$g_sod_klethi_old_job_clue_bits", "underworld witness", "script_sod_companion_apply_player_action"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_lezalit_drill.py",
            ("regular_member_companion_lezalit_drill", "$g_sod_lezalit_ief_discipline_pending", "captured Imperial drill notes"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_lezalit_drill.py",
            ("$g_sod_lezalit_ief_discipline_witnessed", "troop witness", "regular_member_companion_lezalit_drill_choice", "drill trial", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_bunduk_line.py",
            ("regular_member_companion_bunduk_line", "$g_sod_bunduk_line_pending", "Speak plainly"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_bunduk_line.py",
            ("$g_sod_bunduk_line_witnessed", "company witness", "regular_member_companion_bunduk_line_choice", "test the line", "The line obeys first", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_jeremus_wounded.py",
            ("regular_member_companion_jeremus_wounded", "$g_sod_jeremus_triage_pending", "What have you seen"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_jeremus_wounded.py",
            ("$g_sod_jeremus_triage_witnessed", "company witness", "regular_member_companion_jeremus_wounded_choice", "infirmary", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_matheld_line.py",
            ("regular_member_companion_matheld_line", "$g_sod_matheld_no_backward_step_pending", "What did you see"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_matheld_line.py",
            ("Matheld is right to ask", "$g_sod_matheld_no_backward_step_witnessed", "post-battle witness", "shield-line test", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_companion_katrin_ledger.py",
            ("regular_member_companion_katrin_ledger", "$g_sod_katrin_last_coin_pending", "What are people saying"),
        ),
        (
            "src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_katrin_ledger.py",
            ("$g_sod_katrin_last_coin_witnessed", "camp ledger witness", "supply watch", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_companion_nizar_charge.py",
            ("battle_reason_companion_nizar_charge", "$g_sod_nizar_charge_pending", "mark the charge"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_battle_reason_companion_nizar_charge.py",
            ("dust to blind them", "$g_sod_nizar_charge_witnessed", "field setup", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_companion_alayen_standard.py",
            ("lord_companion_alayen_standard", "$g_sod_alayen_standard_pending", "What does it promise"),
        ),
        (
            "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_companion_alayen_standard.py",
            ("Cloth becomes honor", "$g_sod_alayen_standard_witnessed", "public witness", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_companion_baheshtur_rider.py",
            ("black_khergit_companion_baheshtur_rider", "$g_sod_baheshtur_saddle_pending", "beaten riders still choose"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_guard_companion_baheshtur_rider.py",
            ("black_khergit_companion_baheshtur_rider", "$g_sod_baheshtur_saddle_pending", "beaten riders still choose"),
        ),
        (
            "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_companion_baheshtur_rider.py",
            ("$g_sod_baheshtur_saddle_witnessed", "living witness", "script_sod_companion_apply_player_action", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_companion_borcha_road.py",
            ("Borcha says the side road", "$g_sod_borcha_road_origin_center", "script_cf_sod_companion_campaign_available"),
        ),
        (
            "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_companion_borcha_road.py",
            ("Your road man has the eye", "$g_sod_borcha_road_witnessed", "road witness", "script_sod_companion_sync_personal_quest_framework"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_borcha.py",
            ("show me the road", "companion_depth_borcha_road_pending", "script_sod_companion_start_borcha_road_incident"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_borcha.py",
            ("companion_depth_borcha_road_choice", "$g_sod_borcha_road_witnessed", "$g_sod_borcha_road_confronted", "Ask in", "ambush show its teeth", "Mark it safe", "counter-ambush", "Use the route for profit"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_marnid.py",
            ("suspect contract", "companion_depth_marnid_price_pending", "script_sod_companion_start_marnid_market_incident"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_marnid.py",
            ("companion_depth_marnid_price_choice", "$g_sod_marnid_market_evidence", "$g_sod_marnid_market_confronted", "goods merchant", "warehouse", "Expose the contract", "Repay the losses", "Use the evidence for leverage"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_ymira.py",
            ("speak for the captives", "companion_depth_ymira_captive_pending", "script_sod_companion_select_focus_village"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_ymira.py",
            ("companion_depth_ymira_captive_choice", "$g_sod_ymira_refugee_focus_center", "$g_sod_ymira_refugee_witnessed", "mercy has witnesses", "shelter means reaching", "We are close enough", "Guard, feed, and release them", "Ransom the able-bodied", "Keep them chained"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_lezalit.py",
            ("captured Imperial drill", "companion_depth_lezalit_drill_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_lezalit.py",
            ("companion_depth_lezalit_drill_choice", "$g_sod_lezalit_ief_discipline_witnessed", "$g_sod_lezalit_ief_discipline_confronted", "captured drill trial", "Reform the Imperial drill", "Use fear", "Refuse the lesson"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_bunduk.py",
            ("line's grievance", "companion_depth_bunduk_line_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_bunduk.py",
            ("companion_depth_bunduk_line_choice", "$g_sod_bunduk_line_witnessed", "$g_sod_bunduk_line_confronted", "test the watch line", "I back you", "Make a practical compromise", "Enforce command authority"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_jeremus.py",
            ("take me to the wounded", "companion_depth_jeremus_triage_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_jeremus.py",
            ("companion_depth_jeremus_triage_choice", "$g_sod_jeremus_triage_witnessed", "$g_sod_jeremus_triage_confronted", "infirmary crisis", "Treat the helpless", "Use hard triage", "Save company strength first"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_firentis.py",
            ("restitution still asks", "companion_depth_firentis_restitution_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_firentis.py",
            ("companion_depth_firentis_restitution_choice", "$g_sod_firentis_restitution_focus_center", "$g_sod_firentis_restitution_witnessed", "$g_sod_firentis_restitution_confronted", "hearing tested us", "Leave guards, coin, and supplies", "Let truth be spoken", "Say nothing more"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_katrin.py",
            ("put the ledger in my hands", "companion_depth_katrin_coin_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_katrin.py",
            ("companion_depth_katrin_coin_choice", "$g_sod_katrin_last_coin_witnessed", "$g_sod_katrin_last_coin_confronted", "supply watch", "food, medicine, and honest arrears", "Stretch the stores", "Spend for momentum"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_deshavi.py",
            ("show me the trail", "companion_depth_deshavi_tracks_pending", "script_sod_companion_select_focus_village", "script_cf_sod_companion_campaign_available"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_deshavi.py",
            ("companion_depth_deshavi_tracks_choice", "$g_sod_deshavi_trail_focus_center", "$g_sod_deshavi_trail_witnessed", "$g_sod_deshavi_trail_confronted", "follow me beyond the village", "trail bends toward", "Ask the living first", "shelter the vulnerable", "set an ambush", "Hunt the pursuers"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_klethi.py",
            ("old work found your knife", "companion_depth_klethi_knife_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_klethi.py",
            ("companion_depth_klethi_knife_choice", "$g_sod_klethi_old_job_contacted", "$g_sod_klethi_old_job_confronted", "witness outside my own mouth", "nearest useful witness", "Handle it on your own terms", "protect you", "Use the old secret"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_rolf.py",
            ("answer the question about your name", "companion_depth_rolf_name_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_rolf.py",
            ("companion_depth_rolf_name_choice", "$g_sod_rolf_name_challenge_witnessed", "$g_sod_rolf_name_challenge_confronted", "public proof", "Answer with service", "defend your dignity", "Strip away the performance"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_alayen.py",
            ("standard is asking", "companion_depth_alayen_standard_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_alayen.py",
            ("companion_depth_alayen_standard_choice", "$g_sod_alayen_standard_witnessed", "$g_sod_alayen_standard_confronted", "public standard test", "promise to protect", "Keep the oath publicly", "obedience and prestige"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_nizar.py",
            ("impossible charge before it becomes a song", "companion_depth_nizar_charge_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_nizar.py",
            ("companion_depth_nizar_charge_choice", "$g_sod_nizar_charge_witnessed", "$g_sod_nizar_charge_confronted", "charge lane", "planning the way out", "dazzling charge", "Spend blood for a legend"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_baheshtur.py",
            ("speak for the beaten riders", "companion_depth_baheshtur_saddle_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_baheshtur.py",
            ("companion_depth_baheshtur_saddle_choice", "$g_sod_baheshtur_saddle_witnessed", "$g_sod_baheshtur_saddle_confronted", "rider oath trial", "You heard him", "swear freely", "surrender unchained", "Force submission"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_matheld.py",
            ("what the line learned", "companion_depth_matheld_step_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_matheld.py",
            ("companion_depth_matheld_step_choice", "$g_sod_matheld_no_backward_step_witnessed", "$g_sod_matheld_no_backward_step_confronted", "shield-line test", "Temper courage", "Stand firm", "Make every insult cost blood"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_artimenner.py",
            ("weak point before it kills anyone", "companion_depth_artimenner_siege_pending"),
        ),
        (
            "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_artimenner.py",
            ("companion_depth_artimenner_siege_choice", "$g_sod_artimenner_siege_witnessed", "$g_sod_artimenner_siege_confronted", "repair watch", "rebuild the works properly", "Improvise a leaner plan", "answer for it if the works fail"),
        ),
    ):
        raw = read(rel)
        for token in tokens:
            assert_contains(raw, token)

    assert_contains(read("src/menus/centers/common/build_ladders_cont.py"), "build_ladders_artimenner_inspect")
    assert_contains(read("src/menus/centers/common/build_ladders_cont.py"), "$g_sod_artimenner_siege_witnessed")
    assert_contains(read("src/menus/centers/common/build_ladders_cont.py"), "script_sod_companion_sync_personal_quest_framework")
    assert_contains(read("src/menus/centers/castle/build_siege_tower_cont.py"), "build_siege_tower_artimenner_inspect")
    assert_contains(read("src/menus/centers/castle/build_siege_tower_cont.py"), "$g_sod_artimenner_siege_witnessed")
    assert_contains(read("src/menus/centers/castle/build_siege_tower_cont.py"), "script_sod_companion_sync_personal_quest_framework")
    for guarded_dialog, focus_global in (
        (ymira_dialog, "$g_sod_ymira_refugee_focus_center"),
        (deshavi_dialog, "$g_sod_deshavi_trail_focus_center"),
        (read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_firentis.py"), "$g_sod_firentis_restitution_focus_center"),
        (read("src/dialogs/ZZ99_misc_dialogs/anyone_regular_member_companion_ymira_captive.py"), "$g_sod_ymira_refugee_focus_center"),
        (read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_slaver_world_caravan_companion_deshavi_pursuer.py"), "$g_sod_deshavi_trail_focus_center"),
    ):
        assert_contains(guarded_dialog, f'(party_is_active, "{focus_global}")')
    for current_town_dialog in (
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_ymira_refugees.py",
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_companion_deshavi_tracks.py",
    ):
        assert_contains(read(current_town_dialog), '(party_is_active, "$current_town")')

    assert_contains(katrin_dialog, "coins, bread, and promises")
    assert_contains(katrin_dialog, "cooking pot")
    assert_contains(katrin_dialog, "patched the consequences")
    assert_contains(deshavi_dialog, "trail outside camp")
    assert_contains(deshavi_dialog, "before they disappear")
    assert_contains(deshavi_dialog, "Dead hunters cannot chase anyone")
    assert_contains(klethi_dialog, "Old work found my knife")
    assert_contains(klethi_dialog, "opened door means")
    assert_contains(klethi_dialog, "secret bought what you wanted")
    assert_contains(rolf_dialog, "applause and questions")
    assert_contains(rolf_dialog, "name can also be made heavier")
    assert_contains(rolf_dialog, "bruised banner")
    assert_contains(alayen_dialog, "duty or display")
    assert_contains(alayen_dialog, "who is the banner for")
    assert_contains(alayen_dialog, "different victories")
    assert_contains(nizar_dialog, "beautiful enough to be dangerous")
    assert_contains(nizar_dialog, "question with spurs")
    assert_contains(nizar_dialog, "applause can echo")
    assert_contains(baheshtur_dialog, "forced oath is a rope")
    assert_contains(baheshtur_dialog, "living witness")
    assert_contains(baheshtur_dialog, "rider oath trial")
    assert_contains(baheshtur_dialog, "open ground is not freedom")
    assert_contains(matheld_dialog, "Blood-price is easy")
    assert_contains(matheld_dialog, "line learned something")
    assert_contains(matheld_dialog, "shield wall must breathe")
    assert_contains(artimenner_dialog, "weak point in the works")
    assert_contains(artimenner_dialog, "Ignored tolerances")
    assert_contains(artimenner_dialog, "facts be inconvenient")
    assert_contains(companion_bible, "Ymira knows mercy needs guards")
    assert_contains(companion_bible, "water, bandages, names, routes, and morale")
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_02.py"), "sod_companion_action_caravan_protection")
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_02.py"), "sod_companion_action_trade_profit")
    assert_contains(read("src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py"), "sod_companion_action_honorable_peace")
    assert_contains(read("src/scripts/ZF_factions/diplomacy_start_war_between_kingdoms.py"), "sod_companion_action_diplomacy_betrayal")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py"), "sod_companion_action_build_healing")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py"), "sod_companion_action_build_market")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py"), "sod_companion_action_scout_warning")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py"), "sod_companion_action_build_security")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py"), "sod_companion_action_efficient_construction")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/pay_day.py"), "sod_companion_action_unpaid_wages")
    assert_contains(read("src/triggers/ST03_daily/entry_0054.py"), "sod_companion_action_hunger")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py"), "sod_companion_action_black_khergit_camp_defeat")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py"), "Borcha finds a hidden road")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py"), "sod_companion_role_scout")
    assert_contains(read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py"), "sod_companion_role_quartermaster")
    assert_contains(read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py"), "sod_companion_quest_resolved_good")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py"), "sod_companion_action_black_army_security")
    assert_contains(read("src/menus/other/continue_35.py"), "sod_companion_action_tournament_glory")
    assert_contains(read("src/dialogs/ZB01_lords_politics_and_family/anyone_lady_qst_duel_for_lady_succeeded_2.py"), "sod_companion_action_tournament_glory")
    quest_journal = read("src/scripts/ZG_quests/sod_quest_journal_describe_to_s2.py")
    for journal_token in (
        "@Talk to Borcha:",
        "@Talk to Marnid:",
        "@Talk to Ymira:",
        "@Talk to Rolf:",
        "@Talk to Baheshtur:",
        "@Talk to Firentis:",
        "@Talk to Deshavi:",
        "@Talk to Matheld:",
        "@Talk to Alayen:",
        "@Talk to Bunduk:",
        "@Talk to Katrin:",
        "@Talk to Jeremus:",
        "@Talk to Nizar:",
        "@Talk to Lezalit:",
        "@Talk to Artimenner:",
        "@Talk to Klethi:",
        "@Go to the captive or refugee witness:",
        "@Go to a market contact, caravan, or bargain:",
        "@Go to a public witness:",
        "@Find a Black Khergit rider witness",
        "@Go to the restitution village or battle witness:",
        "@Go to the survivor, hunter, or trail focus:",
        "@Ask a ranker what the line learned after battle",
        "@Go to a lord, elder, or public witness:",
        "@Go to the rank-and-file witness:",
        "@Go to the accounts or camp witness, then run Katrin's supply watch",
        "@Go to the wounded or triage witness:",
        "@Mark the charge in a field setup",
        "@Go to the drill or troop witness:",
        "@Go to the siege works or construction witness:",
        "@Go to the tavern contact or old-job witness:",
    ):
        assert_contains(quest_journal, journal_token)

    for name in (
        "Borcha",
        "Marnid",
        "Ymira",
        "Rolf",
        "Baheshtur",
        "Firentis",
        "Deshavi",
        "Matheld",
        "Alayen",
        "Bunduk",
        "Katrin",
        "Jeremus",
        "Nizar",
        "Lezalit",
        "Artimenner",
        "Klethi",
    ):
        assert_contains(companion_bible, f"## {name}")
        assert_contains(companion_checklist, f"## {name}")

    for token in (
        "## Global Framework",
        "## Shared Gameplay Hooks",
        "## Dragon Age Origins Depth Gap",
        "### Companion Quest Framework Migration",
        "### DAO-Style Gap Milestones",
        "## DAO-Style Personal Quest Requirements",
        "## Companion Depth Priority Queue",
        "## Writing Deliverables",
        "### Baseline Writing Coverage",
        "### Writing Coverage Matrix",
        "### Banter Seed Backlog",
        "### Late Reflection Backlog",
        "## Companion Implementation Template",
        "### Identity and Values",
        "### Approval and Reactivity Hooks",
        "### Campfire and Direct Dialogue",
        "### Advisor Role and Degraded State",
        "### Personal Quest Stages and Outcomes",
        "### Cross-Companion Triangle Coverage",
        "### World-System Integration",
        "### Static Tests and Build Verification",
        "## Test Checklist",
        "The Road Keeps Its Own",
        "The Honest Price",
        "## Rolf - A Name Worth Wearing",
        "## Baheshtur - The Unbroken Saddle",
        "## Firentis - Debt of the Sword",
        "## Deshavi - Tracks Through Ash",
        "## Matheld - No Backward Step",
        "## Alayen - The Standard and the Self",
        "## Bunduk - The Men Who Hold the Line",
        "## Katrin - The Last Coin in Camp",
        "## Jeremus - Hands That Will Not Harden",
        "## Nizar - The Impossible Charge",
        "## Artimenner - The Siege That Should Have Worked",
        "## Klethi - A Knife With a Name",
        "Deep background documented.",
        "Voice guide documented.",
        "Approval tiers documented.",
        "Quest outcome index documented.",
        "Every companion has at least one personal quest incident triggered by world play, not only campfire choices.",
        "Every companion personal arc has quest-framework metadata rather than only a camp menu and troop-slot stage.",
        "Every companion personal arc can use quest runtime accept, update, complete, fail, and abort lifecycle hooks where appropriate.",
        "Every companion personal arc writes journal entries for opening, stage update, good outcome, hard outcome, and failure or rupture.",
        "Every companion personal arc records at least one memory event through the quest dialogue memory layer.",
        "Every companion personal arc applies at least one quest outcome consequence beyond approval.",
        "Companion personal arcs can be advanced by quest event dispatch from world systems.",
        "Companion reports show visible aftermath from quest-framework state, not only companion-depth slot state.",
        "- [x] Every companion personal arc has quest-framework metadata rather than only a camp menu and troop-slot stage.",
        "- [x] Every companion personal arc can use quest runtime accept, update, complete, fail, and abort lifecycle hooks where appropriate.",
        "- [x] Every companion personal arc writes journal entries for opening, stage update, good outcome, hard outcome, and failure or rupture.",
        "- [x] Companion reports show visible aftermath from quest-framework state, not only companion-depth slot state.",
        "Use `sod_quest_runtime_accept` when a trust-opened companion arc becomes an active personal quest.",
        "Use `sod_quest_runtime_update` when a companion arc advances from world play or a menu choice.",
        "Use `sod_quest_runtime_complete` for good/trust resolutions.",
        "Use `sod_quest_runtime_fail` or `sod_quest_runtime_abort` for rupture, refusal, or abandoned personal arcs.",
        "Use `sod_quest_dialogue_record_event` for companion memory beats that future dialogue can reference.",
        "Use `sod_quest_journal_update` so personal arcs appear in the quest journal with current stage text.",
        "Use `sod_quest_outcome_apply_consequences` for rewards, penalties, role payoff flags, or world-state changes.",
        "Use `sod_quest_event_dispatch` or existing world hooks to advance companion arcs from battles, captives, diplomacy, construction, and faction systems.",
        "Milestone 1: migrate Ymira and Lezalit personal arcs into the quest framework as prototypes.",
        "Prototype: Ymira and Lezalit have quest-framework IDs and display names.",
        "Prototype: Ymira and Lezalit call quest runtime accept/update/complete/fail hooks from companion-depth stage changes.",
        "Prototype: Ymira and Lezalit show quest-framework aftermath in the companion depth report.",
        "Milestone slice: Bunduk, Jeremus, and Firentis have quest-framework IDs, runtime bridge support, and report aftermath.",
        "Milestone 2: migrate Bunduk, Jeremus, and Firentis with stronger battlefield, casualty, mercy, and discipline hooks.",
        "Milestone slice: all remaining companion arcs have quest-framework IDs, runtime bridge support, and report aftermath.",
        "Milestone 3: migrate all remaining companion arcs into quest-framework identity, journal, memory, and outcome handling.",
        "Milestone 2: migrate Bunduk, Jeremus, and Firentis with stronger battlefield, casualty, mercy, and discipline hooks.",
        "Milestone slice: gameplay-triggered triangle incidents dispatch quest events, record memory, and refresh the journal.",
        "Milestone 4: add triangle incidents that are quest events, not only report text.",
        "Milestone 5: add late-game reflections triggered by repeated value-aligned or value-breaking behavior.",
        "- [x] Add optional late-game reflection hook when the companion's theme has been proven over time.",
        "- [x] Add quest framework ID/name.",
        "- [x] Add at least one recorded memory event.",
        "- [x] Add at least one beyond-campfire incident where world play tests the companion's values.",
        "- [x] Add optional triangle-specific incident when three companions have a strong shared stake.",
        "Add quest framework ID/name.",
        "Add quest journal opening text.",
        "Add quest journal stage update text.",
        "Add quest journal good outcome text.",
        "Add quest journal hard outcome text.",
        "Add quest journal failure or rupture text.",
        "Add at least one recorded memory event.",
        "Add at least one quest outcome consequence beyond approval.",
        "6 campfire mood lines, one per approval band.",
        "1 generic \"ask how you are\" direct dialogue response.",
        "1 role assignment line for each valid role.",
        "1 role-disabled/low-approval sentence.",
        "2 banter seeds with liked companion.",
        "2 banter seeds with disliked companion.",
        "1 late-game reflection line.",
        "Borcha/Marnid: add two practical-friendship banter seeds and two road-vs-status friction seeds.",
        "Ymira/Lezalit/Bunduk: add two mercy-discipline-soldier welfare banter seeds and two argument seeds.",
        "Firentis/Jeremus/Matheld: add two penance-healing banter seeds and two courage-vs-restraint argument seeds.",
        "Rolf/Alayen/Nizar: add two public-honor banter seeds and two legitimacy/glory argument seeds.",
        "Baheshtur/Katrin/Artimenner: add two road-supplies-planning banter seeds and two freedom-vs-accounts argument seeds.",
        "Deshavi/Klethi/Katrin: add two survival-practicality banter seeds and two theft-vs-care argument seeds.",
        "Ymira: late reflection after repeated captive mercy or repeated slave-trade cruelty.",
        "Lezalit: late reflection after repeated disciplined victories or repeated command weakness.",
        "Klethi: late reflection after repeated chosen-belonging choices or repeated betrayal.",
        "Companion banter progresses by approval/quest stage instead of staying mostly static.",
        "Manual QA confirms each companion's quest opening, middle choice, good outcome, hard outcome, warning, and reconciliation.",
        "Ymira: add a fuller captive/refugee quest menu with protection, ransom, and expedience paths.",
        "Add dedicated Mercy Under Arms captive/refugee menu beyond campfire.",
        "Add protection, ransom/weakest-release, and expedience paths.",
        "Lezalit: add multi-stage direct talk and a stronger resolved-good Captain/training payoff.",
        "Lezalit: add a captured Imperial drill quest menu with reform, fear, and refusal paths.",
        "Add dedicated Discipline Without Chains captured Imperial drill menu beyond campfire.",
        "Add reform, fear, and refusal paths.",
        "Bunduk: add soldier-welfare quest incident tied to casualties, wages, or officer cruelty.",
        "Bunduk: add line grievance quest menu with advocate, compromise, and crackdown paths.",
        "Add dedicated Men Who Hold the Line grievance menu beyond campfire.",
        "Add advocate, compromise, and crackdown paths.",
        "Jeremus: add battlefield triage incident beyond campfire.",
        "Jeremus: add triage menu with mercy, hard triage, and company-first paths.",
        "Add dedicated Hands That Will Not Harden triage menu beyond campfire.",
        "Add mercy, hard triage, and company-first paths.",
        "Firentis: add restitution or battlefield mercy incident beyond campfire.",
        "Add dedicated Debt of the Sword restitution menu beyond campfire.",
        "Add restitution, confession, and silence paths.",
        "Katrin: add food/wage shortage incident beyond campfire.",
        "Add dedicated Last Coin in Camp shortage menu beyond campfire.",
        "Add stores, rationing, and glory-spend paths.",
        "Deshavi: add trail warning incident tied to poor villages, Slavers, or raiders.",
        "Add dedicated Tracks Through Ash trail warning menu beyond campfire.",
        "Add shelter, ambush, and hunt-only paths.",
        "Klethi: add underworld/stealth incident beyond campfire.",
        "Add dedicated A Knife With a Name old-job menu beyond campfire.",
        "Add choose, protect, and sellout paths.",
        "Rolf, Alayen, and Nizar: add public honor/glory/noble legitimacy incident cluster.",
        "Rolf: add public legitimacy world incident tied to lordly courts, tournaments, or honors.",
        "Add dedicated A Name Worth Wearing public challenge menu beyond campfire.",
        "Add earn, defend, and expose paths.",
        "Alayen: add oath/standard world incident tied to diplomacy, lord release, or village protection.",
        "Add dedicated The Standard and the Self oath menu beyond campfire.",
        "Add duty, oath, and pride paths.",
        "Nizar: add hard-victory or tournament-glory world incident.",
        "Add dedicated The Impossible Charge heroic action menu beyond campfire.",
        "Add responsible, daring, and blood-legend paths.",
        "Baheshtur, Matheld, and Artimenner: add battlefield freedom/courage/engineering incident cluster.",
        "Baheshtur: add mounted-pursuit or Black Khergit pressure payoff for resolved-good Scout/Captain.",
        "Add dedicated The Unbroken Saddle Black Khergit rider menu beyond campfire.",
        "Add free, pursuit, and submission paths.",
        "Matheld: add battlefield courage incident beyond campfire.",
        "Add dedicated No Backward Step battlefield line menu beyond campfire.",
        "Add temper, stand, and blood-price paths.",
        "Artimenner: add construction/siege-preparation world incident beyond campfire.",
        "Add dedicated The Siege That Should Have Worked construction menu beyond campfire.",
        "Add rebuild, improvise, and blame paths.",
        "Add richer multi-stage direct-talk responses by warning and quest stage.",
        "Static test coverage.",
        "Build verified.",
    ):
        assert_contains(companion_checklist, token)

    companion_immersion_audit = read("docs/COMPANION_QUEST_IMMERSION_AUDIT.md")
    for token in (
        "- [x] Companion depth static test detects direct-talk pending incident entries.",
        "- [x] Camp menus are allowed only as fallback/resolution compatibility.",
        "- [x] Each companion incident has either a direct dialogue branch or a documented adventure surface.",
        "- [x] Each adventure surface stores or derives a focus center/party/cause.",
        "- [x] Quest-framework journal text distinguishes \"talk to companion\" from \"go to place/actor.\"",
        "- [x] Every companion has a pending incident that can be discussed directly with the companion.",
        "- [x] Camp menus are fallback or planning surfaces, not the default climax for every companion quest.",
        "### Adventure Pattern Verification Matrix",
        "| Ymira - Mercy Under Arms | `$g_sod_ymira_refugee_focus_center`; `$g_sod_ymira_refugee_witnessed` |",
        "| Marnid - The Honest Price | `$g_sod_marnid_market_contacted`; center trade identity derived at goods merchant |",
        "| Lezalit - Discipline Without Chains | `$g_sod_lezalit_ief_discipline_pending`; `$g_sod_lezalit_ief_discipline_witnessed` |",
        "| Artimenner - The Siege That Should Have Worked | `$g_sod_artimenner_siege_pending`; `$g_sod_artimenner_siege_cause`; `$g_sod_artimenner_siege_witnessed` |",
        "Direct companion dialogue after witness, with camp fallback",
    ):
        assert_contains(companion_immersion_audit, token)

    for token in (
        "- [ ] Manual QA confirms each companion's quest opening, middle choice, good outcome, hard outcome, warning, and reconciliation.",
        "- [ ] **Manual QA:** The quest is played through in-game once for each major outcome.",
    ):
        assert_contains(companion_checklist, token)

    for token in (
        "## Automated Implementation Status",
        "All native companion first-pass interactive campaign slices are implemented and covered by static QA.",
        "Static success proves the campaign scaffolding is present; manual QA proves the mission flow",
        "- [x] The quest cannot start, advance, or resolve unless the companion is in the party",
        "- [x] At least one non-companion NPC, party, or scene prop can change the quest state.",
        "- [x] At least one interactive climax exists in a menu, scene, mission template, or encounter.",
        "- [x] `py build\\test_companion_depth_system.py`",
        "- [x] `py build\\test_dialogue_immersion_static.py`",
        "- [x] `py build\\doctor.py --doctor-new-only`",
        "- [x] `py build\\build_all.py`",
        "9. Artimenner - implemented first pass after Lezalit",
        "10. Alayen - implemented first pass after Artimenner",
        "11. Rolf - implemented first pass after Alayen",
        "12. Baheshtur - implemented first pass after Rolf",
        "13. Matheld - implemented first pass after Baheshtur",
        "14. Katrin - implemented first pass after Matheld",
        "15. Nizar - implemented first pass after Katrin",
        "## Shared QA Matrix",
        "- [x] Static QA: final resolution is gated behind clue and confrontation progress.",
        "- [x] Static QA: troop ids reference the intended companion only.",
        "Manual QA still required:",
        "- [ ] Complete best, good, hard, and failure paths.",
        "docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md",
    ):
        assert_contains(interactive_quest_checklist, token)

    for token in (
        "# Companion Interactive Quest Playtest Matrix",
        "Use this file for live Warband QA of the companion interactive quest campaign slices.",
        "## Universal Smoke Route",
        "- [ ] Recruit the companion and confirm the quest trigger or direct-talk opening appears only while they are in the party.",
        "- [ ] Visit the wrong target first and confirm witness/contact options are suppressed.",
        "- [ ] Try to resolve immediately after the witness step and confirm the final moral choice is still blocked until the confrontation/climax.",
        "- [ ] Remove the companion after starting but before resolving and verify cleanup or recoverable blocking.",
        "## Ymira - Mercy Under Arms",
        "## Firentis - Debt Of The Sword",
        "## Deshavi - Tracks Through Ash",
        "## Borcha - The Road Keeps Its Own",
        "## Marnid - The Honest Price",
        "## Bunduk - The Men Who Hold The Line",
        "## Jeremus - Hands That Will Not Harden",
        "## Lezalit - Discipline Without Chains",
        "## Artimenner - The Siege That Should Have Worked",
        "## Alayen - The Standard And The Self",
        "## Rolf - A Name Worth Wearing",
        "## Baheshtur - The Unbroken Saddle",
        "## Matheld - No Backward Step",
        "## Nizar - The Impossible Charge",
        "## Katrin - The Last Coin In Camp",
        "No-field-setup camp suppression",
        "Supply-watch combat loss",
        "Rider-oath combat win",
        "Repair-watch defeat",
        "docs/COMPANION_INTERACTIVE_QUEST_QA_COMMANDS.md",
        "Wrong town: witness does not appear outside the focus town.",
        "When a companion passes every row, mark the matching manual QA line",
    ):
        assert_contains(interactive_quest_playtest, token)

    for token in (
        "# Companion Interactive Quest QA Commands",
        "The companion interactive quest QA menu is debug-only.",
        "Choose `DEBUG: Companion interactive quest QA.`",
        "QA: Recruit companion roster and open trust",
        "`ready for live climax`",
        "`ready for aftermath`",
        "These hooks require `$g_sod_debug = 1`.",
        "They are QA accelerators, not replacement quest content.",
        "Nizar: ready for charge-lane test.",
        "Klethi: ready for alley confrontation.",
    ):
        assert_contains(interactive_quest_qa_commands, token)

    assert_contains(campfire, "Make amends for named grievances")
    assert_contains(campfire, "companion_campfire_ymira_mercy_spare")
    assert_contains(campfire, "companion_campfire_ymira_mercy_hard")
    assert_contains(campfire, "companion_campfire_marnid_honest_price_clean")
    assert_contains(campfire, "companion_campfire_marnid_honest_price_hard")
    assert_contains(scripts, "sod_companion_quest_resolved_good")
    assert_contains(scripts, "sod_companion_quest_resolved_hard")
    assert_contains(read("src/scripts/ZG_quests/cf_sod_companion_campaign_available.py"), '"cf_sod_companion_campaign_available"')
    assert_not_contains(campfire, "script_cf_sod_companion")

    for warning_name in (
        "Borcha keeps his voice low",
        "Marnid closes his ledger",
        "Ymira looks at the wounded",
        "Rolf's bow is painfully formal",
        "Baheshtur's hand rests near his reins",
        "Firentis speaks quietly",
        "Deshavi does not soften it",
        "Matheld's stare is blunt as iron",
        "Alayen's courtesy has gone cold",
        "Bunduk folds his arms",
        "Katrin's voice is flat",
        "Jeremus looks exhausted",
        "Nizar smiles without warmth",
        "Lezalit is precise and severe",
        "Artimenner taps a finger",
        "Klethi's joke never arrives",
    ):
        assert_contains(scripts, warning_name)

    for reconciliation_name in (
        "Roads remember, but they also fork",
        "make the next account cleaner",
        "mercy still has a place",
        "A noble correction is still noble",
        "I ride beside you by choice",
        "judge the next deed",
        "Look down at the tracks",
        "the shield slipped",
        "Honor repaired",
        "fewer stupid orders",
        "Supper and wages",
        "keep healing men",
        "A turn in the tale",
        "Correction accepted",
        "listening before things collapse",
        "opens from both sides",
    ):
        assert_contains(scripts, reconciliation_name)

    print("[companion_depth_system] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

