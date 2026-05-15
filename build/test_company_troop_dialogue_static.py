from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_spokesperson_constants_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for token in (
        "sod_company_spokesperson_pay_arrears",
        "sod_company_spokesperson_thin_rations",
        "sod_company_spokesperson_wounded_care",
        "sod_company_spokesperson_hazard_pay",
        "sod_company_spokesperson_noble_honor",
        "sod_company_spokesperson_faith_rites",
        "sod_company_spokesperson_battle_promise_due",
        "sod_company_spokesperson_defeat_shock",
        "sod_company_spokesperson_victory_spoils",
        "sod_company_spokesperson_discipline_threat",
        "sod_company_spokesperson_response_pay_now",
        "sod_company_spokesperson_response_promise",
        "sod_company_spokesperson_response_battle_promise",
        "sod_company_spokesperson_response_ration_change",
        "sod_company_spokesperson_response_recreation",
        "sod_company_spokesperson_response_rites_wounded",
        "sod_company_spokesperson_response_public_honors",
        "sod_company_spokesperson_response_persuade",
        "sod_company_spokesperson_response_mediation",
        "sod_company_spokesperson_response_threaten",
        "sod_company_spokesperson_response_dismiss",
        "sod_company_spokesperson_response_hazard_pay",
        "sod_company_spokesperson_response_victory_feast",
        "sod_company_spokesperson_response_refuse_spectacle",
        "sod_company_spokesperson_response_company_offering",
    ):
        assert_contains(constants, token)


def test_spokesperson_state_and_scripts_exist() -> None:
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    dialogue = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    for token in (
        "$g_sod_company_last_spokesperson_incident_day",
        "$g_sod_company_spokesperson_type",
        "$g_sod_company_spokesperson_class",
        "$g_sod_company_spokesperson_severity",
        "$g_sod_company_spokesperson_mediator",
        "$g_sod_company_spokesperson_last_response",
        "$g_sod_company_last_spokesperson_incident_day",
    ):
        assert_contains(accounts, token)
        assert_contains(dialogue, token)
    for token in (
        "sod_company_dialogue_try_spokesperson_incident",
        "sod_company_dialogue_select_spokesperson_to_regs",
        "sod_company_dialogue_describe_spokesperson_to_s60",
        "sod_company_dialogue_describe_spokesperson_risk_to_s65",
        "sod_company_dialogue_get_mediator_strength_to_reg",
        "sod_company_dialogue_describe_battle_start_morale_to_s60",
        "sod_company_dialogue_process_battle_start_morale",
        "sod_company_dialogue_flag_post_battle_incident",
        "sod_company_dialogue_process_post_battle_prompt",
        "sod_company_dialogue_describe_post_battle_to_s66",
        "sod_company_dialogue_schedule_spokesperson_incident",
        "sod_company_dialogue_process_faith_value_action",
        "sod_company_dialogue_apply_response",
        "sod_company_dialogue_find_mediator_to_regs",
        "sod_company_dialogue_describe_mediator_to_s63",
        "script_sod_company_accounts_update_troop_category_morale",
        "script_sod_company_accounts_apply_pay_choice",
        "script_sod_company_accounts_set_pay_promise",
        "script_sod_company_accounts_set_battle_pay_promise",
        "script_sod_companion_dispatch_player_action",
        "$g_sod_company_faith_morale",
        "sod_company_spokesperson_faith_rites",
        "slot_troop_companion_approval",
        "slot_troop_companion_role",
        "sod_companion_role_quartermaster",
        "sod_companion_role_surgeon",
        "sod_companion_role_captain",
        "(ge, \":approval\", 45)",
        "(neg|troop_slot_ge, \":mediator\", slot_troop_companion_approval, 45)",
        "(try_for_range, \":companion\", companions_begin, companions_end)",
        "(assign, \":best_approval\", 44)",
        "script_sod_companion_get_approval_band_to_s68",
        "script_sod_companion_role_to_s68",
        "serving as {s66}",
        "Company spokesman: no trusted companion is ready",
        "Marnid frames the grievance as terms",
        "Bunduk speaks for the line first",
        "Ymira keeps the wound in view",
        "Jeremus turns the complaint toward triage",
        "Lezalit makes it a question of order",
        "Katrin names the practical truth",
        "Borcha reads the camp like a bad road",
        "Firentis speaks carefully of honor",
        "Artimenner reduces the anger to stores",
        "Klethi can speak to dirty bargains",
        "sod_companion_action_fair_pay",
        "sod_companion_action_threatened_troops",
        "sod_companion_action_strict_discipline",
        "sod_companion_action_empty_speech",
        "sod_companion_action_generous_rations",
        "sod_companion_action_wounded_pay",
        "skl_trade",
        "skl_surgery",
        "skl_pathfinding",
        "skl_leadership",
        "skl_persuasion",
        "script_sod_company_accounts_apply_recreation",
        "script_sod_company_accounts_apply_hazard_pay",
        "script_sod_company_accounts_apply_victory_feast",
        "script_sod_company_accounts_refuse_public_spectacle",
        "sod_companion_action_buy_slaves",
        "sod_companion_action_free_captives",
        "sod_companion_action_ymira_refugee_expedience",
        "faith-minded troops are troubled by captive traffic",
        "sod_company_dialogue_schedule_spokesperson_incident",
        "script_sod_company_accounts_get_battle_morale_context_to_regs",
        "battle-pay will be counted after this fight",
        "unpaid coin and strained accounts",
        "hunger has followed the company onto the field",
        "one part of the host is wavering",
        "pay, food, and command are steady",
        "Victory may steady them",
        "sod_company_spokesperson_victory_spoils",
        "sod_company_spokesperson_defeat_shock",
        "Aftermath: battle-pay is now a live account",
        "Aftermath: victory is still warm",
        "Aftermath: defeat or hard fighting",
        "Spokesperson risk:",
        "Best mediator:",
        "Spokesperson risk: victory claim",
        "Spokesperson risk: defeat shock",
        "Spokesperson risk: discipline threat",
        "A faith-bound spokesman waits",
        "A victory spokesman stands",
        "A shaken spokesman comes forward",
        "A hard-eyed spokesman keeps his voice level",
    ):
        assert_contains(dialogue, token)


