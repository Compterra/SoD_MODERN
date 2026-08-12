#!/usr/bin/env python3
"""Read-only Mount & Blade RGL-log diagnosis with source/export provenance.

The legacy engine reports many failures only after campaign state has already
reached a bad edge.  This tool turns those opaque lines into deterministic,
source-mapped evidence.  It deliberately does not modify saves, source,
generated modules, exports, or a live module directory.
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
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
SENTINEL_VERSION = "1.1.0"
MAX_LIMIT = 500

SCRIPT_ERROR_START_RE = re.compile(r"SCRIPT\s+ERROR\s+ON\s+OPCODE\s+(?P<opcode>\d+)\s*:\s*", re.IGNORECASE)
ENGINE_LINE_RE = re.compile(r";\s*LINE\s+NO\s*:\s*(?P<line>\d+)\s*:", re.IGNORECASE)
SCRIPT_TRACE_RE = re.compile(r"At\s+script\s*:\s*(?P<script>[A-Za-z0-9_]+)\.", re.IGNORECASE)
INVALID_ID_RE = re.compile(r"Invalid\s+(?P<kind>Party|Faction)\s+ID\s*:\s*(?P<value>-?\d+)", re.IGNORECASE)
WARNING_RE = re.compile(r"\bWARNING\s*:\s*(?P<message>[^\r\n]+)", re.IGNORECASE)
PRESENTATION_WARNING_RE = re.compile(r"UNABLE\s+TO\s+MAP\s+GAME\s+PRESENTATION\s+CODE\s*:\s*(?P<name>[A-Za-z0-9_]+)", re.IGNORECASE)
MATERIAL_WARNING_RE = re.compile(r"Unable\s+to\s+find\s+material\s+(?P<name>[A-Za-z0-9_]+)", re.IGNORECASE)
VERTEX_BUFFER_RE = re.compile(r"Out\s+of\s+Static\s+vertex\s+buffer\s+memory", re.IGNORECASE)
SCRIPT_DECLARATION_RE = re.compile(r"^\s*\(\s*[\"'](?P<name>[A-Za-z0-9_]+)[\"']\s*,", re.MULTILINE)
SCRIPT_ID_RE = re.compile(r"^script_(?P<name>[A-Za-z0-9_]+)\s*=\s*(?P<value>-?\d+)\s*$", re.MULTILINE)
OPERATION_ID_RE = re.compile(r"^(?P<name>[A-Za-z][A-Za-z0-9_]*)\s*=\s*(?P<value>\d+)\s*(?:#.*)?$", re.MULTILINE)


class RglLogSentinelError(RuntimeError):
    """The log sentinel could not establish trustworthy local evidence."""


# This is intentionally a narrow, explicit engine contract.  It prevents the
# exact class of invalid dynamic-party callback failure without pretending that
# every local script parameter is an engine-owned party handle.
ENGINE_PARTY_CALLBACK_CONTRACTS: tuple[dict[str, Any], ...] = (
    {
        "id": "game-event-simulate-battle-active-root-parties",
        "script": "game_event_simulate_battle",
        "source_path": "src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py",
        "party_parameters": (":root_defender_party", ":root_attacker_party"),
        "active_gate": '(eq, ":root_parties_active", 1)',
        "unsafe_operations": (
            "store_faction_of_party",
            "party_collect_attachments_to_party",
            "party_slot_eq",
            "party_slot_ge",
            "party_slot_gt",
            "party_get_",
            "party_set_",
            "party_clear",
            "party_add_",
            "party_remove_",
            "inflict_casualties_to_party_group",
            "store_distance_to_party_from_party",
        ),
    },
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def compact(value: object, maximum: int = 500) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    return text if len(text) <= maximum else text[: maximum - 3] + "..."


def line_number(raw: str, offset: int) -> int:
    return raw.count("\n", 0, offset) + 1


def sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise RglLogSentinelError(f"Could not hash {path}: {error}") from error


def require_limit(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_LIMIT:
        raise RglLogSentinelError(f"limit must be an integer from 1 through {MAX_LIMIT}.")
    return value


def require_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise RglLogSentinelError(f"{label} does not exist or is not a file: {resolved}")
    return resolved


def require_directory(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_dir():
        raise RglLogSentinelError(f"{label} does not exist or is not a directory: {resolved}")
    return resolved


def unique_preserving_order(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def parse_script_errors(raw: str) -> list[dict[str, Any]]:
    """Parse every RGL script error, including multiple errors on one line."""

    starts = list(SCRIPT_ERROR_START_RE.finditer(raw))
    events: list[dict[str, Any]] = []
    for ordinal, match in enumerate(starts, start=1):
        end = starts[ordinal].start() if ordinal < len(starts) else len(raw)
        chunk = raw[match.start() : end]
        line_match = ENGINE_LINE_RE.search(chunk)
        message_end = line_match.start() if line_match is not None else len(chunk)
        message_start = match.end() - match.start()
        message = chunk[message_start:message_end].strip(" ;\t\r\n")
        scripts = unique_preserving_order(trace.group("script") for trace in SCRIPT_TRACE_RE.finditer(chunk))
        invalid = INVALID_ID_RE.search(message)
        resource_kind = invalid.group("kind").lower() if invalid is not None else None
        resource_id = int(invalid.group("value")) if invalid is not None else None
        events.append(
            {
                "id": f"rgl:error:{ordinal:04d}",
                "ordinal": ordinal,
                "log_line": line_number(raw, match.start()),
                "opcode": int(match.group("opcode")),
                "engine_line": int(line_match.group("line")) if line_match is not None else None,
                "message": message,
                "resource_kind": resource_kind,
                "resource_id": resource_id,
                "script": scripts[0] if scripts else None,
                "script_trace": scripts,
                "raw": compact(chunk),
            }
        )
    return events


def classify_warning(message: str) -> tuple[str, bool, str | None]:
    presentation = PRESENTATION_WARNING_RE.search(message)
    if presentation is not None:
        name = presentation.group("name")
        expected = name in {"prsnt_game_start", "prsnt_game_escape"}
        return (
            "mb1011_optional_presentation_mapping" if expected else "presentation_mapping",
            not expected,
            name,
        )
    material = MATERIAL_WARNING_RE.search(message)
    if material is not None:
        return "missing_material", True, material.group("name")
    return "engine_warning", False, None


def parse_warnings(raw: str) -> list[dict[str, Any]]:
    """Return bounded, classed warning evidence without confusing it with script errors."""

    warnings: list[dict[str, Any]] = []
    for ordinal, match in enumerate(WARNING_RE.finditer(raw), start=1):
        message = match.group("message").strip()
        category, actionable, subject = classify_warning(message)
        warnings.append(
            {
                "id": f"rgl:warning:{ordinal:04d}",
                "log_line": line_number(raw, match.start()),
                "category": category,
                "actionable": actionable,
                "subject": subject,
                "message": message,
            }
        )
    for ordinal, match in enumerate(VERTEX_BUFFER_RE.finditer(raw), start=1):
        warnings.append(
            {
                "id": f"rgl:info:vertex-buffer:{ordinal:04d}",
                "log_line": line_number(raw, match.start()),
                "category": "engine_buffer_growth",
                "actionable": False,
                "subject": None,
                "message": "The engine expanded its static vertex buffer during startup.",
            }
        )
    return warnings


def summarize_warnings(rows: Sequence[Mapping[str, Any]], *, limit: int) -> tuple[list[dict[str, Any]], bool]:
    """Collapse repetitive startup/asset warnings without discarding raw evidence."""

    groups: dict[tuple[str, bool, str | None, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        key = (
            str(row["category"]),
            bool(row["actionable"]),
            row.get("subject") if isinstance(row.get("subject"), str) else None,
            str(row["message"]),
        )
        groups.setdefault(key, []).append(row)
    summary = [
        {
            "category": key[0],
            "actionable": key[1],
            "subject": key[2],
            "message": key[3],
            "count": len(group),
            "first_log_line": group[0]["log_line"],
            "last_log_line": group[-1]["log_line"],
            "warning_ids": [row["id"] for row in group],
        }
        for key, group in groups.items()
    ]
    summary.sort(key=lambda row: (-row["count"], row["category"], row["message"]))
    return summary[:limit], len(summary) > limit


def build_script_catalog(root: Path) -> dict[str, list[dict[str, Any]]]:
    catalog: dict[str, list[dict[str, Any]]] = {}
    scripts_root = root / "src" / "scripts"
    if not scripts_root.is_dir():
        return catalog
    for path in sorted(scripts_root.rglob("*.py")):
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for match in SCRIPT_DECLARATION_RE.finditer(raw):
            catalog.setdefault(match.group("name"), []).append(
                {
                    "path": project_relative(path, root),
                    "line": line_number(raw, match.start()),
                }
            )
    return catalog


def build_generated_script_catalog(root: Path) -> dict[str, dict[str, Any]]:
    path = root / "compile" / "module_scripts.py"
    if not path.is_file():
        return {}
    raw = path.read_text(encoding="utf-8")
    return {
        match.group("name"): {"path": project_relative(path, root), "line": line_number(raw, match.start())}
        for match in SCRIPT_DECLARATION_RE.finditer(raw)
    }


def build_script_id_catalog(root: Path) -> dict[str, int]:
    path = root / "compile" / "ids" / "ID_scripts.py"
    if not path.is_file():
        return {}
    raw = path.read_text(encoding="utf-8")
    return {match.group("name"): int(match.group("value")) for match in SCRIPT_ID_RE.finditer(raw)}


def build_operation_catalog(root: Path) -> dict[int, str]:
    """Map legacy numeric engine opcodes to the checked-in header names."""

    path = root / "compile" / "headers" / "header_operations.py"
    if not path.is_file():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    return {int(match.group("value")): match.group("name") for match in OPERATION_ID_RE.finditer(raw)}


def annotate_operation_names(events: Sequence[Mapping[str, Any]], operation_catalog: Mapping[int, str]) -> list[dict[str, Any]]:
    """Keep raw RGL opcode evidence while making it immediately readable."""

    return [
        {
            **event,
            "opcode_name": operation_catalog.get(int(event["opcode"])),
        }
        for event in events
    ]


def build_export_script_catalog(root: Path) -> dict[str, dict[str, Any]]:
    path = root / "_export" / "scripts.txt"
    if not path.is_file():
        return {}
    catalog: dict[str, dict[str, Any]] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return catalog
    for index, line in enumerate(lines, start=1):
        if not line.endswith(" -1"):
            continue
        name = line[:-3]
        if re.fullmatch(r"[A-Za-z0-9_]+", name):
            catalog[name] = {
                "path": project_relative(path, root),
                "header_line": index,
                "body_line": index + 1 if index < len(lines) else None,
            }
    return catalog


def script_provenance(
    root: Path,
    script: str | None,
    source_catalog: Mapping[str, list[dict[str, Any]]],
    generated_catalog: Mapping[str, dict[str, Any]],
    id_catalog: Mapping[str, int],
    export_catalog: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    if script is None:
        return {
            "script": None,
            "source": {"state": "unmapped", "records": []},
            "generated": {"state": "unmapped"},
            "export": {"state": "unmapped"},
            "script_id": None,
        }
    source_records = source_catalog.get(script, [])
    return {
        "script": script,
        "source": {
            "state": "found" if len(source_records) == 1 else "ambiguous" if source_records else "missing",
            "records": source_records,
        },
        "generated": {"state": "found", **generated_catalog[script]} if script in generated_catalog else {"state": "missing"},
        "export": {"state": "found", **export_catalog[script]} if script in export_catalog else {"state": "missing"},
        "script_id": id_catalog.get(script),
    }


def normalized_lines(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def first_unsafe_party_use(lines: Sequence[str], parameter: str, unsafe_operations: Sequence[str]) -> int | None:
    for index, line in enumerate(lines):
        if parameter not in line or "party_is_active" in line:
            continue
        if any(f"({operation}" in line for operation in unsafe_operations):
            return index
    return None


def active_gate_has_stale_party_result(lines: Sequence[str], active_gate_index: int) -> bool:
    """Prove the direct failed branch of the active-root gate ends the callback."""

    start = next((index for index in range(active_gate_index - 1, -1, -1) if lines[index].startswith("(try_begin")), None)
    if start is None:
        return False
    depth = 0
    fallback_start: int | None = None
    fallback_end: int | None = None
    for index in range(start, len(lines)):
        line = lines[index]
        if line.startswith("(try_begin") or line.startswith("(try_for_"):
            depth += 1
        elif line.startswith("(else_try") and depth == 1:
            fallback_start = index
        elif line.startswith("(try_end"):
            if depth == 1:
                fallback_end = index
                break
            depth -= 1
    if fallback_start is None or fallback_end is None:
        return False
    return any('(set_trigger_result, 1)' in line for line in lines[fallback_start + 1 : fallback_end])


def evaluate_engine_callback_contract_source(root: Path, contract: Mapping[str, Any]) -> dict[str, Any]:
    relative = Path(str(contract["source_path"]))
    path = root / relative
    if not path.is_file():
        finding = {
            "contract_id": contract["id"],
            "script": contract["script"],
            "path": relative.as_posix(),
            "severity": "error",
            "code": "engine_callback_source_missing",
            "message": f"Required engine callback source is missing: {relative.as_posix()}.",
        }
        return {"id": contract["id"], "script": contract["script"], "path": relative.as_posix(), "passed": False, "checks": [], "findings": [finding]}

    raw = path.read_text(encoding="utf-8")
    lines = normalized_lines(raw)
    script_token = f'(\"{contract["script"]}\",'
    script_declared = script_token in raw
    active_gate = str(contract["active_gate"])
    active_gate_index = next((index for index, line in enumerate(lines) if active_gate in line), None)
    checks: list[dict[str, Any]] = [
        {
            "id": "script_declared",
            "passed": script_declared,
            "message": f"{contract['script']} remains declared in its protected source fragment.",
        }
    ]
    guard_indices: list[int] = []
    for parameter in contract["party_parameters"]:
        guard = f'(party_is_active, "{parameter}")'
        guard_index = next((index for index, line in enumerate(lines) if guard in line), None)
        unsafe_index = first_unsafe_party_use(lines, parameter, contract["unsafe_operations"])
        passed = guard_index is not None and (unsafe_index is None or guard_index < unsafe_index)
        guard_indices.append(guard_index if guard_index is not None else -1)
        checks.append(
            {
                "id": f"active_guard_before_party_read:{parameter}",
                "passed": passed,
                "guard": guard,
                "guard_line": guard_index + 1 if guard_index is not None else None,
                "first_unsafe_line": unsafe_index + 1 if unsafe_index is not None else None,
                "message": f"{parameter} must be checked with party_is_active before its first faction or party read.",
            }
        )
    gate_after_guards = active_gate_index is not None and all(index >= 0 and index < active_gate_index for index in guard_indices)
    gate_before_reads = active_gate_index is not None and all(
        (unsafe := first_unsafe_party_use(lines, parameter, contract["unsafe_operations"])) is None or active_gate_index < unsafe
        for parameter in contract["party_parameters"]
    )
    checks.append(
        {
            "id": "active_root_gate",
            "passed": gate_after_guards and gate_before_reads,
            "gate": active_gate,
            "gate_line": active_gate_index + 1 if active_gate_index is not None else None,
            "message": "Validated dynamic-party handles must control the battle branch before any unsafe party operation.",
        }
    )
    checks.append(
        {
            "id": "inactive_root_finishes_callback",
            "passed": active_gate_index is not None and active_gate_has_stale_party_result(lines, active_gate_index),
            "message": "The failed active-root branch must set the trigger result and end the stale simulation.",
        }
    )
    findings = [
        {
            "contract_id": contract["id"],
            "script": contract["script"],
            "path": relative.as_posix(),
            "severity": "error",
            "code": "engine_callback_party_handle_contract",
            "check_id": check["id"],
            "message": check["message"],
        }
        for check in checks
        if not check["passed"]
    ]
    return {
        "id": contract["id"],
        "script": contract["script"],
        "path": relative.as_posix(),
        "passed": not findings,
        "checks": checks,
        "findings": findings,
    }


def engine_callback_contract_report(root: Path = DEFAULT_REPO_ROOT, *, limit: int = 50) -> dict[str, Any]:
    """Evaluate checked-in engine callback contracts without reading a gameplay log."""

    maximum = require_limit(limit)
    resolved_root = require_directory(Path(root), "repo root")
    contracts = [evaluate_engine_callback_contract_source(resolved_root, contract) for contract in ENGINE_PARTY_CALLBACK_CONTRACTS]
    all_findings = [finding for contract in contracts for finding in contract["findings"]]
    returned = all_findings[:maximum]
    return {
        "contract_version": "devkit.engine-party-callback-contract.v1",
        "tool_version": f"devkit.rgl-log-sentinel.v{SENTINEL_VERSION}",
        "repo_root": str(resolved_root),
        "read_only": True,
        "passed": not all_findings,
        "contract_count": len(contracts),
        "failed_contract_count": sum(1 for contract in contracts if not contract["passed"]),
        "finding_count": len(all_findings),
        "findings": returned,
        "findings_truncated": len(all_findings) > len(returned),
        "contracts": contracts,
        "warnings": [],
    }


def compare_live_export(root: Path, live_module: Path | None, *, limit: int) -> dict[str, Any]:
    """Hash-compare workspace exports to an explicitly supplied live module."""

    export_dir = root / "_export"
    if live_module is None:
        return {
            "state": "not_checked",
            "checked": False,
            "workspace_export": project_relative(export_dir, root),
            "message": "No live module directory was supplied; deployment freshness was not checked.",
            "files": [],
        }
    live = require_directory(live_module, "live module directory")
    if not export_dir.is_dir():
        return {
            "state": "workspace_export_missing",
            "checked": False,
            "workspace_export": project_relative(export_dir, root),
            "live_module": str(live),
            "message": "Workspace _export directory is absent; a fresh build is required before deployment comparison.",
            "files": [],
        }
    export_files = sorted(path for path in export_dir.glob("*.txt") if path.is_file())
    rows: list[dict[str, Any]] = []
    for exported in export_files:
        live_file = live / exported.name
        if not live_file.is_file():
            rows.append({"filename": exported.name, "state": "missing_live", "workspace_sha256": sha256(exported), "live_sha256": None})
            continue
        workspace_hash = sha256(exported)
        live_hash = sha256(live_file)
        rows.append(
            {
                "filename": exported.name,
                "state": "match" if workspace_hash == live_hash else "mismatch",
                "workspace_sha256": workspace_hash,
                "live_sha256": live_hash,
            }
        )
    mismatches = [row for row in rows if row["state"] != "match"]
    return {
        "state": "match" if not mismatches else "mismatch",
        "checked": True,
        "workspace_export": project_relative(export_dir, root),
        "live_module": str(live),
        "checked_file_count": len(rows),
        "matching_file_count": len(rows) - len(mismatches),
        "mismatch_file_count": len(mismatches),
        "scripts_txt_state": next((row["state"] for row in rows if row["filename"] == "scripts.txt"), "missing_workspace"),
        "files": mismatches[:limit],
        "files_truncated": len(mismatches) > min(len(mismatches), limit),
    }


def cluster_script_errors(
    root: Path,
    events: Sequence[Mapping[str, Any]],
    contract_report: Mapping[str, Any],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    """Group contiguous script errors into a single causal chain per callback."""

    source_catalog = build_script_catalog(root)
    generated_catalog = build_generated_script_catalog(root)
    id_catalog = build_script_id_catalog(root)
    export_catalog = build_export_script_catalog(root)
    by_script = {contract["script"]: contract for contract in contract_report["contracts"]}
    raw_clusters: list[list[Mapping[str, Any]]] = []
    for event in events:
        if raw_clusters and raw_clusters[-1][-1].get("script") == event.get("script"):
            raw_clusters[-1].append(event)
        else:
            raw_clusters.append([event])
    clusters: list[dict[str, Any]] = []
    for ordinal, group in enumerate(raw_clusters, start=1):
        script = group[0].get("script")
        invalid_parties = sorted({int(event["resource_id"]) for event in group if event.get("resource_kind") == "party" and event.get("resource_id") is not None})
        invalid_factions = sorted({int(event["resource_id"]) for event in group if event.get("resource_kind") == "faction" and event.get("resource_id") is not None})
        contract = by_script.get(script)
        if invalid_parties and invalid_factions:
            category = "invalid_party_faction_cascade"
            message = (
                f"{script or 'an unmapped callback'} received removed party handle(s) {invalid_parties}; "
                f"later faction reads received undefined value(s) {invalid_factions}."
            )
        elif invalid_parties:
            category = "invalid_party_handle"
            message = f"{script or 'an unmapped callback'} received invalid party handle(s) {invalid_parties}."
        elif invalid_factions:
            category = "invalid_faction_handle"
            message = f"{script or 'an unmapped callback'} received invalid faction handle(s) {invalid_factions}."
        else:
            category = "script_error_chain"
            message = f"{script or 'an unmapped callback'} produced {len(group)} contiguous engine script error(s)."
        clusters.append(
            {
                "id": f"rgl:cluster:{ordinal:04d}",
                "category": category,
                "severity": "error",
                "script": script,
                "message": message,
                "event_count": len(group),
                "event_ids": [event["id"] for event in group],
                "invalid_party_ids": invalid_parties,
                "invalid_faction_ids": invalid_factions,
                "engine_opcodes": sorted({event["opcode"] for event in group}),
                "engine_operations": [
                    {
                        "opcode": opcode,
                        "name": next(
                            (event.get("opcode_name") for event in group if event["opcode"] == opcode),
                            None,
                        ),
                    }
                    for opcode in sorted({event["opcode"] for event in group})
                ],
                "engine_line_numbers": sorted({event["engine_line"] for event in group if event.get("engine_line") is not None}),
                "provenance": script_provenance(root, script, source_catalog, generated_catalog, id_catalog, export_catalog),
                "current_contract": {
                    "state": "covered_pass" if contract is not None and contract["passed"] else "covered_fail" if contract is not None else "uncovered",
                    "contract_id": contract["id"] if contract is not None else None,
                    "finding_count": len(contract["findings"]) if contract is not None else None,
                },
                "recommended_next_step": (
                    "Rebuild and deploy the reviewed export before retesting."
                    if contract is not None and contract["passed"]
                    else "Inspect the mapped source path and add a guarded party-handle contract before rebuilding."
                ),
            }
        )
    return clusters[:limit]


def analysis_state(
    events: Sequence[Mapping[str, Any]],
    clusters: Sequence[Mapping[str, Any]],
    contract_report: Mapping[str, Any],
    deployment: Mapping[str, Any],
) -> str:
    if not contract_report["passed"]:
        return "blocked_by_static_contract"
    if not events:
        return "clean" if deployment.get("state") in {"match", "not_checked"} else "deployment_attention"
    if any(cluster["current_contract"]["state"] in {"covered_fail", "uncovered"} for cluster in clusters):
        return "runtime_error_unresolved"
    if deployment.get("state") == "mismatch":
        return "runtime_error_remediated_source_live_export_stale"
    return "runtime_error_observed_source_contract_passes"


def analyze_log(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    log_path: Path,
    live_module: Path | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """Analyze one gameplay log against the current workspace and optional live module."""

    maximum = require_limit(limit)
    resolved_root = require_directory(Path(root), "repo root")
    log = require_file(Path(log_path), "RGL log")
    try:
        raw = log.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise RglLogSentinelError(f"Could not read RGL log {log}: {error}") from error
    events = annotate_operation_names(parse_script_errors(raw), build_operation_catalog(resolved_root))
    warning_rows = parse_warnings(raw)
    warning_groups, warning_groups_truncated = summarize_warnings(warning_rows, limit=maximum)
    contract_report = engine_callback_contract_report(resolved_root, limit=maximum)
    clusters = cluster_script_errors(resolved_root, events, contract_report, limit=maximum)
    deployment = compare_live_export(resolved_root, Path(live_module) if live_module is not None else None, limit=maximum)
    state = analysis_state(events, clusters, contract_report, deployment)
    warning_counts = Counter(row["category"] for row in warning_rows)
    actionable_warnings = [row for row in warning_rows if row["actionable"]]
    tool_warnings: list[str] = []
    if deployment["state"] == "not_checked":
        tool_warnings.append(deployment["message"])
    elif deployment["state"] == "mismatch":
        tool_warnings.append("The live module differs from workspace _export; gameplay may still exercise an older build.")
    if actionable_warnings:
        tool_warnings.append(f"{len(actionable_warnings)} actionable non-script engine warning(s) were observed.")
    return {
        "contract_version": "devkit.rgl-log-sentinel.v1",
        "tool_version": f"devkit.rgl-log-sentinel.v{SENTINEL_VERSION}",
        "generated_at_utc": utc_now(),
        "scope": {
            "repo_root": str(resolved_root),
            "log_path": str(log),
            "log_sha256": sha256(log),
            "live_module": str(Path(live_module).expanduser().resolve()) if live_module is not None else None,
            "read_only": True,
        },
        "summary": {
            "state": state,
            "script_error_count": len(events),
            "error_cluster_count": len(clusters),
            "invalid_party_faction_cascade_count": sum(1 for cluster in clusters if cluster["category"] == "invalid_party_faction_cascade"),
            "warning_count": len(warning_rows),
            "actionable_warning_count": len(actionable_warnings),
            "warning_categories": dict(sorted(warning_counts.items())),
            "current_engine_callback_contract_passed": contract_report["passed"],
            "deployment_state": deployment["state"],
        },
        "clusters": clusters,
        "script_errors": events[:maximum],
        "script_errors_truncated": len(events) > min(len(events), maximum),
        "warnings": warning_rows[:maximum],
        "warnings_truncated": len(warning_rows) > min(len(warning_rows), maximum),
        "warning_groups": warning_groups,
        "warning_groups_truncated": warning_groups_truncated,
        "engine_callback_contract": contract_report,
        "deployment": deployment,
        "evidence_boundary": [
            "RGL logs prove that the engine emitted an error; they do not reconstruct every save-state or native engine scheduler path.",
            "A passing callback contract proves the checked-in source has the declared guard shape, not that a separate live module directory has been deployed.",
            "The sentinel never changes source, generated modules, exports, save games, or a live module directory.",
        ],
        "tool_warnings": tool_warnings,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# RGL Log Sentinel",
        "",
        f"State: **{summary['state']}**.",
        "",
        f"- Script errors: {summary['script_error_count']}",
        f"- Error clusters: {summary['error_cluster_count']}",
        f"- Invalid-party/faction cascades: {summary['invalid_party_faction_cascade_count']}",
        f"- Actionable warnings: {summary['actionable_warning_count']}",
        f"- Current engine callback contract: {'PASS' if summary['current_engine_callback_contract_passed'] else 'BLOCKED'}",
        f"- Deployment: `{summary['deployment_state']}`",
    ]
    clusters = report.get("clusters", [])
    if clusters:
        lines.extend(["", "## Root-cause clusters", ""])
        for cluster in clusters:
            lines.append(f"- **{cluster['category']}** in `{cluster['script'] or 'unmapped'}` — {cluster['message']}")
            provenance = cluster["provenance"]
            source = provenance["source"]
            if source["records"]:
                record = source["records"][0]
                lines.append(f"  - Source: `{record['path']}:{record['line']}`")
            operations = ", ".join(
                f"{operation['opcode']} ({operation['name'] or 'unmapped'})"
                for operation in cluster.get("engine_operations", [])
            )
            if operations:
                lines.append(f"  - Engine operations: `{operations}`")
            lines.append(f"  - Current contract: `{cluster['current_contract']['state']}`")
            lines.append(f"  - Next step: {cluster['recommended_next_step']}")
    deployment = report.get("deployment", {})
    if deployment.get("checked"):
        lines.extend(["", "## Deployment freshness", ""])
        lines.append(
            f"- `{deployment['matching_file_count']}/{deployment['checked_file_count']}` exported text file(s) match the supplied live module; {deployment['mismatch_file_count']} differ."
        )
        for row in deployment.get("files", [])[:10]:
            lines.append(f"  - `{row['filename']}`: {row['state']}")
    warnings = report.get("warning_groups", [])
    if warnings:
        lines.extend(["", "## Other engine warnings", ""])
        for warning in warnings[:10]:
            prefix = "actionable" if warning["actionable"] else "informational"
            count = f" ×{warning['count']}" if warning["count"] > 1 else ""
            lines.append(f"- `{warning['category']}` ({prefix}){count}: {warning['message']}")
    tool_warnings = report.get("tool_warnings", [])
    if tool_warnings:
        lines.extend(["", "## Tool warnings", "", *(f"- {warning}" for warning in tool_warnings)])
    return "\n".join(lines) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only RGL gameplay-log diagnosis and engine-callback contract checks for SoD Modern.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze", help="Map gameplay log errors to source/generated/export evidence.")
    analyze.add_argument("--log", required=True, type=Path, help="Path to rgl_log.txt.")
    analyze.add_argument("--live-module", type=Path, default=None, help="Optional live Module directory to compare with _export.")
    analyze.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    analyze.add_argument("--limit", type=int, default=50)
    analyze.add_argument("--format", choices=("json", "markdown"), default="json")
    contract = subparsers.add_parser("contract", help="Check engine callback party-handle guards before a build or release.")
    contract.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    contract.add_argument("--limit", type=int, default=50)
    contract.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "analyze":
            report = analyze_log(args.root, log_path=args.log, live_module=args.live_module, limit=args.limit)
            output = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2, sort_keys=True) + "\n"
            sys.stdout.write(output)
            return 0 if report["summary"]["script_error_count"] == 0 and report["engine_callback_contract"]["passed"] and report["deployment"]["state"] in {"match", "not_checked"} else 1
        report = engine_callback_contract_report(args.root, limit=args.limit)
        if args.format == "markdown":
            rendered = {
                "summary": {
                    "state": "clean" if report["passed"] else "blocked_by_static_contract",
                    "script_error_count": 0,
                    "error_cluster_count": 0,
                    "invalid_party_faction_cascade_count": 0,
                    "actionable_warning_count": 0,
                    "current_engine_callback_contract_passed": report["passed"],
                    "deployment_state": "not_checked",
                },
                "clusters": [],
                "deployment": {"checked": False},
                "warnings": [],
                "tool_warnings": [],
            }
            sys.stdout.write(render_markdown(rendered))
        else:
            sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return 0 if report["passed"] else 1
    except RglLogSentinelError as error:
        print(f"rgl_log_sentinel: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
