from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_retinue_constants_slots_and_template_exist() -> None:
    constants = read("src/constants/module_constants.py")
    templates = read("compile/module_party_templates.py")

    for token in [
        "spt_companion_retinue",
        "slot_troop_sod_retinue_party",
        "slot_troop_sod_retinue_capacity",
        "slot_troop_sod_retinue_state",
        "slot_troop_sod_retinue_treasury",
        "slot_troop_sod_retinue_wage_reserve",
        "slot_troop_sod_retinue_strength_order",
        "slot_troop_sod_retinue_recruit_policy",
        "slot_troop_sod_retinue_post_battle_policy",
        "slot_troop_sod_retinue_last_battle_hire_result",
        "slot_troop_sod_retinue_last_battle_hire_amount",
        "slot_troop_sod_retinue_last_battle_hire_troop",
        "slot_troop_sod_retinue_battle_store_party",
        "slot_troop_sod_retinue_last_shortage",
        "slot_troop_sod_retinue_supply_pressure",
        "slot_troop_sod_retinue_last_training_xp",
        "slot_troop_sod_retinue_last_training_hour",
        "slot_troop_sod_retinue_last_desertion_day",
        "slot_party_sod_retinue_owner_troop",
        "slot_party_sod_retinue_anchor_party",
        "sod_retinue_wage_shortage_player_auto_cover",
        "sod_retinue_wage_shortage_purse_only",
        "sod_retinue_state_active",
        "sod_retinue_warning_none",
        "sod_retinue_warning_no_troops_returning",
        "sod_retinue_warning_over_capacity",
        "sod_retinue_warning_above_target",
        "sod_retinue_warning_full_refused",
        "sod_retinue_strength_none",
        "sod_retinue_strength_half",
        "sod_retinue_strength_full",
        "sod_retinue_recruit_policy_none",
        "sod_retinue_recruit_policy_balanced",
        "sod_retinue_post_battle_enabled",
        "sod_retinue_post_battle_disabled",
        "sod_retinue_battle_hire_hired",
        "sod_retinue_battle_hire_opted_out",
        "sod_retinue_battle_hire_no_trust",
        "sod_retinue_battle_hire_no_capacity",
        "sod_retinue_battle_hire_no_gold",
        "sod_retinue_battle_hire_no_leftovers",
        "sod_retinue_pref_scout_irregular",
        "sod_retinue_pref_trade_guard",
        "sod_retinue_pref_mercy_guard",
        "sod_retinue_pref_field_captain",
        "sod_retinue_pref_engineer_support",
        "sod_retinue_pref_skirmisher",
        "sod_retinue_max_command_purse",
        "sod_retinue_half_strength_tolerance",
    ]:
        assert_contains(constants, token)

    assert_contains(templates, '"sod_companion_retinue"')
    assert_contains(templates, "pf_no_label")
    assert_contains(templates, "pf_quest_party")


def test_capacity_uses_companion_stats_not_player_stats() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    capacity_start = retinues.index('"sod_companion_retinue_get_capacity"')
    capacity_end = retinues.index('"sod_companion_retinue_ensure_party"')
    capacity = retinues[capacity_start:capacity_end]

    assert_contains(capacity, '(store_skill_level, ":leadership", "skl_leadership", ":companion")')
    assert_contains(capacity, '(store_attribute_level, ":charisma", ":companion", ca_charisma)')
    assert_contains(capacity, '(store_character_level, ":level", ":companion")')
    assert_contains(capacity, "slot_troop_companion_approval")
    assert_contains(capacity, "slot_troop_companion_warning_state")
    assert_not_contains(capacity, '"trp_player"')
    assert_not_contains(capacity, "slot_troop_renown")


def test_capacity_formula_matches_first_pass_design() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    capacity_start = retinues.index('"sod_companion_retinue_get_capacity"')
    capacity_end = retinues.index('"sod_companion_retinue_ensure_party"')
    capacity = retinues[capacity_start:capacity_end]

    for token in [
        '(assign, ":capacity", 4)',
        '(store_mul, ":leadership_bonus", ":leadership", 5)',
        '(store_div, ":charisma_bonus", ":charisma", 2)',
        '(store_div, ":level_bonus", ":level", 3)',
        '(val_add, ":capacity", 8)',
        '(val_add, ":capacity", 5)',
        '(val_add, ":capacity", 2)',
        '(val_sub, ":capacity", 15)',
        '(val_sub, ":capacity", 8)',
        '(val_sub, ":capacity", 5)',
        "sod_companion_quest_resolved_good",
        "sod_companion_quest_resolved_hard",
        "sod_companion_quest_failed",
        '(val_max, ":capacity", 0)',
    ]:
        assert_contains(capacity, token)


def test_effective_party_helpers_keep_retinue_capacity_separate() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    companion_limit = read("src/scripts/ZA_hardcoded_game_scripts/game_get_party_companion_limit.py")

    for script in [
        '"sod_get_player_effective_party_size"',
        '"sod_get_player_effective_party_capacity"',
        '"sod_player_party_size_describe_to_s1"',
    ]:
        assert_contains(retinues, script)

    size_start = retinues.index('"sod_get_player_effective_party_size"')
    size_end = retinues.index('"sod_get_player_effective_party_capacity"')
    size = retinues[size_start:size_end]
    assert_contains(size, 'party_get_num_companions, ":personal_size", "p_main_party"')
    assert_contains(size, 'script_sod_companion_retinue_get_size')
    assert_contains(size, 'assign, reg0, ":personal_size"')
    assert_contains(size, 'assign, reg1, ":retinue_size"')
    assert_contains(size, 'assign, reg2, ":combined_size"')

    capacity_start = retinues.index('"sod_get_player_effective_party_capacity"')
    capacity_end = retinues.index('"sod_player_party_size_describe_to_s1"')
    capacity = retinues[capacity_start:capacity_end]
    assert_contains(capacity, 'party_get_num_companions, ":personal_size", "p_main_party"')
    assert_contains(capacity, 'party_get_free_companions_capacity, ":personal_free", "p_main_party"')
    assert_contains(capacity, 'script_sod_companion_retinue_get_capacity')
    assert_contains(capacity, 'script_sod_companion_retinue_get_free_capacity')
    assert_contains(capacity, 'assign, reg0, ":personal_capacity"')
    assert_contains(capacity, 'assign, reg1, ":retinue_capacity"')
    assert_contains(capacity, 'assign, reg2, ":combined_capacity"')
    assert_contains(capacity, 'assign, reg3, ":personal_free"')
    assert_contains(capacity, 'assign, reg4, ":retinue_free"')

    describe_start = retinues.index('"sod_player_party_size_describe_to_s1"')
    describe_end = retinues.index('"sod_companion_retinue_describe_report_to_s1"')
    describe = retinues[describe_start:describe_end]
    assert_contains(describe, "Personal command:")
    assert_contains(describe, "Companion retinues:")
    assert_contains(describe, "does not increase your personal party limit")
    assert_contains(describe, "new hires still enter your personal party only when there is native capacity")

    assert_not_contains(companion_limit, "script_sod_get_player_effective_party_capacity")
    assert_not_contains(companion_limit, "script_sod_companion_retinue")


def test_party_size_audit_covers_recruitment_and_reward_flows() -> None:
    audit = read("docs/reports/companion_retinue_party_size_audit.md")

    for token in [
        "party_get_num_companions",
        "party_get_free_companions_capacity",
        "Village recruitment",
        "Tavern mercenary hiring",
        "Prisoner and rescued-troop flows",
        "Quest reward troop flows",
        "script_sod_get_player_effective_party_size",
        "script_sod_get_player_effective_party_capacity",
        "must not call retinue helpers or add companion retinue capacity",
        "Battle participation uses hidden allied retinue parties",
    ]:
        assert_contains(audit, token)


