# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

import audit_string_registers

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = (
    ROOT / "src" / "scripts",
    ROOT / "src" / "menus",
    ROOT / "src" / "dialogs",
    ROOT / "src" / "triggers",
    ROOT / "src" / "presentations",
    ROOT / "src" / "mission_templates",
    ROOT / "src" / "quests",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected stale token: {needle}")


def assert_no_source_sreg_display() -> None:
    offenders: list[str] = []
    for root in SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            raw = path.read_text(encoding="utf-8")
            for line_no, line in enumerate(raw.splitlines(), start=1):
                if audit_string_registers.DISPLAY_SREG_RE.search(line):
                    rel = path.relative_to(ROOT).as_posix()
                    offenders.append(f"{rel}:{line_no}: {line.strip()}")
    if offenders:
        details = "\n".join(offenders[:20])
        raise AssertionError(f"Source still contains non-native display_message/display_log_message s-register calls:\n{details}")


def assert_no_source_unsupported_direct_s_placeholder() -> None:
    offenders: list[str] = []
    for root in SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            raw = path.read_text(encoding="utf-8")
            for line_no, line in enumerate(raw.splitlines(), start=1):
                code = audit_string_registers.code_part(line)
                for match in audit_string_registers.FORMAT_S_RE.finditer(code):
                    if int(match.group(1)) >= 100:
                        rel = path.relative_to(ROOT).as_posix()
                        offenders.append(f"{rel}:{line_no}: {line.strip()}")
    if offenders:
        details = "\n".join(offenders[:20])
        raise AssertionError(f"Source still contains direct {{s100+}} placeholders:\n{details}")


def main() -> int:
    audit_src = read("build/audit_string_registers.py")
    build_all = read("build/build_all.py")
    build_module = read("build_module.bat")
    horde = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    morale = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    companion_campfire_menu = read("src/menus/camp/companion_campfire.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    weekly_migration = read("src/scripts/ZY_helper_scripts/sod_center_weekly_migration.py")
    weekly_desperation = read("src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py")

    assert_contains(audit_src, "String Register Usage Audit")
    assert_contains(audit_src, "LIVE_MESSAGE_RE")
    assert_contains(audit_src, "DEFERRED_STORE_RE")
    assert_contains(audit_src, "DISPLAY_SREG_RE")
    assert_contains(audit_src, "CONDITIONAL_INNER_PLACEHOLDER_RE")
    assert_contains(audit_src, "MALFORMED_REGISTER_PLACEHOLDER_RE")
    assert_contains(audit_src, "NESTED_STRING_STORE_RE")
    assert_contains(audit_src, "unsupported_direct_s_placeholder")
    assert_contains(audit_src, "Non-Native String-Register Display Risks")
    assert_contains(audit_src, "Deferred String-Register Display Risks")
    assert_contains(audit_src, "Nested String-Register Store Risks")
    assert_contains(audit_src, "Unsupported Direct Placeholder Risks")
    assert_contains(audit_src, "Conditional Placeholder Parse Risks")
    assert_contains(audit_src, "process_strings.py")
    assert_contains(audit_src, "display_message|display_log_message")
    assert_contains(audit_src, "Native M&B 1.011 uses")
    assert_contains(audit_src, "High Register Usage (`s50+`)")
    assert_contains(audit_src, "Simple Register Lanes")
    assert_contains(audit_src, "s68-s99")
    assert_contains(audit_src, "Severity Buckets")
    assert_contains(audit_src, "Top 20 High-Risk Source Findings")
    assert_contains(audit_src, "Generated export")
    assert_contains(audit_src, "conditional parse risk(s)")
    assert_contains(audit_src, "nested string-store risk(s)")
    assert_contains(audit_src, "unsupported direct placeholder(s)")
    assert_contains(audit_src, "malformed placeholder(s)")
    assert_contains(audit_src, "--fail-on-critical")
    assert_contains(audit_src, "critical text export risk(s) found")
    assert_contains(build_all, "audit_string_registers_main()")
    assert_contains(build_module, "Post-process text/export audit")
    assert_contains(build_module, "audit_string_registers.py\" --fail-on-critical")
    if not (
        build_module.index("process_global_variables_unused.py")
        < build_module.index("audit_string_registers.py")
        < build_module.index("--doctor-hardcoded-postprocess")
    ):
        raise AssertionError("build_module.bat must audit exported text after process pipeline and before postprocess doctor")

    assert_not_contains(horde, "The Black Khergit horde is moving toward the rich roads around {s60}.")
    assert_contains(horde, 'The Black Khergit horde packs its tents and rides toward another rich trade road.')
    assert_not_contains(horde, "(display_message, s2, 0x222222)")
    for helper in (
        "src/scripts/ZH_heroes/store_troop_name_link.py",
        "src/scripts/ZH_heroes/store_troop_name.py",
        "src/scripts/ZD_centers/store_troop_name_link_fief.py",
        "src/scripts/ZD_centers/store_troop_name_fief.py",
    ):
        raw_helper = read(helper)
        assert_not_contains(raw_helper, "@{s27}")
        assert_not_contains(raw_helper, "@{s37}")
        assert_not_contains(raw_helper, "(str_store_string, \":string\", \"@{s")
    assert_contains(morale, '(display_log_message, "@lord_follow_intent: {s5} intent {reg5}, pressure {reg6}, morale {reg7}, pay {reg8}, fatigue {reg9}, follow {reg10}.", debug_color)')
    assert_contains(morale, '(display_log_message, "@lord_strategy_intent: {s5} intent {reg6}, pressure {reg7}, locked {reg8}.", debug_color)')
    assert_contains(companion_campfire_menu, '"{s68}"')
    assert_contains(companion_campfire_menu, 'script_sod_companion_describe_campfire_to_s68')
    assert_not_contains(companion_campfire_menu, '"{s1}"')
    assert_not_contains(companion_campfire_menu, 'script_sod_companion_describe_campfire_to_s1')
    assert_contains(companion_depth, '("sod_companion_describe_campfire_to_s68",')
    assert_contains(companion_depth, '(str_store_string_reg, s69, s1)')
    assert_contains(companion_depth, '(str_store_string, s68, "@Companion Campfire^^{s69}')
    assert_contains(companion_depth, '("sod_companion_describe_campfire_to_s1",')
    assert_contains(companion_depth, '(str_store_string_reg, s1, s68)')
    for raw_world_events in (weekly_migration, weekly_desperation):
        assert_contains(raw_world_events, "(str_store_party_name_link, s68,")
        assert_contains(raw_world_events, "{s68}")
        assert_not_contains(raw_world_events, "(str_store_party_name_link, s1, \":source_no\")")
        assert_not_contains(raw_world_events, "(str_store_party_name_link, s2, \":dest_no\")")
        assert_not_contains(raw_world_events, "Word spreads that {reg0} villagers have left {s1}")
        assert_not_contains(raw_world_events, "Word spreads that {reg0} townsfolk have left {s1}")
        assert_not_contains(raw_world_events, "Word spreads that {reg0} townsfolk have departed {s1}")
    assert_contains(weekly_desperation, "Desperation grips {s68}")
    assert_not_contains(weekly_desperation, "Desperation grips {s1}")
    assert_no_source_sreg_display()
    assert_no_source_unsupported_direct_s_placeholder()

    audit_string_registers.main()
    report = read("docs/reports/string_register_usage_report.md")
    assert_contains(report, "# String Register Usage Audit")
    assert_contains(report, "## Native Inline Display/Log Placeholder Usage")
    assert_contains(report, "## Non-Native String-Register Display Risks")
    assert_contains(report, "## Deferred String-Register Display Risks")
    assert_contains(report, "## Nested String-Register Store Risks")
    assert_contains(report, "## Unsupported Direct Placeholder Risks")
    assert_contains(report, "## Conditional Placeholder Parse Risks")
    assert_contains(report, "Nested string-register store risks found:")
    assert_contains(report, "Unsupported direct `{s100+}` placeholders found:")
    assert_contains(report, "Conditional placeholders containing inner placeholders found:")
    assert_contains(report, "Malformed register placeholders found:")
    assert_contains(report, "### Severity Buckets")
    assert_contains(report, "## Generated export")
    assert_contains(report, "### Top High-Risk Source Files")
    assert_contains(report, "### Top 20 High-Risk Source Findings")
    assert_contains(report, "### High Register Usage (`s50+`)")
    assert_contains(report, "## Simple Register Lanes")
    assert_contains(report, "`s68-s99`")
    assert_contains(report, "- Non-native string-register display calls found: 0")
    assert_contains(report, "- Deferred string-register display risks found: 0")
    assert_not_contains(report, "The Black Khergit horde is moving toward the rich roads around {s60}.")

    quick_strings = read("_export/quick_strings.txt")
    assert_not_contains(quick_strings, "The_Black_Khergit_horde_is_moving_toward_the_rich_roads_around_{s60}.")
    assert_not_contains(quick_strings, "The_Black_Khergit_horde_is_moving_toward_the_rich_roads_around_{s1}.")

    print("[string_register_audit_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
