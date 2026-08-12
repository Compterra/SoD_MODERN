#!/usr/bin/env python3
"""Static semantic preflight for M&B 1.011 string/register text flow.

The legacy compiler accepts many semantically-invalid text paths. This analyzer
reads generated modules without importing them, identifies visible text sinks,
and tracks the last writer it can prove in the same lexical operation block or
through a statically-known script call. It is deliberately conservative about
branching, engine state, and unknown scripts.
"""

from __future__ import annotations

import argparse
import ast
import bisect
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Sequence


ANALYZER_VERSION = "1.5.0"
TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]

# The engine has 128 string-register slots.  Its text formatter, however,
# only accepts two digits inside a {sN} placeholder, so s100-s127 can be
# copied/manipulated but cannot be interpolated into a formatted string.
ENGINE_STRING_REGISTER_MAX = 127
FORMATTER_STRING_REGISTER_MAX = 99

TARGET_MODULES = (
    "compile/module_dialogs.py",
    "compile/module_game_menus.py",
    "compile/module_presentations.py",
    "compile/module_scripts.py",
    "compile/module_simple_triggers.py",
    "compile/module_mission_templates.py",
    "compile/module_quests.py",
    "compile/module_triggers.py",
)

# Generated M&B 1.011 modules encode a no-argument operation as a bare
# Python name instead of the usual one-element tuple.  A bare name can also be
# ordinary module data (for example ``anyone`` or ``trp_player``), so accepting
# every ``ast.Name`` would turn data lists into fictional operation blocks.
#
# This is the deliberately small, engine-header-derived allowlist of operations
# that may legally occur with no operands.  It includes deprecated aliases
# still emitted by older source fragments and optional-only operations that may
# be written without their optional operands.  Additions should be checked
# against ``compile/headers/header_operations.py`` rather than inferred from
# a generated module alone.
ZERO_ARGUMENT_OPERATIONS = frozenset(
    {
        "add_point_light",
        "all_enemies_defeated",
        "change_screen_buy_mercenaries",
        "change_screen_exchange_members",
        "change_screen_give_members",
        "change_screen_map",
        "change_screen_map_conversation",
        "change_screen_mission",
        "change_screen_quit",
        "change_screen_return",
        "change_screen_trade",
        "change_screen_trade_prisoners",
        "change_screen_training",
        "change_screen_view_character",
        "conversation_screen_is_active",
        "cur_tableau_clear_override_items",
        "cur_tableau_render_as_alpha_mask",
        "disable_menu_option",
        "else_try",
        "else_try_begin",
        "encounter_attack",
        "encountered_party_is_attacker",
        "end_current_battle",
        "end_try",
        "finish_mission",
        "hero_can_join",
        "hero_can_join_as_prisoner",
        "in_meta_mission",
        "is_currently_night",
        "leave_encounter",
        "main_hero_fallen",
        "map_free",
        "mission_cam_clear_target_agent",
        "mission_disable_talk",
        "mission_enable_talk",
        "party_can_join",
        "party_can_join_as_prisoner",
        "party_join",
        "party_join_as_prisoner",
        "race_completed_by_player",
        "reset_item_probabilities",
        "reset_mission_timer_a",
        "reset_mission_timer_b",
        "reset_mission_timer_c",
        "reset_price_rates",
        "reset_visitors",
        "set_party_battle_mode",
        "stop_all_sounds",
        "try_begin",
        "try_end",
    }
)

TEXT_SINK_ARGUMENTS: dict[str, tuple[int, ...]] = {
    "create_text_overlay": (2,),
    "create_button_overlay": (2,),
    "create_game_button_overlay": (2,),
    "overlay_set_text": (2,),
    "display_message": (1,),
    "dialog_box": (1, 2),
    "tutorial_box": (1, 2),
}

PLACEHOLDER_RE = re.compile(r"\{s(?P<number>\d+)\}")
REGISTER_RE = re.compile(r"^s(?P<number>\d+)$")
SOURCE_MARKER_RE = re.compile(
    r"(?m)^\s*#\s*\[\s*(?P<path>src/[^\]\r\n:]+)"
    r"(?::L(?P<start>\d+)(?:-L(?P<end>\d+))?)?\s*\]"
)

SEVERITY_RANK = {"clean": 0, "info": 1, "warning": 2, "error": 3}
VALID_KINDS = frozenset({"all", "dialogue", "menu", "presentation", "message"})


class StringIntegrityError(RuntimeError):
    """A requested integrity analysis cannot be completed safely."""


@dataclass(frozen=True)
class SourceLocation:
    path: str
    line_start: int | None
    line_end: int | None


@dataclass
class ModuleData:
    path: Path
    relative_path: str
    raw: str
    tree: ast.Module
    marker_lines: list[int]
    markers: list[SourceLocation]

    def source_at(self, line: int) -> SourceLocation | None:
        index = bisect.bisect_right(self.marker_lines, line) - 1
        if index < 0:
            return None
        return self.markers[index]


@dataclass
class Writer:
    register: str
    operation: str
    module_path: str
    compile_line: int
    ordinal: int
    source: SourceLocation | None
    source_expression: str | None
    source_kind: str | None
    source_export: dict[str, Any] | None
    source_register: str | None
    source_selector_bounds: tuple[int, int] | None
    input_writer: dict[str, Any] | None
    input_status: str | None
    via_script: str | None = None
    via_script_source: SourceLocation | None = None
    issues: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class SelectorBounds:
    """A lexically proven inclusive numeric range for one local selector."""

    minimum: int
    maximum: int
    compile_line: int
    operation: str


@dataclass(frozen=True)
class CallBarrier:
    ordinal: int
    compile_line: int
    script_symbol: str | None
    source: SourceLocation | None


@dataclass(frozen=True)
class SinkEvent:
    operation: ast.AST
    operation_name: str
    argument_index: int
    ordinal: int
    state: dict[str, Writer]
    unknown_calls: tuple[CallBarrier, ...]
    control_flow: bool
    block_line: int


@dataclass
class BlockFlow:
    final_state: dict[str, Writer]
    unknown_calls: tuple[CallBarrier, ...]
    control_flow: bool
    sink_events: list[SinkEvent]


@dataclass
class ScriptEffect:
    symbol: str
    source: SourceLocation | None
    direct_writes: set[str]
    called_symbols: set[str]
    unresolved_calls: set[str]
    transitive_writes: set[str] = field(default_factory=set)
    transitive_unknown: bool = False


@dataclass
class AnalyzerContext:
    root: Path
    export_index: dict[str, dict[str, Any]]
    script_effects: dict[str, ScriptEffect]
    block_flows: dict[int, BlockFlow] = field(default_factory=dict)
    writer_findings: list[dict[str, Any]] = field(default_factory=list)
    writer_finding_keys: set[tuple[str, int, str, str]] = field(default_factory=set)


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
    raise StringIntegrityError(f"Could not decode {path}: {last_error}")


def source_payload(source: SourceLocation | None) -> dict[str, Any] | None:
    if source is None:
        return None
    return {
        "path": source.path,
        "line_start": source.line_start,
        "line_end": source.line_end,
    }


