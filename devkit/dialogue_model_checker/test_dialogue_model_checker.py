#!/usr/bin/env python3
"""Deterministic model-checker fixtures independent of live module content."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.dialogue_inspector import dialogue_inspector as inspector
from devkit.dialogue_model_checker import dialogue_model_checker as checker


RAW = """
dialogs = [
  [trp_fixture, 'npc', [(eq, ':mode', 1)], 'early', 'early_state', []],
  [trp_fixture, 'npc', [(eq, ':mode', 1)], 'shadowed', 'shadow_state', []],
  [trp_fixture, 'npc', [(eq, ':broken', 1), (neq, ':broken', 1)], 'broken', 'dead_state', []],
  [trp_fixture, 'fallback', [], 'fallback', 'fallback_state', []],
  [trp_fixture, 'fallback', [(eq, ':mode', 2)], 'after fallback', 'after_state', []],
  [trp_fixture, 'ambiguous', [(ge, ':rank', 2)], 'first', 'first_state', []],
  [trp_fixture, 'ambiguous', [(le, ':rank', 4)], 'second', 'second_state', []],
  [plyr, 'player', [(eq, ':answer', 1)], 'Same answer', 'player_a', []],
  [plyr, 'player', [(eq, ':answer', 1)], 'Same answer', 'player_b', []],
  [trp_fixture, 'dead_state', [(eq, ':x', 1), (neq, ':x', 1)], 'still dead', 'close_window', []],
  [trp_fixture, 'branchy', [(store_random_in_range, ':line', 0, 2), try_begin, (eq, ':line', 0), (str_store_string, s68, '@one'), else_try, (eq, ':line', 1), (str_store_string, s68, '@two'), try_end], '{s68}', 'close_window', []],
  [trp_fixture, 'specific_then_fallback', [(eq, ':mode', 1)], 'specific first', 'specific_state', []],
  [trp_fixture, 'specific_then_fallback', [], 'real fallback', 'fallback_state', []],
  [trp_fixture, 'dynamic_relation', [(eq, '$left_value', '$right_value')], 'dynamic values may match', 'close_window', []],
  [trp_fixture, 'dynamic_slot', [(party_slot_eq, ':party', slot_fixture_value, ':wanted_value')], 'dynamic slot comparison', 'close_window', []],
]
"""


def fixture_index() -> checker.DialogueModelIndex:
    entries = inspector.parse_dialogue_entries(RAW)
    inventory = inspector.DialogueInventory(Path("fixture/module_dialogs.py"), entries, False, None)
    routes = tuple(
        checker.RouteModel(entry=entry, constraints=checker.constraints_for_entry(entry), condition_signature=checker.condition_signature(entry))
        for entry in entries
    )
    findings, statuses = checker.analyze_routes(routes)
    return checker.DialogueModelIndex(ROOT, inventory, routes, findings, statuses, [])


def test_proved_findings() -> None:
    index = fixture_index()
    categories = {item["category"] for item in index.findings}
    assert "route_condition_contradiction" in categories
    assert "npc_route_shadowed_by_precedence" in categories
    assert "npc_route_conditionally_ambiguous" in categories
    assert "player_choice_conditionally_ambiguous" in categories
    assert "input_state_has_no_producer" in categories
    assert "dialogue_state_terminally_dead" in categories
    assert index.route_status[2] == "shadowed_proven"
    assert index.route_status[3] == "unreachable_proven"
    state = checker.state_payload(index, "fallback")
    assert state["groups"][0]["routes"][1]["status"] == "shadowed_proven"
    real_fallback = next(route for route in index.routes if route.entry.text == "real fallback")
    assert index.route_status[real_fallback.entry.index] == "reachable_not_proven"


def test_branching_condition_blocks_remain_unproven() -> None:
    index = fixture_index()
    branchy = index.routes[10]
    assert branchy.constraints.unsupported
    assert not branchy.constraints.unsatisfiable
    assert index.route_status[11] == "model_boundary_unproven"
    dynamic_routes = [route for route in index.routes if route.entry.start_state in {"dynamic_relation", "dynamic_slot"}]
    assert all(route.constraints.unsupported for route in dynamic_routes)
    assert all(index.route_status[route.entry.index] == "model_boundary_unproven" for route in dynamic_routes)


def test_workspace_model() -> None:
    index = checker.build_dialogue_model(ROOT)
    summary = checker.summary_payload(index, limit=3)
    assert summary["coverage"]["route_count"] > 1_000
    assert summary["coverage"]["state_count"] > 100
    assert summary["coverage"]["route_statuses"]["model_boundary_unproven"] > 0
    errors = [finding for finding in index.findings if finding["severity"] == "error"]
    assert not errors, errors


def main() -> int:
    test_proved_findings()
    test_branching_condition_blocks_remain_unproven()
    test_workspace_model()
    print("[dialogue_model_checker] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
