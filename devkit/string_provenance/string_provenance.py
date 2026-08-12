#!/usr/bin/env python3
"""Interprocedural, branch-preserving provenance for M&B string registers.

String Integrity correctly treats a script call as a conservative clobber
boundary. This companion slice resolves that boundary one level further: it
parses generated ``module_scripts.py`` without importing it, follows literal
``call_script`` edges, and returns the actual nested writer operations and
their enclosing branch evidence. It never executes generated code, evaluates
save state, or claims that a possible branch happened in a playthrough.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.string_integrity import string_integrity as integrity
from devkit.text_execution_ledger import text_execution_ledger as ledger_module


PROVENANCE_VERSION = "1.0.0"
REGISTER_RE = re.compile(r"^s(?:0|[1-9]\d*)$")
CONTROL_OPEN = frozenset(
    {
        "try_begin", "try_for_agents", "try_for_attached_parties", "try_for_parties", "try_for_players",
        "try_for_prop_instances", "try_for_range", "try_for_range_backwards", "try_for_troops",
    }
)
CONTROL_ALTERNATE = frozenset({"else_try", "else_try_begin"})
CONTROL_CLOSE = frozenset({"try_end", "end_try"})
CONDITION_NAMES = frozenset(
    {
        "eq", "neq", "ge", "gt", "le", "lt", "is_between", "party_is_active",
        "party_slot_eq", "party_slot_ge", "party_slot_gt", "party_slot_le", "party_slot_lt",
        "faction_slot_eq", "faction_slot_ge", "faction_slot_gt", "faction_slot_le", "faction_slot_lt",
        "troop_slot_eq", "troop_slot_ge", "troop_slot_gt", "troop_slot_le", "troop_slot_lt",
        "quest_slot_eq", "quest_slot_ge", "quest_slot_gt", "quest_slot_le", "quest_slot_lt",
        "is_currently_night", "check_quest_active", "check_quest_concluded", "check_quest_failed", "check_quest_succeeded",
    }
)


class StringProvenanceError(RuntimeError):
    """The requested interprocedural provenance query cannot be answered safely."""


@dataclass(frozen=True)
class ConditionEvidence:
    name: str
    args: tuple[str, ...]
    source: dict[str, Any] | None
    block_id: str
    branch: int


@dataclass
class ScriptOperation:
    id: str
    script_symbol: str
    node: ast.AST = field(repr=False)
    name: str = ""
    args: tuple[str, ...] = ()
    ordinal: int = 0
    compile_line: int = 0
    column: int = 0
    source: dict[str, Any] | None = None
    branch_path: tuple[tuple[str, int], ...] = ()
    conditions: tuple[ConditionEvidence, ...] = ()


@dataclass
class ScriptRecord:
    symbol: str
    source: dict[str, Any] | None
    operations: tuple[ScriptOperation, ...]
    opaque_builder: bool = False


@dataclass(frozen=True)
class WriterPath:
    register: str
    call_chain: tuple[str, ...]
    operations: tuple[ScriptOperation, ...]
    writer: ScriptOperation
    source_kind: str
    source_expression: str | None
    source_register: str | None
    source_selector: str | None
    conditions: tuple[ConditionEvidence, ...]


@dataclass
class ScriptPathSummary:
    script_symbol: str
    register: str
    paths: list[WriterPath]
    unresolved_boundaries: list[dict[str, Any]]
    truncated: bool = False


@dataclass
class StringProvenanceIndex:
    root: Path
    module: integrity.ModuleData
    ledger: ledger_module.LedgerIndex
    scripts: dict[str, ScriptRecord]
    writer_counts: dict[str, int]
    warnings: list[str]
    path_cache: dict[tuple[str, str], ScriptPathSummary] = field(default_factory=dict)


@dataclass
class _ControlFrame:
    id: str
    branch: int = 0
    conditions: list[ConditionEvidence] = field(default_factory=list)
    effect_seen: bool = False


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], StringProvenanceIndex]] = {}


def base_operation(name: str) -> str:
    return name.rsplit("|", 1)[-1]


def source_payload(module: integrity.ModuleData, line: int) -> dict[str, Any] | None:
    return integrity.source_payload(module.source_at(line))


def operation_args(node: ast.AST) -> tuple[str, ...]:
    if not isinstance(node, (ast.Tuple, ast.List)):
        return ()
    return tuple(integrity.expression_text(value) for value in node.elts[1:])


def is_condition(operation: ScriptOperation) -> bool:
    base = base_operation(operation.name)
    if base == "call_script":
        return bool(operation.args and operation.args[0].startswith("script_cf_"))
    return (
        base in CONDITION_NAMES
        or base.startswith(("party_slot_", "faction_slot_", "troop_slot_", "quest_slot_", "is_", "check_"))
        or operation.name.startswith(("neg|", "this_or_next|"))
    )


def is_effect(operation: ScriptOperation) -> bool:
    base = base_operation(operation.name)
    return (
        integrity.is_string_writer(base)
        or base == "call_script"
        or base.startswith(("assign", "store_", "val_", "party_", "faction_", "troop_", "display_", "jump_", "spawn_", "remove_", "change_", "start_", "finish_"))
    )


def annotate_operations(module: integrity.ModuleData, symbol: str, nodes: Iterable[ast.AST]) -> tuple[ScriptOperation, ...]:
    operations: list[ScriptOperation] = []
    for ordinal, node in enumerate(nodes):
        name = integrity.operation_name(node)
        if name is None:
            continue
        operations.append(
            ScriptOperation(
                id=f"script-op:{symbol}:{getattr(node, 'lineno', 0)}:{getattr(node, 'col_offset', 0)}",
                script_symbol=symbol,
                node=node,
                name=name,
                args=operation_args(node),
                ordinal=ordinal,
                compile_line=getattr(node, "lineno", 0),
                column=getattr(node, "col_offset", 0),
                source=source_payload(module, getattr(node, "lineno", 0)),
            )
        )
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
            stack.append(_ControlFrame(f"{symbol}:{operation.ordinal}:{counter}"))
            continue
        if is_condition(operation) and stack and not stack[-1].effect_seen:
            frame = stack[-1]
            frame.conditions.append(
                ConditionEvidence(
                    name=operation.name,
                    args=operation.args,
                    source=operation.source,
                    block_id=frame.id,
                    branch=frame.branch,
                )
            )
        if is_effect(operation):
            for frame in stack:
                frame.effect_seen = True
    return tuple(operations)


def script_nodes(operations: ast.AST) -> tuple[Iterable[ast.AST], bool]:
    if isinstance(operations, ast.List):
        return (item for item in operations.elts if integrity.operation_name(item) is not None), False
    return (), True


def build_script_records(module: integrity.ModuleData) -> dict[str, ScriptRecord]:
    scripts_node = integrity.find_assignment_list(module.tree, "scripts")
    if scripts_node is None:
        raise StringProvenanceError("Generated module_scripts.py has no literal scripts list.")
    records: dict[str, ScriptRecord] = {}
    for entry in scripts_node.elts:
        if not isinstance(entry, (ast.Tuple, ast.List)) or len(entry.elts) < 2:
            continue
        identifier = entry.elts[0]
        if not isinstance(identifier, ast.Constant) or not isinstance(identifier.value, str):
            continue
        symbol = f"script_{identifier.value}"
        nodes, opaque = script_nodes(entry.elts[1])
        records[symbol] = ScriptRecord(
            symbol=symbol,
            source=source_payload(module, getattr(entry, "lineno", 0)),
            operations=annotate_operations(module, symbol, nodes),
            opaque_builder=opaque,
        )
    return records


def index_signature(root: Path) -> tuple[tuple[str, int, int], ...]:
    paths = [
        root / "compile" / "module_scripts.py",
        root / "compile" / "module_dialogs.py",
        root / "compile" / "module_game_menus.py",
        root / "_export" / "strings.txt",
        root / "_export" / "quick_strings.txt",
    ]
    rows = []
    for path in paths:
        try:
            stat = path.stat()
        except OSError:
            rows.append((integrity.project_relative(path, root), -1, -1))
        else:
            rows.append((integrity.project_relative(path, root), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def build_string_provenance(root: Path = DEFAULT_REPO_ROOT) -> StringProvenanceIndex:
    root = root.resolve()
    current = index_signature(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == current:
        return cached[1]
    try:
        ledger = ledger_module.build_ledger(root)
    except ledger_module.LedgerError as error:
        raise StringProvenanceError(str(error)) from error
    module_index = ledger.modules.get("compile/module_scripts.py")
    if module_index is None:
        raise StringProvenanceError("Generated compile/module_scripts.py is unavailable to the text execution ledger.")
    module = module_index.module
    scripts = build_script_records(module)
    writer_counts = Counter(
        register
        for script in scripts.values()
        for operation in script.operations
        if (register := integrity.writer_register_from_operation(operation.node)) is not None
    )
    warnings = [
        "Interprocedural paths are built only from literal generated scripts and literal call_script targets. Dynamic builders, missing scripts, recursion, and depth cutoffs remain explicit boundaries.",
        "Branch evidence identifies the enclosing generated try/else branch. It does not evaluate save state or infer an inverse condition for an else_try branch.",
        *ledger.warnings,
    ]
    index = StringProvenanceIndex(root, module, ledger, scripts, dict(writer_counts), list(dict.fromkeys(warnings)))
    _CACHE[root] = (current, index)
    return index


def require_register(value: str) -> str:
    if not isinstance(value, str) or REGISTER_RE.fullmatch(value.strip()) is None:
        raise StringProvenanceError("register must be an s-register such as s68.")
    number = integrity.register_number(value.strip())
    if number > integrity.ENGINE_STRING_REGISTER_MAX:
        raise StringProvenanceError(f"{value.strip()} is outside the M&B 1.011 engine string-register range.")
    return value.strip()


def require_limit(value: int, maximum: int = 100) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise StringProvenanceError(f"limit must be an integer from 1 through {maximum}.")
    return value


def require_query(value: str | None, *, name: str = "query") -> str:
    if not isinstance(value, str) or not value.strip():
        raise StringProvenanceError(f"{name} must not be empty.")
    if len(value) > 500:
        raise StringProvenanceError(f"{name} must be at most 500 characters.")
    return value.strip()


def condition_payload(condition: ConditionEvidence) -> dict[str, Any]:
    return {
        "name": condition.name,
        "args": list(condition.args),
        "source": condition.source,
        "block_id": condition.block_id,
        "branch": condition.branch,
    }


def operation_payload(operation: ScriptOperation) -> dict[str, Any]:
    return {
        "id": operation.id,
        "script_symbol": operation.script_symbol,
        "name": operation.name,
        "args": list(operation.args),
        "ordinal": operation.ordinal,
        "compile_path": "compile/module_scripts.py",
        "compile_line": operation.compile_line,
        "column": operation.column,
        "source": operation.source,
        "branch_path": [{"block_id": block, "branch": branch} for block, branch in operation.branch_path],
        "conditions": [condition_payload(condition) for condition in operation.conditions],
    }


def call_target(operation: ScriptOperation) -> str | None:
    if base_operation(operation.name) != "call_script" or not operation.args:
        return None
    return operation.args[0] if operation.args[0].startswith("script_") else None


def writer_metadata(index: StringProvenanceIndex, operation: ScriptOperation) -> tuple[str, str | None, str | None, str | None]:
    name = base_operation(operation.name)
    source_node = operation.node.elts[2] if isinstance(operation.node, (ast.Tuple, ast.List)) and len(operation.node.elts) >= 3 else None
    if name == "str_clear":
        return "empty", "", None, None
    if name == "str_store_string_reg":
        expression = integrity.expression_text(source_node)
        direct = integrity.string_register(source_node, allow_numeric=True)
        selector = integrity.register_selector_kind(source_node)
        return "register_copy", expression, direct, selector if direct is None else None
    if name.startswith("str_store_"):
        value = integrity.text_value(source_node, index.ledger.export_index)
        return str(value["kind"]), value.get("expression"), None, None
    return "unknown_writer", None, None, None


def combine_conditions(*groups: Sequence[ConditionEvidence]) -> tuple[ConditionEvidence, ...]:
    result: list[ConditionEvidence] = []
    seen: set[tuple[str, tuple[str, ...], str, int]] = set()
    for group in groups:
        for condition in group:
            key = (condition.name, condition.args, condition.block_id, condition.branch)
            if key not in seen:
                seen.add(key)
                result.append(condition)
    return tuple(result)


def _unique_boundaries(boundaries: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for boundary in boundaries:
        key = json.dumps(boundary, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            result.append(boundary)
    return result


def script_writer_paths(
    index: StringProvenanceIndex,
    script_symbol: str,
    register: str,
    *,
    max_depth: int = 8,
    max_paths: int = 80,
    _stack: tuple[str, ...] = (),
) -> ScriptPathSummary:
    """Return exact direct/nested writers of one register from one script.

    Returned paths are static possibilities with literal call edges and branch
    evidence. No paths and no unresolved boundaries prove that the selected
    literal script graph contains no writer within this bounded model.
    """

    if not _stack:
        cached = index.path_cache.get((script_symbol, register))
        if cached is not None:
            return cached
    record = index.scripts.get(script_symbol)
    unresolved: list[dict[str, Any]] = []
    paths: list[WriterPath] = []
    if record is None:
        unresolved.append({"kind": "missing_script", "script_symbol": script_symbol})
    elif record.opaque_builder:
        unresolved.append({"kind": "opaque_script_builder", "script_symbol": script_symbol, "source": record.source})
    elif script_symbol in _stack:
        unresolved.append({"kind": "recursive_call", "script_symbol": script_symbol, "call_chain": list((*_stack, script_symbol))})
    elif len(_stack) >= max_depth:
        unresolved.append({"kind": "depth_cutoff", "script_symbol": script_symbol, "depth": len(_stack)})
    else:
        stack = (*_stack, script_symbol)
        for operation in record.operations:
            destination = integrity.writer_register_from_operation(operation.node)
            if destination == register:
                kind, expression, source_register, selector = writer_metadata(index, operation)
                paths.append(
                    WriterPath(
                        register=register,
                        call_chain=stack,
                        operations=(operation,),
                        writer=operation,
                        source_kind=kind,
                        source_expression=expression,
                        source_register=source_register,
                        source_selector=selector,
                        conditions=operation.conditions,
                    )
                )
            target = call_target(operation)
            if target is None:
                if base_operation(operation.name) == "call_script":
                    unresolved.append(
                        {
                            "kind": "dynamic_script_target",
                            "script_symbol": script_symbol,
                            "operation": operation_payload(operation),
                        }
                    )
                continue
            child = script_writer_paths(
                index,
                target,
                register,
                max_depth=max_depth,
                max_paths=max_paths,
                _stack=stack,
            )
            for path in child.paths:
                paths.append(
                    WriterPath(
                        register=register,
                        call_chain=path.call_chain,
                        operations=(operation, *path.operations),
                        writer=path.writer,
                        source_kind=path.source_kind,
                        source_expression=path.source_expression,
                        source_register=path.source_register,
                        source_selector=path.source_selector,
                        conditions=combine_conditions(operation.conditions, path.conditions),
                    )
                )
            for boundary in child.unresolved_boundaries:
                inherited = dict(boundary)
                inherited.setdefault("via_call", operation.id)
                unresolved.append(inherited)
            if len(paths) >= max_paths:
                break
    truncated = len(paths) > max_paths
    unique_paths: list[WriterPath] = []
    seen_paths: set[tuple[str, tuple[str, ...]]] = set()
    for path in paths[:max_paths]:
        key = (path.writer.id, path.call_chain)
        if key not in seen_paths:
            seen_paths.add(key)
            unique_paths.append(path)
    summary = ScriptPathSummary(script_symbol, register, unique_paths, _unique_boundaries(unresolved), truncated)
    if not _stack:
        index.path_cache[(script_symbol, register)] = summary
    return summary


def writer_path_payload(path: WriterPath) -> dict[str, Any]:
    return {
        "register": path.register,
        "call_chain": list(path.call_chain),
        "call_operations": [operation_payload(operation) for operation in path.operations[:-1]],
        "writer_operation": operation_payload(path.writer),
        "source_kind": path.source_kind,
        "source_expression": path.source_expression,
        "source_register": path.source_register,
        "source_selector": path.source_selector,
        "branch_conditions": [condition_payload(condition) for condition in path.conditions],
    }


def script_paths_payload(index: StringProvenanceIndex, script_symbol: str, register: str, *, limit: int = 40) -> dict[str, Any]:
    maximum = require_limit(limit)
    checked_symbol = require_query(script_symbol, name="script_symbol")
    if not checked_symbol.startswith("script_"):
        checked_symbol = f"script_{checked_symbol}"
    checked_register = require_register(register)
    summary = script_writer_paths(index, checked_symbol, checked_register, max_paths=maximum)
    return {
        "script_symbol": checked_symbol,
        "register": checked_register,
        "writer_path_count": len(summary.paths),
        "returned_count": min(len(summary.paths), maximum),
        "truncated": summary.truncated or len(summary.paths) > maximum,
        "writer_paths": [writer_path_payload(path) for path in summary.paths[:maximum]],
        "unresolved_boundary_count": len(summary.unresolved_boundaries),
        "unresolved_boundaries": summary.unresolved_boundaries[:maximum],
        "interpretation": (
            "No writer paths plus zero unresolved boundaries proves no modeled literal writer for this register in the selected script graph. "
            "A returned writer path is a static possibility with exact call and branch evidence, not runtime certainty."
        ),
        "warnings": index.warnings,
    }


def sink_script_provenance(index: StringProvenanceIndex, sink: dict[str, Any], *, max_paths: int) -> dict[str, Any]:
    context = ledger_module.sink_context(index.ledger, sink)
    display_records = [record for _, records in ledger_module.section_records(context) for record in records]
    calls = [record for record in display_records if ledger_module.base_operation(record.name) == "call_script"]
    dependencies = sink.get("register_assessments", [])
    registers = [item.get("register") for item in dependencies if isinstance(item, dict) and isinstance(item.get("register"), str)]
    register_rows: list[dict[str, Any]] = []
    for register in registers:
        call_rows: list[dict[str, Any]] = []
        any_paths = False
        unresolved: list[dict[str, Any]] = []
        for call in calls:
            symbol = integrity.call_script_symbol(call.node)
            if symbol is None:
                unresolved.append({"kind": "dynamic_script_target", "operation": ledger_module.operation_payload(call)})
                continue
            summary = script_writer_paths(index, symbol, register, max_paths=max_paths)
            any_paths = any_paths or bool(summary.paths)
            unresolved.extend(summary.unresolved_boundaries)
            call_rows.append(
                {
                    "call_operation": ledger_module.operation_payload(call),
                    "script_symbol": symbol,
                    "writer_path_count": len(summary.paths),
                    "writer_paths": [writer_path_payload(path) for path in summary.paths[:max_paths]],
                    "unresolved_boundaries": summary.unresolved_boundaries[:max_paths],
                    "truncated": summary.truncated,
                }
            )
        status = (
            "called_script_writer_paths_proven"
            if any_paths
            else "unresolved_call_boundary"
            if unresolved
            else "no_called_script_writes_register_proven"
        )
        register_rows.append(
            {
                "register": register,
                "status": status,
                "direct_display_context_candidates": [
                    ledger_module.value_candidate_from_record(index.ledger, record)
                    for record in ledger_module.latest_records_for_symbol(display_records, register)
                ],
                "script_calls": call_rows,
                "unresolved_boundaries": _unique_boundaries(unresolved)[:max_paths],
            }
        )
    return {
        "sink_id": sink["id"],
        "sink": sink,
        "execution_context": ledger_module.context_metadata(context),
        "register_count": len(register_rows),
        "registers": register_rows,
    }


def summary_payload(index: StringProvenanceIndex, *, limit: int = 20) -> dict[str, Any]:
    maximum = require_limit(limit)
    direct_writers = sorted(index.writer_counts.items(), key=lambda item: (-item[1], integrity.register_number(item[0])))
    opaque = [record for record in index.scripts.values() if record.opaque_builder]
    return {
        "string_provenance_version": f"devkit.string-provenance.v{PROVENANCE_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {
            "repo_root": str(index.root),
            "read_only": True,
            "authoritative_layer": "compile/module_scripts.py plus visible-sink execution contexts",
        },
        "coverage": {
            "script_count": len(index.scripts),
            "opaque_script_builder_count": len(opaque),
            "direct_string_writer_count": sum(index.writer_counts.values()),
            "register_with_direct_writer_count": len(index.writer_counts),
            "visible_sink_count": len(index.ledger.sinks_by_id),
        },
        "most_written_registers": [
            {"register": register, "direct_writer_count": count}
            for register, count in direct_writers[:maximum]
        ],
        "most_written_registers_truncated": len(direct_writers) > maximum,
        "next_steps": [
            "Use string_provenance_paths with a script and s-register to inspect exact nested call/branch writers.",
            "Use string_provenance_explain for a visible text sink to replace broad script-clobber warnings with modeled call paths.",
            "Use text_explain first when the sink itself is unknown; provenance adds interprocedural detail rather than replacing export/string integrity checks.",
        ],
        "warnings": index.warnings,
    }


def explain(
    index: StringProvenanceIndex,
    *,
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 10,
    max_paths: int = 20,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    path_limit = require_limit(max_paths, 80)
    selection = ledger_module.select_sinks(
        index.ledger,
        query=query,
        sink_id=sink_id,
        kind=kind,
        include_clean=include_clean,
        limit=maximum,
    )
    return {
        "summary": summary_payload(index, limit=maximum),
        **{key: value for key, value in selection.items() if key != "sinks"},
        "explanations": [sink_script_provenance(index, sink, max_paths=path_limit) for sink in selection["sinks"]],
        "warnings": index.warnings,
    }


def render_markdown(payload: dict[str, Any], command: str) -> str:
    if command == "summary":
        coverage = payload["coverage"]
        lines = [
            "# Interprocedural String Provenance",
            "",
            f"- Generated scripts: {coverage['script_count']:,}; direct string writers: {coverage['direct_string_writer_count']:,}; visible sinks: {coverage['visible_sink_count']:,}.",
        ]
    else:
        lines = [f"# String Provenance: {command}", "", "Use JSON output for call-chain and branch evidence."]
    if payload.get("warnings"):
        lines.extend(["", "## Boundaries", "", *(f"- {warning}" for warning in payload["warnings"])])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only interprocedural M&B string-register provenance.")
    parser.add_argument("command", choices=("summary", "paths", "explain"), nargs="?", default="summary")
    parser.add_argument("query", nargs="?", help="Script symbol for paths or visible-sink query for explain.")
    parser.add_argument("--register", help="Required s-register for paths.")
    parser.add_argument("--sink-id")
    parser.add_argument("--kind", default="all", choices=tuple(sorted(ledger_module.VALID_KINDS)))
    parser.add_argument("--only-non-clean", action="store_true")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--max-paths", type=int, default=20)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        index = build_string_provenance(args.root.resolve())
        if args.command == "summary":
            payload = summary_payload(index, limit=args.limit)
        elif args.command == "paths":
            payload = script_paths_payload(index, require_query(args.query, name="script_symbol"), require_register(args.register or ""), limit=args.limit)
        else:
            payload = explain(
                index,
                query=require_query(args.query) if args.query is not None else None,
                sink_id=require_query(args.sink_id, name="sink_id") if args.sink_id is not None else None,
                kind=args.kind,
                include_clean=not args.only_non_clean,
                limit=args.limit,
                max_paths=args.max_paths,
            )
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except (StringProvenanceError, ledger_module.LedgerError, integrity.StringIntegrityError) as error:
        print(f"string_provenance: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