def test_spokesperson_menu_is_registered() -> None:
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    accounts_menu = read("src/menus/camp/company_accounts.py")
    menu = read("src/menus/camp/company_spokesperson.py")
    trigger = read("src/triggers/ST02_every_hour/entry_0086.py")
    dialogue_start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_sod_company_spokesperson_start.py")
    assert_contains(order, "camp/company_spokesperson.py")
    assert_contains(dialog_order, "ZA01_startup_and_dispatch/anyone_sod_company_spokesperson_start.py")
    assert_contains(accounts_menu, "mnu_company_spokesperson_incident")
    assert_not_contains(accounts_menu, "Hear the company's spokesman.")
    assert_not_contains(accounts_menu, "Hear the current company petition.")
    assert_contains(accounts_menu, "company_petition_spokesperson")
    assert_contains(accounts_menu, "company_desertion_spokesperson")
    assert_contains(accounts_menu, "company_mutiny_spokesperson")
    assert_contains(trigger, "script_sod_company_dialogue_find_spokesperson_troop_to_reg")
    assert_contains(trigger, "start_map_conversation, reg63")
    assert_contains(dialogue_start, "sod_company_spokesperson_response")
    assert_contains(dialogue_start, "script_sod_company_dialogue_apply_response")
    assert_contains(dialogue_start, "(eq, \"$g_sod_company_spokesperson_type\", sod_company_spokesperson_victory_spoils)")
    assert_contains(dialogue_start, "(eq, \"$g_sod_company_victory_feast_available\", 1)")
    assert_contains(dialogue_start, "(gt, \":days_since_feast\", 3)")
    assert_contains(dialogue_start, "Name the fighters who carried the day.")
    assert_contains(dialogue_start, "Open the stores for a victory feast.")
    assert_contains(dialogue_start, "No ceremony. We keep marching.")
    assert_not_contains(dialogue_start, "The company has earned public honors.")
    assert_not_contains(dialogue_start, "Make a victory feast before pride turns sour.")
    assert_not_contains(dialogue_start, "No spectacle. We keep marching.")
    for token in (
        "company_spokesperson_pay_now",
        "company_spokesperson_promise",
        "company_spokesperson_battle_promise",
        "company_spokesperson_rations",
        "company_spokesperson_wounded",
        "company_spokesperson_hazard_pay",
        "company_spokesperson_offering",
        "company_spokesperson_mediator",
        "company_spokesperson_threaten",
        "company_spokesperson_dismiss",
        "script_sod_company_dialogue_describe_spokesperson_to_s60",
        "script_sod_company_dialogue_apply_response",
    ):
        assert_contains(menu, token)
    dialogue = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    assert_contains(dialogue, "No one is ready to speak formally")
    assert_contains(dialogue, "(party_stack_get_size, \":stack_size\", \"p_main_party\", \":stack_no\")")
    assert_contains(dialogue, "(gt, \":stack_size\", 0)")
    assert_contains(dialogue, "(main_party_has_troop, \"$g_sod_company_spokesperson_mediator\")")
    assert_contains(dialogue, "(troop_slot_ge, \"$g_sod_company_spokesperson_mediator\", slot_troop_companion_approval, 45)")
    assert_contains(dialogue, "(assign, \":speaker\", \"$g_sod_company_spokesperson_mediator\")")


