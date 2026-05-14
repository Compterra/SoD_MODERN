from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"Missing expected text: {needle}"


def test_camp_jobs_have_constants_and_state_contracts():
    constants = read("src/constants/module_constants.py")
    for name in [
        "sod_camp_job_none",
        "sod_camp_job_scout_route",
        "sod_camp_job_forage_hunt",
        "sod_camp_job_repair_gear",
        "sod_camp_job_ration_stores",
        "sod_camp_job_tend_mounts",
        "sod_camp_job_result_cancelled",
        "sod_camp_passive_job_scout_route",
        "sod_camp_passive_job_count_stores",
        "sod_camp_passive_job_hold_rites",
        "sod_camp_passive_job_study_gates",
        "sod_camp_pressure_scout_route",
        "sod_camp_pressure_prepare_siege",
        "sod_repair_service_ranged",
        "sod_repair_service_melee",
        "sod_repair_service_heavy_armor",
        "sod_repair_service_light_clothes",
        "slot_troop_sod_camp_job",
        "slot_troop_sod_camp_job_pressure",
        "slot_troop_sod_camp_job_pressure_max",
        "slot_troop_sod_camp_job_last_tick_hour",
        "slot_troop_sod_camp_job_last_result",
    ]:
        assert_contains(constants, name)

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    for global_name in [
        "$g_sod_camp_job_active",
        "$g_sod_camp_job_type",
        "$g_sod_camp_job_leader",
        "$g_sod_camp_job_started_hour",
        "$g_sod_camp_job_finish_hour",
        "$g_sod_camp_job_last_result",
    ]:
        assert_contains(scripts, global_name)


def test_passive_camp_jobs_assign_one_job_per_companion():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_initialize_companion_jobs"')
    expected_assignments = [
        ('"trp_npc1"', "sod_camp_passive_job_scout_route", "sod_camp_pressure_scout_route"),
        ('"trp_npc2"', "sod_camp_passive_job_count_stores", "sod_camp_pressure_count_stores"),
        ('"trp_npc3"', "sod_camp_passive_job_hold_rites", "sod_camp_pressure_hold_rites"),
        ('"trp_npc4"', "sod_camp_passive_job_enforce_order", "sod_camp_pressure_enforce_order"),
        ('"trp_npc5"', "sod_camp_passive_job_tend_mounts", "sod_camp_pressure_tend_mounts"),
        ('"trp_npc6"', "sod_camp_passive_job_patrol_pickets", "sod_camp_pressure_patrol_pickets"),
        ('"trp_npc7"', "sod_camp_passive_job_hunt_game", "sod_camp_pressure_hunt_game"),
        ('"trp_npc8"', "sod_camp_passive_job_repair_heavy_armor", "sod_camp_pressure_repair_heavy_armor"),
        ('"trp_npc9"', "sod_camp_passive_job_restore_discipline", "sod_camp_pressure_restore_discipline"),
        ('"trp_npc10"', "sod_camp_passive_job_repair_ranged", "sod_camp_pressure_repair_ranged"),
        ('"trp_npc11"', "sod_camp_passive_job_mend_clothes", "sod_camp_pressure_mend_clothes"),
        ('"trp_npc12"', "sod_camp_passive_job_treat_wounded", "sod_camp_pressure_treat_wounded"),
        ('"trp_npc13"', "sod_camp_passive_job_probe_openings", "sod_camp_pressure_probe_openings"),
        ('"trp_npc14"', "sod_camp_passive_job_repair_melee", "sod_camp_pressure_repair_melee"),
        ('"trp_npc15"', "sod_camp_passive_job_prepare_siege", "sod_camp_pressure_prepare_siege"),
        ('"trp_npc16"', "sod_camp_passive_job_study_gates", "sod_camp_pressure_study_gates"),
    ]
    for companion, job, pressure in expected_assignments:
        assert_contains(scripts, f'(call_script, "script_sod_camp_passive_job_set", {companion}, {job}, {pressure})')

    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    assert_contains(game_start, '(call_script, "script_sod_camp_initialize_companion_jobs")')


