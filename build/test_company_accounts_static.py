from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def test_company_account_constants_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for token in (
        "sod_company_pay_choice_full",
        "sod_company_troop_class_enlisted",
        "sod_company_troop_class_mercenary",
        "sod_company_troop_class_noble",
        "sod_company_troop_class_faith",
        "sod_company_pay_choice_half",
        "sod_company_pay_choice_bonus",
        "sod_company_pay_choice_delay",
        "sod_company_pay_choice_veterans",
        "sod_company_pay_choice_wounded",
        "sod_company_growth_recruit",
        "sod_company_growth_upgrade",
        "sod_company_promise_response_standard",
        "sod_company_threat_response_discipline",
        "sod_company_pay_confidence_trusted",
        "sod_company_pay_confidence_steady",
        "sod_company_pay_confidence_watchful",
        "sod_company_pay_confidence_doubtful",
        "sod_company_pay_confidence_angry",
        "sod_company_pay_confidence_broken",
        "sod_company_camp_strain_calm",
        "sod_company_camp_strain_frayed",
        "sod_company_camp_strain_bitter",
        "sod_company_camp_strain_dangerous",
        "sod_company_camp_strain_splintering",
        "sod_company_ration_policy_thin",
        "sod_company_ration_policy_standard",
        "sod_company_ration_policy_generous",
        "sod_company_ration_policy_officer_austerity",
        "sod_company_ration_confidence_well_fed",
        "sod_company_ration_confidence_adequate",
        "sod_company_ration_confidence_thin",
        "sod_company_ration_confidence_hungry",
        "sod_company_ration_confidence_starving",
        "sod_company_recreation_tavern_round",
        "sod_company_recreation_lodging",
        "sod_company_recreation_strict_discipline",
        "sod_company_recreation_arena_prestige",
        "sod_company_recreation_campfire",
        "sod_company_recreation_religious_rites",
        "sod_company_recreation_company_offering",
        "sod_company_recreation_wounded_care",
        "sod_company_recreation_tavern_rumors",
        "sod_company_recreation_own_coin",
        "sod_company_recreation_village_festival",
        "sod_company_recreation_incident_drunken_brawl",
        "sod_company_recreation_incident_gambling_debt",
        "sod_company_recreation_incident_missing_soldier",
        "sod_company_recreation_incident_insulted_noble",
        "sod_company_recreation_incident_mercenary_overindulgence",
        "sod_company_recreation_incident_local_fine",
        "sod_company_prestige_battle",
        "sod_company_prestige_tournament",
        "sod_company_noble_restlessness_calm",
        "sod_company_noble_restlessness_proud",
        "sod_company_noble_restlessness_restless",
        "sod_company_noble_restlessness_insulted",
        "sod_company_noble_restlessness_withdrawing",
        "sod_company_petition_pay_arrears",
        "sod_company_petition_thin_rations",
        "sod_company_petition_noble_restlessness",
        "sod_company_petition_camp_strain",
        "sod_company_petition_wounded_care",
        "sod_company_petition_stage_murmur",
        "sod_company_petition_stage_formal",
        "sod_company_petition_stage_urgent",
        "sod_company_desertion_stage_watching",
        "sod_company_desertion_stage_request",
        "sod_company_desertion_stage_urgent",
        "sod_company_desertion_response_paid",
        "sod_company_desertion_response_persuade",
        "sod_company_desertion_response_unpaid",
        "sod_company_desertion_response_forbid",
        "sod_company_desertion_response_battle_promise",
        "sod_company_mutiny_stage_warning",
        "sod_company_mutiny_stage_final_warning",
        "sod_company_mutiny_stage_breaking",
        "sod_company_mutiny_response_negotiate",
        "sod_company_mutiny_response_pay",
        "sod_company_mutiny_response_threaten",
        "sod_company_mutiny_response_drill",
        "sod_company_mutiny_resolution_settlement",
        "sod_company_mutiny_resolution_ringleaders_expelled",
        "sod_company_mutiny_resolution_deferred",
        "sod_company_mutiny_resolution_battle",
        "sod_companion_action_tavern_recreation",
        "sod_companion_action_religious_rites",
        "sod_companion_action_strict_discipline",
        "sod_companion_action_peaceful_desertion_allowed",
        "sod_companion_action_peaceful_desertion_forbidden",
        "sod_companion_action_threatened_troops",
        "sod_companion_action_mutiny_negotiated",
        "sod_companion_action_mutiny_suppressed",
        "sod_companion_action_fair_pay",
        "sod_companion_action_bonus_pay",
        "sod_companion_action_half_pay",
        "sod_companion_action_delayed_pay",
        "sod_companion_action_veteran_pay",
        "sod_companion_action_wounded_pay",
        "sod_companion_action_broken_pay_promise",
        "sod_companion_action_generous_rations",
        "sod_companion_action_thin_rations",
        "sod_companion_action_officer_austerity",
        "sod_companion_action_ration_feast",
        "sod_companion_action_petition_mediated",
        "sod_companion_action_drunken_disorder",
        "sod_companion_action_debt_honesty",
        "sod_companion_action_road_practicality",
        "sod_companion_action_empty_speech",
    ):
        assert_contains(constants, token)


