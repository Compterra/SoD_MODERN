# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_duel_trigger_requires_healthy_commanders() -> None:
    raw = read("src/scripts/ZY_helper_scripts/ponavosa_duel_find_commander_pair.py")
    assert raw.count("store_agent_hit_points") >= 3
    assert_contains(raw, "(gt, \":player_hp\", 50)")
    assert_contains(raw, "(gt, \":ally_hp\", 50)")
    assert_contains(raw, "(gt, \":enemy_hp\", 50)")


def test_duel_trigger_uses_organic_no_mans_land_rules() -> None:
    raw = read("src/scripts/ZY_helper_scripts/ponavosa_duel_find_commander_pair.py")
    assert_contains(raw, ":nearby_allies")
    assert_contains(raw, ":nearby_enemy_support")
    assert_contains(raw, "(le, \":nearby_allies\", 5)")
    assert_contains(raw, "(le, \":nearby_enemy_support\", 7)")
    assert_contains(raw, "(is_between, \":dist\", 700, 2201)")


def test_challenge_key_is_separate_from_reinforcements() -> None:
    raw = read("src/mission_templates/_preamble/00_imports.py")
    lead_charge = read("src/mission_templates/0010_lead_charge/lead_charge.py")
    assert_contains(raw, "commander_duel_player_challenge")
    assert_contains(raw, "commander_duel_player_feedback")
    assert_contains(raw, "(key_clicked, key_t)")
    assert_contains(raw, "formations_v =")
    assert_contains(raw, "(key_clicked, key_v)")
    assert_contains(lead_charge, "commander_duel_player_feedback")
    assert "ponavosa_duel_find_commander_pair\", 1),\n        (eq, reg0, 1),\n        (assign, \":allow_reinforcements\", 0)" not in raw


def test_failed_challenges_explain_positioning_rules() -> None:
    raw = read("src/scripts/ZY_helper_scripts/ponavosa_duel_explain_challenge.py")
    assert_contains(raw, "Step out from your line")
    assert_contains(raw, "Move closer to the enemy commander")
    assert_contains(raw, "too battered to answer")
    assert_contains(raw, "still shielded by too many troops")
    assert_contains(raw, "Find open ground between the lines")


def test_duel_aura_has_real_supported_battle_effects() -> None:
    raw = read("src/scripts/ZY_helper_scripts/ponavosa_duel_apply_commander_aura.py")
    assert_contains(raw, "slot_agent_duel_faith_rank")
    assert_contains(raw, "agent_set_speed_limit")
    assert_contains(raw, "agent_ai_set_always_attack_in_melee")
    assert_contains(raw, "agent_set_hit_points")


def test_duel_ui_tracks_layers_and_blessing_pressure() -> None:
    raw = read("src/presentations/0026_ponavosa_commander_duel/ponavosa_commander_duel.py")
    assert_contains(raw, "$g_ponavosa_duel_ally_layer")
    assert_contains(raw, "$g_ponavosa_duel_enemy_layer")
    assert_contains(raw, "$g_ponavosa_duel_blessing")
    assert_contains(raw, "Blessing pressure")


def test_duel_restore_clears_temporary_pressure() -> None:
    raw = read("src/scripts/ZY_helper_scripts/ponavosa_duel_restore.py")
    assert_contains(raw, "agent_ai_set_always_attack_in_melee")
    assert_contains(raw, "slot_agent_duel_pressure")
    assert_contains(raw, "(agent_set_speed_limit, \"$ponavosa_duel_ally_agent\", 60)")
    assert_contains(raw, "(agent_set_speed_limit, \"$ponavosa_duel_enemy_agent\", 60)")


def test_duel_resolution_deepens_routing_shockwave() -> None:
    raw = read("src/scripts/ZY_helper_scripts/ponavosa_duel_resolve.py")
    assert_contains(raw, "Lesser troops start to break")
    assert_contains(raw, "(position_move_y, pos1, -5200)")
    assert_contains(raw, "(agent_set_speed_limit, \":agent_no\", 12)")


if __name__ == "__main__":
    test_duel_trigger_requires_healthy_commanders()
    test_duel_trigger_uses_organic_no_mans_land_rules()
    test_challenge_key_is_separate_from_reinforcements()
    test_failed_challenges_explain_positioning_rules()
    test_duel_aura_has_real_supported_battle_effects()
    test_duel_ui_tracks_layers_and_blessing_pressure()
    test_duel_restore_clears_temporary_pressure()
    test_duel_resolution_deepens_routing_shockwave()
    print("test_commander_duel_static: OK")
