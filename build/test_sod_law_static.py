# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONSTANTS = ROOT / "src" / "constants" / "module_constants.py"
LAW_FRAMEWORK = ROOT / "src" / "scripts" / "ZZ_common_array_processing" / "sod_law_framework.py"
LAW_EFFECTS = ROOT / "src" / "scripts" / "ZZ_common_array_processing" / "sod_law_effects.py"
LAW_AI = ROOT / "src" / "scripts" / "ZZ_common_array_processing" / "sod_law_ai.py"
PRESENTATION = ROOT / "src" / "presentations" / "0019_sod_law" / "sod_law.py"
WEEKLY_LAW_TRIGGER = ROOT / "src" / "triggers" / "ST04_weekly" / "entry_0098.py"
VOLUNTEER_RECRUITMENT = ROOT / "src" / "scripts" / "ZD_centers" / "update_volunteer_troops_in_village.py"
NPC_VOLUNTEER_RECRUITMENT = ROOT / "src" / "scripts" / "ZD_centers" / "update_npc_volunteer_troops_in_village.py"
VILLAGE_MENU = ROOT / "src" / "menus" / "other" / "recruit_volunteers.py"
TOWN_MENU = ROOT / "src" / "menus" / "castle" / "castle_castle.py"
REALM_LAW_REPORT = ROOT / "src" / "menus" / "camp" / "realm_law_report.py"
REPORTS_MENU = ROOT / "src" / "menus" / "camp" / "reports.py"
WEEKLY_BONUSES_REPORT = ROOT / "src" / "menus" / "other" / "weekly_bonuses_report.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_faction_law_constants() -> None:
    raw = read(CONSTANTS)
    for token in (
        "slot_faction_law_1",
        "slot_faction_law_10",
        "faction_laws_begin",
        "faction_laws_end",
        "sod_law_max_active",
        "slot_faction_law_tax_peasants",
        "slot_faction_law_unrest",
        "sod_law_block_conflict",
    ):
        assert_contains(raw, token)

    law_values = set(re.findall(r"(?m)^sod_law_[a-z0-9_]+\s*=\s*([0-9]+)\b", raw))
    expected = {str(i) for i in range(1, 40)}
    assert expected <= law_values


def test_faction_law_helper_scripts_exist() -> None:
    raw = read(LAW_FRAMEWORK)
    for script_id in (
        "sod_law_is_active_for_faction",
        "sod_law_add_to_faction",
        "sod_law_remove_from_faction",
        "sod_law_can_enact_for_faction",
        "sod_law_can_dismiss_for_faction",
        "sod_law_sync_player_legacy_slots",
        "sod_law_migrate_player_legacy_slots",
        "sod_law_maybe_notify_foreign_change",
    ):
        haystack = raw + read(ROOT / "src" / "scripts" / "ZZ_common_array_processing" / "sod_law_reports.py")
        assert_contains(haystack, f'"{script_id}"')

    for spacer in ("sod_law_spacer_villagers", "sod_law_spacer_townspeople", "sod_law_spacer_clergy"):
        assert_contains(raw, spacer)


def test_law_rules_and_effects_are_centralized() -> None:
    framework = read(LAW_FRAMEWORK)
    effects = read(LAW_EFFECTS)
    for pair in (
        ("sod_law_enfranchisement", "sod_law_serfdom"),
        ("sod_law_high_capitation", "sod_law_low_capitation"),
        ("sod_law_low_town_taxes", "sod_law_high_town_taxes"),
        ("sod_law_temple_supremacy", "sod_law_royal_supremacy"),
    ):
        assert_contains(framework, pair[0])
        assert_contains(framework, pair[1])

    for law in (
        "sod_law_village_fairs",
        "sod_law_theocracy",
        "sod_law_holy_war",
        "sod_law_absolute_monarchy",
        "sod_law_elective_monarchy",
    ):
        assert_contains(effects, law)

    assert_contains(effects, "val_clamp, \":tax\", sod_law_tax_peasants_min, sod_law_tax_peasants_max")
    assert_contains(effects, "val_clamp, \":pop\", sod_law_town_population_modifier_min, sod_law_town_population_modifier_max")
    assert_contains(framework, "sod_law_block_unrest")
    assert_contains(framework, "sod_law_ai_tag_oppressive")
    assert_contains(framework, "slot_faction_law_unrest")
    assert_contains(framework, "sod_law_arbitrary_edicts")


