from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_nemesis_constants_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for token in (
        "sod_nemesis_actor_outlaw",
        "sod_nemesis_actor_deserter",
        "sod_nemesis_actor_contract_threat",
        "sod_nemesis_reason_humiliation",
        "sod_nemesis_reason_robbed",
        "sod_nemesis_reason_battle_defeat",
        "sod_nemesis_reason_lord_defeat",
        "sod_nemesis_state_watching",
        "sod_nemesis_state_hunting",
        "slot_troop_sod_nemesis_defeats",
        "slot_troop_sod_nemesis_strength",
        "slot_troop_sod_nemesis_duel_pressure",
        "slot_troop_sod_nemesis_last_duel_day",
        "slot_troop_sod_nemesis_duel_wins",
        "slot_troop_sod_nemesis_adaptation",
        "slot_troop_sod_nemesis_mercy_count",
        "slot_troop_sod_nemesis_capture_count",
        "slot_troop_sod_nemesis_humiliation_count",
        "sod_nemesis_adaptation_anti_cavalry",
        "sod_nemesis_lord_resolution_mercy",
    ):
        assert_contains(constants, token)


def test_hostile_events_feed_nemesis_memory() -> None:
    reputation = read("src/scripts/ZY_helper_scripts/sod_note_hostile_reputation.py")
    nemesis = read("src/scripts/ZY_helper_scripts/sod_nemesis_note_hostile_event.py")
    lord_nemesis = read("src/scripts/ZY_helper_scripts/sod_nemesis_note_lord_event.py")
    victory = read("src/scripts/ZC_parties/total_victory_finalize.py")

    assert_contains(reputation, 'call_script, "script_sod_nemesis_note_hostile_event", ":event_type"')
    assert_contains(victory, 'call_script, "script_sod_nemesis_note_hostile_event", 10')
    assert_contains(victory, 'call_script, "script_sod_nemesis_note_lord_event", ":enemy_leader", sod_nemesis_reason_lord_defeat')
    assert_contains(lord_nemesis, 'neq, ":lord_faction", "fac_kingdom_6"')
    assert_contains(lord_nemesis, "$g_sod_nemesis_last_troop")
    assert_contains(lord_nemesis, "slot_troop_sod_nemesis_defeats")
    assert_contains(lord_nemesis, "slot_troop_sod_nemesis_adaptation")
    assert_contains(lord_nemesis, 'val_min, ":adapt_count", 10')
    assert_contains(lord_nemesis, "itp_type_bow")
    assert_contains(lord_nemesis, "troop_raise_proficiency_linear")
    assert_contains(lord_nemesis, "troop_raise_attribute")
    assert_contains(nemesis, "$g_sod_nemesis_actor_type")
    assert_contains(nemesis, "$g_sod_nemesis_intensity")
    assert_contains(nemesis, "$g_sod_nemesis_last_template")
    assert_contains(nemesis, "sod_nemesis_state_hunting")
    assert_contains(nemesis, "val_min, \"$g_sod_nemesis_intensity\", 5")


def test_nemesis_is_visible_and_affects_grudges() -> None:
    report = read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_hostile_reputation_report.py")
    report_helper = read("src/scripts/ZY_helper_scripts/sod_store_nemesis_memory_report.py")
    shakedown = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_grudge_revenge_shakedown.py")
    intimidation = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_grudge_revenge_intimidation.py")
    doc = read("docs/reports/quests/nemesis_memory_overhaul.md")

    assert_contains(report, "script_sod_store_nemesis_memory_report")
    assert_contains(report, "Intensity {reg17}; last day {reg18}")
    assert_contains(report_helper, "true named nemesis candidate")
    assert_contains(shakedown, "sod_nemesis_reason_robbed")
    assert_contains(shakedown, "sod_nemesis_state_hunting")
    assert_contains(intimidation, "sod_nemesis_reason_humiliation")
    assert_contains(intimidation, "sod_nemesis_state_hunting")
    assert_contains(doc, "first consolidation slice implemented")
    assert_contains(doc, "non-`kingdom_6` lords")
    assert_contains(doc, "Do not create fake named heroes from ordinary troops")