def test_passive_camp_jobs_use_manpower_pressure_and_hourly_camped_updates():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_calculate_manpower"')
    assert_contains(scripts, '(neg|troop_is_hero, ":stack_troop")')
    assert_contains(scripts, '(party_stack_get_num_wounded, ":num_wounded", "p_main_party", ":stack_no")')
    assert_contains(scripts, '(party_get_morale, ":party_morale", "p_main_party")')
    assert_contains(scripts, '"sod_camp_passive_jobs_update"')
    assert_contains(scripts, '(eq, "$g_camp_mode", 1)')
    assert_contains(scripts, '(eq, "$g_player_icon_state", pis_camping)')
    assert_contains(scripts, '(eq, "$g_player_is_captive", 0)')
    assert_contains(scripts, '(store_mul, ":pressure_gain", ":elapsed_hours", 10)')
    assert_contains(scripts, '(val_add, ":pressure_gain", ":manpower_bonus")')
    assert_contains(scripts, '(call_script, "script_sod_camp_passive_job_conditions_to_reg", ":companion", ":job_type")')
    assert_contains(scripts, '(call_script, "script_sod_camp_passive_job_resolve_tick", ":companion", ":job_type")')
    assert_contains(scripts, '(val_sub, ":pressure", ":pressure_max")')
    assert_contains(scripts, '(store_mul, ":pressure_cap", ":pressure_max", 2)')
    assert_contains(scripts, '(val_clamp, ":pressure", 0, ":pressure_cap")')

    trigger = read("src/triggers/ST02_every_hour/entry_0172.py")
    assert_contains(trigger, '(call_script, "script_sod_camp_passive_jobs_update")')


def test_passive_camp_pressure_never_advances_from_menu_clicks():
    menu = read("src/menus/camp/camp_jobs.py")
    assert 'script_sod_camp_passive_jobs_update' not in menu
    assert_contains(menu, '(rest_for_hours_interactive, 6, 5, 1)')


def test_passive_camp_job_conditions_gate_resource_and_context_jobs():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_passive_job_conditions_to_reg"')
    assert_contains(scripts, '"sod_camp_player_inventory_has_free_slot"')
    assert_contains(scripts, '"sod_camp_player_has_tools"')
    assert_contains(scripts, '"sod_camp_find_repairable_equipment"')
    assert_contains(scripts, '"sod_camp_has_lame_horse"')
    assert_contains(scripts, '"sod_camp_player_has_nearby_hostile_center"')
    assert_contains(scripts, '(eq, ":job_type", sod_camp_passive_job_hunt_game)')
    assert_contains(scripts, '(eq, ":job_type", sod_camp_passive_job_tend_mounts)')
    assert_contains(scripts, '(eq, ":job_type", sod_camp_passive_job_prepare_siege)')
    assert_contains(scripts, '(eq, ":job_type", sod_camp_passive_job_study_gates)')
    assert_contains(scripts, '(troop_get_inventory_slot, ":item_no", "trp_player", ":slot_no")')
    assert_contains(scripts, '(eq, ":item_no", "itm_tools")')
    assert_contains(scripts, '(store_distance_to_party_from_party, ":distance", "p_main_party", ":center_no")')


def test_hold_rites_only_increase_chosen_global_faith_without_capping_to_100():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '(eq, ":job_type", sod_camp_passive_job_hold_rites)')
    assert_contains(scripts, '(gt, "$g_sod_faith", 0)')
    assert_contains(scripts, '(val_add, "$g_sod_global_faith", 1)')
    assert_contains(scripts, '(val_clamp, "$g_sod_global_faith", -2000, 2001)')
    assert '(val_min, "$g_sod_global_faith", 100)' not in scripts


def test_camp_repairs_consume_tools_instead_of_using_merchant_gold_repairs():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_repair_one_equipment_with_tools"')
    assert_contains(scripts, '(troop_remove_item, "trp_player", "itm_tools")')
    assert_contains(scripts, '(troop_set_inventory_slot_modifier, ":selected_troop", ":selected_slot", imod_plain)')
    assert_contains(scripts, '(call_script, "script_sod_camp_repair_one_equipment_with_tools", sod_repair_service_heavy_armor)')
    assert_contains(scripts, '(call_script, "script_sod_camp_repair_one_equipment_with_tools", sod_repair_service_light_clothes)')
    assert_contains(scripts, '(call_script, "script_sod_camp_repair_one_equipment_with_tools", sod_repair_service_ranged)')
    assert_contains(scripts, '(call_script, "script_sod_camp_repair_one_equipment_with_tools", sod_repair_service_melee)')


