#!/usr/bin/env python3
"""Semantic change snapshots for an order-sensitive M&B 1.011 workspace.

Text diffs do not tell an LLM whether an edit changed NPC dialogue precedence,
a state writer, a visible string sink, an ID, a trigger's effects, or an export
artifact. This tool records those semantic surfaces as deterministic JSON and
compares them after an intentional edit/build. Baselines are confined to this
DevKit slice; it never writes canonical source, compile, or export files.
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
BASELINE_RELATIVE = Path("devkit/semantic_change_diff/baselines")
SCHEMA = "devkit.semantic-change-snapshot.v1"
DIFF_VERSION = "1.0.0"
ID_LINE_RE = re.compile(r"^\s*(?P<symbol>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>-?\d+)\s*$")
SLUG_RE = re.compile(r"[^a-z0-9]+")

if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.campaign_state_doctor import campaign_state_doctor as state_doctor
from devkit.dialogue_inspector import dialogue_inspector as dialogue
from devkit.string_integrity import string_integrity as string_integrity


class SemanticDiffError(RuntimeError):
    """The requested semantic snapshot or diff cannot be safely completed."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def digest(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_limit(value: int, maximum: int = 300) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise SemanticDiffError(f"limit must be an integer from 1 through {maximum}.")
    return value


