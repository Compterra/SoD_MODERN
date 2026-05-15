from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_before(raw, first, second):
    assert first in raw, f"missing token: {first}"
    assert second in raw, f"missing token: {second}"
    assert raw.index(first) < raw.index(second), f"{first} should appear before {second}"


def assert_dialog_menu_jumps_precede_finish_mission():
    offenders = []
    for path in (ROOT / "src/dialogs").rglob("*.py"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "(jump_to_menu" not in raw or "(finish_mission)" not in raw:
            continue
        if raw.index("(jump_to_menu") > raw.index("(finish_mission)"):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, "dialog queues menu after finish_mission: " + ", ".join(offenders)


def assert_dialog_menu_jumps_finish_mission():
    offenders = []
    for path in (ROOT / "src/dialogs").rglob("*.py"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "(jump_to_menu" not in raw:
            continue
        if "(finish_mission)" not in raw:
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, "dialog jumps to menu without finish_mission: " + ", ".join(offenders)


def assert_no_ambiguous_return_menu_locals():
    offenders = []
    for root in ("src/menus", "src/scripts", "src/dialogs", "src/presentations"):
        for path in (ROOT / root).rglob("*.py"):
            raw = path.read_text(encoding="utf-8", errors="replace")
            if '":return_menu"' in raw:
                offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, "local :return_menu collides with global $return_menu: " + ", ".join(offenders)


def test_menu_presentation_flow_is_well_formed():
    troop_tree_dialog = read(
        "src/dialogs/ZA02_sod_court_and_strategy/"
        "trp_sod_strategy_advisor_plyr_sa_select_3_answer_03.py"
    )
    convince_duel_dialog = read(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_convince_duel_02.py"
    )
    black_khergit_duel_dialog = read(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/"
        "anyone_plyr_black_khergit_khan_duel.py"
    )
    black_khergit_field_duel_dialog = read(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/"
        "anyone_plyr_black_khergit_khan_field_duel.py"
    )
    troop_tree_menu = read("src/menus/other/troop_trees_prsenatation.py")
    troop_tree_end = read("src/menus/other/troop_trees_prsenatation_end.py")
    troop_tree_presentation = read("src/presentations/0018_sod_troop_trees/sod_troop_trees.py")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py")
    description = read("src/presentations/0022_sod_description/sod_description.py")
    retinue_dialog = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_regular_member_retinue_command.py")
    retinue_menu = read("src/menus/camp/companion_retinue_report.py")
    menu_preamble = read("src/menus/_preamble/00_imports.py")

    assert_before(
        troop_tree_dialog,
        '(jump_to_menu, "mnu_troop_trees_prsenatation")',
        "(finish_mission)",
    )
    assert_before(
        convince_duel_dialog,
        '(jump_to_menu, "mnu_convince_duel")',
        "(finish_mission)",
    )
    assert_before(
        black_khergit_duel_dialog,
        '(jump_to_menu, "mnu_sod_black_khergit_khan_duel_prepare")',
        "(finish_mission)",
    )
    assert_before(
        black_khergit_field_duel_dialog,
        '(jump_to_menu, "mnu_sod_black_khergit_khan_duel_prepare")',
        "(finish_mission)",
    )
    assert_before(
        troop_tree_menu,
        '(jump_to_menu, "mnu_troop_trees_prsenatation_end")',
        '(start_presentation, "prsnt_sod_troop_trees")',
    )
    assert troop_tree_menu.count('(jump_to_menu, "mnu_troop_trees_prsenatation_end")') == 2

    for token in [
        '(eq, "$g_sod_sa_in_court", 0)',
        '(start_map_conversation, "trp_sod_strategy_advisor")',
        "(change_screen_return)",
        '(call_script, "script_enter_court", "$g_encountered_party")',
        '(change_screen_map_conversation, "trp_sod_strategy_advisor")',
    ]:
        assert token in troop_tree_end, f"troop tree return menu missing: {token}"

    assert '(create_mesh_overlay, reg1, "mesh_random_merc_troop_tree")' in troop_tree_presentation
    assert "(presentation_set_duration, 0)" in troop_tree_presentation

    assert '(assign, "$g_sod_description_return_to_reports", 1)' in reports_menu
    assert '(jump_to_menu, "mnu_reports")' in description
    assert '(assign, "$g_sod_description_return_to_reports", 0)' in description
    assert '(assign, "$g_sod_retinue_return_menu", 0)' in retinue_dialog
    assert '(assign, "$g_sod_retinue_return_menu", "mnu_companion_retinue_report")' in retinue_menu
    assert '(assign, ":sod_retinue_back_menu", "$g_sod_retinue_return_menu")' in retinue_menu
    assert '(assign, "$g_sod_retinue_return_menu", 0)' in retinue_menu
    assert '(jump_to_menu, ":sod_retinue_back_menu")' in retinue_menu
    assert '":return_menu"' not in retinue_menu
    assert "def build_sod_battle_commander_change_option(option_id, commander_return_menu" in menu_preamble
    assert "option_id, return_menu" not in menu_preamble
    assert '":return_menu"' not in menu_preamble
    assert "(change_screen_return)" in retinue_menu
    assert_dialog_menu_jumps_precede_finish_mission()
    assert_dialog_menu_jumps_finish_mission()
    assert_no_ambiguous_return_menu_locals()


def main():
    test_menu_presentation_flow_is_well_formed()
    print("Menu/presentation flow static checks passed")


if __name__ == "__main__":
    main()