def test_camp_repair_jobs_use_split_repair_service_categories():
    repair_filter = read("src/scripts/ZB_economy_and_trade/sod_item_can_be_repaired_by_service.py")
    assert_contains(repair_filter, '(eq, ":service_type", sod_repair_service_ranged)')
    assert_contains(repair_filter, 'itp_type_bow')
    assert_contains(repair_filter, 'itp_type_crossbow')
    assert_contains(repair_filter, '(eq, ":service_type", sod_repair_service_melee)')
    assert_contains(repair_filter, 'itp_type_one_handed_wpn')
    assert_contains(repair_filter, 'itp_type_two_handed_wpn')
    assert_contains(repair_filter, '(eq, ":service_type", sod_repair_service_heavy_armor)')
    assert_contains(repair_filter, 'itp_type_body_armor')
    assert_contains(repair_filter, '(eq, ":service_type", sod_repair_service_light_clothes)')
    assert_contains(repair_filter, 'itp_type_foot_armor')
    assert_contains(repair_filter, "script_sod_auto_loot_item_is_protected")

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '(call_script, "script_sod_camp_find_repairable_equipment", sod_repair_service_heavy_armor)')
    assert_contains(scripts, '(call_script, "script_sod_camp_find_repairable_equipment", sod_repair_service_light_clothes)')
    assert_contains(scripts, '(call_script, "script_sod_camp_find_repairable_equipment", sod_repair_service_ranged)')
    assert_contains(scripts, '(call_script, "script_sod_camp_find_repairable_equipment", sod_repair_service_melee)')


def test_camp_jobs_menu_reports_passive_roles_manpower_progress_and_blockers():
    menu = read("src/menus/camp/camp_jobs.py")
    assert_contains(menu, '(call_script, "script_sod_camp_job_describe_to_s1")')
    assert_contains(menu, '"Rest six hours and let passive camp roles work."')
    assert_contains(menu, '"Direct order: scout the route for six hours."')

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_passive_jobs_describe_to_s2"')
    assert_contains(scripts, '"sod_camp_passive_job_name_to_s4"')
    assert_contains(scripts, '"sod_camp_passive_job_progress_to_s5"')
    assert_contains(scripts, '"sod_camp_passive_job_condition_text_to_s6"')
    assert_contains(scripts, "Passive camp roles")
    assert_contains(scripts, "Passive companion roles advance automatically while the party is camped")
    assert_contains(scripts, "Manpower: {reg30} fit regulars")
    assert_contains(scripts, "just started")
    assert_contains(scripts, "underway")
    assert_contains(scripts, "close to completion")
    assert_contains(scripts, "ready to produce")
    assert_contains(scripts, "needs free inventory space")
    assert_contains(scripts, "needs tools")
    assert_contains(scripts, "no damaged matching gear")
    assert_contains(scripts, "no lame horses")
    assert_contains(scripts, "no wounded troops")
    assert_contains(scripts, "needs nearby hostile center")
    assert_contains(scripts, '(str_store_string, s1, "@{s1}^^{s2}")')


def test_companions_can_reveal_camp_jobs_through_member_dialogue():
    order = read("src/dialogs/_order_dialogs.txt")
    assert_contains(order, "ZE01_companions_and_named_npcs/anyone_plyr_companion_camp_job_reveal.py")
    assert_contains(order, "ZE01_companions_and_named_npcs/anyone_companion_camp_job_reveal.py")
    assert order.index("ZE01_companions_and_named_npcs/anyone_companion_depth_klethi.py") < order.index("ZE01_companions_and_named_npcs/anyone_plyr_companion_camp_job_reveal.py")
    assert order.index("ZE01_companions_and_named_npcs/anyone_companion_camp_job_reveal.py") < order.index("ZZ99_misc_dialogs/anyone_plyr_member_talk.py")

    player_line = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_camp_job_reveal.py")
    response_line = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_camp_job_reveal.py")
    assert_contains(player_line, '"What work do you take up when we make camp?"')
    assert_contains(player_line, '"companion_camp_job_reveal"')
    assert_contains(response_line, '(call_script, "script_sod_camp_passive_job_dialogue_to_s0", "$g_talk_troop")')
    assert_contains(response_line, '"{s0}"')

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_passive_job_dialogue_to_s0"')
    assert_contains(scripts, '(call_script, "script_sod_camp_passive_job_name_to_s4", ":job_type")')
    assert_contains(scripts, '(call_script, "script_sod_camp_passive_job_progress_to_s5", ":companion")')
    assert_contains(scripts, '(call_script, "script_sod_camp_passive_job_condition_text_to_s6", ":companion", ":job_type")')
    for companion in range(1, 17):
        assert_contains(scripts, f'(eq, ":companion", "trp_npc{companion}")')
    for phrase in [
        "I take Scout Route",
        "I count the stores",
        "I hold rites",
        "I enforce order",
        "I tend the mounts",
        "I patrol the pickets",
        "I hunt wild game",
        "I see to heavy armor",
        "I restore discipline",
        "I repair ranged kit",
        "I mend light clothes",
        "I tend the wounded",
        "I probe for openings",
        "I repair melee weapons",
        "I prepare siege works",
        "I study the gates",
    ]:
        assert_contains(scripts, phrase)