def require_label(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SemanticDiffError("label must not be empty.")
    label = value.strip()
    if len(label) > 100:
        raise SemanticDiffError("label must be at most 100 characters.")
    return label


def slugify(value: str) -> str:
    return SLUG_RE.sub("-", value.casefold()).strip("-")[:80] or "baseline"


def baseline_path(root: Path, label: str) -> Path:
    checked = slugify(require_label(label))
    directory = (root / BASELINE_RELATIVE).resolve()
    path = (directory / f"{checked}.json").resolve()
    try:
        path.relative_to(directory)
    except ValueError as error:  # pragma: no cover - slugify already prevents it
        raise SemanticDiffError("Baseline path escaped the confined DevKit baseline directory.") from error
    return path


def route_identity(entry: dialogue.DialogueEntry) -> str:
    if entry.source is not None:
        return f"{entry.source.path}:L{entry.source.line_start}-L{entry.source.line_end}:{entry.speaker}:{entry.start_state}"
    return f"compile:{entry.compile_line}:{entry.speaker}:{entry.start_state}"


def dialogue_snapshot(root: Path) -> dict[str, Any]:
    inventory = dialogue.load_inventory(root)
    groups: dict[str, list[dict[str, Any]]] = {}
    raw_groups: dict[tuple[str, str], list[dialogue.DialogueEntry]] = {}
    for entry in inventory.entries:
        raw_groups.setdefault((entry.speaker, entry.start_state), []).append(entry)
    for (speaker, state), entries in sorted(raw_groups.items()):
        key = f"{speaker}::{state}"
        routes = []
        for position, entry in enumerate(sorted(entries, key=lambda value: value.index), start=1):
            semantic = {
                "route_id": route_identity(entry),
                "position": position,
                "speaker": entry.speaker,
                "start_state": entry.start_state,
                "end_state": entry.end_state,
                "is_player": entry.is_player,
                "conditions": re.sub(r"\s+", "", entry.conditions),
                "consequences": re.sub(r"\s+", "", entry.consequences),
                "text": entry.text,
                "string_ids": list(entry.string_ids),
                "string_registers": list(entry.string_registers),
            }
            routes.append({"route_id": semantic["route_id"], "fingerprint": digest(semantic), "semantic": semantic})
        groups[key] = routes
    return {
        "compiled_path": project_relative(inventory.compiled_path, root),
        "source_is_newer": inventory.source_is_newer,
        "group_count": len(groups),
        "groups": groups,
    }


def state_writer_snapshot(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    index = state_doctor.build_state_doctor(root)
    resources: dict[str, list[dict[str, Any]]] = {}
    for resource, accesses in index.accesses_by_resource.items():
        writers = []
        for access in accesses:
            if access.action != "write":
                continue
            operation = access.operation
            semantic = {
                "scope_kind": operation.scope_kind,
                "scope_id": operation.scope_id,
                "operation": operation.name,
                "args": list(operation.args),
                "value": access.value,
                "branch_path": list(operation.branch_path),
                "source": {"path": operation.path, "line": operation.line, "end_line": operation.end_line},
            }
            writers.append({"writer_id": f"{operation.scope_id}:{operation.path}:{operation.line}:{operation.ordinal}", "fingerprint": digest(semantic), "semantic": semantic})
        if writers:
            resources[resource] = sorted(writers, key=lambda item: (item["semantic"]["source"]["path"], item["semantic"]["source"]["line"], item["writer_id"]))
    triggers = {}
    for trigger_id, trigger in sorted(index.triggers.items()):
        semantic = {
            "interval": trigger.interval,
            "calls": list(trigger.calls),
            "operations": [
                {"name": operation.name, "args": list(operation.args), "branch_path": list(operation.branch_path)}
                for operation in trigger.operations
            ],
            "source": {"path": trigger.source.path, "line": trigger.source.line, "end_line": trigger.source.end_line},
        }
        triggers[trigger_id] = {"fingerprint": digest(semantic), "semantic": semantic}
    return resources, {
        "trigger_count": len(triggers),
        "triggers": triggers,
        "freshness": index.freshness,
    }


def string_sink_snapshot(root: Path) -> dict[str, Any]:
    report = string_integrity.build_integrity_report(root)
    sinks = {}
    for sink in report["sinks"]:
        source = sink.get("source") or {}
        key = f"{source.get('path', sink['compile_path'])}:{source.get('line_start', sink['compile_line'])}:{sink['kind']}:{sink['context']}"
        semantic = {
            "kind": sink["kind"],
            "context": sink["context"],
            "source": source,
            "text_input": sink["text_input"],
            "status": sink["status"],
            "register_assessments": [
                {
                    "register": assessment["register"],
                    "status": assessment["status"],
                    "issue_codes": [issue["code"] for issue in assessment.get("issues", [])],
                }
                for assessment in sink.get("register_assessments", [])
            ],
        }
        candidate = {"sink_id": sink["id"], "fingerprint": digest(semantic), "semantic": semantic}
        # More than one sink can share a source/context label. Preserve both
        # deterministically instead of losing a route due to a dictionary key.
        unique_key = key
        collision = 2
        while unique_key in sinks:
            unique_key = f"{key}#{collision}"
            collision += 1
        sinks[unique_key] = candidate
    return {
        "sink_count": len(sinks),
        "sinks": sinks,
        "summary": report["summary"],
    }


def id_snapshot(root: Path) -> dict[str, Any]:
    tables: dict[str, dict[str, int]] = {}
    directory = root / "compile" / "ids"
    if not directory.is_dir():
        return {"table_count": 0, "tables": tables}
    for path in sorted(directory.glob("ID_*.py"), key=lambda item: item.name.casefold()):
        entries: dict[str, int] = {}
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="cp1252").splitlines()
        except OSError:
            continue
        for line in lines:
            match = ID_LINE_RE.match(line)
            if match:
                entries[match.group("symbol")] = int(match.group("value"))
        tables[project_relative(path, root)] = entries
    return {"table_count": len(tables), "tables": tables}


def export_snapshot(root: Path) -> dict[str, Any]:
    directory = root / "_export"
    files = {}
    if directory.is_dir():
        for path in sorted(directory.glob("*.txt"), key=lambda item: item.name.casefold()):
            try:
                stat = path.stat()
            except OSError:
                continue
            files[path.name] = {"sha256": sha256_file(path), "bytes": stat.st_size}
    return {"file_count": len(files), "files": files}


def build_snapshot(root: Path = DEFAULT_REPO_ROOT) -> dict[str, Any]:
    root = root.resolve()
    if not (root / "compile").is_dir() or not (root / "src").is_dir():
        raise SemanticDiffError(f"Not a recognizable SoD Modern module workspace: {root}")
    try:
        dialogues = dialogue_snapshot(root)
        writers, triggers = state_writer_snapshot(root)
        strings = string_sink_snapshot(root)
    except (dialogue.InspectorError, state_doctor.CampaignStateError, string_integrity.StringIntegrityError) as error:
        raise SemanticDiffError(str(error)) from error
    return {
        "schema": SCHEMA,
        "created_at_utc": utc_now(),
        "repo_root": str(root),
        "dialogue_precedence": dialogues,
        "state_writers": {"resource_count": len(writers), "resources": writers},
        "string_sinks": strings,
        "generated_ids": id_snapshot(root),
        "trigger_effects": triggers,
        "exports": export_snapshot(root),
        "warnings": [
            "This snapshot is semantic static evidence. It does not execute the engine or certify a runtime/save-state path.",
            "Generated and export layers are observed read-only; build them through the normal reviewed workflow before interpreting an export delta as runtime output.",
        ],
    }


def validate_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, dict) or snapshot.get("schema") != SCHEMA:
        raise SemanticDiffError(f"Snapshot must use schema {SCHEMA}.")
    required = {"dialogue_precedence", "state_writers", "string_sinks", "generated_ids", "trigger_effects", "exports"}
    missing = sorted(required - set(snapshot))
    if missing:
        raise SemanticDiffError("Snapshot is missing semantic surfaces: " + ", ".join(missing))
    return dict(snapshot)