def test_company_account_scripts_exist() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    for token in (
        "sod_company_accounts_initialize",
        "sod_company_accounts_get_current_company_weekly_wage_to_reg",
        "sod_company_accounts_accrue_wages",
        "sod_company_accounts_get_due_to_regs",
        "sod_company_accounts_set_pay_promise",
        "sod_company_accounts_process_pay_promise",
        "sod_company_accounts_set_battle_pay_promise",
        "sod_company_accounts_process_battle_promise_aftermath",
        "sod_company_accounts_apply_threat",
        "sod_company_accounts_describe_promise_to_s50",
        "sod_company_accounts_find_petition_mediator_to_regs",
        "sod_company_accounts_apply_pay_choice",
        "sod_company_accounts_update_morale_pressure",
        "sod_company_accounts_update_troop_category_morale",
        "sod_company_accounts_describe_to_s20",
        "sod_company_accounts_get_pay_confidence_band_to_reg",
        "sod_company_accounts_get_camp_strain_band_to_reg",
        "sod_company_accounts_set_ration_policy",
        "sod_company_accounts_apply_faith_conduct",
        "sod_company_accounts_record_company_growth",
        "sod_company_accounts_get_battle_morale_context_to_regs",
        "sod_company_accounts_apply_ration_feast",
        "sod_company_accounts_apply_victory_feast",
        "sod_company_accounts_update_ration_pressure",
        "sod_company_accounts_adjust_food_consumption_to_reg",
        "sod_company_accounts_describe_rations_to_s23",
        "sod_company_accounts_get_ration_confidence_band_to_reg",
        "sod_company_accounts_get_recreation_cost_to_regs",
        "sod_company_accounts_get_troop_class",
        "sod_company_accounts_describe_local_recreation_to_s54",
        "sod_company_accounts_apply_recreation",
        "sod_company_accounts_try_recreation_incident",
        "sod_company_accounts_apply_arena_prestige",
        "sod_company_accounts_describe_recreation_to_s26",
        "sod_company_accounts_describe_tavern_rumors_to_s30",
        "sod_company_accounts_count_noble_troops_to_regs",
        "sod_company_accounts_describe_category_morale_to_s58",
        "sod_company_accounts_record_public_prestige",
        "sod_company_accounts_record_battle_victory",
        "sod_company_accounts_record_battle_defeat",
        "sod_company_accounts_record_battle_casualties",
        "sod_company_accounts_process_battle_promise_aftermath",
        "sod_company_accounts_get_casualty_compensation_cost_to_regs",
        "sod_company_accounts_apply_casualty_compensation",
        "sod_company_accounts_record_siege_hazard",
        "sod_company_accounts_get_hazard_pay_cost_to_regs",
        "sod_company_accounts_apply_hazard_pay",
        "sod_company_accounts_refuse_public_spectacle",
        "sod_company_accounts_get_victory_reward_cost_to_regs",
        "sod_company_accounts_apply_victory_reward",
        "sod_company_accounts_update_noble_restlessness",
        "sod_company_accounts_get_noble_restlessness_band_to_reg",
        "sod_company_accounts_describe_noble_restlessness_to_s28",
        "sod_company_accounts_try_petition",
        "sod_company_accounts_process_petition_check",
        "sod_company_accounts_apply_petition_response",
        "sod_company_accounts_describe_petition_to_s36",
        "sod_company_accounts_try_peaceful_desertion",
        "sod_company_accounts_process_desertion_check",
        "sod_company_accounts_resolve_desertion",
        "sod_company_accounts_spawn_deserter_party",
        "sod_company_accounts_deserter_party_take_supplies",
        "sod_company_accounts_describe_desertion_to_s40",
        "sod_company_accounts_get_withdrawal_supply_severity_to_reg",
        "sod_company_accounts_try_mutiny",
        "sod_company_accounts_process_mutiny_check",
        "sod_company_accounts_apply_mutiny_warning_response",
        "sod_company_accounts_resolve_mutiny",
        "sod_company_accounts_start_mutiny_battle",
        "sod_company_accounts_describe_mutiny_to_s44",
        "sod_company_accounts_describe_class_voices_to_s52",
        "sod_company_accounts_get_class_wages_to_regs",
        "sod_company_accounts_describe_class_wages_to_s56",
        "script_calculate_player_faction_wage",
        "script_sod_troop_get_doctrine",
        "$g_sod_company_accrued_wages",
        "$g_sod_company_pay_confidence",
        "$g_sod_company_camp_strain",
        "$g_sod_company_companion_morale",
        "$g_sod_company_mercenary_morale",
        "$g_sod_company_noble_morale",
        "$g_sod_company_faith_morale",
        "$g_sod_company_enlisted_morale",
        "$g_sod_company_companion_count",
        "$g_sod_company_mercenary_count",
        "$g_sod_company_enlisted_count",
        "$g_sod_company_ration_policy",
        "$g_sod_company_ration_confidence",
        "$g_sod_company_last_ration_feast_day",
        "$g_sod_company_wage_promise_day",
        "$g_sod_company_wage_promise_due_day",
        "$g_sod_company_wage_promise_amount",
        "$g_sod_company_wage_promise_broken",
        "$g_sod_company_battle_promise_day",
        "$g_sod_company_battle_promise_amount",
        "$g_sod_company_battle_promise_active",
        "$g_sod_company_battle_promise_broken",
        "$g_sod_company_last_recreation_day",
        "$g_sod_company_recreation_memory",
        "$g_sod_company_recreation_quality",
        "$g_sod_company_recreation_excess",
        "$g_sod_company_last_recreation_incident",
        "$g_sod_company_last_recreation_incident_day",
        "$g_sod_company_last_recreation_fine",
        "$g_sod_company_last_religious_observance_day",
        "$g_sod_company_last_prestige_day",
        "$g_sod_company_noble_restlessness",
        "$g_sod_company_noble_count",
        "$g_sod_company_faith_count",
        "$g_sod_company_petition_type",
        "$g_sod_company_petition_stage",
        "$g_sod_company_petition_severity",
        "$g_sod_company_petition_preferred_class",
        "$g_sod_company_last_petition_day",
        "$g_sod_company_desertion_stage",
        "$g_sod_company_desertion_risk",
        "$g_sod_company_desertion_troop",
        "$g_sod_company_desertion_count",
        "$g_sod_company_desertion_demand",
        "$g_sod_company_desertion_class",
        "$g_sod_company_last_desertion_day",
        "$g_sod_company_mutiny_stage",
        "$g_sod_company_mutiny_risk",
        "$g_sod_company_mutiny_bloc_troop",
        "$g_sod_company_mutiny_bloc_count",
        "$g_sod_company_mutiny_demand",
        "$g_sod_company_mutiny_bloc_class",
        "$g_sod_company_last_mutiny_resolution",
        "$g_sod_company_last_mutiny_day",
        "$g_sod_company_last_mutiny_answer_day",
        "$g_sod_company_last_victory_day",
        "$g_sod_company_last_victory_reward_day",
        "$g_sod_company_last_public_honor_day",
        "$g_sod_company_last_casualty_day",
        "$g_sod_company_recent_wounded_count",
        "$g_sod_company_casualty_compensation_pressure",
        "$g_sod_company_last_casualty_compensation_day",
        "$g_sod_company_last_siege_hazard_day",
        "$g_sod_company_siege_hazard_pressure",
        "$g_sod_company_siege_hazard_count",
        "$g_sod_company_last_hazard_pay_day",
        "$g_sod_company_last_victory_feast_day",
        "$g_sod_company_last_refused_spectacle_day",
        "reg60",
        "reg61",
        "reg62",
        "reg63",
        "sod_elite_tier_noble",
        "sod_elite_tier_faith",
        "sod_doctrine_flag_mercenary",
        "sod_companion_action_unpaid_wages",
        "sod_companion_action_food_security",
        "sod_companion_action_hunger",
        "sod_companion_action_generous_rations",
        "sod_companion_action_thin_rations",
        "sod_companion_action_officer_austerity",
        "sod_companion_action_ration_feast",
        "sod_companion_action_tavern_recreation",
        "sod_companion_action_religious_rites",
        "sod_companion_action_strict_discipline",
        "sod_companion_action_drunken_disorder",
        "sod_companion_action_debt_honesty",
        "sod_companion_action_road_practicality",
        "sod_companion_action_empty_speech",
        "sod_companion_action_build_healing",
    ):
        assert_contains(scripts, token)


