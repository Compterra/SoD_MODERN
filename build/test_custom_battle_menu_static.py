from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "0000_hardcoded_mb1011" / "custom_battle_2.py"
PICKER = ROOT / "src" / "menus" / "0000_hardcoded_mb1011" / "start_game_3_custom_battle_picker.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected custom battle behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")
    picker = PICKER.read_text(encoding="utf-8")

    assert_contains(picker, '"start_game_3", mnf_disable_all_keys,')
    assert_contains(picker, '("custom_battle_scenario_1", [], "Skirmish 1"')
    assert_contains(picker, '("custom_battle_scenario_3", [], "Skirmish 2"')
    assert_contains(picker, '("custom_battle_scenario_4", [], "Siege Defense"')
    assert_contains(picker, '("custom_battle_scenario_5", [], "Skirmish 3"')
    assert_contains(picker, '("custom_battle_scenario_6", [], "Siege Attack"')
    assert '##      ("custom_battle_scenario_2", [], "Siege Attack 1"' not in picker

    assert_contains(source, '"custom_battle_2", mnf_disable_all_keys,')
    assert_contains(source, '(assign, "$g_custom_battle_scene", "scn_quick_battle_1")')
    assert_contains(source, '(assign, "$g_custom_battle_scene", "scn_quick_battle_3")')
    assert_contains(source, '(assign, "$g_custom_battle_scene", "scn_quick_battle_4")')
    assert_contains(source, '(assign, "$g_custom_battle_scene", "scn_quick_battle_5")')
    assert_contains(source, '(assign, "$g_custom_battle_scene", "scn_quick_battle_7")')
    assert_contains(source, '(eq, "$g_custom_battle_scenario", 4)')
    assert_contains(source, '(set_jump_mission, "mt_custom_battle_5")')
    assert_contains(source, '(jump_to_scene, "$g_custom_battle_scene")')

    assert '##       (assign, "$g_custom_battle_scene", "scn_quick_battle_6")' not in source

    print("test_custom_battle_menu_static: OK")


if __name__ == "__main__":
    main()
