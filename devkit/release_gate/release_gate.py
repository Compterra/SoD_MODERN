#!/usr/bin/env python3
"""Strict, read-only source/export release preflight for SoD Modern.

This is intentionally a fixed aggregation rather than an arbitrary command
runner.  It stages source assembly and the legacy processors through the
existing parity tool, then combines exact string, dialogue, and order evidence
into one machine-readable release decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.dialogue_model_checker import dialogue_model_checker  # noqa: E402
from devkit.order_control import order_control  # noqa: E402
from devkit.rgl_log_sentinel import rgl_log_sentinel  # noqa: E402
from devkit.string_integrity import string_integrity  # noqa: E402
from devkit.text_export_parity import text_export_parity  # noqa: E402


RELEASE_GATE_VERSION = "1.1.0"
APPROVAL_CONTRACT_RELATIVE = Path("devkit/release_gate/contracts/approved-string-clear-sinks.v1.json")
APPROVAL_CONTRACT_VERSION = "devkit.release-gate.approved-string-clear-sinks.v1"
APPROVAL_SIGNATURE_FIELDS = (
    "code",
    "category",
    "sink_kind",
    "context",
    "register",
    "source_path",
)
STAGE_DIAGNOSTIC_RE = re.compile(r"(?im)^\s*(?:\[[^\]\r\n]+\]\s*)?(WARNING|ERROR)\s*:")
MAX_LIMIT = 200
MAX_TIMEOUT_SECONDS = 300


class ReleaseGateError(RuntimeError):
    """The strict release gate could not establish required local evidence."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_int(value: Any, *, name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise ReleaseGateError(f"{name} must be an integer from {minimum} through {maximum}.")
    return value


def compact(value: Any, *, maximum: int = 400) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ")
    return text if len(text) <= maximum else text[: maximum - 3] + "..."


def bounded_rows(rows: Sequence[Mapping[str, Any]], limit: int) -> tuple[list[dict[str, Any]], bool]:
    payload = [dict(row) for row in rows[:limit]]
    return payload, len(rows) > len(payload)


def approval_contract_path(root: Path) -> Path:
    return (root / APPROVAL_CONTRACT_RELATIVE).resolve()


def load_approval_contract(root: Path) -> dict[str, Any]:
    """Load the exact intentional-blank baseline with strict shape checks."""

    path = approval_contract_path(root)
    if not path.is_file():
        raise ReleaseGateError(f"Required string-clear approval contract is absent: {project_relative(path, root)}")
    try:
        raw = path.read_bytes()
        contract = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseGateError(f"Could not read approval contract {project_relative(path, root)}: {error}") from error
    if not isinstance(contract, dict) or contract.get("contract_version") != APPROVAL_CONTRACT_VERSION:
        raise ReleaseGateError(f"Approval contract must declare {APPROVAL_CONTRACT_VERSION}.")
    rules = contract.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ReleaseGateError("Approval contract must contain a non-empty rules array.")

    normalized_rules: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_signatures: set[tuple[str, ...]] = set()
    for position, raw_rule in enumerate(rules, start=1):
        if not isinstance(raw_rule, dict):
            raise ReleaseGateError(f"Approval rule {position} must be an object.")
        rule_id = raw_rule.get("id")
        reason = raw_rule.get("reason")
        expected_count = raw_rule.get("expected_count")
        signature = raw_rule.get("signature")
        if not isinstance(rule_id, str) or not rule_id.strip() or len(rule_id) > 160:
            raise ReleaseGateError(f"Approval rule {position} has an invalid id.")
        if rule_id in seen_ids:
            raise ReleaseGateError(f"Approval contract contains duplicate rule id: {rule_id}.")
        if not isinstance(reason, str) or not reason.strip() or len(reason) > 1_000:
            raise ReleaseGateError(f"Approval rule {rule_id} needs a concise non-empty reason.")
        if isinstance(expected_count, bool) or not isinstance(expected_count, int) or not 1 <= expected_count <= 10_000:
            raise ReleaseGateError(f"Approval rule {rule_id} expected_count must be an integer from 1 through 10000.")
        if not isinstance(signature, dict) or set(signature) != set(APPROVAL_SIGNATURE_FIELDS):
            raise ReleaseGateError(
                f"Approval rule {rule_id} signature must contain exactly: {', '.join(APPROVAL_SIGNATURE_FIELDS)}."
            )
        normalized_signature: dict[str, str] = {}
        for field in APPROVAL_SIGNATURE_FIELDS:
            value = signature[field]
            if not isinstance(value, str) or not value.strip() or len(value) > 500:
                raise ReleaseGateError(f"Approval rule {rule_id} has an invalid {field} signature value.")
            normalized_signature[field] = value.replace("\\", "/") if field == "source_path" else value
        signature_key = tuple(normalized_signature[field] for field in APPROVAL_SIGNATURE_FIELDS)
        if signature_key in seen_signatures:
            raise ReleaseGateError(f"Approval contract has duplicate signature coverage at rule {rule_id}.")
        seen_ids.add(rule_id)
        seen_signatures.add(signature_key)
        normalized_rules.append(
            {
                "id": rule_id,
                "reason": reason,
                "expected_count": expected_count,
                "signature": normalized_signature,
                "signature_key": signature_key,
            }
        )
    return {
        "path": project_relative(path, root),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "contract_version": APPROVAL_CONTRACT_VERSION,
        "rules": normalized_rules,
    }


