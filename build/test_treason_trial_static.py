from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def test_treason_helper_uses_political_inputs() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_treason_trial.py")
    for token in (
        "sod_treason_select_plea_reaction",
        "sod_treason_select_final_words",
        "sod_treason_apply_spared_outcome",
        "slot_lord_reputation_type",
        "slot_troop_renown",
        "faction_slot_eq",
        "script_troop_get_player_relation",
        "lrep_goodnatured",
        "lrep_upstanding",
        "lrep_martial",
        "lrep_quarrelsome",
        "lrep_selfrighteous",
        "lrep_cunning",
        "lrep_debauched",
    ):
        assert_contains(raw, token)


def test_treason_dialogues_call_helpers_instead_of_raw_random_modulo() -> None:
    accusation = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason.py")
    guilty = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_guilty.py")
    assert_contains(accusation, "script_sod_treason_select_plea_reaction")
    assert_contains(guilty, "script_sod_treason_select_final_words")
    assert_not_contains(accusation, "val_mod")
    assert_not_contains(guilty, "val_mod")


def test_spare_path_stays_custody_mercy_not_release() -> None:
    spare = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_choose.py")
    assert_contains(spare, "script_sod_treason_apply_spared_outcome")
    assert_contains(spare, "slot_prisoner_agreed")
    assert_not_contains(spare, "script_remove_troop_from_prison")
    assert_not_contains(spare, "party_remove_prisoners")
    assert_not_contains(spare, "remove_troops_from_prisoners")


def test_execution_path_keeps_existing_consequences() -> None:
    execution = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_execute.py")
    for token in (
        "script_kill_kingdom_hero",
        "script_sod_diplomacy_record_event",
        "sod_diplomacy_memory_executed_lord",
        "sod_companion_action_execute_lord",
        "script_change_player_honor",
        "script_change_player_party_morale",
        "script_change_troop_renown",
        "script_remove_troop_from_prison",
    ):
        assert_contains(execution, token)


def test_treason_text_polish() -> None:
    treason_files = [
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_choose_02.py",
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_prisoner_chat_treason_final_words.py",
    ]
    raw = "\n".join(read(path) for path in treason_files)
    for stale in ("cimes", "leiniency", "Who are you?^A day passes^We are but children"):
        assert_not_contains(raw, stale)
    assert_contains(raw, "crimes against")
    assert_contains(raw, "leniency")
    assert_contains(raw, "not as a traitor")


if __name__ == "__main__":
    test_treason_helper_uses_political_inputs()
    test_treason_dialogues_call_helpers_instead_of_raw_random_modulo()
    test_spare_path_stays_custody_mercy_not_release()
    test_execution_path_keeps_existing_consequences()
    test_treason_text_polish()
    print("test_treason_trial_static: OK")
