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
