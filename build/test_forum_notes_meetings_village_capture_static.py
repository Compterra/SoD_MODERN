from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_threat_level_no_longer_prints_weekly_debug_warning():
    text = read("src/scripts/ZD_centers/get_center_threat_level.py")
    assert "display_log_message" not in text
    assert "ignored a non-center argument" not in text


def test_faction_notes_do_not_iterate_over_kingdom_heroes_sentinel():
    text = read("src/scripts/ZF_factions/update_faction_notes.py")
    assert 'try_for_range_backwards, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end' in text
    assert 'try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", kingdom_heroes_end' not in text
    assert '(call_script, "script_store_troop_name_link", s10, "trp_player")' in text


def test_lord_meetings_use_safe_conversation_scene_setup():
    accepted = read("src/dialogs/ZZ99_misc_dialogs/anyone_request_meeting_6.py")
    castle_lord = read("src/dialogs/ZZ99_misc_dialogs/anyone_request_meeting_castle_lord.py")
    assert "script_setup_troop_meeting" in accepted
    assert "script_setup_troop_meeting" in castle_lord
    assert '(call_script, "script_store_troop_name", s2, "$lord_requested_to_talk_to")' in accepted


def test_capture_pool_uses_wounded_enemy_companions_for_captives():
    helper = read("src/scripts/ZC_parties/party_prisoners_add_wounded_party_companions.py")
    capture = read("src/scripts/ZC_parties/total_victory_prepare_capture_pool.py")
    assert "party_stack_get_num_wounded" in helper
    assert '(gt, ":num_wounded", 0)' in helper
    assert "script_party_prisoners_add_wounded_party_companions" in capture
    assert "script_party_prisoners_add_party_companions" not in capture


def test_village_bandit_attack_not_hidden_by_special_quest_overlap():
    text = read("src/menus/centers/village/recruit_volunteers.py")
    marker = '("village_attack_bandits"'
    block = text[text.index(marker):text.index('("black_army_attack"', text.index(marker))]
    assert "qst_black_army_aid_warband" not in block
    assert "qst_slavers_deal_with_good_guys" not in block
    assert "qst_jotnar_clan_revenge" not in block
    assert "slot_village_infested_by_bandits" in block

