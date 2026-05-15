from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_ambush_missions_do_not_allow_global_reinforcement_key() -> None:
    city_ambush = read("src/mission_templates/0005_bandits_at_night/bandits_at_night.py")
    village_ambush = read("src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py")
    assert "formations_v" not in city_ambush
    assert "formations_v" not in village_ambush


def test_capture_prisoner_lord_quest_has_dedicated_acceptance_options() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    accept = "ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners.py"
    reject = "ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners_02.py"
    generic = "ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told.py"
    assert accept in order
    assert reject in order
    assert order.index(accept) < order.index(generic)
    assert order.index(reject) < order.index(generic)

    accept_text = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners.py")
    reject_text = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners_02.py")
    generic_accept = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told.py")
    generic_reject = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_02.py")
    assert '(eq, "$random_quest_no", "qst_capture_prisoners")' in accept_text
    assert '(eq, "$random_quest_no", "qst_capture_prisoners")' in reject_text
    assert '(neq, "$random_quest_no", "qst_capture_prisoners")' in generic_accept
    assert '(neq, "$random_quest_no", "qst_capture_prisoners")' in generic_reject


def test_construction_reports_sanitize_stale_finished_project_slots() -> None:
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    assert '(party_slot_ge, ":center_no", ":building_no", 1)' in construction
    assert '(party_set_slot, ":center_no", slot_center_current_improvement, 0)' in construction

    for path in (
        "src/menus/centers/common/center_manage.py",
        "src/menus/kingdom/fief_available_construction_report.py",
        "src/menus/centers/castle/castle_castle.py",
    ):
        assert "script_sod_ensure_center_construction_state" in read(path)


def test_inner_siege_continue_menu_has_no_dead_future_text() -> None:
    menu = read("src/menus/other/continue_14.py")
    assert "TODO: To use for the future" not in menu
    assert "As a last defensive effort" not in menu
    assert "You've been driven away from the walls" in menu
    assert menu.count("(str_store_string, s1,") == 4


