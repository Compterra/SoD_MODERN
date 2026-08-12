from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def script_block(raw: str, script_name: str) -> str:
    start = raw.index(f'(\"{script_name}\",')
    end = raw.index("\n ]),", start) + len("\n ]),")
    return raw[start:end]


def test_campaign_dispatch_has_bounded_persistent_layout() -> None:
    constants = read("src/constants/module_constants.py")
    dispatch = read("src/scripts/ZY_helper_scripts/sod_campaign_dispatch.py")

    for token in [
        "slot_troop_sod_report_pending_base = 400",
        "slot_troop_sod_report_archive_base = 504",
        "slot_troop_sod_report_archive_head_base = 824",
        "slot_troop_sod_report_category_unread_base = 832",
        "slot_troop_sod_report_slots_end = 840",
        "sod_report_archive_entries = 4",
        "sod_report_pending_stride = 13",
        "sod_report_archive_category_stride = 40",
        "sod_report_reason_realm_treaty",
        "sod_report_reason_realm_war",
        "sod_report_reason_slaver_market",
    ]:
        assert_contains(constants, token)

    for token in [
        '"sod_report_record_event"',
        '"sod_report_flush_pending"',
        '"sod_report_describe_overview_to_s68"',
        '"sod_report_describe_category_to_s68"',
        '"sod_report_record_center_event"',
        '"sod_report_record_contract_event"',
        '"sod_report_record_faction_event"',
        "sod_report_archive_entries",
        "slot_troop_sod_report_pending_base",
        "slot_troop_sod_report_archive_base",
    ]:
        assert_contains(dispatch, token)

    assert_not_contains(dispatch, "trp_temp_array")
    assert_contains(dispatch, 'assign, ":source_kind", sod_report_subject_none')
    assert_contains(dispatch, 'assign, ":destination_kind", sod_report_subject_none')
    assert_contains(dispatch, 'assign, ":target_kind", sod_report_subject_none')


