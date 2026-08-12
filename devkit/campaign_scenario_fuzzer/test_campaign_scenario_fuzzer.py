#!/usr/bin/env python3
"""Deterministic fixture checks for safe campaign scenario fuzzing."""

from __future__ import annotations

import json
import sys
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.campaign_scenario_fuzzer import campaign_scenario_fuzzer as fuzzer


STATE_CONTRACTS = {"contract_version": "devkit.campaign-state-contracts.v1", "contracts": []}


def write_fixture(root: Path) -> tuple[Path, Path]:
    scripts = root / "src" / "scripts"
    triggers = root / "src" / "triggers"
    scripts.mkdir(parents=True)
    triggers.mkdir(parents=True)
    scripts.joinpath("fixture.py").write_text(
        textwrap.dedent(
            """
            SCRIPTS = [
              ("fixture_hold", [
                (store_script_param, ":party", 1),
                (try_begin),
                  (gt, ":party", 0),
                  (party_is_active, ":party"),
                  (party_set_ai_behavior, ":party", ai_bhvr_hold),
                (try_end),
              ]),
              ("fixture_bad", [
                (store_script_param, ":party", 1),
                (party_set_ai_behavior, ":party", ai_bhvr_travel_to_party),
              ]),
            ]
            """
        ),
        encoding="utf-8",
    )
    triggers.joinpath("empty.py").write_text("SIMPLE_TRIGGERS = []\n", encoding="utf-8")
    scenarios = {
        "schema": "devkit.campaign-scenario-fuzzer.v1",
        "scenarios": [
            {
                "id": "hold",
                "entry_script": "script_fixture_hold",
                "parameters": [{"party": "camp"}],
                "state": {"parties": {"camp": {"id": 1, "active": True, "template": "pt_fixture", "ai": {}, "slots": {}}}},
                "fuzz": {"integer_ranges": {"$noise": [0, 5]}},
                "assertions": [{"kind": "party_ai_equals", "party": "camp", "field": "behavior", "equals": "ai_bhvr_hold"}],
            },
            {
                "id": "bad",
                "entry_script": "script_fixture_bad",
                "parameters": [{"party": "camp"}],
                "state": {"parties": {"camp": {"id": 1, "active": True, "template": "pt_fixture", "ai": {}, "slots": {}}}},
                "assertions": [{"kind": "party_ai_equals", "party": "camp", "field": "behavior", "equals": "ai_bhvr_hold"}],
            },
        ],
    }
    scenario_path = root / "scenarios.json"
    contracts_path = root / "contracts.json"
    scenario_path.write_text(json.dumps(scenarios), encoding="utf-8")
    contracts_path.write_text(json.dumps(STATE_CONTRACTS), encoding="utf-8")
    return scenario_path, contracts_path


def test_fixture_runs() -> None:
    with tempfile.TemporaryDirectory(prefix="scenario-fuzzer-") as temporary:
        root = Path(temporary)
        scenarios, contracts = write_fixture(root)
        index = fuzzer.build_scenario_fuzzer(root, scenarios_path=scenarios, state_contracts_path=contracts)
        passed = fuzzer.fuzz_payload(index, "hold", iterations=8, seed=9)
        assert passed["status"] == "passed", passed
        failed = fuzzer.fuzz_payload(index, "bad", iterations=2, seed=9)
        assert failed["status"] == "failed"
        assert failed["first_counterexample"] is not None


def test_workspace_scenario() -> None:
    index = fuzzer.build_scenario_fuzzer(ROOT)
    catalog = fuzzer.scenario_catalog_payload(index, scenario_id="black-khergit-camped-lock")
    assert catalog["scenario_count"] == 1
    result = fuzzer.fuzz_payload(index, "black-khergit-camped-lock", iterations=3, seed=3)
    assert result["status"] == "passed", result


def main() -> int:
    test_fixture_runs()
    test_workspace_scenario()
    print("[campaign_scenario_fuzzer] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
