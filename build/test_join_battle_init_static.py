from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "encounter" / "join_attack.py"
INIT_SCRIPT = ROOT / "src" / "scripts" / "ZE_encounters" / "encounter_init_variables.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected join battle behavior: {needle}"


def main() -> None:
    menu = MENU.read_text(encoding="utf-8")
    init_script = INIT_SCRIPT.read_text(encoding="utf-8")

    assert_contains(menu, '"join_battle", mnf_enable_hot_keys')
    assert_contains(menu, '(eq, "$new_encounter", 1)')
    assert_contains(menu, '(assign, "$new_encounter", 0)')
    assert_contains(menu, '(call_script, "script_encounter_init_variables")')
    assert_contains(menu, '("join_attack", [')
    assert_contains(menu, '(call_script, "script_cf_sod_battle_commander_can_start")')
    assert_contains(menu, '(assign, "$g_next_menu", "mnu_join_battle")')

    for live_init in (
        '(assign, "$capture_screen_shown", 0)',
        '(assign, "$loot_screen_shown", 0)',
        '(assign, "$g_battle_result", 0)',
        '(assign, "$cant_leave_encounter", 0)',
        '(assign, "$last_defeated_hero", 0)',
        '(assign, "$last_freed_hero", 0)',
        '(call_script, "script_party_copy", "p_main_party_backup", "p_main_party")',
        '(call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy")',
        '(call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally")',
    ):
        assert_contains(init_script, live_init)
        assert f"##          {live_init}" not in menu, live_init

    print("test_join_battle_init_static: OK")


if __name__ == "__main__":
    main()