def test_checklist_tracks_milestone_one() -> None:
    checklist = read("docs/company/COMPANY_TROOP_DIALOGUE_INCIDENTS_CHECKLIST.md")
    for token in (
        "- [x] Add incident state/constants.",
        "- [x] Add incident selection helper.",
        "- [x] Add camp menu for current spokesperson.",
        "- [x] Add generic response application.",
        "- [x] Add static test.",
        "- [x] Add option from petition/desertion/mutiny menus",
    ):
        assert_contains(checklist, token)


def test_class_specific_voice_and_report_polish() -> None:
    checklist = read("docs/company/COMPANY_TROOP_DIALOGUE_INCIDENTS_CHECKLIST.md")
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    dialogue = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    menu = read("src/menus/camp/company_accounts.py")
    for token in (
        "Contract-minded troops",
        "rations ({reg65})",
        "noble honor ({reg65})",
        "faith and rites ({reg65})",
        "script_sod_company_dialogue_describe_spokesperson_risk_to_s65",
        "trusted mediation turns anger into terms",
        "weak mediation quiets the nearest voices",
        "{s65}",
    ):
        assert_contains(dialogue + accounts, token)
    for token in (
        "company_petition_spokesperson",
        "company_desertion_spokesperson",
        "company_mutiny_spokesperson",
    ):
        assert_contains(menu, token)
    for token in (
        "- [x] Implement mercenary captain incident.",
        "- [x] Implement enlisted spokesman incident.",
        "- [x] Implement noble retainer incident.",
        "- [x] Implement faith troop voice incident.",
        "- [x] Add report watch-point text for each.",
        "- [x] Trigger after slavery, mercy, or rites-related choices when faith troops are present.",
        "- [x] Add role/approval strength checks.",
        "- [x] Failed mediation should still be characterful",
        "- [x] Add companion approval hooks for dismissal, threats, and fair settlements.",
        "- [x] Add unique mediator flavor lines for first pass companions.",
        "- [x] Companion depth hooks receive mediation and harsh-response events.",
        "- [x] Assert mediator companions are named in script/report text.",
        "- [x] Assert company accounts report mentions spokesperson risk and mediator.",
    ):
        assert_contains(checklist, token)


def test_battle_start_morale_feedback_is_hooked() -> None:
    checklist = read("docs/company/COMPANY_TROOP_DIALOGUE_INCIDENTS_CHECKLIST.md")
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    lead_charge = read("src/mission_templates/0010_lead_charge/lead_charge.py")
    for token in (
        "script_sod_company_dialogue_process_battle_start_morale",
        "script_sod_battle_initialize_morale_context",
    ):
        assert_contains(preamble, token)
    assert_contains(lead_charge, "script_sod_company_dialogue_process_battle_start_morale")
    for token in (
        "- [x] Add battle-start morale feedback script.",
        "- [x] Hook mission start.",
        "- [x] Add one short battle-start message when morale state is notable.",
        "- [x] Active battle-promise message when the player has promised pay after the fight.",
        "- [x] Avoid spam: only one message per battle start.",
        "- [x] Use company-account category morale state already calculated for in-battle cohesion.",
        "- [x] Assert battle-start mission hook calls morale feedback script.",
    ):
        assert_contains(checklist, token)


