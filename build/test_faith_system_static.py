from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"Missing expected text: {needle}"


def test_hidden_population_weighted_faith_gain_script_exists():
    scripts = read("src/scripts/ZY_helper_scripts/sod_faith_system.py")
    assert_contains(scripts, '"sod_apply_weekly_population_faith_gain"')
    assert_contains(scripts, '(is_between, "$g_sod_faith", sod_faiths_begin, sod_faiths_end)')
    assert_contains(scripts, '(try_for_range, ":center_no", centers_begin, centers_end)')
    assert_contains(scripts, '(this_or_next|eq, ":center_faction", "fac_player_supporters_faction")')
    assert_contains(scripts, '(eq, ":center_faction", "fac_player_faction")')
    assert_contains(scripts, 'slot_center_sod_local_population')
    assert_contains(scripts, '(call_script, "script_sod_normalize_center_population", ":center_no")')
    assert_contains(scripts, '(call_script, "script_sod_get_center_faith_profile", ":center_no")')
    assert_contains(scripts, '(assign, ":player_support", reg2)')
    assert_contains(scripts, '(try_for_range, ":faith_id", sod_faiths_begin, sod_faiths_end)')
    assert_contains(scripts, '(call_script, "script_sod_get_center_faith_support", ":center_no", ":faith_id")')
    assert_contains(scripts, '(store_mul, ":center_weighted_faith", ":population", ":player_support")')
    assert_contains(scripts, '(val_div, ":center_weighted_faith", ":total_support")')
    assert_contains(scripts, '(store_div, ":faith_gain", ":weighted_faith_population", 500)')
    assert_contains(scripts, '(val_add, "$g_sod_global_faith", ":faith_gain")')
    assert_contains(scripts, '(assign, reg1, ":weighted_faith_population")')
    assert_contains(scripts, '(assign, reg2, ":realm_population")')


def test_weekly_faith_pass_uses_population_weight_after_local_drift():
    trigger = read("src/triggers/ST04_weekly/entry_0132_five_faith_drift.py")
    assert_contains(trigger, '(call_script, "script_sod_apply_weekly_faith_drift", ":center_no")')
    assert_contains(trigger, '(call_script, "script_sod_apply_weekly_population_faith_gain")')
    assert trigger.index('script_sod_apply_weekly_faith_drift') < trigger.index('script_sod_apply_weekly_population_faith_gain')
    assert trigger.index('script_sod_apply_weekly_population_faith_gain') < trigger.index('script_sod_get_realm_faith_profile')


def test_faith_buildings_feed_local_support_not_direct_global_faith():
    for rel in [
        "src/triggers/ST04_weekly/entry_0089.py",
        "src/triggers/ST04_weekly/entry_0090.py",
        "src/triggers/ST04_weekly/entry_0091.py",
    ]:
        text = read(rel)
        assert_contains(text, 'script_sod_change_center_faith_support')
        assert '(val_add, "$g_sod_global_faith"' not in text


def test_faith_ledger_is_debug_only_and_camp_rites_do_not_explain_hidden_gain():
    reports = read("src/menus/reports/report_submenus.py")
    assert_contains(reports, '("view_faith_world_report", [')
    assert_contains(reports, '(this_or_next|eq, "$cheat_mode", 1)')
    assert_contains(reports, '(eq, "$g_sod_cheat_mode", 1)')
    faith_menu = read("src/menus/reports/faith_world_report.py")
    assert_contains(faith_menu, '(neq, "$cheat_mode", 1)')
    assert_contains(faith_menu, '(neq, "$g_sod_cheat_mode", 1)')
    assert_contains(faith_menu, 'jump_to_menu, "mnu_reports"')

    camp_jobs = read("src/scripts/ZY_helper_scripts/sod_camp_jobs.py")
    assert "Faith rises slowly" not in camp_jobs
    assert "company faith deepens" not in camp_jobs
    assert_contains(camp_jobs, "The camp steadies slowly")
    assert_contains(camp_jobs, "The lines settle for the night")
