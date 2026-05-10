from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_pretender_slots_and_startup_defaults() -> None:
    constants = read("src/constants/module_constants.py")
    startup = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    for token in (
        "slot_troop_sod_pretender_claim_pressure",
        "slot_troop_sod_pretender_foothold_center",
        "slot_troop_sod_pretender_backer_lord",
        "slot_troop_sod_pretender_last_action_day",
        "slot_troop_sod_pretender_momentum",
    ):
        assert_contains(constants, token)
        assert_contains(startup, token)
    assert_contains(constants, "sod_pretender_pressure_stirring")
    assert_contains(constants, "sod_pretender_pressure_foothold")


def test_active_pretender_weekly_process_exists() -> None:
    politics = read("src/scripts/ZY_helper_scripts/sod_pretender_politics.py")
    order = read("src/triggers/_order_simple_triggers.txt")
    trigger = read("src/triggers/ST04_weekly/entry_0170.py")
    for token in (
        "sod_pretender_get_claim_pressure_to_reg",
        "sod_pretender_find_foothold_to_reg",
        "sod_pretender_find_backer_lord_to_reg",
        "sod_process_active_pretender_politics",
        "script_sod_house_adjust_memory",
        "slot_faction_has_rebellion_chance",
    ):
        assert_contains(politics, token)
    assert_contains(order, "ST04_weekly/entry_0170.py")
    assert_contains(trigger, "script_sod_process_active_pretender_politics")


def test_pretender_pressure_reaches_reports_and_dialog() -> None:
    house = read("src/scripts/ZY_helper_scripts/sod_house_politics.py")
    suggest = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_join_rebellion_suggest_05.py")
    claim = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_join_rebellion_suggest_3.py")
    assert_contains(house, "Active claimants:")
    assert_contains(house, "slot_troop_sod_pretender_claim_pressure")
    assert_contains(house, "sod_pretender_pressure_stirring")
    assert_contains(suggest, "script_sod_pretender_get_claim_pressure_to_reg")
    assert_contains(suggest, "$sod_rebel_pressure_mod")
    assert_contains(claim, "(val_add, reg0, \"$sod_rebel_pressure_mod\")")


def test_rebellion_debug_messages_are_cheat_gated() -> None:
    for path in (
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_join_rebellion_suggest_2.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_join_rebellion_suggest_4.py",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_join_rebellion_suggest_4_02.py",
    ):
        raw = read(path)
        if "display_message" in raw:
            assert_contains(raw, "(eq, \"$cheat_mode\", 1)")


def test_docs_record_first_pass_overhaul() -> None:
    raw = read("docs/reports/pretender_system_audit.md")
    assert_contains(raw, "Implemented first-pass overhaul")
    assert_contains(raw, "script_sod_process_active_pretender_politics")
    assert_contains(raw, "politically alive")


if __name__ == "__main__":
    test_pretender_slots_and_startup_defaults()
    test_active_pretender_weekly_process_exists()
    test_pretender_pressure_reaches_reports_and_dialog()
    test_rebellion_debug_messages_are_cheat_gated()
    test_docs_record_first_pass_overhaul()
    print("test_pretender_politics_static: OK")
