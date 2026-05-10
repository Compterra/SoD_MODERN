from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_rebel_counterpart_factions_exist() -> None:
    factions = read("compile/module_factions.py")
    for faction in (
        "kingdom_1_rebels",
        "kingdom_2_rebels",
        "kingdom_3_rebels",
        "kingdom_4_rebels",
        "kingdom_5_rebels",
    ):
        assert_contains(factions, f'("{faction}"')
    assert "##  (\"kingdom_1_rebels\"" not in factions


def test_claimant_constants_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for token in (
        'rebel_factions_begin = "fac_kingdom_1_rebels"',
        'rebel_factions_end =   "fac_kingdoms_end"',
        "slot_faction_sod_rebel_counterpart",
        "slot_faction_sod_parent_kingdom",
        "slot_faction_sod_claimant_pretender",
        "slot_faction_sod_claimant_old_ruler",
        "slot_faction_sod_civil_war_state",
        "slot_troop_sod_claimant_allegiance",
        "slot_troop_sod_claimant_rebel_faction",
        "sod_civil_war_open_rebellion",
        "sod_claimant_allegiance_secret_sympathizer",
        "sod_claimant_allegiance_open_rebel",
    ):
        assert_contains(constants, token)


def test_claimant_helper_wiring_exists() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_claimant_civil_war.py")
    startup = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    for token in (
        "sod_pretender_get_rebel_faction_to_reg",
        "sod_parent_kingdom_get_rebel_faction_to_reg",
        "sod_rebel_faction_get_parent_kingdom_to_reg",
        "sod_parent_kingdom_get_pretender_to_reg",
        "sod_initialize_claimant_civil_war_factions",
        "sod_claimant_civil_war_can_activate",
        "sod_claimant_civil_war_activate",
        "sod_troop_has_close_family_tie_to_reg",
        "sod_troop_has_fief_near_faction_to_reg",
        "sod_claimant_exile_lord_party",
        "sod_claimant_choose_defection_target_to_reg",
        "sod_claimant_mark_lord_open_rebel",
        "sod_claimant_try_establish_foothold",
        "sod_claimant_civil_war_check_resolution",
        "sod_lord_describe_claimant_allegiance_to_s1",
        "sod_pretender_describe_own_claimant_war_to_s1",
        "sod_claimant_describe_active_wars_to_s1",
        "sod_resolve_claimant_civil_war_victory",
        "sod_resolve_claimant_civil_war_failure",
        "sod_lord_choose_post_defeat_patron",
        "sfs_inactive_rebellion",
        "sfs_active",
        "slot_faction_sod_rebel_counterpart",
        "slot_troop_sod_claimant_allegiance",
        "slot_troop_spouse",
        "slot_lord_reputation_type",
    ):
        assert_contains(helper, token)
    assert_contains(startup, "script_sod_initialize_claimant_civil_war_factions")
    pretender_politics = read("src/scripts/ZY_helper_scripts/sod_pretender_politics.py")
    assert_contains(pretender_politics, "script_sod_claimant_civil_war_can_activate")
    assert_contains(pretender_politics, "script_sod_claimant_civil_war_activate")


def test_claimant_defection_wiring_exists() -> None:
    daily = read("src/triggers/ST03_daily/entry_0046.py")
    morale = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    hourly = read("src/triggers/ST02_every_hour/entry_0087.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_claimant_civil_war.py")
    assert_contains(daily, "script_sod_claimant_choose_defection_target_to_reg")
    assert_contains(morale, "script_sod_claimant_choose_defection_target_to_reg")
    assert_contains(hourly, "script_sod_claimant_mark_lord_open_rebel")
    for token in (
        "slot_troop_sod_house_grievance",
        "slot_troop_sod_house_loyalty",
        "script_get_number_of_hero_centers",
        "slot_troop_sod_pretender_momentum",
        "rebel_factions_begin",
        "outside_patron_score",
        "sod_claimant_allegiance_secret_sympathizer",
    ):
        assert_contains(helper, token)