def extract_source_markers(raw: str) -> tuple[list[int], list[SourceLocation]]:
    marker_lines: list[int] = []
    markers: list[SourceLocation] = []
    for match in SOURCE_MARKER_RE.finditer(raw):
        line = raw.count("\n", 0, match.start()) + 1
        marker_lines.append(line)
        markers.append(
            SourceLocation(
                path=match.group("path"),
                line_start=int(match.group("start")) if match.group("start") else None,
                line_end=int(match.group("end")) if match.group("end") else None,
            )
        )
    return marker_lines, markers


def load_modules(root: Path) -> tuple[list[ModuleData], list[str]]:
    modules: list[ModuleData] = []
    errors: list[str] = []
    for relative_path in TARGET_MODULES:
        path = root / relative_path
        if not path.is_file():
            errors.append(f"Missing generated module: {relative_path}.")
            continue
        raw = read_text_compatible(path)
        try:
            tree = ast.parse(raw, filename=str(path))
        except SyntaxError as error:
            errors.append(f"Could not parse {relative_path}:{error.lineno}: {error.msg}")
            continue
        marker_lines, markers = extract_source_markers(raw)
        modules.append(
            ModuleData(
                path=path,
                relative_path=relative_path.replace("\\", "/"),
                raw=raw,
                tree=tree,
                marker_lines=marker_lines,
                markers=markers,
            )
        )
    return modules, errors


def expression_text(node: ast.AST | None) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{expression_text(node.left)}|{expression_text(node.right)}"
    try:
        return ast.unparse(node).strip()
    except Exception:
        return "<unavailable>"


def string_register(
    node: ast.AST | None,
    *,
    allow_numeric: bool = False,
) -> str | None:
    match = REGISTER_RE.fullmatch(expression_text(node))
    if match:
        return match.group(0)
    if (
        allow_numeric
        and isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
        and node.value >= 0
    ):
        return f"s{node.value}"
    return None


def register_number(register: str) -> int:
    match = REGISTER_RE.fullmatch(register)
    if match is None:
        raise StringIntegrityError(f"Not a string register: {register}")
    return int(match.group("number"))


def register_band(register: str) -> str:
    number = register_number(register)
    if number <= 67:
        return "legacy_volatile"
    if number <= 99:
        return "feature_scratch"
    if number <= ENGINE_STRING_REGISTER_MAX:
        return "engine_extended_not_placeholder"
    return "unsupported"


def compact_text(value: str | None, maximum: int = 220) -> str | None:
    if value is None:
        return None
    cleaned = value.replace("\r", "\\r").replace("\n", "\\n")
    return cleaned if len(cleaned) <= maximum else cleaned[: maximum - 3] + "..."


def load_export_string_index(root: Path) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    specifications = (
        ("_export/strings.txt", 2, "strings.txt"),
        ("_export/quick_strings.txt", 1, "quick_strings.txt"),
    )
    for relative_path, start_line, layer in specifications:
        path = root / relative_path
        if not path.is_file():
            continue
        for line in read_text_compatible(path).splitlines()[start_line:]:
            identifier, separator, encoded = line.partition(" ")
            if not separator or not (identifier.startswith("str_") or identifier.startswith("qstr_")):
                continue
            index.setdefault(
                identifier,
                {
                    "layer": layer,
                    "path": relative_path,
                    "encoded_text": compact_text(encoded),
                },
            )
    return index


def text_value(
    node: ast.AST | None,
    export_index: dict[str, dict[str, Any]],
    *,
    allow_numeric_register: bool = False,
) -> dict[str, Any]:
    expression = expression_text(node)
    direct_register = string_register(node, allow_numeric=allow_numeric_register)
    if direct_register is not None:
        return {
            "kind": "register",
            "expression": direct_register,
            "literal_preview": None,
            "string_id": None,
            "resolved_export": None,
            "registers": [direct_register],
        }

    literal = node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None
    string_id = expression if expression.startswith(("str_", "qstr_")) else None
    registers: list[str] = []
    if literal is not None:
        registers = [f"s{match.group('number')}" for match in PLACEHOLDER_RE.finditer(literal)]
    return {
        "kind": "string_id" if string_id else "literal" if literal is not None else "dynamic_expression",
        "expression": compact_text(expression),
        "literal_preview": compact_text(literal),
        "string_id": string_id,
        "resolved_export": export_index.get(string_id) if string_id else None,
        "registers": list(dict.fromkeys(registers)),
    }


def operation_name(node: ast.AST) -> str | None:
    # M&B emits zero-argument operations as bare names, for example
    # try_begin, else_try, try_end, and encounter_attack.  They are still
    # operations and must remain in the flow model.
    if isinstance(node, ast.Name):
        return node.id if node.id in ZERO_ARGUMENT_OPERATIONS else None
    # Flag-qualified zero-argument operations are valid M&B syntax, for
    # example ``neg|party_can_join`` in a dialogue condition list.  Treat
    # them as operations so a guarded block is not modeled as unconditional.
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return expression_text(node)
    # The legacy module system accepts either ``(operation, ...)`` or
    # ``[operation, ...]`` as an operation literal. The latter is common in
    # older dialogue fragments and must retain exactly the same data-flow
    # semantics in this analyzer.
    if not isinstance(node, (ast.Tuple, ast.List)) or not node.elts:
        return None
    head = node.elts[0]
    if isinstance(head, ast.Name):
        return head.id
    if isinstance(head, ast.BinOp) and isinstance(head.op, ast.BitOr):
        return expression_text(head)
    return None


def operation_lists(tree: ast.AST) -> Iterable[ast.List]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.List) or not node.elts:
            continue
        # Generated operation blocks are usually homogeneous, but a number of
        # valid module constructs splice in a dynamic expression alongside
        # ordinary operation tuples.  Requiring every direct child to be an
        # operation silently drops the real sinks in those blocks.  Each tuple
        # is still considered only once (as a direct child of this list), and
        # analyze_block ignores the non-operation children.
        if any(operation_name(item) is not None for item in node.elts):
            yield node


def find_assignment_list(tree: ast.Module, name: str) -> ast.List | None:
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == name for target in statement.targets):
            continue
        if isinstance(statement.value, ast.List):
            return statement.value
    return None


def call_script_symbol(operation: ast.AST) -> str | None:
    if (
        not isinstance(operation, (ast.Tuple, ast.List))
        or operation_name(operation) != "call_script"
        or len(operation.elts) < 2
    ):
        return None
    candidate = expression_text(operation.elts[1])
    return candidate if candidate.startswith("script_") else None


def is_string_writer(operation: str) -> bool:
    return operation == "str_clear" or operation.startswith("str_store_")


def writer_register_from_operation(operation: ast.AST) -> str | None:
    name = operation_name(operation)
    if (
        not isinstance(operation, (ast.Tuple, ast.List))
        or name is None
        or not is_string_writer(name)
        or len(operation.elts) < 2
    ):
        return None
    # The generated module may use a raw integer for s100-s127 because the
    # stock header only names the lower registers.  This position is always a
    # destination register, so integer operands are unambiguous here.
    return string_register(operation.elts[1], allow_numeric=True)


