from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_ai_battle_join_menu_sets_late_join_flag() -> None:
    raw = read("src/menus/encounter/pre_join_help_attackers.py")
    assert raw.count('(assign, "$g_sod_joined_ongoing_ai_battle", 1)') >= 2


def test_lead_charge_applies_and_clears_late_join_pressure() -> None:
    raw = read("src/mission_templates/0010_lead_charge/lead_charge.py")
    assert_contains(raw, 'script_sod_battle_apply_late_join_spawn_pressure')
    assert_contains(raw, 'script_sod_battle_compress_late_join_ai_lines')
    assert_contains(raw, '(1, 0, ti_once, [(eq, "$g_sod_joined_ongoing_ai_battle", 1)]')
    assert_contains(raw, '(5, 0, ti_once, [(eq, "$g_sod_joined_ongoing_ai_battle", 1)]')
    assert_contains(raw, '(assign, "$g_sod_joined_ongoing_ai_battle", 0)')


def test_join_battle_non_mission_paths_clear_late_join_flag() -> None:
    raw = read("src/menus/encounter/join_attack.py")
    assert raw.count('(assign, "$g_sod_joined_ongoing_ai_battle", 0)') >= 2
    assert_contains(raw, '(jump_to_menu, "mnu_join_order_attack")')
    assert_contains(raw, '(leave_encounter)')


def test_spawn_pressure_stages_player_party_as_flanking_arrivals() -> None:
    raw = read("src/scripts/ZE_encounters/sod_battle_apply_late_join_spawn_pressure.py")
    assert_contains(raw, '(eq, "$g_sod_joined_ongoing_ai_battle", 1)')
    assert_contains(raw, '(agent_get_party_id, ":agent_party", ":agent_no")')
    assert_contains(raw, '(eq, ":agent_party", "p_main_party")')
    assert_contains(raw, '(position_move_x, pos1, 2800)')
    assert_contains(raw, '(position_move_x, pos1, -2800)')
    assert_contains(raw, '(position_move_y, pos1, 450)')


def test_compression_moves_ai_battle_parties_toward_measured_midpoint() -> None:
    raw = read("src/scripts/ZE_encounters/sod_battle_apply_late_join_spawn_pressure.py")
    assert_contains(raw, '("sod_battle_compress_late_join_ai_lines"')
    assert_contains(raw, '(try_for_agents, ":agent_no")')
    assert_contains(raw, '(position_get_x, ":agent_x", pos1)')
    assert_contains(raw, '(position_get_y, ":agent_y", pos1)')
    assert_contains(raw, '(get_distance_between_positions, ":ai_line_distance", pos2, pos3)')
    assert_contains(raw, '(gt, ":ai_line_distance", 2400)')
    assert_contains(raw, '(val_div, ":enemy_move_x", 4)')
    assert_contains(raw, '(val_div, ":enemy_move_y", 4)')
    assert_contains(raw, '(this_or_next|eq, ":agent_party", "$g_enemy_party")')
    assert_contains(raw, '(eq, ":agent_party", "$g_ally_party")')
    assert_contains(raw, '(val_add, ":agent_x", ":enemy_move_x")')
    assert_contains(raw, '(val_sub, ":agent_x", ":enemy_move_x")')
    assert_contains(raw, '(agent_set_position, ":agent_no", pos1)')


if __name__ == "__main__":
    test_ai_battle_join_menu_sets_late_join_flag()
    test_lead_charge_applies_and_clears_late_join_pressure()
    test_join_battle_non_mission_paths_clear_late_join_flag()
    test_spawn_pressure_stages_player_party_as_flanking_arrivals()
    test_compression_moves_ai_battle_parties_toward_measured_midpoint()
    print("test_late_join_battle_spawns_static: OK")
