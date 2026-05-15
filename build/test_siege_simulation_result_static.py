from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "other" / "continue_16.py"
JOIN_ORDER_MENU = ROOT / "src" / "menus" / "other" / "continue_08.py"
SIEGE_DEFENSE_MENU = ROOT / "src" / "menus" / "other" / "continue_20.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected siege simulation behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")
    join_order = JOIN_ORDER_MENU.read_text(encoding="utf-8")
    siege_defense = SIEGE_DEFENSE_MENU.read_text(encoding="utf-8")

    assert_contains(source, '"castle_attack_walls_with_allies_simulate", mnf_disable_all_keys')
    assert_contains(source, '(call_script, "script_party_calculate_strength", "p_main_party", 1)')
    assert_contains(source, '(call_script, "script_party_calculate_strength", "p_collective_friends", 0)')
    assert_contains(source, '(call_script, "script_party_calculate_strength", "p_collective_enemy", 0)')
    assert_contains(source, '(val_max, ":friend_party_strength", 1)')
    assert_contains(source, '(inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties")')
    assert_contains(source, '(inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties")')
    assert_contains(source, '(inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties")')
    assert_contains(source, '(party_is_active, "$g_enemy_party")')
    assert_contains(source, '(party_is_active, "$g_ally_party")')
    assert_contains(source, '(str_store_string, s10, "@None")')
    assert_contains(source, '(str_store_string, s9, "@None")')
    assert_contains(source, '("continue", [], "Continue...", [(jump_to_menu, "mnu_besiegers_camp_with_allies")])')

    for guarded in (join_order, siege_defense):
        assert_contains(guarded, '(val_max, ":friend_party_strength", 1)')
        assert_contains(guarded, '(party_is_active, "$g_enemy_party")')
        assert_contains(guarded, '(party_is_active, "$g_ally_party")')
        assert_contains(guarded, '(str_store_string, s10, "@None")')
        assert_contains(guarded, '(str_store_string, s9, "@None")')
        assert guarded.index('(party_is_active, "$g_enemy_party")') < guarded.index('(inflict_casualties_to_party_group, "$g_enemy_party"')
        assert guarded.index('(party_is_active, "$g_ally_party")') < guarded.index('(inflict_casualties_to_party_group, "$g_ally_party"')

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
