from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def test_conquistador_horse_turnin_removes_the_counted_alternate_horse() -> None:
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_deliver_horses_thank.py")
    counted = '(call_script, "script_get_troop_item_amount", "trp_player", "itm_rok_saddle_horse2")'
    remove_full = '(troop_remove_items, "trp_player", "itm_rok_saddle_horse2", ":remaining")'
    remove_partial = '(troop_remove_items, "trp_player", "itm_rok_saddle_horse2", reg0)'
    wrong = '(troop_remove_items, "trp_player", "itm_steppe_horse_b", ":remaining")'

    for token in (counted, remove_full, remove_partial):
        assert token in raw
    assert wrong not in raw[raw.index(counted) :]
    assert raw.index(counted) < raw.index(remove_full) < raw.index(remove_partial)


def test_conquistador_horse_turnin_does_not_depend_on_stale_reg5_for_reward() -> None:
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_deliver_horses_thank.py")
    amount = '(quest_get_slot, ":quest_target_amount", "$g_gm_quest", slot_quest_target_amount)'
    remaining = '(assign, ":remaining", ":quest_target_amount")'
    complete_guard = '(eq, ":remaining", 0)'
    reward = '(troop_add_gold, "trp_player", ":quest_gold_reward")'
    succeed = '(call_script, "script_succeed_quest", "$g_gm_quest")'
    fail_message = "could not be completed because the required mounts were no longer"

    for token in (amount, remaining, complete_guard, reward, succeed, fail_message):
        assert token in raw
    assert raw.index(amount) < raw.index(remaining) < raw.index(complete_guard)
    assert raw.index(complete_guard) < raw.index(reward) < raw.index(succeed)
    assert 'reg5)' not in raw


def test_bc_prisoner_turnin_removes_prisoners_and_pays_atomically() -> None:
    player_line = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_02.py")
    reward_line = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_gm_qst_bc_capture_prisoners.py")

    active = '(check_quest_active, "qst_bc_capture_prisoners")'
    count = '(party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop")'
    enough = '(ge, ":count_prisoners", ":quest_target_amount")'
    remove = '(party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount")'
    reward = '(call_script, "script_troop_add_gold", "trp_player", ":gold")'
    succeed = '(call_script, "script_succeed_quest", "qst_bc_capture_prisoners")'
    stale_message = "could not be completed because the required captives were no longer"

    assert active in player_line
    assert remove not in player_line
    for token in (active, count, enough, remove, reward, succeed, stale_message):
        assert token in reward_line
    assert reward_line.index(active) < reward_line.index(count) < reward_line.index(enough)
    assert reward_line.index(enough) < reward_line.index(remove) < reward_line.index(reward)
    assert reward_line.index(reward) < reward_line.index(succeed)


def test_guild_grain_turnin_rechecks_inventory_before_reward() -> None:
    player_line = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_04.py")
    reward_line = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_deliver_grain_thank.py")

    active = '(check_quest_active, "$g_gm_quest")'
    count = '(call_script, "script_get_troop_item_amount", "trp_player", ":quest_target_item")'
    enough = '(ge, reg0, ":quest_target_amount")'
    remove = '(troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount")'
    reward = '(troop_add_gold, "trp_player", ":quest_reward")'
    succeed = '(call_script, "script_succeed_quest", "$g_gm_quest")'
    stale_message = "could not be completed because the required goods were no longer"

    assert active in player_line
    for token in (active, count, enough, remove, reward, succeed, stale_message):
        assert token in reward_line
    assert reward_line.index(count) < reward_line.index(active) < reward_line.index(enough)
    assert reward_line.index(enough) < reward_line.index(remove) < reward_line.index(reward)
    assert reward_line.index(reward) < reward_line.index(succeed)


def test_guild_raise_troops_turnin_rechecks_party_before_reward() -> None:
    player_line = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_07.py")
    reward_line = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_raise_troops_thank.py")

    active = '(check_quest_active, "$g_gm_quest")'
    count = '(party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop")'
    enough = '(ge, ":num_companions", ":quest_target_amount")'
    remove = '(party_remove_members, "p_main_party", ":quest_target_troop", ":quest_target_amount")'
    reward = '(troop_add_gold, "trp_player", 500)'
    succeed = '(call_script, "script_succeed_quest", "$g_gm_quest")'
    stale_message = "could not be completed because the required soldiers were no longer"

    assert active in player_line
    for token in (active, count, enough, remove, reward, succeed, stale_message):
        assert token in reward_line
    assert reward_line.index(count) < reward_line.index(active) < reward_line.index(enough)
    assert reward_line.index(enough) < reward_line.index(remove) < reward_line.index(succeed)
    assert reward_line.index(succeed) < reward_line.index(reward)