def test_campaign_dispatch_is_reachable_and_flushed_on_campaign_cadence() -> None:
    reports = read("src/menus/0000_hardcoded_mb1011/reports.py")
    menu_order = read("src/menus/_order_game_menus.txt")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    daily = read("src/triggers/ST03_daily/campaign_dispatch_daily_flush.py")
    weekly = read("src/triggers/ST04_weekly/campaign_dispatch_weekly_flush.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    options = read("src/menus/0000_hardcoded_mb1011/game_options_3.py")

    assert_contains(reports, "view_campaign_dispatch")
    assert_contains(reports, "mnu_campaign_dispatch")
    assert_contains(menu_order, "reports/campaign_dispatch.py")
    assert_contains(trigger_order, "ST03_daily/campaign_dispatch_daily_flush.py")
    assert_contains(trigger_order, "ST04_weekly/campaign_dispatch_weekly_flush.py")
    assert_contains(daily, "script_sod_report_flush_pending")
    assert_contains(weekly, "script_sod_report_flush_pending")
    assert_contains(game_start, "$g_sod_report_delivery_mode")
    assert_contains(options, "game_options_cycle_campaign_dispatch")
    dispatch_menu = read("src/menus/reports/campaign_dispatch.py")
    for token in [
        "mnu_center_public_health_report",
        "mnu_trade_network_report",
        "mnu_black_khergit_horde_report",
        "mnu_prisoner_economy_report",
        "mnu_mercenary_market_report",
        "mnu_sod_diplomacy_report",
        "mnu_mercenary_world_activity_report",
    ]:
        assert_contains(dispatch_menu, token)


def test_routine_report_emitters_use_dispatch_not_direct_map_lines() -> None:
    migration = read("src/scripts/ZY_helper_scripts/sod_center_weekly_migration.py")
    desperation = read("src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py")
    health = read("src/scripts/ZY_helper_scripts/sod_center_public_health.py")
    tax = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    prisoners = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    contracts = read("src/scripts/ZY_helper_scripts/sod_merc_market_deploy_ai_contract.py")
    slavers = read("src/scripts/ZY_helper_scripts/sod_slavers_black_market.py")
    incidents = read("src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py")
    horde = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    diplomacy = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")

    assert_not_contains(migration, "display_message")
    assert_not_contains(desperation, "display_message")
    assert_contains(migration, "script_sod_report_record_center_event")
    assert_contains(desperation, "script_sod_report_record_center_event")
    assert_contains(health, "sod_report_category_health")
    assert_contains(health, "sod_report_reason_outbreak")
    assert_contains(health, "sod_report_reason_relief")
    assert_contains(health, "Public health: quarantine in")
    assert_contains(tax, "sod_report_reason_tax_departure")
    assert_contains(tax, "sod_report_reason_tax_delivery")
    assert_contains(read("src/scripts/ZY_helper_scripts/sod_trade_network.py"), "sod_report_reason_trade")
    assert_contains(prisoners, "sod_report_reason_prisoner_arrival")
    assert_contains(contracts, "script_sod_report_record_contract_event")
    assert_contains(slavers, "sod_report_reason_slaver_market")
    assert_not_contains(slavers, "Slaver black market transport(s) reached their destination")
    assert_contains(incidents, "script_sod_report_record_event")
    assert_not_contains(incidents, "Black Khergits gather on rich roads")
    assert_contains(horde, "script_sod_report_record_center_event")
    assert_not_contains(horde, "Black Khergit raiders have ridden out from the horde camp")
    assert_contains(diplomacy, "sod_report_reason_realm_treaty")
    assert_contains(diplomacy, "sod_report_reason_realm_war")


def test_notification_queue_is_bounded_and_duplicate_aware() -> None:
    queue = read("src/scripts/ZY_helper_scripts/add_notification_menu.py")
    trigger = read("src/triggers/ST01_every_frame/entry_0006.py")

    for token in [
        'assign, ":queue_limit", 8',
        'assign, ":duplicate", 0',
        'assign, ":insert_slot", -1',
        'troop_slot_eq, "trp_notification_menu_types", ":cur_slot", ":menu_no"',
        'troop_slot_eq, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"',
        'troop_slot_eq, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"',
    ]:
        assert_contains(queue, token)

    assert_contains(trigger, 'assign, ":queue_limit", 8')
    assert_contains(trigger, 'troop_set_slot, "trp_notification_menu_types", ":last_slot", 0')
    assert_contains(trigger, 'troop_set_slot, "trp_notification_menu_var1", ":last_slot", 0')
    assert_contains(trigger, 'troop_set_slot, "trp_notification_menu_var2", ":last_slot", 0')


def test_campaign_dispatch_alert_helpers_have_explicit_minimal_contracts() -> None:
    dispatch = read("src/scripts/ZY_helper_scripts/sod_campaign_dispatch.py")
    recorder = script_block(dispatch, "sod_report_record_event")
    should_alert = script_block(dispatch, "sod_report_should_alert_to_reg")
    show_alert = script_block(dispatch, "sod_report_maybe_show_alert")

    for token in [
        '(store_script_param, ":secondary_kind", 5)',
        '(store_script_param, ":secondary_id", 6)',
        '(store_script_param, ":magnitude", 7)',
        '(store_script_param, ":reason", 8)',
    ]:
        assert_contains(recorder, token)

    for token in [
        '(store_script_param_1, ":severity")',
        '(store_script_param_2, ":primary_kind")',
        '(store_script_param, ":primary_id", 3)',
    ]:
        assert_contains(should_alert, token)
    assert_not_contains(should_alert, ":category")
    assert_not_contains(should_alert, ":secondary_kind")
    assert_not_contains(should_alert, ":secondary_id")

    for token in [
        '(store_script_param_1, ":category")',
        '(store_script_param_2, ":severity")',
        '(store_script_param, ":primary_kind", 3)',
        '(store_script_param, ":primary_id", 4)',
        '(store_script_param, ":magnitude", 5)',
        '(store_script_param, ":reason", 6)',
        '(call_script, "script_sod_report_should_alert_to_reg", ":severity", ":primary_kind", ":primary_id")',
    ]:
        assert_contains(show_alert, token)
    assert_not_contains(show_alert, ":secondary_kind")
    assert_not_contains(show_alert, ":secondary_id")

    for token in [
        '(call_script, "script_sod_report_maybe_show_alert", ":category", ":severity", ":source_kind", ":source_center", ":magnitude", ":reason")',
        '(call_script, "script_sod_report_maybe_show_alert", sod_report_category_contracts, ":severity", ":party_kind", ":party_no", ":magnitude", ":reason")',
        '(call_script, "script_sod_report_maybe_show_alert", ":category", ":severity", sod_report_subject_faction, ":primary_faction", ":magnitude", ":reason")',
    ]:
        assert_contains(dispatch, token)


def main() -> int:
    test_campaign_dispatch_has_bounded_persistent_layout()
    test_campaign_dispatch_is_reachable_and_flushed_on_campaign_cadence()
    test_routine_report_emitters_use_dispatch_not_direct_map_lines()
    test_notification_queue_is_bounded_and_duplicate_aware()
    test_campaign_dispatch_alert_helpers_have_explicit_minimal_contracts()
    print("[campaign_dispatch_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
