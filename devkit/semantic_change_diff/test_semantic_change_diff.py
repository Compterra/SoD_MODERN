#!/usr/bin/env python3
"""Deterministic pure-diff and live-snapshot checks."""

from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.semantic_change_diff import semantic_change_diff as semantic


def fixture_snapshot() -> dict:
    return {
        "schema": semantic.SCHEMA,
        "created_at_utc": "2026-01-01T00:00:00Z",
        "dialogue_precedence": {"groups": {"trp::start": [{"route_id": "r1", "fingerprint": "a"}]}},
        "state_writers": {"resources": {"party_slot:p:slot": [{"writer_id": "w1", "fingerprint": "a"}]}},
        "string_sinks": {"sinks": {"sink": {"fingerprint": "a"}}},
        "generated_ids": {"tables": {"compile/ids/ID_scripts.py": {"script_x": 1}}},
        "trigger_effects": {"triggers": {"trigger:x": {"fingerprint": "a"}}},
        "exports": {"files": {"strings.txt": {"sha256": "a"}}},
    }


def test_cross_surface_diff() -> None:
    before = fixture_snapshot()
    after = copy.deepcopy(before)
    after["dialogue_precedence"]["groups"]["trp::start"].append({"route_id": "r2", "fingerprint": "b"})
    after["state_writers"]["resources"]["party_slot:p:slot"][0]["fingerprint"] = "b"
    after["string_sinks"]["sinks"]["sink"]["fingerprint"] = "b"
    after["generated_ids"]["tables"]["compile/ids/ID_scripts.py"]["script_x"] = 2
    after["trigger_effects"]["triggers"]["trigger:x"]["fingerprint"] = "b"
    after["exports"]["files"]["strings.txt"]["sha256"] = "b"
    payload = semantic.semantic_diff(before, after)
    assert payload["summary"]["risk_level"] == "critical"
    assert payload["summary"]["surface_change_counts"]["dialogue_precedence"] == 1
    assert payload["summary"]["surface_change_counts"]["generated_ids"] == 1


def test_workspace_snapshot() -> None:
    snapshot = semantic.build_snapshot(ROOT)
    assert snapshot["dialogue_precedence"]["group_count"] > 100
    assert snapshot["state_writers"]["resource_count"] > 100
    assert snapshot["string_sinks"]["sink_count"] > 100


def main() -> int:
    test_cross_surface_diff()
    test_workspace_snapshot()
    print("[semantic_change_diff] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
