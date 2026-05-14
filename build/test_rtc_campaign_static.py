# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def test_act_i_salvage_paths_exist_but_are_parked_from_startup() -> None:
    menu = read("src/menus/start_game/rtc_last_smoke.py")
    script = read("src/scripts/ZG_quests/sod_rtc_last_smoke_resolve.py")
    init = read("src/scripts/ZG_quests/sod_rtc_initialize_campaign_state.py")
    start = read("src/menus/0000_hardcoded_mb1011/choose_skill.py")
    party = read("src/scripts/ZC_parties/sod_initialize_party.py")
    assert_contains(start, '(assign, "$g_sod_rtc_enabled", 0)')
    assert_contains(start, '(jump_to_menu, "mnu_banner_selection")')
    assert '"script_sod_rtc_initialize_campaign_state"' not in start
    assert '(jump_to_menu, "mnu_rtc_last_smoke")' not in start
    assert_contains(party, '"sod_apply_rtc_starting_salvage_bonus"')
    assert_contains(party, "party_wound_members")
    assert_contains(init, "qst_rtc_final_confrontation")
    assert_contains(init, "slot_quest_target_party")
    assert_contains(init, "slot_quest_target_party_template")
    assert_contains(init, '(quest_set_slot, "qst_rtc_last_smoke", slot_quest_target_troop, "trp_rtc_garran_ashwake")')
    assert_contains(init, '(quest_set_slot, "qst_rtc_borrowed_names", slot_quest_target_troop, "trp_rtc_lysara_veyne")')
    assert_contains(init, '(quest_set_slot, "qst_rtc_hound_sign", slot_quest_target_troop, "trp_rtc_imperial_courier")')
    assert_contains(init, "(try_for_range, \":rtc_quest\", \"qst_rtc_last_smoke\", \":rtc_quests_end\")")
    party_templates = read("compile/module_party_templates.py")
    assert_contains(party_templates, '("sod_diplomatic_envoy"')
    assert_contains(party_templates, "trp_swadian_messenger")
    assert_contains(menu, '"script_sod_rtc_prepare_temporary_target", "qst_rtc_last_smoke", "pt_sod_diplomatic_envoy"')
    assert_contains(script, "Road event: the survivors' first choice is tied to")
    assert_contains(script, "slot_quest_target_party")
    assert_contains(menu, "Antares taught you")
    assert_contains(menu, "Marina taught you")
    assert_contains(menu, "The One asks")
    assert_contains(script, "Founding pressure: Antarian memory")
    assert_contains(script, "Founding pressure: Marinan memory")
    assert_contains(script, "Founding pressure: The One's faithful")
    for salvage in (
        "sod_rtc_salvage_wounded",
        "sod_rtc_salvage_baggage",
        "sod_rtc_salvage_papers",
        "sod_rtc_salvage_abandoned",
    ):
        assert_contains(menu, f'"script_sod_rtc_last_smoke_resolve", {salvage}')
        assert_contains(script, salvage)
    assert menu.count('(jump_to_menu, "mnu_rtc_borrowed_names")') == 4


def test_borrowed_names_identity_paths_are_wired() -> None:
    menu = read("src/menus/start_game/rtc_borrowed_names.py")
    script = read("src/scripts/ZG_quests/sod_rtc_borrowed_names_choose_identity.py")
    assert_contains(menu, "The wounded you saved lie close enough")
    assert_contains(menu, "The baggage and stores you saved")
    assert_contains(menu, "The military papers you saved")
    assert_contains(menu, "The road you abandoned")
    for reputation in (
        "sod_rtc_reputation_foreign_noble",
        "sod_rtc_reputation_free_captain",
        "sod_rtc_reputation_trade_operator",
        "sod_rtc_reputation_refugee",
        "sod_rtc_reputation_avenger",
    ):
        assert_contains(menu, f'"script_sod_rtc_borrowed_names_choose_identity", {reputation}')
        assert_contains(script, reputation)
    assert_contains(script, "slot_quest_rtc_noble_trust")
    assert_contains(script, "slot_quest_rtc_commoner_trust")
    assert_contains(script, "slot_quest_rtc_merchant_trust")
    assert_contains(script, "sod_rtc_method_trade")
    assert_contains(script, "sod_rtc_pressure_rising")
    assert_contains(script, "Camp event: Lysara's ledger closed over testimony")
    assert_contains(script, '(neq, ":camp_target_party", "p_main_party")')
    assert_contains(script, "remove_party")
    assert_contains(script, '(quest_set_slot, "qst_rtc_borrowed_names", slot_quest_target_party, -1)')
    assert_contains(script, '(quest_set_slot, "qst_rtc_hound_sign", slot_quest_target_party, -1)')
    assert menu.count('(jump_to_menu, "mnu_rtc_hound_sign")') == 5


