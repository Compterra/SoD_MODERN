from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(text, needle, label):
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def assert_not_contains(text, needle, label):
    if needle in text:
        raise AssertionError(f"unexpected {label}: {needle}")


def assert_before(text, first, second, label):
    if first not in text:
        raise AssertionError(f"missing {label} first token: {first}")
    if second not in text:
        raise AssertionError(f"missing {label} second token: {second}")
    if text.index(first) >= text.index(second):
        raise AssertionError(f"wrong order for {label}: {first} should appear before {second}")


def main():
    constants = read("src/constants/module_constants.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_center_public_health.py")
    menus = read("src/menus/kingdom/center_public_health_report.py")
    fief = read("src/menus/0000_hardcoded_mb1011/fief_reports.py")
    fief_prosperity = read("src/menus/kingdom/fief_prosperity_report.py")
    triggers = read("src/triggers/_order_simple_triggers.txt")
    weekly = read("src/triggers/ST04_weekly/entry_0176_public_health.py")
    daily = read("src/triggers/ST03_daily/entry_0177_public_health.py")
    hourly_caravans = read("src/triggers/ST02_every_hour/entry_0049.py")
    dialogs = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_messenger_party_start.py")
    troops = read("compile/module_troops.py")
    town_dweller_info = read("src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_ask_info.py")
    town_dweller_situation = read("src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_ask_situation_public_health.py")
    village_elder_prompt = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_public_health.py")
    village_elder_answer = read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_public_health.py")
    mayor_prompt = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_mayor_public_health.py")
    mayor_answer = read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_public_health.py")
    seneschal_prompt = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_seneschal_public_health.py")
    seneschal_answer = read("src/dialogs/ZZ99_misc_dialogs/anyone_seneschal_public_health.py")
    caravan_health_prompt = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_merchant_caravan_world_health.py")
    caravan_health_answer = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_merchant_caravan_world_health_answer.py")
    goods_merchant_rumor = read("src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_trade_rumor.py")
    order_dialogs = read("src/dialogs/_order_dialogs.txt")
    trade_network = read("src/scripts/ZY_helper_scripts/sod_trade_network.py")
    player_recruits = read("src/scripts/ZD_centers/update_volunteer_troops_in_village.py")
    npc_recruits = read("src/scripts/ZD_centers/update_npc_volunteer_troops_in_village.py")
    town_mercs = read("src/scripts/ZD_centers/update_mercenary_units_of_towns.py")
    town_menu = read("src/menus/centers/castle/castle_castle.py")
    village_menu = read("src/menus/centers/village/recruit_volunteers.py")
    recon_notes = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    goods_market_report = read("src/menus/centers/common/center_goods_market_report.py")
    trade_goods_prices = read("src/scripts/ZB_economy_and_trade/update_trade_good_price_for_party.py")
    castle_support = read("src/scripts/ZY_helper_scripts/sod_castle_support_profile.py")
    design_doc = read("docs/settlements/CENTER_PUBLIC_HEALTH_DESIGN.md")

    for name in (
        "slot_center_health_sanitation",
        "slot_center_health_crowding",
        "slot_center_health_food_quality",
        "slot_center_health_healer_capacity",
        "slot_center_health_disease_risk",
        "slot_center_health_outbreak_type",
        "slot_center_health_outbreak_severity",
        "slot_center_health_quarantine",
        "slot_center_health_refugee_pressure",
        "slot_center_health_war_damage_pressure",
        "slot_center_health_trade_exposure",
        "slot_center_health_recent_aftermath",
        "slot_center_health_recent_exposure",
        "slot_center_health_last_player_exposure_day",
        "slot_center_health_resistance_memory",
        "slot_center_health_last_owner_response_day",
        "sod_outbreak_camp_fever",
        "sod_outbreak_flux",
        "sod_outbreak_pox",
        "sod_outbreak_famine_sickness",
        "sod_outbreak_siege_rot",
        "sod_outbreak_refugee_sickness",
        "sod_trade_route_sickness",
    ):
        assert_contains(constants, name, name)

    for script in (
        '"sod_center_public_health_compute_causes"',
        '"sod_center_public_health_update"',
        '"sod_center_public_health_process_outbreak"',
        '"sod_center_public_health_apply_player_visit_exposure"',
        '"sod_center_public_health_apply_intervention"',
        '"sod_center_public_health_brief_to_s0"',
        '"sod_center_public_health_describe_to_s0"',
        '"sod_center_public_health_try_spawn_relief_mission"',
        '"sod_center_public_health_process_relief_missions"',
        '"sod_center_public_health_try_owner_response"',
        '"sod_center_public_health_wound_castle_garrison"',
        '"sod_center_public_health_apply_social_pressure"',
        '"cf_sod_center_public_health_can_order_intervention"',
        '"sod_center_public_health_relief_institution_to_s0"',
        '"sod_center_public_health_apply_player_clergy_blessing"',
    ):
        assert_contains(helper, script, script)

    for token in (
        "script_sod_get_center_food_profile",
        "script_sod_get_center_population_capacity_profile",
        "sod_center_modifier_disease_resistance_pct",
        "slot_center_has_hospital",
        "slot_center_has_ambulatory",
        "slot_center_has_canalization",
        "slot_center_has_water_supply",
        "slot_center_has_temple",
        "slot_center_has_monastery",
        "slot_faction_slaver_market_heat",
        "slot_faction_jotnar_hearth_pressure",
        "slot_faction_elephant_guard_slaver_alarm",
        "slot_faction_black_khergit_pressure",
        "slot_faction_boar_frontier_pressure",
        "slot_faction_serpent_route_pressure",
        "slot_faction_black_army_contract_heat",
    ):
        assert_contains(helper, token, token)

    assert_contains(helper, "str_store_string_reg, s68, s0", "outbreak warning stable string copy")
    assert_contains(helper, "Public health warning: {s1} is suffering {s68}", "outbreak warning high string register")
    assert_not_contains(helper, "Public health warning: {s1} is suffering {s0}", "outbreak warning volatile s0")
    assert_contains(helper, "script_change_center_health", "bounded health mutator")
    assert_contains(helper, "script_sod_change_center_faith_support", "faith support relief")
    blessing_start = helper.index('("sod_center_public_health_apply_player_clergy_blessing"')
    blessing_end = helper.index('("sod_center_public_health_relief_institution_to_s0"', blessing_start)
    blessing_script = helper[blessing_start:blessing_end]
    assert_contains(blessing_script, "try_for_range, \":center_no\", centers_begin, centers_end", "clergy blessing all centers")
    assert_contains(blessing_script, 'script_sod_change_center_faith_support", ":center_no", "$g_sod_faith", ":faith_delta"', "clergy blessing player faith support")
    assert_not_contains(blessing_script, "display_message", "hidden clergy blessing public message")
    assert_contains(helper, "pt_messenger_party", "relief messenger party")
    relief_start = helper.index('("sod_center_public_health_try_spawn_relief_mission"')
    relief_end = helper.index('("sod_center_public_health_process_relief_missions"', relief_start)
    relief_script = helper[relief_start:relief_end]
    assert_before(relief_script, '(gt, ":relief_party", 0)', '(party_is_active, ":relief_party")', "relief spawn active guard")
    assert_before(relief_script, '(party_is_active, ":relief_party")', '(party_set_faction, ":relief_party", ":origin_faction")', "relief spawn active guard before party setup")
    assert_contains(helper, "sod_messenger_role_public_health_relief", "relief messenger role")
    assert_contains(troops, '"sod_public_health_clergy"', "dedicated public health clergy troop")
    assert_contains(troops, '"Relief Cleric"', "public health clergy troop singular name")
    assert_contains(troops, "itm_robe", "public health clergy robe")
    assert_contains(troops, "itm_pilgrim_hood", "public health clergy hood")
    assert_contains(troops, "itm_staff", "public health clergy staff")
    assert_contains(troops, "itm_quarter_staff", "public health clergy quarter staff")
    assert_contains(troops, "knows_first_aid_2|knows_surgery_1|knows_wound_treatment_2", "public health clergy medical skills")
    assert_contains(relief_script, 'party_add_leader, ":relief_party", "trp_sod_public_health_clergy"', "relief party clergy leader")
    assert_contains(relief_script, 'party_add_members, ":relief_party", "trp_sod_public_health_clergy"', "relief party clergy stack")
    assert_contains(relief_script, 'slot_faction_tier_5_troop', "relief party culture elite escort")
    assert_contains(relief_script, 'party_add_members, ":relief_party", ":escort_troop", ":escort_count"', "relief party small escort")
    assert_not_contains(relief_script, 'party_add_members, ":relief_party", ":messenger_troop"', "relief party messenger troop stack")
    assert_contains(helper, "script_sod_companion_dispatch_player_action", "companion hooks")
    assert_contains(helper, "script_change_player_party_morale", "player visit morale consequence")
    assert_contains(helper, "slot_center_health_last_player_exposure_day", "player visit exposure gate")
    assert_contains(helper, "slot_center_health_resistance_memory", "survivor resistance memory")
    assert_contains(helper, "survivor resistance", "survivor resistance report text")
    for token in (
        "script_sod_center_public_health_try_owner_response",
        "slot_center_health_last_owner_response_day",
        "slot_town_lord",
        "kingdom_heroes_begin",
        "slot_center_health_recent_exposure",
        "script_change_center_health",
        "script_sod_report_record_event",
        "sod_report_category_health",
        "sod_report_reason_relief",
    ):
        assert_contains(helper, token, f"lord owner public health response {token}")
    assert_contains(town_menu, "script_sod_center_public_health_apply_player_visit_exposure", "town/castle visit public health exposure")
    assert_contains(village_menu, "script_sod_center_public_health_apply_player_visit_exposure", "village visit public health exposure")

    assert_contains(weekly, "script_sod_center_public_health_update_all_centers", "weekly public health update")
    assert_contains(daily, "script_sod_center_public_health_process_all_outbreaks", "daily outbreak processing")
    assert_contains(daily, "script_sod_center_public_health_process_relief_missions", "daily relief processing")
    assert_contains(triggers, "ST04_weekly/entry_0176_public_health.py", "weekly manifest entry")
    assert_contains(triggers, "ST03_daily/entry_0177_public_health.py", "daily manifest entry")

    assert_contains(fief, "mnu_center_public_health_report", "fief report link")
    assert_contains(menus, '"{s98}"', "public health report high display register")
    assert_contains(menus, "(str_clear, s98)", "public health report clear display register")
    assert_contains(menus, "str_store_string_reg, s97, s98", "public health report copy-before-append")
    assert_not_contains(menus, '"{s9}"', "public health report old display register")
    assert_not_contains(menus, "@{s8}^^", "public health report old row append")
    assert_contains(fief_prosperity, "script_sod_center_public_health_brief_to_s0", "prosperity report public health brief")
    assert_contains(town_dweller_info, "script_sod_center_public_health_brief_to_s0", "town dweller public health brief")
    assert_contains(recon_notes, "script_sod_store_center_recon_brief_to_s68", "recon notes compact field brief")
    recon_brief = read("src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py")
    assert_contains(recon_brief, "script_sod_center_public_health_compute_causes", "recon brief public health state")
    assert_contains(recon_brief, "An outbreak of {s74} is active.", "recon brief outbreak text")
    assert_not_contains(recon_brief, "Current outbreak:", "recon brief raw outbreak label")
    assert_not_contains(recon_brief, "Recommendation:", "recon brief raw recommendation label")
    assert_contains(goods_market_report, "script_sod_center_public_health_brief_to_s0", "goods market report public health brief")
    assert_contains(goods_market_report, "Public health: {s12}", "goods market report public health text")
    assert_contains(town_dweller_situation, "script_sod_center_public_health_recommendation_to_s0", "town dweller public health recommendation")
    assert_contains(town_dweller_situation, "slot_center_health_recent_aftermath", "town dweller aftermath line")
    assert_contains(village_elder_prompt, "slot_center_health_outbreak_type", "village elder public health prompt")
    assert_contains(village_elder_answer, "script_sod_center_public_health_recommendation_to_s0", "village elder public health answer")
    assert_contains(mayor_prompt, "mayor_public_health", "guild master public health prompt")
    assert_contains(mayor_answer, "script_sod_center_public_health_describe_to_s0", "guild master public health answer")
    assert_contains(seneschal_prompt, "seneschal_public_health", "seneschal public health prompt")
    assert_contains(seneschal_answer, "script_sod_center_public_health_describe_to_s0", "seneschal public health answer")
    assert_contains(caravan_health_prompt, "script_sod_trade_network_describe_caravan_sickness_to_s20", "caravan sickness road prompt")
    assert_contains(caravan_health_answer, "{s20}", "caravan sickness road answer")
    assert_contains(goods_merchant_rumor, "slot_center_health_quarantine", "merchant quarantine rumor")
    assert_contains(goods_merchant_rumor, "slot_center_health_recent_aftermath", "merchant aftermath rumor")
    assert_contains(order_dialogs, "anyone_town_dweller_ask_situation_public_health.py", "town dweller public health order")
    assert_contains(order_dialogs, "anyone_plyr_village_elder_public_health.py", "village elder public health order")
    assert_contains(order_dialogs, "anyone_plyr_mayor_public_health.py", "guild master public health order")
    assert_contains(order_dialogs, "anyone_plyr_seneschal_public_health.py", "seneschal public health order")
    assert_contains(order_dialogs, "anyone_plyr_merchant_caravan_world_health.py", "caravan public health order")
    for token in (
        "Food {reg2}",
        "sanitation {reg3}",
        "crowding pressure {reg4}",
        "healer capacity {reg5}",
        "disease risk {reg6}",
        "Current outbreak",
        "Recommendation",
    ):
        assert_contains(helper, token, token)

    for intervention in (
        "sod_public_health_intervention_fund_healers",
        "sod_public_health_intervention_distribute_grain",
        "sod_public_health_intervention_clean_wells",
        "sod_public_health_intervention_repair_water",
        "sod_public_health_intervention_establish_quarantine",
        "sod_public_health_intervention_lift_quarantine",
        "sod_public_health_intervention_shelter_refugees",
        "sod_public_health_intervention_move_refugees",
        "sod_public_health_intervention_request_temple_aid",
        "sod_public_health_intervention_medicine_shipment",
        "sod_public_health_intervention_grain_shipment",
        "sod_public_health_intervention_burial_cleanup",
    ):
        assert_contains(menus, intervention, intervention)
    assert_contains(helper, "slot_center_health_last_intervention_day", "public health intervention day memory")
    assert_contains(helper, '(neq, ":last_intervention_day", ":today")', "public health one order per day gate")
    if menus.count('script_cf_sod_center_public_health_can_order_intervention", "$g_sod_public_health_report_target"') < 13:
        raise AssertionError("public health intervention menu should gate paid/lift actions and expose the already-ordered line")
    assert_contains(menus, "Orders are already in motion for the neediest fief today.", "public health daily order feedback")
    for token in (
        "quarantine in {s1} slows exposure",
        "lifting quarantine in {s1} while disease risk",
        "slot_center_health_recent_exposure",
        "slot_center_health_refugee_pressure",
        "script_sod_center_apply_tariffs_delta",
        "sod_companion_action_dirty_profit",
        "sod_companion_action_strict_discipline",
    ):
        assert_contains(helper, token, f"quarantine intervention tradeoff {token}")

    assert_contains(dialogs, "public_health_relief_talk", "relief party dialogue")
    assert_contains(dialogs, "slot_party_sod_public_health_destination", "relief destination dialogue")
    assert_contains(dialogs, "slot_party_sod_public_health_health_payload", "player supply payload")
    assert_contains(dialogs, "script_sod_center_public_health_relief_institution_to_s0", "relief party institution dialogue")
    assert_contains(dialogs, "slot_party_sod_public_health_origin_faith", "relief party origin faith dialogue gate")
    assert_contains(dialogs, '(eq, ":origin_faith", "$g_sod_faith")', "same faith clergy blessing gate")
    assert_contains(dialogs, "$g_sod_public_health_last_clergy_blessing_day", "weekly clergy blessing cooldown")
    assert_contains(dialogs, 'script_sod_player_charge_gold", 700', "clergy blessing alms cost")
    assert_contains(dialogs, 'script_sod_center_public_health_apply_player_clergy_blessing", 2', "clergy blessing hidden faith support")
    assert_contains(dialogs, '(neq, ":origin_faith", "$g_sod_faith")', "relief party attack only for rival faith")
    assert_contains(dialogs, 'script_change_badboy_rating", 6', "relief party attack badboy penalty")
    assert_contains(dialogs, "sod_companion_action_abuse_village", "relief party attack companion consequence")
    assert_contains(dialogs, "Word spreads that you attacked a clergy relief party", "relief party attack reputation message")
    for token in (
        "slot_center_has_hospital",
        "slot_center_has_ambulatory",
        "slot_center_has_monastery",
        "slot_center_has_temple",
        "slot_center_has_chapel",
        "slot_center_has_shrine",
        "val_add, \":relief_strength\"",
        "val_add, \":faith_payload\"",
        "healer-clergy houses",
        "slot_center_sod_security_cache_unrest_pressure",
        "slot_center_health_refugee_pressure",
        "slot_center_health_recent_exposure",
        "unrest cools",
    ):
        assert_contains(helper, token, f"relief institution payload token {token}")
    for token in (
        "slot_center_health_outbreak_type",
        "slot_center_health_outbreak_severity",
        "slot_center_health_disease_risk",
        "slot_center_health_quarantine",
        "slot_center_health_recent_exposure",
        "sod_trade_route_sickness",
        "script_change_center_health",
        "sod_trade_network_describe_caravan_sickness_to_s20",
        "slot_party_sod_trade_origin",
        "slot_party_sod_trade_destination",
    ):
        assert_contains(trade_network, token, f"trade network public health token {token}")
    assert_contains(helper, "script_sod_center_apply_tariffs_delta", "outbreak tariff loss")
    assert_contains(helper, "slot_center_mercenary_troop_amount", "town outbreak mercenary loss")
    assert_contains(helper, "slot_center_volunteer_troop_amount", "village outbreak recruit loss")
    assert_contains(helper, "slot_center_npc_volunteer_troop_amount", "village npc outbreak recruit loss")
    assert_contains(helper, "script_sod_center_public_health_wound_castle_garrison", "castle outbreak garrison sickness")
    assert_contains(helper, "party_wound_members", "castle outbreak wounds garrison regulars")
    assert_contains(helper, "sickness in {s1} sends {reg1} garrison soldiers", "castle outbreak garrison message")
    for token in (
        "script_sod_center_public_health_apply_social_pressure",
        "slot_center_sod_security_cache_unrest_pressure",
        "slot_center_health_refugee_pressure",
        "script_sod_center_apply_population_delta",
        "script_change_player_relation_with_center",
        "fear and flight spread",
    ):
        assert_contains(helper, token, f"public health social pressure token {token}")
    for token in (
        "script_sod_center_public_health_compute_causes",
        "slot_center_health_outbreak_type",
        "slot_center_health_outbreak_severity",
        "slot_center_health_quarantine",
        "public_health_disease_risk",
        "readiness_sickness_drag",
        "military_sickness_drag",
        "support_sickness_drag",
    ):
        assert_contains(castle_support, token, f"castle support public health token {token}")
    for label, raw in (
        ("player village recruits", player_recruits),
        ("npc village recruits", npc_recruits),
        ("town mercenaries", town_mercs),
        ("trade goods restock", trade_goods_prices),
    ):
        assert_contains(raw, "script_sod_center_public_health_compute_causes", f"{label} public health cause check")
        assert_contains(raw, "slot_center_health_outbreak_type", f"{label} outbreak check")
        assert_contains(raw, "slot_center_health_quarantine", f"{label} quarantine check")
        assert_contains(raw, "slot_center_health_recent_aftermath", f"{label} aftermath check")
    assert_contains(hourly_caravans, "script_sod_trade_network_process_caravan_arrival_tick", "sick route trigger delegate")
    assert_contains(trade_network, "sod_trade_route_sickness", "sick route departure friction")
    assert_not_contains(helper, "store_random_in_range, \":roll\", 0, 100),\n       (lt, \":roll\", 5)", "flat outbreak roll")
    assert_not_contains(design_doc, "- [ ]", "unchecked public health design checklist item")

    print("public health static checks passed")


def test_public_health_static() -> None:
    main()


if __name__ == "__main__":
    main()
