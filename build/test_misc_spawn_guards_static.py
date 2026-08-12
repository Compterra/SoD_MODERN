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
    pre_spawn = text[:spawn]

    assert '(check_quest_active, "qst_incriminate_loyal_commander")' in text
    assert '(neg|check_quest_concluded, "qst_incriminate_loyal_commander")' in text
    assert '(quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 0)' in text
    assert '(party_is_active, ":quest_target_center")' in pre_spawn
    assert '(party_count_members_of_type, ":messenger_count", "p_main_party", "$g_talk_troop")' in pre_spawn
    assert '(gt, ":messenger_count", 0)' in pre_spawn
    assert '(assign, ":new_party", reg0)' in guard
    assert '(gt, ":new_party", 0)' in guard
    assert '(party_is_active, ":new_party")' in guard


def test_sacrificed_messenger_party_dialog_requires_actual_quest_party():
    text = _read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sacrificed_messenger_start.py")

    assert '(check_quest_active, "qst_incriminate_loyal_commander")' in text
    assert '(neg|check_quest_concluded, "qst_incriminate_loyal_commander")' in text
    assert '(quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 2)' in text
    assert '(quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_target_party, "$g_encountered_party")' in text
    assert '(party_is_active, "$g_encountered_party")' in text


def test_incriminate_loyal_commander_resolves_when_messenger_arrives():
    order = _read("src/triggers/_order_simple_triggers.txt")
    text = _read("src/triggers/ST02_every_hour/entry_0178_incriminate_loyal_commander.py")

    assert "ST02_every_hour/entry_0178_incriminate_loyal_commander.py" in order
    assert '(check_quest_active, "qst_incriminate_loyal_commander")' in text
    assert '(neg|check_quest_concluded, "qst_incriminate_loyal_commander")' in text
    assert '(quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 2)' in text
    assert '(quest_get_slot, ":messenger_party", "qst_incriminate_loyal_commander", slot_quest_target_party)' in text
    assert '(quest_get_slot, ":target_center", "qst_incriminate_loyal_commander", slot_quest_target_center)' in text
    assert '(party_is_active, ":messenger_party")' in text
    assert '(party_is_active, ":target_center")' in text
    assert '(party_get_template_id, ":messenger_template", ":messenger_party")' in text
    assert '(eq, ":messenger_template", "pt_sacrificed_messenger")' in text
    assert '(party_is_in_town, ":messenger_party", ":target_center")' in text
    assert '(store_distance_to_party_from_party, ":distance", ":messenger_party", ":target_center")' in text
    assert '(remove_party, ":messenger_party")' in text
    assert '(quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, -1)' in text
    assert '(call_script, "script_succeed_quest", "qst_incriminate_loyal_commander")' in text


def test_incriminate_loyal_commander_abort_cleans_messenger_party():
    text = _read("src/scripts/ZG_quests/abort_quest.py")
    start = text.index('(eq, ":quest_no", "qst_incriminate_loyal_commander")')
    end = text.index('(eq, ":quest_no", "qst_lend_surgeon")', start)
    block = text[start:end]

    assert '(quest_get_slot, ":messenger_party", "qst_incriminate_loyal_commander", slot_quest_target_party)' in block
    assert '(gt, ":messenger_party", 0)' in block
    assert '(party_is_active, ":messenger_party")' in block
    assert '(party_get_template_id, ":messenger_party_template", ":messenger_party")' in block
    assert '(eq, ":messenger_party_template", "pt_sacrificed_messenger")' in block
    assert '(remove_party, ":messenger_party")' in block
    assert '(quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, -1)' in block


def test_disembark_ship_spawn_is_validated_before_ship_mutation():
    text = _read("src/menus/other/disembark_yes_02.py")
    templates = _read("compile/module_party_templates.py")
    spawn = text.index('(spawn_around_party, "p_main_party", "pt_player_ship")')
    flags = text.index('(party_set_flags, "$g_main_ship_party"', spawn)
    enable = text.index('(enable_party, "$g_main_ship_party")', spawn)

    assert '("player_ship","Ship"' in templates
    assert "pt_none" not in text
    assert '(assign, "$g_main_ship_party", reg0)' in text[spawn:flags]
    assert '(gt, "$g_main_ship_party", 0)' in text[spawn:flags]
    assert '(party_is_active, "$g_main_ship_party")' in text[spawn:flags]
    assert '(gt, "$g_main_ship_party", 0)' in text[flags:enable]
    assert '(party_is_active, "$g_main_ship_party")' in text[flags:enable]