def test_hound_sign_and_door_methods_are_interactive() -> None:
    hound_menu = read("src/menus/start_game/rtc_hound_sign.py")
    hound_resolve = read("src/scripts/ZG_quests/sod_rtc_hound_sign_resolve.py")
    door_menu = read("src/menus/start_game/rtc_door_into_calradia.py")
    door_contact = read("src/scripts/ZG_quests/sod_rtc_door_into_calradia_choose_contact.py")
    act_i_cleanup = read("src/scripts/ZG_quests/sod_rtc_act_i_cleanup_targets.py")
    assert_contains(hound_menu, "The camp expects you to take proof openly")
    assert_contains(hound_menu, "The camp expects quiet hands")
    assert_contains(hound_menu, "The wounded you saved can still speak")
    assert_contains(hound_menu, "The stores you saved give Garran")
    assert_contains(hound_menu, "The papers you saved make the pattern sharper")
    assert_contains(hound_menu, '"script_sod_rtc_prepare_temporary_target", "qst_rtc_hound_sign", "pt_sod_diplomatic_envoy", "p_main_party", 2, 1')
    assert_contains(hound_resolve, "World event: the Hound sign now points to")
    assert_contains(hound_resolve, "slot_quest_target_party")
    assert_contains(hound_resolve, "Hound Sign method: you took the proof openly")
    assert_contains(hound_resolve, "Hound Sign method: you traced supply marks")
    assert_contains(hound_resolve, "The wounded survivors made the Hound sign")
    assert_contains(hound_resolve, "The saved baggage made the Hound sign")
    assert_contains(hound_resolve, "The saved papers made the Hound sign")
    assert_contains(door_menu, "Your proof was taken openly")
    assert_contains(door_menu, "Your proof is supply and ration marks")
    assert_contains(door_menu, "The wounded you saved slow the column")
    assert_contains(door_menu, "The baggage you saved gives the column")
    assert_contains(door_menu, "The papers you saved give the warning shape")
    assert_contains(door_contact, ":proof_method")
    assert_contains(door_contact, ":salvage")
    assert_contains(door_contact, "Your open proof matched the door you chose")
    assert_contains(door_contact, "Your supply proof matched the guild door")
    assert_contains(door_contact, "The wounded you saved matched the first door")
    assert_contains(door_contact, "The baggage you saved matched the guild door")
    assert_contains(door_contact, "The papers you saved matched the first door")
    assert_contains(door_contact, "script_sod_rtc_act_i_cleanup_targets")
    assert_contains(act_i_cleanup, '"sod_rtc_act_i_cleanup_targets"')
    assert_contains(act_i_cleanup, '(try_for_range, ":quest_no", "qst_rtc_last_smoke", "qst_rtc_price_of_bread")')
    assert_contains(act_i_cleanup, "remove_party")
    assert_contains(act_i_cleanup, "slot_quest_target_party_template")


