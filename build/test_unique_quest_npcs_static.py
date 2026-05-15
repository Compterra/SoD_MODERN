from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def test_unique_quest_npc_dialogues_are_registered() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    for token in (
        "trp_fugitive_fugitive_2.py",
        "trp_fugitive2_fugitive_22.py",
        "trp_kidnapped_girl_kidnapped_girl_chat_2.py",
        "anyone_kidnapped_girl_join.py",
        "anyone_kidnapped_girl_wait.py",
        "trp_kidnapped_girl_kidnapped_girl_liberated_battle_2b.py",
        "party_tpl_pt_runaway_slaves_runaway_slave_go_back.py",
        "anyone_runaway_slave_let_go.py",
        "trp_slave_hero_start.py",
        "trp_slave_hero_start_02.py",
        "trp_wine_recipient_event_triggered.py",
    ):
        assert_contains(order, token)


def test_fugitive_denials_are_not_generic_placeholder_lines() -> None:
    first = read("src/dialogs/ZE01_companions_and_named_npcs/trp_fugitive_fugitive_2.py")
    second = read("src/dialogs/ZE01_companions_and_named_npcs/trp_fugitive2_fugitive_22.py")
    assert_contains(first, "That name gets men killed")
    assert_contains(second, "If a lord wants blood")
    assert_not_contains(first + second, "I assure you, I am just one of the dwellers here")


def test_runaway_slave_return_uses_slaver_quest_target() -> None:
    raw = read("src/dialogs/ZZ99_misc_dialogs/party_tpl_pt_runaway_slaves_runaway_slave_go_back.py")
    assert_contains(raw, "qst_slavers_bring_back_runaway_slaves")
    assert_not_contains(raw, "qst_bring_back_runaway_serfs")
    assert_contains(raw, "sod_slaver_action_return_runaways")


def test_freed_runaway_slaves_choose_a_valid_fallback_village() -> None:
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_runaway_slave_let_go.py")
    assert_contains(raw, "script_get_closest_village")
    assert_contains(raw, "neg|is_between")
    assert_contains(raw, "villages_begin")
    assert_contains(raw, "sod_slaver_action_free_runaways")


def test_named_quest_actor_lines_keep_their_quest_surfaces() -> None:
    diego = read("src/dialogs/ZA01_startup_and_dispatch/trp_slave_hero_start.py")
    diego_return = read("src/dialogs/ZA01_startup_and_dispatch/trp_slave_hero_start_02.py")
    wine = read("src/dialogs/ZA01_startup_and_dispatch/trp_wine_recipient_event_triggered.py")
    kidnapped = read("src/dialogs/ZE01_companions_and_named_npcs/trp_kidnapped_girl_kidnapped_girl_chat_2.py")
    assert_contains(diego, "qst_slave_q1")
    assert_contains(diego, "The slavers count chains")
    assert_contains(diego_return, "did {s13} remember the old debt")
    assert_contains(wine, "qst_slavers_deliver_wine")
    assert_contains(wine, "Wine travels badly")
    assert_contains(kidnapped, "get me home")


def test_diego_secret_quest_has_idempotent_start_guards() -> None:
    start = read("src/dialogs/ZA01_startup_and_dispatch/trp_slave_hero_start.py")
    followup = read("src/dialogs/ZA01_startup_and_dispatch/trp_slave_hero_start_02.py")
    accepted = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_prison_break_2_accepted.py")
    refusal = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prison_break_2_9_02.py")
    for token in (
        'neg|check_quest_active, "qst_slave_q1"',
        'neg|check_quest_active, "qst_slave_q2"',
        'neg|check_quest_active, "qst_slave_q3"',
        'neg|check_quest_succeeded, "qst_slave_q3"',
        'neg|check_quest_failed, "qst_slave_q3"',
    ):
        assert_contains(start, token)
    assert_contains(followup, 'check_quest_active, "qst_slave_q2"')
    assert_contains(accepted, 'check_quest_active, "qst_slave_q2"')
    assert_contains(accepted, 'neg|check_quest_active, "qst_slave_q3"')
    assert_contains(refusal, 'script_fail_quest", "qst_slave_q2"')
    assert_contains(refusal, 'script_end_quest", "qst_slave_q2"')


