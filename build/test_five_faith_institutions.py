# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError("Missing expected token: %s" % needle)


def main() -> int:
    constants = read("src/constants/module_constants.py")
    faith = read("src/scripts/ZY_helper_scripts/sod_faith_system.py")
    ascend = read("src/scripts/ZY_helper_scripts/sod_troop_can_faith_ascend_at_center.py")
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    report = read("src/scripts/ZY_helper_scripts/sod_describe_faith_world_report.py")
    doctrine = read("src/scripts/ZY_helper_scripts/sod_describe_elite_doctrine_report.py")
    weekly = read("src/triggers/ST04_weekly/entry_0132_five_faith_drift.py")
    temple = read("src/triggers/ST04_weekly/entry_0089.py")
    shrine_chapel = read("src/triggers/ST04_weekly/entry_0090.py")
    monastery = read("src/triggers/ST04_weekly/entry_0091.py")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py")
    realm_reports = read("src/menus/reports/report_submenus.py")
    faith_menu = read("src/menus/reports/faith_world_report.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    recon_brief = read("src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py")

    for token in (
        "slot_center_sod_faith_1_support",
        "slot_center_sod_faith_2_support",
        "slot_center_sod_faith_3_support",
        "slot_center_sod_faith_4_support",
        "slot_center_sod_faith_5_support",
        "slot_center_sod_dominant_faith",
        "slot_center_sod_faith_tension",
        "slot_center_sod_faith_institution_strength",
        "slot_faction_sod_clergy_legitimacy",
        "sod_faith_tension_soft_cap",
    ):
        assert_contains(constants, token)

    for token in (
        '"sod_get_center_faith_profile"',
        '"sod_change_center_faith_support"',
        '"sod_get_realm_faith_profile"',
        '"sod_apply_weekly_faith_drift"',
        "script_sod_get_center_security_profile",
        "script_sod_get_center_food_profile",
        "sod_center_modifier_faith_stability_flat",
        "val_clamp",
        "slot_center_sod_local_faith",
    ):
        assert_contains(faith, token)

    for token in (
        "script_sod_get_center_faith_profile",
        "slot_center_has_temple",
        "slot_center_has_chapel",
        "sod_faith_ascension_local_min",
        "sod_faith_tension_soft_cap",
        "faith_tension",
        "institution_strength",
    ):
        assert_contains(ascend, token)

    assert_contains(security, "faith_unrest_pressure")
    assert_contains(security, "script_sod_get_center_faith_profile")

    for raw in (temple, shrine_chapel, monastery):
        assert_contains(raw, "script_sod_change_center_faith_support")

    assert_contains(weekly, "script_sod_apply_weekly_faith_drift")
    assert_contains(weekly, "script_sod_get_realm_faith_profile")

    for token in (
        "Faith And Institutions",
        "Dominant realm faith",
        "player-faith support",
        "faith tension",
        "elite",
    ):
        assert_contains(report, token)

    assert_contains(reports_menu, "mnu_realm_reports")
    assert_contains(realm_reports, "view_faith_world_report")
    assert_contains(realm_reports, "Read faith and institution report.")
    assert_contains(realm_reports, "mnu_faith_world_report")
    assert_contains(faith_menu, "script_sod_describe_faith_world_report")
    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68")
    assert_contains(recon_brief, "script_sod_get_center_faith_profile")
    assert_contains(recon_brief, "Religious tension is worsening.")
    assert_contains(doctrine, "Ascension-ready seats")
    assert_contains(doctrine, "manageable local faith tension")

    print("five-faith institution static checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


