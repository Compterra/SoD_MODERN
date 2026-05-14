from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "0000_hardcoded_mb1011" / "custom_battle_2.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected custom battle behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")

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
