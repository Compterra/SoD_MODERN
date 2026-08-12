#!/usr/bin/env python3
"""Semantic dialogue authoring for the Mount & Blade 1.011 module system.

The dialogue compiler evaluates NPC routes in source/compiled order and stops
at the first candidate whose conditions match.  A text editor cannot expose
that rule reliably, so this module treats a dialogue route as a structured
object instead of a loose collection of lines.  It parses modular
``src/dialogs`` fragments without importing them, produces deterministic
Change Router edits, and lets the existing SHA-guarded write gate remain the
only source mutation path.

Nothing here writes generated modules or exports.  ``dialogue_apply`` merely
delegates a reviewed semantic plan to ``change_router.apply_source_edits``.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.change_router import change_router
from devkit.dialogue_inspector import dialogue_inspector


COMPOSER_VERSION = "0.2.1"
MAX_QUERY_LENGTH = 500
MAX_ROUTE_TEXT_LENGTH = 30_000
MAX_LIST_OPERATION_COUNT = 1_000
MAX_CREATE_OPERATION_COUNT = 128
MAX_CREATE_SPEC_FILE_BYTES = 256_000
STATE_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SHADOW_ACKNOWLEDGEMENT = "I acknowledge that an earlier NPC route may shadow this new route."
VALID_ACTIONS = frozenset(
    {
        "replace_text",
        "set_input_state",
        "set_output_state",
        "replace_conditions",
        "insert_condition",
        "remove_condition",
        "replace_consequences",
        "insert_consequence",
        "remove_consequence",
        "bridge_menu",
        "add_route",
        "remove_route",
        "move_route",
    }
)


class DialogueComposerError(RuntimeError):
    """A semantic dialogue operation cannot be safely planned."""


@dataclass(frozen=True)
class SourceDocument:
    """Decoded source content and line offsets for exact AST slicing."""

    path: str
    raw: str
    encoding: str
    offsets: tuple[int, ...]


@dataclass(frozen=True)
class DialogueRoute:
    """One authored DIALOGS entry with source-exact field anchors."""

    id: str
    target_id: str
    path: str
    source_order: int | None
    line: int
    column: int
    index_in_fragment: int
    entry_start: int
    entry_end: int
    entry_segment: str
    speaker: str
    input_state: str
    output_state: str
    text: str
    field_spans: tuple[tuple[int, int], ...]
    speaker_segment: str
    input_segment: str
    conditions_segment: str
    text_segment: str
    output_segment: str
    consequences_segment: str
    condition_operations: tuple[str, ...]
    consequence_operations: tuple[str, ...]


@dataclass
class DialogueComposerIndex:
    """In-memory semantic dialogue index tied to a Change Router snapshot."""

    root: Path
    router: change_router.RouterIndex
    documents: dict[str, SourceDocument]
    routes: tuple[DialogueRoute, ...]
    by_id: dict[str, DialogueRoute]
    by_target: dict[str, tuple[DialogueRoute, ...]]
    compiled_by_route: dict[str, tuple[dialogue_inspector.DialogueEntry, ...]]
    inventory_warning: str | None


@dataclass(frozen=True)
class DialogueCreateSpec:
    """A normalized, deterministic request to add exactly one dialogue route."""

    anchor_route_id: str
    position: str
    speaker: str
    input_state: str
    text: str
    output_state: str
    conditions: tuple[str, ...]
    consequences: tuple[str, ...]
    allow_static_shadow: bool
    shadow_acknowledgement: str | None


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], DialogueComposerIndex]] = {}


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def line_offsets(raw: str) -> tuple[int, ...]:
    offsets = [0]
    for index, character in enumerate(raw):
        if character == "\n":
            offsets.append(index + 1)
    return tuple(offsets)


def node_bounds(node: ast.AST, offsets: Sequence[int]) -> tuple[int, int]:
    start_line = getattr(node, "lineno", None)
    end_line = getattr(node, "end_lineno", None)
    start_column = getattr(node, "col_offset", None)
    end_column = getattr(node, "end_col_offset", None)
    if not all(isinstance(value, int) for value in (start_line, end_line, start_column, end_column)):
        raise DialogueComposerError("A route is missing precise source positions; refresh the source index.")
    if start_line < 1 or end_line < start_line or start_line > len(offsets) or end_line > len(offsets):
        raise DialogueComposerError("A route has an invalid source span.")
    return offsets[start_line - 1] + start_column, offsets[end_line - 1] + end_column


def node_segment(raw: str, node: ast.AST, offsets: Sequence[int]) -> str:
    start, end = node_bounds(node, offsets)
    return raw[start:end]


def expression_text(node: ast.AST) -> str:
    try:
        return ast.unparse(node).strip()
    except Exception:
        return "<unavailable>"


def expression_symbol(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{expression_symbol(node.left)}|{expression_symbol(node.right)}"
    return expression_text(node)


def is_player_speaker(speaker: str) -> bool:
    """Return whether a symbolic M&B speaker expression includes ``plyr``.

    Dialogues commonly use ``anyone|plyr`` rather than bare ``plyr``.  Those
    are player choices: their order controls presentation, but they do not use
    the NPC first-match rule.
    """
    return any(part.strip() == "plyr" for part in speaker.split("|"))


def literal_string(node: ast.AST) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return expression_text(node)


def direct_operations(block: ast.AST) -> tuple[str, ...]:
    if not isinstance(block, ast.List):
        return ()
    result: list[str] = []
    for item in block.elts:
        # Legacy fragments may encode a valid M&B operation with ``[...]``
        # instead of ``(...)``. Preserve its guard semantics for duplicate and
        # first-match checks.
        if isinstance(item, (ast.Tuple, ast.List)) and item.elts:
            result.append(expression_symbol(item.elts[0]))
        # Zero-argument and flag-qualified operations are also valid M&B
        # conditions, e.g. ``party_can_join`` and ``neg|party_can_join``.
        # They are guards, not fallback routes.
        elif isinstance(item, (ast.Name, ast.BinOp)):
            result.append(expression_symbol(item))
    return tuple(result)


def find_dialogs_assignment(tree: ast.Module) -> ast.List | None:
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "DIALOGS" for target in statement.targets):
            continue
        if isinstance(statement.value, ast.List):
            return statement.value
        raise DialogueComposerError("DIALOGS must be assigned a list literal.")
    return None


def source_document(router: change_router.RouterIndex, relative: str) -> SourceDocument:
    fragment = router.fragments[relative]
    raw, encoding, _ = change_router.read_text_with_encoding(change_router.source_path(router, fragment))
    return SourceDocument(relative, raw, encoding, line_offsets(raw))


def parse_routes_in_document(
    router: change_router.RouterIndex,
    document: SourceDocument,
) -> list[DialogueRoute]:
    path = router.root / document.path
    try:
        tree = ast.parse(document.raw, filename=str(path))
    except SyntaxError as error:
        raise DialogueComposerError(
            f"Cannot parse {document.path} at line {error.lineno}: {error.msg}"
        ) from error
    assignment = find_dialogs_assignment(tree)
    if assignment is None:
        return []
    routes: list[DialogueRoute] = []
    fragment = router.fragments[document.path]
    for index, entry in enumerate(assignment.elts, start=1):
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 6:
            # Fragments in this module system are small but occasionally contain
            # helper values next to DIALOGS.  Do not invent an edit target for an
            # entry that does not have the engine's six field route shape.
            continue
        fields = entry.elts
        entry_start, entry_end = node_bounds(entry, document.offsets)
        field_spans = tuple(node_bounds(field, document.offsets) for field in fields[:6])
        line = getattr(entry, "lineno", 0)
        column = getattr(entry, "col_offset", 0)
        route_id = f"dialogue:{document.path}:L{line}:C{column}"
        routes.append(
            DialogueRoute(
                id=route_id,
                target_id=fragment.id,
                path=document.path,
                source_order=fragment.order_position,
                line=line,
                column=column,
                index_in_fragment=index,
                entry_start=entry_start,
                entry_end=entry_end,
                entry_segment=document.raw[entry_start:entry_end],
                speaker=expression_symbol(fields[0]),
                input_state=literal_string(fields[1]),
                output_state=literal_string(fields[4]),
                text=literal_string(fields[3]),
                field_spans=field_spans,
                speaker_segment=node_segment(document.raw, fields[0], document.offsets),
                input_segment=node_segment(document.raw, fields[1], document.offsets),
                conditions_segment=node_segment(document.raw, fields[2], document.offsets),
                text_segment=node_segment(document.raw, fields[3], document.offsets),
                output_segment=node_segment(document.raw, fields[4], document.offsets),
                consequences_segment=node_segment(document.raw, fields[5], document.offsets),
                condition_operations=direct_operations(fields[2]),
                consequence_operations=direct_operations(fields[5]),
            )
        )
    return routes


def normalized_source_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def compiled_route_map(
    root: Path,
    routes: Iterable[DialogueRoute],
) -> tuple[dict[str, tuple[dialogue_inspector.DialogueEntry, ...]], str | None]:
    """Attach compiled order where generated markers can prove a source match."""

    try:
        inventory = dialogue_inspector.load_inventory(root)
    except dialogue_inspector.InspectorError as error:
        return {}, f"Compiled dialogue order is unavailable: {error}"
    by_source: dict[str, list[dialogue_inspector.DialogueEntry]] = defaultdict(list)
    for entry in inventory.entries:
        if entry.source is not None:
            by_source[normalized_source_path(entry.source.path)].append(entry)
    mapped: dict[str, tuple[dialogue_inspector.DialogueEntry, ...]] = {}
    for route in routes:
        candidates = []
        for entry in by_source.get(route.path, []):
            source = entry.source
            if source is not None and source.line_start <= route.line <= source.line_end:
                candidates.append(entry)
        if candidates:
            mapped[route.id] = tuple(candidates)
    warning = None
    if inventory.source_is_newer:
        warning = (
            "compile/module_dialogs.py is older than modular dialogue source; "
            "compiled first-match order is stale until build_dialogs.py is run."
        )
    return mapped, warning


def build_dialogue_composer(root: Path = DEFAULT_REPO_ROOT) -> DialogueComposerIndex:
    """Build a semantic route index without executing module-system fragments."""

    root = root.resolve()
    router = change_router.build_change_router(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == router.signature:
        return cached[1]

    documents: dict[str, SourceDocument] = {}
    routes: list[DialogueRoute] = []
    dialog_paths = router.ordering.get("dialogs", [])
    # Keep unlisted fragments inspectable.  They are sorted after manifest
    # ordered fragments by Change Router, matching its ordering contract.
    if not dialog_paths:
        dialog_paths = sorted(
            (path for path, fragment in router.fragments.items() if fragment.area == "dialogs"),
            key=str.lower,
        )
    for relative in dialog_paths:
        fragment = router.fragments.get(relative)
        if fragment is None or fragment.area != "dialogs" or fragment.syntax_error is not None:
            continue
        document = source_document(router, relative)
        documents[relative] = document
        routes.extend(parse_routes_in_document(router, document))
    compiled, inventory_warning = compiled_route_map(root, routes)
    by_target: dict[str, list[DialogueRoute]] = defaultdict(list)
    for route in routes:
        by_target[route.target_id].append(route)
    index = DialogueComposerIndex(
        root=root,
        router=router,
        documents=documents,
        routes=tuple(routes),
        by_id={route.id: route for route in routes},
        by_target={target: tuple(items) for target, items in by_target.items()},
        compiled_by_route=compiled,
        inventory_warning=inventory_warning,
    )
    _CACHE[root] = (router.signature, index)
    return index


def invalidate_composer(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def compact(text: str, maximum: int = 240) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= maximum else text[: maximum - 3] + "..."


def route_payload(index: DialogueComposerIndex, route: DialogueRoute) -> dict[str, Any]:
    compiled = index.compiled_by_route.get(route.id, ())
    return {
        "route_id": route.id,
        "target_id": route.target_id,
        "source": {
            "path": route.path,
            "line": route.line,
            "column": route.column,
            "fragment_route_index": route.index_in_fragment,
            "section_order": route.source_order,
        },
        "speaker": route.speaker,
        "input_state": route.input_state,
        "output_state": route.output_state,
        "text": route.text,
        "conditions": {
            "operations": list(route.condition_operations),
            "source": compact(route.conditions_segment),
            "is_fallback": not route.condition_operations,
        },
        "consequences": {
            "operations": list(route.consequence_operations),
            "source": compact(route.consequences_segment),
        },
        "compiled_order": [
            {
                "entry_index": entry.index,
                "compile_line": entry.compile_line,
                "is_player": entry.is_player,
                "is_fallback": entry.is_fallback,
            }
            for entry in compiled
        ],
    }


def route_sort_key(route: DialogueRoute) -> tuple[int, int, int, str]:
    return (
        route.source_order if route.source_order is not None else 1_000_000,
        route.line,
        route.column,
        route.id,
    )


def route_shadow_analysis(index: DialogueComposerIndex, route: DialogueRoute) -> dict[str, Any]:
    """Return static first-match hazards, never a claim of runtime reachability."""

    related = sorted(
        (
            candidate
            for candidate in index.routes
            if candidate.id != route.id
            and candidate.speaker == route.speaker
            and candidate.input_state == route.input_state
        ),
        key=route_sort_key,
    )
    ordered = sorted([route, *related], key=route_sort_key)
    position = ordered.index(route)
    preceding = ordered[:position]
    exact_conditions = [
        candidate
        for candidate in preceding
        if candidate.conditions_segment.strip() == route.conditions_segment.strip()
    ]
    prior_fallbacks = [candidate for candidate in preceding if not candidate.condition_operations]
    warnings: list[dict[str, Any]] = []
    player_choice = is_player_speaker(route.speaker)
    if not player_choice and exact_conditions:
        warnings.append(
            {
                "severity": "high",
                "code": "EXACT_PRECEDING_CONDITION",
                "message": "An earlier NPC candidate has the same speaker, input state, and condition block.",
                "route_ids": [candidate.id for candidate in exact_conditions],
            }
        )
    if prior_fallbacks and not player_choice:
        warnings.append(
            {
                "severity": "high",
                "code": "PRECEDING_NPC_FALLBACK",
                "message": "A no-condition NPC route precedes this candidate and can consume the state first.",
                "route_ids": [candidate.id for candidate in prior_fallbacks],
            }
        )
    if player_choice:
        warnings.append(
            {
                "severity": "info",
                "code": "PLAYER_CHOICE_GROUP",
                "message": "Player routes are choices; their order still affects display order but not NPC first-match selection.",
                "route_ids": [],
            }
        )
    return {
        "group": {
            "speaker": route.speaker,
            "input_state": route.input_state,
            "candidate_count": len(ordered),
            "route_position": position + 1,
        },
        "preceding_candidates": [
            {
                "route_id": candidate.id,
                "source": f"{candidate.path}:L{candidate.line}",
                "conditions": compact(candidate.conditions_segment),
                "is_fallback": not candidate.condition_operations,
            }
            for candidate in preceding[-20:]
        ],
        "warnings": warnings,
        "static_only": True,
    }


def dialogue_summary(index: DialogueComposerIndex) -> dict[str, Any]:
    states = defaultdict(int)
    fallback_count = 0
    for route in index.routes:
        states[route.input_state] += 1
        fallback_count += int(not route.condition_operations)
    return {
        "composer_version": f"devkit.dialogue-composer.v{COMPOSER_VERSION}",
        "route_count": len(index.routes),
        "source_fragment_count": len(index.by_target),
        "input_state_count": len(states),
        "fallback_route_count": fallback_count,
        "compiled_route_mapping_count": len(index.compiled_by_route),
        "inventory_warning": index.inventory_warning,
        "warnings": [
            "Route edits preserve source fragment ownership and go through the Change Router SHA gate.",
            "NPC dialogue uses first matching route order; every patch includes static shadow analysis.",
        ],
    }


def require_query(value: str, *, name: str = "query") -> str:
    if not isinstance(value, str) or not value.strip():
        raise DialogueComposerError(f"{name} must not be empty.")
    if len(value) > MAX_QUERY_LENGTH:
        raise DialogueComposerError(f"{name} must be at most {MAX_QUERY_LENGTH} characters.")
    return value.strip()


def require_limit(value: int, *, name: str = "limit", maximum: int = 200) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise DialogueComposerError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_route(index: DialogueComposerIndex, route_id: str) -> DialogueRoute:
    if not isinstance(route_id, str) or not route_id.startswith("dialogue:"):
        raise DialogueComposerError("route_id must be a dialogue ID returned by dialogue_find.")
    route = index.by_id.get(route_id)
    if route is None:
        raise DialogueComposerError("Unknown dialogue route; refresh dialogue_find before editing.")
    return route


def dialogue_find(
    index: DialogueComposerIndex,
    *,
    query: str | None = None,
    input_state: str | None = None,
    output_state: str | None = None,
    source: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Find routes in modular source; no generated order is assumed current."""

    maximum = require_limit(limit)
    if not any(value is not None and str(value).strip() for value in (query, input_state, output_state, source)):
        raise DialogueComposerError("Specify query, input_state, output_state, or source.")
    needle = require_query(query).casefold() if query is not None else None
    input_filter = require_query(input_state, name="input_state") if input_state is not None else None
    output_filter = require_query(output_state, name="output_state") if output_state is not None else None
    source_filter = require_query(source, name="source").casefold() if source is not None else None
    matches: list[DialogueRoute] = []
    for route in index.routes:
        searchable = "\n".join(
            (
                route.speaker,
                route.input_state,
                route.output_state,
                route.text,
                route.conditions_segment,
                route.consequences_segment,
                route.path,
            )
        ).casefold()
        if needle and needle not in searchable:
            continue
        if input_filter and input_filter != route.input_state:
            continue
        if output_filter and output_filter != route.output_state:
            continue
        if source_filter and source_filter not in route.path.casefold():
            continue
        matches.append(route)
    matches.sort(key=route_sort_key)
    return {
        "summary": dialogue_summary(index),
        "match_count": len(matches),
        "returned_count": min(len(matches), maximum),
        "truncated": len(matches) > maximum,
        "routes": [route_payload(index, route) for route in matches[:maximum]],
        "warnings": [warning for warning in (index.inventory_warning,) if warning],
    }