def test_camp_role_readiness_is_consumed_by_sneak_siege_and_battle_hooks():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '"sod_camp_player_has_wounded_troops"')
    assert_contains(scripts, '"sod_camp_apply_klethi_gate_study_to_sneak_chance"')
    assert_contains(scripts, '"sod_camp_apply_artimenner_siege_preparation_to_hours"')
    assert_contains(scripts, '"sod_camp_mark_interrupted_battle_readiness"')
    assert_contains(scripts, '(assign, "$g_sod_camp_gate_study_progress", 0)')
    assert_contains(scripts, '(assign, "$g_sod_camp_siege_works_progress", 0)')
    assert_contains(scripts, '(assign, "$g_sod_camp_interrupted_battle_readiness", "$g_sod_camp_firentis_readiness")')

    approach = read("src/menus/centers/common/approach_gates.py")
    assert_contains(approach, '(call_script, "script_sod_camp_apply_klethi_gate_study_to_sneak_chance", ":get_caught_chance")')
    assert_contains(approach, '(assign, ":get_caught_chance", reg0)')

    ladders = read("src/menus/centers/common/build_ladders_cont.py")
    assert_contains(ladders, '(call_script, "script_sod_camp_apply_artimenner_siege_preparation_to_hours", ":hours_takes", 1)')
    tower = read("src/menus/centers/castle/build_siege_tower_cont.py")
    assert_contains(tower, '(call_script, "script_sod_camp_apply_artimenner_siege_preparation_to_hours", ":hours_takes", 2)')

    encounter = read("src/menus/0000_hardcoded_mb1011/simple_encounter.py")
    assert_contains(encounter, '(call_script, "script_sod_camp_mark_interrupted_battle_readiness")')

    morale = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    assert_contains(morale, '$g_sod_camp_interrupted_battle_readiness')
    assert_contains(morale, '(val_add, "$g_sod_battle_ally_lord_morale", ":camp_readiness_bonus")')
    assert_contains(morale, '(assign, "$g_sod_camp_interrupted_battle_readiness", 0)')


def test_camp_action_links_to_camp_jobs_menu_without_hardcoded_reorder():
    camp_action = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    assert_contains(camp_action, '"Manage camp jobs and expedition roles."')
    assert_contains(camp_action, '(jump_to_menu, "mnu_camp_jobs")')

    order = read("src/menus/_order_game_menus.txt")
    assert_contains(order, "camp/camp_jobs.py")
    assert order.index("camp/companion_retinue_report.py") < order.index("camp/camp_jobs.py")
    assert order.index("camp/camp_jobs.py") < order.index("camp/borcha_road_keeps_own.py")


def test_camp_jobs_start_only_while_camped_and_prevent_overlap():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, '(eq, "$g_sod_camp_job_active", 0)')
    assert_contains(scripts, '(eq, "$g_camp_mode", 1)')
    assert_contains(scripts, '(eq, "$g_player_icon_state", pis_camping)')
    assert_contains(scripts, '(is_between, ":job_type", sod_camp_job_scout_route, sod_camp_job_end)')

    menu = read("src/menus/camp/camp_jobs.py")
    assert_contains(menu, '(assign, "$g_camp_mode", 1)')
    assert_contains(menu, '(assign, "$g_player_icon_state", pis_camping)')
    assert_contains(menu, '(rest_for_hours_interactive, 6, 5, 1)')


def test_camp_jobs_resolve_only_while_camping_hourly():
    trigger = read("src/triggers/ST02_every_hour/entry_0172.py")
    assert_contains(trigger, '(eq, "$g_sod_camp_job_active", 1)')
    assert_contains(trigger, '(eq, "$g_camp_mode", 1)')
    assert_contains(trigger, '(eq, "$g_player_icon_state", pis_camping)')
    assert_contains(trigger, '(ge, ":cur_hours", "$g_sod_camp_job_finish_hour")')
    assert_contains(trigger, '(call_script, "script_sod_camp_job_resolve")')

    order = read("src/triggers/_order_simple_triggers.txt")
    assert_contains(order, "ST02_every_hour/entry_0172.py")


