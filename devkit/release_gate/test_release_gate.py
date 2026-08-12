"""Focused fixture tests for the strict read-only release gate."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.release_gate import release_gate as gate


def approved_finding(rule: dict[str, object], suffix: int) -> dict[str, object]:
    signature = dict(rule["signature"])
    return {
        "id": f"fixture:{rule['id']}:{suffix}",
        "severity": "warning",
        "code": signature["code"],
        "category": signature["category"],
        "sink_kind": signature["sink_kind"],
        "context": signature["context"],
        "register": signature["register"],
        "compile_path": "compile/fixture.py",
        "compile_line": suffix,
        "source": {"path": signature["source_path"]},
        "message": "Fixture intentional blank text sink.",
    }


def clean_string_report(contract: dict[str, object]) -> dict[str, object]:
    findings = []
    for rule in contract["rules"]:
        for occurrence in range(rule["expected_count"]):
            findings.append(approved_finding(rule, occurrence + 1))
    return {
        "sink_findings": findings,
        "writer_contract_findings": [],
        "module_errors": [],
    }


def clean_parity_report() -> dict[str, object]:
    files = [
        {"filename": filename, "status": "match", "normalized_text_match": True}
        for filename in gate.text_export_parity.ALL_GENERATED_EXPORTS
    ]
    clean_stage = {"passed": True, "exit_code": 0, "output": "", "diagnostics": {"warning_count": 0, "error_count": 0, "items": [], "truncated": False}}
    return {
        "scope": {"source_build": True, "comparison_scope": "all"},
        "safety": {"live_workspace_unchanged": True},
        "summary": {
            "state": "source_to_export_parity",
            "checked_file_count": len(files),
            "matched_file_count": len(files),
            "mismatch_file_count": 0,
            "source_stale_area_count": 0,
        },
        "source_to_compile": {
            "performed": True,
            "builder_results": [{**clean_stage, "builder": name} for name in gate.text_export_parity.SOURCE_BUILDER_ORDER],
            "staged_generated_changes": {"changed_count": 0},
        },
        "compile_to_export": {
            "processor_results": [{**clean_stage, "processor": name} for name in gate.text_export_parity.PROCESSOR_ORDER],
            "files": files,
        },
    }


def clean_dialogue_index() -> SimpleNamespace:
    return SimpleNamespace(findings=(), inventory=SimpleNamespace(source_is_newer=False))


def clean_order_report() -> dict[str, object]:
    return {
        "blocker_count": 0,
        "contracts": {"summary": {"failed_contract_count": 0}},
        "generated_order_parity": {"mismatch_count": 0},
        "dialogue_order_hazards": {"hazard_count": 0},
    }


def run_fixture(*, parity: dict[str, object] | None = None, strings: dict[str, object] | None = None) -> dict[str, object]:
    contract = gate.load_approval_contract(REPO_ROOT)
    with (
        patch.object(gate.text_export_parity, "build_export_parity_report", return_value=parity or clean_parity_report()),
        patch.object(gate.string_integrity, "build_integrity_report", return_value=strings or clean_string_report(contract)),
        patch.object(gate.dialogue_model_checker, "build_dialogue_model", return_value=clean_dialogue_index()),
        patch.object(gate.order_control, "build_order_control", return_value=object()),
        patch.object(gate.order_control, "order_verify", return_value=clean_order_report()),
    ):
        return gate.run_release_gate(REPO_ROOT, timeout_seconds=10, limit=50)


def check(report: dict[str, object], check_id: str) -> dict[str, object]:
    for item in report["checks"]:
        if item["id"] == check_id:
            return item
    raise AssertionError(f"Missing check {check_id}")


def test_exact_approval_baseline_passes() -> None:
    report = run_fixture()
    assert report["state"] == "passed", report
    assert report["summary"]["passed_check_count"] == 5
    assert report["approval_contract"]["expected_approved_finding_count"] == 33


def test_extra_matching_blank_sink_blocks_count_drift() -> None:
    contract = gate.load_approval_contract(REPO_ROOT)
    strings = clean_string_report(contract)
    strings["sink_findings"].append(approved_finding(contract["rules"][0], 99))

    report = run_fixture(strings=strings)
    assert report["state"] == "blocked"
    string_check = check(report, "string_integrity_and_approved_blanks")
    assert string_check["state"] == "blocked"
    assert string_check["evidence"]["count_drift_count"] == 1


def test_export_mismatch_blocks_parity() -> None:
    parity = clean_parity_report()
    parity["summary"].update({"state": "mismatch", "matched_file_count": 29, "mismatch_file_count": 1})
    parity["compile_to_export"]["files"][0].update({"status": "mismatch", "normalized_text_match": False})

    report = run_fixture(parity=parity)
    assert report["state"] == "blocked"
    assert check(report, "source_generated_export_parity")["state"] == "blocked"


def test_staged_warning_blocks_compiler_check() -> None:
    parity = clean_parity_report()
    parity["source_to_compile"]["builder_results"][0]["diagnostics"] = {
        "warning_count": 1,
        "error_count": 0,
        "items": [{"severity": "warning", "line": "WARNING: fixture compiler warning"}],
        "truncated": False,
    }

    report = run_fixture(parity=parity)
    assert report["state"] == "blocked"
    assert check(report, "staged_compiler_diagnostics")["state"] == "blocked"


if __name__ == "__main__":
    test_exact_approval_baseline_passes()
    test_extra_matching_blank_sink_blocks_count_drift()
    test_export_mismatch_blocks_parity()
    test_staged_warning_blocks_compiler_check()
    print("test_release_gate: OK")
