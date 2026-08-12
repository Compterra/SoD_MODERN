#!/usr/bin/env python3
"""SoD Modern Workbench: fixed, evidence-backed coordination for Codex.

This is the M&B-native counterpart to CBO's successful Workbench pattern. It
does not emulate Thea's XML, C#, combat, or browser tooling. Instead it joins
the source-aware tools already native to this repository into a small set of
bounded workflows:

* compact impact packets rather than a hunt through thousands of fragments;
* fixed validation profiles rather than arbitrary command execution;
* declarative static contracts and registered scenarios;
* coverage maturity and an honest manual-release checklist; and
* disabled DevKit-only authoring drafts.

It is deliberately LLM-first: deterministic JSON and MCP adapters are the
primary API. Nothing here builds the live module, rewrites source implicitly,
or claims that static evidence proves an in-game result.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.change_router import change_router
from devkit.dialogue_inspector import dialogue_inspector
from devkit.module_atlas import module_atlas
from devkit.order_control import order_control
from devkit.string_integrity import string_integrity
from devkit.text_execution_ledger import text_execution_ledger
from devkit.workspace_audit import workspace_audit


WORKBENCH_VERSION = "0.1.0"
MAX_QUERY_LENGTH = 500
MAX_RESULT_LIMIT = 500
MAX_TIMEOUT_SECONDS = 300
VALID_DEPTHS = ("fast", "standard", "deep")
VALID_DRAFT_KINDS = (
    "constant",
    "dialogue",
    "menu",
    "mission",
    "presentation",
    "quest",
    "script",
    "trigger",
)
EVIDENCE_RANK = {
    "source_only": 0,
    "generated_provenance": 1,
    "test_candidate": 2,
    "registered_scenario": 3,
    "static_contract": 4,
}
SEVERITY_RANK = {"clean": 0, "info": 1, "warning": 2, "error": 3}
SAFE_ARTIFACT_ROOTS = ("devkit/output", "devkit/workbench/reports")
SLUG_RE = re.compile(r"[^a-z0-9]+")
_STRING_REPORT_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], dict[str, Any]]] = {}


class WorkbenchError(RuntimeError):
    """A bounded Workbench request cannot be completed safely."""


@dataclass(frozen=True)
class ResolvedWorkbenchTarget:
    kind: str
    query: str
    entity: module_atlas.ModuleEntity | None
    target_id: str | None
    candidates: tuple[module_atlas.ModuleEntity, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def require_text(value: Any, *, name: str, maximum: int = MAX_QUERY_LENGTH) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkbenchError(f"{name} must be a non-empty string.")
    checked = value.strip()
    if len(checked) > maximum:
        raise WorkbenchError(f"{name} must be at most {maximum} characters.")
    return checked


def require_limit(value: Any, *, name: str = "limit", maximum: int = MAX_RESULT_LIMIT) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise WorkbenchError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_depth(value: str) -> str:
    if value not in VALID_DEPTHS:
        raise WorkbenchError("depth must be one of: " + ", ".join(VALID_DEPTHS))
    return value


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def workbench_dir(root: Path) -> Path:
    candidate = root.resolve() / "devkit" / "workbench"
    return candidate if candidate.is_dir() else TOOL_DIR


def string_report_signature(root: Path) -> tuple[tuple[str, int, int], ...]:
    """Cheap freshness signature for generated text-analysis inputs."""

    paths = [
        *sorted((root / "compile").glob("module_*.py"), key=lambda path: path.name.casefold()),
        *[
            root / "_export" / filename
            for filename in ("strings.txt", "quick_strings.txt", "conversation.txt", "dialog_states.txt", "menus.txt", "presentations.txt")
        ],
    ]
    rows = []
    for path in paths:
        if not path.is_file():
            continue
        stat = path.stat()
        rows.append((project_relative(path, root), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def cached_string_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    signature = string_report_signature(root)
    cached = _STRING_REPORT_CACHE.get(root)
    if cached is not None and cached[0] == signature:
        return cached[1]
    report = string_integrity.build_integrity_report(root)
    _STRING_REPORT_CACHE[root] = (signature, report)
    return report


def catalog_path(root: Path, *parts: str) -> Path:
    return workbench_dir(root).joinpath(*parts)


def read_json(path: Path, *, label: str) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise WorkbenchError(f"Could not read {label}: {error}") from error
    if not isinstance(raw, dict):
        raise WorkbenchError(f"{label} must contain a JSON object.")
    return raw


def load_contract_catalog(root: Path) -> dict[str, Any]:
    catalog = read_json(catalog_path(root, "contracts", "manifest.json"), label="Workbench contract catalog")
    if catalog.get("schema") != "sod-modern.workbench-contract-catalog.v1":
        raise WorkbenchError("Unsupported Workbench contract catalog schema.")
    if not isinstance(catalog.get("contracts"), list):
        raise WorkbenchError("Workbench contract catalog contracts must be a list.")
    return catalog


def load_scenario_catalog(root: Path) -> dict[str, Any]:
    catalog = read_json(catalog_path(root, "scenarios", "manifest.json"), label="Workbench scenario catalog")
    if catalog.get("schema") != "sod-modern.workbench-scenario-catalog.v1":
        raise WorkbenchError("Unsupported Workbench scenario catalog schema.")
    if not isinstance(catalog.get("scenarios"), list):
        raise WorkbenchError("Workbench scenario catalog scenarios must be a list.")
    return catalog


def confined_path(root: Path, relative: str, *, label: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise WorkbenchError(f"{label} must be a non-empty workspace-relative path.")
    candidate = (root.resolve() / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise WorkbenchError(f"{label} must stay inside the workspace.") from error
    return candidate


def artifact_path(root: Path, supplied: str, *, default_directory: str) -> Path:
    """Constrain intentional artifacts to ignored DevKit locations."""

    if not isinstance(supplied, str) or not supplied.strip():
        raise WorkbenchError("artifact name must be a non-empty relative path.")
    path = Path(supplied)
    if path.is_absolute() or ".." in path.parts:
        raise WorkbenchError("artifact name must be a simple relative path.")
    if len(path.parts) == 1:
        path = Path(default_directory) / path
    candidate = (root.resolve() / path).resolve()
    allowed = [(root.resolve() / item).resolve() for item in SAFE_ARTIFACT_ROOTS]
    if not any(_is_relative_to(candidate, directory) for directory in allowed):
        raise WorkbenchError("Workbench artifacts may be written only under devkit/output or devkit/workbench/reports.")
    return candidate


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def slugify(value: str) -> str:
    slug = SLUG_RE.sub("-", value.lower()).strip("-")
    return slug[:80] or "draft"


def workbench_doctor(root: Path = DEFAULT_REPO_ROOT) -> dict[str, Any]:
    root = root.resolve()
    required = {
        "modular_source": root / "src",
        "generated_compile": root / "compile",
        "live_exports": root / "_export",
        "project_builder": root / "build" / "build_all.py",
        "module_atlas": root / "devkit" / "module_atlas" / "module_atlas.py",
        "order_control": root / "devkit" / "order_control" / "order_control.py",
        "mcp_server": root / "devkit" / "mcp_server" / "server.py",
        "contract_catalog": catalog_path(root, "contracts", "manifest.json"),
        "scenario_catalog": catalog_path(root, "scenarios", "manifest.json"),
        "order_contract_catalog": root / "devkit" / "order_control" / "contracts" / "manifest.json",
    }
    rows = [
        {"id": identifier, "path": project_relative(path, root), "exists": path.exists()}
        for identifier, path in required.items()
    ]
    catalog_errors: list[str] = []
    for loader in (load_contract_catalog, load_scenario_catalog):
        try:
            loader(root)
        except WorkbenchError as error:
            catalog_errors.append(str(error))
    ready = all(row["exists"] for row in rows) and not catalog_errors
    return {
        "workbench_version": f"devkit.workbench.v{WORKBENCH_VERSION}",
        "generated_at_utc": utc_now(),
        "ready": ready,
        "python": {"executable": sys.executable, "version": sys.version.split()[0]},
        "checks": rows,
        "catalog_errors": catalog_errors,
        "warnings": [
            "Doctor checks local tooling prerequisites only; it does not build the module or test gameplay.",
            *( ["One or more required Workbench inputs are absent."] if not ready else [] ),
        ],
    }


def workbench_summary(root: Path = DEFAULT_REPO_ROOT) -> dict[str, Any]:
    root = root.resolve()
    doctor = workbench_doctor(root)
    atlas = module_atlas.build_module_atlas(root)
    audit = workspace_audit.audit_workspace(root, max_items=6)
    contracts = contract_drift(root, atlas=atlas, audit=audit)
    scenarios = scenario_list(root)
    try:
        order_summary = order_control.order_summary(order_control.build_order_control(root))
        order_status: dict[str, Any] = {
            "available": True,
            "source_fragment_order": order_summary["source_fragment_order"],
            "generated_ids": order_summary["generated_ids"],
            "contracts": order_summary["contracts"],
        }
    except order_control.OrderControlError as error:
        order_status = {"available": False, "reason": str(error)}
    return {
        "workbench_version": f"devkit.workbench.v{WORKBENCH_VERSION}",
        "generated_at_utc": utc_now(),
        "doctor": doctor,
        "atlas": {
            "entity_count": len(atlas.entities),
            "edge_count": len(atlas.edges),
            "source_area_count": len(module_atlas.SOURCE_AREAS),
        },
        "contracts": contracts["summary"],
        "order_control": order_status,
        "scenarios": scenarios["summary"],
        "workflow": [
            "Start with workbench_impact for a content ID, string, source target, or query.",
            "Run workbench_scope_check with a fixed depth before a source apply or build.",
            "Use workbench_contract_drift, workbench_coverage, and workbench_release_readiness to make evidence gaps explicit.",
            "Use order_summary/order_explain/order_risk before a top-to-bottom move; run workbench_order_report after a reviewed build when ordering itself is in scope.",
            "Use dialogue/presentation specialist tools for those engine-specific semantics; Module Atlas owns the remaining source areas.",
        ],
        "warnings": [
            "The Workbench coordinates static evidence; it is not a runtime simulator or in-game proof system.",
            *audit.get("warnings", []),
        ],
    }


def workbench_order_report(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    baseline: str | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    """Expose Order Control as one fixed Workbench evidence packet."""

    root = root.resolve()
    verification = order_control.order_verify(
        order_control.build_order_control(root),
        baseline=baseline,
        limit=limit,
    )
    return {
        "state": verification["state"],
        "blocker_count": verification["blocker_count"],
        "blockers": verification["blockers"],
        "verification": verification,
        "next_actions": [
            "Review the declared order contracts and exact move diff before source apply.",
            "Run the normal reviewed builder and inspect generated module, ID-table, and export diffs.",
            "For dialogue or engine callback changes, perform the named target in-game smoke path after static evidence is clean.",
        ],
        "warnings": [
            "The Workbench order report is static structural evidence only; it does not execute M&B engine callbacks or dynamic branches.",
            *verification["warnings"],
        ],
    }


def rule_payload(
    rule: Mapping[str, Any],
    *,
    passed: bool,
    actual: Any,
    message: str,
) -> dict[str, Any]:
    return {
        "id": str(rule.get("id", "unnamed-rule")),
        "kind": str(rule.get("kind", "unknown")),
        "label": str(rule.get("label", rule.get("id", "Unnamed rule"))),
        "expected": rule.get("expected"),
        "actual": actual,
        "passed": passed,
        "message": message,
    }


def evaluate_rule(
    rule: Mapping[str, Any],
    *,
    root: Path,
    atlas: module_atlas.ModuleAtlasIndex,
    atlas_integrity: Mapping[str, Any],
    audit: Mapping[str, Any],
    string_report: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    kind = rule.get("kind")
    if kind == "workspace-path":
        path = confined_path(root, str(rule.get("path", "")), label="contract workspace-path")
        exists = path.exists()
        return rule_payload(rule, passed=exists, actual=project_relative(path, root), message="Path exists." if exists else "Required path is missing."), string_report
    if kind == "atlas-area-count":
        actual = len(module_atlas.SOURCE_AREAS)
        expected = rule.get("expected")
        passed = isinstance(expected, int) and actual == expected
        return rule_payload(rule, passed=passed, actual=actual, message="Atlas source-area count matches." if passed else "Atlas source-area count differs."), string_report
    if kind == "integrity-maximum":
        field = str(rule.get("field", ""))
        expected = rule.get("expected")
        actual = atlas_integrity.get(field)
        passed = isinstance(expected, int) and isinstance(actual, int) and actual <= expected
        return rule_payload(rule, passed=passed, actual=actual, message="Integrity threshold is satisfied." if passed else "Integrity threshold is exceeded."), string_report
    if kind == "integrity-summary-minimum":
        if string_report is None:
            string_report = cached_string_report(root)
        field = str(rule.get("field", ""))
        expected = rule.get("expected")
        actual = string_report.get("summary", {}).get(field)
        passed = isinstance(expected, int) and isinstance(actual, int) and actual >= expected
        return rule_payload(rule, passed=passed, actual=actual, message="Text observability threshold is satisfied." if passed else "Text observability threshold is not satisfied."), string_report
    if kind == "atlas-kind-minimum":
        expected = rule.get("expected")
        requested_kind = str(rule.get("entity_kind", ""))
        actual = sum(1 for entity in atlas.entities if entity.kind == requested_kind)
        passed = isinstance(expected, int) and actual >= expected
        return rule_payload(rule, passed=passed, actual=actual, message="Atlas entity minimum is satisfied." if passed else "Atlas entity minimum is not satisfied."), string_report
    if kind == "workspace-audit-maximum":
        field = str(rule.get("field", ""))
        expected = rule.get("expected")
        actual = _nested_value(audit, field)
        passed = isinstance(expected, int) and isinstance(actual, int) and actual <= expected
        return rule_payload(rule, passed=passed, actual=actual, message="Workspace audit threshold is satisfied." if passed else "Workspace audit threshold is exceeded."), string_report
    return rule_payload(rule, passed=False, actual=None, message=f"Unsupported declarative rule kind: {kind!r}."), string_report


def _nested_value(value: Mapping[str, Any], dotted: str) -> Any:
    current: Any = value
    for part in dotted.split("."):
        if not isinstance(current, Mapping):
            return None
        current = current.get(part)
    return current


def contract_drift(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    atlas: module_atlas.ModuleAtlasIndex | None = None,
    audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    catalog = load_contract_catalog(root)
    index = atlas or module_atlas.build_module_atlas(root)
    workspace = audit or workspace_audit.audit_workspace(root, max_items=8)
    integrity = module_atlas.module_integrity(index, limit=100)
    string_report: dict[str, Any] | None = None
    contracts: list[dict[str, Any]] = []
    for definition in catalog["contracts"]:
        if not isinstance(definition, Mapping):
            raise WorkbenchError("Each contract definition must be an object.")
        static = definition.get("static", {})
        rules = static.get("rules", []) if isinstance(static, Mapping) else []
        if not isinstance(rules, list):
            raise WorkbenchError(f"Contract {definition.get('id', '<unnamed>')} rules must be a list.")
        results: list[dict[str, Any]] = []
        for rule in rules:
            if not isinstance(rule, Mapping):
                raise WorkbenchError(f"Contract {definition.get('id', '<unnamed>')} contains a non-object rule.")
            result, string_report = evaluate_rule(
                rule,
                root=root,
                atlas=index,
                atlas_integrity=integrity,
                audit=workspace,
                string_report=string_report,
            )
            results.append(result)
        status = str(definition.get("status", "active"))
        failures = [result for result in results if not result["passed"]]
        contracts.append(
            {
                "id": str(definition.get("id", "unnamed-contract")),
                "title": str(definition.get("title", "Untitled contract")),
                "system": str(definition.get("system", "unknown")),
                "status": status,
                "purpose": str(definition.get("purpose", "")),
                "scenario": definition.get("scenario"),
                "targets": list(definition.get("targets", [])) if isinstance(definition.get("targets", []), list) else [],
                "native_proof": definition.get("nativeProof", {}),
                "rule_count": len(results),
                "failed_rule_count": len(failures),
                "active_blocker": status == "active" and bool(failures),
                "rules": results,
            }
        )
    counts = Counter(contract["status"] for contract in contracts)
    active_blockers = [contract for contract in contracts if contract["active_blocker"]]
    return {
        "catalog": {"schema": catalog["schema"], "version": catalog.get("version")},
        "evaluated_at_utc": utc_now(),
        "summary": {
            "contract_count": len(contracts),
            "contract_count_by_status": dict(sorted(counts.items())),
            "active_blocker_count": len(active_blockers),
            "active_blocker_ids": [contract["id"] for contract in active_blockers],
            "static_integrity": {
                "duplicate_definition_count": integrity["duplicate_definition_count"],
                "unresolved_reference_entity_count": integrity["unresolved_reference_entity_count"],
                "syntax_error_count": integrity["syntax_error_count"],
            },
        },
        "contracts": contracts,
        "warnings": [
            "A passing static contract is evidence, not in-game approval.",
            "Legacy/generated ID fallbacks remain visible in module_integrity and are not relabeled as missing source definitions.",
            *integrity["warnings"],
        ],
    }


def contract_baseline(root: Path = DEFAULT_REPO_ROOT, *, label: str = "baseline") -> dict[str, Any]:
    root = root.resolve()
    checked_label = require_text(label, name="label", maximum=80)
    report = contract_drift(root)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = catalog_path(root, "contracts", "baselines", f"{timestamp}_{slugify(checked_label)}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "sod-modern.workbench-contract-baseline.v1",
        "created_at_utc": utc_now(),
        "label": checked_label,
        "contract_drift": report,
        "evidence_boundary": "Static observation snapshot only; it is not a gameplay approval or a replacement for contract expectations.",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "artifact": {"path": project_relative(path, root), "kind": "contract-baseline", "label": checked_label},
        "summary": report["summary"],
        "warnings": ["Baseline was written under devkit/workbench/contracts/baselines; it did not modify module source, compile output, or exports."],
    }


def scenario_list(root: Path = DEFAULT_REPO_ROOT) -> dict[str, Any]:
    catalog = load_scenario_catalog(root.resolve())
    scenarios = []
    for item in catalog["scenarios"]:
        if not isinstance(item, Mapping):
            raise WorkbenchError("Each scenario definition must be an object.")
        steps = item.get("steps", [])
        if not isinstance(steps, list):
            raise WorkbenchError(f"Scenario {item.get('id', '<unnamed>')} steps must be a list.")
        scenarios.append(
            {
                "id": str(item.get("id", "unnamed-scenario")),
                "title": str(item.get("title", "Untitled scenario")),
                "category": str(item.get("category", "unknown")),
                "purpose": str(item.get("purpose", "")),
                "evidence_level": str(item.get("evidence_level", "structural")),
                "proof_note": str(item.get("proof_note", "")),
                "targets": list(item.get("targets", [])) if isinstance(item.get("targets", []), list) else [],
                "step_count": len(steps),
                "steps": [
                    {"kind": step.get("kind"), "action": step.get("action"), "path": step.get("path"), "label": step.get("label")}
                    for step in steps
                    if isinstance(step, Mapping)
                ],
            }
        )
    counts = Counter(scenario["category"] for scenario in scenarios)
    return {
        "catalog": {"schema": catalog["schema"], "version": catalog.get("version")},
        "summary": {"scenario_count": len(scenarios), "scenario_count_by_category": dict(sorted(counts.items()))},
        "scenarios": scenarios,
        "warnings": ["Scenarios are registered fixed steps only. They cannot run a caller-supplied shell command."],
    }


def builtin_scenario_step(root: Path, action: str) -> dict[str, Any]:
    if action == "workspace_audit":
        payload = workspace_audit.audit_workspace(root, max_items=8)
        return {"passed": True, "data": payload, "warnings": payload.get("warnings", [])}
    if action == "module_integrity":
        index = module_atlas.build_module_atlas(root)
        payload = module_atlas.module_integrity(index, limit=100)
        passed = payload["finding_count"] == 0
        return {"passed": passed, "data": payload, "warnings": payload["warnings"]}
    if action == "string_integrity_summary":
        report = cached_string_report(root)
        payload = string_integrity.summary_payload(report, limit=100)
        return {"passed": not payload["module_errors"], "data": payload, "warnings": payload["warnings"]}
    raise WorkbenchError(f"Scenario requested unsupported builtin action {action!r}.")


def run_registered_scenario(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    scenario_id: str,
    timeout_seconds: int = 90,
    write_report: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    checked_id = require_text(scenario_id, name="scenario_id")
    timeout = require_limit(timeout_seconds, name="timeout_seconds", maximum=MAX_TIMEOUT_SECONDS)
    catalog = load_scenario_catalog(root)
    definitions = [item for item in catalog["scenarios"] if isinstance(item, Mapping) and item.get("id") == checked_id]
    if not definitions:
        raise WorkbenchError(f"No registered Workbench scenario named {checked_id!r}.")
    scenario = definitions[0]
    steps = scenario.get("steps", [])
    assert isinstance(steps, list)
    results: list[dict[str, Any]] = []
    for ordinal, step in enumerate(steps, start=1):
        if not isinstance(step, Mapping):
            raise WorkbenchError(f"Scenario {checked_id} has an invalid step at position {ordinal}.")
        kind = step.get("kind")
        label = str(step.get("label", f"Step {ordinal}"))
        if kind == "builtin":
            action = require_text(step.get("action"), name=f"scenario {checked_id} builtin action")
            try:
                outcome = builtin_scenario_step(root, action)
                results.append({"ordinal": ordinal, "label": label, "kind": kind, "action": action, **outcome})
            except (WorkbenchError, module_atlas.ModuleAtlasError, workspace_audit.AuditError, string_integrity.StringIntegrityError) as error:
                results.append({"ordinal": ordinal, "label": label, "kind": kind, "action": action, "passed": False, "error": str(error), "warnings": []})
            continue
        if kind == "python-test":
            relative = require_text(step.get("path"), name=f"scenario {checked_id} test path")
            path = confined_path(root, relative, label="scenario test path")
            if not path.is_file() or not path.suffix.casefold() == ".py":
                results.append({"ordinal": ordinal, "label": label, "kind": kind, "path": relative, "passed": False, "error": "Registered Python test file is missing.", "warnings": []})
                continue
            try:
                completed = subprocess.run(
                    [sys.executable, "-B", str(path)],
                    cwd=root,
                    text=True,
                    capture_output=True,
                    timeout=timeout,
                    check=False,
                )
                output = (completed.stdout + completed.stderr).strip()
                if len(output) > 4_000:
                    output = output[:3_997] + "..."
                results.append(
                    {
                        "ordinal": ordinal,
                        "label": label,
                        "kind": kind,
                        "path": relative,
                        "command": [sys.executable, "-B", relative],
                        "passed": completed.returncode == 0,
                        "exit_code": completed.returncode,
                        "output": output,
                        "warnings": [],
                    }
                )
            except subprocess.TimeoutExpired:
                results.append({"ordinal": ordinal, "label": label, "kind": kind, "path": relative, "passed": False, "error": f"Timed out after {timeout} seconds.", "warnings": []})
            continue
        raise WorkbenchError(f"Scenario {checked_id} uses unsupported registered step kind {kind!r}.")
    passed = all(result["passed"] for result in results)
    payload = {
        "scenario": {
            "id": checked_id,
            "title": scenario.get("title"),
            "category": scenario.get("category"),
            "evidence_level": scenario.get("evidence_level"),
            "proof_note": scenario.get("proof_note"),
        },
        "executed_at_utc": utc_now(),
        "passed": passed,
        "step_count": len(results),
        "passed_step_count": sum(1 for result in results if result["passed"]),
        "results": results,
        "warnings": [
            "Scenario execution uses only registered builtins and registered Python test paths; it cannot run arbitrary commands.",
            "A scenario result is structural/test evidence, not a live M&B gameplay certificate.",
        ],
    }
    if write_report:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = artifact_path(root, f"{timestamp}_{slugify(checked_id)}.json", default_directory="devkit/workbench/reports")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        payload["artifact"] = {"path": project_relative(path, root), "kind": "scenario-report"}
    return payload


def exact_alias_candidates(
    index: module_atlas.ModuleAtlasIndex,
    query: str,
) -> list[module_atlas.ModuleEntity]:
    matches = list(index.by_alias.get(query, ()))
    if matches:
        return matches
    prefix_matches = []
    for kind, prefix in module_atlas.PREFIX_BY_KIND.items():
        if query.startswith(prefix):
            prefix_matches.extend(entity for entity in index.by_alias.get(query, ()) if entity.kind == kind)
    return sorted(dict.fromkeys(prefix_matches), key=module_atlas.entity_sort_key)


def resolve_workbench_target(
    index: module_atlas.ModuleAtlasIndex,
    target: str,
    *,
    limit: int = 12,
) -> ResolvedWorkbenchTarget:
    checked = require_text(target, name="target")
    maximum = require_limit(limit)
    if checked.startswith("module:"):
        entity = module_atlas.require_entity(index, checked)
        return ResolvedWorkbenchTarget("atlas_entity", checked, entity, entity.target_id, (entity,))
    if checked.startswith("source:"):
        fragment = change_router.target_fragment(index.router, checked)
        entities = tuple(index.by_target.get(fragment.id, ())[:maximum])
        return ResolvedWorkbenchTarget("source_target", checked, entities[0] if len(entities) == 1 else None, fragment.id, entities)
    exact = exact_alias_candidates(index, checked)
    if len(exact) == 1:
        entity = exact[0]
        return ResolvedWorkbenchTarget("exact_alias", checked, entity, entity.target_id, (entity,))
    found = module_atlas.module_find(index, query=checked, limit=maximum)
    candidates = tuple(index.by_id[item["entity_id"]] for item in found["entities"])
    primary = candidates[0] if len(candidates) == 1 else None
    return ResolvedWorkbenchTarget("query", checked, primary, primary.target_id if primary else None, candidates)


def scope_plan(index: module_atlas.ModuleAtlasIndex, entity: module_atlas.ModuleEntity) -> dict[str, Any]:
    fragment = index.router.fragments[entity.path]
    candidates = change_router.test_candidates(index.router, fragment, limit=3)
    area_notes = {
        "dialogs": "Use dialogue_context/dialogue_patch for first-match route semantics and compiled-order hazards.",
        "presentations": "Use presentation_canvas/presentation_patch for overlay geometry and shared register bindings.",
        "menus": "Use menu_flow plus text_explain when visible text or transitions are involved.",
        "mission_templates": "Use mission_timeline to inspect authored event/timing blocks before a build.",
        "scripts": "Use script_flow and entity_references to inspect direct callers/callees and globals/registers.",
        "triggers": "Use trigger_timeline to inspect scheduling and direct operation links.",
        "quests": "Use quest_registry and entity_references to inspect direct usage before removal or text changes.",
        "constants": "Use entity_references to inspect dependent authored references before changing a constant expression.",
    }
    return {
        "entity_id": entity.id,
        "source_target_id": entity.target_id,
        "area": entity.area,
        "fixed_steps": [
            {"id": "syntax-and-order", "kind": "change-router-verify", "detail": "Parse the exact source fragment and report ordering/generated freshness."},
            {"id": "static-test-candidates", "kind": "registered-local-tests", "detail": "Run only Change Router-selected local static tests at standard/deep depth.", "candidates": candidates},
            {"id": "isolated-area-build", "kind": "staged-build", "detail": "Run only at deep depth; the builder executes in a temporary isolated workspace."},
            {"id": "area-specialist", "kind": "specialist", "detail": area_notes[entity.area]},
        ],
        "evidence_boundary": "This plan contains fixed repository checks only. It cannot execute a caller-supplied command and it never writes compile/ or _export/.",
    }


def workbench_scope_check(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    entity_id: str,
    depth: str = "standard",
    expected_sha256: str | None = None,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    root = root.resolve()
    checked_depth = require_depth(depth)
    timeout = require_limit(timeout_seconds, name="timeout_seconds", maximum=MAX_TIMEOUT_SECONDS)
    index = module_atlas.build_module_atlas(root)
    entity = module_atlas.require_entity(index, entity_id)
    run_tests = checked_depth in {"standard", "deep"}
    stage_build = checked_depth == "deep"
    verification = change_router.verify_change(
        index.router,
        entity.target_id,
        expected_sha256=expected_sha256,
        run_tests=run_tests,
        stage_build_check=stage_build,
        max_tests=3 if checked_depth == "deep" else 1,
        timeout_seconds=timeout,
    )
    integrity = module_atlas.module_integrity(index, limit=30)
    passed = bool(verification["syntax"].get("passed"))
    if run_tests:
        passed = passed and bool(verification["tests_passed"])
    if stage_build:
        staged = verification["staged_build"]
        passed = passed and (not staged.get("available") or bool(staged.get("passed")))
    return {
        "entity": module_atlas.entity_payload(index, entity),
        "depth": checked_depth,
        "plan": scope_plan(index, entity),
        "passed": passed,
        "verification": verification,
        "global_static_integrity": {
            "finding_count": integrity["finding_count"],
            "duplicate_definition_count": integrity["duplicate_definition_count"],
            "unresolved_reference_entity_count": integrity["unresolved_reference_entity_count"],
            "syntax_error_count": integrity["syntax_error_count"],
        },
        "warnings": [
            "Scope checks are fixed, bounded source/build evidence. They do not rebuild the live workspace or export files.",
            "Passing static checks does not establish dynamic M&B condition reachability or in-game display behavior.",
            *verification["warnings"],
        ],
    }


def selector_matches(entity: module_atlas.ModuleEntity, selector: str) -> bool:
    if not isinstance(selector, str):
        return False
    if ":" in selector:
        kind, name = selector.split(":", 1)
        return entity.kind == kind and (entity.name == name or name in entity.aliases)
    return selector == entity.id or selector in entity.aliases or selector == entity.name


def mapped_evidence(
    entity: module_atlas.ModuleEntity,
    *,
    contracts: Sequence[Mapping[str, Any]],
    scenarios: Sequence[Mapping[str, Any]],
    index: module_atlas.ModuleAtlasIndex,
) -> tuple[str, list[str], list[str], int]:
    contract_ids = [
        str(contract.get("id"))
        for contract in contracts
        if any(selector_matches(entity, selector) for selector in contract.get("targets", []) if isinstance(selector, str))
    ]
    scenario_ids = [
        str(scenario.get("id"))
        for scenario in scenarios
        if any(selector_matches(entity, selector) for selector in scenario.get("targets", []) if isinstance(selector, str))
    ]
    test_count = len(change_router.test_candidates(index.router, index.router.fragments[entity.path], limit=3))
    if contract_ids:
        maturity = "static_contract"
    elif scenario_ids:
        maturity = "registered_scenario"
    elif test_count:
        maturity = "test_candidate"
    elif index.router.generated_by_source.get(entity.path):
        maturity = "generated_provenance"
    else:
        maturity = "source_only"
    return maturity, contract_ids, scenario_ids, test_count


def workbench_coverage(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    area: str = "all",
    kind: str | None = None,
    query: str | None = None,
    gaps_only: bool = False,
    limit: int = 50,
) -> dict[str, Any]:
    root = root.resolve()
    maximum = require_limit(limit)
    index = module_atlas.build_module_atlas(root)
    checked_area = module_atlas.require_area(area)
    checked_kind = module_atlas.require_query(kind, name="kind") if kind is not None else None
    needle = module_atlas.require_query(query).casefold() if query is not None else None
    contracts = load_contract_catalog(root)["contracts"]
    scenarios = load_scenario_catalog(root)["scenarios"]
    entries: list[dict[str, Any]] = []
    for entity in index.entities:
        if checked_area != "all" and entity.area != checked_area:
            continue
        if checked_kind and entity.kind != checked_kind:
            continue
        if needle and needle not in module_atlas.entity_search_text(entity):
            continue
        maturity, contract_ids, scenario_ids, test_count = mapped_evidence(entity, contracts=contracts, scenarios=scenarios, index=index)
        if gaps_only and EVIDENCE_RANK[maturity] > EVIDENCE_RANK["generated_provenance"]:
            continue
        entries.append(
            {
                "entity_id": entity.id,
                "area": entity.area,
                "kind": entity.kind,
                "name": entity.name,
                "source": {"path": entity.path, "line": entity.line},
                "coverage_maturity": maturity,
                "exact_contract_ids": contract_ids,
                "registered_scenario_ids": scenario_ids,
                "static_test_candidate_count": test_count,
                "has_generated_provenance": bool(index.router.generated_by_source.get(entity.path)),
            }
        )
    entries.sort(key=lambda item: (EVIDENCE_RANK[item["coverage_maturity"]], item["area"], item["kind"], item["name"].casefold(), item["source"]["path"], item["source"]["line"]))
    maturity_counts = Counter(entry["coverage_maturity"] for entry in entries)
    return {
        "filters": {"area": checked_area, "kind": checked_kind, "query": query, "gaps_only": gaps_only},
        "match_count": len(entries),
        "returned_count": min(len(entries), maximum),
        "truncated": len(entries) > maximum,
        "coverage_count_by_maturity": dict(sorted(maturity_counts.items())),
        "entries": entries[:maximum],
        "warnings": [
            "Coverage is exact only for a declared contract target, registered scenario target, generated provenance, or Change Router test candidate.",
            "Broad system context is intentionally not relabeled as proof for each entity.",
        ],
    }


def coverage_for_entity(
    root: Path,
    index: module_atlas.ModuleAtlasIndex,
    entity: module_atlas.ModuleEntity,
) -> dict[str, Any]:
    contracts = load_contract_catalog(root)["contracts"]
    scenarios = load_scenario_catalog(root)["scenarios"]
    maturity, contract_ids, scenario_ids, test_count = mapped_evidence(entity, contracts=contracts, scenarios=scenarios, index=index)
    return {
        "entity_id": entity.id,
        "coverage_maturity": maturity,
        "exact_contract_ids": contract_ids,
        "registered_scenario_ids": scenario_ids,
        "static_test_candidate_count": test_count,
        "generated_provenance": module_atlas.generated_payload(index, entity),
    }


def workbench_text_lint(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    query: str | None = None,
    kind: str = "all",
    severity: str = "warning",
    limit: int = 50,
) -> dict[str, Any]:
    root = root.resolve()
    maximum = require_limit(limit)
    if severity not in {"all", "info", "warning", "error"}:
        raise WorkbenchError("severity must be one of: all, info, warning, error.")
    report = cached_string_report(root)
    sinks = string_integrity.query_sinks(report, query=query, kind=kind, include_clean=False, limit=maximum)
    threshold = SEVERITY_RANK[severity] if severity != "all" else 0
    findings = [
        finding
        for finding in [*report["writer_contract_findings"], *report["sink_findings"]]
        if severity == "all" or SEVERITY_RANK.get(str(finding.get("severity", "clean")), 0) >= threshold
    ]
    findings.sort(key=lambda item: (-SEVERITY_RANK.get(str(item.get("severity", "clean")), 0), str(item.get("code", ""))))
    return {
        "filters": {"query": query, "kind": kind, "severity": severity},
        "summary": report["summary"],
        "finding_count": len(findings),
        "returned_finding_count": min(len(findings), maximum),
        "findings_truncated": len(findings) > maximum,
        "findings": findings[:maximum],
        "sinks": sinks,
        "evidence_boundary": "Text lint follows static generated-operation and source-marker evidence. Branches, dynamic IDs, and game state remain explicit uncertainty.",
        "warnings": report["warnings"],
    }


def compact_code_matches(payload: Mapping[str, Any], *, maximum: int) -> dict[str, Any]:
    matches = list(payload.get("matches", []))
    return {
        "match_count": payload.get("match_count", len(matches)),
        "returned_count": min(len(matches), maximum),
        "truncated": len(matches) > maximum,
        "matches": matches[:maximum],
        "warnings": payload.get("warnings", []),
    }


def optional_text_evidence(root: Path, query: str, *, limit: int) -> dict[str, Any]:
    """Build the expensive string packet only when an agent explicitly asks."""

    report = cached_string_report(root)
    sinks = string_integrity.query_sinks(report, query=query, kind="all", include_clean=True, limit=min(limit, 20))
    try:
        ledger = text_execution_ledger.build_ledger(root)
        explanations = text_execution_ledger.explain(
            ledger,
            query=query,
            kind="all",
            include_clean=True,
            limit=min(limit, 5),
            max_steps=60,
        )
    except text_execution_ledger.LedgerError as error:
        explanations = {"available": False, "error": str(error)}
    return {
        "string_integrity": sinks,
        "text_execution": explanations,
        "evidence_boundary": "The packet is static source/generated evidence; use it to select an exact in-game smoke path rather than treating it as runtime execution.",
    }


def workbench_impact(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    target: str,
    limit: int = 12,
    include_text_evidence: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    maximum = require_limit(limit)
    index = module_atlas.build_module_atlas(root)
    resolved = resolve_workbench_target(index, target, limit=maximum)
    router = index.router
    entities = list(resolved.candidates)
    primary = resolved.entity
    context: dict[str, Any] | None = None
    graph: dict[str, Any] | None = None
    change_impact: dict[str, Any] | None = None
    coverage: dict[str, Any] | None = None
    source_context: dict[str, Any] | None = None
    if primary is not None:
        context = module_atlas.module_context(index, primary.id, max_lines=80, related_limit=min(maximum, 30))
        graph = module_atlas.module_graph(index, primary.id, direction="both", depth=2, max_nodes=min(maximum * 5, 120))
        change_impact = change_router.change_impact(router, primary.target_id, related_limit=min(maximum, 30))
        coverage = coverage_for_entity(root, index, primary)
    elif resolved.target_id is not None:
        source_context = change_router.linked_context(router, resolved.target_id, max_lines=80, related_limit=min(maximum, 30))
        change_impact = change_router.change_impact(router, resolved.target_id, related_limit=min(maximum, 30))
    raw_matches = change_router.code_find(router, resolved.query, scope="all", limit=maximum)
    text_packet = optional_text_evidence(root, resolved.query, limit=maximum) if include_text_evidence else None
    ambiguity = None
    if primary is None and entities:
        ambiguity = "The target resolves to multiple semantic entities; inspect candidates and choose an exact module: entity ID before editing."
    if not entities and resolved.target_id is None:
        ambiguity = "No exact semantic owner was resolved. Use source-search evidence before attempting an edit."
    return {
        "target": {
            "input": resolved.query,
            "resolution_kind": resolved.kind,
            "primary_entity_id": primary.id if primary else None,
            "source_target_id": resolved.target_id,
            "candidate_count": len(entities),
            "candidates": [module_atlas.entity_payload(index, entity, include_fields=False, block_operation_limit=12) for entity in entities[:maximum]],
            "ambiguous": ambiguity is not None,
            "ambiguity_note": ambiguity,
        },
        "primary_context": context,
        "dependency_graph": graph,
        "source_context": source_context,
        "change_impact": change_impact,
        "coverage": coverage,
        "raw_search": compact_code_matches(raw_matches, maximum=maximum),
        "text_evidence": text_packet,
        "next_actions": (
            [
                "Inspect the exact semantic context and dependency graph.",
                "Run workbench_scope_check with the returned primary entity ID before source authoring.",
                "Create a semantic patch through dialogue_patch, presentation_patch, or module_patch; inspect the SHA-guarded diff before apply.",
            ]
            if primary is not None
            else [
                "Select one exact returned module entity or source target.",
                "Use code_find/linked_context for evidence that is outside the semantic Atlas.",
                "Do not infer a source owner from a broad text search alone.",
            ]
        ),
        "warnings": [
            "Impact is source/generated/static evidence; it does not execute dynamic M&B conditions or menus.",
            "Set include_text_evidence=true for the heavier string/register packet when diagnosing wrong displayed text.",
        ],
    }


def source_freshness_blockers(audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    blockers = []
    consistency = audit.get("consistency", {}) if isinstance(audit, Mapping) else {}
    for row in consistency.get("source_to_compile_freshness", []) if isinstance(consistency, Mapping) else []:
        if not isinstance(row, Mapping):
            continue
        if not row.get("compile_exists") or row.get("direct_input_is_newer"):
            blockers.append(
                {
                    "id": "generated-freshness",
                    "area": row.get("source_area"),
                    "message": f"{row.get('source_area')} source is newer than or missing {row.get('compile_module')}; a reviewed build is required before runtime validation.",
                }
            )
    return blockers


def render_release_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# SoD Modern Workbench Release Readiness",
        "",
        "This is a static/manual review checklist, not an in-game release certificate.",
        "",
        f"- Structural state: **{payload.get('state', 'unknown')}**",
        f"- Blocking evidence items: **{payload.get('blocker_count', 0)}**",
        "",
        "## Blocking evidence",
        "",
    ]
    blockers = payload.get("blockers", [])
    if blockers:
        for blocker in blockers:
            lines.append(f"- `{blocker.get('id', 'unknown')}`: {blocker.get('message', '')}")
    else:
        lines.append("- No static blockers were reported.")
    lines.extend(["", "## Required manual gates", ""])
    for item in payload.get("manual_gates", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Evidence boundary", "", str(payload.get("evidence_boundary", "")), ""])
    return "\n".join(lines)


def workbench_release_readiness(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    write_report: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    doctor = workbench_doctor(root)
    audit = workspace_audit.audit_workspace(root, max_items=12)
    atlas = module_atlas.build_module_atlas(root)
    integrity = module_atlas.module_integrity(atlas, limit=100)
    contracts = contract_drift(root, atlas=atlas, audit=audit)
    order_verification = order_control.order_verify(order_control.build_order_control(root), limit=100)
    string_summary = string_integrity.summary_payload(cached_string_report(root), limit=25)
    blockers: list[dict[str, Any]] = []
    if not doctor["ready"]:
        blockers.append({"id": "doctor", "message": "Workbench prerequisites are incomplete; inspect doctor checks."})
    for contract in contracts["contracts"]:
        if contract["active_blocker"]:
            blockers.append({"id": f"contract:{contract['id']}", "message": f"Active contract has {contract['failed_rule_count']} failing rule(s)."})
    for contract in order_verification["contracts"]["contracts"]:
        if contract["active_blocker"]:
            blockers.append({"id": f"order-contract:{contract['id']}", "message": f"Protected order contract failed: {contract.get('title', contract['id'])}."})
    for item in source_freshness_blockers(audit):
        blockers.append(item)
    if integrity["finding_count"]:
        blockers.append({"id": "module-integrity", "message": f"Module Atlas reports {integrity['finding_count']} direct static structural finding(s)."})
    if string_summary["module_errors"]:
        blockers.append({"id": "text-analysis", "message": "String integrity could not analyze one or more generated modules."})
    state = "structural_blocked" if blockers else "structural_ready_for_manual_review"
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now(),
        "state": state,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "doctor": {"ready": doctor["ready"], "catalog_error_count": len(doctor["catalog_errors"])},
        "module_integrity": {
            "finding_count": integrity["finding_count"],
            "generated_id_fallback_entity_count": integrity["generated_id_fallback_entity_count"],
        },
        "contracts": contracts["summary"],
        "order_control": {
            "state": order_verification["state"],
            "blocker_count": order_verification["blocker_count"],
            "contracts": order_verification["contracts"]["summary"],
            "generated_marker_order_mismatch_count": order_verification["generated_order_parity"]["mismatch_count"],
            "generated_marker_observability_gap_count": order_verification["generated_order_parity"]["generated_marker_observability_gap_count"],
            "dialogue_order_hazard_count": order_verification["dialogue_order_hazards"]["hazard_count"],
        },
        "text_observability": {
            "text_sink_count": string_summary["summary"]["text_sink_count"],
            "writer_contract_finding_count": string_summary["summary"]["writer_contract_finding_count"],
            "module_error_count": len(string_summary["module_errors"]),
        },
        "worktree": audit.get("worktree", {}),
        "manual_gates": [
            "Review the exact source diff and SHA-guarded semantic plan for every intended source change.",
            "Run the normal reviewed module build; inspect generated and export diffs instead of overwriting them blindly.",
            "Run a fixed Workbench scenario and/or scope check for each changed source area.",
            "Perform the target in-game smoke path: dialogue/menu/presentation/mission behavior remains an engine-runtime gate.",
            "When visible text changes, verify strings.txt and quick_strings.txt as well as the target screen after build.",
            "When order changes, inspect Order Control's manifest/ID diff and make an explicit save-compatibility decision for every generated-ID shift.",
        ],
        "evidence_boundary": "This report assembles static structure, source/compile freshness, contract, text-observability, and worktree evidence. It never certifies an in-game release.",
        "warnings": [
            *audit.get("warnings", []),
            *integrity["warnings"],
            *order_verification["warnings"],
            *string_summary["warnings"],
        ],
    }
    if write_report:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        json_path = artifact_path(root, f"{timestamp}_release-readiness.json", default_directory="devkit/workbench/reports")
        markdown_path = json_path.with_suffix(".md")
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        markdown_path.write_text(render_release_markdown(payload), encoding="utf-8")
        payload["artifacts"] = [
            {"path": project_relative(json_path, root), "kind": "release-readiness-json"},
            {"path": project_relative(markdown_path, root), "kind": "release-readiness-markdown"},
        ]
    return payload


def draft_template(kind: str, title: str) -> dict[str, Any]:
    tool_map = {
        "constant": {"find": "module_find", "patch": "module_patch", "verify": "module_verify"},
        "dialogue": {"find": "dialogue_find", "patch": "dialogue_patch", "verify": "dialogue_verify"},
        "menu": {"find": "menu_flow", "patch": "module_patch", "verify": "module_verify"},
        "mission": {"find": "mission_timeline", "patch": "module_patch", "verify": "module_verify"},
        "presentation": {"find": "presentation_find", "patch": "presentation_patch", "verify": "presentation_verify"},
        "quest": {"find": "quest_registry", "patch": "module_patch", "verify": "module_verify"},
        "script": {"find": "script_flow", "patch": "module_patch", "verify": "module_verify"},
        "trigger": {"find": "trigger_timeline", "patch": "module_patch", "verify": "module_verify"},
    }
    return {
        "schema": "sod-modern.workbench-draft.v1",
        "state": "disabled",
        "kind": kind,
        "title": title,
        "created_at_utc": utc_now(),
        "authoring_intent": {
            "summary": "Describe the player-visible goal and the owning module-system entry before promoting this draft into a semantic source plan.",
            "player_path": [],
            "engine_entry": None,
            "text_sources": [],
            "runtime_unknowns": [],
        },
        "required_evidence": [
            "An exact source owner returned by Workbench impact or a specialist find tool.",
            "A bounded dependency graph and scope-check result.",
            "A SHA-guarded semantic patch plan reviewed before any source apply.",
            "A normal build diff and a targeted in-game smoke result before promotion claims.",
        ],
        "tool_route": tool_map[kind],
        "promotion_boundary": "This draft lives only under devkit/workbench/drafts and is not module data. It never activates content or edits src/, compile/, or _export/.",
    }


def workbench_draft(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    kind: str,
    title: str,
    output_name: str | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    if kind not in VALID_DRAFT_KINDS:
        raise WorkbenchError("kind must be one of: " + ", ".join(VALID_DRAFT_KINDS))
    checked_title = require_text(title, name="title", maximum=160)
    if not isinstance(overwrite, bool):
        raise WorkbenchError("overwrite must be a boolean.")
    filename = output_name or f"{slugify(kind)}_{slugify(checked_title)}.draft.json"
    if not filename.endswith(".json"):
        filename += ".json"
    if "/" in filename or "\\" in filename or ".." in filename:
        raise WorkbenchError("output_name must be a simple filename.")
    destination = catalog_path(root, "drafts", filename)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise WorkbenchError("Draft already exists; choose a different output_name or set overwrite=true explicitly.")
    payload = draft_template(kind, checked_title)
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "artifact": {"path": project_relative(destination, root), "kind": "disabled-authoring-draft", "draft_kind": kind},
        "draft": payload,
        "warnings": ["Draft creation is an intentional DevKit artifact write only. No module source, generated module, or export file was changed."],
    }


def write_cli_payload(root: Path, payload: Mapping[str, Any], output: str | None) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output is None:
        sys.stdout.write(rendered)
        return
    path = artifact_path(root, output, default_directory="devkit/workbench/reports")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SoD Modern LLM-first Workbench: fixed impact, validation, contracts, scenarios, coverage, and release evidence.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    for name in ("doctor", "summary", "contract-drift", "scenario-list"):
        command = subparsers.add_parser(name)
        command.add_argument("--output")
    impact = subparsers.add_parser("impact")
    impact.add_argument("target")
    impact.add_argument("--limit", type=int, default=12)
    impact.add_argument("--include-text-evidence", action="store_true")
    impact.add_argument("--output")
    scope = subparsers.add_parser("scope-check")
    scope.add_argument("entity_id")
    scope.add_argument("--depth", choices=VALID_DEPTHS, default="standard")
    scope.add_argument("--expected-sha256")
    scope.add_argument("--timeout-seconds", type=int, default=90)
    scope.add_argument("--output")
    lint = subparsers.add_parser("text-lint")
    lint.add_argument("--query")
    lint.add_argument("--kind", default="all")
    lint.add_argument("--severity", choices=("all", "info", "warning", "error"), default="warning")
    lint.add_argument("--limit", type=int, default=50)
    lint.add_argument("--output")
    order_report = subparsers.add_parser("order-report")
    order_report.add_argument("--baseline")
    order_report.add_argument("--limit", type=int, default=100)
    order_report.add_argument("--output")
    baseline = subparsers.add_parser("contract-baseline")
    baseline.add_argument("--label", default="baseline")
    baseline.add_argument("--output")
    coverage = subparsers.add_parser("coverage")
    coverage.add_argument("--area", default="all")
    coverage.add_argument("--kind")
    coverage.add_argument("--query")
    coverage.add_argument("--gaps-only", action="store_true")
    coverage.add_argument("--limit", type=int, default=50)
    coverage.add_argument("--output")
    scenario = subparsers.add_parser("scenario-run")
    scenario.add_argument("scenario_id")
    scenario.add_argument("--timeout-seconds", type=int, default=90)
    scenario.add_argument("--write-report", action="store_true")
    scenario.add_argument("--output")
    release = subparsers.add_parser("release-readiness")
    release.add_argument("--write-report", action="store_true")
    release.add_argument("--output")
    draft = subparsers.add_parser("draft")
    draft.add_argument("kind", choices=VALID_DRAFT_KINDS)
    draft.add_argument("title")
    draft.add_argument("--output-name")
    draft.add_argument("--overwrite", action="store_true")
    draft.add_argument("--output")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    command = args.command or "summary"
    try:
        if command == "doctor":
            payload = workbench_doctor(root)
        elif command == "summary":
            payload = workbench_summary(root)
        elif command == "impact":
            payload = workbench_impact(root, target=args.target, limit=args.limit, include_text_evidence=args.include_text_evidence)
        elif command == "scope-check":
            payload = workbench_scope_check(root, entity_id=args.entity_id, depth=args.depth, expected_sha256=args.expected_sha256, timeout_seconds=args.timeout_seconds)
        elif command == "text-lint":
            payload = workbench_text_lint(root, query=args.query, kind=args.kind, severity=args.severity, limit=args.limit)
        elif command == "order-report":
            payload = workbench_order_report(root, baseline=args.baseline, limit=args.limit)
        elif command == "contract-drift":
            payload = contract_drift(root)
        elif command == "contract-baseline":
            payload = contract_baseline(root, label=args.label)
        elif command == "coverage":
            payload = workbench_coverage(root, area=args.area, kind=args.kind, query=args.query, gaps_only=args.gaps_only, limit=args.limit)
        elif command == "scenario-list":
            payload = scenario_list(root)
        elif command == "scenario-run":
            payload = run_registered_scenario(root, scenario_id=args.scenario_id, timeout_seconds=args.timeout_seconds, write_report=args.write_report)
        elif command == "release-readiness":
            payload = workbench_release_readiness(root, write_report=args.write_report)
        elif command == "draft":
            payload = workbench_draft(root, kind=args.kind, title=args.title, output_name=args.output_name, overwrite=args.overwrite)
        else:
            raise WorkbenchError(f"Unknown Workbench command {command!r}.")
        write_cli_payload(root, payload, getattr(args, "output", None))
        return 0
    except (
        WorkbenchError,
        change_router.ChangeRouterError,
        module_atlas.ModuleAtlasError,
        order_control.OrderControlError,
        string_integrity.StringIntegrityError,
        text_execution_ledger.LedgerError,
        workspace_audit.AuditError,
    ) as error:
        parser.error(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