def test_first_three_camp_jobs_have_mechanical_effects_and_safety():
    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, "sod_camp_job_scout_route")
    assert_contains(scripts, "$g_sod_camp_scout_readiness_until_hour")
    assert_contains(scripts, "$g_sod_camp_scout_readiness")
    assert_contains(scripts, "sod_camp_job_forage_hunt")
    assert_contains(scripts, '(troop_add_items, "trp_player", "itm_smoked_fish", ":yield")')
    assert_contains(scripts, '(val_clamp, ":yield", 1, 9)')
    assert_contains(scripts, "sod_camp_job_repair_gear")
    assert_contains(scripts, '(call_script, "script_sod_repair_player_party_equipment", sod_repair_service_all)')
    assert_contains(read("src/scripts/ZB_economy_and_trade/sod_item_can_be_repaired_by_service.py"), "script_sod_auto_loot_item_is_protected")


def test_borcha_scout_route_temporarily_boosts_camped_sight_range():
    menu = read("src/menus/camp/camp_jobs.py")
    assert_contains(menu, '(main_party_has_troop, "trp_npc1")')
    assert_contains(menu, '(call_script, "script_sod_camp_job_start", sod_camp_job_scout_route, 6, "trp_npc1")')
    assert_contains(menu, '"Direct order: scout the route. Requires Borcha."')

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, "$g_sod_camp_borcha_sight_bonus")
    assert_contains(scripts, "$g_sod_camp_borcha_sight_until_hour")

    skill_callback = read("src/scripts/ZA_hardcoded_game_scripts/game_get_skill_modifier_for_troop.py")
    assert_contains(skill_callback, '(eq, ":skill_no", "skl_spotting")')
    assert_contains(skill_callback, '(eq, "$g_camp_mode", 1)')
    assert_contains(skill_callback, '(eq, "$g_player_icon_state", pis_camping)')
    assert_contains(skill_callback, '(main_party_has_troop, "trp_npc1")')
    assert_contains(skill_callback, '(val_add, ":modifier_value", "$g_sod_camp_borcha_sight_bonus")')


def test_marnid_ration_stores_lowers_camped_food_consumption():
    menu = read("src/menus/camp/camp_jobs.py")
    assert_contains(menu, '(main_party_has_troop, "trp_npc2")')
    assert_contains(menu, '(call_script, "script_sod_camp_job_start", sod_camp_job_ration_stores, 6, "trp_npc2")')
    assert_contains(menu, '"Direct order: count and sort stores. Requires Marnid."')

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, "$g_sod_camp_marnid_food_consumption_pct")
    assert_contains(scripts, "$g_sod_camp_marnid_food_until_hour")
    assert_contains(scripts, "Food consumption while camped is reduced by 25 percent")

    food_trigger = read("src/triggers/ST03_daily/entry_0054.py")
    assert_contains(food_trigger, '(eq, "$g_camp_mode", 1)')
    assert_contains(food_trigger, '(eq, "$g_player_icon_state", pis_camping)')
    assert_contains(food_trigger, '(main_party_has_troop, "trp_npc2")')
    assert_contains(food_trigger, '(val_mul, ":consumption_amount", "$g_sod_camp_marnid_food_consumption_pct")')
    assert_contains(food_trigger, '(val_div, ":consumption_amount", 100)')


def test_baheshtur_tend_mounts_unlames_random_horse():
    menu = read("src/menus/camp/camp_jobs.py")
    assert_contains(menu, '(main_party_has_troop, "trp_npc5")')
    assert_contains(menu, '(call_script, "script_sod_camp_job_start", sod_camp_job_tend_mounts, 6, "trp_npc5")')
    assert_contains(menu, '"Direct order: tend the mounts. Requires Baheshtur."')

    scripts = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert_contains(scripts, "script_sod_camp_job_unlame_random_horse")
    assert_contains(scripts, "itp_type_horse")
    assert_contains(scripts, "imod_lame")
    assert_contains(scripts, "(troop_set_inventory_slot_modifier, \":selected_troop\", \":selected_slot\", imod_plain)")