def test_lord_nemesis_feeds_battlefield_duels() -> None:
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    finder = read("src/scripts/ZY_helper_scripts/ponavosa_duel_find_commander_pair.py")
    begin = read("src/scripts/ZY_helper_scripts/ponavosa_duel_begin.py")
    aura = read("src/scripts/ZY_helper_scripts/ponavosa_duel_apply_commander_aura.py")
    resolve = read("src/scripts/ZY_helper_scripts/ponavosa_duel_resolve.py")
    report_helper = read("src/scripts/ZY_helper_scripts/sod_store_nemesis_memory_report.py")
    doc = read("docs/reports/quests/nemesis_memory_overhaul.md")

    assert_contains(preamble, "slot_troop_sod_nemesis_duel_pressure")
    assert_contains(preamble, ":nemesis_present")
    assert_contains(preamble, '(eq, ":nemesis_present", 1)')
    assert_contains(preamble, 'val_min, ":challenge_chance", 65')
    assert_contains(finder, 'eq, ":enemy_troop", "$g_sod_nemesis_last_troop"')
    assert_contains(finder, ":enemy_priority")
    assert_contains(begin, "$ponavosa_duel_nemesis")
    assert_contains(begin, '(assign, "$ponavosa_duel_nemesis", 0)')
    assert_contains(begin, "Your nemesis forces the issue")
    assert_contains(aura, "Nemesis strength {reg3}")
    assert_contains(resolve, "Defeat only feeds your nemesis")
    assert_contains(resolve, "slot_troop_sod_nemesis_duel_wins")
    assert_contains(report_helper, "duel pressure {reg23}")
    assert_contains(report_helper, "Current adaptation: {s21}")
    assert_contains(report_helper, "Mercy {reg25}; captures {reg26}; humiliations {reg28}")
    assert_contains(doc, "existing battlefield duel mechanics")


def test_lord_nemesis_resolution_forks() -> None:
    resolution = read("src/scripts/ZY_helper_scripts/sod_nemesis_note_lord_resolution.py")
    capture = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_defeat_lord_answer_02.py")
    release = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_defeat_lord_answer_06.py")
    prisoner_release = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_prisoner_chat_noble_release.py")
    humiliation = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cc_humilitae_2.py")
    aura = read("src/scripts/ZY_helper_scripts/ponavosa_duel_apply_commander_aura.py")

    assert_contains(resolution, "slot_troop_sod_nemesis_mercy_count")
    assert_contains(resolution, "slot_troop_sod_nemesis_capture_count")
    assert_contains(resolution, "slot_troop_sod_nemesis_humiliation_count")
    assert_contains(resolution, 'val_min, ":mercy_count", 99')
    assert_contains(resolution, 'val_min, ":capture_count", 99')
    assert_contains(resolution, 'val_min, ":humiliation_count", 99')
    assert_contains(resolution, "Mercy complicates")
    assert_contains(resolution, "Chains sharpen")
    assert_contains(capture, "sod_nemesis_lord_resolution_capture")
    assert_contains(release, "sod_nemesis_lord_resolution_mercy")
    assert_contains(prisoner_release, "sod_nemesis_lord_resolution_mercy")
    assert_contains(humiliation, "sod_nemesis_lord_resolution_humiliation")
    assert_contains(aura, "mounted pressure")
    assert_contains(aura, "single combat")


def test_lord_nemesis_has_custom_dialog_lines() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    talk = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_sod_nemesis_lord_memory.py")
    humiliated = read("src/dialogs/ZB01_lords_politics_and_family/anyone_sod_nemesis_lord_memory_humiliated.py")
    adapted = read("src/dialogs/ZB01_lords_politics_and_family/anyone_sod_nemesis_lord_memory_adapted.py")
    hostile = read("src/dialogs/ZB01_lords_politics_and_family/anyone_sod_nemesis_lord_hostile_fight.py")
    captured = read("src/dialogs/ZB01_lords_politics_and_family/anyone_sod_nemesis_defeat_lord_captured.py")
    released = read("src/dialogs/ZB01_lords_politics_and_family/anyone_sod_nemesis_defeat_lord_released.py")

    assert_contains(order, "anyone_plyr_sod_nemesis_lord_memory.py")
    assert_contains(order, "anyone_sod_nemesis_lord_hostile_fight.py")
    assert_contains(order, "anyone_auto_proceed_sod_nemesis_defeat_lord_answer_1.py")
    assert_contains(order, "anyone_auto_proceed_sod_nemesis_defeat_lord_answer_2.py")
    assert_contains(talk, "sod_nemesis_lord_memory")
    assert_contains(talk, 'eq, "$g_sod_nemesis_last_troop", "$g_talk_troop"')
    assert_contains(humiliated, "I have counted every laugh")
    assert_contains(adapted, "I remember enough to drill against {s21}")
    assert_contains(hostile, "I have worn the shape of your victories into my bones")
    assert_contains(captured, "Chains again")
    assert_contains(released, "Mercy again")


if __name__ == "__main__":
    test_nemesis_constants_exist()
    test_hostile_events_feed_nemesis_memory()
    test_nemesis_is_visible_and_affects_grudges()
    test_lord_nemesis_feeds_battlefield_duels()
    test_lord_nemesis_resolution_forks()
    test_lord_nemesis_has_custom_dialog_lines()
    print("test_nemesis_memory_static: OK")