def test_startup_and_wage_trigger_are_wired() -> None:
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    trigger = read("src/triggers/ST02_every_hour/entry_0133.py")
    assert_contains(game_start, "script_sod_company_accounts_initialize")
    assert_contains(trigger, "script_sod_company_accounts_accrue_wages")
    assert_contains(trigger, "script_sod_company_accounts_process_pay_promise")
    assert_contains(trigger, "script_sod_company_accounts_process_petition_check")
    assert_contains(trigger, "script_sod_company_accounts_process_desertion_check")
    assert_contains(trigger, "script_sod_company_accounts_process_mutiny_check")
    assert_not_contains(trigger, "jump_to_menu, \"mnu_pay_day\"")


def test_company_accounts_menu_is_reachable() -> None:
    order = read("src/menus/_order_game_menus.txt")
    camp_action = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    reports = read("src/menus/0000_hardcoded_mb1011/reports.py")
    menu = read("src/menus/camp/company_accounts.py")
    assert_contains(order, "camp/company_accounts.py")
    assert_contains(camp_action, "mnu_company_accounts")
    assert_contains(camp_action, "mnu_company_rations")
    assert_contains(camp_action, "mnu_company_recreation")
    assert_contains(reports, "mnu_company_accounts")
    for token in (
        "company_accounts_pay_full",
        "company_accounts_pay_half",
        "company_accounts_pay_bonus",
        "company_accounts_pay_veterans",
        "company_accounts_pay_wounded",
        "company_accounts_hazard_pay",
        "company_accounts_delay",
        "company_rations_thin",
        "company_rations_standard",
        "company_rations_generous",
        "company_rations_austerity",
        "company_rations_feast",
        "company_recreation_tavern_round",
        "company_recreation_lodging",
        "company_recreation_own_coin",
        "company_recreation_rites",
        "company_recreation_offering",
        "company_recreation_wounded",
        "company_recreation_campfire",
        "company_recreation_victory_feast",
        "company_recreation_village_festival",
        "company_recreation_strict",
        "company_recreation_rumors",
        "company_tavern_rumors",
        "company_petition",
        "company_petition_hear_out",
        "company_petition_reassure",
        "company_petition_companion_mediation",
        "company_petition_dismiss",
        "company_desertion_petition",
        "company_desertion_paid",
        "company_desertion_persuade",
        "company_desertion_unpaid",
        "company_desertion_forbid",
        "taking {reg59} denars, {reg60} food, {reg61} prisoners, {reg62} goods, and {reg63} horses",
        "company_mutiny_warning",
        "company_mutiny_negotiate",
        "company_mutiny_pay_half",
        "company_mutiny_drill",
        "company_mutiny_threaten",
        "company_mutiny_resolution",
        "company_mutiny_resolve_settlement",
        "company_mutiny_resolve_expel",
        "company_mutiny_resolve_battle",
        "company_mutiny_resolve_defer",
        "taking {reg59} denars, {reg60} food, {reg61} prisoners, {reg62} goods, and {reg63} horses",
        "mnu_trade_network_report",
        "script_sod_company_accounts_describe_to_s20",
        "script_sod_company_accounts_describe_rations_to_s23",
        "script_sod_company_accounts_describe_recreation_to_s26",
        "script_sod_company_accounts_describe_tavern_rumors_to_s30",
        "script_sod_company_accounts_describe_petition_to_s36",
        "script_sod_company_accounts_describe_desertion_to_s40",
        "script_sod_company_accounts_describe_mutiny_to_s44",
        "script_sod_company_accounts_apply_pay_choice",
        "script_sod_company_accounts_apply_casualty_compensation",
        "script_sod_company_accounts_apply_hazard_pay",
        "script_sod_company_accounts_apply_victory_reward",
        "script_sod_company_accounts_apply_victory_feast",
        "script_sod_company_accounts_refuse_public_spectacle",
        "script_sod_company_accounts_apply_petition_response",
        "script_sod_company_accounts_find_petition_mediator_to_regs",
        "script_sod_company_accounts_resolve_desertion",
        "script_sod_company_accounts_apply_mutiny_warning_response",
        "script_sod_company_accounts_resolve_mutiny",
        "script_sod_company_accounts_set_ration_policy",
        "script_sod_company_accounts_apply_ration_feast",
        "script_sod_company_accounts_apply_recreation",
        "sod_company_pay_choice_full",
        "sod_company_pay_choice_half",
        "sod_company_pay_choice_bonus",
        "sod_company_pay_choice_delay",
        "sod_company_pay_choice_veterans",
        "sod_company_pay_choice_wounded",
        "sod_company_ration_policy_thin",
        "sod_company_ration_policy_standard",
        "sod_company_ration_policy_generous",
        "sod_company_ration_policy_officer_austerity",
        "sod_company_recreation_tavern_round",
        "sod_company_recreation_lodging",
        "sod_company_recreation_own_coin",
        "sod_company_recreation_religious_rites",
        "sod_company_recreation_company_offering",
        "sod_company_recreation_wounded_care",
        "sod_company_recreation_campfire",
        "sod_company_recreation_village_festival",
        "sod_company_recreation_strict_discipline",
    ):
        assert_contains(menu, token)
    for token in (
        "Issue thin rations (70% food use, morale suffers).",
        "Issue standard rations (normal food use).",
        "Issue generous rations (130% food use, morale improves).",
        "Order officer austerity (85% food use, officers share hardship).",
        "Open the stores for a ration feast (spend 3 food, morale +5).",
    ):
        assert_contains(menu, token)
    for token in (
        "company_accounts_promise",
        "company_accounts_battle_promise",
        "company_accounts_threaten",
        "company_accounts_rations",
        "company_accounts_recreation",
    ):
        assert_not_contains(menu, token)
    assert_not_contains(menu, "(ge, \"$g_sod_company_petition_stage\", sod_company_petition_stage_murmur)")
    assert_contains(menu, "(ge, \"$g_sod_company_desertion_stage\", sod_company_desertion_stage_request)")
    assert_contains(menu, "(ge, \"$g_sod_company_mutiny_stage\", sod_company_mutiny_stage_warning)")