def test_price_of_bread_listed_paths_are_wired() -> None:
    menu = read("src/menus/start_game/rtc_price_of_bread.py")
    script = read("src/scripts/ZG_quests/sod_rtc_price_of_bread_resolve.py")
    for outcome in ("1", "2", "4", "5"):
        assert_contains(menu, f'"script_sod_rtc_price_of_bread_resolve", {outcome}')
    assert_contains(menu, "script_sod_rtc_price_of_bread_bind_world")
    assert_contains(menu, "slot_quest_target_center")
    assert_contains(menu, "slot_quest_target_amount")
    assert_contains(script, "script_sod_rtc_price_of_bread_bind_world")
    assert_contains(script, "script_sod_rtc_price_of_bread_apply_local_aftermath")
    assert_contains(script, "script_sod_rtc_price_of_bread_describe_aftermath_to_s49")
    assert_contains(script, "script_sod_rtc_price_of_bread_cleanup_bandit_target")
    assert_contains(script, "Because the wounded survived the smoke")
    assert_contains(script, "Because the baggage survived the smoke")
    assert_contains(script, "Because the papers survived the smoke")
    assert_contains(script, "Because the village heard you first")
    assert_contains(script, "Because the guild heard you first")
    assert menu.count('(jump_to_menu, "mnu_rtc_three_offers")') == 6


def test_price_of_bread_world_memory_contract_is_wired() -> None:
    bind_world = read("src/scripts/ZG_quests/sod_rtc_price_of_bread_bind_world.py")
    aftermath = read("src/scripts/ZG_quests/sod_rtc_price_of_bread_apply_local_aftermath.py")
    rumor = read("src/scripts/ZG_quests/sod_rtc_price_of_bread_describe_aftermath_to_s49.py")
    prepare_bandits = read("src/scripts/ZG_quests/sod_rtc_price_of_bread_prepare_bandit_target.py")
    cleanup_bandits = read("src/scripts/ZG_quests/sod_rtc_price_of_bread_cleanup_bandit_target.py")
    prepare_helper = read("src/scripts/ZG_quests/sod_rtc_prepare_temporary_target.py")
    rtc_world_target_sources = (
        read("src/menus/start_game/rtc_last_smoke.py"),
        read("src/menus/start_game/rtc_hound_sign.py"),
        read("src/scripts/ZG_quests/sod_rtc_three_offers_prepare_route_target.py"),
        read("src/scripts/ZG_quests/sod_rtc_first_recognition_prepare_witness_target.py"),
        read("src/scripts/ZG_quests/sod_rtc_war_of_witnesses_prepare_target.py"),
        read("src/scripts/ZG_quests/sod_rtc_last_road_prepare_strategy_target.py"),
        read("src/scripts/ZG_quests/sod_rtc_final_confrontation_prepare_target.py"),
    )
    for raw in rtc_world_target_sources:
        assert_not_contains(raw, '"pt_scout_party"')
    for token in (
        "slot_quest_target_center",
        "slot_quest_target_troop",
        "trp_rtc_tamsin_reedhand",
        "slot_quest_object_troop",
        "trp_rtc_celeste_di_marina",
        "slot_quest_giver_troop",
        "trp_rtc_brother_odran",
        "slot_quest_target_amount",
    ):
        assert_contains(bind_world, token)
    assert_contains(bind_world, "script_sod_rtc_price_of_bread_prepare_bandit_target")
    assert_contains(aftermath, "slot_quest_sod_chain_choice")
    assert_contains(aftermath, "script_change_player_relation_with_center")
    assert_contains(aftermath, "script_change_center_prosperity")
    assert_contains(rumor, "str_store_party_name_link")
    assert_contains(prepare_bandits, '"pt_bandits"')
    assert_contains(prepare_bandits, "slot_quest_target_party")
    assert_contains(prepare_bandits, "script_sod_rtc_prepare_temporary_target")
    assert_contains(prepare_helper, '"sod_rtc_prepare_temporary_target"')
    assert_contains(prepare_helper, "spawn_around_party")
    assert_contains(prepare_helper, "slot_quest_target_party_template")
    assert_contains(prepare_helper, "(quest_set_slot, \":quest_no\", slot_quest_target_party, -1)")
    assert_contains(cleanup_bandits, "remove_party")


