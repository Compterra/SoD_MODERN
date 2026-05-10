from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale generic dialogue remains: {token}"


def test_high_frequency_dialogue_openers_have_world_voice() -> None:
    checks = {
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_83.py": (
            "Our wheels are warm and the ledgers are open",
            "Yes? What do you want?",
        ),
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_133.py": (
            "grain, recruits, trouble on the road, or village need",
            "\"Good day, {sir/madam}.\",",
        ),
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_135.py": (
            "Prices are moving with the roads again",
            "Welcome {sir/madam}. What can I do for you?",
        ),
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_85.py": (
            "Prison stones hear enough lies",
            "Yes? What do you want?",
        ),
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_90.py": (
            "Gate is watched, chain is ready",
            "What do you want?",
        ),
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_36.py": (
            "sellswords under arms",
            "What do you want?",
        ),
    }
    for path, (new_line, stale_line) in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
        assert_not_contains(raw, stale_line)


def test_pretalk_loops_are_not_flat_anything_else_prompts() -> None:
    checks = {
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_pretalk.py": "The hall is still listening",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lady_pretalk.py": "before the room begins inventing stories",
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_jester_jester_else.py": "The court is briefly unmoored from consequence",
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_pretalk.py": "The map is still open",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
        assert_not_contains(raw, "Anything else?")


def test_special_faction_openers_keep_identity() -> None:
    checks = {
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_33.py": "The Serpent Host listens when ambition has teeth",
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_34.py": "my ledgers are hungry",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start_02.py": "The coffles are counted",
        "src/dialogs/ZA01_startup_and_dispatch/anyone_start_50.py": "The walls are awake",
    }
    for path, token in checks.items():
        assert_contains(read(path), token)


def test_economy_and_town_pretalk_loops_have_place_voice() -> None:
    checks = {
        "src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_pretalk.py": "The scales are still out",
        "src/dialogs/ZC01_centers_and_economy/anyone_merchant_pretalk.py": "The road does not wait long",
        "src/dialogs/ZC01_centers_and_economy/anyone_merchant_trade.py": "The counter is still open",
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_pretalk.py": "The village still has ears on us",
        "src/dialogs/ZC01_centers_and_economy/anyone_mayor_pretalk.py": "The town ledger is not closed",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_pretalk.py": "The cups are still wet",
        "src/dialogs/ZZ99_misc_dialogs/anyone_book_trade_completed.py": "A book leaves lighter than coin",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
        assert_not_contains(raw, "\"Anything else?\"")


def test_deserter_and_underworld_repeats_are_not_menu_skeletons() -> None:
    checks = {
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_deserters_start.py": "Your silver still buys you quiet",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_deserters_start.py": "Your silver still buys you quiet",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_merc_deserters_start.py": "Your silver still buys you quiet",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_ramun_the_slave_trader_ramun_pre_talk.py": "The chain has two ends",
        "src/dialogs/ZZ99_misc_dialogs/anyone_gm_pretalk.py": "The contract table is still open",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
        assert_not_contains(raw, "What do you want?\\")


def test_player_backout_lines_are_contextual_choices() -> None:
    checks = {
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_give_order_06.py": "Hold your men for now",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_suggest_raid_village_2.py": "Leave that village out of our plans",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_talk_ask_location_2.py": "I will find my bearings another way",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_demand_toll_2_02.py": "I will not dirty this road",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_recruit_decision_04.py": "Keep them with their families",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_trade_talk_03.py": "Keep the storehouse sealed",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavern_traveler_companion_location_ask_money_02.py": "Too steep for tavern smoke",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_castle_guard_players_02.py": "Keep your watch",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
        assert_not_contains(raw, "\"Never mind.\"")


def test_quest_facing_dialogue_has_stakes() -> None:
    checks = {
        "src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_requested_09.py": "No contract worth your steel",
        "src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_stall.py": "Come back before the chance spoils",
        "src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_taken.py": "I will mark your name beside the debt",
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_active_mission_3.py": "someone asks whether help is truly coming",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_active_mission_3.py": "My seal is on this business now",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_deliver_message_rejected.py": "A sealed word loses value",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_request_mission_ask.py": "Bring that matter to a clean end",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lady_ask_for_quest_05.py": "a cause worthy of being seen",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
    assert_not_contains(read("src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_requested_09.py"), "I am afraid I can't offer you a job right now")
    assert_not_contains(read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_raise_troops_rejected.py"), "good luck to you then")


def test_information_dialogue_reads_as_world_speech() -> None:
    checks = {
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective.py": "get out of these chains",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective_03.py": "Men mend faster near walls",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective_05.py": "A thin banner wins no battles",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective_07.py": "Burned stores speak loudly",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective_09.py": "hunger is patient",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective_13.py": "the order beneath it no longer sits cleanly",
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sa_select_3.py": "Choose the lens",
        "src/dialogs/ZZ99_misc_dialogs/anyone_trainer_combat_begin.py": "A bad habit learned here",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_dweller_talk_04.py": "What should an outsider know about this town?",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
    assert_not_contains(read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_objective_13.py"), "I don't know:")
    assert_not_contains(read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sa_select_3.py"), "What do you want to know about them?")


def test_support_npc_dialogue_has_role_voice() -> None:
    checks = {
        "src/dialogs/ZZ99_misc_dialogs/anyone_seneschal_pretalk.py": "household rolls are still open",
        "src/dialogs/ZZ99_misc_dialogs/anyone_member_castellan_pretalk.py": "The keys are still in my hand",
        "src/dialogs/ZZ99_misc_dialogs/anyone_mate_chat_pre_talk.py": "The detachment is waiting on your word",
        "src/dialogs/ZZ99_misc_dialogs/anyone_castle_gate_guard_pretalk.py": "The gate is still barred",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavern_traveler_pretalk.py": "more roads in my head",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_request_meeting_3.py": "Let the hall keep its secrets",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_bookseller_talk_02.py": "Keep the pages dry",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_talk.py": "Show me your skills and kit",
    }
    for path, new_line in checks.items():
        raw = read(path)
        assert_contains(raw, new_line)
    for path in (
        "src/dialogs/ZZ99_misc_dialogs/anyone_seneschal_pretalk.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_member_castellan_pretalk.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_mate_chat_pre_talk.py",
    ):
        assert_not_contains(read(path), "\"Anything else?\"")


def test_recent_companion_depth_lines_avoid_stage_direction_colons() -> None:
    stale_lines = {
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_lezalit.py": "Here are the Imperial notes:",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_nizar.py": "Here is the shape of it:",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_ymira.py": "This is the part that matters:",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_alayen.py": "no easy answer:",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_baheshtur.py": "The Unbroken Saddle is simple:",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_artimenner.py": "This is how men die:",
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_katrin.py": "Here it is, then:",
    }
    for path, stale_line in stale_lines.items():
        assert_not_contains(read(path), stale_line)


def test_seven_oaths_dialogue_keeps_craft_voice_and_personal_aftermath() -> None:
    craft_checks = {
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_garric_ashbow_aftermath.py": (
            "covered line",
            "I know the difference from range",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_oswin_ditchwright_aftermath.py": (
            "failure points",
            "works master",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sir_aldrik_vane_aftermath.py": (
            "public witness",
            "lawful terms",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mirelle_voss_aftermath.py": (
            "doors",
            "Tib",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_tomas_reed_aftermath.py": (
            "discipline",
            "cruelty",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_beren_hardhand_aftermath.py": (
            "bounded",
            "Halvorn",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_sister_elianor_aftermath.py": (
            "sanctuary",
            "wounded",
        ),
    }
    for path, tokens in craft_checks.items():
        raw = read(path)
        for token in tokens:
            assert_contains(raw, token)
        assert_not_contains(raw, "I will join you.")
        assert_not_contains(raw, "I will stay here.")
        assert_not_contains(raw, "I cannot join you.")
        assert_not_contains(raw, "Then I come.")
        assert_not_contains(raw, "parted with respect after Ashwick's defense")


def test_seven_oaths_campaign_text_avoids_implementation_language() -> None:
    board = read("src/menus/start_game/seven_ash_recruitment_map.py")
    council = read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_mother_hilda_oath_council.py")

    assert_not_contains(board, "not a place where recruitment resolves")
    assert_not_contains(board, "implementation slice")
    assert_not_contains(board, "campaign state")
    assert_not_contains(board, "dialogue and scenes")
    assert_contains(board, "No mark on it wins a defender")
    assert_contains(board, "where the next conversation waits")

    assert_not_contains(council, "Choose plainly")
    assert_not_contains(council, "Then homes")
    assert_not_contains(council, "Then we give")
    assert_not_contains(council, "Then Ashwick")
    assert_not_contains(council, "Then the village")


if __name__ == "__main__":
    test_high_frequency_dialogue_openers_have_world_voice()
    test_pretalk_loops_are_not_flat_anything_else_prompts()
    test_special_faction_openers_keep_identity()
    test_economy_and_town_pretalk_loops_have_place_voice()
    test_deserter_and_underworld_repeats_are_not_menu_skeletons()
    test_player_backout_lines_are_contextual_choices()
    test_quest_facing_dialogue_has_stakes()
    test_information_dialogue_reads_as_world_speech()
    test_support_npc_dialogue_has_role_voice()
    test_recent_companion_depth_lines_avoid_stage_direction_colons()
    test_seven_oaths_dialogue_keeps_craft_voice_and_personal_aftermath()
    test_seven_oaths_campaign_text_avoids_implementation_language()
    print("test_dialogue_immersion_static: OK")