def test_company_wage_debt_uses_live_main_party_payroll() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    payday = read("src/menus/0000_hardcoded_mb1011/pay_day.py")
    for token in (
        '"sod_company_accounts_get_current_company_weekly_wage_to_reg"',
        'party_get_num_companion_stacks, ":num_stacks", "p_main_party"',
        'neg|troop_is_hero, ":stack_troop"',
        'script_game_get_troop_wage',
        'assign, reg1, ":paid_troops"',
        'script_sod_company_accounts_get_current_company_weekly_wage_to_reg',
        'assign, "$g_sod_company_accrued_wages", 0',
        'store_mul, ":max_live_debt", reg31, 3',
    ):
        assert_contains(scripts, token)
    assert_contains(menu, "script_sod_company_accounts_get_current_company_weekly_wage_to_reg")
    assert_not_contains(menu, "script_calculate_player_faction_wage")
    for token in (
        'script_sod_company_accounts_get_current_company_weekly_wage_to_reg',
        'assign, ":current_company_weekly_wage", reg0',
        'le, ":current_company_weekly_wage", 0',
        'assign, "$g_player_debt_to_party_members", 0',
        'store_mul, ":max_live_debt", ":current_company_weekly_wage", 3',
    ):
        assert_contains(payday, token)


def test_ration_policy_hooks_are_wired() -> None:
    food_trigger = read("src/triggers/ST03_daily/entry_0054.py")
    morale = read("src/scripts/ZC_parties/get_player_party_morale_values.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    assert_contains(food_trigger, "script_sod_company_accounts_adjust_food_consumption_to_reg")
    assert_contains(food_trigger, "script_sod_company_accounts_update_ration_pressure")
    assert_contains(morale, "$g_player_party_morale_modifier_rations")
    assert_contains(morale, "$g_sod_company_ration_policy")
    assert_contains(morale, "sod_company_ration_policy_thin")
    assert_contains(morale, "sod_company_ration_policy_generous")
    assert_contains(scripts, "troop_remove_item")
    assert_contains(scripts, "food_begin")
    assert_contains(scripts, "food_end")
    assert_contains(companion_depth, "sod_companion_action_generous_rations")
    assert_contains(companion_depth, "sod_companion_action_thin_rations")
    assert_contains(companion_depth, "sod_companion_action_officer_austerity")
    assert_contains(companion_depth, "sod_companion_action_ration_feast")
    assert_contains(companion_depth, "sod_companion_action_petition_mediated")


def test_morale_compatibility_is_preserved() -> None:
    morale = read("src/scripts/ZC_parties/get_player_party_morale_values.py")
    payday = read("src/menus/0000_hardcoded_mb1011/pay_day.py")
    assert_contains(morale, "$g_player_debt_to_party_members")
    assert_contains(morale, "$g_player_party_morale_modifier_company_accounts")
    assert_contains(morale, "$g_sod_company_camp_strain")
    assert_contains(payday, "sod_companion_action_unpaid_wages")


def test_arena_prestige_relief_is_wired() -> None:
    tournament_won = read("src/menus/other/continue_35.py")
    total_victory = read("src/scripts/ZC_parties/total_victory_finalize.py")
    total_defeat = read("src/menus/other/total_defeat.py")
    company_accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    assert_contains(tournament_won, "script_sod_company_accounts_apply_arena_prestige")
    assert_contains(total_victory, "script_sod_company_accounts_record_battle_victory")
    assert_contains(total_victory, "script_sod_company_accounts_record_battle_casualties")
    assert_contains(total_victory, "script_sod_company_accounts_record_siege_hazard")
    assert_contains(total_defeat, "script_sod_company_accounts_record_battle_defeat")
    assert_contains(total_victory, "walled_centers_begin")
    assert_contains(company_accounts, "sod_company_prestige_battle")
    assert_contains(companion_depth, "sod_companion_action_tavern_recreation")
    assert_contains(companion_depth, "sod_companion_action_religious_rites")
    assert_contains(companion_depth, "sod_companion_action_strict_discipline")


def test_noble_restlessness_report_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    assert_contains(scripts, "script_sod_company_accounts_describe_noble_restlessness_to_s28")
    assert_contains(scripts, "Noble and faith pressure")
    assert_contains(scripts, "ordinary tavern relief")
    assert_contains(scripts, "arena glory")


def test_company_account_report_fields_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    reports = read("src/menus/0000_hardcoded_mb1011/reports.py")
    for token in (
        "Company Accounts",
        "Morale",
        "Weekly Cost of Party",
        "Total Amount owed",
        "Next Payday",
        "Last Time Paid",
        "Current Ration Policy",
        "Current issue",
        "Pay confidence",
        "Camp strain",
        "script_sod_company_accounts_describe_class_wages_to_s56",
        "Wage weight by class",
        "enlisted {reg56}, mercenary {reg57}, noble {reg58}, faith {reg59}",
        "{s56}",
        "{s50}",
    ):
        assert_contains(scripts, token)
    assert_contains(menu, "script_sod_company_accounts_describe_to_s20")
    assert_contains(reports, "mnu_company_accounts")


def test_mercenary_pay_expectations_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "script_sod_company_accounts_get_class_wages_to_regs",
        "(gt, reg57, 0)",
        "(eq, \":policy\", sod_company_ration_policy_generous)",
        "(eq, \":choice\", sod_company_pay_choice_bonus)",
        "(val_sub, \"$g_sod_company_desertion_risk\", 8)",
        "(val_sub, \"$g_sod_company_mutiny_risk\", 6)",
        "Contract steel is carrying the payroll",
    ):
        assert_contains(scripts, token)
    assert_contains(docs, "- [x] Mercenaries expect timely coin more than generous rations.")
    assert_contains(docs, "- [x] Mercenary grievance falls faster from bonus pay.")


