from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_kidnapped_girl_ransom_pay_validates_spawn_before_charging_gold():
    raw = read("src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_bandits_awaiting_ransom_bandits_awaiting_ransom_pay.py")

    active_index = raw.index('(party_is_active, ":girl_party")')
    charge_index = raw.index('(call_script, "script_sod_player_charge_gold"')
    remove_index = raw.index('(party_remove_prisoners, ":quest_target_party", "trp_kidnapped_girl", 1)')
    target_index = raw.index('(quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":girl_party")')
    state_index = raw.index('(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2)')

    assert active_index < charge_index < remove_index < target_index < state_index
    assert '(check_quest_active, "qst_kidnapped_girl")' in raw
    assert '(neg|check_quest_concluded, "qst_kidnapped_girl")' in raw
    assert '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party")' in raw
    assert '(party_is_active, "$g_encountered_party")' in raw
    assert '(party_count_prisoners_of_type, ":girl_prisoners", ":quest_target_party", "trp_kidnapped_girl")' in raw
    assert "The kidnapped girl could not be placed on the map" in raw


def test_kidnapped_girl_ransom_bandit_dialogues_require_live_target_party():
    guarded_paths = (
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_bandits_awaiting_ransom_start.py",
        "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_bandits_awaiting_ransom_start_02.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_bandits_awaiting_ransom_plyr_bandits_awaiting_ransom_intro_1.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_bandits_awaiting_ransom_intro_1.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_bandits_awaiting_ransom_b.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_bandits_awaiting_ransom_b2.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_bandits_awaiting_ransom_b2_02.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_bandits_awaiting_ransom_b2_03.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_bandits_awaiting_ransom_no_money.py",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_bandits_awaiting_ransom_fight.py",
    )
    for path in guarded_paths:
        raw = read(path)
        assert '(check_quest_active, "qst_kidnapped_girl")' in raw
        assert '(neg|check_quest_concluded, "qst_kidnapped_girl")' in raw
        assert '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party")' in raw
        assert '(party_is_active, "$g_encountered_party")' in raw


def test_serpent_spy_ransom_pay_validates_spawn_before_charging_gold():
    raw = read("src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_militia_awaiting_ransom_militia_awaiting_ransom_pay.py")

    active_index = raw.index('(party_is_active, "$g_sh_spy")')
    charge_index = raw.index('(call_script, "script_sod_player_charge_gold"')
    state_index = raw.index('(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)')

    assert active_index < charge_index < state_index
    assert '(assign, "$g_sh_spy", 0)' in raw
    assert "The freed spy could not be placed on the map" in raw


def test_serpent_spy_fight_uses_battle_rescue_instead_of_pre_spawning_spy():
    raw = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_militia_awaiting_ransom_fight.py")

    assert "(encounter_attack)" in raw
    assert "pt_sh_spy" not in raw
    assert 'slot_quest_current_state, 1' not in raw
    count_index = raw.index('(party_count_prisoners_of_type, ":spy_prisoners", ":quest_target_party", "trp_sh_spy")')
    add_index = raw.index('(party_add_prisoners, ":quest_target_party", "trp_sh_spy", 1)')
    attack_index = raw.index("(encounter_attack)")
    assert count_index < add_index < attack_index


def test_player_patrol_split_validates_spawn_before_removing_companion():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_check_leadership.py")
    option = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_talk_02.py")
    denied = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_check_leadership_02.py")

    active_index = raw.index('(party_is_active, ":new_patrol")')
    remove_index = raw.index('(remove_member_from_party, ":soldier")')
    add_index = raw.index('(party_add_leader, ":new_patrol", ":soldier")')

    assert active_index < remove_index < add_index
    assert "Your soldier remains with you" in raw
    assert "I will take a patrol and keep close to the company." in raw
    assert "Take command of a patrol." in option
    assert "Become Party" not in option
    assert "field another patrol" in denied
    assert "lead additional parties" not in denied


if __name__ == "__main__":
    test_kidnapped_girl_ransom_pay_validates_spawn_before_charging_gold()
    test_kidnapped_girl_ransom_bandit_dialogues_require_live_target_party()
    test_serpent_spy_ransom_pay_validates_spawn_before_charging_gold()
    test_serpent_spy_fight_uses_battle_rescue_instead_of_pre_spawning_spy()
    test_player_patrol_split_validates_spawn_before_removing_companion()
    print("test_dialog_followup_spawn_guards_static: OK")
