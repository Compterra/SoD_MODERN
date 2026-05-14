from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def prisoner_script():
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    start = raw.index('("sod_prisoner_train_destroyed"')
    end = raw.index('("sod_process_prisoner_trains"')
    return raw, raw[start:end]


def test_prisoner_train_factory_validates_spawn_before_mutating_party():
    raw = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    start = raw.index('("cf_sod_create_prisoner_train"')
    end = raw.index('("sod_player_prepare_prisoner_train_order"')
    factory = raw[start:end]

    spawn_index = factory.index('(spawn_around_party, ":origin", "pt_prisoner_train_party")')
    active_index = factory.index('(neg|party_is_active, ":result")')
    mutate_index = factory.index('(party_set_faction, ":result", ":faction_no")')
    assert spawn_index < active_index < mutate_index
    assert '(assign, ":fail_reason", sod_prisoner_train_fail_invalid_origin)' in factory
    assert '(assign, ":result", -1)' in factory


def test_prisoner_destroyed_military_fugitive_spawn_is_guarded():
    _, destroyed = prisoner_script()

    spawn_index = destroyed.index('(spawn_around_party, ":train_party", "pt_runaway_serfs")')
    active_index = destroyed.index('(party_is_active, ":military_fugitive_party")')
    faction_index = destroyed.index('(party_set_faction, ":military_fugitive_party", ":origin_faction")')
    ai_index = destroyed.index('(party_set_ai_behavior, ":military_fugitive_party", ai_bhvr_travel_to_party)')
    assert spawn_index < active_index < faction_index < ai_index


def test_prisoner_destroyed_scattered_fugitive_spawn_is_guarded():
    _, destroyed = prisoner_script()

    scattered_start = destroyed.index('(ge, ":scattered", 12)')
    scattered = destroyed[scattered_start:]
    active_index = scattered.index('(party_is_active, ":fugitive_party")')
    ai_index = scattered.index('(party_set_ai_behavior, ":fugitive_party", ai_bhvr_travel_to_party)')
    assert active_index < ai_index


def test_prisoner_destroyed_bandit_spawn_is_guarded():
    _, destroyed = prisoner_script()

    bandit_start = destroyed.index('(ge, ":bandit_recruits", 8)')
    bandit = destroyed[bandit_start:]
    active_index = bandit.index('(party_is_active, ":bandit_party")')
    slot_index = bandit.index('(party_set_slot, ":bandit_party", slot_party_sod_threat_type')
    add_index = bandit.index('(party_add_members, ":bandit_party", "trp_bandit", ":bandit_recruits")')
    assert active_index < slot_index < add_index
