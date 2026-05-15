from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_runaway_serf_acceptance_cleans_up_partial_spawn_before_starting_quest():
    raw = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_accepted.py")

    assert '(assign, ":start_random_quest", 1)' in raw
    assert '(assign, ":spawned_serf_parties", 0)' in raw
    assert '(lt, ":spawned_serf_parties", 3)' in raw
    assert '(assign, ":start_random_quest", 0)' in raw
    assert "The runaway serf trail could not be placed on the map" in raw

    cleanup_index = raw.index('(lt, ":spawned_serf_parties", 3)')
    start_guard_index = raw.index('(eq, ":start_random_quest", 1),\n      (call_script, "script_start_quest"')
    assert cleanup_index < start_guard_index

    for global_name in (
        "$qst_bring_back_runaway_serfs_party_1",
        "$qst_bring_back_runaway_serfs_party_2",
        "$qst_bring_back_runaway_serfs_party_3",
    ):
        assert f'(assign, "{global_name}", 0)' in raw
        assert f'(remove_party, "{global_name}")' in raw


def test_follow_spy_acceptance_starts_only_after_both_parties_spawn():
    raw = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_mission_follow_spy_accepted.py")

    assert '(assign, ":spawn_ok", 0)' in raw
    assert '(assign, ":spawn_ok", 1)' in raw
    assert '(eq, ":spawn_ok", 1)' in raw
    assert "The spy trail could not be placed on the map" in raw

    spawn_partners_index = raw.index('(spawn_around_party, "p_main_party", "pt_spy_partners")')
    spawn_spy_index = raw.index('(spawn_around_party, "$g_encountered_party", "pt_spy")')
    start_guard_index = raw.index('(eq, ":spawn_ok", 1)')
    start_quest_index = raw.index('(call_script, "script_start_quest"')
    assert spawn_partners_index < start_guard_index < start_quest_index
    assert spawn_spy_index < start_guard_index < start_quest_index

    for global_name in (
        "$qst_follow_spy_spy_party",
        "$qst_follow_spy_spy_partners_party",
    ):
        assert f'(assign, "{global_name}", 0)' in raw
        assert f'(remove_party, "{global_name}")' in raw


def test_follow_spy_party_dialogs_require_current_quest_parties():
    spy_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_spy_start.py")
    partners_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_spy_partners_start.py")
    spy_arrest = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_follow_spy_talk.py")
    partners_arrest = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_spy_partners_talk.py")

    for raw in (spy_start, partners_start, spy_arrest, partners_arrest):
        assert '(check_quest_active, "qst_follow_spy")' in raw
        assert '(neg|check_quest_concluded, "qst_follow_spy")' in raw
        assert '(party_is_active, "$g_encountered_party")' in raw

    assert '(eq, "$qst_follow_spy_spy_party", "$g_encountered_party")' in spy_start
    assert '(eq, "$qst_follow_spy_spy_party", "$g_encountered_party")' in spy_arrest
    assert '(eq, "$qst_follow_spy_spy_partners_party", "$g_encountered_party")' in partners_start
    assert '(eq, "$qst_follow_spy_spy_partners_party", "$g_encountered_party")' in partners_arrest


def test_follow_spy_legacy_trigger_guards_party_globals_before_distance_checks():
    raw = read("compile/module_triggers.py")
    start = raw.index("# Follow Spy quest")
    end = raw.index("### Raiders quest", start)
    block = raw[start:end]

    assert '(is_between, ":quest_giver_center", centers_begin, centers_end)' in block
    assert '(is_between, ":quest_object_center", centers_begin, centers_end)' in block
    assert '(gt, "$qst_follow_spy_spy_party", 0)' in block
    assert '(gt, "$qst_follow_spy_spy_partners_party", 0)' in block
    assert '(assign, ":spy_active", 1)' in block
    assert '(assign, ":partner_active", 1)' in block
    assert '(this_or_next|eq, ":spy_active", 0)' in block
    assert '(eq, ":partner_active", 0)' in block
    assert '(eq, ":spy_active", 1)' in block
    assert '(eq, ":partner_active", 1)' in block
    assert block.index('(gt, "$qst_follow_spy_spy_party", 0)') < block.index('(store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_follow_spy_spy_party")')
    assert block.index('(gt, "$qst_follow_spy_spy_partners_party", 0)') < block.index('(store_distance_to_party_from_party, ":cur_distance", "$qst_follow_spy_spy_partners_party", "$qst_follow_spy_spy_party")')


def test_follow_spy_abort_clears_party_globals():
    raw = read("src/scripts/ZG_quests/abort_quest.py")
    start = raw.index('(eq, ":quest_no", "qst_follow_spy")')
    end = raw.index('(eq, ":quest_no", "qst_capture_enemy_hero")', start)
    block = raw[start:end]

    assert '(gt, "$qst_follow_spy_spy_party", 0)' in block
    assert '(gt, "$qst_follow_spy_spy_partners_party", 0)' in block
    assert '(assign, "$qst_follow_spy_spy_party", 0)' in block
    assert '(assign, "$qst_follow_spy_spy_partners_party", 0)' in block
    assert '(assign, "$qst_follow_spy_no_active_parties", 1)' in block


def test_runaway_slave_acceptance_cleans_up_partial_spawn_before_starting_quest():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_bring_back_runaway_slaves_accepted.py")

    assert '(assign, ":spawned_slave_parties", 0)' in raw
    assert '(lt, ":spawned_slave_parties", 3)' in raw
    assert "The runaway slave trail could not be placed on the map" in raw

    cleanup_index = raw.index('(lt, ":spawned_slave_parties", 3)')
    start_quest_index = raw.index('(call_script, "script_start_quest"')
    assert cleanup_index < start_quest_index

    for global_name in (
        "$qst_bring_back_runaway_slaves_party_1",
        "$qst_bring_back_runaway_slaves_party_2",
        "$qst_bring_back_runaway_slaves_party_3",
    ):
        assert f'(assign, "{global_name}", 0)' in raw
        assert f'(remove_party, "{global_name}")' in raw
