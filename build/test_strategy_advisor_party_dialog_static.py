from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    camp = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    council = read("src/menus/kingdom/talk_council_marshal.py")
    sa_council = read("src/menus/kingdom/sa_council.py")
    troop_tree_return = read("src/menus/other/troop_trees_prsenatation_end.py")

    member_chat = read("src/dialogs/ZA01_startup_and_dispatch/anyone_member_chat_04.py")
    member_talk_02 = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_talk_02.py")
    member_talk_03 = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_talk_03.py")
    member_talk_04 = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_talk_04.py")
    member_talk_05 = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_talk_05.py")

    start = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_start.py")
    event = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_event_triggered_02.py")
    siege_event = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_event_triggered.py")
    auto_start = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_auto_proceed_start.py")
    auto_event = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_auto_proceed_event_triggered.py")
    pretalk = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_pretalk.py")
    continue_ledgers = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_plyr_startegy_advisor_continue.py")

    sa_select_2 = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sa_select_2.py")
    sa_select_3 = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sa_select_3.py")
    sa_select_1_close = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_1_09.py")
    sa_select_2_close = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_2_answer_19.py")
    sa_select_3_time = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer.py")
    sa_select_3_service = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_02.py")
    troop_tree = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_03.py")
    sa_select_3_overview = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_04.py")
    sa_select_3_nobles = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_05.py")
    sa_select_3_melee_infantry = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_06.py")
    sa_select_3_ranged_infantry = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_07.py")
    sa_select_3_melee_cavalry = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_08.py")
    sa_select_3_ranged_cavalry = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_09.py")
    sa_select_3_commoners = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_10.py")
    sa_select_3_back = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sa_select_3_answer_11.py")

    war_room = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room.py")
    war_room_allies = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_allies.py")
    war_room_clock = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_clock.py")
    war_room_company = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_company.py")
    war_room_frontier = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_frontier.py")
    war_room_terror = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_terror.py")
    war_room_minifactions = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions.py")
    minifaction_slavers = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_slavers.py")
    minifaction_jotnar = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_jotnar.py")
    minifaction_elephant = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_elephant.py")
    minifaction_black_khergits = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_black_khergits.py")
    minifaction_boar = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_boar.py")
    minifaction_serpent = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_serpent.py")
    minifaction_black_army = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_black_army.py")
    war_room_back = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_answer_back.py")
    minifaction_back = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_back.py")
    last_order_open = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_last_order_opening_answer_open.py")
    last_order_wait = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_last_order_opening_answer_wait.py")
    last_order_rescue = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_after_rescue.py")

    assert_contains(camp, '("camp_strategy_advisor"')
    assert_contains(camp, '(main_party_has_troop, "trp_sod_strategy_advisor")')
    assert_contains(camp, '(assign, "$sa_talk_after_siege", 0)')
    assert_contains(camp, '(start_map_conversation, "trp_sod_strategy_advisor")')
    assert_contains(council, '(change_screen_map_conversation, "trp_sod_strategy_advisor")')
    assert_contains(council, '("talk_council_advisor", [')
    assert_contains(council, '(eq, "$g_sod_sa_in_court", 1)')
    assert_contains(sa_council, '(assign, "$g_sod_sa_in_court", 1)')
    assert_contains(sa_council, '(assign, "$sa_talk_after_siege", 0)')
    assert_contains(sa_council, '(party_remove_members, "p_main_party", "trp_sod_strategy_advisor", 1)')

    assert order.index("ZA01_startup_and_dispatch/anyone_member_chat_04.py") < order.index("ZA01_startup_and_dispatch/anyone_member_chat_06.py")
    assert order.index("ZA01_startup_and_dispatch/trp_sod_strategy_advisor_start.py") < order.index("ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_pretalk.py")
    assert order.index("ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_pretalk.py") < order.index("ZA01_startup_and_dispatch/trp_sod_strategy_advisor_plyr_startegy_advisor_continue.py")

    assert_contains(member_chat, '[trp_sod_strategy_advisor, "member_chat"')
    assert_contains(member_chat, '(main_party_has_troop, "trp_sod_strategy_advisor")')
    assert_contains(member_chat, '"startegy_advisor_continue"')
    assert_contains(member_chat, '(assign, "$sa_talk_after_siege", 0)')
    for blocked in [member_talk_02, member_talk_03, member_talk_04, member_talk_05]:
        assert_contains(blocked, '(neq, "$g_talk_troop", "trp_sod_strategy_advisor")')

    for entry in [start, event, auto_start, auto_event]:
        assert_contains(entry, '(this_or_next|main_party_has_troop, "trp_sod_strategy_advisor")')
        assert_contains(entry, '(eq, "$g_sod_sa_in_court", 1)')
    assert_contains(siege_event, '(main_party_has_troop, "trp_sod_strategy_advisor")')
    assert_contains(start, '"startegy_advisor_continue"')
    assert_contains(event, '"startegy_advisor_continue"')
    assert_contains(auto_start, '(assign, "$g_sod_player_asked_for_troop_tree", 0)')
    assert_contains(auto_start, '"sa_select_3"')
    assert_contains(auto_event, '(assign, "$g_sod_player_asked_for_troop_tree", 0)')
    assert_contains(auto_event, '"sa_select_3"')

    assert_contains(pretalk, '"startegy_advisor_continue"')
    assert_contains(continue_ledgers, '"Open the old campaign ledgers with me."')
    assert_contains(continue_ledgers, '"sa_select_1"')
    assert_contains(sa_select_2, "Narrow the ledger. Which people do you mean?")
    assert_not_contains(sa_select_2, '"Which?"')
    assert_contains(sa_select_3, "Choose the lens.")
    assert_contains(sa_select_1_close, "Close the ledgers for now.")
    assert_contains(sa_select_1_close, '"sod_sa_pretalk"')
    assert_contains(sa_select_2_close, "Leave that ledger closed.")
    assert_contains(sa_select_3_time, "Estimate when the Imperial Legion will arrive.")
    assert_not_contains(sa_select_3_time, "Tell me estimate time")
    assert_contains(sa_select_3_service, "Open your own Legion years")
    assert_contains(troop_tree, "Lay out their divisions and ranks")
    assert_contains(sa_select_3_overview, "Give me the field overview first.")
    assert_contains(sa_select_3_nobles, "What do their nobles bring to the field?")
    assert_contains(sa_select_3_melee_infantry, "Mark their close infantry for me.")
    assert_contains(sa_select_3_ranged_infantry, "Where do their foot archers and missile troops matter?")
    assert_contains(sa_select_3_melee_cavalry, "Show me the weight and weakness of their shock cavalry.")
    assert_contains(sa_select_3_ranged_cavalry, "How should we read their mounted skirmishers?")
    assert_contains(sa_select_3_commoners, "protect them and still draw strength from them")
    for polished in [
        sa_select_3_service,
        troop_tree,
        sa_select_3_nobles,
        sa_select_3_melee_infantry,
        sa_select_3_ranged_infantry,
        sa_select_3_melee_cavalry,
        sa_select_3_ranged_cavalry,
    ]:
        assert_not_contains(polished, "Tell me about")
    assert_not_contains(troop_tree, "break out their divisions")
    assert_contains(sa_select_3_back, "That is enough of the ledgers for now.")
    assert_not_contains(sa_select_1_close, "Nevermind.")
    assert_not_contains(sa_select_2_close, "Nevermind.")
    assert_not_contains(sa_select_3_back, "Nevermind.")

    assert_contains(troop_tree, '(assign, "$g_sod_player_asked_for_troop_tree", 1)')
    assert_contains(troop_tree, '(finish_mission)')
    assert_contains(troop_tree, '(jump_to_menu, "mnu_troop_trees_prsenatation")')
    assert_contains(troop_tree_return, '(eq, "$g_sod_sa_in_court", 0)')
    assert_contains(troop_tree_return, '(start_map_conversation, "trp_sod_strategy_advisor")')
    assert_contains(troop_tree_return, '(change_screen_map_conversation, "trp_sod_strategy_advisor")')

    assert_contains(war_room, '"sod_sa_war_room_answer"')
    assert_contains(war_room_back, '"sod_sa_pretalk"')
    assert_contains(minifaction_back, '"sod_sa_war_room"')
    for answer in [war_room_allies, war_room_clock, war_room_company, war_room_frontier, war_room_terror]:
        assert_contains(answer, '"sod_sa_war_room"')
    assert_contains(war_room_minifactions, '"sod_sa_war_room_minifactions_answer"')
    for answer in [
        minifaction_slavers,
        minifaction_jotnar,
        minifaction_elephant,
        minifaction_black_khergits,
        minifaction_boar,
        minifaction_serpent,
        minifaction_black_army,
    ]:
        assert_contains(answer, '"sod_sa_war_room_minifactions_answer"')
    assert_contains(last_order_open, '"sod_sa_last_order_network"')
    assert_contains(last_order_wait, '"sod_sa_pretalk"')
    assert_not_contains(last_order_rescue, "Very well.")

    for path in [
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_war_room.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_father.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_calradia.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_name.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_loyalty.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_father_mistakes.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_trust.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_last_order_opening.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_last_order_active.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_last_order_after.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_imperial_victory.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_centurion_death.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_alliance_victory.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_ruthless_victory.py",
        "trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_final_closure.py",
    ]:
        assert_contains(order, path)

    print("test_strategy_advisor_party_dialog_static: OK")


if __name__ == "__main__":
    main()