def test_enlisted_pay_patience_rules_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "(gt, reg56, 0)",
        "(gt, reg56, reg57)",
        "(assign, \":preferred_class\", sod_company_troop_class_enlisted)",
        "(store_sub, \":days_since_victory\", \":cur_day\", \"$g_sod_company_last_victory_day\")",
        "(le, \":days_since_victory\", 3)",
        "(ge, \"$g_sod_company_pay_confidence\", 65)",
        "(val_sub, \":pay_score\", 12)",
        "(val_add, \":risk\", 8)",
        "(val_sub, \":risk\", 10)",
    ):
        assert_contains(scripts, token)
    assert_contains(docs, "- [x] Enlisted troops are most sensitive to repeated unpaid wages.")
    assert_contains(docs, "- [x] Enlisted troops forgive delay after victories if pay confidence is high.")


def test_noble_faith_withdrawal_rules_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "sod_company_accounts_get_withdrawal_supply_severity_to_reg",
        "(eq, \":troop_class\", sod_company_troop_class_noble)",
        "(eq, \":troop_class\", sod_company_troop_class_faith)",
        "(val_sub, reg62, 2)",
        "script_sod_company_accounts_get_withdrawal_supply_severity_to_reg\", reg39, 1",
        "script_sod_company_accounts_get_withdrawal_supply_severity_to_reg\", \"$g_sod_company_mutiny_bloc_class\", 2",
        "$g_sod_company_last_religious_observance_day",
        "(val_sub, \":risk\", 10)",
    ):
        assert_contains(scripts, token)
    assert_contains(docs, "- [x] Noble/faith troops are less likely to steal supplies during desertion.")
    assert_contains(docs, "- [x] Faith troops can support the player during mutiny if the player's conduct aligns with their doctrine.")


def test_faith_conduct_reactivity_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    slavers = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    diplomacy = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "sod_company_accounts_apply_faith_conduct",
        "sod_companion_action_free_captives",
        "sod_companion_action_buy_slaves",
        "sod_companion_action_carry_slaves",
        "sod_companion_action_religious_rites",
        "sod_companion_action_generous_rations",
        "(val_add, \"$g_sod_company_noble_restlessness\", \":outrage\")",
        "(val_sub, \"$g_sod_company_noble_restlessness\", \":relief\")",
        "(store_current_day, \"$g_sod_company_last_religious_observance_day\")",
    ):
        assert_contains(scripts, token)
    for token in (
        "script_sod_company_accounts_apply_faith_conduct",
        "sod_companion_action_free_captives",
        "sod_companion_action_buy_slaves",
        "sod_companion_action_carry_slaves",
    ):
        assert_contains(slavers, token)
    assert_contains(diplomacy, "script_sod_company_accounts_apply_faith_conduct")
    assert_contains(docs, "- [x] Faith troops react to ration generosity, mercy, sacrilege, slavery, and holy obligations.")
    assert_contains(scripts, "script_sod_company_accounts_describe_class_voices_to_s52")
    assert_contains(scripts, "Company voices")
    assert_contains(scripts, "hazard silver")
    assert_contains(scripts, "faith-minded troops")


def test_company_accounts_checklist_tracks_v2_gaps() -> None:
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    assert_not_contains(docs, "- [ ]")
    for token in (
        "v1 includes final warning, negotiation pressure, and an optional battle route.",
        "Decision: no automatic post-loot interruption in v1",
        "Decision: yes, local-fine incidents also reduce nearby center relation",
        "Decision: deserters/expelled ringleaders become real `pt_deserters` map parties in v1",
    ):
        assert_contains(docs, token)


def test_local_recreation_flavor_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    for token in (
        "sod_company_accounts_describe_local_recreation_to_s54",
        "Local relief",
        "prosperous {s56}",
        "garrison {s56}",
        "living {s56}",
        "strained {s56}",
        "script_get_closest_center",
        "slot_town_prosperity",
        "slot_village_state",
        "{s54}",
    ):
        assert_contains(scripts, token)


def test_company_rations_report_shows_supply_time_and_policy_effects() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    for token in (
        "sod_company_accounts_get_daily_food_consumption_to_regs",
        "script_sod_company_accounts_adjust_food_consumption_to_reg",
        "script_count_edible_food",
        "(store_div, \":base_consumption\", \":num_men\", 5)",
        "(store_mul, \":total_hours\", \":edible_food\", 24)",
        "(store_div, \":weeks_left\", \":total_hours\", 168)",
        "(store_mod, \":hours_remainder\", \":total_hours\", 168)",
        "Food left: {reg33} week(s), {reg34} day(s), {reg35} hour(s).",
        "Estimated Daily Consumption: {reg32} provisions/day under {s24} rations.",
        "Stores: {reg31} provisions. Base need before policy: {reg36} provisions/day.",
        "Thin: 70% food use; morale suffers.",
        "Standard: normal food use; stable morale.",
        "Generous: 130% food use; morale improves while stores last.",
        "Officer austerity: 85% food use; officers and companions share hardship openly.",
        "Ration feast: spends 3 provisions now; morale +5 and camp strain -10",
    ):
        assert_contains(scripts, token)