def test_price_of_bread_memory_reaches_finale() -> None:
    continuity_files = (
        "src/menus/start_game/rtc_three_offers.py",
        "src/menus/start_game/rtc_companions_take_sides.py",
        "src/menus/start_game/rtc_first_recognition.py",
        "src/menus/start_game/rtc_crown_council.py",
        "src/menus/start_game/rtc_hounds_terms.py",
        "src/menus/start_game/rtc_war_of_witnesses.py",
        "src/menus/start_game/rtc_last_road.py",
        "src/menus/start_game/rtc_final_confrontation.py",
    )
    for path in continuity_files:
        raw = read(path)
        assert_contains(raw, "slot_quest_target_center")
        assert_contains(raw, "slot_quest_sod_chain_choice")

    handoff_scripts = (
        "src/scripts/ZG_quests/sod_rtc_price_of_bread_resolve.py",
        "src/scripts/ZG_quests/sod_rtc_three_offers_choose_route.py",
        "src/scripts/ZG_quests/sod_rtc_first_recognition_resolve.py",
        "src/scripts/ZG_quests/sod_rtc_crown_council_resolve.py",
        "src/scripts/ZG_quests/sod_rtc_hounds_terms_resolve.py",
        "src/scripts/ZG_quests/sod_rtc_war_of_witnesses_resolve.py",
        "src/scripts/ZG_quests/sod_rtc_last_road_resolve.py",
    )
    for path in handoff_scripts:
        raw = read(path)
        assert_contains(raw, "slot_quest_target_center")
        assert_contains(raw, "slot_quest_target_amount")


def test_three_offers_route_proof_target_is_wired() -> None:
    menu = read("src/menus/start_game/rtc_three_offers.py")
    constants = read("src/constants/module_constants.py")
    choose = read("src/scripts/ZG_quests/sod_rtc_three_offers_choose_route.py")
    companions = read("src/scripts/ZG_quests/sod_rtc_companions_take_sides_resolve.py")
    prepare = read("src/scripts/ZG_quests/sod_rtc_three_offers_prepare_route_target.py")
    cleanup = read("src/scripts/ZG_quests/sod_rtc_three_offers_cleanup_route_target.py")
    assert_contains(menu, "rtc_offer_bread_oath")
    assert_contains(menu, "rtc_offer_books_oath")
    assert_contains(menu, "rtc_offer_witness_oath")
    assert_contains(menu, "The wounded survivors are now living proof")
    assert_contains(menu, "The saved baggage makes the offers practical")
    assert_contains(menu, "Because the village heard you first")
    assert_contains(constants, "sod_rtc_offer_bread_oath")
    assert_contains(constants, "sod_rtc_offer_books_oath")
    assert_contains(constants, "sod_rtc_offer_witness_oath")
    assert_contains(choose, "script_sod_rtc_three_offers_prepare_route_target")
    assert_contains(prepare, "script_sod_rtc_prepare_temporary_target")
    assert_contains(choose, "slot_quest_target_party")
    assert_contains(choose, "slot_quest_target_party_template")
    assert_contains(choose, "You swore the bread oath")
    assert_contains(choose, "You swore by the books")
    assert_contains(choose, "You swore before witnesses")
    assert_contains(choose, "The wounded survivors bent the offer toward mercy")
    assert_contains(choose, "The saved baggage bent the offer toward logistics")
    assert_contains(choose, "The village contact bent the offer toward common testimony")
    assert_contains(choose, "sod_rtc_flag_witness_commoner")
    assert_contains(choose, "sod_rtc_flag_witness_fourth")
    assert_contains(choose, "sod_rtc_flag_witness_noble")
    assert_contains(companions, "script_sod_rtc_three_offers_cleanup_route_target")
    for template in (
        '"pt_sod_diplomatic_envoy"',
        '"pt_merchant_caravan"',
        '"pt_bandits"',
    ):
        assert_contains(prepare, template)
    assert_contains(cleanup, "remove_party")


