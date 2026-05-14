from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "other" / "continue_16.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected siege simulation behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")

    assert_contains(source, '"castle_attack_walls_with_allies_simulate", mnf_disable_all_keys')
    assert_contains(source, '(call_script, "script_party_calculate_strength", "p_main_party", 1)')
    assert_contains(source, '(call_script, "script_party_calculate_strength", "p_collective_friends", 0)')
    assert_contains(source, '(call_script, "script_party_calculate_strength", "p_collective_enemy", 0)')
    assert_contains(source, '(inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties")')
    assert_contains(source, '(inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties")')
    assert_contains(source, '(inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties")')
    assert_contains(source, '("continue", [], "Continue...", [(jump_to_menu, "mnu_besiegers_camp_with_allies")])')

    for stale in (
        '##        (assign, reg0, ":player_party_strength")',
        '##        (assign, reg1, ":friend_party_strength")',
        '##        (assign, reg2, ":enemy_party_strength")',
        '##        (assign, reg3, "$g_enemy_party")',
        '##        (assign, reg4, "$g_ally_party")',
        '##        (display_message, "@player_str={reg0} friend_str={reg1} enemy_str={reg2}", debug_color)',
        '##        (display_message, "@enemy_party={reg3} ally_party={reg4}", debug_color)',
    ):
        assert stale not in source, stale

    print("test_siege_simulation_result_static: OK")


if __name__ == "__main__":
    main()
