from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_guarded_rescue_acceptance(path, quest_id, template_id):
    raw = read(path)

    assert '(assign, "$g_sod_last_rescue_spawn_ok", 0)' in raw
    assert f'(spawn_around_party, ":quest_target_center", "{template_id}")' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert '(party_is_active, ":quest_target_party")' in raw
    assert '(assign, "$g_sod_last_rescue_spawn_ok", 1)' in raw

    guard_index = raw.index('(assign, "$g_sod_last_rescue_spawn_ok", 1)')
    gold_index = raw.index('(call_script, "script_troop_add_gold"')
    start_index = raw.index(f'(call_script, "script_start_quest", "{quest_id}"')
    assert guard_index < gold_index < start_index


def assert_ordered(path, tokens):
    raw = read(path)
    offset = 0
    for token in tokens:
        index = raw.find(token, offset)
        if index < 0:
            raise AssertionError(f"{path}: missing ordered token after {offset}: {token}")
        offset = index + len(token)


def test_kidnapped_girl_acceptance_requires_valid_bandit_party():
    assert_guarded_rescue_acceptance(
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_quest_brief.py",
        "qst_kidnapped_girl",
        "pt_bandits_awaiting_ransom",
    )

    taken = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_kidnapped_girl_quest_taken.py")
    assert "$g_sod_last_rescue_spawn_ok" in taken
    assert "The bandits' trail has gone cold" in taken


def test_serpent_spy_acceptance_requires_valid_militia_party():
    assert_guarded_rescue_acceptance(
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_spy.py",
        "qst_serpent_host_free_spy",
        "pt_militia_awaiting_ransom",
    )

    taken = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_mission_told_free_spy_taken.py")
    assert "$g_sod_last_rescue_spawn_ok" in taken
    assert "The militia column has slipped from our sight" in taken

    briefing = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_06.py")
    assert_ordered(
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_spy.py",
        (
            '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_target_party, ":quest_target_party")',
            '(party_add_prisoners, ":quest_target_party", "trp_sh_spy", 1)',
            '(party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold)',
        ),
    )
    assert "One of my spies was taken near {s13}" in briefing
    assert "Ramsacking" not in briefing


def test_jotnar_clansmen_acceptance_requires_valid_slaver_party():
    assert_guarded_rescue_acceptance(
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_clansmen.py",
        "qst_jotnar_clan_free_clansmen",
        "pt_slaves_with_jotnar_clansmen",
    )

    taken = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_mission_told_free_clansmen_taken.py")
    assert "$g_sod_last_rescue_spawn_ok" in taken
    assert "The slaver party has vanished from the route" in taken


def test_jotnar_freed_clansmen_handoff_after_battle_is_guarded():
    assert_ordered(
        "src/scripts/ZC_parties/event_player_defeated_enemy_party.py",
        (
            '(quest_slot_eq, "qst_jotnar_clan_free_clansmen", slot_quest_target_party, "$g_enemy_party")',
            '(spawn_around_party, "p_main_party", "pt_jotnar_clansmen")',
            '(assign, ":freed_clansmen_party", reg0)',
            '(gt, ":freed_clansmen_party", 0)',
            '(party_is_active, ":freed_clansmen_party")',
            '(quest_set_slot, "qst_jotnar_clan_free_clansmen", slot_quest_target_party, ":freed_clansmen_party")',
            '(party_set_ai_behavior, ":freed_clansmen_party", ai_bhvr_hold)',
            '(party_set_flags, ":freed_clansmen_party", pf_default_behavior, 0)',
            "The freed Jotnar clansmen gather near your camp",
            '(call_script, "script_succeed_quest", "qst_jotnar_clan_free_clansmen")',
            "The freed Jotnar clansmen scatter from the broken slaver camp",
        ),
    )


def test_jotnar_clansmen_completion_requires_actual_rescued_party():
    assert_ordered(
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_jotnar_clansmen_start.py",
        (
            '(check_quest_active, "qst_jotnar_clan_free_clansmen")',
            '(neg|check_quest_concluded, "qst_jotnar_clan_free_clansmen")',
            '(quest_get_slot, ":quest_target_party", "qst_jotnar_clan_free_clansmen", slot_quest_target_party)',
            '(eq, "$g_encountered_party", ":quest_target_party")',
            '(party_is_active, "$g_encountered_party")',
            '(store_distance_to_party_from_party, ":dist", "$g_encountered_party", "p_sod_merc_guild_4")',
            '(lt, ":dist", 2)',
            '(quest_get_slot, ":quest_target_party", "qst_jotnar_clan_free_clansmen", slot_quest_target_party)',
            '(call_script, "script_succeed_quest", "qst_jotnar_clan_free_clansmen")',
            '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_jotnar_support, 2)',
            '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1)',
            '(party_is_active, ":quest_target_party")',
            '(party_get_template_id, ":encounter_template", ":quest_target_party")',
            '(eq, ":encounter_template", "pt_jotnar_clansmen")',
            '(remove_party, ":quest_target_party")',
        ),
    )