def test_claimant_resolution_wiring_exists() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_claimant_civil_war.py")
    trigger = read("src/triggers/ST03_daily/entry_0171.py")
    order = read("src/triggers/_order_simple_triggers.txt")
    constants = read("src/constants/module_constants.py")
    random_faction = read("src/scripts/ZF_factions/cf_get_random_active_faction_except_player_faction_and_faction.py")
    for token in (
        "script_sod_claimant_maintain_rebel_ai",
        "script_sod_claimant_civil_war_check_resolution",
    ):
        assert_contains(trigger, token)
    assert_contains(order, "ST03_daily/entry_0171.py")
    for token in (
        "script_give_center_to_faction",
        "slot_faction_sod_civil_war_parent_fiefs",
        "slot_faction_sod_civil_war_rebel_fiefs",
        "sod_civil_war_rebel_victory",
        "sod_civil_war_loyalist_victory",
        "sod_claimant_allegiance_old_ruler_remnant",
        "sod_claimant_allegiance_reconciled",
        "slot_troop_sod_claimant_old_ruler_status",
        "script_change_player_honor",
        "script_change_troop_renown",
        "script_change_player_relation_with_troop",
        "script_sod_claimant_exile_lord_party",
        "set_relation, \":parent_faction\", \":other_faction\", \":rebel_relation\"",
        "slot_troop_sod_house_grievance",
        "sod_resolve_claimant_civil_war_victory",
        "sod_resolve_claimant_civil_war_failure",
        "slot_troop_original_faction",
        "slot_faction_culture",
    ):
        assert_contains(helper, token)
    assert_contains(constants, "sod_old_ruler_status_remnant_claimant")
    assert_contains(random_faction, "neg|is_between, \":faction_no\", rebel_factions_begin, rebel_factions_end")


def test_claimant_compatibility_guards_exist() -> None:
    decide_ai = read("src/scripts/ZF_factions/decide_faction_ai.py")
    declare_war = read("src/scripts/ZF_factions/faction_chose_an_opponent_and_declare_war.py")
    propose_peace = read("src/scripts/ZF_factions/faction_propose_peace.py")
    start_war = read("src/scripts/ZF_factions/diplomacy_start_war_between_kingdoms.py")
    start_peace = read("src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py")
    process_ai = read("src/scripts/ZF_factions/process_kingdom_parties_ai.py")
    select_marshall = read("src/scripts/ZF_factions/select_faction_marshall.py")
    strength = read("src/scripts/ZF_factions/faction_recalculate_strength.py")
    continue_71 = read("src/menus/other/continue_71.py")
    continue_72 = read("src/menus/other/continue_72.py")

    assert_contains(decide_ai, "is_between, \":faction_no\", rebel_factions_begin, rebel_factions_end")
    assert_contains(decide_ai, "script_sod_claimant_maintain_rebel_ai")
    for raw in (declare_war, propose_peace):
        assert_contains(raw, "neg|is_between, \":faction_no\", rebel_factions_begin, rebel_factions_end")
        assert_contains(raw, "neg|is_between, \":other_faction\", rebel_factions_begin, rebel_factions_end")
    for raw in (start_war, start_peace):
        assert_contains(raw, "neg|is_between, \":faction_a\", rebel_factions_begin, rebel_factions_end")
        assert_contains(raw, "neg|is_between, \":faction_b\", rebel_factions_begin, rebel_factions_end")
    assert_contains(process_ai, "script_process_hero_ai")
    assert_contains(select_marshall, "slot_faction_marshall")
    assert_contains(strength, "script_faction_get_number_of_armies")
    assert_contains(continue_71, "$supported_pretender")
    assert_contains(continue_71, "fac_player_supporters_faction")
    assert_contains(continue_72, "notification_rebels_switched_to_faction")


def test_kingdom_6_is_excluded_and_old_rebellion_path_remains() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_claimant_civil_war.py")
    old_player_path = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_give_conclude.py")
    old_quit_path = read("src/dialogs/ZB01_lords_politics_and_family/anyone_pretender_quit_rebel.py")
    assert "fac_kingdom_6_rebels" not in helper
    assert_contains(helper, '"fac_kingdom_1", "fac_kingdom_6"')
    assert_contains(old_player_path, "$supported_pretender")
    assert_contains(old_player_path, "fac_player_supporters_faction")
    assert_contains(old_quit_path, "pretender_quit_rebel")


def test_independent_claimant_scaffold_does_not_use_player_supporters_as_rebel_shell() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_claimant_civil_war.py")
    assert '"fac_player_supporters_faction"' not in read("compile/module_factions.py")
    assert "script_change_troop_faction\", \":backer\", \"fac_player_supporters_faction\"" not in helper
    assert "script_give_center_to_faction\", \":support_base\", \"fac_player_supporters_faction\"" not in helper