def test_post_battle_prompt_pressure_is_hooked() -> None:
    checklist = read("docs/company/COMPANY_TROOP_DIALOGUE_INCIDENTS_CHECKLIST.md")
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    dialogue = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    describe_start = dialogue.index('("sod_company_dialogue_describe_spokesperson_to_s60"')
    describe_body = dialogue[describe_start:dialogue.index('("sod_company_dialogue_describe_battle_start_morale_to_s60"', describe_start)]
    for token in (
        "script_sod_company_dialogue_process_post_battle_prompt",
        "script_sod_company_dialogue_describe_post_battle_to_s66",
        "sod_company_accounts_record_battle_victory",
        "sod_company_accounts_record_battle_defeat",
        "{s66}",
        "Settle casualty care first; any ceremony should come through a camp spokesman",
        "the accounts screen keeps to pay, rations, and recovery",
        "(eq, \"$g_sod_company_spokesperson_type\", sod_company_spokesperson_victory_spoils)",
        "(eq, \"$g_sod_company_victory_feast_available\", 1)",
    ):
        assert_contains(accounts + dialogue, token)
    assert_contains(describe_body, '(eq, "$g_sod_company_spokesperson_dialogue_active", 0)')
    assert_contains(describe_body, "script_sod_company_dialogue_try_spokesperson_incident")
    assert_not_contains(dialogue, "Company accounts can pay casualty care, share spoils, hold honors")
    assert_not_contains(dialogue, "The accounts menu can turn triumph into pay, honors")
    for token in (
        "- [x] Add post-victory prompt state.",
        "- [x] Add post-defeat prompt state.",
        "- [x] Improve report lines for recent battle aftermath.",
        "- [x] Post-battle victory hook can flag victory-spoils or wounded-care incidents.",
        "- [x] Total defeat hook can flag defeat-shock incidents.",
        "- [x] Assert victory and defeat hooks can create post-battle incident pressure.",
    ):
        assert_contains(checklist, token)


def test_hourly_scheduling_and_source_of_truth() -> None:
    checklist = read("docs/company/COMPANY_TROOP_DIALOGUE_INCIDENTS_CHECKLIST.md")
    hourly = read("src/triggers/ST02_every_hour/entry_0133.py")
    menu = read("src/menus/camp/company_spokesperson.py")
    dialogue = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    companion = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "script_sod_company_accounts_process_petition_check",
        "script_sod_company_accounts_process_desertion_check",
        "script_sod_company_accounts_process_mutiny_check",
        "script_sod_company_dialogue_schedule_spokesperson_incident",
    ):
        assert_contains(hourly, token)
    for token in (
        "company_spokesperson_recreation",
        "company_spokesperson_persuade",
        "sod_company_spokesperson_response_recreation",
        "sod_company_spokesperson_response_persuade",
        "sod_company_spokesperson_response_hazard_pay",
        "sod_company_spokesperson_response_victory_feast",
        "sod_company_spokesperson_response_refuse_spectacle",
        "sod_company_spokesperson_response_company_offering",
    ):
        assert_contains(menu + dialogue, token)
    assert_contains(companion, "script_sod_company_dialogue_process_faith_value_action")
    for token in (
        "- [x] Daily/hourly company pressure processing can schedule spokesperson incidents.",
        "- [x] Company-account pay/ration/recreation helpers remain the source of actual state changes.",
        "- [x] Keep helper outputs register-safe for the current Module System register limit.",
        "- [x] Relevant skill where useful.",
    ):
        assert_contains(checklist, token)


if __name__ == "__main__":
    test_spokesperson_constants_exist()
    test_spokesperson_state_and_scripts_exist()
    test_spokesperson_menu_is_registered()
    test_checklist_tracks_milestone_one()
    test_class_specific_voice_and_report_polish()
    test_battle_start_morale_feedback_is_hooked()
    test_post_battle_prompt_pressure_is_hooked()
    test_hourly_scheduling_and_source_of_truth()
    print("test_company_troop_dialogue_static: OK")