def register_selector_kind(node: ast.AST | None) -> str:
    """Classify the source operand of str_store_string_reg.

    M&B resolves operation operands at runtime.  A local/global/general
    register may therefore intentionally hold a string-register number for a
    dynamic copy.  That is a meaningful analysis boundary, not a malformed
    operation by itself.
    """
    if string_register(node, allow_numeric=True) is not None:
        return "direct"
    expression = expression_text(node)
    if expression.startswith((":", "$")) or re.fullmatch(r"reg\d+", expression):
        return "indirect"
    return "invalid"


def local_selector_name(node: ast.AST | None) -> str | None:
    expression = expression_text(node)
    return expression if expression.startswith(":") else None


def integer_literal(node: ast.AST | None) -> int | None:
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
    ):
        return node.value
    return None


def numeric_bounds_for(
    node: ast.AST | None,
    selectors: dict[str, SelectorBounds],
) -> tuple[int, int] | None:
    literal = integer_literal(node)
    if literal is not None:
        return (literal, literal)
    local = local_selector_name(node)
    if local is None:
        return None
    evidence = selectors.get(local)
    return (evidence.minimum, evidence.maximum) if evidence else None


def apply_selector_operation(
    operation: ast.AST,
    selectors: dict[str, SelectorBounds],
) -> None:
    """Track simple local integer ranges in a linear, branch-free block.

    This is intentionally small: it proves direct assignments, arithmetic with
    known ranges, and random-in-range selectors.  Anything else clears prior
    knowledge rather than guessing at M&B runtime values.
    """
    name = operation_name(operation)
    if not isinstance(operation, (ast.Tuple, ast.List)) or name is None or len(operation.elts) < 2:
        return
    destination = local_selector_name(operation.elts[1])
    if destination is None:
        return

    bounds: tuple[int, int] | None = None
    if name == "assign" and len(operation.elts) >= 3:
        bounds = numeric_bounds_for(operation.elts[2], selectors)
    elif name == "store_random_in_range" and len(operation.elts) >= 4:
        lower = numeric_bounds_for(operation.elts[2], selectors)
        upper = numeric_bounds_for(operation.elts[3], selectors)
        if lower and upper and lower[0] == lower[1] and upper[0] == upper[1]:
            # M&B random ranges use an exclusive upper bound.
            if lower[0] < upper[0]:
                bounds = (lower[0], upper[0] - 1)
    elif name in {"store_add", "store_sub"} and len(operation.elts) >= 4:
        left = numeric_bounds_for(operation.elts[2], selectors)
        right = numeric_bounds_for(operation.elts[3], selectors)
        if left and right:
            if name == "store_add":
                bounds = (left[0] + right[0], left[1] + right[1])
            else:
                bounds = (left[0] - right[1], left[1] - right[0])
    elif name in {"val_add", "val_sub"} and len(operation.elts) >= 3:
        prior = selectors.get(destination)
        delta = numeric_bounds_for(operation.elts[2], selectors)
        if prior and delta and delta[0] == delta[1]:
            if name == "val_add":
                bounds = (prior.minimum + delta[0], prior.maximum + delta[0])
            else:
                bounds = (prior.minimum - delta[0], prior.maximum - delta[0])
    elif name.startswith(("store_", "val_")):
        # It writes a numeric destination we do not model.
        selectors.pop(destination, None)
        return
    else:
        return

    if bounds is None:
        selectors.pop(destination, None)
    else:
        selectors[destination] = SelectorBounds(
            minimum=bounds[0],
            maximum=bounds[1],
            compile_line=operation.lineno,
            operation=name,
        )