def test_first_recognition_witness_target_is_wired() -> None:
    menu = read("src/menus/start_game/rtc_first_recognition.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_first_recognition_resolve.py")
    council = read("src/scripts/ZG_quests/sod_rtc_crown_council_resolve.py")
    prepare = read("src/scripts/ZG_quests/sod_rtc_first_recognition_prepare_witness_target.py")
    cleanup = read("src/scripts/ZG_quests/sod_rtc_first_recognition_cleanup_witness_target.py")
    assert_contains(menu, "sod_rtc_offer_bread_oath")
    assert_contains(menu, "sod_rtc_offer_books_oath")
    assert_contains(menu, "sod_rtc_offer_witness_oath")
    assert_contains(resolve, "script_sod_rtc_first_recognition_prepare_witness_target")
    assert_contains(prepare, "script_sod_rtc_prepare_temporary_target")
    assert_contains(resolve, "slot_quest_target_party")
    assert_contains(resolve, "slot_quest_target_party_template")
    assert_contains(resolve, "The bread oath shaped first recognition")
    assert_contains(resolve, "The books oath shaped first recognition")
    assert_contains(resolve, "The witness oath shaped first recognition")
    assert_contains(council, "script_sod_rtc_first_recognition_cleanup_witness_target")
    for template in (
        '"pt_sod_diplomatic_envoy"',
        '"pt_merchant_caravan"',
        '"pt_bandits"',
    ):
        assert_contains(prepare, template)
    assert_contains(cleanup, "remove_party")


def test_companions_take_sides_has_interactive_answers() -> None:
    menu = read("src/menus/start_game/rtc_companions_take_sides.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_companions_take_sides_resolve.py")
    first_recognition = read("src/scripts/ZG_quests/sod_rtc_first_recognition_resolve.py")
    for oath in (
        "sod_rtc_offer_bread_oath",
        "sod_rtc_offer_books_oath",
        "sod_rtc_offer_witness_oath",
    ):
        assert_contains(menu, oath)
        assert_contains(resolve, oath)
    for option in (
        "rtc_companions_reassure",
        "rtc_companions_rebuke",
        "rtc_companions_compromise",
        "rtc_companions_ignore",
    ):
        assert_contains(menu, option)
    for answer in ("1", "2", "3", "4"):
        assert_contains(menu, f'"script_sod_rtc_companions_take_sides_resolve", {answer}')
    assert_contains(resolve, ":campfire_answer")
    assert_contains(resolve, "sod_companion_action_honorable_peace")
    assert_contains(resolve, "sod_companion_action_lezalit_ief_harsh")
    assert_contains(resolve, "sod_companion_action_orderly_profit")
    assert_contains(resolve, "sod_companion_action_retreat_or_fail")
    assert_contains(resolve, "The company heard the bread oath")
    assert_contains(resolve, "The company heard the books oath")
    assert_contains(resolve, "The company heard the witness oath")
    assert_contains(first_recognition, "slot_quest_sod_chain_choice")
    assert_contains(first_recognition, "qst_rtc_crown_council")


def test_hounds_terms_envoy_world_target_is_wired() -> None:
    menu = read("src/menus/start_game/rtc_hounds_terms.py")
    council = read("src/scripts/ZG_quests/sod_rtc_crown_council_resolve.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_hounds_terms_resolve.py")
    prepare = read("src/scripts/ZG_quests/sod_rtc_hounds_terms_prepare_envoy.py")
    cleanup = read("src/scripts/ZG_quests/sod_rtc_hounds_terms_cleanup_envoy.py")
    handle = read("src/scripts/ZG_quests/sod_rtc_hounds_terms_handle_envoy.py")
    witness_war_menu = read("src/menus/start_game/rtc_war_of_witnesses.py")
    assert_contains(menu, "script_sod_rtc_hounds_terms_prepare_envoy")
    assert_contains(menu, "script_sod_rtc_hounds_terms_handle_envoy")
    assert_contains(menu, "The terms attack the bread oath directly")
    assert_contains(menu, "The terms attack the books oath directly")
    assert_contains(menu, "The terms attack the witness oath directly")
    assert_contains(menu, "rtc_terms_reject_release")
    assert_contains(menu, "rtc_terms_reject_detain")
    assert_contains(council, "script_sod_rtc_hounds_terms_prepare_envoy")
    assert_contains(resolve, "script_sod_rtc_hounds_terms_cleanup_envoy")
    assert_contains(resolve, "slot_quest_sod_chain_choice")
    assert_contains(resolve, "slot_quest_object_troop")
    assert_contains(resolve, "The Hound's terms tried to own the bread oath")
    assert_contains(resolve, "The Hound's terms tried to own the books oath")
    assert_contains(resolve, "The Hound's terms tried to own the witness oath")
    assert_contains(handle, "sod_companion_action_honorable_peace")
    assert_contains(handle, "sod_companion_action_diplomacy_betrayal")
    assert_contains(handle, "sod_companion_action_scout_warning")
    assert_contains(witness_war_menu, ":envoy_handling")
    assert_contains(prepare, '"pt_sod_diplomatic_envoy"')
    assert_contains(prepare, "script_sod_rtc_prepare_temporary_target")
    assert_contains(prepare, "slot_quest_target_party")
    assert_contains(cleanup, "remove_party")


