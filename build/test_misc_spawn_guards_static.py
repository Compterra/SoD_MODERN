from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_merchant_looter_quest_only_flags_live_spawned_parties():
    text = _read("src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_looters_brief.py")
    spawn = text.index('(spawn_around_party, "$g_encountered_party", "pt_bandits")')
    flag = text.index("(party_set_flags, \":looter_party\", pf_quest_party, 1)", spawn)
    guard = text[spawn:flag]

    assert '(assign, ":looter_party", reg0)' in guard
    assert '(gt, ":looter_party", 0)' in guard
    assert '(party_is_active, ":looter_party")' in guard
    assert '(quest_set_slot, "qst_deal_with_looters", slot_quest_target_amount, ":spawned_looters")' in text


def test_sacrificed_messenger_removes_troop_only_after_party_spawn_succeeds():
    text = _read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sacrificed_messenger_3.py")
    spawn = text.index('(spawn_around_party, "p_main_party", "pt_sacrificed_messenger")')
    remove = text.index('(party_remove_members, "p_main_party", "$g_talk_troop", 1)', spawn)
    guard = text[spawn:remove]

    assert '(assign, ":new_party", reg0)' in guard
    assert '(gt, ":new_party", 0)' in guard
    assert '(party_is_active, ":new_party")' in guard


def test_disembark_ship_spawn_is_validated_before_ship_mutation():
    text = _read("src/menus/other/disembark_yes_02.py")
    spawn = text.index('(spawn_around_party, "p_main_party", "pt_none")')
    flags = text.index('(party_set_flags, "$g_main_ship_party"', spawn)
    enable = text.index('(enable_party, "$g_main_ship_party")', spawn)

    assert '(assign, "$g_main_ship_party", reg0)' in text[spawn:flags]
    assert '(gt, "$g_main_ship_party", 0)' in text[spawn:flags]
    assert '(party_is_active, "$g_main_ship_party")' in text[spawn:flags]
    assert '(gt, "$g_main_ship_party", 0)' in text[flags:enable]
    assert '(party_is_active, "$g_main_ship_party")' in text[flags:enable]