def writer_contract_issues(
    operation: str,
    source_register: str | None,
    source_expression: str | None,
    source_selector_kind: str | None,
    source_selector_bounds: tuple[int, int] | None = None,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if operation == "str_store_string" and source_register is not None:
        issues.append(
            {
                "code": "STR_STORE_STRING_REGISTER_COPY",
                "severity": "error",
                "message": (
                    "str_store_string expects a string id or quick string. "
                    "Use str_store_string_reg to copy an s-register."
                ),
            }
        )
    if operation == "str_store_string_reg" and source_register is None:
        if source_selector_kind == "indirect_bounded" and source_selector_bounds is not None:
            lower, upper = source_selector_bounds
            if lower < 0 or upper > ENGINE_STRING_REGISTER_MAX:
                issues.append(
                    {
                        "code": "DYNAMIC_STRING_REGISTER_SELECTOR_OUT_OF_RANGE",
                        "severity": "error",
                        "message": (
                            "str_store_string_reg uses the runtime selector "
                            f"'{source_expression or '<missing>'}', bounded to s{lower}-s{upper}; "
                            f"the engine only supports s0-s{ENGINE_STRING_REGISTER_MAX}."
                        ),
                    }
                )
            else:
                issues.append(
                    {
                        "code": "DYNAMIC_STRING_REGISTER_SOURCE_BOUNDED",
                        "severity": "info",
                        "message": (
                            "str_store_string_reg uses the runtime selector "
                            f"'{source_expression or '<missing>'}', lexically bounded to s{lower}-s{upper}."
                        ),
                    }
                )
        elif source_selector_kind == "indirect":
            issues.append(
                {
                    "code": "DYNAMIC_STRING_REGISTER_SOURCE_NOT_PROVEN",
                    "severity": "warning",
                    "message": (
                        "str_store_string_reg uses the runtime selector "
                        f"'{source_expression or '<missing>'}'; static analysis cannot prove that it resolves to s0-s127."
                    ),
                }
            )
        else:
            issues.append(
                {
                    "code": "STR_STORE_STRING_REG_SOURCE",
                    "severity": "error",
                    "message": (
                        "str_store_string_reg must resolve to an s-register, not "
                        f"'{source_expression or '<missing>'}'."
                    ),
                }
            )
    return issues


def writer_payload(writer: Writer | None) -> dict[str, Any] | None:
    if writer is None:
        return None
    return {
        "register": writer.register,
        "register_band": register_band(writer.register),
        "operation": writer.operation,
        "compile_path": writer.module_path,
        "compile_line": writer.compile_line,
        "source": source_payload(writer.source),
        "source_expression": writer.source_expression,
        "source_kind": writer.source_kind,
        "source_export": writer.source_export,
        "source_register": writer.source_register,
        "source_selector_bounds": list(writer.source_selector_bounds) if writer.source_selector_bounds else None,
        "input_writer": writer.input_writer,
        "input_status": writer.input_status,
        "via_script": writer.via_script,
        "via_script_source": source_payload(writer.via_script_source),
        "issues": writer.issues,
    }


def add_writer_finding(
    context: AnalyzerContext,
    module: ModuleData,
    operation: ast.AST,
    writer: Writer,
    issue: dict[str, str],
) -> None:
    key = (module.relative_path, writer.compile_line, writer.register, issue["code"])
    if key in context.writer_finding_keys:
        return
    context.writer_finding_keys.add(key)
    context.writer_findings.append(
        {
            "id": f"writer:{module.relative_path}:{writer.compile_line}:{writer.register}:{issue['code']}",
            "severity": issue["severity"],
            "code": issue["code"],
            "message": issue["message"],
            "register": writer.register,
            "operation": writer.operation,
            "compile_path": module.relative_path,
            "compile_line": writer.compile_line,
            "source": source_payload(writer.source),
            "writer": writer_payload(writer),
        }
    )


def make_writer(
    context: AnalyzerContext,
    module: ModuleData,
    operation: ast.AST,
    ordinal: int,
    state: dict[str, Writer],
    selectors: dict[str, SelectorBounds],
    *,
    record_findings: bool,
) -> Writer | None:
    name = operation_name(operation)
    if not isinstance(operation, (ast.Tuple, ast.List)) or name is None or not is_string_writer(name):
        return None
    register = writer_register_from_operation(operation)
    if register is None:
        return None
    source_node = operation.elts[2] if len(operation.elts) >= 3 else None
    is_register_copy = name == "str_store_string_reg"
    source = (
        text_value(
            source_node,
            context.export_index,
            allow_numeric_register=is_register_copy,
        )
        if source_node is not None
        else None
    )
    source_register = string_register(
        source_node,
        allow_numeric=is_register_copy,
    )
    source_expression = source["expression"] if source else None
    source_selector = register_selector_kind(source_node) if is_register_copy else None
    source_selector_bounds: tuple[int, int] | None = None
    if source_selector == "indirect":
        selector_name = local_selector_name(source_node)
        evidence = selectors.get(selector_name) if selector_name else None
        if evidence is not None:
            source_selector = "indirect_bounded"
            source_selector_bounds = (evidence.minimum, evidence.maximum)
    issues = writer_contract_issues(
        name,
        source_register,
        source_expression,
        source_selector,
        source_selector_bounds,
    )
    if register_number(register) > ENGINE_STRING_REGISTER_MAX:
        issues.append(
            {
                "code": "UNSUPPORTED_STRING_REGISTER",
                "severity": "error",
                "message": (
                    f"{register} is outside the M&B 1.011 engine range "
                    f"s0-s{ENGINE_STRING_REGISTER_MAX}."
                ),
            }
        )
    if source_register and register_number(source_register) > ENGINE_STRING_REGISTER_MAX:
        issues.append(
            {
                "code": "UNSUPPORTED_STRING_REGISTER_SOURCE",
                "severity": "error",
                "message": (
                    f"{name} reads {source_register}, outside the M&B 1.011 engine range "
                    f"s0-s{ENGINE_STRING_REGISTER_MAX}."
                ),
            }
        )

    input_writer = writer_payload(state.get(source_register)) if source_register else None
    input_status: str | None = None
    if source_register:
        input_status = "resolved_in_same_block" if input_writer else "external_or_prior_state"

    writer = Writer(
        register=register,
        operation=name,
        module_path=module.relative_path,
        compile_line=operation.lineno,
        ordinal=ordinal,
        source=module.source_at(operation.lineno),
        source_expression=source_expression,
        source_kind=(
            "dynamic_register_selector_bounded"
            if source_selector == "indirect_bounded"
            else "dynamic_register_selector"
            if source_selector == "indirect"
            else source["kind"] if source else None
        ),
        source_export=source["resolved_export"] if source else None,
        source_register=source_register,
        source_selector_bounds=source_selector_bounds,
        input_writer=input_writer,
        input_status=input_status,
        issues=issues,
    )
    if record_findings:
        for issue in issues:
            add_writer_finding(context, module, operation, writer, issue)
    return writer


def local_function_definitions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    """Return top-level helpers without importing generated module Python.

    A few generated scripts are assembled by pure local builder functions, for
    example ``("sod_get_center_modifier", _build_get_center_modifier_ops())``.
    Importing the generated module to expand those functions would execute
    authored build-time code, so the integrity checker instead walks the
    builder's AST conservatively.
    """
    return {
        statement.name: statement
        for statement in tree.body
        if isinstance(statement, ast.FunctionDef)
    }


def operation_nodes_in_builder(builder: ast.FunctionDef) -> Iterable[ast.AST]:
    """Yield engine operation literals from one builder without entering nested code."""
    pending: list[ast.AST] = list(reversed(builder.body))
    while pending:
        node = pending.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(node, (ast.Tuple, ast.List)) and operation_name(node) is not None:
            yield node
        pending.extend(reversed(list(ast.iter_child_nodes(node))))


def script_effect_nodes(
    operations: ast.AST,
    function_definitions: dict[str, ast.FunctionDef],
) -> Iterable[ast.AST] | None:
    """Resolve literal script operations or a zero-argument local builder.

    ``module_scripts.py`` occasionally contains a call expression in the
    generated ``scripts`` list.  It is still a real exported script, not a
    missing runtime symbol.  Resolve only zero-argument local functions and
    remain conservative for every other expression.
    """
    if isinstance(operations, ast.List):
        return (
            candidate
            for candidate in ast.walk(operations)
            if isinstance(candidate, (ast.Tuple, ast.List)) and operation_name(candidate) is not None
        )
    if (
        isinstance(operations, ast.Call)
        and isinstance(operations.func, ast.Name)
        and not operations.args
        and not operations.keywords
    ):
        builder = function_definitions.get(operations.func.id)
        if builder is not None:
            return operation_nodes_in_builder(builder)
    return None


def script_effects_from_module(module: ModuleData) -> dict[str, ScriptEffect]:
    scripts = find_assignment_list(module.tree, "scripts")
    if scripts is None:
        return {}
    function_definitions = local_function_definitions(module.tree)
    effects: dict[str, ScriptEffect] = {}
    for entry in scripts.elts:
        if not isinstance(entry, ast.Tuple) or len(entry.elts) < 2:
            continue
        script_id = entry.elts[0].value if isinstance(entry.elts[0], ast.Constant) and isinstance(entry.elts[0].value, str) else None
        operations = entry.elts[1]
        if not script_id:
            continue
        direct_writes: set[str] = set()
        called_symbols: set[str] = set()
        unresolved_calls: set[str] = set()
        effect_nodes = script_effect_nodes(operations, function_definitions)
        if effect_nodes is None:
            # Preserve the previous conservative behaviour for arbitrary
            # generated expressions that cannot be inspected safely.
            unresolved_calls.add(f"<opaque script builder: {expression_text(operations)}>")
            effect_nodes = ()
        for candidate in effect_nodes:
            register = writer_register_from_operation(candidate)
            if register is not None:
                direct_writes.add(register)
            if operation_name(candidate) == "call_script":
                symbol = call_script_symbol(candidate)
                if symbol is None:
                    unresolved_calls.add(expression_text(candidate.elts[1]) if len(candidate.elts) > 1 else "<missing>")
                else:
                    called_symbols.add(symbol)
        symbol = f"script_{script_id}"
        effects[symbol] = ScriptEffect(
            symbol=symbol,
            source=module.source_at(entry.lineno),
            direct_writes=direct_writes,
            called_symbols=called_symbols,
            unresolved_calls=unresolved_calls,
        )

    for effect in effects.values():
        effect.transitive_writes = set(effect.direct_writes)
        effect.transitive_unknown = bool(effect.unresolved_calls)
    for _ in range(max(1, len(effects))):
        changed = False
        for effect in effects.values():
            writes = set(effect.direct_writes)
            unknown = bool(effect.unresolved_calls)
            for symbol in effect.called_symbols:
                callee = effects.get(symbol)
                if callee is None:
                    unknown = True
                    continue
                writes.update(callee.transitive_writes)
                unknown = unknown or callee.transitive_unknown
            if writes != effect.transitive_writes or unknown != effect.transitive_unknown:
                effect.transitive_writes = writes
                effect.transitive_unknown = unknown
                changed = True
        if not changed:
            break
    return effects


def control_flow_present(operations: Sequence[ast.AST]) -> bool:
    return any(
        (name := operation_name(operation)) is not None
        and (name in {"try_begin", "else_try", "try_end"} or name.startswith("try_for_"))
        for operation in operations
    )


def apply_script_effect(
    context: AnalyzerContext,
    module: ModuleData,
    operation: ast.AST,
    ordinal: int,
    state: dict[str, Writer],
    unknown_calls: list[CallBarrier],
) -> None:
    symbol = call_script_symbol(operation)
    effect = context.script_effects.get(symbol) if symbol else None
    if effect is None:
        unknown_calls.append(
            CallBarrier(
                ordinal=ordinal,
                compile_line=operation.lineno,
                script_symbol=symbol,
                source=module.source_at(operation.lineno),
            )
        )
        return
    for register in sorted(effect.transitive_writes, key=register_number):
        state[register] = Writer(
            register=register,
            operation="call_script",
            module_path=module.relative_path,
            compile_line=operation.lineno,
            ordinal=ordinal,
            source=module.source_at(operation.lineno),
            source_expression=symbol,
            source_kind="script_result",
            source_export=None,
            source_register=None,
            source_selector_bounds=None,
            input_writer=None,
            input_status=None,
            via_script=symbol,
            via_script_source=effect.source,
        )
    if effect.transitive_unknown:
        unknown_calls.append(
            CallBarrier(
                ordinal=ordinal,
                compile_line=operation.lineno,
                script_symbol=symbol,
                source=module.source_at(operation.lineno),
            )
        )


def analyze_block(context: AnalyzerContext, module: ModuleData, block: ast.List) -> BlockFlow:
    cached = context.block_flows.get(id(block))
    if cached is not None:
        return cached

    operations = [item for item in block.elts if operation_name(item) is not None]
    state: dict[str, Writer] = {}
    selectors: dict[str, SelectorBounds] = {}
    unknown_calls: list[CallBarrier] = []
    sink_events: list[SinkEvent] = []
    has_control_flow = control_flow_present(operations)

    for ordinal, operation in enumerate(operations):
        name = operation_name(operation)
        if isinstance(operation, (ast.Tuple, ast.List)) and name in TEXT_SINK_ARGUMENTS:
            for argument_index in TEXT_SINK_ARGUMENTS[name]:
                if len(operation.elts) > argument_index:
                    sink_events.append(
                        SinkEvent(
                            operation=operation,
                            operation_name=name,
                            argument_index=argument_index,
                            ordinal=ordinal,
                            state=dict(state),
                            unknown_calls=tuple(unknown_calls),
                            control_flow=has_control_flow,
                            block_line=block.lineno,
                        )
                    )
        writer = make_writer(
            context,
            module,
            operation,
            ordinal,
            state,
            selectors,
            record_findings=True,
        )
        if writer is not None:
            state[writer.register] = writer
        if name == "call_script":
            apply_script_effect(context, module, operation, ordinal, state, unknown_calls)
        if not has_control_flow:
            apply_selector_operation(operation, selectors)

    flow = BlockFlow(
        final_state=dict(state),
        unknown_calls=tuple(unknown_calls),
        control_flow=has_control_flow,
        sink_events=sink_events,
    )
    context.block_flows[id(block)] = flow
    return flow


def issue(code: str, severity: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


def highest_severity(issues: Iterable[dict[str, Any]]) -> str:
    result = "clean"
    for item in issues:
        severity = item.get("severity", "clean")
        if SEVERITY_RANK.get(severity, 0) > SEVERITY_RANK[result]:
            result = severity
    return result


def assess_register(
    register: str,
    state: dict[str, Writer],
    unknown_calls: Sequence[CallBarrier],
    sink_ordinal: int,
    control_flow: bool,
) -> dict[str, Any]:
    number = register_number(register)
    writer = state.get(register)
    issues: list[dict[str, str]] = []
    barriers = [
        barrier
        for barrier in unknown_calls
        if writer is not None and barrier.ordinal > writer.ordinal and barrier.ordinal < sink_ordinal
    ]

    if number > ENGINE_STRING_REGISTER_MAX:
        issues.append(
            issue(
                "UNSUPPORTED_STRING_REGISTER",
                "error",
                (
                    f"{register} is outside the M&B 1.011 engine range "
                    f"s0-s{ENGINE_STRING_REGISTER_MAX}."
                ),
            )
        )
    if writer is None:
        issues.append(
            issue(
                "REGISTER_WRITER_NOT_PROVEN",
                "info",
                "No writer was found in this lexical operation block; the value depends on prior, external, or engine state.",
            )
        )
        status = "external_or_prior_state"
    else:
        has_dynamic_selector = any(
            item["code"] == "DYNAMIC_STRING_REGISTER_SOURCE_NOT_PROVEN"
            for item in writer.issues
        )
        has_bounded_selector = any(
            item["code"] == "DYNAMIC_STRING_REGISTER_SOURCE_BOUNDED"
            for item in writer.issues
        )
        status = (
            "dynamic_selector_not_proven"
            if has_dynamic_selector
            else "dynamic_selector_bounded"
            if has_bounded_selector
            else "resolved_via_script" if writer.via_script else "resolved_in_same_block"
        )
        issues.extend(writer.issues)
        if writer.operation == "str_clear":
            issues.append(
                issue(
                    "STRING_REGISTER_CLEARED_BEFORE_SINK",
                    "warning",
                    f"{register} was cleared by the last known lexical writer before this text sink.",
                )
            )
        if writer.source_register and writer.input_status == "external_or_prior_state":
            issues.append(
                issue(
                    "COPIED_SOURCE_NOT_PROVEN",
                    "info",
                    f"{writer.operation} copied {writer.source_register}, whose writer is not proven in the same block.",
                )
            )
        if barriers:
            severity = "warning" if number <= 67 else "info"
            issues.append(
                issue(
                    "UNKNOWN_SCRIPT_MAY_CLOBBER_REGISTER",
                    severity,
                    f"An unresolved script effect runs after {register}'s last known writer and before this sink.",
                )
            )

    confidence = "high"
    if writer is None or barriers:
        confidence = "low"
    elif any(
        item["code"] == "DYNAMIC_STRING_REGISTER_SOURCE_NOT_PROVEN"
        for item in writer.issues
    ):
        confidence = "low"
    elif any(
        item["code"] == "DYNAMIC_STRING_REGISTER_SOURCE_BOUNDED"
        for item in writer.issues
    ):
        confidence = "medium"
    elif control_flow:
        confidence = "medium"
    return {
        "register": register,
        "register_band": register_band(register),
        "status": status,
        "confidence": confidence,
        "last_known_writer": writer_payload(writer),
        "unknown_call_barriers": [
            {
                "compile_line": barrier.compile_line,
                "script_symbol": barrier.script_symbol,
                "source": source_payload(barrier.source),
            }
            for barrier in barriers
        ],
        "issues": issues,
    }


def category_for_operation(module: ModuleData, operation: str) -> str:
    if operation in {"display_message", "dialog_box", "tutorial_box"}:
        return "message"
    if "presentations" in module.relative_path or operation.startswith(("create_", "overlay_")):
        return "presentation"
    return "message"


def make_sink(
    context: AnalyzerContext,
    module: ModuleData,
    *,
    kind: str,
    category: str,
    text_node: ast.AST,
    compile_line: int,
    column: int,
    source: SourceLocation | None,
    state: dict[str, Writer],
    unknown_calls: Sequence[CallBarrier],
    sink_ordinal: int,
    control_flow: bool,
    analysis_scope: str,
    context_label: str,
    argument_index: int | None = None,
) -> dict[str, Any]:
    text = text_value(text_node, context.export_index)
    assessments = [
        assess_register(
            register,
            state,
            unknown_calls,
            sink_ordinal,
            control_flow,
        )
        for register in text["registers"]
    ]
    issues = [item for assessment in assessments for item in assessment["issues"]]
    placeholder_issues = [
        issue(
            "STRING_REGISTER_PLACEHOLDER_NOT_RENDERABLE",
            "error",
            (
                f"{{{register}}} cannot be rendered by the M&B 1.011 formatter; "
                f"placeholders support s0-s{FORMATTER_STRING_REGISTER_MAX}."
            ),
        )
        for register in text["registers"]
        if register_number(register) > FORMATTER_STRING_REGISTER_MAX
    ]
    issues.extend(placeholder_issues)
    status = highest_severity(issues)
    return {
        "id": f"sink:{module.relative_path}:{compile_line}:{column}:{kind}:{argument_index if argument_index is not None else 0}",
        "kind": kind,
        "category": category,
        "compile_path": module.relative_path,
        "compile_line": compile_line,
        "compile_column": column,
        "source": source_payload(source),
        "context": context_label,
        "text_input": text,
        "register_assessments": assessments,
        "sink_issues": placeholder_issues,
        "status": status,
        "analysis_scope": analysis_scope,
        "control_flow_present": control_flow,
    }


def empty_flow() -> BlockFlow:
    return BlockFlow(final_state={}, unknown_calls=(), control_flow=False, sink_events=[])


def flow_for_node(
    context: AnalyzerContext,
    module: ModuleData,
    node: ast.AST | None,
) -> BlockFlow:
    if isinstance(node, ast.List):
        return analyze_block(context, module, node)
    return empty_flow()


def flow_end_ordinal(flow: BlockFlow) -> int:
    values = [writer.ordinal for writer in flow.final_state.values()]
    values.extend(barrier.ordinal for barrier in flow.unknown_calls)
    return (max(values) + 1) if values else 0


def shifted_flow_state(
    flow: BlockFlow,
    offset: int,
) -> tuple[dict[str, Writer], tuple[CallBarrier, ...]]:
    state = {
        register: replace(writer, ordinal=writer.ordinal + offset)
        for register, writer in flow.final_state.items()
    }
    barriers = tuple(
        replace(barrier, ordinal=barrier.ordinal + offset)
        for barrier in flow.unknown_calls
    )
    return state, barriers


def generic_operation_sinks(
    context: AnalyzerContext,
    modules: Sequence[ModuleData],
) -> list[dict[str, Any]]:
    sinks: list[dict[str, Any]] = []
    for module in modules:
        for block in operation_lists(module.tree):
            flow = analyze_block(context, module, block)
            for event in flow.sink_events:
                text_node = event.operation.elts[event.argument_index]
                sinks.append(
                    make_sink(
                        context,
                        module,
                        kind=f"operation_{event.operation_name}",
                        category=category_for_operation(module, event.operation_name),
                        text_node=text_node,
                        compile_line=event.operation.lineno,
                        column=event.operation.col_offset,
                        source=module.source_at(event.operation.lineno),
                        state=event.state,
                        unknown_calls=event.unknown_calls,
                        sink_ordinal=event.ordinal,
                        control_flow=event.control_flow,
                        analysis_scope=f"operation block beginning at compile line {event.block_line}",
                        context_label=f"{event.operation_name} argument {event.argument_index}",
                        argument_index=event.argument_index,
                    )
                )
    return sinks


def dialogue_text_sinks(
    context: AnalyzerContext,
    module: ModuleData,
) -> list[dict[str, Any]]:
    dialogs = find_assignment_list(module.tree, "dialogs")
    if dialogs is None:
        return []
    sinks: list[dict[str, Any]] = []
    for entry in dialogs.elts:
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 6:
            continue
        conditions = entry.elts[2]
        flow = flow_for_node(context, module, conditions)
        speaker = expression_text(entry.elts[0])
        start_state = expression_text(entry.elts[1])
        end_state = expression_text(entry.elts[4])
        sinks.append(
            make_sink(
                context,
                module,
                kind="dialogue_text",
                category="dialogue",
                text_node=entry.elts[3],
                compile_line=entry.lineno,
                column=entry.col_offset,
                source=module.source_at(entry.lineno),
                state=flow.final_state,
                unknown_calls=flow.unknown_calls,
                sink_ordinal=flow_end_ordinal(flow),
                control_flow=flow.control_flow,
                analysis_scope="dialogue condition block before text evaluation",
                context_label=f"{speaker}::{start_state}->{end_state}",
            )
        )
    return sinks


def menu_text_sinks(
    context: AnalyzerContext,
    module: ModuleData,
) -> list[dict[str, Any]]:
    menus = find_assignment_list(module.tree, "game_menus")
    if menus is None:
        return []
    sinks: list[dict[str, Any]] = []
    for menu in menus.elts:
        if not isinstance(menu, (ast.List, ast.Tuple)) or len(menu.elts) < 6:
            continue
        menu_id = expression_text(menu.elts[0])
        menu_flow = flow_for_node(context, module, menu.elts[4])
        sinks.append(
            make_sink(
                context,
                module,
                kind="menu_text",
                category="menu",
                text_node=menu.elts[2],
                compile_line=menu.lineno,
                column=menu.col_offset,
                source=module.source_at(menu.lineno),
                state=menu_flow.final_state,
                unknown_calls=menu_flow.unknown_calls,
                sink_ordinal=flow_end_ordinal(menu_flow),
                control_flow=menu_flow.control_flow,
                analysis_scope="menu operation block before menu text evaluation",
                context_label=menu_id,
            )
        )
        options = menu.elts[5]
        if not isinstance(options, ast.List):
            continue
        for option in options.elts:
            if not isinstance(option, (ast.List, ast.Tuple)) or len(option.elts) < 3:
                continue
            option_id = expression_text(option.elts[0])
            option_flow = flow_for_node(context, module, option.elts[1])
            menu_state, menu_barriers = shifted_flow_state(menu_flow, 0)
            option_state, option_barriers = shifted_flow_state(option_flow, 100000)
            menu_state.update(option_state)
            combined_barriers = tuple((*menu_barriers, *option_barriers))
            sinks.append(
                make_sink(
                    context,
                    module,
                    kind="menu_option_text",
                    category="menu",
                    text_node=option.elts[2],
                    compile_line=option.lineno,
                    column=option.col_offset,
                    source=module.source_at(option.lineno),
                    state=menu_state,
                    unknown_calls=combined_barriers,
                    sink_ordinal=200000,
                    control_flow=menu_flow.control_flow or option_flow.control_flow,
                    analysis_scope="menu operations followed by option condition block",
                    context_label=f"{menu_id}.{option_id}",
                )
            )
    return sinks


def sink_issue_findings(sinks: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for sink in sinks:
        for assessment in sink["register_assessments"]:
            for item in assessment["issues"]:
                findings.append(
                    {
                        "id": f"{sink['id']}:{assessment['register']}:{item['code']}",
                        "severity": item["severity"],
                        "code": item["code"],
                        "message": item["message"],
                        "sink_id": sink["id"],
                        "sink_kind": sink["kind"],
                        "category": sink["category"],
                        "register": assessment["register"],
                        "compile_path": sink["compile_path"],
                        "compile_line": sink["compile_line"],
                        "source": sink["source"],
                        "context": sink["context"],
                    }
                )
        for item in sink.get("sink_issues", []):
            findings.append(
                {
                    "id": f"{sink['id']}:{item['code']}",
                    "severity": item["severity"],
                    "code": item["code"],
                    "message": item["message"],
                    "sink_id": sink["id"],
                    "sink_kind": sink["kind"],
                    "category": sink["category"],
                    "register": None,
                    "compile_path": sink["compile_path"],
                    "compile_line": sink["compile_line"],
                    "source": sink["source"],
                    "context": sink["context"],
                }
            )
    return findings


def sorted_findings(findings: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        findings,
        key=lambda item: (
            -SEVERITY_RANK.get(item.get("severity", "clean"), 0),
            item.get("compile_path", ""),
            int(item.get("compile_line", 0) or 0),
            item.get("id", ""),
        ),
    )


def script_effect_summary(effects: dict[str, ScriptEffect]) -> dict[str, Any]:
    return {
        "script_count": len(effects),
        "scripts_with_direct_string_writes": sum(bool(effect.direct_writes) for effect in effects.values()),
        "scripts_with_transitive_string_writes": sum(bool(effect.transitive_writes) for effect in effects.values()),
        "scripts_with_unresolved_calls": sum(effect.transitive_unknown for effect in effects.values()),
        "distinct_string_registers_written": sorted(
            {
                register
                for effect in effects.values()
                for register in effect.transitive_writes
            },
            key=register_number,
        ),
    }


def summary_for(
    modules: Sequence[ModuleData],
    sinks: Sequence[dict[str, Any]],
    writer_findings: Sequence[dict[str, Any]],
    effects: dict[str, ScriptEffect],
) -> dict[str, Any]:
    category_counts = Counter(sink["category"] for sink in sinks)
    kind_counts = Counter(sink["kind"] for sink in sinks)
    status_counts = Counter(sink["status"] for sink in sinks)
    register_bands = Counter()
    assessment_issues = Counter()
    register_reference_count = 0
    source_mapped_sink_count = 0
    for sink in sinks:
        if sink["source"] is not None:
            source_mapped_sink_count += 1
        for assessment in sink["register_assessments"]:
            register_reference_count += 1
            register_bands[assessment["register_band"]] += 1
            for item in assessment["issues"]:
                assessment_issues[item["code"]] += 1
        for item in sink.get("sink_issues", []):
            assessment_issues[item["code"]] += 1
    writer_codes = Counter(item["code"] for item in writer_findings)
    return {
        "module_count": len(modules),
        "module_source_marker_count": sum(len(module.markers) for module in modules),
        "text_sink_count": len(sinks),
        "source_mapped_sink_count": source_mapped_sink_count,
        "sink_count_by_category": dict(sorted(category_counts.items())),
        "sink_count_by_kind": dict(sorted(kind_counts.items())),
        "sink_status_count": dict(sorted(status_counts.items())),
        "string_register_reference_count": register_reference_count,
        "string_register_reference_count_by_band": dict(sorted(register_bands.items())),
        "sink_issue_count_by_code": dict(sorted(assessment_issues.items())),
        "writer_contract_finding_count": len(writer_findings),
        "writer_contract_finding_count_by_code": dict(sorted(writer_codes.items())),
        "script_effects": script_effect_summary(effects),
    }


def build_integrity_report(root: Path = DEFAULT_REPO_ROOT) -> dict[str, Any]:
    root = root.resolve()
    if not (root / "compile").is_dir() or not (root / "src").is_dir():
        raise StringIntegrityError(f"Not a recognizable SoD Modern module workspace: {root}")

    modules, module_errors = load_modules(root)
    module_by_path = {module.relative_path: module for module in modules}
    script_module = module_by_path.get("compile/module_scripts.py")
    effects = script_effects_from_module(script_module) if script_module else {}
    context = AnalyzerContext(
        root=root,
        export_index=load_export_string_index(root),
        script_effects=effects,
    )

    sinks = generic_operation_sinks(context, modules)
    dialogue_module = module_by_path.get("compile/module_dialogs.py")
    if dialogue_module:
        sinks.extend(dialogue_text_sinks(context, dialogue_module))
    menu_module = module_by_path.get("compile/module_game_menus.py")
    if menu_module:
        sinks.extend(menu_text_sinks(context, menu_module))

    sinks.sort(key=lambda sink: (sink["compile_path"], sink["compile_line"], sink["id"]))
    writer_findings = sorted_findings(context.writer_findings)
    sink_findings = sorted_findings(sink_issue_findings(sinks))
    warnings = [
        (
            "Static analysis follows lexical operation order and statically-known script effects. "
            "Branches, engine state, and unresolved script effects remain conservative rather than assumed correct."
        ),
        (
            "A register marked external_or_prior_state is not automatically broken; "
            "its writer is simply not provable inside the current generated operation block."
        ),
    ]
    if module_errors:
        warnings.append("One or more target generated modules could not be analyzed.")
    if any(module.markers for module in modules) is False:
        warnings.append("No generated source markers were found; source provenance is unavailable.")

    return {
        "analysis_version": f"devkit.string-integrity.v{ANALYZER_VERSION}",
        "scope": {
            "repo_root": str(root),
            "read_only": True,
            "generated_modules": [module.relative_path for module in modules],
            "excluded_actions": [
                "No source fragment was changed.",
                "No builder or legacy processor was run.",
                "No export file was rewritten.",
            ],
        },
        "summary": summary_for(modules, sinks, writer_findings, effects),
        "writer_contract_findings": writer_findings,
        "sink_findings": sink_findings,
        "sinks": sinks,
        "module_errors": module_errors,
        "warnings": warnings,
    }


def require_limit(limit: int) -> int:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 200:
        raise StringIntegrityError("limit must be an integer from 1 through 200.")
    return limit


def query_sinks(
    report: dict[str, Any],
    *,
    query: str | None = None,
    register: int | None = None,
    kind: str = "all",
    include_clean: bool = False,
    limit: int = 30,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    if kind not in VALID_KINDS:
        raise StringIntegrityError(f"kind must be one of: {', '.join(sorted(VALID_KINDS))}.")
    if query is not None and (not query.strip() or len(query) > 500):
        raise StringIntegrityError("query must be non-empty and at most 500 characters.")
    if register is not None and (isinstance(register, bool) or not 0 <= register <= 999):
        raise StringIntegrityError("register must be an integer from 0 through 999.")

    register_name = f"s{register}" if register is not None else None
    normalized_query = query.lower() if query else None
    selected: list[dict[str, Any]] = []
    for sink in report["sinks"]:
        if kind != "all" and sink["category"] != kind:
            continue
        if not include_clean and sink["status"] == "clean":
            continue
        if register_name and register_name not in sink["text_input"]["registers"]:
            continue
        if normalized_query:
            source_path = sink["source"]["path"] if sink["source"] else ""
            haystack = " ".join(
                [
                    sink["context"],
                    sink["compile_path"],
                    source_path,
                    sink["text_input"]["expression"] or "",
                    sink["text_input"]["literal_preview"] or "",
                ]
            ).lower()
            if normalized_query not in haystack:
                continue
        selected.append(sink)
    selected.sort(
        key=lambda sink: (
            -SEVERITY_RANK.get(sink["status"], 0),
            sink["compile_path"],
            sink["compile_line"],
            sink["id"],
        )
    )

    def finding_category(finding: dict[str, Any]) -> str:
        path = finding.get("compile_path", "")
        if path.endswith("module_dialogs.py"):
            return "dialogue"
        if path.endswith("module_game_menus.py"):
            return "menu"
        if path.endswith("module_presentations.py"):
            return "presentation"
        return "message"

    selected_writer_findings: list[dict[str, Any]] = []
    for finding in report["writer_contract_findings"]:
        if kind != "all" and finding_category(finding) != kind:
            continue
        if register_name and finding.get("register") != register_name:
            continue
        if normalized_query:
            source = finding.get("source") or {}
            writer = finding.get("writer") or {}
            haystack = " ".join(
                [
                    finding.get("compile_path", ""),
                    source.get("path", ""),
                    finding.get("message", ""),
                    writer.get("source_expression", "") or "",
                ]
            ).lower()
            if normalized_query not in haystack:
                continue
        selected_writer_findings.append(finding)

    return {
        "summary": report["summary"],
        "filters": {
            "query": query,
            "register": register_name,
            "kind": kind,
            "include_clean": include_clean,
        },
        "match_count": len(selected),
        "returned_count": min(len(selected), maximum),
        "truncated": len(selected) > maximum,
        "sinks": selected[:maximum],
        "writer_contract_match_count": len(selected_writer_findings),
        "writer_contract_findings": selected_writer_findings[:maximum],
        "writer_contract_truncated": len(selected_writer_findings) > maximum,
        "module_errors": report["module_errors"],
        "warnings": report["warnings"],
    }


def summary_payload(report: dict[str, Any], limit: int = 30) -> dict[str, Any]:
    maximum = require_limit(limit)
    relevant_sink_findings = [
        finding
        for finding in report["sink_findings"]
        if finding["severity"] in {"error", "warning"}
    ]
    return {
        "summary": report["summary"],
        "writer_contract_findings": report["writer_contract_findings"][:maximum],
        "writer_contract_findings_total": len(report["writer_contract_findings"]),
        "sink_findings": relevant_sink_findings[:maximum],
        "sink_findings_total": len(relevant_sink_findings),
        "module_errors": report["module_errors"],
        "warnings": report["warnings"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# SoD Modern String Integrity Summary",
        "",
        "Read-only static semantic preflight over generated M&B 1.011 modules.",
        "",
        f"- Text sinks analyzed: {summary['text_sink_count']:,}.",
        f"- String-register reads: {summary['string_register_reference_count']:,}.",
        f"- Source-mapped sinks: {summary['source_mapped_sink_count']:,}.",
        f"- Writer-contract findings: {summary['writer_contract_finding_count']:,}.",
        f"- Scripts with transitive string writes: {summary['script_effects']['scripts_with_transitive_string_writes']:,}.",
        "",
        "## Sink categories",
        "",
        "| Category | Sinks |",
        "| --- | ---: |",
    ]
    for category, count in summary["sink_count_by_category"].items():
        lines.append(f"| {category} | {count:,} |")

    lines.extend(["", "## Actionable findings", ""])
    findings = [*payload.get("writer_contract_findings", []), *payload.get("sink_findings", [])]
    if not findings:
        lines.append("- No error- or warning-level static findings in the returned window.")
    else:
        for finding in findings:
            location = f"{finding.get('compile_path', '')}:{finding.get('compile_line', '')}"
            lines.append(f"- {finding['severity']} {finding['code']} at {location}: {finding['message']}")

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
    raise StringIntegrityError("Refusing to write an integrity artifact under _export/.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only SoD Modern string/register integrity preflight.")
    subparsers = parser.add_subparsers(dest="command", required=False)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--limit", type=int, default=30)
    summary_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    summary_parser.add_argument("--output")

    sinks_parser = subparsers.add_parser("sinks")
    sinks_parser.add_argument("--query")
    sinks_parser.add_argument("--register", type=int)
    sinks_parser.add_argument("--kind", choices=tuple(sorted(VALID_KINDS)), default="all")
    sinks_parser.add_argument("--include-clean", action="store_true")
    sinks_parser.add_argument("--limit", type=int, default=30)
    sinks_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    sinks_parser.add_argument("--output")

    args = parser.parse_args(argv)
    command = args.command or "summary"
    if args.command is None:
        args.limit = 30
        args.format = "json"
        args.output = None

    try:
        report = build_integrity_report(DEFAULT_REPO_ROOT)
        if command == "summary":
            payload = summary_payload(report, args.limit)
        else:
            payload = query_sinks(
                report,
                query=args.query,
                register=args.register,
                kind=args.kind,
                include_clean=args.include_clean,
                limit=args.limit,
            )
        rendered = json.dumps(payload, indent=2, sort_keys=True) if args.format == "json" else render_markdown(payload)
        if args.output:
            path = output_path(args.output, DEFAULT_REPO_ROOT)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
        else:
            sys.stdout.write(rendered + ("" if rendered.endswith("\n") else "\n"))
    except StringIntegrityError as error:
        print(f"string_integrity: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