def test_recreation_disorder_incidents_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "sod_company_accounts_try_recreation_incident",
        "sod_company_recreation_own_coin",
        "sod_company_recreation_village_festival",
        "sod_company_recreation_incident_drunken_brawl",
        "sod_company_recreation_incident_gambling_debt",
        "sod_company_recreation_incident_missing_soldier",
        "sod_company_recreation_incident_insulted_noble",
        "sod_company_recreation_incident_mercenary_overindulgence",
        "sod_company_recreation_incident_local_fine",
        "$g_sod_company_last_recreation_incident",
        "Last disorder",
        "store_random_in_range",
        "slot_center_player_relation",
        "$g_sod_company_last_recreation_fine",
    ):
        assert_contains(scripts, token)
    assert_contains(menu, "company_recreation_own_coin")
    assert_contains(menu, "company_recreation_village_festival")
    assert_contains(menu, "tavern disorder follows")
    assert_contains(companion_depth, "sod_companion_action_drunken_disorder")


def test_tavern_rumor_intelligence_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    for token in (
        "sod_company_accounts_describe_tavern_rumors_to_s30",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_black_khergit_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
        "$g_sod_trade_network_last_result_party",
        "Tavern Intelligence",
        "caravan masters",
    ):
        assert_contains(scripts, token)
    assert_contains(menu, "company_recreation_rumors")
    assert_contains(menu, "company_tavern_rumors")
    assert_contains(menu, "mnu_trade_network_report")


def test_company_petition_pressure_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    for token in (
        "Petition risk",
        "Pay arrears",
        "Ration grievance",
        "Noble restlessness",
        "Wounded care",
        "General camp strain",
        "Likely voice",
        "Company voices",
        "can speak as",
        "Company petition: no trusted companion is positioned",
        "contractual",
        "oath-bound",
        "honor, public victory, shame",
        "formal petition likely",
        "urgent petition",
    ):
        assert_contains(scripts, token)
    assert_not_contains(menu, "company_accounts_petition")
    assert_not_contains(menu, "Hear the current company petition.")
    for token in (
        "company_petition",
        "script_sod_company_accounts_describe_petition_to_s36",
        "script_sod_company_accounts_apply_petition_response",
    ):
        assert_contains(menu, token)


def test_peaceful_desertion_request_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "Desertion risk",
        "watching the road",
        "request likely",
        "urgent request",
        "{s49} group",
        "contract exit",
        "formal withdrawal",
        "oath crisis",
        "party_remove_members",
        "spawn_around_party",
        "pt_deserters",
        "party_add_members",
        "script_sod_company_accounts_spawn_deserter_party",
        "script_sod_company_accounts_deserter_party_take_supplies",
        "add_gold_to_party",
        "player_has_item",
        "party_get_num_prisoner_stacks",
        "party_prisoner_stack_get_troop_id",
        "party_prisoner_stack_get_size",
        "party_remove_prisoners",
        "party_add_prisoners",
        "trade_goods_begin",
        "trade_goods_end",
        "horses_begin",
        "horses_end",
        "sod_company_desertion_response_paid",
        "sod_company_desertion_response_persuade",
        "sod_company_desertion_response_unpaid",
        "sod_company_desertion_response_forbid",
        "sod_company_desertion_response_battle_promise",
        "sod_company_accounts_set_battle_pay_promise",
        "battle-pay promise",
    ):
        assert_contains(scripts, token)
    for token in (
        "company_desertion_petition",
        "company_desertion_paid",
        "company_desertion_persuade",
        "company_desertion_battle_promise",
        "Promise pay after the next battle",
        "company_desertion_unpaid",
        "company_desertion_forbid",
    ):
        assert_contains(menu, token)
    assert_contains(companion_depth, "sod_companion_action_peaceful_desertion_allowed")
    assert_contains(companion_depth, "sod_companion_action_peaceful_desertion_forbidden")


def test_mutiny_warning_foundation_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "Mutiny warning",
        "warning signs",
        "final warning",
        "near breaking",
        "hard {s49} bloc",
        "contract turned into a weapon",
        "officer's rebuke",
        "oath-crisis ultimatum",
        "sod_company_mutiny_response_negotiate",
        "sod_company_mutiny_response_pay",
        "sod_company_mutiny_response_threaten",
        "sod_company_mutiny_response_drill",
        "sod_company_mutiny_resolution_settlement",
        "sod_company_mutiny_resolution_ringleaders_expelled",
        "sod_company_mutiny_resolution_deferred",
        "sod_company_mutiny_resolution_battle",
        "sod_company_accounts_start_mutiny_battle",
        "Company Mutineers",
        "$g_encountered_party_template",
        "$new_encounter",
        "$cant_leave_encounter",
        "$g_sod_company_last_mutiny_answer_day",
        "(lt, \":bloc_size\", 6)",
        ":days_since_answer",
        "ringleaders",
        "script_sod_company_accounts_spawn_deserter_party",
        "script_sod_company_accounts_deserter_party_take_supplies",
    ):
        assert_contains(scripts, token)
    for token in (
        "company_mutiny_warning",
        "company_mutiny_negotiate",
        "company_mutiny_pay_half",
        "company_mutiny_drill",
        "company_mutiny_threaten",
        "company_mutiny_resolution",
        "company_mutiny_resolve_settlement",
        "company_mutiny_resolve_expel",
        "company_mutiny_resolve_battle",
        "mnu_simple_encounter",
        "company_mutiny_resolve_defer",
    ):
        assert_contains(menu, token)
    assert_contains(companion_depth, "sod_companion_action_threatened_troops")
    assert_contains(companion_depth, "sod_companion_action_mutiny_negotiated")
    assert_contains(companion_depth, "sod_companion_action_mutiny_suppressed")