def write_baseline(root: Path, snapshot: Mapping[str, Any], *, label: str, overwrite: bool = False) -> dict[str, Any]:
    path = baseline_path(root, label)
    if path.exists() and not overwrite:
        raise SemanticDiffError(f"Baseline already exists: {project_relative(path, root)}. Use overwrite=true only after reviewing it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "baseline": {
            "label": slugify(label),
            "path": project_relative(path, root),
            "sha256": sha256_file(path),
            "created_at_utc": snapshot.get("created_at_utc"),
        },
        "mutation_scope": "A semantic baseline was written only under devkit/semantic_change_diff/baselines/; no module source, compile, or export file was changed.",
    }


def load_baseline(root: Path, label: str) -> tuple[Path, dict[str, Any]]:
    path = baseline_path(root, label)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SemanticDiffError(f"No semantic baseline named {slugify(label)!r}. Capture one before the edit with semantic_change_snapshot.") from error
    except (OSError, json.JSONDecodeError) as error:
        raise SemanticDiffError(f"Could not read semantic baseline {project_relative(path, root)}: {error}") from error
    return path, validate_snapshot(payload)


def sample(values: Sequence[Any], limit: int) -> tuple[list[Any], bool]:
    return list(values[:limit]), len(values) > limit


def keyed_delta(before: Mapping[str, Any], after: Mapping[str, Any], *, limit: int, value_fingerprint=lambda value: value) -> dict[str, Any]:
    before_keys = set(before)
    after_keys = set(after)
    added = sorted(after_keys - before_keys)
    removed = sorted(before_keys - after_keys)
    changed = sorted(key for key in before_keys & after_keys if value_fingerprint(before[key]) != value_fingerprint(after[key]))
    return {
        "added_count": len(added),
        "removed_count": len(removed),
        "changed_count": len(changed),
        "added": sample(added, limit)[0],
        "removed": sample(removed, limit)[0],
        "changed": sample(changed, limit)[0],
        "truncated": len(added) > limit or len(removed) > limit or len(changed) > limit,
    }


