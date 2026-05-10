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
    assert '(store_faction_of_party, ":center_faction", "$current_town")' in block
    assert '(lt, "$g_encountered_party_2", 1)' not in block
    assert '"$g_encountered_party_faction"' not in block


def test_gate_siege_option_not_blocked_by_unrelated_second_party():
    text = read("src/menus/centers/common/approach_gates.py")
    marker = '("castle_start_siege"'
    block = text[text.index(marker):text.index('("castle_leave"', text.index(marker))]
    assert '(store_faction_of_party, ":center_faction", "$g_encountered_party")' in block
    assert '(lt, "$g_encountered_party_2", 1)' not in block
    assert '"$g_encountered_party_faction"' not in block


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