def dialogue_context(
    index: DialogueComposerIndex,
    route_id: str,
    *,
    max_lines: int = 100,
    related_limit: int = 20,
) -> dict[str, Any]:
    route = require_route(index, route_id)
    maximum_lines = require_limit(max_lines, name="max_lines", maximum=400)
    maximum_related = require_limit(related_limit, name="related_limit", maximum=100)
    router_context = change_router.linked_context(
        index.router,
        route.target_id,
        focus_line=route.line,
        max_lines=maximum_lines,
        related_limit=maximum_related,
    )
    return {
        "route": route_payload(index, route),
        "first_match_analysis": route_shadow_analysis(index, route),
        "source_context": router_context,
        "edit_capabilities": sorted(VALID_ACTIONS),
        "warnings": [warning for warning in (index.inventory_warning,) if warning],
    }


def parse_expression(value: str, *, name: str) -> ast.AST:
    if not isinstance(value, str) or not value.strip():
        raise DialogueComposerError(f"{name} must be a non-empty Python source expression.")
    if len(value) > MAX_ROUTE_TEXT_LENGTH:
        raise DialogueComposerError(f"{name} exceeds the {MAX_ROUTE_TEXT_LENGTH:,}-character safety limit.")
    try:
        return ast.parse(value.strip(), mode="eval").body
    except SyntaxError as error:
        raise DialogueComposerError(f"{name} is not a valid Python expression: {error.msg}") from error


