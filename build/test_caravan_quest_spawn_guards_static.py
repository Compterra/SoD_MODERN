from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_caravan_acceptance_guarded(path, quest_id, template_id, warning_text):
    raw = read(path)

    assert f'(spawn_around_party, "$g_encountered_party", "{template_id}")' in raw
    assert '(party_is_active, ":quest_target_center")' in raw
    assert '(party_is_active, "$g_encountered_party")' in raw
    assert '(gt, ":quest_target_party", 0)' in raw
    assert '(party_is_active, ":quest_target_party")' in raw
    assert warning_text in raw

    spawn_index = raw.index(f'(spawn_around_party, "$g_encountered_party", "{template_id}")')
    assert raw.index('(party_is_active, ":quest_target_center")') < spawn_index
    assert raw.index('(party_is_active, "$g_encountered_party")') < spawn_index
    active_index = raw.index('(party_is_active, ":quest_target_party")')
    target_slot_index = raw.index(f'(quest_set_slot, "{quest_id}", slot_quest_target_party')
    state_slot_index = raw.index(f'(quest_set_slot, "{quest_id}", slot_quest_current_state')
    start_index = raw.index(f'(call_script, "script_start_quest", "{quest_id}"')
    assert active_index < target_slot_index < state_slot_index < start_index


def assert_ordered(raw, tokens):
    offset = 0
    for token in tokens:
        index = raw.find(token, offset)
        if index < 0:
            raise AssertionError(f"missing ordered token after {offset}: {token}")
        offset = index + len(token)


def assert_caravan_order_updates_ai(path, quest_id, expected_behavior):
    raw = read(path)
    assert_ordered(
        raw,
        (
            f'(quest_get_slot, ":quest_target_party", "{quest_id}", slot_quest_target_party)',
            '(gt, ":quest_target_party", 0)',
            '(party_is_active, ":quest_target_party")',
            f'(party_set_ai_behavior, ":quest_target_party", {expected_behavior})',
            '(party_set_ai_object, ":quest_target_party", "p_main_party")',
            '(party_set_flags, ":quest_target_party", pf_default_behavior, 0)',
            f'(quest_set_slot, "{quest_id}", slot_quest_current_state, 1)',
        ),
    )


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


def test_slaver_caravan_completion_requires_actual_quest_party():
    raw = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start.py")
    tokens = (
        '(quest_get_slot, ":quest_target_party", "qst_slavers_escort_merchant_caravan", slot_quest_target_party)',
        '(gt, ":quest_target_party", 0)',
        '(eq, "$g_encountered_party", ":quest_target_party")',
        '(party_is_active, ":quest_target_party")',
        '(quest_get_slot, ":quest_target_center", "qst_slavers_escort_merchant_caravan", slot_quest_target_center)',
        '(party_is_active, ":quest_target_center")',
        '(quest_slot_eq, "qst_slavers_escort_merchant_caravan", slot_quest_current_state, 1)',
        '(store_distance_to_party_from_party, ":dist", ":quest_target_center", "$g_encountered_party")',
        '(quest_get_slot, reg14, "qst_slavers_escort_merchant_caravan", slot_quest_gold_reward)',
        '(str_store_party_name, s21, ":quest_target_center")',
        '(call_script, "script_end_quest", "qst_slavers_escort_merchant_caravan")',
    )
    offset = 0
    for token in tokens:
        index = raw.find(token, offset)
        if index < 0:
            raise AssertionError(f"slaver caravan completion missing ordered token: {token}")
        offset = index + len(token)


def test_caravan_completion_display_registers_are_prepared_before_text():
    for path, quest_id, distance_party in (
        (
            "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_02.py",
            "qst_escort_merchant_caravan",
            '":quest_target_party"',
        ),
        (
            "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_army_caravan_start.py",
            "qst_black_army_escort_merchant_caravan",
            '"p_main_party"',
        ),
        (
            "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start.py",
            "qst_slavers_escort_merchant_caravan",
            '"$g_encountered_party"',
        ),
    ):
        raw = read(path)
        text_index = raw.index("Here is your pay: {reg14} denars.")
        condition_block = raw[:text_index]
        assert f'(quest_get_slot, ":quest_target_party", "{quest_id}", slot_quest_target_party)' in condition_block
        assert '(gt, ":quest_target_party", 0)' in condition_block
        assert '(party_is_active, ":quest_target_party")' in condition_block
        assert f'(quest_get_slot, ":quest_target_center", "{quest_id}", slot_quest_target_center)' in condition_block
        assert '(party_is_active, ":quest_target_center")' in condition_block
        assert f'(store_distance_to_party_from_party, ":dist", ":quest_target_center", {distance_party})' in condition_block
        assert f'(quest_get_slot, reg14, "{quest_id}", slot_quest_gold_reward)' in condition_block
        assert '(str_store_party_name, s21, ":quest_target_center")' in condition_block


def test_caravan_follow_and_wait_orders_update_actual_party_ai():
    for quest_id, follow_path, wait_path in (
        (
            "qst_escort_merchant_caravan",
            "src/dialogs/ZC01_centers_and_economy/anyone_merchant_caravan_follow_lead.py",
            "src/dialogs/ZC01_centers_and_economy/anyone_merchant_caravan_stay_here.py",
        ),
        (
            "qst_black_army_escort_merchant_caravan",
            "src/dialogs/ZC01_centers_and_economy/anyone_black_army_merchant_caravan_follow_lead.py",
            "src/dialogs/ZC01_centers_and_economy/anyone_black_army_merchant_caravan_stay_here.py",
        ),
        (
            "qst_slavers_escort_merchant_caravan",
            "src/dialogs/ZC01_centers_and_economy/anyone_slavers_merchant_caravan_follow_lead.py",
            "src/dialogs/ZC01_centers_and_economy/anyone_slavers_merchant_caravan_stay_here.py",
        ),
    ):
        assert_caravan_order_updates_ai(follow_path, quest_id, "ai_bhvr_track_party")
        assert_caravan_order_updates_ai(wait_path, quest_id, "ai_bhvr_hold")


if __name__ == "__main__":
    test_standard_merchant_caravan_spawn_is_guarded()
    test_black_army_caravan_spawn_is_guarded()
    test_slaver_caravan_spawn_is_guarded()
    test_slaver_caravan_completion_requires_actual_quest_party()
    test_caravan_completion_display_registers_are_prepared_before_text()
    test_caravan_follow_and_wait_orders_update_actual_party_ai()
    print("test_caravan_quest_spawn_guards_static: OK")
