#!/usr/bin/env python3
"""Read-only execution ledger for visible Mount & Blade 1.011 text.

The ledger compiles a bounded, queryable view of generated module operations.
It does not execute generated Python or game code. Instead, it connects a
visible sink to its lexical conditions, s-register writers, script calls,
selector evidence, global-variable history, menu transitions, source markers,
and string export resolution.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.string_integrity import string_integrity as integrity


LEDGER_VERSION = "0.1.0"
GLOBAL_RE = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*")
LOCAL_RE = re.compile(r":[A-Za-z_][A-Za-z0-9_]*")
STRING_REGISTER_RE = re.compile(r"(?<![A-Za-z0-9_])s\d+(?![A-Za-z0-9_])")
GENERAL_REGISTER_RE = re.compile(r"(?<![A-Za-z0-9_])reg\d+(?![A-Za-z0-9_])")
SYMBOL_RE = re.compile(
    r"\$[A-Za-z_][A-Za-z0-9_]*|:[A-Za-z_][A-Za-z0-9_]*|"
    r"(?<![A-Za-z0-9_])s\d+(?![A-Za-z0-9_])|"
    r"(?<![A-Za-z0-9_])reg\d+(?![A-Za-z0-9_])"
)
SYMBOL_INPUT_RE = re.compile(
    r"^(?:\$[A-Za-z_][A-Za-z0-9_]*|:[A-Za-z_][A-Za-z0-9_]*|s\d+|reg\d+)$"
)
VALID_KINDS = integrity.VALID_KINDS
CONTROL_OPERATIONS = frozenset(
    {
        "else_try_begin",
        "end_try",
        "try_begin",
        "else_try",
        "try_end",
        "try_for_range",
        "try_for_range_backwards",
        "try_for_parties",
        "try_for_agents",
        "try_for_prop_instances",
        "try_for_players",
    }
)
CONDITION_OPERATIONS = frozenset(
    {
        "eq",
        "neq",
        "gt",
        "ge",
        "lt",
        "le",
        "is_between",
        "neg|eq",
        "neg|neq",
        "neg|gt",
        "neg|ge",
        "neg|lt",
        "neg|le",
    }
)
GLOBAL_WRITE_OPERATIONS = frozenset(
    {
        "assign",
        "val_add",
        "val_sub",
        "val_mul",
        "val_div",
        "val_mod",
        "store_add",
        "store_sub",
        "store_mul",
        "store_div",
        "store_mod",
        "store_random_in_range",
        "store_current_day",
        "store_current_hours",
        "store_time_of_day",
        "store_trigger_param_1",
        "store_trigger_param_2",
        "store_trigger_param_3",
    }
)
TRANSITION_OPERATIONS = frozenset(
    {
        "jump_to_menu",
        "start_presentation",
        "change_screen_return",
        "change_screen_trade",
        "change_screen_exchange_members",
        "change_screen_buy_mercenaries",
        "change_screen_view_character",
        "change_screen_map_conversation",
    }
)


class LedgerError(RuntimeError):
    """The requested execution-ledger query cannot be answered safely."""


@dataclass
class OperationRecord:
    id: str
    name: str
    args: tuple[str, ...]
    module_path: str
    compile_line: int
    column: int
    source: dict[str, Any] | None
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    category: str
    node: ast.AST = field(repr=False)
    block_id: str = ""
    ordinal: int = 0


@dataclass
class BlockRecord:
    id: str
    module_path: str
    compile_line: int
    column: int
    node: ast.List = field(repr=False)
    operations: list[OperationRecord] = field(default_factory=list)


@dataclass
class ModuleIndex:
    module: integrity.ModuleData
    blocks: dict[str, BlockRecord]
    block_by_operation_key: dict[tuple[int, int], BlockRecord]
    operation_by_key: dict[tuple[int, int], OperationRecord]
    dialogues_by_line: dict[int, ast.AST]
    menus_by_line: dict[int, ast.AST]
    menu_options_by_line: dict[int, tuple[ast.AST, ast.AST]]


@dataclass
class LedgerIndex:
    root: Path
    signature: tuple[tuple[str, int, int], ...]
    integrity_report: dict[str, Any]
    export_index: dict[str, dict[str, Any]]
    modules: dict[str, ModuleIndex]
    sinks_by_id: dict[str, dict[str, Any]]
    operation_count: int
    writers_by_symbol: dict[str, list[OperationRecord]]
    readers_by_symbol: dict[str, list[OperationRecord]]
    menu_inbound: dict[str, list[OperationRecord]]
    menu_outbound: dict[str, list[OperationRecord]]
    script_effects: dict[str, integrity.ScriptEffect]
    warnings: list[str]


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], LedgerIndex]] = {}


def source_payload(source: integrity.SourceLocation | None) -> dict[str, Any] | None:
    return integrity.source_payload(source)


def base_operation(name: str) -> str:
    return name.rsplit("|", 1)[-1]


def compact(value: str | None, maximum: int = 220) -> str | None:
    return integrity.compact_text(value, maximum)


def symbol_sort_key(symbol: str) -> tuple[int, int, str]:
    if symbol.startswith("s") and symbol[1:].isdigit():
        return (0, int(symbol[1:]), symbol)
    if symbol.startswith("reg") and symbol[3:].isdigit():
        return (1, int(symbol[3:]), symbol)
    if symbol.startswith("$"):
        return (2, 0, symbol)
    if symbol.startswith(":"):
        return (3, 0, symbol)
    return (4, 0, symbol)


def symbols_in_expression(expression: str) -> set[str]:
    return set(SYMBOL_RE.findall(expression))


def direct_symbol(expression: str) -> str | None:
    return expression if SYMBOL_INPUT_RE.fullmatch(expression) else None


def operation_category(name: str) -> str:
    base = base_operation(name)
    if base in CONTROL_OPERATIONS:
        return "control"
    if name in CONDITION_OPERATIONS or base in CONDITION_OPERATIONS:
        return "condition"
    if base == "call_script":
        return "script_call"
    if base in TRANSITION_OPERATIONS:
        return "transition"
    if base in integrity.TEXT_SINK_ARGUMENTS:
        return "text_sink"
    if integrity.is_string_writer(base):
        return "string_writer"
    if base in GLOBAL_WRITE_OPERATIONS or base.startswith(("store_", "val_")):
        return "value_writer"
    return "operation"


def operation_writes(name: str, node: ast.AST, args: Sequence[str]) -> set[str]:
    base = base_operation(name)
    writes: set[str] = set()
    if integrity.is_string_writer(base):
        register = integrity.writer_register_from_operation(node)
        if register is not None:
            writes.add(register)
    elif base in GLOBAL_WRITE_OPERATIONS or base.startswith(("store_", "val_")):
        if args:
            destination = direct_symbol(args[0])
            if destination is not None:
                writes.add(destination)
    return writes


def operation_payload(record: OperationRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "name": record.name,
        "args": list(record.args),
        "category": record.category,
        "compile_path": record.module_path,
        "compile_line": record.compile_line,
        "column": record.column,
        "source": record.source,
        "reads": list(record.reads),
        "writes": list(record.writes),
    }


def workspace_signature(root: Path) -> tuple[tuple[str, int, int], ...]:
    files = [root / relative for relative in integrity.TARGET_MODULES]
    files.extend(root / "_export" / name for name in ("strings.txt", "quick_strings.txt"))
    signature: list[tuple[str, int, int]] = []
    for path in files:
        try:
            stat = path.stat()
        except OSError:
            signature.append((integrity.project_relative(path, root), -1, -1))
        else:
            signature.append((integrity.project_relative(path, root), stat.st_mtime_ns, stat.st_size))
    return tuple(signature)


def require_limit(limit: int, maximum: int = 100) -> int:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= maximum:
        raise LedgerError(f"limit must be an integer from 1 through {maximum}.")
    return limit


def require_query(query: str | None) -> str:
    if not isinstance(query, str) or not query.strip():
        raise LedgerError("query must not be empty.")
    if len(query) > 500:
        raise LedgerError("query must be at most 500 characters.")
    return query


def build_module_index(module: integrity.ModuleData) -> ModuleIndex:
    blocks: dict[str, BlockRecord] = {}
    block_by_operation_key: dict[tuple[int, int], BlockRecord] = {}
    operation_by_key: dict[tuple[int, int], OperationRecord] = {}

    for block_node in integrity.operation_lists(module.tree):
        direct_operations = [
            item for item in block_node.elts if integrity.operation_name(item) is not None
        ]
        if not direct_operations:
            continue
        block_id = (
            f"block:{module.relative_path}:{block_node.lineno}:{block_node.col_offset}"
        )
        block = BlockRecord(
            id=block_id,
            module_path=module.relative_path,
            compile_line=block_node.lineno,
            column=block_node.col_offset,
            node=block_node,
        )
        blocks[block_id] = block
        for ordinal, node in enumerate(direct_operations):
            name = integrity.operation_name(node)
            assert name is not None
            args = (
                tuple(compact(integrity.expression_text(arg)) or "" for arg in node.elts[1:])
                if isinstance(node, ast.Tuple)
                else ()
            )
            writes = operation_writes(name, node, args)
            reads = set().union(*(symbols_in_expression(argument) for argument in args))
            reads.difference_update(writes)
            record = OperationRecord(
                id=f"op:{module.relative_path}:{node.lineno}:{node.col_offset}",
                name=name,
                args=args,
                module_path=module.relative_path,
                compile_line=node.lineno,
                column=node.col_offset,
                source=source_payload(module.source_at(node.lineno)),
                reads=tuple(sorted(reads, key=symbol_sort_key)),
                writes=tuple(sorted(writes, key=symbol_sort_key)),
                category=operation_category(name),
                node=node,
                block_id=block_id,
                ordinal=ordinal,
            )
            block.operations.append(record)
            key = (node.lineno, node.col_offset)
            # A tuple is direct in only one AST list. Keep the first record if
            # malformed input somehow produces a duplicate location.
            block_by_operation_key.setdefault(key, block)
            operation_by_key.setdefault(key, record)

    dialogues_by_line: dict[int, ast.AST] = {}
    dialogs = integrity.find_assignment_list(module.tree, "dialogs")
    if dialogs is not None:
        for entry in dialogs.elts:
            if isinstance(entry, (ast.List, ast.Tuple)) and len(entry.elts) >= 6:
                dialogues_by_line.setdefault(entry.lineno, entry)

    menus_by_line: dict[int, ast.AST] = {}
    menu_options_by_line: dict[int, tuple[ast.AST, ast.AST]] = {}
    menus = integrity.find_assignment_list(module.tree, "game_menus")
    if menus is not None:
        for menu in menus.elts:
            if not isinstance(menu, (ast.List, ast.Tuple)) or len(menu.elts) < 6:
                continue
            menus_by_line.setdefault(menu.lineno, menu)
            options = menu.elts[5]
            if not isinstance(options, ast.List):
                continue
            for option in options.elts:
                if isinstance(option, (ast.List, ast.Tuple)) and len(option.elts) >= 3:
                    menu_options_by_line.setdefault(option.lineno, (menu, option))

    return ModuleIndex(
        module=module,
        blocks=blocks,
        block_by_operation_key=block_by_operation_key,
        operation_by_key=operation_by_key,
        dialogues_by_line=dialogues_by_line,
        menus_by_line=menus_by_line,
        menu_options_by_line=menu_options_by_line,
    )


def menu_id(node: ast.AST) -> str:
    if not isinstance(node, (ast.List, ast.Tuple)) or not node.elts:
        return "<unknown-menu>"
    return integrity.expression_text(node.elts[0])


def menu_owner_for_record(module_index: ModuleIndex, record: OperationRecord) -> str | None:
    for menu in module_index.menus_by_line.values():
        end_line = getattr(menu, "end_lineno", menu.lineno)
        if menu.lineno <= record.compile_line <= end_line:
            return menu_id(menu)
    return None


def transition_target(record: OperationRecord) -> str | None:
    if base_operation(record.name) != "jump_to_menu" or not record.args:
        return None
    target = record.args[0]
    return target[4:] if target.startswith("mnu_") else target


def build_ledger(root: Path = DEFAULT_REPO_ROOT) -> LedgerIndex:
    """Build or reuse a read-only generated-module execution ledger."""
    root = root.resolve()
    if not (root / "compile").is_dir() or not (root / "src").is_dir():
        raise LedgerError(f"Not a recognizable SoD Modern module workspace: {root}")
    signature = workspace_signature(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == signature:
        return cached[1]

    integrity_report = integrity.build_integrity_report(root)
    export_index = integrity.load_export_string_index(root)
    modules, module_errors = integrity.load_modules(root)
    module_indexes = {
        module.relative_path: build_module_index(module)
        for module in modules
    }
    writers_by_symbol: dict[str, list[OperationRecord]] = defaultdict(list)
    readers_by_symbol: dict[str, list[OperationRecord]] = defaultdict(list)
    menu_inbound: dict[str, list[OperationRecord]] = defaultdict(list)
    menu_outbound: dict[str, list[OperationRecord]] = defaultdict(list)
    operation_count = 0
    for module_index in module_indexes.values():
        for block in module_index.blocks.values():
            for record in block.operations:
                operation_count += 1
                for symbol in record.writes:
                    writers_by_symbol[symbol].append(record)
                for symbol in record.reads:
                    readers_by_symbol[symbol].append(record)
                target = transition_target(record)
                if target is not None:
                    menu_inbound[target].append(record)
                    owner = menu_owner_for_record(module_index, record)
                    if owner is not None:
                        menu_outbound[owner].append(record)

    script_module = next(
        (
            module_index.module
            for relative_path, module_index in module_indexes.items()
            if relative_path.endswith("module_scripts.py")
        ),
        None,
    )
    script_effects = integrity.script_effects_from_module(script_module) if script_module else {}
    warnings = [
        (
            "The ledger is a static execution model. It preserves branches, globals, "
            "and unresolved calls as explicit evidence boundaries rather than simulating game state."
        ),
        *integrity_report["warnings"],
    ]
    if module_errors:
        warnings.append("One or more generated modules could not be parsed for the execution ledger.")

    ledger = LedgerIndex(
        root=root,
        signature=signature,
        integrity_report=integrity_report,
        export_index=export_index,
        modules=module_indexes,
        sinks_by_id={sink["id"]: sink for sink in integrity_report["sinks"]},
        operation_count=operation_count,
        writers_by_symbol={key: list(value) for key, value in writers_by_symbol.items()},
        readers_by_symbol={key: list(value) for key, value in readers_by_symbol.items()},
        menu_inbound={key: list(value) for key, value in menu_inbound.items()},
        menu_outbound={key: list(value) for key, value in menu_outbound.items()},
        script_effects=script_effects,
        warnings=list(dict.fromkeys(warnings)),
    )
    _CACHE[root] = (signature, ledger)
    return ledger


def block_for_node(module_index: ModuleIndex, node: ast.AST | None) -> BlockRecord | None:
    if not isinstance(node, ast.List):
        return None
    for block in module_index.blocks.values():
        if block.node is node:
            return block
    return None


def menu_context_payload(menu: ast.AST) -> dict[str, Any]:
    return {
        "menu_id": menu_id(menu),
        "compile_line": getattr(menu, "lineno", 0),
    }


def sink_context(
    ledger: LedgerIndex,
    sink: dict[str, Any],
) -> dict[str, Any]:
    """Return the semantic operation blocks evaluated before this text sink."""
    module_index = ledger.modules.get(sink["compile_path"])
    if module_index is None:
        return {
            "type": "unavailable",
            "label": sink["context"],
            "display_blocks": [],
            "post_display_blocks": [],
        }

    if sink["kind"] == "dialogue_text":
        entry = module_index.dialogues_by_line.get(sink["compile_line"])
        if isinstance(entry, (ast.List, ast.Tuple)) and len(entry.elts) >= 6:
            speaker = integrity.expression_text(entry.elts[0])
            start_state = integrity.expression_text(entry.elts[1])
            end_state = integrity.expression_text(entry.elts[4])
            return {
                "type": "dialogue",
                "label": f"{speaker}::{start_state}->{end_state}",
                "dialogue": {
                    "speaker": speaker,
                    "start_state": start_state,
                    "end_state": end_state,
                },
                "display_blocks": [
                    ("dialogue_conditions", block_for_node(module_index, entry.elts[2])),
                ],
                "post_display_blocks": [
                    ("dialogue_consequences", block_for_node(module_index, entry.elts[5])),
                ],
            }

    if sink["kind"] == "menu_text":
        menu = module_index.menus_by_line.get(sink["compile_line"])
        if isinstance(menu, (ast.List, ast.Tuple)) and len(menu.elts) >= 6:
            return {
                "type": "menu",
                "label": menu_id(menu),
                "menu": menu_context_payload(menu),
                "display_blocks": [
                    ("menu_operations", block_for_node(module_index, menu.elts[4])),
                ],
                "post_display_blocks": [],
            }

    if sink["kind"] == "menu_option_text":
        pair = module_index.menu_options_by_line.get(sink["compile_line"])
        if pair is not None:
            menu, option = pair
            option_id = integrity.expression_text(option.elts[0])
            display_blocks: list[tuple[str, BlockRecord | None]] = []
            if isinstance(menu, (ast.List, ast.Tuple)) and len(menu.elts) >= 6:
                display_blocks.append(("menu_operations", block_for_node(module_index, menu.elts[4])))
            if isinstance(option, (ast.List, ast.Tuple)) and len(option.elts) >= 2:
                display_blocks.append(("option_conditions", block_for_node(module_index, option.elts[1])))
            post_blocks: list[tuple[str, BlockRecord | None]] = []
            if isinstance(option, (ast.List, ast.Tuple)) and len(option.elts) >= 4:
                post_blocks.append(("option_consequences", block_for_node(module_index, option.elts[3])))
            return {
                "type": "menu_option",
                "label": f"{menu_id(menu)}.{option_id}",
                "menu": menu_context_payload(menu),
                "option_id": option_id,
                "display_blocks": display_blocks,
                "post_display_blocks": post_blocks,
            }

    column = sink_column(sink)
    operation = (
        module_index.operation_by_key.get((sink["compile_line"], column))
        if column is not None
        else None
    )
    if operation is None:
        # Integrity records use the operation column for generic sinks. Older
        # artifacts may omit it, so fall back to a line match.
        operation = next(
            (
                record
                for record in module_index.operation_by_key.values()
                if record.compile_line == sink["compile_line"]
            ),
            None,
        )
    block = (
        module_index.blocks.get(operation.block_id)
        if operation is not None
        else None
    )
    return {
        "type": "operation",
        "label": sink["context"],
        "display_blocks": [("operation_block", block)],
        "post_display_blocks": [],
        "sink_operation_id": operation.id if operation else None,
    }


def timeline_for_block(
    block: BlockRecord | None,
    *,
    end_operation_id: str | None = None,
    limit: int,
) -> dict[str, Any]:
    if block is None:
        return {
            "block": None,
            "event_count": 0,
            "returned_count": 0,
            "truncated": False,
            "events": [],
        }
    records = list(block.operations)
    if end_operation_id is not None:
        for index, record in enumerate(records):
            if record.id == end_operation_id:
                records = records[: index + 1]
                break
    return {
        "block": {
            "id": block.id,
            "compile_path": block.module_path,
            "compile_line": block.compile_line,
            "column": block.column,
        },
        "event_count": len(records),
        "returned_count": min(len(records), limit),
        "truncated": len(records) > limit,
        "events": [operation_payload(record) for record in records[:limit]],
    }


def context_metadata(context: dict[str, Any]) -> dict[str, Any]:
    result = {
        "type": context["type"],
        "label": context["label"],
    }
    for key in ("dialogue", "menu", "option_id", "sink_operation_id"):
        if key in context:
            result[key] = context[key]
    return result


def section_records(
    context: dict[str, Any],
    *,
    post_display: bool = False,
) -> list[tuple[str, list[OperationRecord]]]:
    key = "post_display_blocks" if post_display else "display_blocks"
    sections: list[tuple[str, list[OperationRecord]]] = []
    for role, block in context.get(key, []):
        if block is None:
            sections.append((role, []))
            continue
        records = list(block.operations)
        if not post_display and context.get("sink_operation_id") and role == "operation_block":
            sink_operation_id = context["sink_operation_id"]
            for index, record in enumerate(records):
                if record.id == sink_operation_id:
                    records = records[: index + 1]
                    break
        sections.append((role, records))
    return sections


def timeline_sections(
    sections: Sequence[tuple[str, list[OperationRecord]]],
    *,
    limit: int,
) -> dict[str, Any]:
    remaining = limit
    payload: list[dict[str, Any]] = []
    total = 0
    for role, records in sections:
        total += len(records)
        shown = records[: max(remaining, 0)]
        remaining -= len(shown)
        payload.append(
            {
                "role": role,
                "event_count": len(records),
                "returned_count": len(shown),
                "truncated": len(shown) < len(records),
                "events": [operation_payload(record) for record in shown],
            }
        )
    return {
        "event_count": total,
        "returned_count": sum(section["returned_count"] for section in payload),
        "truncated": total > limit,
        "sections": payload,
    }


def latest_records_for_symbol(
    records: Sequence[OperationRecord],
    symbol: str,
    *,
    limit: int = 8,
) -> list[OperationRecord]:
    matches = [record for record in records if symbol in record.writes]
    return list(reversed(matches[-limit:]))


def value_candidate_from_record(
    ledger: LedgerIndex,
    record: OperationRecord,
) -> dict[str, Any]:
    base = base_operation(record.name)
    result: dict[str, Any] = {
        "operation_id": record.id,
        "operation": record.name,
        "compile_path": record.module_path,
        "compile_line": record.compile_line,
        "source": record.source,
    }
    if base == "str_clear":
        result.update({"kind": "empty", "value": ""})
        return result
    if (
        base == "str_store_string"
        and isinstance(record.node, ast.Tuple)
        and len(record.node.elts) >= 3
    ):
        value = integrity.text_value(record.node.elts[2], ledger.export_index)
        result.update({"kind": "str_store_string", "value": value})
        return result
    if (
        base == "str_store_string_reg"
        and isinstance(record.node, ast.Tuple)
        and len(record.node.elts) >= 3
    ):
        source = integrity.expression_text(record.node.elts[2])
        result.update({"kind": "register_copy", "source_register_or_selector": source})
        return result
    result.update(
        {
            "kind": "engine_or_dynamic_writer",
            "args": list(record.args),
        }
    )
    return result


def dynamic_selector_candidates(
    ledger: LedgerIndex,
    writer: dict[str, Any] | None,
    display_records: Sequence[OperationRecord],
) -> dict[str, Any] | None:
    if not writer:
        return None
    bounds = writer.get("source_selector_bounds")
    if not isinstance(bounds, list) or len(bounds) != 2:
        return None
    lower, upper = bounds
    if not isinstance(lower, int) or not isinstance(upper, int):
        return None
    register_names = [f"s{number}" for number in range(lower, min(upper, lower + 31) + 1)]
    candidates: list[dict[str, Any]] = []
    for register in register_names:
        latest = latest_records_for_symbol(display_records, register, limit=1)
        if latest:
            candidate = value_candidate_from_record(ledger, latest[0])
            candidate["selector_register"] = register
            candidates.append(candidate)
        else:
            candidates.append(
                {
                    "selector_register": register,
                    "kind": "writer_not_proven_in_display_context",
                }
            )
    return {
        "source_expression": writer.get("source_expression"),
        "bounds": [lower, upper],
        "candidate_register_count": upper - lower + 1,
        "returned_candidate_count": len(candidates),
        "truncated": upper - lower + 1 > len(register_names),
        "candidates": candidates,
    }


def register_dependencies(
    ledger: LedgerIndex,
    sink: dict[str, Any],
    display_records: Sequence[OperationRecord],
) -> list[dict[str, Any]]:
    dependencies: list[dict[str, Any]] = []
    for assessment in sink["register_assessments"]:
        register = assessment["register"]
        writer = assessment.get("last_known_writer")
        local_candidates = [
            value_candidate_from_record(ledger, record)
            for record in latest_records_for_symbol(display_records, register)
        ]
        dependency = {
            "register": register,
            "register_band": assessment["register_band"],
            "status": assessment["status"],
            "confidence": assessment["confidence"],
            "issues": assessment["issues"],
            "last_known_writer": writer,
            "display_context_writer_candidates": local_candidates,
        }
        selector = dynamic_selector_candidates(ledger, writer, display_records)
        if selector is not None:
            dependency["dynamic_selector"] = selector
        dependencies.append(dependency)
    return dependencies


def script_calls(
    ledger: LedgerIndex,
    records: Sequence[OperationRecord],
) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for record in records:
        if base_operation(record.name) != "call_script":
            continue
        symbol = integrity.call_script_symbol(record.node)
        effect = ledger.script_effects.get(symbol) if symbol else None
        calls.append(
            {
                "operation": operation_payload(record),
                "script_symbol": symbol,
                "resolved_static_effect": effect is not None,
                "transitive_string_register_writes": (
                    sorted(effect.transitive_writes, key=integrity.register_number)
                    if effect is not None
                    else []
                ),
                "has_unresolved_nested_call": (
                    effect.transitive_unknown if effect is not None else True
                ),
                "script_source": source_payload(effect.source) if effect is not None else None,
            }
        )
    return calls


def global_state_dependencies(
    ledger: LedgerIndex,
    records: Sequence[OperationRecord],
    *,
    per_symbol_limit: int = 8,
) -> list[dict[str, Any]]:
    globals_read = sorted(
        {
            symbol
            for record in records
            for symbol in record.reads
            if symbol.startswith("$")
        }
    )
    result: list[dict[str, Any]] = []
    for symbol in globals_read:
        writers = ledger.writers_by_symbol.get(symbol, [])
        readers = ledger.readers_by_symbol.get(symbol, [])
        result.append(
            {
                "symbol": symbol,
                "workspace_writer_count": len(writers),
                "workspace_reader_count": len(readers),
                "writers": [
                    operation_payload(record)
                    for record in writers[:per_symbol_limit]
                ],
                "writers_truncated": len(writers) > per_symbol_limit,
            }
        )
    return result


def menu_navigation(
    ledger: LedgerIndex,
    context: dict[str, Any],
    *,
    limit: int = 12,
) -> dict[str, Any] | None:
    menu = context.get("menu")
    if not isinstance(menu, dict):
        return None
    identifier = menu["menu_id"]
    inbound = ledger.menu_inbound.get(identifier, [])
    outbound = ledger.menu_outbound.get(identifier, [])
    return {
        "menu_id": identifier,
        "inbound_count": len(inbound),
        "outbound_count": len(outbound),
        "inbound": [operation_payload(record) for record in inbound[:limit]],
        "outbound": [operation_payload(record) for record in outbound[:limit]],
        "inbound_truncated": len(inbound) > limit,
        "outbound_truncated": len(outbound) > limit,
    }


def condition_and_control_events(
    records: Sequence[OperationRecord],
    *,
    limit: int = 40,
) -> dict[str, Any]:
    selected = [
        record
        for record in records
        if record.category in {"condition", "control"}
    ]
    return {
        "event_count": len(selected),
        "returned_count": min(len(selected), limit),
        "truncated": len(selected) > limit,
        "events": [operation_payload(record) for record in selected[:limit]],
    }


def possible_text_model(
    sink: dict[str, Any],
    dependencies: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "template": sink["text_input"],
        "substitutions": [
            {
                "register": dependency["register"],
                "status": dependency["status"],
                "confidence": dependency["confidence"],
                "last_known_writer": dependency["last_known_writer"],
                "display_context_writer_candidates": dependency[
                    "display_context_writer_candidates"
                ],
                "dynamic_selector": dependency.get("dynamic_selector"),
            }
            for dependency in dependencies
        ],
        "note": (
            "This is a static set of template and substitution candidates, not a claim "
            "that every branch or game-state value is reachable in one playthrough."
        ),
    }


def sink_column(sink: dict[str, Any]) -> int | None:
    column = sink.get("compile_column")
    if isinstance(column, int):
        return column
    # Legacy String Integrity artifacts encoded the column in the stable ID.
    # Relative paths cannot contain a colon, so the first numeric pair is safe.
    parts = sink["id"].split(":")
    if len(parts) >= 5:
        try:
            return int(parts[3])
        except ValueError:
            return None
    return None


def sink_haystack(sink: dict[str, Any]) -> str:
    source = sink.get("source") or {}
    text = sink["text_input"]
    return " ".join(
        (
            sink["id"],
            sink["context"],
            sink["compile_path"],
            source.get("path", ""),
            text.get("expression") or "",
            text.get("literal_preview") or "",
        )
    ).casefold()


def select_sinks(
    ledger: LedgerIndex,
    *,
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 20,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    if kind not in VALID_KINDS:
        raise LedgerError(f"kind must be one of: {', '.join(sorted(VALID_KINDS))}.")
    if query is not None:
        require_query(query)
    if sink_id is not None and (not isinstance(sink_id, str) or not sink_id.strip()):
        raise LedgerError("sink_id must not be empty.")
    if query is None and sink_id is None:
        raise LedgerError("Specify query or sink_id.")

    if sink_id is not None:
        candidate = ledger.sinks_by_id.get(sink_id)
        selected = [candidate] if candidate is not None else []
    else:
        query_folded = query.casefold() if query else ""
        selected = []
        for sink in ledger.integrity_report["sinks"]:
            if kind != "all" and sink["category"] != kind:
                continue
            if not include_clean and sink["status"] == "clean":
                continue
            if query_folded not in sink_haystack(sink):
                continue
            selected.append(sink)

    selected = [sink for sink in selected if sink is not None]
    selected.sort(
        key=lambda sink: (
            -integrity.SEVERITY_RANK.get(sink["status"], 0),
            sink["compile_path"],
            sink["compile_line"],
            sink["id"],
        )
    )
    return {
        "filters": {
            "query": query,
            "sink_id": sink_id,
            "kind": kind,
            "include_clean": include_clean,
        },
        "match_count": len(selected),
        "returned_count": min(len(selected), maximum),
        "truncated": len(selected) > maximum,
        "sinks": selected[:maximum],
    }


def explain_sink(
    ledger: LedgerIndex,
    sink: dict[str, Any],
    *,
    max_steps: int,
) -> dict[str, Any]:
    context = sink_context(ledger, sink)
    display_sections = section_records(context)
    post_sections = section_records(context, post_display=True)
    display_records = [
        record
        for _, records in display_sections
        for record in records
    ]
    post_records = [
        record
        for _, records in post_sections
        for record in records
    ]
    dependencies = register_dependencies(ledger, sink, display_records)
    return {
        "sink": sink,
        "execution_context": context_metadata(context),
        "display_timeline": timeline_sections(display_sections, limit=max_steps),
        "post_display_timeline": timeline_sections(post_sections, limit=min(max_steps, 60)),
        "conditions_and_control": condition_and_control_events(display_records),
        "register_dependencies": dependencies,
        "script_calls_before_display": script_calls(ledger, display_records),
        "global_state_dependencies": global_state_dependencies(ledger, display_records),
        "menu_navigation": menu_navigation(ledger, context),
        "possible_text": possible_text_model(sink, dependencies),
    }


def explain(
    ledger: LedgerIndex,
    *,
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 10,
    max_steps: int = 100,
) -> dict[str, Any]:
    maximum_steps = require_limit(max_steps, 250)
    selection = select_sinks(
        ledger,
        query=query,
        sink_id=sink_id,
        kind=kind,
        include_clean=include_clean,
        limit=limit,
    )
    return {
        "summary": ledger_summary(ledger),
        **{key: value for key, value in selection.items() if key != "sinks"},
        "explanations": [
            explain_sink(ledger, sink, max_steps=maximum_steps)
            for sink in selection["sinks"]
        ],
        "warnings": ledger.warnings,
    }


def symbol_kind(symbol: str) -> str:
    if symbol.startswith("$"):
        return "global"
    if symbol.startswith(":"):
        return "local"
    if symbol.startswith("s"):
        return "string_register"
    if symbol.startswith("reg"):
        return "general_register"
    return "unknown"


def register_history(
    ledger: LedgerIndex,
    symbol: str,
    *,
    limit: int = 30,
) -> dict[str, Any]:
    if not isinstance(symbol, str) or not SYMBOL_INPUT_RE.fullmatch(symbol):
        raise LedgerError("symbol must be an s-register, reg-register, local, or global variable.")
    maximum = require_limit(limit)
    writers = sorted(
        ledger.writers_by_symbol.get(symbol, []),
        key=lambda record: (record.module_path, record.compile_line, record.column),
    )
    readers = sorted(
        ledger.readers_by_symbol.get(symbol, []),
        key=lambda record: (record.module_path, record.compile_line, record.column),
    )
    events = [
        {"access": "write", "operation": operation_payload(record)}
        for record in writers
    ] + [
        {"access": "read", "operation": operation_payload(record)}
        for record in readers
    ]
    events.sort(
        key=lambda item: (
            item["operation"]["compile_path"],
            item["operation"]["compile_line"],
            item["operation"]["column"],
            item["access"],
        )
    )
    return {
        "summary": ledger_summary(ledger),
        "symbol": symbol,
        "symbol_kind": symbol_kind(symbol),
        "workspace_writer_count": len(writers),
        "workspace_reader_count": len(readers),
        "event_count": len(events),
        "returned_count": min(len(events), maximum),
        "truncated": len(events) > maximum,
        "events": events[:maximum],
        "warnings": ledger.warnings,
    }


def possible_texts(
    ledger: LedgerIndex,
    *,
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 10,
) -> dict[str, Any]:
    selection = select_sinks(
        ledger,
        query=query,
        sink_id=sink_id,
        kind=kind,
        include_clean=include_clean,
        limit=limit,
    )
    entries: list[dict[str, Any]] = []
    for sink in selection["sinks"]:
        context = sink_context(ledger, sink)
        display_records = [
            record
            for _, records in section_records(context)
            for record in records
        ]
        dependencies = register_dependencies(ledger, sink, display_records)
        entries.append(
            {
                "sink_id": sink["id"],
                "context": context_metadata(context),
                "source": sink["source"],
                "status": sink["status"],
                "possible_text": possible_text_model(sink, dependencies),
            }
        )
    return {
        "summary": ledger_summary(ledger),
        **{key: value for key, value in selection.items() if key != "sinks"},
        "entries": entries,
        "warnings": ledger.warnings,
    }


def ledger_summary(ledger: LedgerIndex) -> dict[str, Any]:
    sinks = ledger.integrity_report["sinks"]
    integrity_summary = ledger.integrity_report["summary"]
    category_counts = Counter(sink["category"] for sink in sinks)
    block_count = sum(len(module.blocks) for module in ledger.modules.values())
    source_mapped_operations = sum(
        record.source is not None
        for module in ledger.modules.values()
        for block in module.blocks.values()
        for record in block.operations
    )
    return {
        "ledger_version": f"devkit.text-execution-ledger.v{LEDGER_VERSION}",
        "generated_module_count": len(ledger.modules),
        "operation_count": ledger.operation_count,
        "operation_block_count": block_count,
        "source_mapped_operation_count": source_mapped_operations,
        "visible_sink_count": len(sinks),
        "visible_sink_count_by_category": dict(sorted(category_counts.items())),
        "tracked_symbol_writer_count": len(ledger.writers_by_symbol),
        "tracked_symbol_reader_count": len(ledger.readers_by_symbol),
        "menu_transition_count": sum(len(values) for values in ledger.menu_inbound.values()),
        "known_script_effect_count": len(ledger.script_effects),
        "string_integrity_overview": {
            "text_sink_count": integrity_summary["text_sink_count"],
            "source_mapped_sink_count": integrity_summary["source_mapped_sink_count"],
            "sink_status_count": integrity_summary["sink_status_count"],
            "sink_issue_count_by_code": integrity_summary["sink_issue_count_by_code"],
            "script_effects": {
                key: value
                for key, value in integrity_summary["script_effects"].items()
                if key != "distinct_string_registers_written"
            },
        },
    }


def summary_payload(ledger: LedgerIndex, limit: int = 20) -> dict[str, Any]:
    maximum = require_limit(limit)
    dynamic_findings = [
        finding
        for finding in ledger.integrity_report["writer_contract_findings"]
        if "DYNAMIC_STRING_REGISTER" in finding["code"]
    ]
    global_symbols = sorted(
        (
            (symbol, len(records))
            for symbol, records in ledger.writers_by_symbol.items()
            if symbol.startswith("$")
        ),
        key=lambda item: (-item[1], item[0]),
    )
    return {
        "summary": ledger_summary(ledger),
        "dynamic_selector_findings": dynamic_findings[:maximum],
        "dynamic_selector_finding_count": len(dynamic_findings),
        "most_written_globals": [
            {"symbol": symbol, "writer_count": count}
            for symbol, count in global_symbols[:maximum]
        ],
        "most_written_globals_truncated": len(global_symbols) > maximum,
        "warnings": ledger.warnings,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# SoD Modern Text Execution Ledger",
        "",
        "Read-only, generated-module execution evidence for visible text.",
        "",
        f"- Generated operations indexed: {summary['operation_count']:,}.",
        f"- Visible text sinks: {summary['visible_sink_count']:,}.",
        f"- Source-mapped operations: {summary['source_mapped_operation_count']:,}.",
        f"- Known script effects: {summary['known_script_effect_count']:,}.",
        f"- Menu transitions: {summary['menu_transition_count']:,}.",
    ]
    if "explanations" in payload:
        lines.extend(["", "## Explanations", ""])
        if not payload["explanations"]:
            lines.append("- No matching text sink.")
        for explanation in payload["explanations"]:
            sink = explanation["sink"]
            context = explanation["execution_context"]
            lines.extend(
                (
                    f"- {context['label']} at {sink['compile_path']}:{sink['compile_line']}",
                    f"  - sink: {sink['kind']} ({sink['status']})",
                    f"  - template: {sink['text_input']['expression']}",
                    f"  - display events: {explanation['display_timeline']['event_count']}",
                    f"  - register dependencies: {len(explanation['register_dependencies'])}",
                )
            )
    if "symbol" in payload:
        lines.extend(
            (
                "",
                "## Symbol history",
                "",
                f"- Symbol: {payload['symbol']} ({payload['symbol_kind']}).",
                f"- Workspace writers: {payload['workspace_writer_count']:,}.",
                f"- Workspace readers: {payload['workspace_reader_count']:,}.",
            )
        )
    if payload.get("warnings"):
        lines.extend(["", "## Limits", ""])
        lines.extend(f"- {warning}" for warning in payload["warnings"])
    return "\n".join(lines) + "\n"


def output_path(path_arg: str, root: Path) -> Path:
    path = Path(path_arg)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    export_root = (root / "_export").resolve()
    try:
        path.relative_to(export_root)
    except ValueError:
        return path
    raise LedgerError("Refusing to write a ledger artifact under _export/.")


def add_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--query")
    parser.add_argument("--sink-id")
    parser.add_argument("--kind", choices=tuple(sorted(VALID_KINDS)), default="all")
    parser.add_argument(
        "--only-non-clean",
        action="store_true",
        help="Hide clean sink results; the default is to explain matching text regardless of status.",
    )
    parser.add_argument("--limit", type=int, default=10)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only SoD Modern visible-text execution ledger."
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--limit", type=int, default=20)
    summary_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    summary_parser.add_argument("--output")

    explain_parser = subparsers.add_parser("explain")
    add_selection_arguments(explain_parser)
    explain_parser.add_argument("--max-steps", type=int, default=100)
    explain_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    explain_parser.add_argument("--output")

    history_parser = subparsers.add_parser("history")
    history_parser.add_argument("symbol")
    history_parser.add_argument("--limit", type=int, default=30)
    history_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    history_parser.add_argument("--output")

    possible_parser = subparsers.add_parser("possible-texts")
    add_selection_arguments(possible_parser)
    possible_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    possible_parser.add_argument("--output")

    args = parser.parse_args(argv)
    command = args.command or "summary"
    if args.command is None:
        args.limit = 20
        args.format = "json"
        args.output = None

    try:
        ledger = build_ledger(DEFAULT_REPO_ROOT)
        if command == "summary":
            payload = summary_payload(ledger, args.limit)
        elif command == "explain":
            payload = explain(
                ledger,
                query=args.query,
                sink_id=args.sink_id,
                kind=args.kind,
                include_clean=not args.only_non_clean,
                limit=args.limit,
                max_steps=args.max_steps,
            )
        elif command == "history":
            payload = register_history(ledger, args.symbol, limit=args.limit)
        else:
            payload = possible_texts(
                ledger,
                query=args.query,
                sink_id=args.sink_id,
                kind=args.kind,
                include_clean=not args.only_non_clean,
                limit=args.limit,
            )
        rendered = (
            json.dumps(payload, indent=2, sort_keys=True)
            if args.format == "json"
            else render_markdown(payload)
        )
        if args.output:
            path = output_path(args.output, DEFAULT_REPO_ROOT)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                rendered + ("" if rendered.endswith("\n") else "\n"),
                encoding="utf-8",
            )
        else:
            sys.stdout.write(rendered + ("" if rendered.endswith("\n") else "\n"))
    except (LedgerError, integrity.StringIntegrityError) as error:
        print(f"text_execution_ledger: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