def finding_signature(finding: Mapping[str, Any]) -> tuple[str, ...]:
    source = finding.get("source")
    source_path = source.get("path", "") if isinstance(source, Mapping) else ""
    values = {
        "code": finding.get("code", ""),
        "category": finding.get("category", ""),
        "sink_kind": finding.get("sink_kind", ""),
        "context": finding.get("context", ""),
        "register": finding.get("register", ""),
        "source_path": source_path,
    }
    return tuple(str(values[field]).replace("\\", "/") for field in APPROVAL_SIGNATURE_FIELDS)


def finding_evidence(finding: Mapping[str, Any]) -> dict[str, Any]:
    source = finding.get("source") if isinstance(finding.get("source"), Mapping) else {}
    return {
        "id": finding.get("id"),
        "severity": finding.get("severity"),
        "code": finding.get("code"),
        "category": finding.get("category"),
        "register": finding.get("register"),
        "sink_kind": finding.get("sink_kind"),
        "context": finding.get("context"),
        "compile_path": finding.get("compile_path"),
        "compile_line": finding.get("compile_line"),
        "source_path": source.get("path"),
        "message": compact(finding.get("message", "")),
    }


def string_clear_assessment(report: Mapping[str, Any], approval: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    """Apply exact-count approval rules only to analyzed visible text sinks."""

    rules = list(approval["rules"])
    rules_by_signature = {rule["signature_key"]: rule for rule in rules}
    observed = Counter()
    unexpected: list[dict[str, Any]] = []
    sink_total = 0
    writer_total = 0

    for finding in report.get("sink_findings", []):
        if not isinstance(finding, Mapping) or finding.get("severity") not in {"warning", "error"}:
            continue
        sink_total += 1
        rule = rules_by_signature.get(finding_signature(finding))
        if rule is None:
            unexpected.append({"kind": "sink", **finding_evidence(finding)})
        else:
            observed[rule["id"]] += 1

    # Writer-contract findings have a different proof shape and are not
    # eligible for a blank-text sink approval.  A new warning here needs an
    # explicit technical review rather than silently inheriting a UI baseline.
    for finding in report.get("writer_contract_findings", []):
        if not isinstance(finding, Mapping) or finding.get("severity") not in {"warning", "error"}:
            continue
        writer_total += 1
        unexpected.append({"kind": "writer_contract", **finding_evidence(finding)})

    rule_rows: list[dict[str, Any]] = []
    count_drift: list[dict[str, Any]] = []
    for rule in rules:
        actual = observed[rule["id"]]
        row = {
            "id": rule["id"],
            "reason": rule["reason"],
            "expected_count": rule["expected_count"],
            "observed_count": actual,
            "status": "approved" if actual == rule["expected_count"] else "count_drift",
            "signature": rule["signature"],
        }
        rule_rows.append(row)
        if actual != rule["expected_count"]:
            count_drift.append(row)

    unexpected_rows, unexpected_truncated = bounded_rows(unexpected, limit)
    drift_rows, drift_truncated = bounded_rows(count_drift, limit)
    return {
        "passed": not unexpected and not count_drift and not report.get("module_errors"),
        "sink_warning_or_error_count": sink_total,
        "writer_warning_or_error_count": writer_total,
        "approved_warning_or_error_count": sum(observed.values()),
        "unexpected_count": len(unexpected),
        "unexpected": unexpected_rows,
        "unexpected_truncated": unexpected_truncated,
        "count_drift_count": len(count_drift),
        "count_drift": drift_rows,
        "count_drift_truncated": drift_truncated,
        "module_error_count": len(report.get("module_errors", [])),
        "module_errors": list(report.get("module_errors", []))[:limit],
        "module_errors_truncated": len(report.get("module_errors", [])) > limit,
        "rules": rule_rows,
    }


def stage_diagnostic_assessment(parity_report: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    """Aggregate bounded builder/processor command outcomes and diagnostics."""

    source_to_compile = parity_report.get("source_to_compile", {})
    compile_to_export = parity_report.get("compile_to_export", {})
    stage_rows: list[tuple[str, Mapping[str, Any]]] = []
    if isinstance(source_to_compile, Mapping):
        stage_rows.extend(("source_builder", row) for row in source_to_compile.get("builder_results", []) if isinstance(row, Mapping))
    if isinstance(compile_to_export, Mapping):
        stage_rows.extend(("legacy_processor", row) for row in compile_to_export.get("processor_results", []) if isinstance(row, Mapping))

    failed: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    warning_count = 0
    error_count = 0
    for phase, row in stage_rows:
        command = str(row.get("builder") or row.get("processor") or row.get("path") or "unknown")
        if row.get("passed") is not True:
            failed.append({"phase": phase, "command": command, "exit_code": row.get("exit_code"), "output": compact(row.get("output", ""), maximum=800)})
        diagnostic_summary = row.get("diagnostics")
        if isinstance(diagnostic_summary, Mapping):
            row_warnings = int(diagnostic_summary.get("warning_count", 0) or 0)
            row_errors = int(diagnostic_summary.get("error_count", 0) or 0)
            item_rows = diagnostic_summary.get("items", [])
            items = item_rows if isinstance(item_rows, list) else []
            for item in items:
                if isinstance(item, Mapping):
                    diagnostics.append({
                        "phase": phase,
                        "command": command,
                        "severity": item.get("severity"),
                        "line": compact(item.get("line", ""), maximum=500),
                    })
        else:
            row_warnings = 0
            row_errors = 0
            for line in str(row.get("output", "")).splitlines():
                match = STAGE_DIAGNOSTIC_RE.match(line)
                if match is None:
                    continue
                severity = match.group(1).lower()
                if severity == "warning":
                    row_warnings += 1
                else:
                    row_errors += 1
                diagnostics.append({"phase": phase, "command": command, "severity": severity, "line": compact(line, maximum=500)})
        warning_count += row_warnings
        error_count += row_errors

    diagnostic_rows, diagnostic_truncated = bounded_rows(diagnostics, limit)
    failed_rows, failed_truncated = bounded_rows(failed, limit)
    expected_builder_count = len(text_export_parity.SOURCE_BUILDER_ORDER)
    expected_processor_count = len(text_export_parity.PROCESSOR_ORDER)
    actual_builders = len(source_to_compile.get("builder_results", [])) if isinstance(source_to_compile, Mapping) else 0
    actual_processors = len(compile_to_export.get("processor_results", [])) if isinstance(compile_to_export, Mapping) else 0
    performed_source_build = bool(source_to_compile.get("performed")) if isinstance(source_to_compile, Mapping) else False
    completeness_errors: list[str] = []
    if not performed_source_build:
        completeness_errors.append("The parity run did not perform a staged source build.")
    if actual_builders != expected_builder_count:
        completeness_errors.append(f"Expected {expected_builder_count} staged source builders but observed {actual_builders}.")
    if actual_processors != expected_processor_count:
        completeness_errors.append(f"Expected {expected_processor_count} staged legacy processors but observed {actual_processors}.")
    return {
        "passed": not failed and not warning_count and not error_count and not completeness_errors,
        "stage_count": len(stage_rows),
        "source_builder_count": actual_builders,
        "legacy_processor_count": actual_processors,
        "failed_command_count": len(failed),
        "failed_commands": failed_rows,
        "failed_commands_truncated": failed_truncated,
        "warning_count": warning_count,
        "error_count": error_count,
        "diagnostics": diagnostic_rows,
        "diagnostics_truncated": diagnostic_truncated,
        "completeness_errors": completeness_errors,
    }


def parity_assessment(parity_report: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    """Require exact staged source/generated/all-export parity evidence."""

    scope = parity_report.get("scope", {})
    safety = parity_report.get("safety", {})
    summary = parity_report.get("summary", {})
    source_to_compile = parity_report.get("source_to_compile", {})
    compile_to_export = parity_report.get("compile_to_export", {})
    scope_data = scope if isinstance(scope, Mapping) else {}
    safety_data = safety if isinstance(safety, Mapping) else {}
    summary_data = summary if isinstance(summary, Mapping) else {}
    expected_exports = len(text_export_parity.ALL_GENERATED_EXPORTS)
    rows = compile_to_export.get("files", []) if isinstance(compile_to_export, Mapping) else []
    row_by_name = {row.get("filename"): row for row in rows if isinstance(row, Mapping)}
    required_text_rows = []
    blockers: list[str] = []

    if scope_data.get("source_build") is not True:
        blockers.append("Parity evidence did not use staged source assembly.")
    if scope_data.get("comparison_scope") != "all":
        blockers.append("Parity evidence did not cover every generated export.")
    if summary_data.get("state") != "source_to_export_parity":
        blockers.append(f"Parity state is {summary_data.get('state')!r}, not source_to_export_parity.")
    if summary_data.get("checked_file_count") != expected_exports:
        blockers.append(f"Expected {expected_exports} checked exports but observed {summary_data.get('checked_file_count')}.")
    if summary_data.get("matched_file_count") != expected_exports or summary_data.get("mismatch_file_count") != 0:
        blockers.append("Not every staged export matches the live export.")
    if safety_data.get("live_workspace_unchanged") is not True:
        blockers.append("Parity staging did not prove that the live compile/export surface remained unchanged.")
    changes = source_to_compile.get("staged_generated_changes") if isinstance(source_to_compile, Mapping) else None
    changed_count = changes.get("changed_count") if isinstance(changes, Mapping) else None
    if changed_count != 0:
        blockers.append(f"Staged source assembly differs from live generated modules ({changed_count} changed modules).")
    stale_count = summary_data.get("source_stale_area_count")
    if stale_count != 0:
        blockers.append(f"Source freshness reports {stale_count} newer modular source areas.")
    for filename in ("strings.txt", "quick_strings.txt"):
        row = row_by_name.get(filename)
        status = row.get("status") if isinstance(row, Mapping) else None
        normalized_match = row.get("normalized_text_match") if isinstance(row, Mapping) else None
        required_text_rows.append({"filename": filename, "status": status, "normalized_text_match": normalized_match})
        if not isinstance(row, Mapping) or normalized_match is not True:
            blockers.append(f"{filename} did not prove normalized staged/export parity.")
    returned_blockers, blockers_truncated = bounded_rows([{"message": item} for item in blockers], limit)
    return {
        "passed": not blockers,
        "expected_export_count": expected_exports,
        "summary": dict(summary_data),
        "safety": {"live_workspace_unchanged": safety_data.get("live_workspace_unchanged")},
        "staged_generated_change_count": changed_count,
        "required_text_exports": required_text_rows,
        "blockers": returned_blockers,
        "blockers_truncated": blockers_truncated,
    }


def dialogue_assessment(index: Any, *, limit: int) -> dict[str, Any]:
    findings = list(getattr(index, "findings", ()))
    errors = [finding for finding in findings if isinstance(finding, Mapping) and finding.get("severity") == "error"]
    error_rows, error_truncated = bounded_rows(errors, limit)
    inventory = getattr(index, "inventory", None)
    source_is_newer = getattr(inventory, "source_is_newer", None)
    blockers: list[dict[str, Any]] = []
    if source_is_newer is True:
        blockers.append({"message": "Generated dialogue is older than its canonical dialogue input."})
    blockers.extend({"finding": row} for row in error_rows)
    return {
        "passed": not errors and source_is_newer is not True,
        "finding_count": len(findings),
        "error_count": len(errors),
        "errors": error_rows,
        "errors_truncated": error_truncated,
        "source_is_newer": source_is_newer,
        "blockers": blockers[:limit],
        "blockers_truncated": len(blockers) > limit,
    }


def order_assessment(verification: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    contracts = verification.get("contracts", {})
    contract_summary = contracts.get("summary", {}) if isinstance(contracts, Mapping) else {}
    generated = verification.get("generated_order_parity", {})
    hazards = verification.get("dialogue_order_hazards", {})
    blockers: list[str] = []
    if verification.get("blocker_count") != 0:
        blockers.append(f"Order Control reports {verification.get('blocker_count')} active blocker(s).")
    if contract_summary.get("failed_contract_count") != 0:
        blockers.append(f"Order Control reports {contract_summary.get('failed_contract_count')} failed contract(s).")
    if not isinstance(generated, Mapping) or generated.get("mismatch_count") != 0:
        blockers.append(f"Generated-order parity reports {generated.get('mismatch_count') if isinstance(generated, Mapping) else None} mismatch(es).")
    if not isinstance(hazards, Mapping) or hazards.get("hazard_count") != 0:
        blockers.append(f"Dialogue-order review reports {hazards.get('hazard_count') if isinstance(hazards, Mapping) else None} hazard(s).")
    returned_blockers, blockers_truncated = bounded_rows([{"message": item} for item in blockers], limit)
    return {
        "passed": not blockers,
        "blocker_count": verification.get("blocker_count"),
        "failed_contract_count": contract_summary.get("failed_contract_count"),
        "generated_order_mismatch_count": generated.get("mismatch_count") if isinstance(generated, Mapping) else None,
        "dialogue_order_hazard_count": hazards.get("hazard_count") if isinstance(hazards, Mapping) else None,
        "blockers": returned_blockers,
        "blockers_truncated": blockers_truncated,
    }


def engine_callback_assessment(report: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    """Normalize protected dynamic-party callback evidence for the release gate."""

    findings = [item for item in report.get("findings", []) if isinstance(item, Mapping)]
    rows, truncated = bounded_rows(findings, limit)
    passed = report.get("passed") is True and not findings
    return {
        "passed": passed,
        "contract_version": report.get("contract_version"),
        "contract_count": report.get("contract_count"),
        "failed_contract_count": report.get("failed_contract_count"),
        "finding_count": len(findings),
        "findings": rows,
        "findings_truncated": truncated,
    }


def check_payload(check_id: str, title: str, passed: bool, summary: str, evidence: Mapping[str, Any], blockers: Sequence[Mapping[str, Any]] = ()) -> dict[str, Any]:
    return {
        "id": check_id,
        "title": title,
        "state": "passed" if passed else "blocked",
        "summary": summary,
        "evidence": dict(evidence),
        "blocking_findings": [dict(blocker) for blocker in blockers],
    }


def run_release_gate(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    timeout_seconds: int = 120,
    limit: int = 30,
) -> dict[str, Any]:
    """Run the fixed all-layer release preflight without writing the workspace."""

    timeout = require_int(timeout_seconds, name="timeout_seconds", minimum=10, maximum=MAX_TIMEOUT_SECONDS)
    maximum = require_int(limit, name="limit", minimum=1, maximum=MAX_LIMIT)
    root = root.resolve()
    approval = load_approval_contract(root)
    checks: list[dict[str, Any]] = []

    try:
        parity_report = text_export_parity.build_export_parity_report(
            root,
            source_build=True,
            scope="all",
            max_diffs=maximum,
            timeout_seconds=timeout,
        )
        parity = parity_assessment(parity_report, limit=maximum)
        checks.append(
            check_payload(
                "source_generated_export_parity",
                "Source, generated-module, and export parity",
                parity["passed"],
                "All 30 staged generated exports, including strings and quick strings, must match the live export while staged generated modules match live compile inputs.",
                {key: value for key, value in parity.items() if key not in {"blockers", "blockers_truncated", "passed"}},
                parity["blockers"],
            )
        )
        diagnostics = stage_diagnostic_assessment(parity_report, limit=maximum)
        diagnostic_blockers: list[dict[str, Any]] = [
            *[{"message": item} for item in diagnostics["completeness_errors"]],
            *diagnostics["failed_commands"],
            *diagnostics["diagnostics"],
        ]
        checks.append(
            check_payload(
                "staged_compiler_diagnostics",
                "Staged builder and legacy-processor diagnostics",
                diagnostics["passed"],
                "Every required staged builder and processor must complete without WARNING: or ERROR: diagnostics.",
                {key: value for key, value in diagnostics.items() if key not in {"failed_commands", "failed_commands_truncated", "diagnostics", "diagnostics_truncated", "completeness_errors", "passed"}},
                diagnostic_blockers[:maximum],
            )
        )
    except text_export_parity.TextExportParityError as error:
        checks.extend(
            [
                check_payload(
                    "source_generated_export_parity",
                    "Source, generated-module, and export parity",
                    False,
                    "The isolated staged parity replay could not complete.",
                    {},
                    [{"message": str(error)}],
                ),
                check_payload(
                    "staged_compiler_diagnostics",
                    "Staged builder and legacy-processor diagnostics",
                    False,
                    "No trustworthy staged compiler-diagnostic result exists because parity staging failed.",
                    {},
                    [{"message": str(error)}],
                ),
            ]
        )

    try:
        string_report = string_integrity.build_integrity_report(root)
        strings = string_clear_assessment(string_report, approval, limit=maximum)
        string_blockers: list[dict[str, Any]] = [
            *[{"module_error": item} for item in strings["module_errors"]],
            *strings["count_drift"],
            *strings["unexpected"],
        ]
        checks.append(
            check_payload(
                "string_integrity_and_approved_blanks",
                "String integrity and exact intentional-blank baseline",
                strings["passed"],
                "Only the checked-in exact intentional blank sink signatures and counts are allowed; all other warning/error string findings block release.",
                {
                    key: value
                    for key, value in strings.items()
                    if key not in {"unexpected", "unexpected_truncated", "count_drift", "count_drift_truncated", "module_errors", "module_errors_truncated", "rules", "passed"}
                } | {"approval_rule_count": len(strings["rules"]), "approved_rules": strings["rules"]},
                string_blockers[:maximum],
            )
        )
    except string_integrity.StringIntegrityError as error:
        checks.append(
            check_payload(
                "string_integrity_and_approved_blanks",
                "String integrity and exact intentional-blank baseline",
                False,
                "String integrity analysis could not complete.",
                {},
                [{"message": str(error)}],
            )
        )

    try:
        dialogue_index = dialogue_model_checker.build_dialogue_model(root)
        dialogue_result = dialogue_assessment(dialogue_index, limit=maximum)
        checks.append(
            check_payload(
                "dialogue_model",
                "Dialogue reachability model",
                dialogue_result["passed"],
                "The branch-free dialogue model must contain no hard error finding and use current compiled dialogue input.",
                {key: value for key, value in dialogue_result.items() if key not in {"errors", "errors_truncated", "blockers", "blockers_truncated", "passed"}},
                dialogue_result["blockers"],
            )
        )
    except dialogue_model_checker.DialogueModelError as error:
        checks.append(
            check_payload(
                "dialogue_model",
                "Dialogue reachability model",
                False,
                "Dialogue model analysis could not complete.",
                {},
                [{"message": str(error)}],
            )
        )

    try:
        order_index = order_control.build_order_control(root)
        order_result = order_assessment(order_control.order_verify(order_index, limit=maximum), limit=maximum)
        checks.append(
            check_payload(
                "order_and_id_contracts",
                "Order, generated-ID, and dialogue-precedence contracts",
                order_result["passed"],
                "No active order contract failure, source/generated ordering mismatch, or static dialogue-order hazard is permitted.",
                {key: value for key, value in order_result.items() if key not in {"blockers", "blockers_truncated", "passed"}},
                order_result["blockers"],
            )
        )
    except order_control.OrderControlError as error:
        checks.append(
            check_payload(
                "order_and_id_contracts",
                "Order, generated-ID, and dialogue-precedence contracts",
                False,
                "Order-control analysis could not complete.",
                {},
                [{"message": str(error)}],
            )
        )

    try:
        callback_report = rgl_log_sentinel.engine_callback_contract_report(root, limit=maximum)
        callback_result = engine_callback_assessment(callback_report, limit=maximum)
        checks.append(
            check_payload(
                "engine_callback_party_handle_contracts",
                "Engine callback dynamic-party handle contracts",
                callback_result["passed"],
                "Protected engine callbacks must validate dynamic party handles before any party/faction read and end stale invocations safely.",
                {
                    key: value
                    for key, value in callback_result.items()
                    if key not in {"findings", "findings_truncated", "passed"}
                },
                callback_result["findings"],
            )
        )
    except rgl_log_sentinel.RglLogSentinelError as error:
        checks.append(
            check_payload(
                "engine_callback_party_handle_contracts",
                "Engine callback dynamic-party handle contracts",
                False,
                "Engine callback party-handle contract analysis could not complete.",
                {},
                [{"message": str(error)}],
            )
        )

    blocked_checks = [check for check in checks if check["state"] != "passed"]
    blocker_count = sum(len(check["blocking_findings"]) for check in blocked_checks)
    state = "passed" if not blocked_checks else "blocked"
    warnings = [] if state == "passed" else ["Strict release gate is blocked; inspect the exact check evidence before changing source or refreshing an approval baseline."]
    return {
        "release_gate_version": f"devkit.release-gate.v{RELEASE_GATE_VERSION}",
        "generated_at_utc": utc_now(),
        "state": state,
        "scope": {
            "repo_root": str(root),
            "read_only": True,
            "staged_source_build": True,
            "comparison_scope": "all",
            "required_generated_export_count": len(text_export_parity.ALL_GENERATED_EXPORTS),
        },
        "approval_contract": {
            "path": approval["path"],
            "sha256": approval["sha256"],
            "contract_version": approval["contract_version"],
            "rule_count": len(approval["rules"]),
            "expected_approved_finding_count": sum(rule["expected_count"] for rule in approval["rules"]),
        },
        "summary": {
            "check_count": len(checks),
            "passed_check_count": len(checks) - len(blocked_checks),
            "blocked_check_count": len(blocked_checks),
            "blocking_finding_count": blocker_count,
        },
        "checks": checks,
        "evidence_boundary": [
            "The parity replay and all analyses are read-only; no live compile or export file is written.",
            "A passing static gate proves current source/generated/export coherence and declared contracts, not every dynamic engine state or in-game presentation path.",
            "The approved blank baseline is exact evidence, not a blanket suppression; any changed signature or count requires a reviewed contract edit.",
        ],
        "warnings": warnings,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# SoD Modern Strict Release Gate",
        "",
        f"State: **{report['state']}**.",
        "",
        f"- Checks: {summary['passed_check_count']}/{summary['check_count']} passed.",
        f"- Blocking findings: {summary['blocking_finding_count']}.",
        f"- Approval baseline: {report['approval_contract']['expected_approved_finding_count']} exact intentional blank findings across {report['approval_contract']['rule_count']} rules.",
        "",
        "## Checks",
        "",
    ]
    for check in report["checks"]:
        icon = "PASS" if check["state"] == "passed" else "BLOCKED"
        lines.append(f"- **{icon}** `{check['id']}` — {check['summary']}")
        for blocker in check["blocking_findings"][:10]:
            message = blocker.get("message") or blocker.get("line") or blocker.get("id") or json.dumps(blocker, sort_keys=True)
            lines.append(f"  - {compact(message, maximum=500)}")
    if report.get("warnings"):
        lines.extend(["", "## Warnings", "", *(f"- {warning}" for warning in report["warnings"])])
    return "\n".join(lines) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run strict, read-only source/generated/export release evidence for SoD Modern.")
    parser.add_argument("command", choices=("run",), nargs="?", default="run")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = run_release_gate(args.root, timeout_seconds=args.timeout_seconds, limit=args.limit)
    except ReleaseGateError as error:
        print(f"release_gate: {error}", file=sys.stderr)
        return 2
    if args.format == "markdown":
        sys.stdout.write(render_markdown(report))
    else:
        sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return 0 if report["state"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