def test_retinue_storage_transfer_and_treasury_helpers_exist() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    for token in [
        '"sod_companion_retinue_ensure_party"',
        "pt_sod_companion_retinue",
        "party_attach_to_party",
        "slot_party_type, spt_companion_retinue",
        "slot_party_sod_retinue_owner_troop",
        '"sod_companion_retinue_can_accept_troop"',
        '"sod_companion_retinue_add_troops"',
        '"sod_companion_retinue_remove_troops"',
        '"sod_companion_retinue_add_troops_up_to_capacity"',
        '"sod_companion_retinue_remove_troops_up_to_capacity"',
        '"sod_companion_retinue_select_main_party_troop"',
        '"sod_companion_retinue_select_retinue_troop"',
        '"sod_companion_retinue_describe_transfer_to_s1"',
        "party_remove_members, \"p_main_party\"",
        "party_add_members, \"p_main_party\"",
        "party_get_free_companions_capacity, \":free_capacity\", \"p_main_party\"",
        "is_between, \":troop\", soldiers_begin, soldiers_end",
        "is_between, \":stack_troop\", soldiers_begin, soldiers_end",
        "neg|troop_is_hero",
        '"sod_companion_retinue_add_gold"',
        '"sod_companion_retinue_remove_gold"',
        "troop_remove_gold, \"trp_player\"",
        "script_troop_add_gold",
        "slot_troop_sod_retinue_treasury",
        "slot_troop_sod_retinue_wage_reserve",
        '"sod_companion_retinue_set_recruit_policy"',
        '"sod_companion_retinue_set_post_battle_policy"',
        '"sod_companion_retinue_note_post_battle_hire_result"',
        '"sod_companion_retinue_describe_post_battle_hire_to_s22"',
        '"sod_companion_retinue_get_surplus_gold"',
        '"sod_companion_retinue_calculate_recruit_budget"',
        '"sod_companion_retinue_calculate_upgrade_budget"',
        '"sod_companion_retinue_select_recruit_troop"',
        '"sod_companion_retinue_get_recruit_cost"',
        '"sod_companion_retinue_select_upgrade_troop"',
        '"sod_companion_retinue_get_upgrade_cost"',
        '"sod_companion_retinue_set_strength_order"',
        '"cf_sod_companion_retinue_accepts_strength_order"',
        '"sod_companion_retinue_update_warning_state"',
        '"sod_companion_retinue_process_strength_order"',
        "sod_retinue_strength_none",
        "sod_retinue_strength_half",
        "sod_retinue_strength_full",
        "sod_retinue_recruit_policy_cautious",
        "sod_retinue_recruit_policy_balanced",
        "sod_retinue_recruit_policy_eager",
        "slot_troop_sod_retinue_post_battle_policy",
        "sod_retinue_post_battle_enabled",
        "sod_retinue_post_battle_disabled",
    ]:
        assert_contains(retinues, token)


def test_retinues_are_not_external_follower_parties() -> None:
    start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_151.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    assert_contains(start, "slot_party_type, spt_player_mercenaries")
    assert_contains(start, "slot_party_type, spt_player_patrol")
    assert_not_contains(start, "spt_companion_retinue")
    assert_contains(retinues, "spt_companion_retinue")


def test_lifecycle_and_wages_are_hooked() -> None:
    depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    wages = read("src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py")
    start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    assert_contains(depth, "script_sod_companion_retinue_process_daily")
    assert_contains(depth, "script_sod_companion_retinue_cleanup_for_departure")
    assert_contains(start, "script_sod_companion_retinue_repair_all")
    assert_contains(wages, "spt_companion_retinue")
    assert_contains(wages, "slot_party_sod_retinue_owner_troop")
    assert_contains(wages, "script_sod_companion_retinue_get_weekly_wage")
    assert_contains(wages, 'val_add, ":retinue_wages", reg0')
    assert_contains(wages, 'val_add, ":nongarrison_wages", ":retinue_wages"')
    assert_contains(retinues, "script_sod_companion_retinue_get_weekly_wage")
    assert_contains(retinues, "script_calculate_weekly_party_wage")
    assert_contains(retinues, '(store_skill_level, ":leadership", "skl_leadership", ":companion")')
    assert_contains(retinues, 'val_min, ":leadership_discount", 30')
    assert_contains(retinues, "slot_troop_sod_retinue_last_invoice")
    assert_contains(retinues, '"sod_companion_retinue_pay_weekly_wages"')
    assert_contains(retinues, '"sod_companion_retinue_update_wage_reserve"')
    assert_contains(retinues, '"sod_companion_retinue_update_supply_and_morale"')
    assert_contains(retinues, '"sod_companion_retinue_apply_training"')
    assert_contains(retinues, "script_sod_companion_retinue_process_strength_order")
    assert retinues.index("script_sod_companion_retinue_process_strength_order") < retinues.index("script_sod_companion_retinue_try_autorecruit")


def test_autonomy_is_scaffolded_but_guarded() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    for script in [
        "cf_sod_companion_retinue_can_self_manage",
        "sod_companion_retinue_try_autorecruit",
        "sod_companion_retinue_try_autoupgrade",
        "sod_companion_retinue_try_post_battle_hire",
        "sod_companion_retinue_process_post_battle_hires",
    ]:
        assert_contains(retinues, f'"{script}"')

    eligibility_start = retinues.index('"cf_sod_companion_retinue_can_self_manage"')
    eligibility_end = retinues.index('"sod_companion_retinue_select_recruit_troop"')
    eligibility = retinues[eligibility_start:eligibility_end]
    for token in [
        "main_party_has_troop",
        "slot_troop_prisoner_of_party",
        "store_troop_health",
        'ge, ":health", 35',
        "sod_companion_warning_pending",
        "sod_companion_warning_final",
        "sod_companion_warning_broken",
        "slot_troop_companion_personal_quest_stage, sod_companion_quest_failed",
        "sod_retinue_state_suspended",
        "sod_retinue_state_detached",
        "sod_retinue_state_pending_cleanup",
        "$g_player_is_captive",
        "map_free",
        "$g_sod_retinue_battle_bridge_active",
        "$g_battle_result",
    ]:
        assert_contains(eligibility, token)

    assert_contains(retinues, "slot_troop_sod_retinue_strength_order, sod_retinue_strength_none")
    assert_contains(retinues, "slot_troop_sod_retinue_recruit_policy, sod_retinue_recruit_policy_none")
    assert_contains(retinues, "script_sod_companion_retinue_calculate_recruit_budget")
    assert_contains(retinues, "script_sod_companion_retinue_calculate_upgrade_budget")
    assert_contains(retinues, "script_sod_companion_retinue_get_surplus_gold")
    assert_contains(retinues, "slot_troop_sod_retinue_wage_reserve")
    assert_contains(retinues, "script_sod_companion_retinue_get_free_capacity")
    assert_contains(retinues, "script_sod_companion_retinue_select_recruit_troop")
    assert_contains(retinues, "script_sod_companion_retinue_get_recruit_cost")
    assert_contains(retinues, "script_sod_companion_retinue_select_upgrade_troop")
    assert_contains(retinues, "script_sod_companion_retinue_get_upgrade_cost")


def test_autonomous_recruiting_uses_preferences_budget_and_target() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    for token in [
        '"sod_companion_retinue_select_recruit_troop"',
        '"sod_companion_retinue_get_identity"',
        '"sod_companion_retinue_describe_identity_to_s27"',
        '"cf_sod_companion_retinue_troop_matches_preference"',
        '"trp_npc1"',
        '"trp_khergit_tribesman"',
        '"sod_companion_retinue_select_local_recruit_troop"',
        '"trp_npc5"',
        '"trp_khergit_tribesman"',
        '"trp_npc10"',
        '"trp_rhodok_tribesman"',
        '"trp_npc16"',
        '"trp_watchman"',
        "slot_troop_companion_role",
        "sod_companion_role_quartermaster",
        "sod_companion_role_surgeon",
        "sod_companion_role_scout",
        "sod_companion_role_captain",
        "sod_companion_role_engineer",
        '"sod_companion_retinue_try_autorecruit"',
        "script_cf_sod_companion_retinue_can_self_manage",
        "slot_troop_sod_retinue_strength_order, sod_retinue_strength_none",
        "slot_troop_sod_retinue_recruit_policy, sod_retinue_recruit_policy_none",
        "script_cf_sod_companion_retinue_accepts_strength_order",
        "script_sod_companion_retinue_get_target_size",
        "assign, \":recruit_target\", \":target_size\"",
        "val_sub, \":recruit_target\", sod_retinue_half_strength_tolerance",
        "script_sod_companion_retinue_calculate_recruit_budget",
        "script_sod_companion_retinue_select_local_recruit_troop",
        "script_sod_companion_retinue_get_recruit_cost",
        "slot_troop_sod_retinue_treasury",
        "slot_center_volunteer_troop_type",
        "slot_center_volunteer_troop_amount",
        "script_spend_center_population_for_recruitment",
        "party_add_members, \":retinue_party\", \":recruit_troop\", \":take\"",
        "script_sod_company_accounts_record_company_growth",
        "sod_company_growth_recruit",
        "slot_troop_sod_retinue_last_recruit_hour",
    ]:
        assert_contains(retinues, token)