def test_crown_council_evidence_tactics_are_wired() -> None:
    constants = read("src/constants/module_constants.py")
    menu = read("src/menus/start_game/rtc_crown_council.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_crown_council_resolve.py")
    assert_contains(constants, "sod_rtc_council_answer_bread_witness")
    assert_contains(constants, "sod_rtc_council_answer_merchant_books")
    assert_contains(menu, "rtc_council_bread_witness")
    assert_contains(menu, "rtc_council_merchant_books")
    assert_contains(menu, "Your bread oath has reached the council")
    assert_contains(menu, "Your books oath has reached the council")
    assert_contains(menu, "Your witness oath has reached the council")
    assert_contains(resolve, "Crown Council answer: the bread witness held")
    assert_contains(resolve, "Crown Council answer: the merchant books spoke")
    assert_contains(resolve, "Crown Council oath memory: the bread oath")
    assert_contains(resolve, "Crown Council oath memory: the books oath")
    assert_contains(resolve, "Crown Council oath memory: the witness oath")
    assert_contains(resolve, "sod_rtc_flag_witness_commoner")
    assert_contains(resolve, "sod_rtc_flag_witness_fourth")


def test_war_of_witnesses_world_target_is_wired() -> None:
    menu = read("src/menus/start_game/rtc_war_of_witnesses.py")
    constants = read("src/constants/module_constants.py")
    hounds = read("src/scripts/ZG_quests/sod_rtc_hounds_terms_resolve.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_war_of_witnesses_resolve.py")
    prepare = read("src/scripts/ZG_quests/sod_rtc_war_of_witnesses_prepare_target.py")
    cleanup = read("src/scripts/ZG_quests/sod_rtc_war_of_witnesses_cleanup_target.py")
    assert_contains(menu, "script_sod_rtc_war_of_witnesses_prepare_target")
    assert_contains(menu, "rtc_witness_envoy_leverage")
    assert_contains(menu, "The witness war comes for the bread oath first")
    assert_contains(menu, "The witness war comes for the books oath first")
    assert_contains(menu, "The witness war comes for the witness oath first")
    assert_contains(menu, "sod_rtc_witness_war_envoy_leverage")
    assert_contains(constants, "sod_rtc_witness_war_envoy_leverage")
    assert_contains(hounds, "script_sod_rtc_war_of_witnesses_prepare_target")
    assert_contains(prepare, "script_sod_rtc_prepare_temporary_target")
    assert_contains(resolve, ":envoy_handling")
    assert_contains(resolve, "slot_quest_sod_chain_choice")
    assert_contains(resolve, "slot_quest_object_troop")
    assert_contains(resolve, "sod_rtc_witness_war_envoy_leverage")
    assert_contains(resolve, "You used the detained envoy as hard leverage")
    assert_contains(resolve, "The bread oath survived the witness war")
    assert_contains(resolve, "The books oath survived the witness war")
    assert_contains(resolve, "The witness oath survived the witness war")
    assert_contains(resolve, "Because you detained the envoy")
    assert_contains(resolve, "qst_rtc_last_road")
    assert_contains(resolve, "script_sod_rtc_war_of_witnesses_cleanup_target")
    for template in (
        '"pt_sod_diplomatic_envoy"',
        '"pt_merchant_caravan"',
        '"pt_bandits_awaiting_ransom"',
        '"pt_bandits"',
    ):
        assert_contains(prepare, template)
    assert_contains(prepare, "slot_quest_target_party")
    assert_contains(cleanup, "remove_party")


