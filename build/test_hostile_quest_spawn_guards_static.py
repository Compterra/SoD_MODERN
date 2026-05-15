from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_validates_spawn_before_start(raw, start_token):
    active_index = raw.index('(party_is_active, ":quest_target_party")')
    start_index = raw.index(start_token)
    assert active_index < start_index


def assert_ordered(raw, tokens):
    position = -1
    for token in tokens:
        next_position = raw.find(token, position + 1)
        assert next_position != -1, f"Missing token after offset {position}: {token}"
        position = next_position


def test_standard_troublesome_bandits_spawn_is_guarded():
    raw = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_troublesome_bandits_quest_brief.py")

    assert '(spawn_around_party, ":quest_giver_center", "pt_troublesome_bandits")' in raw
    assert '(assign, ":quest_target_party", reg0)' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert "The troublesome bandits could not be placed on the map" in raw
    assert_validates_spawn_before_start(raw, '(call_script, "script_start_quest", "qst_troublesome_bandits"')
    assert raw.index('(party_is_active, ":quest_target_party")') < raw.index('(quest_set_slot, "qst_troublesome_bandits", slot_quest_target_party')


def test_guild_troublesome_bandits_spawn_is_guarded():
    raw = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_gm_troublesome_bandits_quest_brief.py")

    assert '(spawn_around_party, ":merc_base", ":p_template")' in raw
    assert '(assign, ":quest_target_party", reg0)' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert "The guild target could not be placed on the map" in raw
    assert_validates_spawn_before_start(raw, '(call_script, "script_start_quest", "$random_quest_no"')
    assert raw.index('(party_is_active, ":quest_target_party")') < raw.index('(party_add_members, ":quest_target_party"')


def test_elephant_guard_bastard_spawn_is_guarded():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_bastard_quest_brief.py")

    assert '(spawn_around_party, reg3, "pt_ravaging_bandits")' in raw
    assert '(assign, ":cur_party", reg0)' in raw
    assert '(gt, ":cur_party", 0)' in raw
    assert '(party_is_active, ":cur_party")' in raw
    assert "The Khergit chieftain could not be placed on the map" in raw
    assert raw.index('(party_is_active, ":cur_party")') < raw.index('(party_add_members, ":cur_party", "trp_khergit_chieftain"')
    assert raw.index('(party_is_active, ":cur_party")') < raw.index('(call_script, "script_start_quest", "qst_elephant_guard_capture_the_bastard"')
    assert "I'll find this bastard and bring him to you." in raw
    assert "I'll fing this bastard" not in raw


def test_jotnar_aid_warband_spawn_is_guarded():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_jc_aid_warband_quest_brief.py")

    assert '(spawn_around_party, ":quest_target_center", "pt_jotnar_clan_warriors")' in raw
    assert '(assign, ":quest_target_party", reg0)' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert "The Jotnar warband could not be placed on the map" in raw
    assert raw.index('(party_is_active, ":quest_target_party")') < raw.index('(quest_set_slot, "qst_jotnar_clan_aid_warband", slot_quest_target_party')
    assert_validates_spawn_before_start(raw, '(call_script, "script_start_quest", "$random_quest_no"')
    assert raw.index('(str_store_party_name_link, s8, ":quest_target_center")') < raw.index('(str_store_string, s2, "@{s9} asked you to help Jotnar Clan warriors garrisoned near {s8}.")')


def test_jotnar_aid_warband_result_menu_resolves_once_from_continue():
    raw = read("src/menus/other/continue_26.py")

    option_start = raw.index('("continue"')
    condition_block = raw[:option_start]
    continue_option = raw[option_start:]

    assert "The enemy breaks. The Jotnar warriors hold the field" in condition_block
    assert "(change_screen_map)" not in condition_block
    assert '(call_script, "script_succeed_quest", "qst_jotnar_clan_aid_warband")' not in condition_block
    assert_ordered(
        continue_option,
        [
            '(try_begin)',
            '(eq, "$g_battle_result", 1)',
            '(call_script, "script_succeed_quest", "qst_jotnar_clan_aid_warband")',
            '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_jotnar_support, 2)',
            '(else_try)',
            '(call_script, "script_fail_quest", "qst_jotnar_clan_aid_warband")',
            '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_retreat_or_fail, 1)',
            '(try_end)',
            '(change_screen_map)',
        ],
    )


if __name__ == "__main__":
    test_standard_troublesome_bandits_spawn_is_guarded()
    test_guild_troublesome_bandits_spawn_is_guarded()
    test_elephant_guard_bastard_spawn_is_guarded()
    test_jotnar_aid_warband_spawn_is_guarded()
    test_jotnar_aid_warband_result_menu_resolves_once_from_continue()
    print("test_hostile_quest_spawn_guards_static: OK")
