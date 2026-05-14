from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_guarded_rescue_acceptance(path, quest_id, template_id):
    raw = read(path)

    assert '(assign, "$g_sod_last_rescue_spawn_ok", 0)' in raw
    assert f'(spawn_around_party, ":quest_target_center", "{template_id}")' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert '(party_is_active, ":quest_target_party")' in raw
    assert '(assign, "$g_sod_last_rescue_spawn_ok", 1)' in raw

    guard_index = raw.index('(assign, "$g_sod_last_rescue_spawn_ok", 1)')
    gold_index = raw.index('(call_script, "script_troop_add_gold"')
    start_index = raw.index(f'(call_script, "script_start_quest", "{quest_id}"')
    assert guard_index < gold_index < start_index


def test_kidnapped_girl_acceptance_requires_valid_bandit_party():
    assert_guarded_rescue_acceptance(
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_quest_brief.py",
        "qst_kidnapped_girl",
        "pt_bandits_awaiting_ransom",
    )

    taken = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_kidnapped_girl_quest_taken.py")
    assert "$g_sod_last_rescue_spawn_ok" in taken
    assert "The bandits' trail has gone cold" in taken


def test_serpent_spy_acceptance_requires_valid_militia_party():
    assert_guarded_rescue_acceptance(
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_spy.py",
        "qst_serpent_host_free_spy",
        "pt_militia_awaiting_ransom",
    )

    taken = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_mission_told_free_spy_taken.py")
    assert "$g_sod_last_rescue_spawn_ok" in taken
    assert "The militia column has slipped from our sight" in taken


def test_jotnar_clansmen_acceptance_requires_valid_slaver_party():
    assert_guarded_rescue_acceptance(
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_clansmen.py",
        "qst_jotnar_clan_free_clansmen",
        "pt_slaves_with_jotnar_clansmen",
    )

    taken = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_mission_told_free_clansmen_taken.py")
    assert "$g_sod_last_rescue_spawn_ok" in taken
    assert "The slaver party has vanished from the route" in taken
