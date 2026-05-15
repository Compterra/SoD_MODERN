from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DEBUG_COLOR_MESSAGE_RE = re.compile(
    r'\((?:display_message|display_log_message),\s*"@[^"\n]*",\s*debug_color\)'
)
DEBUG_GUARD_RE = re.compile(
    r'\$g_sod_debug|\$cheat_mode|:debug|eq,\s*1,\s*0|g_sod_diplomacy_notification_level'
)
DEBUG_CONTEXT_LINES = 36
WHOLE_FILE_DEBUG_GUARDS = {
    "src/triggers/ST02_every_hour/entry_0173_string_probe.py": '(eq, "$g_sod_debug", 1)',
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_not_contains(raw: str, token: str, label: str) -> None:
    assert token not in raw, f"{label}: unexpected shipped debug token {token!r}"


def test_common_gameplay_paths_do_not_emit_leftover_debug_messages() -> None:
    cases = {
        "companion tavern refresh": read("src/scripts/ZH_heroes/update_companion_candidates_in_taverns.py"),
        "auto loot": read("src/scripts/ZZ_common_array_processing/auto_loot_all.py"),
        "join battle retreat": read("src/menus/encounter/join_attack.py"),
        "prisoner agreement": read("src/scripts/ZC_parties/determine_prisoner_agreed.py"),
        "kingdom party limits": read("src/scripts/ZC_parties/create_kingdom_party_if_below_limit.py"),
        "kingdom party creation": read("src/scripts/ZC_parties/cf_create_kingdom_party.py"),
        "lord party upgrade": read("src/scripts/ZC_parties/cf_party_upgrade_with_xp.py"),
        "distance factor": read("src/scripts/ZY_helper_scripts/calculate_dist_factor.py"),
        "center security": read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py"),
        "trade route setup": read("src/scripts/ZB_economy_and_trade/set_trade_route_between_centers.py"),
        "rebellion rival argument": read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_join_rebellion_suggest_2_02.py"),
        "weekly rents": read("src/triggers/ST04_weekly/entry_0038.py"),
        "tax couriers": read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py"),
        "quest consequences": read("src/scripts/ZG_quests/sod_quest_outcome_apply_consequences.py"),
        "player faction activation": read("src/scripts/ZF_factions/activate_deactivate_player_faction.py"),
        "battle renown": read("src/scripts/ZY_helper_scripts/calculate_renown_value.py"),
    }

    assert_not_contains(cases["companion tavern refresh"], "Companion tavern debug", "companion tavern refresh")
    assert_not_contains(cases["auto loot"], "Auto-loot debug", "auto loot")
    assert_not_contains(cases["join battle retreat"], "Player retreats from battle", "join battle retreat")
    assert_not_contains(cases["prisoner agreement"], "piss off", "prisoner agreement")
    assert_not_contains(cases["kingdom party limits"], "out of {reg1} caravans", "kingdom party limits")
    assert_not_contains(cases["kingdom party creation"], "created a caravan party", "kingdom party creation")
    assert_not_contains(cases["lord party upgrade"], "Upgrading {s1}'s party", "lord party upgrade")
    assert_not_contains(cases["distance factor"], "Bug : Calculate dist factor", "distance factor")
    assert_not_contains(cases["center security"], "Bug : center security profile", "center security")
    assert_not_contains(cases["trade route setup"], "ERROR: More than 15 trade routes", "trade route setup")
    assert_not_contains(cases["rebellion rival argument"], "Rebellion chance -30 from rival", "rebellion rival argument")
    assert_not_contains(cases["battle renown"], "Debug: renown value for this battle", "battle renown")
    for label, raw in cases.items():
        assert_not_contains(raw, "@DEBUG", label)


def test_exported_string_tables_do_not_ship_leftover_debug_messages() -> None:
    exports = {
        "strings.txt": read("_export/strings.txt"),
        "quick_strings.txt": read("_export/quick_strings.txt"),
    }
    for label, raw in exports.items():
        assert_not_contains(raw, "Companion_tavern_debug", label)
        assert_not_contains(raw, "Companion tavern debug", label)
        assert_not_contains(raw, "Auto-loot_debug", label)
        assert_not_contains(raw, "Auto-loot debug", label)
        assert_not_contains(raw, "Debug:_renown_value_for_this_battle", label)
        assert_not_contains(raw, "Debug: renown value for this battle", label)


def test_battle_renown_debug_does_not_replace_gameplay_feedback() -> None:
    raw = read("src/scripts/ZY_helper_scripts/calculate_renown_value.py")
    player_feedback = raw.index("@This victory will be spoken of widely.")
    debug_feedback = raw.index("@Renown debug: battle value {reg8}.")
    assert player_feedback < debug_feedback
    assert '(display_message, "@Renown debug: battle value {reg8}.", debug_color)' in raw


def test_debug_color_messages_are_guarded() -> None:
    offenders: list[str] = []
    for path in sorted((ROOT / "src").rglob("*.py")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        rel = path.relative_to(ROOT).as_posix()
        whole_file_guard = WHOLE_FILE_DEBUG_GUARDS.get(rel)
        if whole_file_guard:
            top_context = " ".join(lines[:12])
            assert whole_file_guard in top_context, f"{rel}: expected whole-file debug guard {whole_file_guard}"
        for line_no, line in enumerate(lines, start=1):
            if line.lstrip().startswith("#"):
                continue
            if not DEBUG_COLOR_MESSAGE_RE.search(line):
                continue
            if whole_file_guard:
                continue
            start = max(0, line_no - DEBUG_CONTEXT_LINES)
            context = " ".join(lines[start:line_no])
            if not DEBUG_GUARD_RE.search(context):
                offenders.append(f"{rel}:{line_no}: {line.strip()}")

    assert not offenders, "unguarded debug_color display messages:\n" + "\n".join(offenders)


if __name__ == "__main__":
    test_common_gameplay_paths_do_not_emit_leftover_debug_messages()
    test_exported_string_tables_do_not_ship_leftover_debug_messages()
    test_debug_color_messages_are_guarded()
    print("test_debug_log_hygiene_static: OK")