def test_jotnar_clansmen_follow_response_requires_actual_rescue_party():
    assert_ordered(
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_jotnar_clansmen.py",
        (
            '(check_quest_active, "qst_jotnar_clan_free_clansmen")',
            '(neg|check_quest_concluded, "qst_jotnar_clan_free_clansmen")',
            '(quest_slot_eq, "qst_jotnar_clan_free_clansmen", slot_quest_target_party, "$g_encountered_party")',
            '(party_is_active, "$g_encountered_party")',
            "Yes. Stay close and I will get you home.",
            '(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party)',
            '(party_set_ai_object, "$g_encountered_party", "p_main_party")',
            '(party_set_flags, "$g_encountered_party", pf_default_behavior, 0)',
            '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1)',
        ),
    )

    wait = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_jotnar_clansmen_02.py")
    assert "Wait here. I need a moment." in wait


def test_serpent_spy_party_handoff_requires_actual_rescued_party():
    assert_ordered(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_militia_awaiting_ransom_militia_awaiting_ransom_pay.py",
        (
            '(spawn_around_party, ":quest_target_party", "pt_sh_spy")',
            '(assign, "$g_sh_spy", reg0)',
            '(party_is_active, "$g_sh_spy")',
            '(party_remove_prisoners, ":quest_target_party", "trp_sh_spy", 1)',
            '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)',
            '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_sh_spy")',
        ),
    )

    fight = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_militia_awaiting_ransom_fight.py")
    assert "(encounter_attack)" in fight
    assert "pt_sh_spy" not in fight
    assert 'slot_quest_current_state, 1' not in fight
    assert_ordered(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_militia_awaiting_ransom_fight.py",
        (
            '(quest_get_slot, ":quest_target_party", "qst_serpent_host_free_spy", slot_quest_target_party)',
            '(party_count_prisoners_of_type, ":spy_prisoners", ":quest_target_party", "trp_sh_spy")',
            '(eq, ":spy_prisoners", 0)',
            '(party_add_prisoners, ":quest_target_party", "trp_sh_spy", 1)',
            "(encounter_attack)",
        ),
    )

    assert_ordered(
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sh_spy_start.py",
        (
            '(check_quest_active, "qst_serpent_host_free_spy")',
            '(neg|check_quest_concluded, "qst_serpent_host_free_spy")',
            '(quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party")',
            '(party_is_active, "$g_encountered_party")',
        ),
    )


def test_serpent_spy_follow_and_wait_responses_are_guarded():
    for path in (
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sh_spy_encounter_1.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sh_spy_encounter_1_02.py",
    ):
        assert_ordered(
            path,
            (
                '(check_quest_active, "qst_serpent_host_free_spy")',
                '(neg|check_quest_concluded, "qst_serpent_host_free_spy")',
                '(quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party")',
                '(party_is_active, "$g_encountered_party")',
            ),
        )

    join = read("src/dialogs/ZZ99_misc_dialogs/anyone_sh_spy_join_02.py")
    wait = read("src/dialogs/ZZ99_misc_dialogs/anyone_spy_wait.py")
    no_room = read("src/dialogs/ZZ99_misc_dialogs/anyone_sh_spy_join.py")
    assert "Good. I will keep up." in join
    assert "sod_companion_action_free_captives" in join
    for raw in (wait, no_room):
        assert '(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold)' in raw
        assert '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party")' in raw
        assert '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)' in raw
    assert "nee to give" not in wait


def test_serpent_spy_battle_rescue_conversation_is_reachable_and_safe():
    start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_106.py")
    assert '(eq, ":cur_troop", "trp_sh_spy")' in start
    assert '(eq, ":cur_troop", "trp_kidnapped_girl")' not in start

    order = read("src/dialogs/_order_dialogs.txt")
    for path in (
        "ZZ99_misc_dialogs/trp_sh_spy_plyr_sh_spy_liberated_battle.py",
        "ZZ99_misc_dialogs/trp_sh_spy_sh_spy_liberated_battle_join.py",
        "ZZ99_misc_dialogs/trp_sh_spy_sh_spy_liberated_battle_join_02.py",
        "ZZ99_misc_dialogs/trp_sh_spy_plyr_sh_spy_liberated_battle_02.py",
        "ZZ99_misc_dialogs/trp_sh_spy_sh_spy_liberated_battle_wait.py",
    ):
        assert path in order

    join = read("src/dialogs/ZZ99_misc_dialogs/trp_sh_spy_sh_spy_liberated_battle_join_02.py")
    wait = read("src/dialogs/ZZ99_misc_dialogs/trp_sh_spy_sh_spy_liberated_battle_wait.py")
    assert '(party_add_members, "p_main_party", "trp_sh_spy", 1)' in join
    assert '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)' in join
    assert "sod_companion_action_free_captives" in join
    assert '(spawn_around_party, "p_main_party", "pt_sh_spy")' in wait
    assert '(party_is_active, ":spy_party")' in wait
    assert '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_target_party, ":spy_party")' in wait


