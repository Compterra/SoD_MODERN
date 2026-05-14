from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_kidnapped_girl_ransom_pay_validates_spawn_before_charging_gold():
    raw = read("src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_bandits_awaiting_ransom_bandits_awaiting_ransom_pay.py")

    active_index = raw.index('(party_is_active, ":girl_party")')
    charge_index = raw.index('(call_script, "script_sod_player_charge_gold"')
    remove_index = raw.index('(remove_member_from_party, "trp_kidnapped_girl"')
    state_index = raw.index('(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2)')

    assert active_index < charge_index < remove_index < state_index
    assert "The kidnapped girl could not be placed on the map" in raw


def test_serpent_spy_ransom_pay_validates_spawn_before_charging_gold():
    raw = read("src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_militia_awaiting_ransom_militia_awaiting_ransom_pay.py")

    active_index = raw.index('(party_is_active, "$g_sh_spy")')
    charge_index = raw.index('(call_script, "script_sod_player_charge_gold"')
    state_index = raw.index('(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)')

    assert active_index < charge_index < state_index
    assert '(assign, "$g_sh_spy", 0)' in raw
    assert "The freed spy could not be placed on the map" in raw


def test_serpent_spy_fight_validates_spawn_before_advancing_quest():
    raw = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_militia_awaiting_ransom_fight.py")

    active_index = raw.index('(party_is_active, "$g_sh_spy")')
    state_index = raw.index('(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)')

    assert active_index < state_index
    assert '(assign, "$g_sh_spy", 0)' in raw
    assert "The fight can wait until the prisoner is located" in raw


def test_player_patrol_split_validates_spawn_before_removing_companion():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_check_leadership.py")

    active_index = raw.index('(party_is_active, ":new_patrol")')
    remove_index = raw.index('(remove_member_from_party, ":soldier")')
    add_index = raw.index('(party_add_leader, ":new_patrol", ":soldier")')

    assert active_index < remove_index < add_index
    assert "Your companion remains with you" in raw