def test_companion_identity_preferences_are_flavorful_not_locking() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    checklist = read("docs/COMPANION_RETINUE_IMPLEMENTATION_CHECKLIST.md")

    identity = retinues[retinues.index('"sod_companion_retinue_get_identity"'):retinues.index('"sod_companion_retinue_get_capacity"')]
    for token in [
        "sod_retinue_pref_scout_irregular",
        "sod_retinue_pref_trade_guard",
        "sod_retinue_pref_mercy_guard",
        "sod_retinue_pref_noble_guard",
        "sod_retinue_pref_horse_archer",
        "sod_retinue_pref_redeemed_infantry",
        "sod_retinue_pref_archer_tracker",
        "sod_retinue_pref_shield_wall",
        "sod_retinue_pref_field_captain",
        "sod_retinue_pref_crossbow_veteran",
        "sod_retinue_pref_household_guard",
        "sod_retinue_pref_healer_escort",
        "sod_retinue_pref_glory_cavalry",
        "sod_retinue_pref_drilled_infantry",
        "sod_retinue_pref_engineer_support",
        "sod_retinue_pref_skirmisher",
        "@scouts and road irregulars",
        "@trade guards and mercantile escorts",
        "@protectors and mercy-minded escorts",
        "@drilled infantry and recruits under formation training",
        "@skirmishers, knife-fighters, and light irregulars",
    ]:
        assert_contains(identity, token)

    capacity = retinues[retinues.index('"sod_companion_retinue_get_capacity"'):retinues.index('"sod_companion_retinue_ensure_party"')]
    assert_contains(capacity, "script_sod_companion_retinue_get_identity")
    assert_contains(capacity, 'assign, ":martial_grade", reg1')
    assert_contains(capacity, 'ge, ":martial_grade", 3')
    assert_contains(capacity, 'val_add, ":capacity", 4')
    assert_contains(capacity, 'lt, ":martial_grade", 0')
    assert_contains(capacity, 'val_sub, ":capacity", 2')
    assert_contains(capacity, "sod_retinue_pref_healer_escort")
    assert_contains(capacity, "sod_retinue_pref_engineer_support")

    preference = retinues[retinues.index('"cf_sod_companion_retinue_troop_matches_preference"'):retinues.index('"sod_companion_retinue_select_local_recruit_troop"')]
    for token in [
        "script_sod_companion_retinue_select_recruit_troop",
        "script_sod_companion_retinue_get_identity",
        "trp_rhodok_tribesman",
        "trp_sod_mar_crossbowman",
        "trp_khergit_tribesman",
        "trp_sod_ade_light",
        "trp_refugee",
        "trp_manhunter",
    ]:
        assert_contains(preference, token)
    assert_not_contains(preference, "party_remove_members")
    assert_not_contains(preference, "party_add_members")

    training = retinues[retinues.index('"sod_companion_retinue_apply_training"'):retinues.index('"sod_companion_retinue_get_account_totals_to_regs"')]
    assert_contains(training, "script_cf_sod_companion_retinue_troop_matches_preference")
    assert_contains(training, 'val_add, ":stack_xp", 6')
    assert_contains(training, 'party_add_xp_to_stack, ":retinue_party", ":stack_no", ":stack_xp"')

    report = retinues[retinues.index('"sod_companion_retinue_describe_status_to_s20"'):retinues.index('"sod_companion_retinue_describe_focus_to_s1"')]
    assert_contains(report, "Captain's focus: {s27}.")
    assert_contains(report, "Order: full strength.")

    assert_contains(checklist, "- [x] Add optional preferred troop categories per companion.")
    assert_contains(checklist, "- [x] Do not forbid off-theme troops unless there is a strong narrative reason.")


def test_autonomous_recruiting_uses_location_culture_and_opportunity() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    start = retinues.index('"sod_companion_retinue_select_local_recruit_troop"')
    end = retinues.index('"sod_companion_retinue_get_recruit_cost"')
    selector = retinues[start:end]

    for token in [
        "$current_town",
        "centers_begin",
        "store_distance_to_party_from_party",
        "villages_begin",
        "villages_end",
        "slot_center_volunteer_troop_type",
        "slot_center_volunteer_troop_amount",
        "spt_town",
        "spt_castle",
        "store_faction_of_party",
        '"fac_kingdom_1"',
        '"trp_swadian_recruit"',
        '"fac_kingdom_2"',
        '"trp_vaegir_recruit"',
        '"fac_kingdom_3"',
        '"trp_khergit_tribesman"',
        '"fac_kingdom_4"',
        '"trp_nord_recruit"',
        '"fac_kingdom_5"',
        '"trp_rhodok_tribesman"',
        "script_sod_companion_retinue_select_recruit_troop",
    ]:
        assert_contains(selector, token)


def test_desired_strength_orders_right_size_and_warn() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    menu = read("src/menus/camp/companion_retinue_report.py")

    for token in [
        '"cf_sod_companion_retinue_accepts_strength_order"',
        "slot_troop_companion_approval",
        "lt, \":approval\", 45",
        "sod_companion_quest_resolved_hard",
        "lt, \":approval\", 55",
        "sod_companion_quest_failed",
        "sod_companion_warning_pending",
        "sod_companion_warning_final",
        "sod_companion_warning_broken",
        "sod_retinue_warning_full_refused",
        "will not take a full-strength command while trust is this strained",
        '"sod_companion_retinue_update_warning_state"',
        "sod_retinue_warning_no_troops_returning",
        "sod_retinue_warning_over_capacity",
        "sod_retinue_warning_above_target",
        "Retinue is over capacity; reclaim troops or reduce the command.",
        "Trust is too strained for a full-strength command.",
        '"sod_companion_retinue_process_strength_order"',
        "slot_troop_sod_retinue_strength_order, sod_retinue_strength_none",
        "script_sod_companion_retinue_select_retinue_troop",
        "party_get_free_companions_capacity, \":player_free\", \"p_main_party\"",
        "party_add_members, \"p_main_party\", \":troop\", \":amount\"",
        "party_remove_members, \":retinue_party\", \":troop\", \":amount\"",
        "returns {reg20} {s21} from their retinue to your command",
        "discharges {s21} because your party has no room to receive them",
        "script_sod_companion_retinue_process_strength_order",
    ]:
        assert_contains(retinues, token)

    process_start = retinues.index('"sod_companion_retinue_process_strength_order"')
    process_end = retinues.index('"sod_companion_retinue_try_autorecruit"')
    process = retinues[process_start:process_end]
    assert_not_contains(process, "party_remove_prisoners")
    assert_not_contains(process, "troop_remove_gold")

    assert_contains(menu, "Stand this retinue down.")
    assert_contains(menu, "Keep this retinue at half strength.")
    assert_contains(menu, "Build this retinue to full strength.")


def test_autonomous_upgrading_uses_retinue_party_and_surplus_budget() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    for token in [
        '"sod_companion_retinue_select_upgrade_troop"',
        "troop_get_upgrade_troop",
        "slot_troop_sod_upgrade1",
        "slot_troop_sod_upgrade2",
        "script_sod_troop_get_elite_tier",
        "lt, reg0, sod_elite_tier_noble",
        '"sod_companion_retinue_get_upgrade_cost"',
        "troop_is_mounted, \":upgrade\"",
        '"sod_companion_retinue_try_autoupgrade"',
        "script_cf_sod_companion_retinue_can_self_manage",
        "slot_troop_sod_retinue_strength_order, sod_retinue_strength_none",
        "script_sod_companion_retinue_calculate_upgrade_budget",
        "slot_troop_sod_retinue_party",
        "party_slot_eq, \":retinue_party\", slot_party_type, spt_companion_retinue",
        "party_remove_members, \":retinue_party\", \":stack_troop\", \":take\"",
        "party_add_members, \":retinue_party\", \":upgrade_troop\", \":take\"",
        "troop_set_slot, \":companion\", slot_troop_sod_retinue_treasury",
        "script_sod_company_accounts_record_company_growth",
        "sod_company_growth_upgrade",
        "slot_troop_sod_retinue_last_upgrade_hour",
    ]:
        assert_contains(retinues, token)

    autoupgrade_start = retinues.index('"sod_companion_retinue_try_autoupgrade"')
    autoupgrade_end = retinues.index('"sod_companion_retinue_try_post_battle_hire"')
    autoupgrade = retinues[autoupgrade_start:autoupgrade_end]
    assert_not_contains(autoupgrade, "p_main_party")
    assert_not_contains(autoupgrade, "trp_player")