def test_kidnapped_girl_party_handoff_requires_actual_rescued_party():
    assert_ordered(
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_kidnapped_girl_start.py",
        (
            '(check_quest_active, "qst_kidnapped_girl")',
            '(neg|check_quest_concluded, "qst_kidnapped_girl")',
            '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 2)',
            '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party")',
            '(party_is_active, "$g_encountered_party")',
        ),
    )

    for path in (
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_encounter_1.py",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_encounter_1_02.py",
    ):
        assert_ordered(
            path,
            (
                '(check_quest_active, "qst_kidnapped_girl")',
                '(neg|check_quest_concluded, "qst_kidnapped_girl")',
                '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 2)',
                '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party")',
                '(party_is_active, "$g_encountered_party")',
            ),
        )

    join = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_kidnapped_girl_join_02.py")
    assert "Thank you. I will stay close." in join
    assert "sod_companion_action_free_captives" in join


def test_kidnapped_girl_battle_rescue_is_guarded_and_spawn_safe():
    start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_105.py")
    assert '(eq, "$talk_context", tc_hero_freed)' in start
    assert '(check_quest_active, "qst_kidnapped_girl")' in start
    assert '(neg|check_quest_concluded, "qst_kidnapped_girl")' in start
    assert '(eq, ":cur_troop", "trp_kidnapped_girl")' in start

    for path in (
        "src/dialogs/ZD01_encounters_battles_and_prisoners/trp_kidnapped_girl_plyr_kidnapped_girl_liberated_battle.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/trp_kidnapped_girl_plyr_kidnapped_girl_liberated_battle_02.py",
    ):
        raw = read(path)
        assert '(check_quest_active, "qst_kidnapped_girl")' in raw
        assert '(neg|check_quest_concluded, "qst_kidnapped_girl")' in raw

    join = read("src/dialogs/ZD01_encounters_battles_and_prisoners/trp_kidnapped_girl_kidnapped_girl_liberated_battle_2a_02.py")
    assert '(party_add_members, "p_main_party", "trp_kidnapped_girl", 1)' in join
    assert "sod_companion_action_free_captives" in join
    assert '(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3)' in join

    assert_ordered(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/trp_kidnapped_girl_kidnapped_girl_liberated_battle_2b.py",
        (
            '(spawn_around_party, "p_main_party", "pt_kidnapped_girl")',
            '(assign, ":girl_party", reg0)',
            '(gt, ":girl_party", 0)',
            '(party_is_active, ":girl_party")',
            '(quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":girl_party")',
            '(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2)',
            "The rescued girl could not find a safe place on the map",
        ),
    )


def test_rescue_dialogue_typos_are_cleaned_up():
    spy_member = read("src/dialogs/ZZ99_misc_dialogs/trp_sh_spy_plyr_spy_chat_1.py")
    spy_start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_106.py")

    assert "When do I get my reward?" in spy_member
    assert "When I'll get my reward?" not in spy_member
    assert "Did the Serpent Host send you?" in spy_start
    assert "Did the Serpent Host sent you" not in spy_start


if __name__ == "__main__":
    test_kidnapped_girl_acceptance_requires_valid_bandit_party()
    test_serpent_spy_acceptance_requires_valid_militia_party()
    test_jotnar_clansmen_acceptance_requires_valid_slaver_party()
    test_jotnar_freed_clansmen_handoff_after_battle_is_guarded()
    test_jotnar_clansmen_completion_requires_actual_rescued_party()
    test_jotnar_clansmen_follow_response_requires_actual_rescue_party()
    test_serpent_spy_party_handoff_requires_actual_rescued_party()
    test_serpent_spy_follow_and_wait_responses_are_guarded()
    test_serpent_spy_battle_rescue_conversation_is_reachable_and_safe()
    test_kidnapped_girl_party_handoff_requires_actual_rescued_party()
    test_kidnapped_girl_battle_rescue_is_guarded_and_spawn_safe()
    test_rescue_dialogue_typos_are_cleaned_up()
    print("test_rescue_quest_spawn_guards_static: OK")
