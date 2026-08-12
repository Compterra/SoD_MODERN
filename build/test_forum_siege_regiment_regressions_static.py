from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_construction_report_has_own_menu_line():
    text = read("src/scripts/ZB_economy_and_trade/describe_current_project.py")
    assert "@^Construction:" in text
    assert "@You are currently developing" not in text


def test_inside_siege_option_uses_current_center_faction_and_not_second_party_gate():
    text = read("src/menus/centers/castle/castle_castle.py")
    marker = '("town_start_siege_from_inside"'
    block = text[text.index(marker):text.index('("town_leave"', text.index(marker))]
    assert '(call_script, "script_cf_sod_center_player_can_start_siege", "$current_town")' in block
    assert '(store_faction_of_party, ":center_faction", "$current_town")' in block
    assert '(store_relation, ":center_relation", ":center_faction", "fac_player_supporters_faction")' in block
    assert '(this_or_next|neq, ":center_faction", "$players_kingdom")' in block
    assert '(lt, ":center_relation", 0)' in block
    assert '(neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player")' in block
    assert '(assign, "$g_encountered_party", "$current_town")' in block
    assert '(assign, "$g_encountered_party_faction", ":center_faction")' in block
    assert '(lt, "$g_encountered_party_2", 1)' not in block
    assert '(store_faction_of_party, ":center_faction", "$g_encountered_party")' not in block
    assert '(neq, ":center_faction", "$players_kingdom")' not in block


def test_gate_siege_option_not_blocked_by_unrelated_second_party():
    text = read("src/menus/centers/common/approach_gates.py")
    marker = '("castle_start_siege"'
    block = text[text.index(marker):text.index('("castle_leave"', text.index(marker))]
    assert '(call_script, "script_cf_sod_center_player_can_start_siege", "$g_encountered_party")' in block
    assert '(store_faction_of_party, ":center_faction", "$g_encountered_party")' in block
    assert '(store_relation, ":center_relation", ":center_faction", "fac_player_supporters_faction")' in block
    assert '(this_or_next|neq, ":center_faction", "$players_kingdom")' in block
    assert '(lt, ":center_relation", 0)' in block
    assert '(neg|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")' in block
    assert '(assign, "$g_encountered_party_faction", ":center_faction")' in block
    assert '(lt, "$g_encountered_party_2", 1)' not in block
    assert '(neq, ":center_faction", "$players_kingdom")' not in block


def test_siege_option_recovers_stale_besieger_slots():
    text = read("src/scripts/ZD_centers/cf_sod_center_player_can_start_siege.py")
    assert '(is_between, ":center_no", walled_centers_begin, walled_centers_end)' in text
    assert '(lt, ":siege_party", -1)' in text
    assert '(neg|party_is_active, ":siege_party")' in text
    assert '(party_slot_eq, ":siege_party", slot_party_ai_state, spai_besieging_center)' in text
    assert '(party_slot_eq, ":siege_party", slot_party_ai_object, ":center_no")' in text
    assert '(party_get_battle_opponent, ":siege_opponent", ":siege_party")' in text
    assert '(party_set_slot, ":center_no", slot_center_is_besieged_by, -1)' in text
    assert '(this_or_next|faction_slot_eq, ":siege_party_faction", slot_faction_marshall, "trp_player")' in text


def test_starved_sieges_eventually_force_surrender():
    text = read("src/menus/centers/castle/siege_request_meeting.py")
    assert "slot_center_siege_begin_hours" in text
    assert '(ge, ":siege_days", 30)' in text
    assert '(assign, "$g_enemy_surrenders", 1)' in text
    assert "can no longer refuse terms" in text


def test_regiment_reorganization_does_not_trim_party_on_exchange_open():
    text = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_chat_talk_02.py")
    assert "(change_screen_exchange_members, 0)" in text
    assert "script_cf_fix_party_size" not in text
    assert "allowed party size" not in text

