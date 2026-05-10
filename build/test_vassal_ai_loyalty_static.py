from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_vassal_land_loyalty_constants_exist():
    constants = read("src/constants/module_constants.py")
    required = [
        "slot_troop_sod_lord_land_satisfaction",
        "slot_troop_sod_lord_ruler_confidence",
        "slot_troop_sod_lord_last_land_grievance_day",
        "slot_troop_sod_lord_fief_expectation",
        "slot_troop_sod_lord_patron_target_faction",
        "slot_troop_sod_lord_last_patron_seek_day",
        "slot_troop_sod_lord_last_patron_offer_day",
        "slot_troop_sod_lord_last_petition_day",
        "slot_troop_sod_lord_last_poached_day",
        "slot_faction_sod_landless_lord_count",
        "slot_faction_sod_disgruntled_lord_count",
        "slot_faction_sod_vassal_loyalty_health",
        "sod_lord_intent_disgruntled_landless",
        "sod_lord_intent_seeking_patron",
    ]
    for token in required:
        assert token in constants


def test_vassal_land_loyalty_scripts_feed_ai():
    script = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    required = [
        '"sod_lord_update_land_satisfaction"',
        '"sod_lord_choose_patron_faction_to_reg"',
        '"sod_lord_process_patronage_path"',
        "script_get_number_of_hero_centers",
        "slot_troop_sod_lord_land_satisfaction",
        "slot_troop_sod_lord_ruler_confidence",
        "slot_troop_loyalty",
        "sod_lord_intent_disgruntled_landless",
        "sod_lord_intent_seeking_patron",
        "script_sod_lord_get_campaign_pressure",
        "script_sod_lord_get_battle_willingness",
        "script_sod_lord_adjust_follow_marshal_chance",
        "slot_faction_sod_landless_lord_count",
        "slot_faction_sod_disgruntled_lord_count",
        "slot_faction_sod_vassal_loyalty_health",
    ]
    for token in required:
        assert token in script


def test_vassal_land_loyalty_is_player_kingdom_visible():
    script = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert '"fac_player_supporters_faction"' in script
    assert "slot_troop_player_relation" in script
    assert "landless and resentful" in script
    assert "ruler confidence" in script


def test_landless_lords_have_patronage_decision_ladder():
    script = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    respawn = read("src/triggers/ST03_daily/entry_0046.py")
    required = [
        "slot_troop_sod_lord_patron_target_faction",
        "slot_troop_sod_lord_last_patron_seek_day",
        "slot_troop_sod_lord_last_patron_offer_day",
        "slot_troop_change_to_faction",
        "$g_sod_lord_offers_allegience",
        "fac_commoners",
        "fac_player_supporters_faction",
        "fac_kingdom_6",
    ]
    for token in required:
        assert token in script
    assert "script_sod_lord_process_patronage_path" in daily
    assert "start_map_conversation" in daily
    assert "script_sod_lord_choose_patron_faction_to_reg" in respawn


def test_player_can_persuade_landless_lords_after_battle_or_capture():
    script = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    order = read("src/dialogs/_order_dialogs.txt")
    postbattle = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_defeat_lord_landless_offer.py")
    prisoner = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_noble_landless_offer.py")
    required_script_tokens = [
        '"sod_lord_player_find_grantable_center_to_reg"',
        '"sod_lord_player_can_persuade_landless_to_reg"',
        '"sod_lord_apply_player_landless_persuasion"',
        "store_attribute_level",
        "ca_charisma",
        "skl_persuasion",
        "script_get_number_of_hero_centers",
        "script_give_center_to_lord",
        "script_change_troop_faction",
        "script_remove_troop_from_prison",
    ]
    for token in required_script_tokens:
        assert token in script
    assert "script_sod_lord_player_can_persuade_landless_to_reg" in postbattle
    assert "script_sod_lord_apply_player_landless_persuasion" in read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_sod_landless_lord_offer_postbattle_confirm.py")
    assert "script_sod_lord_player_can_persuade_landless_to_reg" in prisoner
    assert "script_sod_lord_apply_player_landless_persuasion" in read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_noble_landless_offer_confirm.py")
    assert "anyone_plyr_defeat_lord_landless_offer.py" in order
    assert "anyone_plyr_prisoner_chat_noble_landless_offer.py" in order


def test_landless_lord_politics_are_visible_and_affect_fiefs():
    assign = read("src/scripts/ZD_centers/assign_lords_to_empty_centers.py")
    give = read("src/scripts/ZD_centers/give_center_to_lord.py")
    notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    rumors = read("src/scripts/ZY_helper_scripts/get_rumor_to_s61.py")
    order = read("src/dialogs/_order_dialogs.txt")
    chancellor = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_chancellor_landless_report.py")
    script = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert "slot_troop_sod_lord_last_petition_day" in script
    assert '"sod_lord_describe_landless_politics_to_s68"' in script
    assert "slot_troop_sod_lord_last_poached_day" in script
    assert "val_add, \":score\", 80" in assign
    assert "slot_troop_sod_lord_ruler_confidence" in give
    assert "script_sod_lord_describe_landless_politics_to_s68" in notes
    assert "Landless lords" in script
    assert "stronger patrons" in rumors
    assert "trp_sod_chancellor_plyr_chancellor_talk_landless.py" in order
    assert "script_sod_lord_describe_landless_politics_to_s68" in chancellor