def test_targeted_pay_choices_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "sod_company_pay_choice_veterans",
        "sod_company_pay_choice_wounded",
        "sod_companion_action_veteran_pay",
        "sod_companion_action_wounded_pay",
        "party_stack_get_num_wounded",
        "$g_sod_company_casualty_compensation_pressure",
        "Claims",
        "sod_company_accounts_apply_casualty_compensation",
        "$g_sod_company_siege_hazard_pressure",
        "siege hazard",
        "sod_company_accounts_apply_hazard_pay",
        "$g_sod_company_last_victory_feast_day",
        "Victory claims",
        "sod_company_accounts_apply_victory_feast",
        "$g_sod_company_last_refused_spectacle_day",
        "sod_company_accounts_refuse_public_spectacle",
        "$g_sod_company_noble_restlessness",
    ):
        assert_contains(scripts, token)
    assert_contains(menu, "company_accounts_pay_veterans")
    assert_contains(menu, "company_accounts_pay_wounded")
    assert_contains(menu, "company_accounts_hazard_pay")
    assert_contains(menu, "company_recreation_victory_feast")
    assert_contains(companion_depth, "sod_companion_action_fair_pay")
    assert_contains(companion_depth, "sod_companion_action_bonus_pay")
    assert_contains(companion_depth, "sod_companion_action_half_pay")
    assert_contains(companion_depth, "sod_companion_action_delayed_pay")
    assert_contains(companion_depth, "sod_companion_action_veteran_pay")
    assert_contains(companion_depth, "sod_companion_action_wounded_pay")
    assert_contains(companion_depth, "sod_companion_action_debt_honesty")
    assert_contains(companion_depth, "sod_companion_action_road_practicality")
    assert_contains(companion_depth, "sod_companion_action_empty_speech")


def test_company_growth_debt_hook_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    recruit = read("src/scripts/ZD_centers/village_recruit_volunteers_recruit.py")
    upgrade = read("src/menus/other/sod_upgrade_continue.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "sod_company_accounts_record_company_growth",
        "sod_company_growth_recruit",
        "sod_company_growth_upgrade",
        "$g_player_debt_to_party_members",
        "$g_sod_company_accrued_wages",
        "sod_companion_action_unpaid_wages",
    ):
        assert_contains(scripts, token)
    assert_contains(recruit, "script_sod_company_accounts_record_company_growth")
    assert_contains(recruit, "sod_company_growth_recruit")
    assert_contains(upgrade, "script_sod_company_accounts_record_company_growth")
    assert_contains(upgrade, "sod_company_growth_upgrade")
    assert_contains(docs, "- [x] Add helper call from troop upgrade/hiring if debt should affect confidence.")


def test_company_accounts_feed_battle_morale() -> None:
    company = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    battle_context = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    coherence = read("src/scripts/ZZ_common_array_processing/coherence.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "sod_company_accounts_get_battle_morale_context_to_regs",
        "$g_sod_company_pay_confidence",
        "$g_sod_company_camp_strain",
        "$g_sod_company_ration_confidence",
        "$g_sod_company_companion_morale",
        "$g_sod_company_mercenary_morale",
        "$g_sod_company_noble_morale",
        "$g_sod_company_faith_morale",
        "$g_sod_company_enlisted_morale",
        "script_sod_company_accounts_update_troop_category_morale",
        "weakest_category",
        "category_average",
        "$g_player_debt_to_party_members",
        "$g_sod_company_mutiny_risk",
        "reg60",
        "reg61",
        "reg62",
        "reg63",
    ):
        assert_contains(company, token)
    assert_contains(battle_context, "script_sod_company_accounts_get_battle_morale_context_to_regs")
    assert_contains(battle_context, "$g_sod_battle_ally_lord_morale\", reg60")
    assert_contains(battle_context, "$g_sod_battle_ally_pay_strain\", reg61")
    assert_contains(battle_context, "$g_sod_battle_ally_fatigue\", reg62")
    assert_contains(battle_context, "$g_sod_battle_ally_supply_confidence\", reg63")
    assert_contains(coherence, "Ally/company battle morale context")
    assert_contains(docs, "- [x] Company-account morale feeds in-battle morale and routing context.")
    assert_contains(docs, "In-battle morale now uses troop-category morale")


def test_troop_category_morale_split() -> None:
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "sod_company_accounts_update_troop_category_morale",
        "sod_company_accounts_describe_category_morale_to_s58",
        "$g_sod_company_companion_morale",
        "$g_sod_company_mercenary_morale",
        "$g_sod_company_noble_morale",
        "$g_sod_company_faith_morale",
        "$g_sod_company_enlisted_morale",
        "$g_sod_company_companion_count",
        "$g_sod_company_mercenary_count",
        "$g_sod_company_noble_count",
        "$g_sod_company_faith_count",
        "$g_sod_company_enlisted_count",
        "sod_company_troop_class_mercenary",
        "sod_company_troop_class_noble",
        "sod_company_troop_class_faith",
        "Troop-category morale",
        "Watch point:",
        "mercenary confidence is the softest",
        "enlisted morale is the weak point",
        "weakest_category",
        "category_average",
    ):
        assert_contains(accounts, token)
    assert_contains(docs, "distinct morale scores surfaced in the company report")


def test_pay_promise_and_threat_routes_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    trigger = read("src/triggers/ST02_every_hour/entry_0133.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    for token in (
        "sod_company_accounts_set_pay_promise",
        "sod_company_accounts_process_pay_promise",
        "sod_company_accounts_set_battle_pay_promise",
        "sod_company_accounts_apply_threat",
        "sod_company_accounts_describe_promise_to_s50",
        "$g_sod_company_wage_promise_due_day",
        "$g_sod_company_wage_promise_broken",
        "$g_sod_company_battle_promise_active",
        "$g_sod_company_battle_promise_broken",
        "Broken promises",
        "after the next battle",
        "defeat has not erased your battle-pay promise",
        "{s50}",
    ):
        assert_contains(scripts, token)
    assert_not_contains(menu, "company_accounts_promise")
    assert_not_contains(menu, "company_accounts_battle_promise")
    assert_not_contains(menu, "Victory will make it due quickly; defeat will not erase it.")
    assert_not_contains(menu, "company_accounts_threaten")
    assert_contains(menu, "company_desertion_battle_promise")
    assert_contains(menu, "company_mutiny_threaten")
    assert_contains(trigger, "script_sod_company_accounts_process_pay_promise")
    assert_contains(companion_depth, "sod_companion_action_broken_pay_promise")