def validate_operation(value: str, *, name: str = "operation") -> str:
    expression = parse_expression(value, name=name)
    if not isinstance(expression, (ast.Tuple, ast.Name)):
        raise DialogueComposerError(f"{name} must be an operation tuple such as '(assign, \":x\", 1)' or a zero-argument operation name.")
    return value.strip()


def validate_operation_list(value: str, *, name: str) -> str:
    expression = parse_expression(value, name=name)
    if not isinstance(expression, ast.List):
        raise DialogueComposerError(f"{name} must be a list of operations, for example '[(assign, \":x\", 1)]'.")
    if len(expression.elts) > MAX_LIST_OPERATION_COUNT:
        raise DialogueComposerError(f"{name} contains too many operation entries.")
    for item in expression.elts:
        if not isinstance(item, (ast.Tuple, ast.Name)):
            raise DialogueComposerError(f"{name} may contain only operation tuples or zero-argument operation names.")
    return value.strip()


def validate_symbol_expression(value: str, *, name: str) -> str:
    parse_expression(value, name=name)
    return value.strip()


def is_symbolic_speaker_expression(expression: ast.AST) -> bool:
    if isinstance(expression, ast.Name):
        return True
    return (
        isinstance(expression, ast.BinOp)
        and isinstance(expression.op, ast.BitOr)
        and is_symbolic_speaker_expression(expression.left)
        and is_symbolic_speaker_expression(expression.right)
    )