def test_last_road_strategy_world_target_is_wired() -> None:
    menu = read("src/menus/start_game/rtc_last_road.py")
    constants = read("src/constants/module_constants.py")
    witness_war = read("src/scripts/ZG_quests/sod_rtc_war_of_witnesses_resolve.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_last_road_resolve.py")
    prepare = read("src/scripts/ZG_quests/sod_rtc_last_road_prepare_strategy_target.py")
    cleanup = read("src/scripts/ZG_quests/sod_rtc_last_road_cleanup_strategy_target.py")
    assert_contains(menu, "script_sod_rtc_last_road_prepare_strategy_target")
    assert_contains(menu, ":envoy_handling")
    assert_contains(menu, "The detained envoy still changes the road")
    assert_contains(menu, "The last road carries the bread oath forward")
    assert_contains(menu, "The last road carries the books oath forward")
    assert_contains(menu, "The last road carries the witness oath forward")
    assert_contains(menu, "rtc_last_turn_accusation")
    assert_contains(constants, "sod_rtc_last_road_turn_accusation")
    assert_contains(witness_war, "script_sod_rtc_last_road_prepare_strategy_target")
    assert_contains(witness_war, "slot_quest_sod_chain_choice")
    assert_contains(resolve, "script_sod_rtc_last_road_prepare_strategy_target")
    assert_contains(resolve, "script_sod_rtc_last_road_cleanup_strategy_target")
    assert_contains(resolve, ":envoy_handling")
    assert_contains(resolve, "slot_quest_object_troop")
    assert_contains(resolve, "The detained envoy shapes the last road")
    assert_contains(resolve, "The bread oath shapes the last road")
    assert_contains(resolve, "The books oath shapes the last road")
    assert_contains(resolve, "The witness oath shapes the last road")
    assert_contains(resolve, "turn the accusation back")
    assert_contains(resolve, "sod_companion_action_diplomacy_betrayal")
    assert_contains(resolve, "sod_companion_action_honorable_peace")
    assert_contains(resolve, "qst_rtc_final_confrontation")
    assert_contains(resolve, "slot_quest_sod_chain_choice")
    assert_contains(prepare, ":force_refresh")
    assert_contains(prepare, "script_sod_rtc_prepare_temporary_target")
    assert_contains(prepare, "sod_rtc_last_road_turn_accusation")
    for template in (
        '"pt_kingdom_caravan_party"',
        '"pt_sod_diplomatic_envoy"',
        '"pt_bandits"',
    ):
        assert_contains(prepare, template)
    assert_contains(prepare, "slot_quest_target_party")
    assert_contains(cleanup, "remove_party")


def test_final_confrontation_world_target_is_wired() -> None:
    menu = read("src/menus/start_game/rtc_final_confrontation.py")
    last_road = read("src/scripts/ZG_quests/sod_rtc_last_road_resolve.py")
    resolve = read("src/scripts/ZG_quests/sod_rtc_final_confrontation_resolve.py")
    prepare = read("src/scripts/ZG_quests/sod_rtc_final_confrontation_prepare_target.py")
    cleanup = read("src/scripts/ZG_quests/sod_rtc_final_confrontation_cleanup_target.py")
    assert_contains(menu, "script_sod_rtc_final_confrontation_prepare_target")
    assert_contains(menu, ":envoy_handling")
    assert_contains(menu, "The detained envoy's shadow")
    assert_contains(menu, "The bread oath reaches the final hour")
    assert_contains(menu, "The books oath reaches the final hour")
    assert_contains(menu, "The witness oath reaches the final hour")
    assert_contains(menu, "sod_rtc_last_road_turn_accusation")
    assert_contains(last_road, "script_sod_rtc_final_confrontation_prepare_target")
    assert_contains(last_road, "slot_quest_sod_chain_choice")
    assert_contains(resolve, "script_sod_rtc_final_confrontation_prepare_target")
    assert_contains(resolve, "script_sod_rtc_final_confrontation_cleanup_target")
    assert_contains(resolve, ":envoy_handling")
    assert_contains(resolve, "slot_quest_object_troop")
    assert_contains(resolve, ":last_strategy")
    assert_contains(resolve, "The bread oath survives the final hour")
    assert_contains(resolve, "The books oath survives the final hour")
    assert_contains(resolve, "The witness oath survives the final hour")
    assert_contains(resolve, "sod_rtc_last_road_turn_accusation")
    assert_contains(resolve, "Because the last road turned the accusation back")
    assert_contains(resolve, "The ending still carries")
    assert_contains(resolve, "sod_companion_action_diplomacy_betrayal")
    assert_contains(resolve, "sod_companion_action_honorable_peace")
    assert_contains(resolve, "script_change_player_relation_with_center")
    assert_contains(prepare, ":force_refresh")
    assert_contains(prepare, "script_sod_rtc_prepare_temporary_target")
    for template in (
        '"pt_sod_diplomatic_envoy"',
        '"pt_bandits"',
    ):
        assert_contains(prepare, template)
    assert_contains(prepare, "slot_quest_target_party")
    assert_contains(cleanup, "remove_party")


