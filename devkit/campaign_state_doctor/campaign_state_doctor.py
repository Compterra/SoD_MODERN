#!/usr/bin/env python3
"""Read-only temporal state diagnostics for Mount & Blade 1.011 campaigns.

The compiler can validate a tuple of operations while still accepting two
scripts that overwrite the same party AI or slot state in a later campaign
tick.  This tool makes those temporal boundaries inspectable without claiming
to emulate the engine.  It reads canonical modular source, builds a bounded
script/trigger call model, and evaluates explicit state contracts.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ANALYZER_VERSION = "1.1.0"
TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
DEFAULT_CONTRACTS_PATH = TOOL_DIR / "contracts.json"

SOURCE_AREAS: tuple[tuple[str, str], ...] = (
    ("scripts", "src/scripts"),
    ("triggers", "src/triggers"),
)

CONTROL_OPEN = frozenset(
    {
        "try_begin",
        "try_for_agents",
        "try_for_attached_parties",
        "try_for_parties",
        "try_for_players",
        "try_for_prop_instances",
        "try_for_range",
        "try_for_range_backwards",
        "try_for_troops",
    }
)
CONTROL_ALTERNATE = frozenset({"else_try"})
CONTROL_CLOSE = frozenset({"try_end", "end_try"})
CONDITION_OPERATIONS = frozenset(
    {
        "eq",
        "neq",
        "ge",
        "gt",
        "le",
        "lt",
        "is_between",
        "party_is_active",
        "party_slot_eq",
        "party_slot_ge",
        "party_slot_gt",
        "party_slot_le",
        "party_slot_lt",
        "faction_slot_eq",
        "faction_slot_ge",
        "faction_slot_gt",
        "faction_slot_le",
        "faction_slot_lt",
        "troop_slot_eq",
        "troop_slot_ge",
        "troop_slot_gt",
        "troop_slot_le",
        "troop_slot_lt",
        "quest_slot_eq",
        "quest_slot_ge",
        "quest_slot_gt",
        "quest_slot_le",
        "quest_slot_lt",
        "check_quest_active",
        "check_quest_concluded",
        "check_quest_failed",
        "check_quest_succeeded",
        "is_currently_night",
        "main_party_has_troop",
    }
)

PARTY_AI_FIELDS = {
    "party_set_ai_behavior": "behavior",
    "party_set_ai_initiative": "initiative",
    "party_set_ai_object": "object",
    "party_set_ai_target_position": "target_position",
    "party_set_ai_patrol_radius": "patrol_radius",
    "script_party_set_ai_state": "state",
}
PARTY_SLOT_READ_PREFIXES = ("party_get_slot", "party_slot_")
FACTION_SLOT_READ_PREFIXES = ("faction_get_slot", "faction_slot_")
TROOP_SLOT_READ_PREFIXES = ("troop_get_slot", "troop_slot_")
TEMPORAL_AI_CATEGORIES = frozenset(
    {
        "party_ai_behavior",
        "party_ai_initiative",
        "party_ai_object",
        "party_ai_target_position",
        "party_ai_patrol_radius",
        "party_ai_state",
    }
)
GLOBAL_WRITE_PREFIXES = ("assign", "store_", "val_")
SYMBOL_RE = re.compile(r"(?<![A-Za-z0-9_])(?:\$[A-Za-z_][A-Za-z0-9_]*|:[A-Za-z_][A-Za-z0-9_]*)")


class CampaignStateError(RuntimeError):
    """The requested temporal state analysis cannot be completed safely."""


@dataclass(frozen=True)
class SourceRef:
    path: str
    line: int
    end_line: int


@dataclass(frozen=True)
class ConditionEvidence:
    operation_id: str
    name: str
    args: tuple[str, ...]
    source: SourceRef
    block_id: str
    branch: int


@dataclass
class Operation:
    id: str
    scope_kind: str
    scope_id: str
    path: str
    line: int
    end_line: int
    ordinal: int
    name: str
    args: tuple[str, ...]
    branch_path: tuple[tuple[str, int], ...] = ()
    conditions: tuple[ConditionEvidence, ...] = ()

    @property
    def source(self) -> SourceRef:
        return SourceRef(self.path, self.line, self.end_line)


@dataclass(frozen=True)
class StateAccess:
    id: str
    operation: Operation
    action: str
    category: str
    resource: str
    family: str
    subject: str
    value: str | None
    slot: str | None


@dataclass
class ScriptRecord:
    symbol: str
    source: SourceRef
    operations: list[Operation]
    calls: tuple[str, ...] = ()


@dataclass
class TriggerRecord:
    id: str
    source: SourceRef
    interval: str
    cadence: str
    operations: list[Operation]
    calls: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionPath:
    trigger_id: str
    cadence: str
    call_path: tuple[str, ...]


@dataclass
class StateDoctorIndex:
    root: Path
    contracts_path: Path
    source_files: tuple[str, ...]
    scripts: dict[str, ScriptRecord]
    triggers: dict[str, TriggerRecord]
    operations: tuple[Operation, ...]
    accesses: tuple[StateAccess, ...]
    accesses_by_resource: dict[str, list[StateAccess]]
    accesses_by_family: dict[str, list[StateAccess]]
    callers: dict[str, list[str]]
    trigger_paths: dict[str, list[ExecutionPath]]
    parse_findings: list[dict[str, Any]]
    contracts: list[dict[str, Any]]
    warnings: list[str]
    freshness: dict[str, Any]
    findings: list[dict[str, Any]] = field(default_factory=list)
    contract_results: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ControlFrame:
    id: str
    kind: str
    branch: int = 0
    conditions: list[ConditionEvidence] = field(default_factory=list)
    effect_seen: bool = False


_CACHE: dict[tuple[Path, Path], tuple[tuple[tuple[str, int, int], ...], StateDoctorIndex]] = {}


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text_compatible(path: Path) -> str:
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error
    raise CampaignStateError(f"Could not decode {path}: {last_error}")


def source_payload(source: SourceRef) -> dict[str, Any]:
    return {"path": source.path, "line": source.line, "end_line": source.end_line}


def require_limit(limit: int, maximum: int = 200) -> int:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= maximum:
        raise CampaignStateError(f"limit must be an integer from 1 through {maximum}.")
    return limit


def require_query(query: str | None, *, name: str = "query") -> str:
    if not isinstance(query, str) or not query.strip():
        raise CampaignStateError(f"{name} must not be empty.")
    if len(query) > 500:
        raise CampaignStateError(f"{name} must be at most 500 characters.")
    return query.strip()


def base_operation(name: str) -> str:
    return name.rsplit("|", 1)[-1]


def canonical_script_symbol(value: str) -> str:
    return value if value.startswith("script_") else f"script_{value}"


def expression_token(node: ast.AST) -> str:
    """Render an operand without importing or evaluating module source."""

    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return node.value
        if node.value is None:
            return "None"
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{expression_token(node.left)}|{expression_token(node.right)}"
    try:
        return ast.unparse(node).replace("\n", " ").strip()
    except Exception:  # pragma: no cover - defensive for malformed AST nodes
        return "<dynamic-expression>"


def operation_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if not isinstance(node, ast.Tuple) or not node.elts:
        return None
    head = node.elts[0]
    if isinstance(head, ast.Name):
        return head.id
    if isinstance(head, ast.BinOp) and isinstance(head.op, ast.BitOr):
        return expression_token(head)
    return None


def source_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for _, relative in SOURCE_AREAS:
        directory = root / relative
        if directory.is_dir():
            files.extend(path for path in directory.rglob("*.py") if "__pycache__" not in path.parts)
    return sorted(set(files), key=lambda path: project_relative(path, root).casefold())


def source_signature(root: Path, contracts_path: Path) -> tuple[tuple[str, int, int], ...]:
    paths = [*source_python_files(root), contracts_path]
    rows: list[tuple[str, int, int]] = []
    for path in paths:
        relative = project_relative(path, root)
        try:
            stat = path.stat()
        except OSError:
            rows.append((relative, -1, -1))
        else:
            rows.append((relative, stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def assignment_values(tree: ast.AST, name: str) -> list[ast.AST]:
    values: list[ast.AST] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            values.append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name and node.value is not None:
            values.append(node.value)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            values.append(node.value)
    return sorted(values, key=lambda value: (getattr(value, "lineno", 0), getattr(value, "col_offset", 0)))


def sequence_elements(node: ast.AST) -> list[ast.AST] | None:
    return list(node.elts) if isinstance(node, (ast.List, ast.Tuple)) else None


def parse_operations(
    node: ast.AST,
    *,
    scope_kind: str,
    scope_id: str,
    path: str,
    findings: list[dict[str, Any]],
) -> list[Operation]:
    elements = sequence_elements(node)
    if elements is None:
        findings.append(
            {
                "id": f"parse:{path}:{getattr(node, 'lineno', 0)}:{scope_id}",
                "severity": "warning",
                "category": "unsupported_dynamic_operation_block",
                "summary": f"{scope_id} has a non-literal operation block; the state doctor did not evaluate it.",
                "source": source_payload(SourceRef(path, getattr(node, "lineno", 0), getattr(node, "end_lineno", getattr(node, "lineno", 0)))),
            }
        )
        return []
    operations: list[Operation] = []
    for ordinal, item in enumerate(elements):
        name = operation_name(item)
        if name is None:
            continue
        args = tuple(expression_token(arg) for arg in item.elts[1:]) if isinstance(item, ast.Tuple) else ()
        line = getattr(item, "lineno", getattr(node, "lineno", 0))
        end_line = getattr(item, "end_lineno", line)
        operations.append(
            Operation(
                id=f"op:{path}:{line}:{getattr(item, 'col_offset', 0)}",
                scope_kind=scope_kind,
                scope_id=scope_id,
                path=path,
                line=line,
                end_line=end_line,
                ordinal=ordinal,
                name=name,
                args=args,
            )
        )
    annotate_control_flow(operations)
    return operations


def is_condition_operation(operation: Operation) -> bool:
    base = base_operation(operation.name)
    if base == "call_script":
        return bool(operation.args and operation.args[0].startswith("script_cf_"))
    if base in CONDITION_OPERATIONS:
        return True
    return (
        base.startswith(("party_slot_", "faction_slot_", "troop_slot_", "quest_slot_", "is_", "check_"))
        or operation.name.startswith(("neg|", "this_or_next|"))
    )


def accesses_for_operation(operation: Operation) -> list[StateAccess]:
    """Classify only durable campaign state, leaving locals as control evidence."""

    base = base_operation(operation.name)
    args = operation.args
    accesses: list[StateAccess] = []

    def add(
        action: str,
        category: str,
        subject: str,
        *,
        field: str | None = None,
        slot: str | None = None,
        value: str | None = None,
    ) -> None:
        resource_suffix = slot if slot is not None else field
        resource = f"{category}:{subject}" + (f":{resource_suffix}" if resource_suffix else "")
        family = f"{category}:*" + (f":{resource_suffix}" if resource_suffix else "")
        accesses.append(
            StateAccess(
                id=f"state:{operation.id}:{len(accesses)}",
                operation=operation,
                action=action,
                category=category,
                resource=resource,
                family=family,
                subject=subject,
                value=value,
                slot=slot,
            )
        )

    if base in PARTY_AI_FIELDS and args:
        field = PARTY_AI_FIELDS[base]
        value_index = 1 if base != "script_party_set_ai_state" else 1
        add("write", f"party_ai_{field}", args[0], field=field, value=args[value_index] if len(args) > value_index else None)
    elif base == "call_script" and len(args) >= 3 and args[0] == "script_party_set_ai_state":
        add("write", "party_ai_state", args[1], field="state", value=args[2])
    elif base == "party_set_slot" and len(args) >= 3:
        add("write", "party_slot", args[0], slot=args[1], value=args[2])
    elif base == "party_get_slot" and len(args) >= 3:
        add("read", "party_slot", args[1], slot=args[2])
    elif base.startswith("party_slot_") and len(args) >= 2:
        add("read", "party_slot", args[0], slot=args[1])
    elif base == "faction_set_slot" and len(args) >= 3:
        add("write", "faction_slot", args[0], slot=args[1], value=args[2])
    elif base == "faction_get_slot" and len(args) >= 3:
        add("read", "faction_slot", args[1], slot=args[2])
    elif base.startswith("faction_slot_") and len(args) >= 2:
        add("read", "faction_slot", args[0], slot=args[1])
    elif base == "troop_set_slot" and len(args) >= 3:
        add("write", "troop_slot", args[0], slot=args[1], value=args[2])
    elif base == "troop_get_slot" and len(args) >= 3:
        add("read", "troop_slot", args[1], slot=args[2])
    elif base.startswith("troop_slot_") and len(args) >= 2:
        add("read", "troop_slot", args[0], slot=args[1])
    elif base == "party_set_faction" and len(args) >= 2:
        add("write", "party_faction", args[0], field="faction", value=args[1])
    elif base == "party_set_icon" and len(args) >= 2:
        add("write", "party_icon", args[0], field="icon", value=args[1])
    elif base == "party_attach_to_party" and len(args) >= 2:
        add("write", "party_attachment", args[0], field="attached_to", value=args[1])
    elif base == "party_detach" and args:
        add("write", "party_attachment", args[0], field="attached_to", value="<none>")
    elif base == "remove_party" and args:
        add("write", "party_lifecycle", args[0], field="active", value="0")

    global_destination: str | None = None
    if args and args[0].startswith("$") and base.startswith(GLOBAL_WRITE_PREFIXES):
        global_destination = args[0]
        add("write", "global", global_destination, field="value", value=base)
    for argument in args:
        for symbol in SYMBOL_RE.findall(argument):
            if symbol.startswith("$") and symbol != global_destination:
                add("read", "global", symbol, field="value")
    return accesses


def operation_has_state_effect(operation: Operation) -> bool:
    if any(access.action == "write" for access in accesses_for_operation(operation)):
        return True
    base = base_operation(operation.name)
    if base == "call_script":
        return not (operation.args and operation.args[0].startswith("script_cf_"))
    return base.startswith(
        (
            "display_",
            "jump_",
            "spawn_",
            "remove_",
            "party_attach",
            "party_detach",
            "change_",
            "start_",
            "finish_",
        )
    )


def annotate_control_flow(operations: Sequence[Operation]) -> None:
    """Attach shallow branch evidence to operations in a generated-style block.

    It intentionally does not choose a branch.  A distinct branch marker proves
    mutual exclusion only within the same ``try`` block; any other overlap stays
    explicitly possible.
    """

    stack: list[_ControlFrame] = []
    counter = 0
    for operation in operations:
        base = base_operation(operation.name)
        if base in CONTROL_ALTERNATE:
            if stack:
                frame = stack[-1]
                frame.branch += 1
                frame.conditions = []
                frame.effect_seen = False
            operation.branch_path = tuple((frame.id, frame.branch) for frame in stack)
            operation.conditions = tuple(condition for frame in stack for condition in frame.conditions)
            continue
        if base in CONTROL_CLOSE:
            operation.branch_path = tuple((frame.id, frame.branch) for frame in stack)
            operation.conditions = tuple(condition for frame in stack for condition in frame.conditions)
            if stack:
                stack.pop()
            continue

        operation.branch_path = tuple((frame.id, frame.branch) for frame in stack)
        operation.conditions = tuple(condition for frame in stack for condition in frame.conditions)
        if base in CONTROL_OPEN:
            counter += 1
            stack.append(_ControlFrame(f"{operation.scope_id}:{operation.ordinal}:{counter}", base))
            continue

        if is_condition_operation(operation) and stack and not stack[-1].effect_seen:
            frame = stack[-1]
            frame.conditions.append(
                ConditionEvidence(
                    operation_id=operation.id,
                    name=operation.name,
                    args=operation.args,
                    source=operation.source,
                    block_id=frame.id,
                    branch=frame.branch,
                )
            )
        if operation_has_state_effect(operation):
            for frame in stack:
                frame.effect_seen = True


def direct_calls(operations: Iterable[Operation]) -> tuple[str, ...]:
    calls = [
        operation.args[0]
        for operation in operations
        if base_operation(operation.name) == "call_script" and operation.args and operation.args[0].startswith("script_")
    ]
    return tuple(dict.fromkeys(calls))


def cadence_label(interval: str) -> str:
    try:
        numeric = float(interval)
    except ValueError:
        return f"engine/event interval {interval}"
    if numeric == 1:
        return "every 1 hour"
    if numeric == 24:
        return "every 24 hours"
    return f"every {numeric:g} hours"


def parse_source(
    root: Path,
) -> tuple[dict[str, ScriptRecord], dict[str, TriggerRecord], list[dict[str, Any]], tuple[str, ...]]:
    scripts: dict[str, ScriptRecord] = {}
    triggers: dict[str, TriggerRecord] = {}
    findings: list[dict[str, Any]] = []
    files = source_python_files(root)
    for path in files:
        relative = project_relative(path, root)
        try:
            tree = ast.parse(read_text_compatible(path), filename=str(path))
        except (OSError, SyntaxError, CampaignStateError) as error:
            findings.append(
                {
                    "id": f"parse:{relative}",
                    "severity": "error",
                    "category": "source_parse_error",
                    "summary": f"Could not parse canonical source for state analysis: {error}",
                    "source": {"path": relative, "line": getattr(error, "lineno", 0), "end_line": getattr(error, "lineno", 0)},
                }
            )
            continue

        for collection in assignment_values(tree, "SCRIPTS"):
            entries = sequence_elements(collection)
            if entries is None:
                findings.append(
                    {
                        "id": f"parse:{relative}:{getattr(collection, 'lineno', 0)}:SCRIPTS",
                        "severity": "warning",
                        "category": "unsupported_dynamic_script_collection",
                        "summary": "A SCRIPTS assignment is non-literal and was not modeled.",
                        "source": source_payload(SourceRef(relative, getattr(collection, "lineno", 0), getattr(collection, "end_lineno", getattr(collection, "lineno", 0)))),
                    }
                )
                continue
            for entry in entries:
                parts = sequence_elements(entry)
                if parts is None or len(parts) < 2 or not isinstance(parts[0], ast.Constant) or not isinstance(parts[0].value, str):
                    continue
                symbol = canonical_script_symbol(parts[0].value)
                source = SourceRef(relative, getattr(entry, "lineno", 0), getattr(entry, "end_lineno", getattr(entry, "lineno", 0)))
                operations = parse_operations(parts[1], scope_kind="script", scope_id=symbol, path=relative, findings=findings)
                record = ScriptRecord(symbol=symbol, source=source, operations=operations)
                record.calls = direct_calls(operations)
                if symbol in scripts:
                    findings.append(
                        {
                            "id": f"duplicate-script:{symbol}",
                            "severity": "error",
                            "category": "duplicate_script_definition",
                            "summary": f"{symbol} has multiple canonical source definitions.",
                            "source": source_payload(source),
                        }
                    )
                    continue
                scripts[symbol] = record

        for collection in assignment_values(tree, "SIMPLE_TRIGGERS"):
            entries = sequence_elements(collection)
            if entries is None:
                findings.append(
                    {
                        "id": f"parse:{relative}:{getattr(collection, 'lineno', 0)}:SIMPLE_TRIGGERS",
                        "severity": "warning",
                        "category": "unsupported_dynamic_trigger_collection",
                        "summary": "A SIMPLE_TRIGGERS assignment is non-literal and was not modeled.",
                        "source": source_payload(SourceRef(relative, getattr(collection, "lineno", 0), getattr(collection, "end_lineno", getattr(collection, "lineno", 0)))),
                    }
                )
                continue
            for entry in entries:
                parts = sequence_elements(entry)
                if parts is None or len(parts) < 2:
                    continue
                interval = expression_token(parts[0])
                trigger_id = f"trigger:{relative}:{getattr(entry, 'lineno', 0)}"
                source = SourceRef(relative, getattr(entry, "lineno", 0), getattr(entry, "end_lineno", getattr(entry, "lineno", 0)))
                operations = parse_operations(parts[1], scope_kind="simple_trigger", scope_id=trigger_id, path=relative, findings=findings)
                record = TriggerRecord(
                    id=trigger_id,
                    source=source,
                    interval=interval,
                    cadence=cadence_label(interval),
                    operations=operations,
                )
                record.calls = direct_calls(operations)
                triggers[trigger_id] = record
    return scripts, triggers, findings, tuple(project_relative(path, root) for path in files)


def build_trigger_paths(
    scripts: Mapping[str, ScriptRecord],
    triggers: Mapping[str, TriggerRecord],
) -> tuple[dict[str, list[ExecutionPath]], list[str]]:
    paths: dict[str, list[ExecutionPath]] = defaultdict(list)
    warnings: list[str] = []
    seen: set[tuple[str, str, tuple[str, ...]]] = set()
    cycle_count = 0
    depth_cutoff_count = 0
    missing_symbols: set[str] = set()

    def walk(trigger: TriggerRecord, symbol: str, chain: tuple[str, ...], depth: int) -> None:
        nonlocal cycle_count, depth_cutoff_count
        if depth > 12:
            depth_cutoff_count += 1
            return
        key = (trigger.id, symbol, chain)
        if key in seen:
            return
        seen.add(key)
        paths[symbol].append(ExecutionPath(trigger.id, trigger.cadence, chain))
        record = scripts.get(symbol)
        if record is None:
            missing_symbols.add(symbol)
            return
        for child in record.calls:
            if child in chain:
                cycle_count += 1
                continue
            walk(trigger, child, (*chain, child), depth + 1)

    for trigger in triggers.values():
        for root_call in trigger.calls:
            walk(trigger, root_call, (root_call,), 1)
    if cycle_count:
        warnings.append(
            f"Static trigger-path expansion encountered {cycle_count:,} recursive call boundary/boundaries; recursive branches remain unresolved rather than being flattened into a fictional timeline."
        )
    if depth_cutoff_count:
        warnings.append(
            f"Static trigger-path expansion stopped at depth 12 on {depth_cutoff_count:,} branch(es); inspect a focused script/resource timeline for deeper call evidence."
        )
    if missing_symbols:
        sample = ", ".join(sorted(missing_symbols)[:8])
        suffix = "" if len(missing_symbols) <= 8 else ", ..."
        warnings.append(
            f"{len(missing_symbols):,} called script symbol(s) have no modeled canonical source definition: {sample}{suffix}."
        )
    return {key: value for key, value in paths.items()}, list(dict.fromkeys(warnings))


def compute_freshness(root: Path, source_files: Sequence[str]) -> dict[str, Any]:
    paths = [root / relative for relative in source_files]
    newest = max(paths, key=lambda path: path.stat().st_mtime_ns) if paths else None
    compile_files = [root / "compile" / "module_scripts.py", root / "compile" / "module_simple_triggers.py"]
    existing_compile = [path for path in compile_files if path.is_file()]
    newest_compile = max(existing_compile, key=lambda path: path.stat().st_mtime_ns) if existing_compile else None
    source_newer = bool(newest and (newest_compile is None or newest.stat().st_mtime_ns > newest_compile.stat().st_mtime_ns))
    return {
        "newest_source": project_relative(newest, root) if newest else None,
        "newest_compile": project_relative(newest_compile, root) if newest_compile else None,
        "source_is_newer_than_state_compile": source_newer,
    }


def conditions_payload(conditions: Sequence[ConditionEvidence]) -> list[dict[str, Any]]:
    return [
        {
            "operation_id": condition.operation_id,
            "name": condition.name,
            "args": list(condition.args),
            "source": source_payload(condition.source),
            "block_id": condition.block_id,
            "branch": condition.branch,
        }
        for condition in conditions
    ]


def operation_payload(operation: Operation) -> dict[str, Any]:
    return {
        "id": operation.id,
        "scope_kind": operation.scope_kind,
        "scope_id": operation.scope_id,
        "name": operation.name,
        "args": list(operation.args),
        "ordinal": operation.ordinal,
        "source": source_payload(operation.source),
        "branch_path": [{"block_id": block_id, "branch": branch} for block_id, branch in operation.branch_path],
        "conditions": conditions_payload(operation.conditions),
    }


def access_payload(access: StateAccess, index: StateDoctorIndex | None = None) -> dict[str, Any]:
    result = {
        "id": access.id,
        "action": access.action,
        "category": access.category,
        "resource": access.resource,
        "family": access.family,
        "subject": access.subject,
        "slot": access.slot,
        "value": access.value,
        "operation": operation_payload(access.operation),
    }
    if index is not None and access.operation.scope_kind == "script":
        paths = index.trigger_paths.get(access.operation.scope_id, [])
        result["trigger_paths"] = [
            {"trigger_id": path.trigger_id, "cadence": path.cadence, "call_path": list(path.call_path)}
            for path in paths[:8]
        ]
        result["trigger_path_count"] = len(paths)
    return result


def finding_access_payload(access: StateAccess, index: StateDoctorIndex) -> dict[str, Any]:
    """Keep finding lists compact; ``timeline`` exposes full branch evidence."""

    paths = index.trigger_paths.get(access.operation.scope_id, []) if access.operation.scope_kind == "script" else []
    return {
        "id": access.id,
        "category": access.category,
        "resource": access.resource,
        "subject": access.subject,
        "value": access.value,
        "operation": {
            "id": access.operation.id,
            "name": access.operation.name,
            "args": list(access.operation.args),
            "source": source_payload(access.operation.source),
        },
        "trigger_paths": [
            {"trigger_id": path.trigger_id, "cadence": path.cadence, "call_path": list(path.call_path)}
            for path in paths[:3]
        ],
        "trigger_path_count": len(paths),
    }


def paths_are_exclusive(left: Operation, right: Operation) -> bool:
    left_branches = dict(left.branch_path)
    right_branches = dict(right.branch_path)
    return any(left_branches[block] != right_branches[block] for block in left_branches.keys() & right_branches.keys())


def is_static_control_value(value: str) -> bool:
    """Return whether a token is a compile-time value, not a runtime register."""

    return (
        not value.startswith((":", "$"))
        and re.fullmatch(r"(?:-?\d+|[A-Za-z_][A-Za-z0-9_]*)", value) is not None
        and re.fullmatch(r"reg\d+", value) is None
    )


def strict_equality_requirement(condition: ConditionEvidence, local: str) -> str | None:
    """Return the exact value required for a local by an unmodified ``eq``."""

    if condition.name != "eq" or len(condition.args) != 2:
        return None
    left, right = condition.args
    if left == local:
        return right
    if right == local:
        return left
    return None


def operation_writes_local(operation: Operation, local: str) -> bool:
    """Conservatively identify a non-condition operation that replaces a local."""

    if not operation.args or operation.args[0] != local or is_condition_operation(operation):
        return False
    return base_operation(operation.name) not in (CONTROL_OPEN | CONTROL_ALTERNATE | CONTROL_CLOSE)


def local_guard_is_completed_before_later_write(left: StateAccess, right: StateAccess, script: ScriptRecord) -> bool:
    """Prove that a completed local assignment makes the later guard impossible.

    This is deliberately narrow: the value must be static, the assignment must
    be in the exact branch that performed the earlier AI write, no later local
    writer may intervene, and the later write must require a conflicting plain
    ``eq`` value.  It recognizes state machines such as ``:deployed = 1``
    followed by a fallback guarded by ``:deployed == 0`` without guessing at
    dynamic values or script effects.
    """

    operations = sorted(script.operations, key=lambda operation: operation.ordinal)
    operations_by_id = {operation.id: operation for operation in operations}

    for assignment in reversed(operations):
        if not left.operation.ordinal < assignment.ordinal < right.operation.ordinal:
            continue
        if base_operation(assignment.name) != "assign" or len(assignment.args) < 2:
            continue
        local, assigned_value = assignment.args[0], assignment.args[1]
        if not local.startswith(":") or not is_static_control_value(assigned_value):
            continue
        if assignment.branch_path != left.operation.branch_path:
            continue

        # A condition directly after the first write can abort the enclosing
        # branch before this assignment executes. Nested try blocks are safe:
        # their failure only closes the nested block before the assignment.
        if any(
            is_condition_operation(operation) and operation.branch_path == left.operation.branch_path
            for operation in operations
            if left.operation.ordinal < operation.ordinal < assignment.ordinal
        ):
            continue

        for condition in right.operation.conditions:
            required_value = strict_equality_requirement(condition, local)
            guard = operations_by_id.get(condition.operation_id)
            if (
                required_value is None
                or not is_static_control_value(required_value)
                or required_value == assigned_value
                or guard is None
                or not assignment.ordinal < guard.ordinal <= right.operation.ordinal
            ):
                continue

            # Do not carry the proof through another possible write before
            # the guard itself. Writes after the guard do not matter: that
            # branch cannot begin once its contradictory guard has failed.
            if any(
                operation_writes_local(operation, local) and not paths_are_exclusive(assignment, operation)
                for operation in operations
                if assignment.ordinal < operation.ordinal < guard.ordinal
            ):
                continue
            return True
    return False


def spawned_party_subject_is_rebound(left: StateAccess, right: StateAccess, script: ScriptRecord) -> bool:
    """Prove that the later local selector is a freshly spawned party.

    M&B places the party created by ``spawn_around_party`` in ``reg0``.  We
    accept only the direct ``assign :local, reg0`` form in the same exact block
    as the later write, so an earlier write through the reused local cannot be
    mistaken for a write to the newly created party.
    """

    subject = left.subject
    if not subject.startswith(":"):
        return False
    operations = sorted(script.operations, key=lambda operation: operation.ordinal)
    for index, assignment in enumerate(operations):
        if not left.operation.ordinal < assignment.ordinal < right.operation.ordinal:
            continue
        if base_operation(assignment.name) != "assign" or assignment.args[:2] != (subject, "reg0"):
            continue
        if index == 0:
            continue
        spawn = operations[index - 1]
        if (
            base_operation(spawn.name) == "spawn_around_party"
            and spawn.branch_path == assignment.branch_path == right.operation.branch_path
        ):
            return True
    return False


def is_explicit_ai_state_refresh(left: StateAccess, right: StateAccess) -> bool:
    """Identify an adjacent reset/reapply used to force AI initialization."""

    left_args = left.operation.args
    right_args = right.operation.args
    return (
        left.category == right.category == "party_ai_state"
        and left.value == "spai_undefined"
        and right.value not in {None, "spai_undefined"}
        and left.operation.ordinal + 1 == right.operation.ordinal
        and left.operation.branch_path == right.operation.branch_path
        and base_operation(left.operation.name) == base_operation(right.operation.name) == "call_script"
        and len(left_args) >= 4
        and len(right_args) >= 4
        and left_args[0] == right_args[0] == "script_party_set_ai_state"
        and left_args[1] == right_args[1]
        and left_args[3] == "-1"
    )


def operation_call_target(operation: Operation) -> str | None:
    if base_operation(operation.name) != "call_script" or not operation.args:
        return None
    return operation.args[0] if operation.args[0].startswith("script_") else None


def condition_has_token(condition: ConditionEvidence, token: str) -> bool:
    return token == condition.name or token in condition.args


def condition_matches_predicate(condition: ConditionEvidence, predicate: str) -> bool:
    return base_operation(condition.name) == "call_script" and bool(condition.args) and condition.args[0] == predicate


def local_slot_bindings(script: ScriptRecord) -> dict[str, set[str]]:
    bindings: dict[str, set[str]] = defaultdict(set)
    for operation in script.operations:
        base = base_operation(operation.name)
        if base in {"party_get_slot", "faction_get_slot", "troop_get_slot"} and len(operation.args) >= 3:
            bindings[operation.args[0]].add(operation.args[2])
    return dict(bindings)


def operation_is_travel_write(operation: Operation, travel_behavior: str) -> bool:
    return (
        base_operation(operation.name) == "party_set_ai_behavior"
        and len(operation.args) >= 2
        and operation.args[1] == travel_behavior
    )


def condition_origin_equals_target(
    conditions: Sequence[ConditionEvidence],
    bindings: Mapping[str, set[str]],
    origin_slot: str,
    target_slot: str,
) -> bool:
    origin_values = {symbol for symbol, slots in bindings.items() if origin_slot in slots}
    target_values = {symbol for symbol, slots in bindings.items() if target_slot in slots}
    for condition in conditions:
        if base_operation(condition.name) != "eq" or len(condition.args) < 2:
            continue
        left, right = condition.args[0], condition.args[1]
        if (left in origin_values and (right in target_values or "target" in right)) or (
            right in origin_values and (left in target_values or "target" in left)
        ):
            return True
    return False


def condition_has_comparison(conditions: Sequence[ConditionEvidence], operator: str, token: str) -> bool:
    return any(base_operation(condition.name) == operator and token in condition.args for condition in conditions)


def evaluate_stationary_camp(contract: Mapping[str, Any], index: StateDoctorIndex) -> dict[str, Any]:
    contract_id = str(contract.get("id", "<unnamed-contract>"))
    scope_scripts = tuple(str(value) for value in contract.get("scope_scripts", ()) if isinstance(value, str))
    predicate = str(contract.get("camped_predicate", ""))
    lock_script = str(contract.get("lock_script", ""))
    travel_behavior = str(contract.get("travel_behavior", "ai_bhvr_travel_to_party"))
    origin_slot = str(contract.get("origin_slot", ""))
    target_slot = str(contract.get("target_slot", ""))
    relocation_counter = str(contract.get("relocation_counter", ":days_camped"))
    approach_distance = str(contract.get("approach_distance", ":camp_target_dist"))
    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    predicate_record = index.scripts.get(predicate)
    checks.append(
        {
            "id": "camped_predicate_exists",
            "passed": predicate_record is not None,
            "message": f"Camped-state predicate {predicate} {'exists' if predicate_record is not None else 'is missing'}.",
            "evidence": [source_payload(predicate_record.source)] if predicate_record else [],
        }
    )

    lock_record = index.scripts.get(lock_script)
    hold_writes = [
        operation
        for operation in (lock_record.operations if lock_record else [])
        if base_operation(operation.name) == "party_set_ai_behavior" and len(operation.args) >= 2 and operation.args[1] == "ai_bhvr_hold"
    ]
    checks.append(
        {
            "id": "lock_script_holds_ai",
            "passed": bool(hold_writes),
            "message": f"Lock script {lock_script} {'sets hold AI' if hold_writes else 'does not prove a hold-AI write'}.",
            "evidence": [source_payload(operation.source) for operation in hold_writes],
        }
    )

    predicate_uses = 0
    for symbol in scope_scripts:
        script = index.scripts.get(symbol)
        lock_calls = [operation for operation in (script.operations if script else []) if operation_call_target(operation) == lock_script]
        checks.append(
            {
                "id": f"{symbol}:steady_lock",
                "passed": script is not None and bool(lock_calls),
                "message": (
                    f"{symbol} {'calls the lock helper' if lock_calls else 'does not call the lock helper'} "
                    "on a modeled state path."
                ),
                "evidence": [source_payload(operation.source) for operation in lock_calls],
            }
        )
        if script is None:
            continue
        bindings = local_slot_bindings(script)
        for operation in script.operations:
            if operation_call_target(operation) == predicate:
                predicate_uses += 1
            if not operation_is_travel_write(operation, travel_behavior):
                continue
            conditions = operation.conditions
            predicate_state = any(condition_matches_predicate(condition, predicate) for condition in conditions)
            slot_state = condition_origin_equals_target(conditions, bindings, origin_slot, target_slot) and condition_has_comparison(conditions, "le", approach_distance)
            relocation = condition_has_comparison(conditions, "ge", relocation_counter)
            approach = condition_has_comparison(conditions, "gt", approach_distance)
            if (predicate_state or slot_state) and not relocation and not approach:
                timeline = [
                    {
                        "step": 1,
                        "kind": "camped_state",
                        "message": "The active branch proves a pitched/camped state.",
                        "conditions": conditions_payload(conditions),
                    },
                    {
                        "step": 2,
                        "kind": "ai_write",
                        "message": f"The same branch assigns {travel_behavior} instead of stationary AI.",
                        "source": source_payload(operation.source),
                        "operation": operation_payload(operation),
                    },
                    {
                        "step": 3,
                        "kind": "contract_violation",
                        "message": "A pitched camp can move without an explicit relocation or approach transition.",
                    },
                ]
                violations.append(
                    {
                        "id": f"{contract_id}:{operation.id}",
                        "severity": "error",
                        "category": "stationary_camp_movement",
                        "summary": f"{symbol} can assign travel AI while the camped-state branch is active.",
                        "contract_id": contract_id,
                        "resource": f"party_ai:*:behavior",
                        "source": source_payload(operation.source),
                        "counterexample": timeline,
                        "recommendation": f"Route pitched-camp maintenance through {lock_script}; move only after clearing/replacing the camped target state.",
                    }
                )
    checks.append(
        {
            "id": "camped_predicate_used",
            "passed": predicate_uses > 0,
            "message": f"Camped-state predicate {predicate} is used by {predicate_uses} modeled contract scope(s).",
            "evidence": [],
        }
    )
    passed = not violations and all(check["passed"] for check in checks)
    return {
        "id": contract_id,
        "kind": "stationary_camp",
        "description": str(contract.get("description", "")),
        "passed": passed,
        "check_count": len(checks),
        "checks": checks,
        "violation_count": len(violations),
        "violations": violations,
        "limitations": [
            "The contract is static and branch-preserving; it does not simulate exact map position, save state, or engine AI resolution.",
            "A travel write is accepted only when its local branch exposes explicit relocation or approach evidence.",
        ],
    }


def contract_scope_scripts(contract: Mapping[str, Any], index: StateDoctorIndex) -> tuple[ScriptRecord, ...]:
    """Resolve an explicit contract scope without broad name-based guessing.

    AI intent contracts are deliberately opt-in.  A party template may be
    manipulated by many generic helpers, so treating every matching string in
    the workspace as part of an intent would produce attractive but unreliable
    "proof."  The checked-in scope is the authority and missing scripts are a
    failed check rather than silently ignored evidence.
    """

    symbols = tuple(
        str(value)
        for value in contract.get("scope_scripts", ())
        if isinstance(value, str) and value
    )
    return tuple(index.scripts[symbol] for symbol in symbols if symbol in index.scripts)


def contract_scope_operations(contract: Mapping[str, Any], index: StateDoctorIndex) -> list[Operation]:
    return [operation for script in contract_scope_scripts(contract, index) for operation in script.operations]


def token_in_conditions(operation: Operation, token: str | None) -> bool:
    if not token:
        return True
    return any(token == condition.name or token in condition.args for condition in operation.conditions)


def literal_integer(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value, 10)
    except ValueError:
        return None


def intent_check(
    check_id: str,
    passed: bool,
    message: str,
    operations: Sequence[Operation] = (),
) -> dict[str, Any]:
    return {
        "id": check_id,
        "passed": passed,
        "message": message,
        "evidence": [source_payload(operation.source) for operation in operations],
    }


def intent_violation(
    contract_id: str,
    intent: str,
    category: str,
    summary: str,
    operations: Sequence[Operation] = (),
    recommendation: str = "Add an explicit checked-in contract scope and make the transition visible in the modeled branch.",
) -> dict[str, Any]:
    return {
        "id": f"{contract_id}:{category}",
        "severity": "error",
        "category": category,
        "summary": summary,
        "contract_id": contract_id,
        "intent": intent,
        "source": source_payload(operations[0].source) if operations else None,
        "evidence": [operation_payload(operation) for operation in operations[:12]],
        "recommendation": recommendation,
    }


def evaluate_party_ai_intent(contract: Mapping[str, Any], index: StateDoctorIndex) -> dict[str, Any]:
    """Evaluate one opt-in party-template AI lifecycle contract.

    The schema deliberately describes *intent*, not a fictional simulation:
    ``stationary``, ``patrol``, ``escort``, ``raid_return``, and ``despawn``
    each map to a small set of observable M&B operations.  A caller can add
    more specific branch tokens or script scopes as a feature matures.  The
    result says "not proven" when a dynamic selector/value cannot be resolved;
    it never claims that a generic party helper acts on a particular template.
    """

    contract_id = str(contract.get("id", "<unnamed-contract>"))
    intent = str(contract.get("intent", ""))
    scope_symbols = tuple(
        str(value)
        for value in contract.get("scope_scripts", ())
        if isinstance(value, str) and value
    )
    scripts = contract_scope_scripts(contract, index)
    operations = contract_scope_operations(contract, index)
    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    missing_scope = [symbol for symbol in scope_symbols if symbol not in index.scripts]
    checks.append(
        intent_check(
            "scope_scripts_exist",
            bool(scope_symbols) and not missing_scope,
            (
                "All declared intent scope scripts exist."
                if scope_symbols and not missing_scope
                else "Intent scope is empty or references missing script(s): " + ", ".join(missing_scope or ["<empty>"])
            ),
            [index.scripts[symbol].operations[0] for symbol in scope_symbols if symbol in index.scripts and index.scripts[symbol].operations],
        )
    )

    party_template = contract.get("party_template")
    party_selector = contract.get("party_selector")
    if not isinstance(party_selector, str) or not party_selector:
        party_selector = None
    if isinstance(party_template, str) and party_template:
        mentions = [operation for operation in operations if party_template in operation.args]
        checks.append(
            intent_check(
                "party_template_evidence",
                bool(mentions),
                f"Declared party template {party_template} {'is' if mentions else 'is not'} referenced in the scoped operations.",
                mentions,
            )
        )

    def matching(name: str, *, value: str | None = None) -> list[Operation]:
        result = [operation for operation in operations if base_operation(operation.name) == name]
        if value is not None:
            result = [operation for operation in result if len(operation.args) >= 2 and operation.args[1] == value]
        if party_selector is not None:
            result = [operation for operation in result if operation.args and operation.args[0] == party_selector]
        return result

    def same_party_possible(left: Operation, right: Operation) -> bool:
        """Keep a contract from combining AI writes for unrelated locals.

        The static model cannot resolve a symbolic party identity across every
        helper.  It can, however, require the exact first argument to agree
        and reject writes proven to live in alternate branches.  A contract
        may additionally set ``party_selector`` when its scope uses several
        party locals.
        """

        return bool(left.args and right.args and left.args[0] == right.args[0] and not paths_are_exclusive(left, right))

    if intent == "stationary":
        expected_behavior = str(contract.get("expected_behavior", "ai_bhvr_hold"))
        writes = matching("party_set_ai_behavior", value=expected_behavior)
        checks.append(
            intent_check(
                "stationary_behavior",
                bool(writes),
                f"Scoped code {'contains' if writes else 'does not contain'} {expected_behavior} behavior writes.",
                writes,
            )
        )
        forbidden = tuple(str(value) for value in contract.get("forbidden_behaviors", ()) if isinstance(value, str))
        allowed_when = str(contract.get("allowed_when", "")) or None
        forbidden_writes = [
            operation
            for behavior in forbidden
            for operation in matching("party_set_ai_behavior", value=behavior)
            if not token_in_conditions(operation, allowed_when)
        ]
        checks.append(
            intent_check(
                "stationary_forbidden_behavior_guarded",
                not forbidden_writes,
                "No forbidden movement behavior is exposed outside its declared transition guard."
                if not forbidden_writes
                else "A forbidden movement behavior is not guarded by the declared transition token.",
                forbidden_writes,
            )
        )
        if not writes:
            violations.append(
                intent_violation(
                    contract_id,
                    intent,
                    "ai_intent_stationary_not_proven",
                    f"{contract_id} does not prove its stationary {expected_behavior} write in the declared scope.",
                    recommendation="Add the holding helper or scope the contract to the helper that owns the camp's stationary AI.",
                )
            )
        if forbidden_writes:
            violations.append(
                intent_violation(
                    contract_id,
                    intent,
                    "ai_intent_stationary_unprotected_movement",
                    f"{contract_id} exposes a movement behavior outside the declared transition guard.",
                    forbidden_writes,
                    recommendation="Put the movement write behind the declared relocation/approach condition or split it into an explicit intent transition.",
                )
            )
    elif intent == "patrol":
        expected_behavior = str(contract.get("expected_behavior", "ai_bhvr_patrol_location"))
        behavior_writes = matching("party_set_ai_behavior", value=expected_behavior)
        radius_writes = matching("party_set_ai_patrol_radius")
        minimum = contract.get("minimum_radius")
        maximum = contract.get("maximum_radius")
        if isinstance(minimum, bool) or not isinstance(minimum, int):
            minimum = None
        if isinstance(maximum, bool) or not isinstance(maximum, int):
            maximum = None
        compatible_pairs = [
            (behavior, radius)
            for behavior in behavior_writes
            for radius in radius_writes
            if same_party_possible(behavior, radius)
        ]
        valid_pairs = [
            (behavior, radius)
            for behavior, radius in compatible_pairs
            if (value := literal_integer(radius.args[1] if len(radius.args) >= 2 else None)) is not None
            and (minimum is None or value >= minimum)
            and (maximum is None or value <= maximum)
        ]
        paired_evidence = [operation for pair in compatible_pairs for operation in pair]
        checks.extend(
            (
                intent_check(
                    "patrol_behavior",
                    bool(behavior_writes),
                    f"Scoped code {'contains' if behavior_writes else 'does not contain'} {expected_behavior} behavior writes.",
                    behavior_writes,
                ),
                intent_check(
                    "patrol_radius",
                    bool(valid_pairs),
                    "A patrol behavior and literal radius share a possible party path within the declared range."
                    if valid_pairs
                    else "No patrol behavior/radius pair shares a possible party path with a declared literal range.",
                    [operation for pair in valid_pairs for operation in pair] or paired_evidence or radius_writes,
                ),
            )
        )
        if not behavior_writes or not valid_pairs:
            violations.append(
                intent_violation(
                    contract_id,
                    intent,
                    "ai_intent_patrol_not_proven",
                    f"{contract_id} does not prove the declared patrol behavior and radius bounds.",
                    paired_evidence or radius_writes or behavior_writes,
                    recommendation="Set an explicit patrol behavior and literal patrol radius in the scoped helper, or record why a dynamic radius is bounded.",
                )
            )
    elif intent == "escort":
        target = str(contract.get("attach_to", "")) or None
        attachments = matching("party_attach_to_party")
        if target is not None:
            attachments = [operation for operation in attachments if len(operation.args) >= 2 and operation.args[1] == target]
        require_detach = bool(contract.get("require_detach", False))
        detaches = matching("party_detach")
        if attachments and require_detach:
            detaches = [
                detach
                for detach in detaches
                if any(same_party_possible(attachment, detach) for attachment in attachments)
            ]
        checks.extend(
            (
                intent_check(
                    "escort_attachment",
                    bool(attachments),
                    "Scoped code contains the declared escort attachment."
                    if attachments
                    else "Scoped code does not prove the declared escort attachment.",
                    attachments,
                ),
                intent_check(
                    "escort_detach_lifecycle",
                    bool(detaches) if require_detach else True,
                    "Escort detach behavior is present when required."
                    if (not require_detach or detaches)
                    else "Escort contract requires a detach lifecycle but none is modeled.",
                    detaches,
                ),
            )
        )
        if not attachments or (require_detach and not detaches):
            violations.append(
                intent_violation(
                    contract_id,
                    intent,
                    "ai_intent_escort_attachment_not_proven",
                    f"{contract_id} does not prove its required escort attachment lifecycle.",
                    attachments or detaches,
                    recommendation="Attach the escort through party_attach_to_party and, when it can leave the role, add an explicit party_detach path.",
                )
            )
    elif intent == "raid_return":
        return_behavior = str(contract.get("return_behavior", "ai_bhvr_travel_to_party"))
        return_target = str(contract.get("return_target", "")) or None
        return_when = str(contract.get("return_when", "")) or None
        writes = matching("party_set_ai_behavior", value=return_behavior)
        if return_target is not None:
            target_writes = [
                operation
                for operation in matching("party_set_ai_object")
                if len(operation.args) >= 2 and operation.args[1] == return_target
            ]
            writes = [
                behavior
                for behavior in writes
                if any(same_party_possible(behavior, target) for target in target_writes)
            ]
        guarded = [operation for operation in writes if token_in_conditions(operation, return_when)]
        checks.append(
            intent_check(
                "raid_return_transition",
                bool(guarded),
                "A declared return behavior is present on the declared return condition."
                if guarded
                else "The declared raid return behavior/condition is not proven in scope.",
                guarded or writes,
            )
        )
        if not guarded:
            violations.append(
                intent_violation(
                    contract_id,
                    intent,
                    "ai_intent_raid_return_not_proven",
                    f"{contract_id} does not prove its raid return transition.",
                    writes,
                    recommendation="Put the return AI write under a clear return condition and name the intended target in the contract.",
                )
            )
    elif intent == "despawn":
        when = str(contract.get("despawn_when", "")) or None
        removals = matching("remove_party")
        guarded = [operation for operation in removals if token_in_conditions(operation, when)]
        checks.append(
            intent_check(
                "despawn_transition",
                bool(guarded),
                "A party removal is present on the declared despawn condition."
                if guarded
                else "The declared despawn condition/removal is not proven in scope.",
                guarded or removals,
            )
        )
        if not guarded:
            violations.append(
                intent_violation(
                    contract_id,
                    intent,
                    "ai_intent_despawn_not_proven",
                    f"{contract_id} does not prove its despawn transition.",
                    removals,
                    recommendation="Keep remove_party in the scoped cleanup path and expose its expiry/terminal condition in the same branch.",
                )
            )
    else:
        violations.append(
            intent_violation(
                contract_id,
                intent or "<missing>",
                "unsupported_ai_intent",
                f"{contract_id} uses unsupported party AI intent {intent!r}.",
                recommendation="Use one of: stationary, patrol, escort, raid_return, despawn.",
            )
        )

    # Scope/template failures are contract failures in their own right.  They
    # need a dedicated evidence item so an LLM does not mistake an empty scope
    # for a successful no-op intent.
    for check in checks:
        if check["passed"]:
            continue
        if check["id"] in {"scope_scripts_exist", "party_template_evidence"}:
            violations.append(
                intent_violation(
                    contract_id,
                    intent or "<missing>",
                    f"ai_intent_{check['id']}",
                    check["message"],
                    recommendation="Correct the checked-in contract scope/template evidence before relying on this intent result.",
                )
            )

    # Repeated checks can expose the same root problem; retain deterministic
    # unique categories in MCP/CLI results.
    unique_violations: list[dict[str, Any]] = []
    seen_categories: set[str] = set()
    for violation in violations:
        category = str(violation["category"])
        if category in seen_categories:
            continue
        seen_categories.add(category)
        unique_violations.append(violation)
    return {
        "id": contract_id,
        "kind": "party_ai_intent",
        "intent": intent,
        "description": str(contract.get("description", "")),
        "party_template": party_template,
        "party_selector": party_selector,
        "scope_scripts": list(scope_symbols),
        "passed": not unique_violations and all(check["passed"] for check in checks),
        "check_count": len(checks),
        "checks": checks,
        "violation_count": len(unique_violations),
        "violations": unique_violations,
        "limitations": [
            "Party-template ownership is opt-in through scope_scripts; the analyzer will not infer that a generic helper targets a template from naming alone.",
            "Dynamic patrol radii, runtime party selectors, and engine movement resolution remain explicit evidence boundaries rather than assumed values.",
        ],
    }


def evaluate_contracts(index: StateDoctorIndex) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for contract in index.contracts:
        kind = contract.get("kind")
        if kind == "stationary_camp":
            results.append(evaluate_stationary_camp(contract, index))
        elif kind == "party_ai_intent":
            results.append(evaluate_party_ai_intent(contract, index))
        else:
            results.append(
                {
                    "id": str(contract.get("id", "<unnamed-contract>")),
                    "kind": kind,
                    "passed": False,
                    "check_count": 0,
                    "checks": [],
                    "violation_count": 1,
                    "violations": [
                        {
                            "id": f"unsupported-contract:{contract.get('id', '<unnamed>')}",
                            "severity": "error",
                            "category": "unsupported_contract_kind",
                            "summary": f"Campaign State Doctor does not implement contract kind {kind!r}.",
                            "contract_id": contract.get("id"),
                        }
                    ],
                    "limitations": [],
                }
            )
    return results


def temporal_overwrite_findings(index: StateDoctorIndex) -> list[dict[str, Any]]:
    """Find conflicting AI writes that are not proven to be alternate branches.

    This intentionally uses exact symbolic party selectors.  ``:party_no`` and
    ``:camp_party`` are not assumed identical; a broad alias claim would turn a
    useful warning into noise.  Contracts cover the higher-level role cases.
    """

    findings: list[dict[str, Any]] = []
    for script in index.scripts.values():
        by_resource: dict[str, list[StateAccess]] = defaultdict(list)
        for access in index.accesses:
            if access.operation.scope_id != script.symbol or access.action != "write" or access.category not in TEMPORAL_AI_CATEGORIES:
                continue
            by_resource[access.resource].append(access)
        for resource, writes in by_resource.items():
            ordered = sorted(writes, key=lambda access: access.operation.ordinal)
            for left_index, left in enumerate(ordered):
                for right in ordered[left_index + 1 :]:
                    if left.value == right.value or paths_are_exclusive(left.operation, right.operation):
                        continue
                    if local_guard_is_completed_before_later_write(left, right, script):
                        continue
                    if spawned_party_subject_is_rebound(left, right, script):
                        continue
                    if is_explicit_ai_state_refresh(left, right):
                        findings.append(
                            {
                                "id": f"ai-state-refresh:{left.id}:{right.id}",
                                "severity": "info",
                                "category": "explicit_ai_state_refresh",
                                "summary": (
                                    f"{script.symbol} explicitly resets {resource} before immediately reapplying "
                                    f"{right.value!r}; the reset forces the state helper to initialize the new intent."
                                ),
                                "resource": resource,
                                "source": source_payload(right.operation.source),
                                "writes": [finding_access_payload(left, index), finding_access_payload(right, index)],
                                "evidence": [
                                    {
                                        "step": 1,
                                        "kind": "explicit_reset",
                                        "message": "Clears the current AI state before reinitialization.",
                                        "source": source_payload(left.operation.source),
                                    },
                                    {
                                        "step": 2,
                                        "kind": "immediate_reapply",
                                        "message": f"Immediately sets the intended {right.value!r} state.",
                                        "source": source_payload(right.operation.source),
                                    },
                                ],
                                "recommendation": "Review as an intentional refresh unless the reset/reapply pair ceases to be adjacent.",
                            }
                        )
                        continue
                    findings.append(
                        {
                            "id": f"temporal-overwrite:{left.id}:{right.id}",
                            "severity": "warning",
                            "category": "possible_temporal_ai_overwrite",
                            "summary": (
                                f"{script.symbol} writes conflicting {left.category} values to {resource} on paths "
                                "not proven mutually exclusive."
                            ),
                            "resource": resource,
                            "source": source_payload(right.operation.source),
                            "writes": [finding_access_payload(left, index), finding_access_payload(right, index)],
                            "counterexample": [
                                {"step": 1, "kind": "first_write", "message": f"Writes {left.value!r}.", "source": source_payload(left.operation.source)},
                                {"step": 2, "kind": "later_write", "message": f"Can later overwrite with {right.value!r}.", "source": source_payload(right.operation.source)},
                            ],
                            "recommendation": "Make the branches explicitly exclusive, centralize the intent in one helper, or add an explicit state contract.",
                        }
                    )
    return findings


def ownership_candidates(index: StateDoctorIndex) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for family, accesses in index.accesses_by_family.items():
        writers = [access for access in accesses if access.action == "write"]
        scripts = sorted({access.operation.scope_id for access in writers if access.operation.scope_kind == "script"})
        if len(scripts) < 3 or not any(token in family for token in ("slot_", "party_ai_", "faction_slot", "troop_slot")):
            continue
        candidates.append(
            {
                "family": family,
                "writer_script_count": len(scripts),
                "writer_scripts": scripts[:20],
                "write_count": len(writers),
                "recommendation": "Review whether this state has a single owner or needs a checked-in temporal contract.",
            }
        )
    return sorted(candidates, key=lambda item: (-item["writer_script_count"], -item["write_count"], item["family"]))


def load_contracts(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CampaignStateError(f"Could not read campaign state contracts at {path}: {error}") from error
    contracts = payload.get("contracts") if isinstance(payload, dict) else None
    if not isinstance(contracts, list) or not all(isinstance(contract, dict) for contract in contracts):
        raise CampaignStateError("Campaign state contracts must contain a 'contracts' object list.")
    ids = [contract.get("id") for contract in contracts]
    if any(not isinstance(identifier, str) or not identifier for identifier in ids) or len(set(ids)) != len(ids):
        raise CampaignStateError("Campaign state contract IDs must be unique non-empty strings.")
    return [dict(contract) for contract in contracts]


def build_state_doctor(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    contracts_path: Path | None = None,
) -> StateDoctorIndex:
    """Build or reuse the source-only campaign-state index."""

    root = root.resolve()
    if not (root / "src" / "scripts").is_dir() or not (root / "src" / "triggers").is_dir():
        raise CampaignStateError(f"Not a recognizable SoD Modern source workspace: {root}")
    checked_contracts = (contracts_path or (root / "devkit" / "campaign_state_doctor" / "contracts.json")).resolve()
    if not checked_contracts.is_file() and contracts_path is None:
        checked_contracts = DEFAULT_CONTRACTS_PATH
    signature = source_signature(root, checked_contracts)
    key = (root, checked_contracts)
    cached = _CACHE.get(key)
    if cached is not None and cached[0] == signature:
        return cached[1]

    scripts, triggers, parse_findings, source_files = parse_source(root)
    all_operations = tuple(operation for script in scripts.values() for operation in script.operations) + tuple(
        operation for trigger in triggers.values() for operation in trigger.operations
    )
    accesses = tuple(access for operation in all_operations for access in accesses_for_operation(operation))
    by_resource: dict[str, list[StateAccess]] = defaultdict(list)
    by_family: dict[str, list[StateAccess]] = defaultdict(list)
    for access in accesses:
        by_resource[access.resource].append(access)
        by_family[access.family].append(access)
    callers: dict[str, list[str]] = defaultdict(list)
    for script in scripts.values():
        for child in script.calls:
            callers[child].append(script.symbol)
    trigger_paths, path_warnings = build_trigger_paths(scripts, triggers)
    freshness = compute_freshness(root, source_files)
    warnings = [
        "Campaign State Doctor is a static, branch-preserving model; it does not execute the M&B engine, resolve saves, or claim an in-game path is certain.",
        "Exact symbolic party selectors are kept distinct unless a contract provides stronger role evidence.",
        *path_warnings,
    ]
    if freshness["source_is_newer_than_state_compile"]:
        warnings.append(
            "Canonical state source is newer than compile/module_scripts.py or compile/module_simple_triggers.py; analyze the source result, then rebuild before treating it as exported runtime proof."
        )
    index = StateDoctorIndex(
        root=root,
        contracts_path=checked_contracts,
        source_files=source_files,
        scripts=scripts,
        triggers=triggers,
        operations=all_operations,
        accesses=accesses,
        accesses_by_resource={key: list(value) for key, value in by_resource.items()},
        accesses_by_family={key: list(value) for key, value in by_family.items()},
        callers={key: sorted(set(value)) for key, value in callers.items()},
        trigger_paths=trigger_paths,
        parse_findings=parse_findings,
        contracts=load_contracts(checked_contracts),
        warnings=list(dict.fromkeys(warnings)),
        freshness=freshness,
    )
    index.contract_results = evaluate_contracts(index)
    index.findings = [
        *parse_findings,
        *(violation for result in index.contract_results for violation in result["violations"]),
        *temporal_overwrite_findings(index),
    ]
    severity_rank = {"error": 0, "warning": 1, "info": 2}
    index.findings.sort(key=lambda finding: (severity_rank.get(str(finding.get("severity")), 3), str(finding.get("category")), str(finding.get("id"))))
    _CACHE[key] = (signature, index)
    return index


def findings_payload(
    index: StateDoctorIndex,
    *,
    severity: str = "all",
    query: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    if severity not in {"all", "error", "warning", "info"}:
        raise CampaignStateError("severity must be one of: all, error, warning, info.")
    needle = require_query(query).casefold() if query is not None else None
    selected: list[dict[str, Any]] = []
    for finding in index.findings:
        if severity != "all" and finding.get("severity") != severity:
            continue
        haystack = json.dumps(finding, sort_keys=True).casefold()
        if needle is not None and needle not in haystack:
            continue
        selected.append(finding)
    return {
        "severity": severity,
        "query": query,
        "finding_count": len(selected),
        "returned_count": min(len(selected), maximum),
        "truncated": len(selected) > maximum,
        "findings": selected[:maximum],
        "warnings": index.warnings,
    }


def summary_payload(index: StateDoctorIndex, *, limit: int = 20) -> dict[str, Any]:
    maximum = require_limit(limit)
    severity_counts = Counter(str(finding.get("severity", "info")) for finding in index.findings)
    access_counts = Counter(access.category for access in index.accesses)
    ownership = ownership_candidates(index)
    contract_counts = Counter("passed" if result["passed"] else "failed" for result in index.contract_results)
    trigger_path_count = sum(len(paths) for paths in index.trigger_paths.values())
    return {
        "campaign_state_doctor_version": f"devkit.campaign-state-doctor.v{ANALYZER_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {
            "repo_root": str(index.root),
            "read_only": True,
            "authoritative_layer": "src/scripts and src/triggers",
            "contracts_path": project_relative(index.contracts_path, index.root),
        },
        "source": {
            "file_count": len(index.source_files),
            "script_count": len(index.scripts),
            "simple_trigger_count": len(index.triggers),
            "operation_count": len(index.operations),
            "freshness": index.freshness,
        },
        "state_model": {
            "access_count": len(index.accesses),
            "resource_count": len(index.accesses_by_resource),
            "resource_family_count": len(index.accesses_by_family),
            "access_categories": dict(sorted(access_counts.items())),
            "trigger_reachable_script_count": len(index.trigger_paths),
            "trigger_path_count": trigger_path_count,
        },
        "contracts": {
            "count": len(index.contract_results),
            "passed_count": contract_counts["passed"],
            "failed_count": contract_counts["failed"],
            "results": [
                {
                    "id": result["id"],
                    "kind": result["kind"],
                    "passed": result["passed"],
                    "violation_count": result["violation_count"],
                }
                for result in index.contract_results
            ],
        },
        "findings": {
            "total": len(index.findings),
            "by_severity": dict(sorted(severity_counts.items())),
            "returned_count": min(len(index.findings), maximum),
            "truncated": len(index.findings) > maximum,
            "items": index.findings[:maximum],
        },
        "shared_state_ownership_candidates": {
            "count": len(ownership),
            "returned_count": min(len(ownership), maximum),
            "truncated": len(ownership) > maximum,
            "items": ownership[:maximum],
        },
        "next_steps": [
            "Use campaign_state_contracts to inspect contract checks and counterexample evidence.",
            "Use campaign_state_findings to filter errors or warnings before editing.",
            "Use campaign_state_resource then campaign_state_timeline to inspect every reader/writer and trigger path for one state field.",
        ],
        "warnings": index.warnings,
    }


def contracts_payload(index: StateDoctorIndex, *, contract_id: str | None = None) -> dict[str, Any]:
    checked_id = require_query(contract_id, name="contract_id") if contract_id is not None else None
    results = [result for result in index.contract_results if checked_id is None or result["id"] == checked_id]
    if checked_id is not None and not results:
        raise CampaignStateError(f"No campaign state contract found with id {checked_id!r}.")
    return {
        "contract_id": checked_id,
        "contract_count": len(results),
        "passed_count": sum(1 for result in results if result["passed"]),
        "failed_count": sum(1 for result in results if not result["passed"]),
        "contracts": results,
        "warnings": index.warnings,
    }


def ai_intents_payload(index: StateDoctorIndex, *, intent: str | None = None) -> dict[str, Any]:
    """Return only party-AI intent contracts, including legacy stationary camps.

    ``stationary_camp`` predates the generic ``party_ai_intent`` schema but is
    an intent contract in exactly the same sense. Keeping both in this focused
    view lets callers inspect camps, patrols, escorts, return paths, and
    despawns without filtering unrelated durable-state contracts themselves.
    """

    checked_intent = require_query(intent, name="intent") if intent is not None else None
    rows = []
    for result in index.contract_results:
        if result.get("kind") not in {"stationary_camp", "party_ai_intent"}:
            continue
        result_intent = "stationary_camp" if result.get("kind") == "stationary_camp" else result.get("intent")
        if checked_intent is not None and result_intent != checked_intent:
            continue
        rows.append(result)
    if checked_intent is not None and not rows:
        raise CampaignStateError(f"No evaluated AI intent contract found with intent {checked_intent!r}.")
    return {
        "intent": checked_intent,
        "intent_contract_count": len(rows),
        "passed_count": sum(1 for result in rows if result["passed"]),
        "failed_count": sum(1 for result in rows if not result["passed"]),
        "contracts": rows,
        "warnings": index.warnings,
    }


def matching_resources(index: StateDoctorIndex, query: str) -> list[str]:
    needle = query.casefold()
    direct = [resource for resource in index.accesses_by_resource if resource.casefold() == needle]
    if direct:
        return sorted(direct)
    return sorted(resource for resource in index.accesses_by_resource if needle in resource.casefold())


def resource_payload(index: StateDoctorIndex, query: str, *, limit: int = 30) -> dict[str, Any]:
    maximum = require_limit(limit)
    checked_query = require_query(query)
    resources = matching_resources(index, checked_query)
    rows: list[dict[str, Any]] = []
    for resource in resources[:maximum]:
        accesses = index.accesses_by_resource[resource]
        writers = [access for access in accesses if access.action == "write"]
        readers = [access for access in accesses if access.action == "read"]
        scripts = sorted({access.operation.scope_id for access in accesses if access.operation.scope_kind == "script"})
        rows.append(
            {
                "resource": resource,
                "family": accesses[0].family if accesses else None,
                "access_count": len(accesses),
                "writer_count": len(writers),
                "reader_count": len(readers),
                "script_count": len(scripts),
                "scripts": scripts[:20],
                "sample_accesses": [access_payload(access, index) for access in accesses[:5]],
            }
        )
    return {
        "query": checked_query,
        "resource_count": len(resources),
        "returned_count": len(rows),
        "truncated": len(resources) > maximum,
        "resources": rows,
        "warnings": index.warnings,
    }


def timeline_payload(index: StateDoctorIndex, resource: str, *, limit: int = 60) -> dict[str, Any]:
    maximum = require_limit(limit)
    checked_resource = require_query(resource, name="resource")
    resources = matching_resources(index, checked_resource)
    events: list[StateAccess] = []
    for resolved in resources:
        events.extend(index.accesses_by_resource[resolved])
    events.sort(key=lambda access: (access.operation.scope_kind, access.operation.scope_id, access.operation.path, access.operation.ordinal))
    trigger_routes: list[dict[str, Any]] = []
    for event in events:
        if event.operation.scope_kind != "script":
            continue
        for path in index.trigger_paths.get(event.operation.scope_id, []):
            row = {
                "trigger_id": path.trigger_id,
                "cadence": path.cadence,
                "call_path": list(path.call_path),
                "event_id": event.id,
            }
            if row not in trigger_routes:
                trigger_routes.append(row)
    return {
        "resource_query": checked_resource,
        "resolved_resources": resources,
        "event_count": len(events),
        "returned_count": min(len(events), maximum),
        "truncated": len(events) > maximum,
        "events": [access_payload(event, index) for event in events[:maximum]],
        "trigger_routes": trigger_routes[:maximum],
        "trigger_routes_truncated": len(trigger_routes) > maximum,
        "temporal_interpretation": [
            "Operation order is exact within a single source operation block and call path.",
            "Multiple engine callbacks or trigger roots are not assigned a fictional total order; they remain separate scheduler boundaries.",
            "Different symbolic party selectors are intentionally not treated as the same runtime party without contract evidence.",
        ],
        "warnings": index.warnings,
    }


def render_markdown(payload: dict[str, Any], *, command: str) -> str:
    if command == "summary":
        source = payload["source"]
        state = payload["state_model"]
        contracts = payload["contracts"]
        findings = payload["findings"]
        lines = [
            "# Campaign State Doctor",
            "",
            "Read-only temporal state model over canonical `src/scripts` and `src/triggers`.",
            "",
            "## Coverage",
            "",
            f"- {source['script_count']:,} scripts, {source['simple_trigger_count']:,} simple triggers, and {source['operation_count']:,} modeled operations.",
            f"- {state['access_count']:,} durable-state accesses across {state['resource_count']:,} exact resources.",
            f"- Contracts: {contracts['passed_count']} passed / {contracts['failed_count']} failed.",
            f"- Findings: {findings['total']} total ({', '.join(f'{key}={value}' for key, value in findings['by_severity'].items()) or 'none'}).",
            "",
            "## Contract status",
            "",
        ]
        for contract in contracts["results"]:
            lines.append(f"- {contract['id']}: {'pass' if contract['passed'] else 'FAIL'}; {contract['violation_count']} violation(s).")
    elif command == "findings":
        lines = ["# Campaign State Findings", ""]
        for finding in payload["findings"]:
            lines.append(f"- [{finding.get('severity', 'info')}] {finding.get('summary', finding.get('id'))}")
    elif command == "contracts":
        lines = ["# Campaign State Contracts", ""]
        for contract in payload["contracts"]:
            lines.append(f"- {contract['id']}: {'pass' if contract['passed'] else 'FAIL'}; {contract['violation_count']} violation(s).")
    else:
        lines = [f"# Campaign State Doctor: {command}", "", "Use JSON output for full source-mapped evidence."]
    if payload.get("warnings"):
        lines.extend(["", "## Model boundaries", ""])
        lines.extend(f"- {warning}" for warning in payload["warnings"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only temporal campaign-state diagnostics for SoD Modern.")
    parser.add_argument("command", choices=("summary", "findings", "resource", "timeline", "contracts", "ai-intents"))
    parser.add_argument("query", nargs="?", help="Required resource query for resource/timeline; optional text filter for findings.")
    parser.add_argument("--root", default=str(DEFAULT_REPO_ROOT), help="Module workspace root; defaults to this DevKit's workspace.")
    parser.add_argument("--contracts", help="Optional checked-in/fixture contract file path.")
    parser.add_argument("--severity", default="all", choices=("all", "error", "warning", "info"))
    parser.add_argument("--contract-id")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve()
        contracts_path = Path(args.contracts).resolve() if args.contracts else None
        index = build_state_doctor(root, contracts_path=contracts_path)
        if args.command == "summary":
            payload = summary_payload(index, limit=args.limit)
        elif args.command == "findings":
            payload = findings_payload(index, severity=args.severity, query=args.query, limit=args.limit)
        elif args.command == "contracts":
            payload = contracts_payload(index, contract_id=args.contract_id)
        elif args.command == "ai-intents":
            payload = ai_intents_payload(index, intent=args.query)
        elif args.command == "resource":
            payload = resource_payload(index, require_query(args.query), limit=args.limit)
        else:
            payload = timeline_payload(index, require_query(args.query, name="resource"), limit=args.limit)
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, command=args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except CampaignStateError as error:
        print(f"campaign_state_doctor: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