def dialogue_group_delta(before: Mapping[str, Any], after: Mapping[str, Any], limit: int) -> dict[str, Any]:
    raw = keyed_delta(before, after, limit=limit, value_fingerprint=lambda value: [route["route_id"] + ":" + route["fingerprint"] for route in value])
    groups = []
    for key in raw["changed"]:
        prior = before[key]
        current = after[key]
        old_ids = [route["route_id"] for route in prior]
        new_ids = [route["route_id"] for route in current]
        common = set(old_ids) & set(new_ids)
        moved = [identifier for identifier in common if old_ids.index(identifier) != new_ids.index(identifier)]
        changed_routes = [
            identifier
            for identifier in common
            if next(route["fingerprint"] for route in prior if route["route_id"] == identifier)
            != next(route["fingerprint"] for route in current if route["route_id"] == identifier)
        ]
        groups.append(
            {
                "group": key,
                "before_route_count": len(prior),
                "after_route_count": len(current),
                "added_route_ids": [identifier for identifier in new_ids if identifier not in old_ids][:limit],
                "removed_route_ids": [identifier for identifier in old_ids if identifier not in new_ids][:limit],
                "moved_route_ids": sorted(moved)[:limit],
                "changed_route_ids": sorted(changed_routes)[:limit],
                "before_precedence": old_ids[:limit],
                "after_precedence": new_ids[:limit],
            }
        )
    raw["groups"] = groups
    return raw


def id_delta(before: Mapping[str, Mapping[str, int]], after: Mapping[str, Mapping[str, int]], limit: int) -> dict[str, Any]:
    tables = []
    total = 0
    for table in sorted(set(before) | set(after)):
        old = before.get(table, {})
        new = after.get(table, {})
        delta = keyed_delta(old, new, limit=limit)
        total += delta["added_count"] + delta["removed_count"] + delta["changed_count"]
        if delta["added_count"] or delta["removed_count"] or delta["changed_count"]:
            delta["table"] = table
            delta["value_shifts"] = [
                {"symbol": symbol, "before": old[symbol], "after": new[symbol]}
                for symbol in delta["changed"]
            ]
            tables.append(delta)
    return {"table_change_count": len(tables), "symbol_change_count": total, "tables": tables[:limit], "truncated": len(tables) > limit}


def semantic_diff(before: Mapping[str, Any], after: Mapping[str, Any], *, limit: int = 100) -> dict[str, Any]:
    maximum = require_limit(limit)
    prior = validate_snapshot(before)
    current = validate_snapshot(after)
    dialogue_delta = dialogue_group_delta(prior["dialogue_precedence"]["groups"], current["dialogue_precedence"]["groups"], maximum)
    writer_delta = keyed_delta(
        prior["state_writers"]["resources"],
        current["state_writers"]["resources"],
        limit=maximum,
        value_fingerprint=lambda value: [item["writer_id"] + ":" + item["fingerprint"] for item in value],
    )
    string_delta = keyed_delta(
        prior["string_sinks"]["sinks"], current["string_sinks"]["sinks"], limit=maximum,
        value_fingerprint=lambda value: value["fingerprint"],
    )
    ids = id_delta(prior["generated_ids"]["tables"], current["generated_ids"]["tables"], maximum)
    trigger_delta = keyed_delta(
        prior["trigger_effects"]["triggers"], current["trigger_effects"]["triggers"], limit=maximum,
        value_fingerprint=lambda value: value["fingerprint"],
    )
    export_delta = keyed_delta(
        prior["exports"]["files"], current["exports"]["files"], limit=maximum,
        value_fingerprint=lambda value: value.get("sha256"),
    )
    counts = {
        "dialogue_precedence": dialogue_delta["added_count"] + dialogue_delta["removed_count"] + dialogue_delta["changed_count"],
        "state_writers": writer_delta["added_count"] + writer_delta["removed_count"] + writer_delta["changed_count"],
        "string_sinks": string_delta["added_count"] + string_delta["removed_count"] + string_delta["changed_count"],
        "generated_ids": ids["symbol_change_count"],
        "trigger_effects": trigger_delta["added_count"] + trigger_delta["removed_count"] + trigger_delta["changed_count"],
        "exports": export_delta["added_count"] + export_delta["removed_count"] + export_delta["changed_count"],
    }
    risk = "critical" if counts["generated_ids"] else "high" if counts["dialogue_precedence"] or counts["trigger_effects"] else "review" if any(counts.values()) else "clean"
    return {
        "semantic_change_diff_version": f"devkit.semantic-change-diff.v{DIFF_VERSION}",
        "before_created_at_utc": prior.get("created_at_utc"),
        "after_created_at_utc": current.get("created_at_utc"),
        "summary": {"risk_level": risk, "surface_change_counts": counts, "total_surface_change_count": sum(counts.values())},
        "dialogue_precedence": dialogue_delta,
        "state_writers": writer_delta,
        "string_sinks": string_delta,
        "generated_ids": ids,
        "trigger_effects": trigger_delta,
        "exports": export_delta,
        "next_steps": [
            "Inspect changed dialogue precedence before relying on an NPC route; first-match behavior can change even when text did not.",
            "Inspect changed state writers and trigger effects before testing campaign AI/lifecycle behavior.",
            "Treat generated-ID shifts as a deliberate compatibility decision, then inspect normal build/export diffs rather than overwriting them.",
            "Use String Integrity and Interprocedural String Provenance for changed sinks with register-related evidence.",
        ],
        "warnings": [*prior.get("warnings", []), *current.get("warnings", [])],
    }


