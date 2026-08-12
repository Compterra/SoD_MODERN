"""Fixture tests for the M&B-native CBO-style Workbench workflows."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.module_atlas.test_module_atlas import make_workspace
from devkit.workbench import workbench


CONTRACTS = {
    "schema": "sod-modern.workbench-contract-catalog.v1",
    "version": 1,
    "contracts": [
        {
            "id": "fixture-topology",
            "title": "Fixture topology",
            "system": "fixture",
            "status": "active",
            "purpose": "Proves declarative Workbench rule evaluation.",
            "scenario": "fixture-structure",
            "targets": ["menu:fixture_menu"],
            "static": {
                "rules": [
                    {"id": "areas", "kind": "atlas-area-count", "expected": 8, "label": "All areas"},
                    {"id": "integrity", "kind": "integrity-maximum", "field": "finding_count", "expected": 0, "label": "No direct structural findings"},
                    {"id": "source", "kind": "workspace-path", "path": "src", "label": "Source exists"}
                ]
            },
            "nativeProof": {"policy": "fixture", "detail": "No runtime claim."}
        }
    ]
}

SCENARIOS = {
    "schema": "sod-modern.workbench-scenario-catalog.v1",
    "version": 1,
    "scenarios": [
        {
            "id": "fixture-structure",
            "title": "Fixture structure",
            "category": "fixture",
            "purpose": "Proves only registered scenario steps execute.",
            "evidence_level": "structural",
            "proof_note": "No runtime claim.",
            "targets": ["menu:fixture_menu"],
            "steps": [
                {"kind": "builtin", "action": "module_integrity", "label": "Atlas integrity"},
                {"kind": "python-test", "path": "devkit/fixture_test.py", "label": "Fixture Python test"}
            ]
        }
    ]
}

ORDER_CONTRACTS = {
    "schema": "sod-modern.order-control-contract-catalog.v1",
    "version": 1,
    "contracts": [],
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def make_workbench_config(root: Path) -> None:
    workbench_root = root / "devkit" / "workbench"
    write_json(workbench_root / "contracts" / "manifest.json", CONTRACTS)
    write_json(workbench_root / "scenarios" / "manifest.json", SCENARIOS)
    write_json(root / "devkit" / "order_control" / "contracts" / "manifest.json", ORDER_CONTRACTS)
    for relative in (
        "drafts/.gitignore",
        "reports/.gitignore",
        "contracts/baselines/.gitignore",
    ):
        path = workbench_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("*\n!.gitignore\n", encoding="utf-8")
    fixture_test = root / "devkit" / "fixture_test.py"
    fixture_test.parent.mkdir(parents=True, exist_ok=True)
    fixture_test.write_text("print('fixture scenario: OK')\n", encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="workbench-") as temporary:
        root = Path(temporary)
        make_workspace(root)
        make_workbench_config(root)

        scenarios = workbench.scenario_list(root)
        assert scenarios["summary"]["scenario_count"] == 1
        contracts = workbench.contract_drift(root)
        assert contracts["summary"]["active_blocker_count"] == 0

        index = workbench.module_atlas.build_module_atlas(root)
        menu = workbench.module_atlas.resolve_named_entity(index, "menu", "fixture_menu")
        impact = workbench.workbench_impact(root, target="fixture_menu", limit=5)
        assert impact["target"]["primary_entity_id"] == menu.id
        assert impact["coverage"]["coverage_maturity"] == "static_contract"

        scope = workbench.workbench_scope_check(root, entity_id=menu.id, depth="fast")
        assert scope["passed"] is True
        assert scope["plan"]["source_target_id"] == menu.target_id

        coverage = workbench.workbench_coverage(root, area="menus", limit=10)
        assert coverage["match_count"] == 2
        assert any(entry["coverage_maturity"] == "static_contract" for entry in coverage["entries"])

        text_lint = workbench.workbench_text_lint(root, severity="all", limit=10)
        assert text_lint["summary"]["text_sink_count"] == 0

        order_report = workbench.workbench_order_report(root, limit=10)
        assert order_report["state"] == "structural_order_ready_for_review"
        assert order_report["verification"]["contracts"]["summary"]["active_blocker_count"] == 0

        scenario = workbench.run_registered_scenario(root, scenario_id="fixture-structure", timeout_seconds=30)
        assert scenario["passed"] is True
        assert scenario["passed_step_count"] == 2

        baseline = workbench.contract_baseline(root, label="fixture")
        assert (root / baseline["artifact"]["path"]).is_file()
        draft = workbench.workbench_draft(root, kind="menu", title="Fixture Menu")
        assert draft["draft"]["state"] == "disabled"
        assert (root / draft["artifact"]["path"]).is_file()

    print("test_workbench: OK")


if __name__ == "__main__":
    main()