def validate_speaker_expression(value: Any, *, name: str) -> str:
    if not isinstance(value, str):
        raise DialogueComposerError(f"{name} must be a symbolic M&B speaker expression such as 'anyone' or 'plyr'.")
    expression = parse_expression(value, name=name)
    if not is_symbolic_speaker_expression(expression):
        raise DialogueComposerError(
            f"{name} must contain only symbolic speaker names joined with '|'; literals and calls are not allowed."
        )
    return value.strip()


def validate_state_identifier(value: Any, *, name: str) -> str:
    if not isinstance(value, str) or not STATE_IDENTIFIER_RE.fullmatch(value):
        raise DialogueComposerError(
            f"{name} must be a non-empty M&B dialogue state identifier using letters, digits, and underscores."
        )
    return value


def validate_dialogue_text(value: Any, *, name: str) -> str:
    if not isinstance(value, str):
        raise DialogueComposerError(f"{name} must be a string.")
    if len(value) > MAX_ROUTE_TEXT_LENGTH:
        raise DialogueComposerError(f"{name} exceeds the {MAX_ROUTE_TEXT_LENGTH:,}-character safety limit.")
    if not value.startswith("@"):
        raise DialogueComposerError(
            f"{name} must start with '@' so the new route has an explicit M&B inline dialogue string."
        )
    return value