def test_post_battle_hiring_only_takes_unclaimed_rescued_troops() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    victory_menu = read("src/menus/other/continue_06.py")

    start = retinues.index('"sod_companion_retinue_try_post_battle_hire"')
    end = retinues.index('"sod_companion_retinue_process_post_battle_hires"')
    post_battle = retinues[start:end]
    for token in [
        "$g_sod_retinue_post_battle_hiring_disabled",
        "slot_troop_sod_retinue_post_battle_policy, sod_retinue_post_battle_disabled",
        "script_cf_sod_companion_retinue_can_self_manage",
        "slot_troop_sod_retinue_strength_order, sod_retinue_strength_none",
        "slot_troop_sod_retinue_recruit_policy, sod_retinue_recruit_policy_none",
        "script_sod_companion_retinue_note_post_battle_hire_result",
        "sod_retinue_battle_hire_opted_out",
        "sod_retinue_battle_hire_no_order",
        "sod_retinue_battle_hire_no_trust",
        "sod_retinue_battle_hire_no_capacity",
        "sod_retinue_battle_hire_no_gold",
        "sod_retinue_battle_hire_no_leftovers",
        "sod_retinue_battle_hire_hired",
        "party_get_num_companion_stacks, \":num_stacks\", \"p_temp_party\"",
        "script_sod_companion_retinue_select_recruit_troop",
        "assign, \":preferred_troop\", reg0",
        "eq, \":stack_troop\", \":preferred_troop\"",
        "party_stack_get_troop_id, \":stack_troop\", \"p_temp_party\"",
        "neg|troop_is_hero",
        "script_sod_troop_get_elite_tier",
        "lt, reg0, sod_elite_tier_noble",
        "script_sod_companion_retinue_calculate_recruit_budget",
        "party_remove_members, \"p_temp_party\", \":selected_troop\", \":selected_count\"",
        "party_add_members, \":retinue_party\", \":selected_troop\", \":selected_count\"",
        "slot_troop_sod_retinue_treasury",
        "script_sod_company_accounts_record_company_growth",
        "has taken {reg20} {s21} from the freed stragglers under their command",
    ]:
        assert_contains(post_battle, token)
    assert_contains(retinues, "Last battlefield hiring: wanted recruits, but the command purse lacked surplus gold.")
    assert_contains(retinues, "Last battlefield hiring: wanted recruits, but the retinue had no room under its current order.")
    assert_contains(retinues, "Last battlefield hiring: wanted recruits, but command trust or captain readiness was not steady enough.")
    assert_not_contains(post_battle, "party_get_num_prisoners")
    assert_not_contains(post_battle, "party_remove_prisoners")

    assert_contains(victory_menu, "script_sod_companion_retinue_process_post_battle_hires")
    assert victory_menu.index("change_screen_exchange_with_party") < victory_menu.index("script_sod_companion_retinue_process_post_battle_hires")
    assert victory_menu.index("script_sod_companion_retinue_process_post_battle_hires") < victory_menu.index("script_total_victory_distribute_leftovers")


