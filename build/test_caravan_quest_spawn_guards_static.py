from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_caravan_acceptance_guarded(path, quest_id, template_id, warning_text):
    raw = read(path)

    assert f'(spawn_around_party, "$g_encountered_party", "{template_id}")' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert '(party_is_active, ":quest_target_party")' in raw
    assert warning_text in raw

    active_index = raw.index('(party_is_active, ":quest_target_party")')
    target_slot_index = raw.index(f'(quest_set_slot, "{quest_id}", slot_quest_target_party')
    state_slot_index = raw.index(f'(quest_set_slot, "{quest_id}", slot_quest_current_state')
    start_index = raw.index(f'(call_script, "script_start_quest", "{quest_id}"')
    assert active_index < target_slot_index < state_slot_index < start_index


def test_standard_merchant_caravan_spawn_is_guarded():
    assert_caravan_acceptance_guarded(
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_escort_merchant_caravan_quest_brief.py",
        "qst_escort_merchant_caravan",
        "pt_merchant_caravan",
        "The merchant caravan could not be placed on the map",
    )


def test_black_army_caravan_spawn_is_guarded():
    assert_caravan_acceptance_guarded(
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_black_army_escort_merchant_caravan_quest_brief.py",
        "qst_black_army_escort_merchant_caravan",
        "pt_black_army_caravan",
        "The Black Army caravan could not be placed on the map",
    )


def test_slaver_caravan_spawn_is_guarded():
    assert_caravan_acceptance_guarded(
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_slavers_escort_merchant_caravan_quest_brief.py",
        "qst_slavers_escort_merchant_caravan",
        "pt_slavers_caravan",
        "The slaver caravan could not be placed on the map",
    )