def test_presentation_uses_faction_api() -> None:
    raw = read(PRESENTATION)
    assert_contains(raw, "script_sod_law_can_enact_for_faction")
    assert_contains(raw, "script_sod_law_store_block_reason_text")
    assert_contains(raw, "script_sod_law_add_to_faction")
    assert_contains(raw, "script_sod_law_remove_from_faction")
    assert "troop_set_slot, \"trp_law\"" not in raw
    assert "troop_get_slot, \":new_law\", \"trp_law\"" not in raw
    assert "script_activate_law" not in raw
    assert "script_deactivate_law" not in raw


def test_weekly_and_ai_wiring() -> None:
    trigger = read(WEEKLY_LAW_TRIGGER)
    tax_trigger = read(ROOT / "src" / "triggers" / "ST04_weekly" / "entry_0038.py")
    recruitment = read(VOLUNTEER_RECRUITMENT)
    npc_recruitment = read(NPC_VOLUNTEER_RECRUITMENT)
    ai = read(LAW_AI)
    assert_contains(trigger, "script_sod_law_ai_process_all_factions")
    assert_contains(trigger, "script_sod_law_initialize_all_faction_defaults")
    assert_contains(trigger, "script_sod_law_calculate_center_support")
    assert_contains(trigger, "script_sod_law_apply_center_compliance_pressure")
    assert_contains(trigger, "slot_faction_law_village_faith_modifier")
    assert_contains(trigger, "slot_faction_law_town_prosperity_modifier")
    assert_contains(tax_trigger, "script_sod_law_calculate_center_tax_compliance")
    assert_contains(recruitment, "script_sod_law_calculate_center_tax_compliance")
    assert_contains(recruitment, ":law_recruitment_compliance")
    assert_contains(npc_recruitment, "script_sod_law_calculate_center_tax_compliance")
    assert_contains(npc_recruitment, ":law_recruitment_compliance")
    assert_contains(read(LAW_EFFECTS), '"sod_law_apply_center_compliance_pressure"')
    assert_contains(read(LAW_EFFECTS), "Legal resistance")
    assert_contains(read(LAW_EFFECTS), "accept the realm's laws readily")
    assert_contains(ai, '"sod_law_ai_process_faction"')
    assert_contains(ai, '"sod_law_ai_score_law_for_faction"')
    assert_contains(ai, '"sod_law_ai_apply_stability_adjustment"')
    assert ai.count("script_sod_law_ai_apply_stability_adjustment") >= 2
    assert_contains(ai, "sod_law_ai_tag_oppressive")
    assert_contains(ai, "sod_law_ai_tag_legitimizing")
    assert_contains(ai, "slot_faction_law_legitimacy")


def test_realm_law_report_surface() -> None:
    report_menu = read(REALM_LAW_REPORT)
    reports_menu = read(REPORTS_MENU)
    weekly_report = read(WEEKLY_BONUSES_REPORT)
    report_script = read(ROOT / "src" / "scripts" / "ZZ_common_array_processing" / "sod_law_reports.py")
    assert_contains(report_menu, "script_sod_law_describe_realm_law_report")
    assert_contains(reports_menu, "mnu_realm_law_report")
    assert_contains(reports_menu, "view_weekly_law_bonuses_report")
    assert_contains(weekly_report, "slot_faction_law_village_relation_modifier")
    assert "$g_sod_village_rep_modifier" not in weekly_report
    assert_contains(report_script, '"sod_law_append_player_compliance_report"')
    assert_contains(report_script, "Local compliance")
    assert_contains(report_script, "Resisting collectors")
    assert_contains(report_script, '"sod_law_describe_center_compliance_to_s21"')
    assert_contains(report_script, "Legal mood")
    assert_contains(report_script, "Foreign realm laws")
    assert_contains(report_script, "Unknown realms omitted due to insufficient intelligence")
    village_menu = read(VILLAGE_MENU)
    assert_contains(village_menu, "{s21}")
    assert_contains(village_menu, "script_sod_law_describe_center_compliance_to_s21")
    town_menu = read(TOWN_MENU)
    assert_contains(town_menu, "{s21}")
    assert_contains(town_menu, "script_sod_law_describe_center_compliance_to_s21")


if __name__ == "__main__":
    test_faction_law_constants()
    test_faction_law_helper_scripts_exist()
    test_law_rules_and_effects_are_centralized()
    test_presentation_uses_faction_api()
    test_weekly_and_ai_wiring()
    test_realm_law_report_surface()
    print("test_sod_law_static: OK")