def test_diego_becomes_unique_non_tavern_companion_after_success() -> None:
    troops = read("compile/module_troops.py")
    mission = read("src/mission_templates/0024_prison_break/prison_break.py")
    taverns = read("src/scripts/ZH_heroes/update_companion_candidates_in_taverns.py")
    constants = read("src/constants/module_constants.py")
    assert_contains(troops, '"diego_companion"')
    assert_contains(troops, '"Diego"')
    assert_contains(troops, "tf_hero|tf_unmoveable_in_party_window")
    assert_contains(troops, "itm_slave_neck_chain")
    assert_contains(mission, 'script_sod_special_companion_recruit", "trp_diego_companion", 60, sod_companion_role_spymaster')
    assert_contains(mission, 'neg|main_party_has_troop, "trp_diego_companion"')
    assert_contains(mission, 'script_sod_quest_dialogue_record_event", "qst_slave_q3", "trp_diego_companion"')
    assert_contains(mission, 'script_sod_quest_journal_update')
    assert_contains(constants, 'companions_end = "trp_diego_companion"')
    assert_contains(constants, 'special_companions_begin = "trp_diego_companion"')
    assert_contains(constants, 'special_companions_end = "trp_kingdom_heroes_including_player_begin"')
    assert_not_contains(taverns, "trp_diego_companion")


