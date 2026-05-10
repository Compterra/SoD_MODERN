from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_house_memory_helpers_exist() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_house_politics.py")
    assert_contains(raw, "sod_house_adjust_memory")
    assert_contains(raw, "sod_house_note_lord_captured_by_player")
    assert_contains(raw, "sod_house_note_lord_released_by_player")
    assert_contains(raw, "sod_house_note_fief_change")
    assert_contains(raw, "sod_house_describe_noble_houses_to_s1")
    assert_contains(raw, "sod_strategy_advisor_describe_house_politics_to_s1")
    assert_contains(raw, "slot_troop_sod_house_grievance")
    assert_contains(raw, "slot_troop_sod_house_loyalty")
    assert_contains(raw, "slot_troop_sod_house_claim_strength")
    assert_contains(raw, "script_change_player_relation_with_troop")
    assert_contains(raw, ":player_realm_transfer")


def test_house_event_hooks_are_wired() -> None:
    capture = read("src/scripts/ZC_parties/event_hero_taken_prisoner_by_player.py")
    release = read("src/scripts/ZH_heroes/remove_troop_from_prison.py")
    fiefs = read("src/scripts/ZD_centers/give_center_to_lord.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    assert_contains(capture, "script_sod_house_note_lord_captured_by_player")
    assert_contains(release, "script_sod_house_note_lord_released_by_player")
    assert_contains(release, ":was_player_prisoner")
    assert_contains(fiefs, "script_sod_house_note_fief_change")
    assert "#        (call_script, \"script_change_player_relation_with_troop\"" not in fiefs
    assert_contains(game_start, "$g_sod_house_politics_active")


def test_house_report_and_advisor_are_wired() -> None:
    menu = read("src/menus/reports/noble_houses_report.py")
    reports = read("src/menus/reports/report_submenus.py")
    menu_order = read("src/menus/_order_game_menus.txt")
    dialog_choice = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_answer_houses.py")
    dialog_reply = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_houses.py")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    assert_contains(menu, "noble_houses_report")
    assert_contains(menu, "script_sod_house_describe_noble_houses_to_s1")
    assert_contains(reports, "mnu_noble_houses_report")
    assert_contains(menu_order, "reports/noble_houses_report.py")
    assert_contains(dialog_choice, "Which noble houses need watching?")
    assert_contains(dialog_reply, "script_sod_strategy_advisor_describe_house_politics_to_s1")
    assert_contains(dialog_order, "trp_sod_strategy_advisor_sod_sa_war_room_houses.py")


if __name__ == "__main__":
    test_house_memory_helpers_exist()
    test_house_event_hooks_are_wired()
    test_house_report_and_advisor_are_wired()
    print("test_house_politics_static: OK")
