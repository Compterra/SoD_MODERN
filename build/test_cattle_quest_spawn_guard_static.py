from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_create_cattle_herd_requires_active_spawned_party():
    raw = read("src/scripts/ZY_helper_scripts/create_cattle_herd.py")

    assert '(gt, ":herd_party", 0)' in raw
    assert '(party_is_active, ":herd_party")' in raw
    assert raw.index('(gt, ":herd_party", 0)') < raw.index('(party_is_active, ":herd_party")') < raw.index('(party_set_slot, ":herd_party", slot_party_type, spt_cattle_herd)')


def test_move_cattle_herd_quest_starts_only_after_real_herd_spawn():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_move_cattle_herd_quest_brief.py")

    assert '(assign, "$g_sod_last_cattle_herd_spawn_ok", 0)' in raw
    assert '(store_random_in_range, ":cattle_amount", 6, 12)' in raw
    assert '(call_script, "script_create_cattle_herd", "$g_encountered_party", ":cattle_amount")' in raw
    assert '(assign, "$g_sod_last_cattle_herd_spawn_ok", 1)' in raw

    active_index = raw.index('(party_is_active, ":herd_party")')
    slot_index = raw.index('(quest_set_slot, "qst_move_cattle_herd", slot_quest_target_party, ":herd_party")')
    start_index = raw.index('(call_script, "script_start_quest", "qst_move_cattle_herd"')
    assert active_index < slot_index < start_index


def test_move_cattle_herd_response_handles_spawn_failure():
    raw = read("src/dialogs/ZZ99_misc_dialogs/anyone_move_cattle_herd_quest_taken.py")

    assert "$g_sod_last_cattle_herd_spawn_ok" in raw
    assert "The herd cannot be gathered right now" in raw