def test_terminal_failures_return_to_live_play() -> None:
    crown_council = read("src/menus/start_game/rtc_crown_council.py")
    hounds_terms = read("src/menus/start_game/rtc_hounds_terms.py")
    last_road = read("src/menus/start_game/rtc_last_road.py")
    final = read("src/menus/start_game/rtc_final_confrontation.py")
    assert_contains(crown_council, '(jump_to_menu, "mnu_banner_selection")')
    assert_contains(hounds_terms, '(jump_to_menu, "mnu_banner_selection")')
    assert_contains(last_road, '(jump_to_menu, "mnu_banner_selection")')
    assert final.count('(jump_to_menu, "mnu_banner_selection")') == 5


def test_endings_are_queryable_after_final_resolution() -> None:
    constants = read("src/constants/module_constants.py")
    final = read("src/scripts/ZG_quests/sod_rtc_final_confrontation_resolve.py")
    archive = read("src/scripts/ZG_quests/sod_rtc_archive_campaign_ending.py")
    assert_contains(constants, "slot_quest_rtc_final_ending")
    assert_contains(constants, "slot_quest_rtc_successor_unlock")
    assert_contains(constants, "sod_rtc_flag_envoy_accusation_turned")
    assert_contains(final, '"script_sod_rtc_archive_campaign_ending"')
    assert_contains(final, "sod_rtc_flag_envoy_accusation_turned")
    assert_contains(archive, "sod_rtc_flag_envoy_accusation_turned")
    assert_contains(archive, "won a public accusation battle")
    assert_contains(archive, "The first oath of this crown was bread")
    assert_contains(archive, "The first oath of this crown was books")
    assert_contains(archive, "The first oath of this crown was witness")
    for ending in (
        "sod_rtc_ending_crown_of_law",
        "sod_rtc_ending_crown_of_iron",
        "sod_rtc_ending_crown_of_coin",
        "sod_rtc_ending_crown_of_ashes",
        "sod_rtc_ending_crown_of_faith",
        "sod_rtc_ending_crown_of_vengeance",
        "sod_rtc_ending_crown_of_return",
        "sod_rtc_ending_crown_of_empire",
        "sod_rtc_ending_unworn_crown",
    ):
        assert_contains(archive, ending)


if __name__ == "__main__":
    test_act_i_salvage_paths_exist_but_are_parked_from_startup()
    test_borrowed_names_identity_paths_are_wired()
    test_hound_sign_and_door_methods_are_interactive()
    test_price_of_bread_listed_paths_are_wired()
    test_price_of_bread_world_memory_contract_is_wired()
    test_price_of_bread_memory_reaches_finale()
    test_three_offers_route_proof_target_is_wired()
    test_first_recognition_witness_target_is_wired()
    test_companions_take_sides_has_interactive_answers()
    test_hounds_terms_envoy_world_target_is_wired()
    test_crown_council_evidence_tactics_are_wired()
    test_war_of_witnesses_world_target_is_wired()
    test_last_road_strategy_world_target_is_wired()
    test_final_confrontation_world_target_is_wired()
    test_terminal_failures_return_to_live_play()
    test_endings_are_queryable_after_final_resolution()
    print("test_rtc_campaign_static: OK")
