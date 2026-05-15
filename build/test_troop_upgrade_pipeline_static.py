from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    upgrader = read("src/scripts/ZC_parties/cf_party_upgrade_with_xp.py")
    permission = read("src/scripts/ZY_helper_scripts/sod_troop_can_upgrade_at_center.py")
    town_menu = read("src/menus/other/sod_upgrade_continue.py")
    menu_preamble = read("src/menus/_preamble/00_imports.py")
    checklist = read("docs/tooling/TROOP_UPGRADE_PIPELINE_REFACTOR_CHECKLIST.md")

    for token in [
        '"cf_party_upgrade_with_xp"',
        '"sod_party_upgrade_context_to_regs"',
        '"sod_party_upgrade_find_ai_training_center_to_reg"',
        '"sod_party_upgrade_stack_paths_to_regs"',
        '"sod_party_upgrade_path_allowed_to_reg"',
        '"sod_party_upgrade_apply_elite_cap_to_reg"',
        '"sod_party_upgrade_apply_path_to_regs"',
        '"sod_party_upgrade_debug_report_path"',
        '"sod_party_upgrade_debug_report_summary"',
    ]:
        assert_contains(upgrader, token)

    for token in [
        "party_get_attached_to",
        "script_sod_party_upgrade_find_ai_training_center_to_reg",
        "slot_town_lord, \":lord_troop\"",
        "slot_faction_central_center",
        "slot_center_is_besieged_by, -1",
        "store_faction_of_party",
        "Legacy non-lord callers keep the old implicit town context",
        "only no-center-safe upgrades may apply",
        "lord-owned safe fief",
        "faction central center",
        "faction-owned safe center",
        "no safe center",
    ]:
        assert_contains(upgrader, token)

    assert upgrader.count("script_sod_get_cost_to_upgrade_troop_at") == 1
    assert upgrader.count("party_remove_members") == 1
    assert upgrader.count("party_add_members") == 1
    assert_not_contains(upgrader, "#UPGRADE 1")
    assert_not_contains(upgrader, "#UPGRADE 2")

    for token in [
        "script_sod_troop_store_upgrade_fail_reason",
        "str_store_string_reg, s73, s0",
        "SoD upgrade debug:",
        "SoD upgrade debug summary:",
        "(eq, \"$g_sod_debug\", 1)",
        "party_slot_eq, \":party_no\", slot_party_type, spt_kingdom_hero_party",
        "(assign, reg1, \":fail_reason\")",
        "(assign, reg2, \":fail_reason\")",
        "(assign, reg3, \":result_code\")",
        "(assign, reg4, \":spent\")",
    ]:
        assert_contains(upgrader, token)

    for token in [
        "sod_elite_tier_faith",
        "(lt, \":faith_roll\", 12)",
        "(val_min, \":count\", 1)",
        "sod_elite_tier_noble",
        "(store_add, \":noble_cap\", 2, \":artifact_bias\")",
    ]:
        assert_contains(upgrader, token)

    for token in [
        "reg0",
        "reg1",
        "slot_center_has_barracks",
        "slot_center_has_range",
        "slot_center_has_stables",
        "slot_center_has_chapter",
        "slot_center_has_temple",
        "slot_center_has_chapel",
        "script_cf_sod_center_mercenary_guild_hall_supports_troop",
        "sod_upgrade_fail_wrong_faction",
        "sod_upgrade_fail_merc_permission",
    ]:
        assert_contains(permission, token)

    assert_contains(town_menu, 'script_sod_can_upgrade_troops_here", ":upgrade1", "$g_sod_upgrade_center"')
    assert_contains(town_menu, 'script_sod_can_upgrade_troops_here", ":upgrade2", "$g_sod_upgrade_center"')
    assert_contains(menu_preamble, 'script_sod_can_upgrade_troops_here", ":upgrade1", ":upgrade_center"')
    assert_contains(menu_preamble, 'script_sod_can_upgrade_troops_here", ":upgrade2", ":upgrade_center"')

    for token in [
        "# Troop Upgrade Pipeline Refactor Checklist",
        "- [x] Preserve `script_cf_party_upgrade_with_xp` as the public entrypoint.",
        "- [x] Add mobile AI lord fallback training-center selection.",
        "- [x] Keep player-facing upgrade menus on center-specific permission checks.",
        "- [x] Add a debug-only AI upgrade report for attempts, skips, context, and gold spent.",
        "- [ ] Future balancing: review AI upgrade gold pools, faith-roll odds, and noble caps after playtesting.",
    ]:
        assert_contains(checklist, token)

    print("test_troop_upgrade_pipeline_static: OK")


if __name__ == "__main__":
    main()