def test_mercenary_encounter_handles_stale_party_boss_data() -> None:
    troop_name = read("src/scripts/ZH_heroes/store_troop_name.py")
    assert '(neg|is_between, ":troop", 0, "trp_last_troop")' in troop_name
    assert '@an unknown commander' in troop_name

    merc_ask = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_party_encounter_mercs_ask.py")
    for token in (
        '(str_store_string, s1, "@an unknown captain")',
        '(str_store_string, s2, "@an unmarked company")',
        '(str_store_string, s3, "@uncertain service")',
        '(is_between, ":troop", 0, "trp_last_troop")',
        '(is_between, ":troop_fac", 0, "fac_factions_end")',
        '(is_between, "$g_encountered_party_faction", 0, "fac_factions_end")',
    ):
        assert token in merc_ask

    merc_attack = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs_attack.py")
    assert '[anyone, "party_encounter_mercs_attack"' in merc_attack
    assert '[anyone|plyr, "party_encounter_mercs_attack"' not in merc_attack
    assert '(party_get_num_companions, ":num_companions", "$g_encountered_party")' in merc_attack
    assert '(gt, ":num_companions", 0)' in merc_attack
    assert '(is_between, ":troop", 0, "trp_last_troop")' in merc_attack
    assert '(is_between, ":troop_fac", 0, "fac_factions_end")' in merc_attack
    assert 'script_make_kingdom_hostile_to_player' in merc_attack
    assert '(call_script, "script_sod_safe_leave_encounter")' in merc_attack
    assert '(encounter_attack)' in merc_attack

    merc_ultimatum = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs_02.py")
    assert "script_let_nearby_parties_join_current_battle" not in merc_ultimatum
    assert "script_make_kingdom_hostile_to_player" not in merc_ultimatum

    merc_intro = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs.py")
    assert "Who are you?" in merc_intro
    assert "Wha are you?" not in merc_intro

    prisoner_accept = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_accept3_02.py")
    assert "provisions and equipment" in prisoner_accept
    assert "equiment" not in prisoner_accept

    merc_hostile_refuse = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs_hostile_attacker_2_02.py")
    assert '(assign, "$g_enemy_party", "$g_encountered_party")' in merc_hostile_refuse
    assert 'script_let_nearby_parties_join_current_battle' in merc_hostile_refuse
    assert '(encounter_attack)' in merc_hostile_refuse

    lord_attack = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_attack_verify_commit.py")
    assert '(assign, "$g_enemy_party", "$g_encountered_party")' in lord_attack
    assert 'script_let_nearby_parties_join_current_battle' in lord_attack
    assert '(encounter_attack)' in lord_attack

    hostile_fight = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_hostile_attacker_02.py")
    assert '(assign, "$g_enemy_party", "$g_encountered_party")' in hostile_fight
    assert 'script_let_nearby_parties_join_current_battle' in hostile_fight
    assert '(encounter_attack)' in hostile_fight

    terminal_threats = [
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_attack.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_barter_02.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_barter_3b.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_barter_reputation_block.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_grudge_revenge_intimidation.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_grudge_revenge_shakedown.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_recruit.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandits_awaiting_remeet_2.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_bandit_talk.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/party_tpl_pt_bandits_plyr_looters_2.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/party_tpl_pt_bandits_plyr_looters_2_02.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_deserter_barter_3b.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_deserter_dishonorable_response.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_deserter_talk.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_deserter_paid_talk_2b.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_hostile_faction_bluff_fail.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_hostile_leader_duel_accepts.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_job_board_surrender_refuse.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_stated.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_ravaging_bandits_intro_2.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_troublesome_bandits_intro_2.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_party_encounter_offer_dont_fight_02.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_capitalist_avoid_battle_ask_02.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_centurion_avoid_battle_denied.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_centurion_avoid_battle_03.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_bandits_awaiting_ransom_fight.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_militia_awaiting_ransom_fight.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_boar_clan_attack.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_chieftain_intro_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_capitalist_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_crusader_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_imperialist_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_liberator_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_nihilistic_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_racist_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_respectful_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_sane_6.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_boar_clan_talk.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_boar_clan_talk_02.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_slavers_jc_intro_2.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_threaten_1.py",
        "src/dialogs/ZZ99_misc_dialogs/party_tpl_pt_enemy_enemy_talk_2.py",
    ]
    for path in terminal_threats:
        raw = read(path)
        assert '(assign, "$g_enemy_party", "$g_encountered_party")' in raw
        assert 'script_let_nearby_parties_join_current_battle' in raw
        assert '(encounter_attack)' in raw

    messenger = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_messenger_party_start.py")
    for token in (
        "This road will not carry a rival faith's mercy",
        "The chest reaches its lord or we die around it",
        "Then defend it.",
    ):
        text_index = messenger.index(token)
        attack_index = messenger.index("(encounter_attack)", text_index)
        branch = messenger[text_index:attack_index]
        assert '(assign, "$g_enemy_party", "$g_encountered_party")' in branch
        assert 'script_let_nearby_parties_join_current_battle' in branch

    lord_fight_responses = [
        "src/dialogs/ZA01_startup_and_dispatch/anyone_auto_proceed_party_encounter_lord_hostile_attacker_2_fight_02.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_sod_nemesis_lord_hostile_fight.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_party_encounter_lord_hostile_attacker_2_fight.py",
        *[
            f"src/dialogs/ZB01_lords_politics_and_family/anyone_party_encounter_lord_hostile_attacker_2_fight_{idx:02d}.py"
            for idx in range(2, 9)
        ],
    ]
    for path in lord_fight_responses:
        raw = read(path)
        assert '(assign, "$g_enemy_party", "$g_encountered_party")' in raw
        assert 'script_let_nearby_parties_join_current_battle' in raw
        assert '(encounter_attack)' in raw

    prisoner_execute = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_die4.py")
    assert '[anyone, "prisoner_chat_die4"' in prisoner_execute
    assert '[anyone|plyr, "prisoner_chat_die4"' not in prisoner_execute
    assert "You slit the prisoner's throat" in prisoner_execute


def test_dialog_encounter_attack_branches_prepare_battle_context() -> None:
    for path in (ROOT / "src/dialogs").rglob("*.py"):
        raw = path.read_text(encoding="utf-8")
        offset = 0
        while True:
            attack_index = raw.find("(encounter_attack)", offset)
            if attack_index < 0:
                break
            branch_window = raw[max(0, attack_index - 800):attack_index]
            rel_path = path.relative_to(ROOT).as_posix()
            assert '(assign, "$g_enemy_party", "$g_encountered_party")' in branch_window, rel_path
            assert 'script_let_nearby_parties_join_current_battle' in branch_window, rel_path
            offset = attack_index + 1


def test_quest_start_dialogues_validate_spawn_and_name_parties() -> None:
    guarded_starts = {
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_quest_brief.py": "qst_kidnapped_girl",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_clansmen.py": "qst_jotnar_clan_free_clansmen",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_spy.py": "qst_serpent_host_free_spy",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_escort_merchant_caravan_quest_brief.py": "qst_escort_merchant_caravan",
    }
    for path, quest_id in guarded_starts.items():
        raw = read(path)
        assert f'(quest_get_slot, ":quest_target_center", "{quest_id}", slot_quest_target_center)' in raw
        assert '(party_is_active, ":quest_target_center")' in raw
        assert '(party_is_active, "$g_encountered_party")' in raw


if __name__ == "__main__":
    test_ambush_missions_do_not_allow_global_reinforcement_key()
    test_capture_prisoner_lord_quest_has_dedicated_acceptance_options()
    test_construction_reports_sanitize_stale_finished_project_slots()
    test_mercenary_encounter_handles_stale_party_boss_data()
    test_dialog_encounter_attack_branches_prepare_battle_context()
    test_quest_start_dialogues_validate_spawn_and_name_parties()
    print("test_bug_batch_forum_regressions_static: OK")