def validate_operation_sequence(value: Any, *, name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise DialogueComposerError(f"{name} must be a JSON array of M&B operation strings.")
    if len(value) > MAX_CREATE_OPERATION_COUNT:
        raise DialogueComposerError(f"{name} contains too many operations; maximum is {MAX_CREATE_OPERATION_COUNT}.")
    operations: list[str] = []
    for index, operation in enumerate(value):
        if not isinstance(operation, str):
            raise DialogueComposerError(f"{name}[{index}] must be a source operation string.")
        operations.append(validate_operation(operation, name=f"{name}[{index}]"))
    return tuple(operations)


def expression_signature(value: str, *, name: str) -> str:
    expression = parse_expression(value, name=name)
    return ast.dump(expression, annotate_fields=False, include_attributes=False)


def speaker_signature(value: str) -> str:
    return expression_signature(value, name="speaker")


def condition_signature(value: str) -> str:
    return expression_signature(value, name="conditions")


def render_operation_sequence(operations: Sequence[str], indent: str) -> str:
    if not operations:
        return "[]"
    child = indent + "  "
    return "[\n" + "\n".join(f"{child}{operation}," for operation in operations) + f"\n{indent}]"


def parse_create_spec(value: Any) -> DialogueCreateSpec:
    if not isinstance(value, dict):
        raise DialogueComposerError("spec must be a JSON object.")
    allowed = {
        "anchor_route_id",
        "position",
        "speaker",
        "input_state",
        "text",
        "output_state",
        "conditions",
        "consequences",
        "allow_static_shadow",
        "shadow_acknowledgement",
    }
    unexpected = sorted(set(value) - allowed)
    if unexpected:
        raise DialogueComposerError("spec has unsupported field(s): " + ", ".join(unexpected))
    required = ("anchor_route_id", "position", "speaker", "input_state", "text", "output_state")
    missing = [field for field in required if field not in value]
    if missing:
        raise DialogueComposerError("spec is missing: " + ", ".join(missing))
    anchor_route_id = require_query(value["anchor_route_id"], name="spec.anchor_route_id")
    position = value["position"]
    if position not in {"before", "after"}:
        raise DialogueComposerError("spec.position must be 'before' or 'after'.")
    allow_static_shadow = value.get("allow_static_shadow", False)
    if not isinstance(allow_static_shadow, bool):
        raise DialogueComposerError("spec.allow_static_shadow must be a boolean when supplied.")
    acknowledgement = value.get("shadow_acknowledgement")
    if acknowledgement is not None and not isinstance(acknowledgement, str):
        raise DialogueComposerError("spec.shadow_acknowledgement must be a string when supplied.")
    return DialogueCreateSpec(
        anchor_route_id=anchor_route_id,
        position=position,
        speaker=validate_speaker_expression(value["speaker"], name="spec.speaker"),
        input_state=validate_state_identifier(value["input_state"], name="spec.input_state"),
        text=validate_dialogue_text(value["text"], name="spec.text"),
        output_state=validate_state_identifier(value["output_state"], name="spec.output_state"),
        conditions=validate_operation_sequence(value.get("conditions", []), name="spec.conditions"),
        consequences=validate_operation_sequence(value.get("consequences", []), name="spec.consequences"),
        allow_static_shadow=allow_static_shadow,
        shadow_acknowledgement=acknowledgement,
    )


def create_spec_payload(spec: DialogueCreateSpec) -> dict[str, Any]:
    return {
        "anchor_route_id": spec.anchor_route_id,
        "position": spec.position,
        "speaker": spec.speaker,
        "input_state": spec.input_state,
        "text": spec.text,
        "output_state": spec.output_state,
        "conditions": list(spec.conditions),
        "consequences": list(spec.consequences),
        "allow_static_shadow": spec.allow_static_shadow,
        "shadow_acknowledgement_required": spec.allow_static_shadow,
    }


def quoted(value: str, *, name: str) -> str:
    if not isinstance(value, str):
        raise DialogueComposerError(f"{name} must be a string.")
    if len(value) > MAX_ROUTE_TEXT_LENGTH:
        raise DialogueComposerError(f"{name} exceeds the {MAX_ROUTE_TEXT_LENGTH:,}-character safety limit.")
    return json.dumps(value, ensure_ascii=False)


def list_item_segments(segment: str, *, name: str) -> list[str]:
    expression = parse_expression(segment, name=name)
    if not isinstance(expression, ast.List):
        raise DialogueComposerError(f"{name} is no longer an operation list; refresh the route before editing.")
    if len(expression.elts) > MAX_LIST_OPERATION_COUNT:
        raise DialogueComposerError(f"{name} contains too many operations.")
    offsets = line_offsets(segment)
    return [node_segment(segment, item, offsets) for item in expression.elts]


def rebuilt_list(items: Sequence[str]) -> str:
    """Rebuild just a condition/consequence list without touching sibling fields."""

    if not items:
        return "[]"
    return "[\n    " + ",\n    ".join(item.strip() for item in items) + ",\n]"


def append_or_prepend_list(segment: str, operation: str, position: str, *, name: str) -> str:
    items = list_item_segments(segment, name=name)
    if position == "start":
        items.insert(0, operation)
    elif position == "end":
        items.append(operation)
    else:
        raise DialogueComposerError("position must be 'start' or 'end'.")
    return rebuilt_list(items)


def remove_list_item(segment: str, operation_index: int | None, *, name: str) -> str:
    if isinstance(operation_index, bool) or not isinstance(operation_index, int) or operation_index < 0:
        raise DialogueComposerError("operation_index must be a zero-based non-negative integer.")
    items = list_item_segments(segment, name=name)
    if operation_index >= len(items):
        raise DialogueComposerError(f"operation_index={operation_index} is outside the {len(items)} operation(s) in {name}.")
    del items[operation_index]
    return rebuilt_list(items)


def occurrence_edit(raw: str, start: int, end: int, new_text: str) -> dict[str, Any]:
    if not 0 <= start < end <= len(raw):
        raise DialogueComposerError("Semantic edit range is outside its source fragment.")
    old_text = raw[start:end]
    occurrences = change_router.all_occurrences(raw, old_text)
    try:
        occurrence = occurrences.index(start) + 1
    except ValueError as error:
        raise DialogueComposerError("Could not anchor the semantic edit in its source fragment.") from error
    return {
        "old_text": old_text,
        "new_text": new_text,
        "occurrence": occurrence,
        "expected_occurrences": len(occurrences),
    }


def field_edit(document: SourceDocument, route: DialogueRoute, field: str, replacement: str) -> dict[str, Any]:
    positions = {
        "speaker": 0,
        "input_state": 1,
        "conditions": 2,
        "text": 3,
        "output_state": 4,
        "consequences": 5,
    }
    if field not in positions:
        raise DialogueComposerError(f"Unknown route field: {field}")
    start, end = route.field_spans[positions[field]]
    return occurrence_edit(document.raw, start, end, replacement)


def item_with_separator(document: SourceDocument, route: DialogueRoute) -> tuple[int, int]:
    """Return a removable list-item span including one syntactic comma when present."""

    raw = document.raw
    start = route.entry_start
    line_start = raw.rfind("\n", 0, start) + 1
    if raw[line_start:start].strip() == "":
        start = line_start
    end = route.entry_end
    cursor = end
    while cursor < len(raw) and raw[cursor] in " \t":
        cursor += 1
    if cursor < len(raw) and raw[cursor] == ",":
        end = cursor + 1
        while end < len(raw) and raw[end] in " \t":
            end += 1
        if raw.startswith("\r\n", end):
            end += 2
        elif end < len(raw) and raw[end] == "\n":
            end += 1
    return start, end


def leading_indent(raw: str, offset: int) -> str:
    start = raw.rfind("\n", 0, offset) + 1
    prefix = raw[start:offset]
    return prefix if prefix.strip() == "" else ""


def render_route(new_route: dict[str, Any], indent: str) -> str:
    if not isinstance(new_route, dict):
        raise DialogueComposerError("new_route must be an object with speaker, input_state, text, and output_state.")
    required = ("speaker", "input_state", "text", "output_state")
    missing = [field for field in required if field not in new_route]
    if missing:
        raise DialogueComposerError("new_route is missing: " + ", ".join(missing))
    speaker = validate_symbol_expression(str(new_route["speaker"]), name="new_route.speaker")
    input_state = quoted(new_route["input_state"], name="new_route.input_state")
    text = quoted(new_route["text"], name="new_route.text")
    output_state = quoted(new_route["output_state"], name="new_route.output_state")
    conditions = validate_operation_list(str(new_route.get("conditions", "[]")), name="new_route.conditions")
    consequences = validate_operation_list(str(new_route.get("consequences", "[]")), name="new_route.consequences")
    child = indent + "  "
    return "\n".join(
        (
            "[",
            f"{child}{speaker},",
            f"{child}{input_state},",
            f"{child}{conditions},",
            f"{child}{text},",
            f"{child}{output_state},",
            f"{child}{consequences},",
            f"{indent}]",
        )
    )


def render_created_route(spec: DialogueCreateSpec, indent: str) -> str:
    """Render a route only from the normalized create contract, never prose."""

    child = indent + "  "
    conditions = render_operation_sequence(spec.conditions, child)
    consequences = render_operation_sequence(spec.consequences, child)
    return "\n".join(
        (
            "[",
            f"{child}{spec.speaker},",
            f"{child}{quoted(spec.input_state, name='spec.input_state')},",
            f"{child}{conditions},",
            f"{child}{quoted(spec.text, name='spec.text')},",
            f"{child}{quoted(spec.output_state, name='spec.output_state')},",
            f"{child}{consequences},",
            f"{indent}]",
        )
    )


def precedes_created_route(candidate: DialogueRoute, anchor: DialogueRoute, position: str) -> bool:
    """Compare an existing route against an anchored insertion point."""

    if candidate.target_id == anchor.target_id:
        if position == "before":
            return candidate.entry_start < anchor.entry_start
        return candidate.entry_start <= anchor.entry_start
    return route_sort_key(candidate) < route_sort_key(anchor)


def creation_safety_analysis(
    index: DialogueComposerIndex,
    anchor: DialogueRoute,
    spec: DialogueCreateSpec,
) -> dict[str, Any]:
    requested_speaker = speaker_signature(spec.speaker)
    requested_conditions = condition_signature(render_operation_sequence(spec.conditions, ""))
    candidates = sorted(
        (
            route
            for route in index.routes
            if route.input_state == spec.input_state
            and speaker_signature(route.speaker_segment) == requested_speaker
        ),
        key=route_sort_key,
    )
    preceding = [
        route
        for route in candidates
        if precedes_created_route(route, anchor, spec.position)
    ]
    exact_duplicates = [
        route
        for route in candidates
        if condition_signature(route.conditions_segment) == requested_conditions
    ]
    exact_preceding = [
        route
        for route in preceding
        if condition_signature(route.conditions_segment) == requested_conditions
    ]
    prior_fallbacks = [route for route in preceding if not route.condition_operations]
    warnings: list[dict[str, Any]] = []
    player_choice = is_player_speaker(spec.speaker)
    if not player_choice and exact_preceding:
        warnings.append(
            {
                "severity": "high",
                "code": "EXACT_PRECEDING_CONDITION",
                "message": "An earlier candidate has the same speaker, input state, and condition block.",
                "route_ids": [route.id for route in exact_preceding],
            }
        )
    if prior_fallbacks and not player_choice:
        warnings.append(
            {
                "severity": "high",
                "code": "PRECEDING_NPC_FALLBACK",
                "message": "A no-condition NPC route precedes this insertion and can consume the state first.",
                "route_ids": [route.id for route in prior_fallbacks],
            }
        )
    if player_choice:
        warnings.append(
            {
                "severity": "info",
                "code": "PLAYER_CHOICE_GROUP",
                "message": "Player route order is deterministic display order; it is not NPC first-match selection.",
                "route_ids": [],
            }
        )
    output_consumers = [
        route.id for route in index.routes if route.input_state == spec.output_state
    ]
    if not output_consumers and spec.output_state != "close_window":
        warnings.append(
            {
                "severity": "warning",
                "code": "OUTPUT_STATE_NOT_FOUND",
                "message": "No current authored route consumes the requested output state; it may be created later or be engine-handled.",
                "route_ids": [],
            }
        )
    return {
        "static_only": True,
        "anchor_route_id": anchor.id,
        "insertion": spec.position,
        "group": {
            "speaker": spec.speaker,
            "input_state": spec.input_state,
            "existing_candidate_count": len(candidates),
            "prospective_position": len(preceding) + 1,
        },
        "duplicate_route_ids": [route.id for route in exact_duplicates],
        "preceding_candidates": [
            {
                "route_id": route.id,
                "source": f"{route.path}:L{route.line}",
                "conditions": compact(route.conditions_segment),
                "is_fallback": not route.condition_operations,
            }
            for route in preceding[-20:]
        ],
        "output_state_consumer_route_ids": output_consumers[:20],
        "output_state_consumers_truncated": len(output_consumers) > 20,
        "warnings": warnings,
    }


def require_safe_creation(spec: DialogueCreateSpec, safety: dict[str, Any]) -> None:
    duplicates = safety["duplicate_route_ids"]
    if duplicates:
        raise DialogueComposerError(
            "The requested route duplicates an existing speaker/input-state/condition signature: "
            + ", ".join(duplicates[:5])
            + ". Choose a distinct condition block or edit the existing route."
        )
    blockers = [warning for warning in safety["warnings"] if warning["severity"] == "high"]
    if not blockers:
        return
    if not spec.allow_static_shadow:
        codes = ", ".join(warning["code"] for warning in blockers)
        raise DialogueComposerError(
            "The requested NPC route has a static first-match risk ("
            + codes
            + "). Choose a safe anchor/condition, or set allow_static_shadow=true and provide the exact acknowledgement: "
            + repr(SHADOW_ACKNOWLEDGEMENT)
        )
    if spec.shadow_acknowledgement != SHADOW_ACKNOWLEDGEMENT:
        raise DialogueComposerError(
            "allow_static_shadow=true requires spec.shadow_acknowledgement exactly equal to "
            + repr(SHADOW_ACKNOWLEDGEMENT)
        )


def create_route_edits(
    index: DialogueComposerIndex,
    spec: DialogueCreateSpec,
) -> tuple[DialogueRoute, list[dict[str, Any]], dict[str, Any]]:
    anchor = require_route(index, spec.anchor_route_id)
    safety = creation_safety_analysis(index, anchor, spec)
    require_safe_creation(spec, safety)
    document = index.documents[anchor.path]
    indent = leading_indent(document.raw, anchor.entry_start)
    rendered = render_created_route(spec, indent)
    if spec.position == "after":
        replacement = anchor.entry_segment + ",\n" + indent + rendered
    else:
        replacement = rendered + ",\n" + indent + anchor.entry_segment
    return anchor, [occurrence_edit(document.raw, anchor.entry_start, anchor.entry_end, replacement)], safety


def semantic_edits(
    index: DialogueComposerIndex,
    route: DialogueRoute,
    *,
    action: str,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_route: dict[str, Any] | None = None,
    anchor_route_id: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Translate a bounded semantic action into Change Router edit anchors."""

    if action not in VALID_ACTIONS:
        raise DialogueComposerError("action must be one of: " + ", ".join(sorted(VALID_ACTIONS)))
    document = index.documents[route.path]
    metadata: dict[str, Any] = {"action": action, "route_id": route.id}
    if action == "replace_text":
        return [field_edit(document, route, "text", quoted(value, name="value"))], metadata
    if action == "set_input_state":
        return [field_edit(document, route, "input_state", quoted(value, name="value"))], metadata
    if action == "set_output_state":
        return [field_edit(document, route, "output_state", quoted(value, name="value"))], metadata
    if action == "replace_conditions":
        return [field_edit(document, route, "conditions", validate_operation_list(value or "", name="value"))], metadata
    if action == "replace_consequences":
        return [field_edit(document, route, "consequences", validate_operation_list(value or "", name="value"))], metadata
    if action in {"insert_condition", "insert_consequence"}:
        checked_operation = validate_operation(operation or "")
        field = "conditions" if action == "insert_condition" else "consequences"
        source = route.conditions_segment if field == "conditions" else route.consequences_segment
        replacement = append_or_prepend_list(source, checked_operation, position, name=field)
        return [field_edit(document, route, field, replacement)], {**metadata, "operation": checked_operation, "position": position}
    if action in {"remove_condition", "remove_consequence"}:
        field = "conditions" if action == "remove_condition" else "consequences"
        source = route.conditions_segment if field == "conditions" else route.consequences_segment
        replacement = remove_list_item(source, operation_index, name=field)
        return [field_edit(document, route, field, replacement)], {**metadata, "operation_index": operation_index}
    if action == "bridge_menu":
        menu_id = require_query(value or "", name="value")
        if not re.fullmatch(r"mnu_[A-Za-z0-9_]+", menu_id):
            raise DialogueComposerError("bridge_menu value must be a menu constant such as mnu_my_menu.")
        bridge = f'(jump_to_menu, "{menu_id}")'
        replacement = append_or_prepend_list(route.consequences_segment, bridge, position, name="consequences")
        return [field_edit(document, route, "consequences", replacement)], {**metadata, "menu_id": menu_id, "position": position}
    if action == "add_route":
        anchor = require_route(index, anchor_route_id or route.id)
        if anchor.target_id != route.target_id:
            raise DialogueComposerError("add_route anchor_route_id must refer to the same source fragment.")
        placement = position
        if placement not in {"before", "after"}:
            raise DialogueComposerError("add_route position must be 'before' or 'after'.")
        indent = leading_indent(document.raw, anchor.entry_start)
        rendered = render_route(new_route or {}, indent)
        if placement == "after":
            replacement = anchor.entry_segment + ",\n" + indent + rendered
        else:
            replacement = rendered + ",\n" + indent + anchor.entry_segment
        return [occurrence_edit(document.raw, anchor.entry_start, anchor.entry_end, replacement)], {
            **metadata,
            "anchor_route_id": anchor.id,
            "position": placement,
        }
    if action == "remove_route":
        start, end = item_with_separator(document, route)
        return [occurrence_edit(document.raw, start, end, "")], metadata
    if action == "move_route":
        anchor = require_route(index, anchor_route_id or "")
        if anchor.id == route.id:
            raise DialogueComposerError("move_route anchor_route_id must be a different route.")
        if anchor.target_id != route.target_id:
            raise DialogueComposerError("move_route can only reorder routes within one source fragment.")
        if position not in {"before", "after"}:
            raise DialogueComposerError("move_route position must be 'before' or 'after'.")
        remove_start, remove_end = item_with_separator(document, route)
        indent = leading_indent(document.raw, anchor.entry_start)
        if position == "after":
            insertion = anchor.entry_segment + ",\n" + indent + route.entry_segment
        else:
            insertion = route.entry_segment + ",\n" + indent + anchor.entry_segment
        return [
            occurrence_edit(document.raw, remove_start, remove_end, ""),
            occurrence_edit(document.raw, anchor.entry_start, anchor.entry_end, insertion),
        ], {**metadata, "anchor_route_id": anchor.id, "position": position}
    raise DialogueComposerError(f"Unhandled dialogue action: {action}")


def dialogue_patch(
    index: DialogueComposerIndex,
    route_id: str,
    *,
    action: str,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_route: dict[str, Any] | None = None,
    anchor_route_id: str | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    route = require_route(index, route_id)
    edits, semantic = semantic_edits(
        index,
        route,
        action=action,
        value=value,
        operation=operation,
        position=position,
        operation_index=operation_index,
        new_route=new_route,
        anchor_route_id=anchor_route_id,
    )
    plan = change_router.patch_plan(
        index.router,
        route.target_id,
        edits,
        expected_sha256=expected_sha256,
    )
    return {
        "semantic_operation": semantic,
        "route": route_payload(index, route),
        "first_match_analysis": route_shadow_analysis(index, route),
        "change_router_plan": plan,
        "apply_contract": {
            "tool": "dialogue_apply",
            "route_id": route.id,
            "action": action,
            "required_expected_sha256": plan["target"]["base_sha256"],
            "dry_run_default": True,
            "guarantees": plan["apply_contract"]["guarantees"],
        },
        "warnings": [
            *([index.inventory_warning] if index.inventory_warning else []),
            "Review the static first-match analysis and unified diff before a non-dry-run apply.",
        ],
    }


def dialogue_create_plan(
    index: DialogueComposerIndex,
    spec_value: Any,
    *,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Plan one canonical new route with deterministic placement and safety rules."""

    spec = parse_create_spec(spec_value)
    anchor, edits, safety = create_route_edits(index, spec)
    plan = change_router.patch_plan(
        index.router,
        anchor.target_id,
        edits,
        expected_sha256=expected_sha256,
    )
    return {
        "creator_version": f"devkit.dialogue-composer.v{COMPOSER_VERSION}",
        "creation_spec": create_spec_payload(spec),
        "anchor_route": route_payload(index, anchor),
        "prospective_route": {
            "source_path": anchor.path,
            "insertion": spec.position,
            "speaker": spec.speaker,
            "input_state": spec.input_state,
            "text": spec.text,
            "output_state": spec.output_state,
            "conditions": list(spec.conditions),
            "consequences": list(spec.consequences),
        },
        "static_creation_safety": safety,
        "change_router_plan": plan,
        "apply_contract": {
            "tool": "dialogue_create_apply",
            "required_expected_sha256": plan["target"]["base_sha256"],
            "required_expected_plan_id": plan["plan_id"],
            "dry_run_default": True,
            "guarantees": [
                "The route is rendered only from the structured creation spec.",
                "The anchor fixes the exact source fragment and before/after placement.",
                "The source SHA and plan ID must both still match when apply is requested.",
                "Only modular source may be written; compile/ and _export/ are never written here.",
            ],
        },
        "warnings": [
            *([index.inventory_warning] if index.inventory_warning else []),
            *(
                [
                    "Static first-match acknowledgement was explicitly supplied; review the listed NPC shadow risk before apply."
                ]
                if spec.allow_static_shadow
                else []
            ),
            "Review the exact unified diff before a non-dry-run apply.",
        ],
    }


def dialogue_create_apply(
    index: DialogueComposerIndex,
    spec_value: Any,
    *,
    expected_sha256: str,
    expected_plan_id: str,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Rehearse or apply one exact previously reviewed creation plan."""

    spec = parse_create_spec(spec_value)
    anchor, edits, safety = create_route_edits(index, spec)
    current_plan = change_router.patch_plan(
        index.router,
        anchor.target_id,
        edits,
        expected_sha256=expected_sha256,
    )
    if not isinstance(expected_plan_id, str) or current_plan["plan_id"] != expected_plan_id:
        raise DialogueComposerError(
            "expected_plan_id does not match the current deterministic creation plan; refresh dialogue_create_plan and review its diff."
        )
    result = change_router.apply_source_edits(
        index.router,
        anchor.target_id,
        edits,
        expected_sha256=expected_sha256,
        dry_run=dry_run,
    )
    if not dry_run:
        invalidate_composer(index.root)
    return {
        "creation_spec": create_spec_payload(spec),
        "anchor_route_id": anchor.id,
        "static_creation_safety": safety,
        "result": result,
        "follow_up": {
            "find_tool": "dialogue_find",
            "find_input_state": spec.input_state,
            "verify_tool": "dialogue_verify",
            "note": "After a non-dry apply, find the newly assigned stable route ID, verify it, then run the reviewed module build before testing in-game.",
        },
        "warnings": [
            *result["warnings"],
            "Generated dialogue and exports were not changed by this tool.",
        ],
    }


def dialogue_apply(
    index: DialogueComposerIndex,
    route_id: str,
    *,
    action: str,
    expected_sha256: str,
    dry_run: bool = True,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_route: dict[str, Any] | None = None,
    anchor_route_id: str | None = None,
) -> dict[str, Any]:
    route = require_route(index, route_id)
    edits, semantic = semantic_edits(
        index,
        route,
        action=action,
        value=value,
        operation=operation,
        position=position,
        operation_index=operation_index,
        new_route=new_route,
        anchor_route_id=anchor_route_id,
    )
    result = change_router.apply_source_edits(
        index.router,
        route.target_id,
        edits,
        expected_sha256=expected_sha256,
        dry_run=dry_run,
    )
    if not dry_run:
        invalidate_composer(index.root)
    return {
        "semantic_operation": semantic,
        "route_id": route.id,
        "result": result,
        "warnings": [
            *result["warnings"],
            "Generated dialogue and exports were not changed; use dialogue_verify, then intentionally review/build downstream output.",
        ],
    }


def dialogue_verify(
    index: DialogueComposerIndex,
    route_id: str,
    *,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    route = require_route(index, route_id)
    verification = change_router.verify_change(
        index.router,
        route.target_id,
        expected_sha256=expected_sha256,
        run_tests=run_tests,
        stage_build_check=stage_build_check,
        max_tests=max_tests,
        timeout_seconds=timeout_seconds,
    )
    return {
        "route": route_payload(index, route),
        "first_match_analysis": route_shadow_analysis(index, route),
        "change_router_verification": verification,
        "warnings": [
            *verification["warnings"],
            "A static clean result does not prove runtime conditions; inspect compiled order after an intentional dialogue build.",
        ],
    }


def write_payload(payload: dict[str, Any], output: str | None, root: Path) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output:
        path = change_router.output_path(output, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def parse_json_argument(value: str | None, *, name: str, expected: type[Any]) -> Any:
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise DialogueComposerError(f"{name} must be JSON: {error}") from error
    if not isinstance(parsed, expected):
        raise DialogueComposerError(f"{name} must decode to a {expected.__name__}.")
    return parsed


def parse_json_file_argument(
    value: str | None,
    *,
    name: str,
    expected: type[Any],
    root: Path,
) -> Any:
    if not isinstance(value, str) or not value.strip():
        raise DialogueComposerError(f"{name} must be a non-empty repo-relative JSON file path.")
    candidate = Path(value)
    path = (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise DialogueComposerError(f"{name} must remain inside the module workspace.") from error
    if not path.is_file():
        raise DialogueComposerError(f"{name} does not exist or is not a file: {project_relative(path, root)}")
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:
        raise DialogueComposerError(f"Could not read {name}: {error}") from error
    if len(raw.encode("utf-8")) > MAX_CREATE_SPEC_FILE_BYTES:
        raise DialogueComposerError(f"{name} exceeds the {MAX_CREATE_SPEC_FILE_BYTES:,}-byte safety limit.")
    return parse_json_argument(raw, name=name, expected=expected)


def cli_create_spec(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    if args.spec is not None:
        return parse_json_argument(args.spec, name="spec", expected=dict)
    return parse_json_file_argument(args.spec_file, name="spec_file", expected=dict, root=root)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Semantic, SHA-guarded dialogue editing for SoD Modern modular source."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    for name in ("summary",):
        command = subparsers.add_parser(name)
        command.add_argument("--output")
    find = subparsers.add_parser("find")
    find.add_argument("--query")
    find.add_argument("--input-state")
    find.add_argument("--output-state")
    find.add_argument("--source")
    find.add_argument("--limit", type=int, default=20)
    find.add_argument("--output")
    context = subparsers.add_parser("context")
    context.add_argument("route_id")
    context.add_argument("--max-lines", type=int, default=100)
    context.add_argument("--related-limit", type=int, default=20)
    context.add_argument("--output")
    for name in ("patch", "apply"):
        command = subparsers.add_parser(name)
        command.add_argument("route_id")
        command.add_argument("action", choices=sorted(VALID_ACTIONS))
        command.add_argument("--value")
        command.add_argument("--operation")
        command.add_argument("--position", default="end")
        command.add_argument("--operation-index", type=int)
        command.add_argument("--new-route")
        command.add_argument("--anchor-route-id")
        command.add_argument("--expected-sha256")
        command.add_argument("--output")
        if name == "apply":
            command.add_argument("--apply", action="store_true")
    create_plan = subparsers.add_parser("create-plan")
    create_plan_inputs = create_plan.add_mutually_exclusive_group(required=True)
    create_plan_inputs.add_argument("--spec", help="JSON object conforming to contracts/dialogue-create.v1.schema.json")
    create_plan_inputs.add_argument("--spec-file", help="Repo-relative UTF-8 JSON request file")
    create_plan.add_argument("--expected-sha256")
    create_plan.add_argument("--output")
    create_apply = subparsers.add_parser("create-apply")
    create_apply_inputs = create_apply.add_mutually_exclusive_group(required=True)
    create_apply_inputs.add_argument("--spec", help="The exact JSON object used for create-plan")
    create_apply_inputs.add_argument("--spec-file", help="The exact repo-relative UTF-8 JSON request file used for create-plan")
    create_apply.add_argument("--expected-sha256", required=True)
    create_apply.add_argument("--expected-plan-id", required=True)
    create_apply.add_argument("--apply", action="store_true")
    create_apply.add_argument("--output")
    verify = subparsers.add_parser("verify")
    verify.add_argument("route_id")
    verify.add_argument("--expected-sha256")
    verify.add_argument("--run-tests", action="store_true")
    verify.add_argument("--stage-build", action="store_true")
    verify.add_argument("--max-tests", type=int, default=3)
    verify.add_argument("--timeout-seconds", type=int, default=90)
    verify.add_argument("--output")
    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        index = build_dialogue_composer(args.root)
        if command == "summary":
            payload = dialogue_summary(index)
        elif command == "find":
            payload = dialogue_find(
                index,
                query=args.query,
                input_state=args.input_state,
                output_state=args.output_state,
                source=args.source,
                limit=args.limit,
            )
        elif command == "context":
            payload = dialogue_context(index, args.route_id, max_lines=args.max_lines, related_limit=args.related_limit)
        elif command == "patch":
            payload = dialogue_patch(
                index,
                args.route_id,
                action=args.action,
                value=args.value,
                operation=args.operation,
                position=args.position,
                operation_index=args.operation_index,
                new_route=parse_json_argument(args.new_route, name="new_route", expected=dict),
                anchor_route_id=args.anchor_route_id,
                expected_sha256=args.expected_sha256,
            )
        elif command == "apply":
            if not args.expected_sha256:
                raise DialogueComposerError("apply requires --expected-sha256 from a dialogue patch plan.")
            payload = dialogue_apply(
                index,
                args.route_id,
                action=args.action,
                expected_sha256=args.expected_sha256,
                dry_run=not args.apply,
                value=args.value,
                operation=args.operation,
                position=args.position,
                operation_index=args.operation_index,
                new_route=parse_json_argument(args.new_route, name="new_route", expected=dict),
                anchor_route_id=args.anchor_route_id,
            )
        elif command == "create-plan":
            payload = dialogue_create_plan(
                index,
                cli_create_spec(args, index.root),
                expected_sha256=args.expected_sha256,
            )
        elif command == "create-apply":
            payload = dialogue_create_apply(
                index,
                cli_create_spec(args, index.root),
                expected_sha256=args.expected_sha256,
                expected_plan_id=args.expected_plan_id,
                dry_run=not args.apply,
            )
        elif command == "verify":
            payload = dialogue_verify(
                index,
                args.route_id,
                expected_sha256=args.expected_sha256,
                run_tests=args.run_tests,
                stage_build_check=args.stage_build,
                max_tests=args.max_tests,
                timeout_seconds=args.timeout_seconds,
            )
        else:
            raise DialogueComposerError(f"Unknown command: {command}")
        write_payload(payload, getattr(args, "output", None), index.root)
        return 0
    except (DialogueComposerError, change_router.ChangeRouterError) as error:
        parser.error(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