def test_claimant_player_facing_visibility_exists() -> None:
    helper = read("src/scripts/ZY_helper_scripts/sod_claimant_civil_war.py")
    house = read("src/scripts/ZY_helper_scripts/sod_house_politics.py")
    faction_notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    troop_notes = read("src/scripts/ZH_heroes/update_troop_notes.py")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    advisor_player = read(
        "src/dialogs/ZA02_sod_court_and_strategy/"
        "trp_sod_strategy_advisor_plyr_sod_sa_war_room_answer_claimants.py"
    )
    advisor_answer = read(
        "src/dialogs/ZA02_sod_court_and_strategy/"
        "trp_sod_strategy_advisor_sod_sa_war_room_claimants.py"
    )
    traveler_player = read(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/"
        "anyone_plyr_tavern_traveler_talk_claimant_wars.py"
    )
    traveler_answer = read(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/"
        "anyone_tavern_traveler_claimant_wars.py"
    )
    lord_player = read(
        "src/dialogs/ZB01_lords_politics_and_family/"
        "anyone_plyr_lord_talk_ask_something_2_claimant.py"
    )
    lord_answer = read(
        "src/dialogs/ZB01_lords_politics_and_family/"
        "anyone_lord_talk_claimant_allegiance.py"
    )
    pretender_player = read(
        "src/dialogs/ZB01_lords_politics_and_family/"
        "anyone_plyr_supported_pretender_talk_claimant_status.py"
    )
    pretender_answer = read(
        "src/dialogs/ZB01_lords_politics_and_family/"
        "anyone_supported_pretender_claimant_status.py"
    )
    pretender_start_player = read(
        "src/dialogs/ZA01_startup_and_dispatch/"
        "anyone_plyr_pretender_start_04.py"
    )
    pretender_start_answer = read(
        "src/dialogs/ZB01_lords_politics_and_family/"
        "anyone_pretender_claimant_status.py"
    )

    for token in (
        "Claimant wars:",
        "active rebel lord parties",
        "the pretender is near restoration",
        "the loyalists still hold the larger inheritance",
        "sod_troop_has_claimant_dialog_to_reg",
        "sod_lord_store_claimant_flavor_to_s5",
        "This is treason wearing a crown.",
        "Every hall has its own version of this war.",
        "The clerks have begun to choose their words carefully",
        "I keep the old seals wrapped, not buried.",
    ):
        assert_contains(helper, token)
    for token in (
        "Rebel fiefs",
        "loyalist fiefs",
        "rebel lord parties",
        "old ruler",
        "war age",
        "likely rebel victory",
        "script_sod_claimant_describe_active_wars_to_s1",
    ):
        assert_contains(house, token)
    assert_contains(faction_notes, "script_sod_claimant_describe_active_wars_to_s1")
    assert_contains(troop_notes, "Claimant politics")
    assert_contains(troop_notes, "old-ruler remnant")
    assert_contains(dialog_order, "trp_sod_strategy_advisor_plyr_sod_sa_war_room_answer_claimants.py")
    assert_contains(dialog_order, "trp_sod_strategy_advisor_sod_sa_war_room_claimants.py")
    assert_contains(dialog_order, "anyone_plyr_tavern_traveler_talk_claimant_wars.py")
    assert_contains(dialog_order, "anyone_lord_talk_claimant_allegiance.py")
    assert_contains(dialog_order, "anyone_supported_pretender_claimant_status.py")
    assert_contains(dialog_order, "anyone_pretender_claimant_status.py")
    assert_contains(advisor_player, "Which claimant wars could change the map?")
    assert_contains(advisor_answer, "script_sod_claimant_describe_active_wars_to_s1")
    assert_contains(traveler_player, "Any claimant courts stirring on the roads?")
    assert_contains(traveler_answer, "script_sod_claimant_describe_active_wars_to_s1")
    assert_contains(lord_player, "Where do you stand in the claimant wars?")
    assert_contains(lord_player, "script_sod_troop_has_claimant_dialog_to_reg")
    assert_contains(lord_answer, "script_sod_lord_describe_claimant_allegiance_to_s1")
    assert_contains(pretender_player, "How does your claim stand beyond our banners?")
    assert_contains(pretender_answer, "script_sod_pretender_describe_own_claimant_war_to_s1")
    assert_contains(pretender_start_player, "How does your claim stand beyond these halls?")
    assert_contains(pretender_start_answer, "script_sod_pretender_describe_own_claimant_war_to_s1")


def test_checklist_notes_scaffolding_targets() -> None:
    doc = read("docs/reports/pretender_system_audit.md")
    assert_contains(doc, "Claimant Civil War Overhaul Checklist")
    assert_contains(doc, "fac_kingdom_1_rebels")
    assert_contains(doc, "script_sod_initialize_claimant_civil_war_factions")


if __name__ == "__main__":
    test_rebel_counterpart_factions_exist()
    test_claimant_constants_exist()
    test_claimant_helper_wiring_exists()
    test_claimant_defection_wiring_exists()
    test_claimant_resolution_wiring_exists()
    test_claimant_compatibility_guards_exist()
    test_kingdom_6_is_excluded_and_old_rebellion_path_remains()
    test_independent_claimant_scaffold_does_not_use_player_supporters_as_rebel_shell()
    test_claimant_player_facing_visibility_exists()
    test_checklist_notes_scaffolding_targets()
    print("test_claimant_civil_war_static: OK")