def test_diego_has_post_rescue_dialogue_and_slaver_reactions() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    slavers = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    for token in (
        "trp_diego_companion_member_chat.py",
        "trp_diego_companion_plyr_talk_about.py",
        "trp_diego_companion_about.py",
        "trp_diego_companion_plyr_role.py",
        "trp_diego_companion_role.py",
        "trp_diego_companion_plyr_chainbreaker.py",
        "trp_diego_companion_chainbreaker.py",
        "trp_diego_companion_plyr_warning.py",
        "trp_diego_companion_warning.py",
        "trp_diego_companion_plyr_reconcile.py",
        "trp_diego_companion_reconcile.py",
        "trp_diego_companion_plyr_late_reflection.py",
        "trp_diego_companion_late_reflection.py",
        "trp_diego_companion_plyr_leave.py",
        "trp_diego_companion_departure_confirm.py",
        "trp_diego_companion_plyr_departure_confirm_yes.py",
        "trp_diego_companion_plyr_departure_confirm_no.py",
        "trp_diego_companion_departure.py",
        "anyone_plyr_ransom_broker_find_diego.py",
        "anyone_ransom_broker_find_diego.py",
    ):
        assert_contains(order, token)
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/trp_diego_companion_member_chat.py"), "long memory for chains")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_chainbreaker.py"), "slot_faction_slaver_market_heat")
    assert_contains(slavers, "Diego helps the runaways scatter")
    assert_contains(slavers, "Diego says buying chains")
    assert_contains(slavers, "Diego walks the broken Slaver line")
    assert_contains(slavers, "slot_troop_companion_approval")
    assert_contains(slavers, "$g_sod_diego_warning_pending")
    assert_contains(slavers, "$g_sod_diego_anti_slaver_proof")
    assert_contains(slavers, "trp_refugee")
    assert_contains(slavers, "chainbreaker_chance")
    assert_contains(slavers, '(ge, ":diego_approval", 45)')
    assert_contains(slavers, "keeps the freed moving away from your banner")
    assert_contains(slavers, "Trust will take more than one broken lock")
    assert_contains(slavers, 'troop_slot_eq, "trp_diego_companion", slot_troop_companion_role, sod_companion_role_spymaster')
    assert_contains(slavers, '(val_min, ":chainbreaker_chance", 40)')
    assert_contains(slavers, "slot_troop_companion_trust_tier")
    if slavers.count('(call_script, "script_sod_companion_get_approval_band_to_reg", "trp_diego_companion")') < 7:
        raise AssertionError("Diego Slaver reactions must refresh cached trust tier after approval changes")
    assert_contains(slavers, 'main_party_has_troop, "trp_diego_companion"')
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_warning.py"), "A chain bought cleanly")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_reconcile.py"), "Cages opened")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_late_reflection.py"), "Counting names")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_role.py"), "Put me near prisoners")
    assert_contains(read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_ransom_broker_diego_watch.py"), "counts keys")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_departure.py"), "script_sod_diego_cleanup_departure")
    assert_contains(read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_ransom_broker_find_diego.py"), "script_sod_diego_rejoin_from_underroad")
    depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    campfire = read("src/menus/camp/companion_campfire.py")
    assert_contains(depth, "sod_diego_companion_describe_to_s34")
    assert_contains(depth, "His Chainbreaker work")
    assert_contains(depth, "Chainbreaker work is disabled")
    assert_contains(depth, "Lezalit's talk of discipline")
    assert_contains(depth, "Marnid's ledgers")
    assert_contains(depth, "sod_diego_cleanup_departure")
    assert_contains(depth, "sod_diego_rejoin_from_underroad")
    assert_contains(depth, "sod_special_companion_process_daily")
    assert_contains(depth, "sod_special_companion_apply_player_action")
    assert_contains(depth, "sod_special_companion_recruit")
    assert_contains(depth, "sod_special_companion_role_eligibility_to_reg")
    assert_contains(depth, "sod_companion_action_elephant_guard_support")
    assert_contains(depth, "sod_companion_action_jotnar_support")
    assert_contains(depth, "sod_companion_action_defeat_imperials")
    assert_contains(depth, "sod_companion_action_abuse_village")
    assert_contains(depth, "sod_companion_action_threatened_troops")
    assert_contains(depth, "sod_companion_action_execute_lord")
    assert_contains(depth, "sod_companion_role_spymaster")
    assert_contains(depth, "special_companions_begin")
    assert_contains(depth, "special_companions_end")
    assert_contains(depth, 'script_recruit_troop_as_companion", ":companion"')
    assert_contains(depth, 'troop_set_slot, "trp_diego_companion", slot_troop_playerparty_history, pp_history_dismissed')
    assert_contains(depth, 'troop_set_slot, "trp_diego_companion", slot_troop_playerparty_history, pp_history_indeterminate')
    assert_contains(depth, "{s16}{s34}")
    assert_not_contains(campfire, "companion_campfire_diego_chainbreaker")
    assert_not_contains(campfire, "Ask Diego to watch for captives")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/trp_diego_companion_plyr_chainbreaker.py"), "How do we hurt the Slaver web?")


def test_special_companion_static_safety_rules_for_diego() -> None:
    troops = read("compile/module_troops.py")
    mission = read("src/mission_templates/0024_prison_break/prison_break.py")
    taverns = read("src/scripts/ZH_heroes/update_companion_candidates_in_taverns.py")
    dialogs = read("src/dialogs/_order_dialogs.txt")
    notes = read("src/scripts/ZH_heroes/update_troop_notes.py")
    locations = read("src/scripts/ZH_heroes/update_troop_location_notes.py")
    assert_contains(troops, '"slave_hero"')
    assert_contains(troops, '"slave_hero", "One-Eyed Slave", "One-Eyed Slave", tf_hero|tf_inactive')
    assert_contains(troops, '"diego_companion"')
    assert_contains(mission, 'neg|main_party_has_troop, "trp_diego_companion"')
    assert_contains(mission, 'script_sod_special_companion_recruit", "trp_diego_companion"')
    assert_not_contains(taverns, "trp_diego_companion")
    assert_contains(dialogs, "trp_slave_hero_start.py")
    assert_contains(dialogs, "trp_diego_companion_member_chat.py")
    assert_contains(notes, '(eq, ":troop_no", "trp_slave_hero")')
    assert_contains(notes, '(add_troop_note_from_sreg, ":troop_no", 0, s49, 0)')
    assert_contains(notes, '(add_troop_note_from_sreg, ":troop_no", 1, s49, 0)')
    assert_contains(notes, '(add_troop_note_from_sreg, ":troop_no", 2, s49, 0)')
    assert_contains(locations, '(eq, ":troop_no", "trp_slave_hero")')
    assert_contains(locations, '(add_troop_note_from_sreg, ":troop_no", 2, s49, 0)')


def test_kidnapped_girl_no_room_preserves_quest_party_identity() -> None:
    map_join = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_kidnapped_girl_join.py")
    map_wait = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_kidnapped_girl_wait.py")
    troop_no_room = read("src/dialogs/ZE01_companions_and_named_npcs/trp_kidnapped_girl_kidnapped_girl_liberated_map_2a.py")
    troop_wait = read("src/dialogs/ZE01_companions_and_named_npcs/trp_kidnapped_girl_kidnapped_girl_liberated_map_2b.py")
    for raw in (map_join, map_wait, troop_no_room, troop_wait):
        assert_contains(raw, "party_set_icon")
        assert_contains(raw, "icon_woman")
        assert_contains(raw, "ai_bhvr_hold")
        assert_contains(raw, "slot_quest_target_party")
        assert_contains(raw, "slot_quest_current_state, 2")


def test_battle_no_room_respawns_kidnapped_girl_party_not_companion_party() -> None:
    raw = read("src/dialogs/ZD01_encounters_battles_and_prisoners/trp_kidnapped_girl_kidnapped_girl_liberated_battle_2b.py")
    assert_contains(raw, "spawn_around_party")
    assert_contains(raw, "pt_kidnapped_girl")
    assert_contains(raw, "icon_woman")
    assert_contains(raw, "slot_quest_target_party")
    assert_contains(raw, "slot_quest_current_state, 2")
    assert_not_contains(raw, "add_companion_party")