def test_company_accounts_menu_uses_clear_ledger_summary() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menu = read("src/menus/camp/company_accounts.py")
    for token in (
        "Morale: {reg35}.",
        "Weekly Cost of Party: {s23}.",
        "Total Amount owed: {reg22} denars.",
        "Next Payday: {s63}.",
        "Last Time Paid: {s26}.",
        "Current Ration Policy: {s64}.",
        "Current issue: {s67}",
        "Pay confidence: {s21}. Camp strain: {s22}.",
        "(party_get_morale, reg35, \"p_main_party\")",
        "(store_add, reg34, reg31, reg54)",
        "script_sod_companion_retinue_get_account_totals_to_regs",
        "({reg31} party, {reg54} retinue)",
        "{s65}",
        "reg30",
        "reg31",
        "reg32",
        "reg33",
        "(store_sub, reg30, 7, reg24)",
        "(store_sub, reg33, reg22, reg23)",
        "due now",
        "in {reg30} day(s)",
        "{reg24} day(s) ago",
        "today",
        "sod_company_ration_policy_thin",
        "sod_company_ration_policy_standard",
        "sod_company_ration_policy_generous",
        "sod_company_ration_policy_officer_austerity",
        "Retinue:",
        "Claims:",
        "Victory claims:",
    ):
        assert_contains(scripts, token)
    ledger_tokens = (
        "Morale: {reg35}.",
        "Weekly Cost of Party: {s23}.",
        "Total Amount owed: {reg22} denars.",
        "Next Payday: {s63}.",
        "Last Time Paid: {s26}.",
        "Current Ration Policy: {s64}.",
        "Current issue: {s67}",
    )
    last_pos = -1
    for token in ledger_tokens:
        pos = scripts.index(token)
        assert pos > last_pos, f"ledger token out of order: {token}"
        last_pos = pos
    assert_not_contains(scripts, "Pay confidence: {s21} ({reg25})")
    assert_not_contains(scripts, "Camp strain: {s22} ({reg26})")
    assert_not_contains(scripts, "The choices below show what you will pay now")
    assert_contains(menu, '"Pay {reg25} denars; clear the account."')
    assert_contains(menu, '"Pay {reg25} denars; leave {reg26} owed, but ease strain."')
    assert_contains(menu, '"Pay {reg25} denars; clear debt and raise confidence."')
    assert_contains(menu, "(ge, reg23, reg25)")
    assert_contains(menu, '"The company books are clear."')
    assert_not_contains(menu, "No company wages are currently due.")
    assert_contains(scripts, "(this_or_next|ge, reg24, 7)")
    assert_contains(menu, '"Pay {reg25} denars to wounded first; {reg26} remains."')
    assert_contains(menu, '"Pay 0 now; delay raises strain and weakens trust."')
    assert_not_contains(menu, "company_accounts_promise")
    assert_not_contains(menu, "company_accounts_battle_promise")
    assert_not_contains(menu, "company_accounts_threaten")


def test_post_battle_morale_consequences_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    victory = read("src/scripts/ZC_parties/total_victory_finalize.py")
    defeat = read("src/menus/other/total_defeat.py")
    docs = read("docs/company/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md")
    for token in (
        "sod_company_accounts_record_battle_victory",
        "sod_company_accounts_record_battle_defeat",
        "sod_company_accounts_process_battle_promise_aftermath",
        "script_sod_company_accounts_record_battle_casualties",
        "victory buys patience for unpaid wages",
        "defeat makes unpaid wages sound louder than orders",
        "$g_sod_company_petition_severity",
        "$g_sod_company_desertion_risk",
        "$g_sod_company_mutiny_risk",
    ):
        assert_contains(scripts, token)
    assert_contains(victory, "script_sod_company_accounts_record_battle_victory")
    assert_contains(defeat, "script_sod_company_accounts_record_battle_defeat")
    assert_contains(docs, "post-battle morale consequences for victories, defeats, unpaid wages, and active battle promises")


if __name__ == "__main__":
    test_company_account_constants_exist()
    test_company_account_scripts_exist()
    test_startup_and_wage_trigger_are_wired()
    test_company_accounts_menu_is_reachable()
    test_ration_policy_hooks_are_wired()
    test_morale_compatibility_is_preserved()
    test_arena_prestige_relief_is_wired()
    test_noble_restlessness_report_is_wired()
    test_company_account_report_fields_are_wired()
    test_mercenary_pay_expectations_are_wired()
    test_enlisted_pay_patience_rules_are_wired()
    test_noble_faith_withdrawal_rules_are_wired()
    test_faith_conduct_reactivity_is_wired()
    test_company_accounts_checklist_tracks_v2_gaps()
    test_local_recreation_flavor_is_wired()
    test_company_rations_report_shows_supply_time_and_policy_effects()
    test_recreation_disorder_incidents_are_wired()
    test_tavern_rumor_intelligence_is_wired()
    test_company_petition_pressure_is_wired()
    test_peaceful_desertion_request_is_wired()
    test_mutiny_warning_foundation_is_wired()
    test_targeted_pay_choices_are_wired()
    test_company_growth_debt_hook_is_wired()
    test_company_accounts_feed_battle_morale()
    test_troop_category_morale_split()
    test_pay_promise_and_threat_routes_are_wired()
    test_company_accounts_menu_uses_clear_ledger_summary()
    test_post_battle_morale_consequences_are_wired()
    print("test_company_accounts_static: OK")