def test_retinue_management_menu_is_safe_and_reachable() -> None:
    camp = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    order = read("src/menus/_order_game_menus.txt")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    dialog = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_retinue_command.py")
    menu = read("src/menus/camp/companion_retinue_report.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    assert_contains(camp, "mnu_companion_retinue_report")
    assert_contains(camp, "Review companion retinues.")
    assert_contains(order, "camp/companion_retinue_report.py")
    assert_contains(dialog_order, "ZZ99_misc_dialogs/anyone_plyr_regular_member_retinue_command.py")
    assert_contains(dialog, "Let's speak about the troops under your command.")
    assert_contains(dialog, "regular_member_retinue_command")
    assert_contains(dialog, "script_sod_companion_retinue_describe_dialogue_to_s28")
    assert_contains(dialog, "Show me your command rolls.")
    assert_contains(dialog, "is_between, \"$g_talk_troop\", companions_begin, companions_end")
    assert_contains(dialog, "main_party_has_troop, \"$g_talk_troop\"")
    assert_contains(dialog, "mnu_companion_retinue_manage")

    assert_contains(menu, '"companion_retinue_report"')
    assert_contains(menu, '"companion_retinue_manage"')
    assert_contains(menu, '"companion_retinue_assign_troops"')
    assert_contains(menu, '"companion_retinue_reclaim_troops"')
    assert_contains(menu, "script_sod_companion_retinue_describe_report_to_s1")
    assert_contains(menu, "script_sod_companion_retinue_describe_focus_to_s1")
    assert_contains(menu, "script_sod_companion_retinue_describe_transfer_to_s1")
    assert_contains(menu, "script_sod_companion_retinue_set_strength_order")
    assert_contains(menu, "script_sod_companion_retinue_set_recruit_policy")
    assert_contains(menu, "sod_retinue_strength_none")
    assert_contains(menu, "sod_retinue_strength_half")
    assert_contains(menu, "sod_retinue_strength_full")
    assert_contains(menu, "sod_retinue_recruit_policy_none")
    assert_contains(menu, "sod_retinue_recruit_policy_cautious")
    assert_contains(menu, "sod_retinue_recruit_policy_balanced")
    assert_contains(menu, "sod_retinue_recruit_policy_eager")
    assert_contains(menu, "$g_sod_retinue_post_battle_hiring_disabled")
    assert_contains(menu, "Disable all post-battle retinue hiring.")
    assert_contains(menu, "Enable post-battle retinue hiring.")
    assert_contains(menu, "Do not take freed troops after battles.")
    assert_contains(menu, "Allow taking suitable freed troops after battles.")
    assert_contains(menu, "script_sod_companion_retinue_set_post_battle_policy")
    assert_contains(menu, "sod_retinue_post_battle_enabled")
    assert_contains(menu, "sod_retinue_post_battle_disabled")
    assert_contains(menu, "script_sod_companion_retinue_add_gold")
    assert_contains(menu, "script_sod_companion_retinue_remove_gold")
    assert_contains(menu, "script_sod_companion_retinue_can_accept_troop")
    assert_contains(menu, "script_sod_companion_retinue_add_troops")
    assert_contains(menu, "script_sod_companion_retinue_remove_troops")
    assert_contains(menu, "script_sod_companion_retinue_add_troops_up_to_capacity")
    assert_contains(menu, "script_sod_companion_retinue_remove_troops_up_to_capacity")
    assert_contains(menu, "script_sod_companion_retinue_select_main_party_troop")
    assert_contains(menu, "script_sod_companion_retinue_select_retinue_troop")
    assert_contains(menu, "party_get_free_companions_capacity")
    assert_contains(menu, "$g_sod_retinue_focus_companion")
    assert_contains(menu, "$g_sod_retinue_selected_troop")
    assert_contains(menu, "main_party_has_troop")
    assert_not_contains(menu, "change_screen_exchange_with_party")
    assert_not_contains(menu, "change_screen_exchange_members")

    assert_contains(retinues, "sod_companion_retinue_describe_report_to_s1")
    assert_contains(retinues, "sod_companion_retinue_describe_focus_to_s1")
    assert_contains(retinues, "sod_companion_retinue_describe_transfer_to_s1")
    assert_contains(retinues, "sod_companion_retinue_describe_dialogue_to_s28")
    assert_contains(retinues, "sod_companion_retinue_describe_voice_to_s29")
    assert_contains(retinues, "Road men do best")
    assert_contains(retinues, "I will not waste lives for pride")
    assert_contains(retinues, "Crossbows, veterans, steady infantry")
    assert_contains(retinues, "Give me quiet feet, quick hands")
    assert_contains(retinues, "Command distinction: your personal party")
    assert_contains(retinues, "external follower parties are separate map companies")
    assert_contains(retinues, "garrisons remain tied to towns and castles")
    assert_contains(retinues, "Warning: loyalty is strained.")
    assert_contains(retinues, "Assigning costly troops to this command")
    assert_contains(retinues, "Warning: your personal party can currently receive only {reg26}.")
    assert_contains(retinues, "Reclaiming the whole stack would exceed your direct command capacity.")
    assert_contains(retinues, "The purse holds {reg23} denars; wages due this week are {reg24}.")
    assert_contains(retinues, "not a full command while trust is this strained")
    assert_contains(retinues, "Post-battle retinue hiring: enabled for companions who allow it.")
    assert_contains(retinues, "Captain's focus: {s27}.")
    assert_contains(retinues, "Captain's note: {s24} {s22}")
    assert_contains(retinues, "Last battlefield hiring:")


def test_command_purse_pays_retinue_wages_first() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    payday = read("src/menus/0000_hardcoded_mb1011/pay_day.py")

    assert_contains(retinues, '"sod_companion_retinue_pay_weekly_wages"')
    assert_contains(retinues, "script_sod_companion_retinue_get_weekly_wage")
    assert_contains(retinues, "slot_troop_sod_retinue_treasury")
    assert_contains(retinues, "slot_troop_sod_retinue_wage_reserve")
    assert_contains(retinues, "slot_troop_sod_retinue_last_shortage")
    assert_contains(retinues, "troop_set_slot, \":companion\", slot_troop_sod_retinue_treasury")
    assert_contains(retinues, '"sod_companion_retinue_get_surplus_gold"')
    assert_contains(retinues, "store_sub, \":surplus\", \":treasury\", \":reserve\"")
    assert_contains(retinues, '"sod_companion_retinue_calculate_recruit_budget"')
    assert_contains(retinues, '"sod_companion_retinue_calculate_upgrade_budget"')
    assert_contains(retinues, "assign, reg0, \":total_paid_by_purses\"")
    assert_contains(retinues, "assign, reg2, \":total_shortage\"")
    assert_contains(retinues, "assign, reg3, \":player_covered_shortage\"")
    assert_contains(retinues, "assign, reg4, \":unpaid_shortage\"")
    assert_contains(retinues, "sod_retinue_wage_shortage_player_auto_cover")
    assert_contains(retinues, "sod_retinue_wage_shortage_purse_only")
    assert_contains(retinues, "script_sod_companion_retinue_apply_unpaid_wage_consequences")
    assert_contains(retinues, "Wage reserve: {reg25} week(s).")

    assert_contains(payday, "script_sod_companion_retinue_pay_weekly_wages")
    assert_contains(payday, "val_sub, \":total_wages\", reg10")
    assert_contains(payday, "val_add, \":total_wages\", reg12")
    assert_contains(payday, "Companion command cost: {reg10} denars")
    assert_contains(payday, "Retinue shortages covered by this wage bill: {reg12} denars")


def test_retinue_supply_morale_and_training_are_separate_from_player_overcrowding() -> None:
    constants = read("src/constants/module_constants.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    morale = read("src/scripts/ZC_parties/get_player_party_morale_values.py")
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")

    for token in [
        "slot_troop_sod_retinue_supply_pressure",
        "slot_troop_sod_retinue_last_morale",
        "slot_troop_sod_retinue_last_training_xp",
        "slot_troop_sod_retinue_last_training_hour",
        "slot_troop_sod_retinue_last_desertion_day",
    ]:
        assert_contains(constants, token)

    for token in [
        '"sod_companion_retinue_update_supply_and_morale"',
        "store_skill_level, \":leadership\", \"skl_leadership\", \":companion\"",
        "slot_troop_companion_role",
        "sod_companion_role_quartermaster",
        "sod_companion_role_captain",
        "slot_troop_sod_retinue_supply_pressure",
        "cohesion {reg26}",
        "health {s25}",
        "loyalty risk {s26}",
        "supply pressure {reg27}",
        '"sod_companion_retinue_apply_desertion_risk"',
        "party_remove_members, \":retinue_party\", \":troop\", \":deserters\"",
        '"sod_companion_retinue_apply_training"',
        "store_skill_level, \":trainer\", \"skl_trainer\", \":companion\"",
        "party_add_xp_to_stack, \":retinue_party\", \":stack_no\", \":stack_xp\"",
        "sod_retinue_policy_training",
        "sod_companion_quest_resolved_good",
        "sod_companion_quest_resolved_hard",
        "val_min, \":xp_per_stack\", 60",
        '"sod_companion_retinue_get_account_totals_to_regs"',
    ]:
        assert_contains(retinues, token)

    assert_contains(morale, "$g_player_party_morale_modifier_retinue_cohesion")
    assert_contains(morale, "script_sod_companion_retinue_get_account_totals_to_regs")
    assert_contains(morale, "lt, reg(75), 45")
    assert_contains(morale, "val_sub, \":new_morale\", \"$g_player_party_morale_modifier_retinue_cohesion\"")
    assert_contains(accounts, "Companion command accounts:")
    assert_contains(accounts, "Companion retinue supply pressure:")
    assert_contains(start, "$g_sod_retinue_wage_shortage_policy")


def test_relationship_effects_drive_retinue_risk_and_reports() -> None:
    constants = read("src/constants/module_constants.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")

    assert_contains(constants, "sod_companion_quest_failed")

    capacity = retinues[retinues.index('"sod_companion_retinue_get_capacity"'):retinues.index('"sod_companion_retinue_ensure_party"')]
    for token in [
        "sod_companion_warning_broken",
        '(val_sub, ":capacity", 20)',
        "sod_companion_quest_failed",
        '(assign, ":capacity", 0)',
    ]:
        assert_contains(capacity, token)

    ensure = retinues[retinues.index('"sod_companion_retinue_ensure_party"'):retinues.index('"sod_companion_retinue_get_size"')]
    assert_contains(ensure, "slot_troop_companion_personal_quest_stage")
    assert_contains(ensure, "sod_companion_quest_failed")
    assert_contains(ensure, "slot_troop_sod_retinue_state, sod_retinue_state_suspended")

    recruit_budget = retinues[retinues.index('"sod_companion_retinue_calculate_recruit_budget"'):retinues.index('"sod_companion_retinue_calculate_upgrade_budget"')]
    upgrade_budget = retinues[retinues.index('"sod_companion_retinue_calculate_upgrade_budget"'):retinues.index('"cf_sod_companion_retinue_can_self_manage"')]
    for section in [recruit_budget, upgrade_budget]:
        assert_contains(section, "slot_troop_companion_approval")
        assert_contains(section, 'ge, ":approval", 80')
        assert_contains(section, 'val_mul, ":budget", 80')
        assert_contains(section, 'lt, ":approval", 20')
        assert_contains(section, 'val_mul, ":budget", 120')

    morale = retinues[retinues.index('"sod_companion_retinue_update_supply_and_morale"'):retinues.index('"sod_companion_retinue_apply_desertion_risk"')]
    for token in [
        "slot_troop_companion_approval",
        "slot_troop_companion_warning_state",
        "slot_troop_companion_personal_quest_stage",
        "sod_companion_warning_pending",
        "sod_companion_warning_acknowledged",
        "sod_companion_warning_final",
        "sod_companion_warning_broken",
        "sod_companion_quest_resolved_good",
        "sod_companion_quest_resolved_hard",
        "sod_companion_quest_failed",
    ]:
        assert_contains(morale, token)

    daily = retinues[retinues.index('"sod_companion_retinue_process_daily"'):retinues.index('"sod_companion_retinue_repair_all"')]
    assert_contains(daily, 'le, ":retinue_morale", 20')
    assert_contains(daily, "slot_troop_companion_warning_state")
    assert_contains(daily, "script_sod_companion_retinue_apply_desertion_risk")

    report = retinues[retinues.index('"sod_companion_retinue_describe_status_to_s20"'):retinues.index('"sod_companion_retinue_describe_focus_to_s1"')]
    assert_contains(report, "health {s25}; loyalty risk {s26}")
    assert_contains(report, "health {s6}; loyalty risk {s7}")
    assert_contains(report, "@fracturing")
    assert_contains(report, "@serious")
    assert_contains(report, "@watchful")


def test_retinue_battle_bridge_uses_hidden_allied_parties_not_main_party_merge() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    simple_encounter = read("src/menus/0000_hardcoded_mb1011/simple_encounter.py")
    victory = read("src/scripts/ZC_parties/total_victory_finalize.py")
    defeat = read("src/menus/other/total_defeat.py")
    qa = read("docs/COMPANION_RETINUE_BATTLE_QA.md")

    for token in [
        '"sod_companion_retinue_join_current_battle"',
        "party_quick_attach_to_current_battle, \":retinue_party\", 0",
        '"sod_companion_retinue_snapshot_for_battle"',
        '"sod_companion_retinue_validate_battle_outcome"',
        "$g_sod_retinue_battle_bridge_active",
        '"sod_companion_retinue_finish_battle_bridge"',
        "party_attach_to_party, \":retinue_party\", \"p_main_party\"",
        '"sod_companion_retinue_handle_player_defeat"',
        "distribute_party_among_party_group, \"p_temp_party\", \"$g_enemy_party\"",
        "slot_troop_sod_retinue_state, sod_retinue_state_suspended",
        '"cf_sod_companion_retinue_can_merge_fallback"',
        '"sod_companion_retinue_join_current_battle_by_merge_fallback"',
        '"sod_companion_retinue_finish_merge_fallback"',
        "$g_sod_retinue_battle_bridge_force_merge",
        "$g_sod_retinue_battle_bridge_mode",
        "slot_troop_sod_retinue_battle_store_party",
        "disable_party, \":store_party\"",
        "party_count_members_of_type, \":player_has_type\", \"p_main_party\", \":stack_troop\"",
        "party_add_members, \":store_party\", \":stack_troop\", \":stack_size\"",
        "party_add_members, \"p_main_party\", \":stack_troop\", \":stack_size\"",
        "party_remove_members, \":retinue_party\", \":stack_troop\", \":stack_size\"",
        "party_remove_members, \"p_main_party\", \":stack_troop\", \":restore\"",
        "party_add_members, \":retinue_party\", \":stack_troop\", \":restore\"",
        "Retinue battle repair: removed duplicate post-battle troops",
    ]:
        assert_contains(retinues, token)

    join_start = retinues.index('("sod_companion_retinue_join_current_battle"')
    join_end = retinues.index('("sod_companion_retinue_finish_merge_fallback"')
    join_bridge = retinues[join_start:join_end]
    assert_not_contains(join_bridge, "party_remove_members")
    assert_not_contains(join_bridge, "party_add_members")

    fallback_start = retinues.index('("sod_companion_retinue_join_current_battle_by_merge_fallback"')
    fallback_end = retinues.index('("sod_companion_retinue_join_current_battle"')
    fallback = retinues[fallback_start:fallback_end]
    assert_contains(fallback, "script_cf_sod_companion_retinue_can_merge_fallback")
    assert_contains(fallback, "disable_party, \":store_party\"")
    assert_not_contains(fallback, "party_quick_attach_to_current_battle")

    assert_contains(simple_encounter, "script_sod_companion_retinue_join_current_battle")
    assert_contains(simple_encounter, "script_sod_companion_retinue_finish_battle_bridge")
    assert_contains(victory, "script_sod_companion_retinue_finish_battle_bridge")
    assert_contains(defeat, "script_sod_companion_retinue_handle_player_defeat")
    assert defeat.index("script_sod_companion_retinue_handle_player_defeat") < defeat.index("script_party_remove_all_companions")

    for token in [
        "Ordinary Field Battle",
        "Siege Attack",
        "Siege Defense",
        "Village Raid Defense",
        "Ambush Or Quest Battle",
        "Merge Fallback Check",
        "No retinue stack is duplicated after battle.",
    ]:
        assert_contains(qa, token)


def test_departure_capture_and_failure_rules_are_explicit() -> None:
    constants = read("src/constants/module_constants.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    retire = read("src/scripts/ZH_heroes/retire_companion.py")
    quitting = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_yes.py")
    capture = read("src/scripts/ZC_parties/event_player_captured_as_prisoner.py")
    wilderness_capture = read("src/menus/other/continue_48.py")
    depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")

    for token in [
        "sod_retinue_departure_cleanup",
        "sod_retinue_departure_peaceful",
        "sod_retinue_departure_angry",
        "sod_retinue_departure_captured",
        "sod_retinue_state_suspended",
        "sod_retinue_state_pending_cleanup",
    ]:
        assert_contains(constants, token)

    assert_contains(retinues, '"sod_companion_retinue_suspend_for_absence"')
    absence = retinues[retinues.index('"sod_companion_retinue_suspend_for_absence"'):retinues.index('"sod_companion_retinue_cleanup_for_departure"')]
    for token in [
        "script_sod_companion_retinue_clear_battle_store",
        "party_set_ai_behavior, \":retinue_party\", ai_bhvr_hold",
        "party_attach_to_party, \":retinue_party\", \"p_main_party\"",
        "slot_party_sod_retinue_state, sod_retinue_state_suspended",
        "slot_party_sod_retinue_anchor_party, \"p_main_party\"",
        "slot_troop_sod_retinue_state, sod_retinue_state_suspended",
        "slot_troop_sod_retinue_recruit_policy, sod_retinue_recruit_policy_none",
        "slot_troop_sod_retinue_last_shortage, 0",
        "slot_troop_sod_retinue_wage_reserve, 0",
    ]:
        assert_contains(absence, token)

    cleanup = retinues[retinues.index('"sod_companion_retinue_cleanup_for_departure"'):]
    for token in [
        "sod_retinue_departure_captured",
        "script_sod_companion_retinue_suspend_for_absence",
        "sod_retinue_departure_angry",
        "slot_troop_companion_approval",
        "sod_companion_warning_broken",
        "sod_companion_warning_final",
        "party_get_free_companions_capacity, \":free_capacity\", \"p_main_party\"",
        "party_add_members, \"p_main_party\", \":stack_troop\", \":return_amount\"",
        "party_remove_members, \":retinue_party\", \":stack_troop\", \":still_in_retinue\"",
        "script_troop_add_gold",
        "follow the companion or scatter",
        "scatter for lack of room",
        "slot_troop_sod_retinue_treasury, 0",
        "slot_troop_sod_retinue_strength_order, sod_retinue_strength_none",
        "slot_troop_sod_retinue_recruit_policy, sod_retinue_recruit_policy_none",
    ]:
        assert_contains(cleanup, token)

    daily = retinues[retinues.index('"sod_companion_retinue_process_daily"'):retinues.index('"sod_companion_retinue_repair_all"')]
    repair = retinues[retinues.index('"sod_companion_retinue_repair_all"'):retinues.index('"sod_companion_retinue_suspend_for_absence"')]
    for section in [daily, repair]:
        assert_contains(section, "slot_troop_sod_retinue_state, sod_retinue_state_suspended")
        assert_contains(section, "script_sod_companion_retinue_suspend_for_absence")
        assert_contains(section, "script_sod_companion_retinue_cleanup_for_departure")
        assert section.index("script_sod_companion_retinue_suspend_for_absence") < section.index("script_sod_companion_retinue_cleanup_for_departure")

    accept = retinues[retinues.index('"sod_companion_retinue_can_accept_troop"'):retinues.index('"sod_companion_retinue_add_troops"')]
    assert_contains(accept, "sod_retinue_state_suspended")
    assert_contains(accept, "sod_retinue_state_detached")
    assert_contains(accept, "sod_retinue_state_pending_cleanup")
    assert_contains(accept, "slot_troop_prisoner_of_party")
    assert_contains(accept, "store_troop_health")
    assert_contains(accept, "ge, \":health\", 35")
    assert_contains(accept, "slot_troop_companion_personal_quest_stage, sod_companion_quest_failed")

    payday = retinues[retinues.index('"sod_companion_retinue_pay_weekly_wages"'):retinues.index('"sod_companion_retinue_apply_unpaid_wage_consequences"')]
    assert_contains(payday, "slot_troop_sod_retinue_state, sod_retinue_state_suspended")

    defeat = retinues[retinues.index('"sod_companion_retinue_handle_player_defeat"'):retinues.index('"sod_companion_retinue_process_daily"')]
    for token in [
        "distribute_party_among_party_group, \"p_temp_party\", \"$g_enemy_party\"",
        "remove_party, \":retinue_party\"",
        "slot_troop_sod_retinue_state, sod_retinue_state_suspended",
        "slot_troop_sod_retinue_post_battle_policy, sod_retinue_post_battle_disabled",
        "slot_troop_sod_retinue_recruit_policy, sod_retinue_recruit_policy_none",
    ]:
        assert_contains(defeat, token)

    assert_contains(retire, "sod_retinue_departure_peaceful")
    assert retire.index("script_sod_companion_retinue_cleanup_for_departure") < retire.index("remove_member_from_party")
    assert_contains(quitting, "sod_retinue_departure_angry")
    assert quitting.index("script_sod_companion_retinue_cleanup_for_departure") < quitting.index("remove_member_from_party")
    assert_contains(capture, "script_sod_companion_retinue_handle_player_defeat")
    assert_contains(wilderness_capture, "script_sod_companion_retinue_handle_player_defeat")
    assert wilderness_capture.index("script_sod_companion_retinue_handle_player_defeat") < wilderness_capture.index("remove_member_from_party")
    assert_contains(depth, "sod_companion_cleanup_absent_state")
    assert_contains(depth, "slot_troop_sod_retinue_state, sod_retinue_state_suspended")
    assert_contains(depth, "script_sod_companion_retinue_suspend_for_absence")


def test_retinue_exploit_and_edge_case_controls_are_hardened() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    wages = read("src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py")
    morale = read("src/scripts/ZC_parties/get_player_party_morale_values.py")
    external_start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_151.py")
    external_order = read("src/scripts/ZC_parties/sod_external_party_set_order.py")
    safe_party = read("src/scripts/ZC_parties/sod_party_is_safe_active_to_reg.py")
    retinue_menu = read("src/menus/camp/companion_retinue_report.py")
    enter_town = read("src/scripts/ZZ_common_array_processing/enter_town_center_from_passage.py")
    tournament = read("src/menus/arena_tournament/tournament_view_participants.py")
    sneak = read("src/menus/other/continue_45.py")

    assert_contains(retinues, '"sod_companion_retinue_sanitize_state"')
    sanitize = retinues[retinues.index('"sod_companion_retinue_sanitize_state"'):retinues.index('"sod_companion_retinue_get_capacity"')]
    for token in [
        "val_clamp, \":approval\", 0, 101",
        "sod_companion_warning_none",
        "sod_companion_warning_broken",
        "sod_companion_quest_none",
        "sod_companion_quest_failed",
        "sod_retinue_state_inactive",
        "sod_retinue_state_pending_cleanup",
        "sod_retinue_policy_balanced",
        "sod_retinue_policy_guard_companion",
        "sod_retinue_strength_none",
        "sod_retinue_strength_full",
        "sod_retinue_recruit_policy_none",
        "sod_retinue_recruit_policy_eager",
        "sod_retinue_post_battle_enabled",
        "sod_retinue_post_battle_disabled",
        "sod_retinue_max_command_purse",
        "slot_troop_sod_retinue_treasury",
        "val_min, \":treasury\", sod_retinue_max_command_purse",
        "slot_troop_sod_retinue_last_shortage",
        "slot_troop_sod_retinue_wage_reserve",
        "slot_troop_sod_retinue_last_morale",
        "slot_troop_sod_retinue_supply_pressure",
        "slot_troop_sod_retinue_last_training_xp",
        "slot_party_sod_retinue_owner_troop",
        "slot_party_sod_retinue_anchor_party, \"p_main_party\"",
        "party_set_ai_behavior, \":retinue_party\", ai_bhvr_hold",
        "slot_party_ai_state, spai_undefined",
        "slot_party_ai_object, -1",
        "slot_party_ai_substate, 0",
        "slot_party_follow_me, 0",
        "party_get_num_prisoner_stacks",
        "party_remove_prisoners, \":retinue_party\"",
        "troop_is_hero, \":stack_troop\"",
        "party_add_members, \"p_main_party\", \":stack_troop\", \":stack_size\"",
        "neg|is_between, \":stack_troop\", soldiers_begin, soldiers_end",
        "party_remove_members, \":retinue_party\", \":stack_troop\", \":stack_size\"",
    ]:
        assert_contains(sanitize, token)

    capacity = retinues[retinues.index('"sod_companion_retinue_get_capacity"'):retinues.index('"sod_companion_retinue_ensure_party"')]
    assert_contains(capacity, "script_sod_companion_retinue_sanitize_state")
    assert capacity.index("script_sod_companion_retinue_sanitize_state") < capacity.index("slot_troop_companion_approval")

    ensure = retinues[retinues.index('"sod_companion_retinue_ensure_party"'):retinues.index('"sod_companion_retinue_get_size"')]
    assert_contains(ensure, "script_sod_companion_retinue_sanitize_state")
    assert_contains(ensure, "slot_party_ai_state, spai_undefined")
    assert_contains(ensure, "slot_party_ai_object, -1")
    assert_contains(ensure, "slot_party_ai_substate, 0")
    assert_contains(ensure, "slot_party_follow_me, 0")

    gold = retinues[retinues.index('"sod_companion_retinue_add_gold"'):retinues.index('"sod_companion_retinue_get_surplus_gold"')]
    for token in [
        "store_troop_gold, \":player_gold\", \"trp_player\"",
        "ge, \":player_gold\", \":amount\"",
        "troop_remove_gold, \"trp_player\", \":amount\"",
        "val_max, \":treasury\", 0",
        "val_min, \":treasury\", sod_retinue_max_command_purse",
        "ge, \":treasury\", \":amount\"",
        "val_sub, \":treasury\", \":amount\"",
        "script_troop_add_gold",
        "script_sod_companion_retinue_update_wage_reserve",
    ]:
        assert_contains(gold, token)

    for script_name in [
        '"sod_companion_retinue_pay_weekly_wages"',
        '"sod_companion_retinue_try_autorecruit"',
        '"sod_companion_retinue_try_autoupgrade"',
        '"sod_companion_retinue_try_post_battle_hire"',
    ]:
        start = retinues.index(script_name)
        end = retinues.find('("', start + 1)
        section = retinues[start:end if end != -1 else len(retinues)]
        assert_contains(section, "val_max, \":treasury\", 0")

    for token in [
        "script_sod_companion_retinue_get_account_totals_to_regs",
        "$g_player_party_morale_modifier_retinue_cohesion",
        "val_sub, \":new_morale\", \"$g_player_party_morale_modifier_retinue_cohesion\"",
    ]:
        assert_contains(morale, token)
    assert_contains(wages, "spt_companion_retinue")
    assert_contains(wages, "script_sod_companion_retinue_get_weekly_wage")
    assert_contains(wages, "val_add, \":nongarrison_wages\", \":retinue_wages\"")

    warning = retinues[retinues.index('"sod_companion_retinue_update_warning_state"'):retinues.index('"sod_companion_retinue_set_strength_order"')]
    autorecruit = retinues[retinues.index('"sod_companion_retinue_try_autorecruit"'):retinues.index('"sod_companion_retinue_try_autoupgrade"')]
    post_battle = retinues[retinues.index('"sod_companion_retinue_try_post_battle_hire"'):retinues.index('"sod_companion_retinue_process_post_battle_hires"')]
    assert_contains(warning, "sod_retinue_half_strength_tolerance")
    assert_contains(autorecruit, "sod_retinue_half_strength_tolerance")
    assert_contains(post_battle, "sod_retinue_half_strength_tolerance")
    assert_contains(post_battle, "party_get_num_companion_stacks, \":num_stacks\", \"p_temp_party\"")
    assert_contains(post_battle, "party_remove_members, \"p_temp_party\", \":selected_troop\", \":selected_count\"")
    assert_contains(post_battle, "party_add_members, \":retinue_party\", \":selected_troop\", \":selected_count\"")

    accept = retinues[retinues.index('"sod_companion_retinue_can_accept_troop"'):retinues.index('"sod_companion_retinue_add_troops"')]
    add = retinues[retinues.index('"sod_companion_retinue_add_troops"'):retinues.index('"sod_companion_retinue_remove_troops"')]
    remove = retinues[retinues.index('"sod_companion_retinue_remove_troops"'):retinues.index('"sod_companion_retinue_add_troops_up_to_capacity"')]
    for section in [accept, add, remove]:
        assert_contains(section, "gt, \":amount\", 0")
        assert_contains(section, "is_between, \":troop\", soldiers_begin, soldiers_end")
        assert_contains(section, "neg|troop_is_hero")
    assert_contains(add, "party_count_members_of_type, \":available_now\", \"p_main_party\", \":troop\"")
    assert_contains(add, "ge, \":available_now\", \":amount\"")
    assert_contains(remove, "party_count_members_of_type, \":available\", \":retinue_party\", \":troop\"")
    assert_contains(remove, "ge, \":available\", \":amount\"")
    assert_contains(remove, "party_get_free_companions_capacity, \":free_capacity\", \"p_main_party\"")
    assert_contains(remove, "ge, \":free_capacity\", \":amount\"")

    assert_not_contains(retinue_menu, "change_screen_exchange_with_party")
    assert_not_contains(retinue_menu, "change_screen_exchange_members")
    assert_contains(retinue_menu, "script_sod_companion_retinue_add_troops")
    assert_contains(retinue_menu, "script_sod_companion_retinue_remove_troops")
    assert_contains(retinues, "Wages due this week: {reg24} denars")
    assert_contains(retinues, "Command purse cannot cover this week's wages")
    assert_contains(external_start, "spt_player_mercenaries")
    assert_contains(external_start, "spt_player_patrol")
    assert_not_contains(external_start, "spt_companion_retinue")
    assert_contains(external_order, "spt_player_mercenaries")
    assert_contains(external_order, "spt_player_patrol")
    assert_not_contains(external_order, "spt_companion_retinue")
    assert_contains(safe_party, "neg|party_slot_eq, \":party_no\", slot_party_type, spt_companion_retinue")

    assert_contains(enter_town, "script_sod_companion_retinue_repair_all")
    assert_contains(tournament, "script_sod_companion_retinue_repair_all")
    assert_contains(sneak, "script_sod_companion_retinue_repair_all")


def test_retinue_integration_audit_surfaces_are_covered() -> None:
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    faction_wage = read("src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py")
    troop_wage = read("src/scripts/ZA_hardcoded_game_scripts/game_get_troop_wage.py")
    total_wage = read("src/scripts/ZA_hardcoded_game_scripts/game_get_total_wage.py")
    morale = read("src/scripts/ZC_parties/get_player_party_morale_values.py")
    accounts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    payday = read("src/menus/0000_hardcoded_mb1011/pay_day.py")
    nearby_join = read("src/scripts/ZB_economy_and_trade/let_nearby_parties_join_current_battle.py")
    nearby_strength = read("src/scripts/ZC_parties/party_calculate_and_set_nearby_friend_strength.py")
    simple_encounter = read("src/menus/0000_hardcoded_mb1011/simple_encounter.py")
    siege_defense = read("src/menus/centers/castle/siege_defender_join_battle.py")
    siege_attack = read("src/menus/centers/castle/siege_request_meeting.py")
    siege_ally = read("src/menus/centers/castle/talk_to_siege_commander.py")
    village_raid = read("src/menus/centers/village/village_raid_attack.py")
    defeat = read("src/menus/other/total_defeat.py")
    capture = read("src/scripts/ZC_parties/event_player_captured_as_prisoner.py")
    recruit = read("src/scripts/ZH_heroes/recruit_troop_as_companion.py")
    retire = read("src/scripts/ZH_heroes/retire_companion.py")
    quitting = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_yes.py")
    depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    external_start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_151.py")
    external_order = read("src/scripts/ZC_parties/sod_external_party_set_order.py")

    for token in [
        "spt_companion_retinue",
        "slot_party_sod_retinue_owner_troop",
        "script_sod_companion_retinue_get_weekly_wage",
        "val_add, \":nongarrison_wages\", \":retinue_wages\"",
    ]:
        assert_contains(faction_wage, token)
    assert_contains(total_wage, "script_calculate_player_faction_wage")
    assert_not_contains(troop_wage, "spt_companion_retinue")

    for token in [
        "$g_player_party_morale_modifier_retinue_cohesion",
        "script_sod_companion_retinue_get_account_totals_to_regs",
        "val_sub, \":new_morale\", \"$g_player_party_morale_modifier_retinue_cohesion\"",
    ]:
        assert_contains(morale, token)
    for token in [
        "Companion command accounts",
        "Companion retinue supply pressure",
        "script_sod_companion_retinue_get_account_totals_to_regs",
    ]:
        assert_contains(accounts, token)
    for token in [
        "script_sod_companion_retinue_pay_weekly_wages",
        "Companion command cost",
        "Retinue shortages covered by this wage bill",
        "Unpaid retinue shortages",
    ]:
        assert_contains(payday, token)
    for token in [
        '"sod_companion_retinue_add_gold"',
        '"sod_companion_retinue_remove_gold"',
        '"sod_companion_retinue_get_upgrade_cost"',
        '"sod_companion_retinue_try_autoupgrade"',
        '"sod_companion_retinue_apply_training"',
        '"sod_companion_retinue_update_supply_and_morale"',
        "slot_troop_companion_grievance",
    ]:
        assert_contains(retinues, token)

    capacity = retinues[retinues.index('"sod_companion_retinue_get_capacity"'):retinues.index('"sod_companion_retinue_ensure_party"')]
    supply_morale = retinues[retinues.index('"sod_companion_retinue_update_supply_and_morale"'):retinues.index('"sod_companion_retinue_apply_desertion_risk"')]
    accepts_order = retinues[retinues.index('"cf_sod_companion_retinue_accepts_strength_order"'):retinues.index('"sod_companion_retinue_update_warning_state"')]
    for section in [capacity, supply_morale, accepts_order]:
        assert_contains(section, "slot_troop_companion_grievance")
    assert_contains(capacity, "val_sub, \":capacity\", 8")
    assert_contains(supply_morale, "val_add, \":supply_pressure\", 2")
    assert_contains(supply_morale, "val_sub, \":morale\", 8")
    assert_contains(accepts_order, "ge, \":grievance\", 75")

    for script in [nearby_join, nearby_strength]:
        assert_contains(script, "spt_companion_retinue")
        assert_contains(script, "neg|party_slot_eq")
    for menu in [simple_encounter, siege_defense, siege_attack, siege_ally, village_raid]:
        assert_contains(menu, "script_sod_companion_retinue_join_current_battle")
        assert_contains(menu, "set_party_battle_mode")
        assert menu.index("script_sod_companion_retinue_join_current_battle") < menu.index("set_party_battle_mode")
    assert_contains(simple_encounter, "script_sod_companion_retinue_finish_battle_bridge")
    assert_contains(defeat, "script_sod_companion_retinue_handle_player_defeat")
    assert_contains(capture, "script_sod_companion_retinue_handle_player_defeat")

    assert_contains(recruit, "script_sod_companion_retinue_ensure_party")
    assert recruit.index("party_force_add_members") < recruit.index("script_sod_companion_retinue_ensure_party")
    assert_contains(recruit, "script_sod_companion_retinue_update_warning_state")
    assert_contains(retire, "script_sod_companion_retinue_cleanup_for_departure")
    assert_contains(quitting, "script_sod_companion_retinue_cleanup_for_departure")
    assert_contains(depth, "script_sod_companion_retinue_process_daily")
    assert_contains(depth, "script_sod_companion_cleanup_absent_state")
    assert_contains(depth, "script_sod_companion_retinue_suspend_for_absence")
    assert_contains(depth, "script_sod_companion_apply_role_effects")

    assert_contains(external_start, "spt_player_mercenaries")
    assert_contains(external_start, "spt_player_patrol")
    assert_not_contains(external_start, "spt_companion_retinue")
    assert_contains(external_order, "spt_player_mercenaries")
    assert_contains(external_order, "spt_player_patrol")
    assert_not_contains(external_order, "spt_companion_retinue")


if __name__ == "__main__":
    test_retinue_constants_slots_and_template_exist()
    test_capacity_uses_companion_stats_not_player_stats()
    test_capacity_formula_matches_first_pass_design()
    test_effective_party_helpers_keep_retinue_capacity_separate()
    test_party_size_audit_covers_recruitment_and_reward_flows()
    test_retinue_storage_transfer_and_treasury_helpers_exist()
    test_retinues_are_not_external_follower_parties()
    test_lifecycle_and_wages_are_hooked()
    test_autonomy_is_scaffolded_but_guarded()
    test_autonomous_recruiting_uses_preferences_budget_and_target()
    test_companion_identity_preferences_are_flavorful_not_locking()
    test_autonomous_recruiting_uses_location_culture_and_opportunity()
    test_desired_strength_orders_right_size_and_warn()
    test_autonomous_upgrading_uses_retinue_party_and_surplus_budget()
    test_post_battle_hiring_only_takes_unclaimed_rescued_troops()
    test_retinue_management_menu_is_safe_and_reachable()
    test_command_purse_pays_retinue_wages_first()
    test_retinue_supply_morale_and_training_are_separate_from_player_overcrowding()
    test_relationship_effects_drive_retinue_risk_and_reports()
    test_retinue_battle_bridge_uses_hidden_allied_parties_not_main_party_merge()
    test_departure_capture_and_failure_rules_are_explicit()
    test_retinue_exploit_and_edge_case_controls_are_hardened()
    test_retinue_integration_audit_surfaces_are_covered()
    print("test_companion_retinue_static: OK")