def snapshot_payload(root: Path, *, label: str | None = None, overwrite: bool = False) -> dict[str, Any]:
    snapshot = build_snapshot(root)
    result = {"snapshot": snapshot}
    if label is not None:
        result.update(write_baseline(root, snapshot, label=label, overwrite=overwrite))
    else:
        result["mutation_scope"] = "Read-only current snapshot; supply a label to write a confined DevKit baseline."
    return result


def diff_payload(root: Path, *, baseline: str, limit: int = 100) -> dict[str, Any]:
    path, prior = load_baseline(root, baseline)
    current = build_snapshot(root)
    result = semantic_diff(prior, current, limit=limit)
    result["baseline"] = {"label": slugify(baseline), "path": project_relative(path, root), "sha256": sha256_file(path)}
    return result


def render_markdown(payload: Mapping[str, Any], command: str) -> str:
    if command == "diff":
        summary = payload["summary"]
        lines = [
            "# Semantic Change Diff",
            "",
            f"- Risk: {summary['risk_level']}; changed surfaces: {summary['total_surface_change_count']}.",
            *[f"- {key}: {value}" for key, value in summary["surface_change_counts"].items()],
        ]
    else:
        snapshot = payload["snapshot"]
        lines = [
            "# Semantic Change Snapshot",
            "",
            f"- Dialogue groups: {snapshot['dialogue_precedence']['group_count']:,}.",
            f"- State resources with writers: {snapshot['state_writers']['resource_count']:,}.",
            f"- Visible string sinks: {snapshot['string_sinks']['sink_count']:,}.",
        ]
    if payload.get("warnings"):
        lines.extend(["", "## Boundaries", "", *(f"- {warning}" for warning in payload["warnings"])])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cross-layer semantic snapshot and diff for SoD Modern edits.")
    parser.add_argument("command", choices=("snapshot", "diff"), nargs="?", default="snapshot")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--label", help="Optional confined baseline label for snapshot.")
    parser.add_argument("--baseline", help="Required baseline label for diff.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        if args.command == "snapshot":
            payload = snapshot_payload(root, label=args.label, overwrite=args.overwrite)
        else:
            if args.baseline is None:
                raise SemanticDiffError("--baseline is required for semantic diff.")
            payload = diff_payload(root, baseline=args.baseline, limit=args.limit)
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except SemanticDiffError as error:
        print(f"semantic_change_diff: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
