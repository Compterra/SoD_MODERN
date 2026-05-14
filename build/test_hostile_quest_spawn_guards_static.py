from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_validates_spawn_before_start(raw, start_token):
    active_index = raw.index('(party_is_active, ":quest_target_party")')
    start_index = raw.index(start_token)
    assert active_index < start_index


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


def test_jotnar_aid_warband_spawn_is_guarded():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_jc_aid_warband_quest_brief.py")

    assert '(spawn_around_party, ":quest_target_center", "pt_jotnar_clan_warriors")' in raw
    assert '(assign, ":quest_target_party", reg0)' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert "The Jotnar warband could not be placed on the map" in raw
    assert raw.index('(party_is_active, ":quest_target_party")') < raw.index('(quest_set_slot, "qst_jotnar_clan_aid_warband", slot_quest_target_party')
    assert_validates_spawn_before_start(raw, '(call_script, "script_start_quest", "$random_quest_no"')
