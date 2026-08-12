#!/usr/bin/env python3
"""LLM-first presentation layout composer for Mount & Blade 1.011.

Presentation source is executable operation code, not a declarative UI tree.
This module reconstructs the statically knowable part of each presentation:
creation operations, position/size register writes, overlay bindings, text,
mesh, color, and alpha.  It deliberately marks dynamic paths as unresolved
instead of presenting an invented visual layout.

Semantic edits become exact Change Router anchors.  The only operation here
that can write source is ``presentation_apply`` and it delegates to the
existing SHA-guarded source-only Change Router gate.
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.change_router import change_router


COMPOSER_VERSION = "0.1.0"
MAX_QUERY_LENGTH = 500
MAX_LAYOUT_VALUE_LENGTH = 30_000
MAX_OVERLAP_FINDINGS = 300
OVERLAY_CREATE_RE = re.compile(r"^create_(?:[a-z0-9_]+_)?overlay$")
TEXTUAL_KINDS = frozenset({"text", "button", "game_button", "check_box", "combo_button"})
MESH_KINDS = frozenset({"mesh", "image", "image_button"})
VALID_ACTIONS = frozenset(
    {
        "move_overlay",
        "resize_overlay",
        "align_overlay",
        "set_text",
        "set_mesh",
        "set_color",
        "set_alpha",
        "add_overlay",
        "remove_overlay",
        "add_trigger",
        "remove_trigger",
        "replace_trigger_operations",
    }
)


class PresentationLayoutError(RuntimeError):
    """A static layout or semantic edit request is unsafe or incomplete."""


@dataclass(frozen=True)
class SourceDocument:
    path: str
    raw: str
    encoding: str
    offsets: tuple[int, ...]


@dataclass(frozen=True)
class ComponentBinding:
    """One x/y source expression and the operation that supplied it."""

    raw: str | None = None
    value: float | None = None
    start: int | None = None
    end: int | None = None
    line: int | None = None
    register: str | None = None

    @property
    def static(self) -> bool:
        return self.value is not None and self.start is not None and self.end is not None


@dataclass
class Overlay:
    id: str
    target_id: str
    path: str
    presentation_id: str
    presentation_key: str
    trigger: str
    trigger_line: int
    source_order: int | None
    line: int
    column: int
    creation_start: int
    creation_end: int
    creation_segment: str
    creation_operation: str
    kind: str
    identifier: str
    content: str | None
    content_start: int | None
    content_end: int | None
    position_x: ComponentBinding = field(default_factory=ComponentBinding)
    position_y: ComponentBinding = field(default_factory=ComponentBinding)
    size_x: ComponentBinding = field(default_factory=ComponentBinding)
    size_y: ComponentBinding = field(default_factory=ComponentBinding)
    color: ComponentBinding = field(default_factory=ComponentBinding)
    alpha: ComponentBinding = field(default_factory=ComponentBinding)
    position_register: str | None = None
    size_register: str | None = None
    operation_spans: list[tuple[int, int]] = field(default_factory=list)
    previous_string_writers: tuple[str, ...] = ()
    dynamic: bool = False


@dataclass(frozen=True)
class TriggerBlock:
    name: str
    line: int
    start: int
    end: int
    list_start: int
    list_end: int
    operation_count: int


@dataclass
class Presentation:
    id: str
    key: str
    target_id: str
    path: str
    line: int
    source_order: int | None
    trigger_list_start: int
    trigger_list_end: int
    triggers: tuple[TriggerBlock, ...]
    overlays: list[Overlay]
    nested_layout_operation_count: int = 0


@dataclass
class PresentationLayoutIndex:
    root: Path
    router: change_router.RouterIndex
    documents: dict[str, SourceDocument]
    presentations: tuple[Presentation, ...]
    by_key: dict[str, Presentation]
    by_name: dict[str, tuple[Presentation, ...]]
    overlays: tuple[Overlay, ...]
    overlay_by_id: dict[str, Overlay]


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], PresentationLayoutIndex]] = {}


def line_offsets(raw: str) -> tuple[int, ...]:
    offsets = [0]
    for index, character in enumerate(raw):
        if character == "\n":
            offsets.append(index + 1)
    return tuple(offsets)


def node_bounds(node: ast.AST, offsets: Sequence[int]) -> tuple[int, int]:
    values = (
        getattr(node, "lineno", None),
        getattr(node, "end_lineno", None),
        getattr(node, "col_offset", None),
        getattr(node, "end_col_offset", None),
    )
    if not all(isinstance(value, int) for value in values):
        raise PresentationLayoutError("A presentation node is missing exact source positions.")
    start_line, end_line, start_column, end_column = values
    if start_line < 1 or end_line < start_line or start_line > len(offsets) or end_line > len(offsets):
        raise PresentationLayoutError("A presentation node has an invalid source span.")
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


def literal_string(node: ast.AST) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return expression_text(node)


def content_literal(expression: str | None) -> str | None:
    """Return a direct quoted overlay value without resolving runtime state.

    Overlay content commonly points at an ``s`` register populated earlier in
    the trigger. That expression is intentionally *not* a text value: showing
    it in a human text field and writing it back as a quoted string would turn
    a dynamic UI label into the literal characters ``s68``. Keep the raw
    expression available separately and expose a value only when the source is
    an actual Python string literal.
    """

    if not isinstance(expression, str) or not expression.strip():
        return None
    try:
        node = ast.parse(expression, mode="eval").body
    except SyntaxError:
        return None
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def literal_number(node: ast.AST) -> float | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        value = literal_number(node.operand)
        if value is not None:
            return -value if isinstance(node.op, ast.USub) else value
    return None


def format_number(value: float | int) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise PresentationLayoutError("Layout coordinate values must be finite numbers.")
    numeric = float(value)
    return str(int(numeric)) if numeric.is_integer() else format(numeric, ".6g")


def component_from_node(document: SourceDocument, node: ast.AST, register: str | None) -> ComponentBinding:
    start, end = node_bounds(node, document.offsets)
    return ComponentBinding(
        raw=document.raw[start:end],
        value=literal_number(node),
        start=start,
        end=end,
        line=getattr(node, "lineno", None),
        register=register,
    )


def find_presentations_assignment(tree: ast.Module) -> ast.List | None:
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "PRESENTATIONS" for target in statement.targets):
            continue
        if isinstance(statement.value, ast.List):
            return statement.value
        raise PresentationLayoutError("PRESENTATIONS must be assigned a list literal.")
    return None


def source_document(router: change_router.RouterIndex, relative: str) -> SourceDocument:
    fragment = router.fragments[relative]
    raw, encoding, _ = change_router.read_text_with_encoding(change_router.source_path(router, fragment))
    return SourceDocument(relative, raw, encoding, line_offsets(raw))


def operation_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Tuple) and node.elts:
        return expression_symbol(node.elts[0])
    if isinstance(node, ast.Name):
        return node.id
    return None


def operation_arguments(node: ast.AST) -> list[ast.AST]:
    return list(node.elts[1:]) if isinstance(node, ast.Tuple) else []


def overlay_kind(operation: str) -> str:
    value = operation.removeprefix("create_").removesuffix("_overlay")
    return value or "unknown"


def is_create_overlay(operation: str | None) -> bool:
    return bool(operation and OVERLAY_CREATE_RE.fullmatch(operation))


def component_payload(component: ComponentBinding) -> dict[str, Any]:
    return {
        "expression": component.raw,
        "value": component.value,
        "static": component.static,
        "line": component.line,
        "position_register": component.register,
    }


def parse_trigger(
    document: SourceDocument,
    presentation: Presentation,
    trigger_name: str,
    trigger_line: int,
    operations: ast.List,
) -> list[Overlay]:
    """Interpret direct layout operations in one trigger in execution order."""

    position_state: dict[str, dict[str, ComponentBinding]] = defaultdict(dict)
    most_recent: dict[str, Overlay] = {}
    overlays: list[Overlay] = []
    string_writers: set[str] = set()
    for statement in operations.elts:
        name = operation_name(statement)
        arguments = operation_arguments(statement)
        if name is None:
            continue
        statement_start, statement_end = node_bounds(statement, document.offsets)
        if name in {"position_set_x", "position_set_y"} and len(arguments) >= 2:
            register = expression_symbol(arguments[0])
            axis = "x" if name.endswith("_x") else "y"
            position_state[register][axis] = component_from_node(document, arguments[1], register)
            continue
        if name in {"str_store_string", "str_store_string_reg", "str_store_troop_name", "str_store_party_name", "str_store_item_name", "str_store_agent_name", "str_clear"} and arguments:
            string_writers.add(expression_symbol(arguments[0]))
            continue
        if is_create_overlay(name) and arguments:
            identifier = expression_symbol(arguments[0])
            content = None
            content_start = None
            content_end = None
            if len(arguments) >= 2:
                content = node_segment(document.raw, arguments[1], document.offsets)
                content_start, content_end = node_bounds(arguments[1], document.offsets)
            line = getattr(statement, "lineno", 0)
            column = getattr(statement, "col_offset", 0)
            overlay = Overlay(
                id=f"overlay:{document.path}:L{line}:C{column}",
                target_id=presentation.target_id,
                path=document.path,
                presentation_id=presentation.id,
                presentation_key=presentation.key,
                trigger=trigger_name,
                trigger_line=trigger_line,
                source_order=presentation.source_order,
                line=line,
                column=column,
                creation_start=statement_start,
                creation_end=statement_end,
                creation_segment=document.raw[statement_start:statement_end],
                creation_operation=name,
                kind=overlay_kind(name),
                identifier=identifier,
                content=content,
                content_start=content_start,
                content_end=content_end,
                operation_spans=[(statement_start, statement_end)],
                previous_string_writers=tuple(sorted(string_writers)),
                dynamic=trigger_name != "ti_on_presentation_load",
            )
            overlays.append(overlay)
            most_recent[identifier] = overlay
            continue
        if name.startswith("overlay_set_") and arguments:
            identifier = expression_symbol(arguments[0])
            overlay = most_recent.get(identifier)
            if overlay is None:
                continue
            overlay.operation_spans.append((statement_start, statement_end))
            if name in {"overlay_set_position", "overlay_set_size"} and len(arguments) >= 2:
                register = expression_symbol(arguments[1])
                state = position_state.get(register, {})
                if name == "overlay_set_position":
                    overlay.position_register = register
                    overlay.position_x = state.get("x", ComponentBinding(register=register))
                    overlay.position_y = state.get("y", ComponentBinding(register=register))
                else:
                    overlay.size_register = register
                    overlay.size_x = state.get("x", ComponentBinding(register=register))
                    overlay.size_y = state.get("y", ComponentBinding(register=register))
            elif name == "overlay_set_text" and len(arguments) >= 2:
                overlay.content = node_segment(document.raw, arguments[1], document.offsets)
                overlay.content_start, overlay.content_end = node_bounds(arguments[1], document.offsets)
            elif name == "overlay_set_color" and len(arguments) >= 2:
                overlay.color = component_from_node(document, arguments[1], None)
            elif name == "overlay_set_alpha" and len(arguments) >= 2:
                overlay.alpha = component_from_node(document, arguments[1], None)
    return overlays


def parse_presentations_in_document(
    router: change_router.RouterIndex,
    document: SourceDocument,
) -> list[Presentation]:
    path = router.root / document.path
    try:
        tree = ast.parse(document.raw, filename=str(path))
    except SyntaxError as error:
        raise PresentationLayoutError(f"Cannot parse {document.path} at line {error.lineno}: {error.msg}") from error
    assignment = find_presentations_assignment(tree)
    if assignment is None:
        return []
    fragment = router.fragments[document.path]
    presentations: list[Presentation] = []
    for ordinal, entry in enumerate(assignment.elts, start=1):
        if not isinstance(entry, (ast.Tuple, ast.List)) or len(entry.elts) < 4 or not isinstance(entry.elts[3], ast.List):
            continue
        presentation_id = literal_string(entry.elts[0])
        line = getattr(entry, "lineno", 0)
        key = f"presentation:{document.path}:L{line}:N{ordinal}"
        trigger_blocks: list[TriggerBlock] = []
        trigger_nodes: list[tuple[str, int, ast.List]] = []
        trigger_list_start, trigger_list_end = node_bounds(entry.elts[3], document.offsets)
        for trigger in entry.elts[3].elts:
            if not isinstance(trigger, (ast.Tuple, ast.List)) or len(trigger.elts) < 2 or not isinstance(trigger.elts[1], ast.List):
                continue
            event = expression_symbol(trigger.elts[0])
            operations = trigger.elts[1]
            list_start, list_end = node_bounds(operations, document.offsets)
            trigger_start, trigger_end = node_bounds(trigger, document.offsets)
            trigger_blocks.append(
                TriggerBlock(
                    name=event,
                    line=getattr(trigger, "lineno", 0),
                    start=trigger_start,
                    end=trigger_end,
                    list_start=list_start,
                    list_end=list_end,
                    operation_count=len(operations.elts),
                )
            )
            trigger_nodes.append((event, getattr(trigger, "lineno", 0), operations))
        presentation = Presentation(
            id=presentation_id,
            key=key,
            target_id=fragment.id,
            path=document.path,
            line=line,
            source_order=fragment.order_position,
            trigger_list_start=trigger_list_start,
            trigger_list_end=trigger_list_end,
            triggers=tuple(trigger_blocks),
            overlays=[],
        )
        for event, trigger_line, operations in trigger_nodes:
            presentation.overlays.extend(parse_trigger(document, presentation, event, trigger_line, operations))
            direct = set(id(item) for item in operations.elts)
            nested = sum(1 for item in ast.walk(operations) if id(item) not in direct and is_create_overlay(operation_name(item)))
            presentation.nested_layout_operation_count += nested
        presentations.append(presentation)
    return presentations


def build_presentation_layout(root: Path = DEFAULT_REPO_ROOT) -> PresentationLayoutIndex:
    """Build static presentation and overlay links without executing fragments."""

    root = root.resolve()
    router = change_router.build_change_router(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == router.signature:
        return cached[1]
    documents: dict[str, SourceDocument] = {}
    presentations: list[Presentation] = []
    paths = router.ordering.get("presentations", [])
    if not paths:
        paths = sorted((path for path, fragment in router.fragments.items() if fragment.area == "presentations"), key=str.lower)
    for relative in paths:
        fragment = router.fragments.get(relative)
        if fragment is None or fragment.area != "presentations" or fragment.syntax_error is not None:
            continue
        document = source_document(router, relative)
        documents[relative] = document
        presentations.extend(parse_presentations_in_document(router, document))
    overlays = [overlay for presentation in presentations for overlay in presentation.overlays]
    by_name: dict[str, list[Presentation]] = defaultdict(list)
    for presentation in presentations:
        by_name[presentation.id].append(presentation)
    index = PresentationLayoutIndex(
        root=root,
        router=router,
        documents=documents,
        presentations=tuple(presentations),
        by_key={presentation.key: presentation for presentation in presentations},
        by_name={name: tuple(items) for name, items in by_name.items()},
        overlays=tuple(overlays),
        overlay_by_id={overlay.id: overlay for overlay in overlays},
    )
    _CACHE[root] = (router.signature, index)
    return index


def invalidate_layout(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def require_query(value: str, *, name: str = "query") -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationLayoutError(f"{name} must not be empty.")
    if len(value) > MAX_QUERY_LENGTH:
        raise PresentationLayoutError(f"{name} must be at most {MAX_QUERY_LENGTH} characters.")
    return value.strip()


def require_limit(value: int, *, name: str = "limit", maximum: int = 200) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise PresentationLayoutError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_overlay(index: PresentationLayoutIndex, overlay_id: str) -> Overlay:
    if not isinstance(overlay_id, str) or not overlay_id.startswith("overlay:"):
        raise PresentationLayoutError("overlay_id must be an overlay ID returned by presentation_find or presentation_canvas.")
    overlay = index.overlay_by_id.get(overlay_id)
    if overlay is None:
        raise PresentationLayoutError("Unknown overlay; refresh presentation_find before editing.")
    return overlay


def resolve_presentation(index: PresentationLayoutIndex, value: str) -> Presentation:
    value = require_query(value, name="presentation_id")
    if value.startswith("presentation:"):
        presentation = index.by_key.get(value)
        if presentation is None:
            raise PresentationLayoutError("Unknown presentation key; refresh presentation_find.")
        return presentation
    matches = index.by_name.get(value, ())
    if not matches:
        raise PresentationLayoutError(f"No presentation named {value!r} was found.")
    if len(matches) > 1:
        raise PresentationLayoutError(f"Presentation id {value!r} is ambiguous; use its presentation_key from presentation_find.")
    return matches[0]


def overlay_payload(overlay: Overlay) -> dict[str, Any]:
    literal = content_literal(overlay.content)
    return {
        "overlay_id": overlay.id,
        "identifier": overlay.identifier,
        "kind": overlay.kind,
        "creation_operation": overlay.creation_operation,
        "source": {"path": overlay.path, "line": overlay.line, "column": overlay.column, "target_id": overlay.target_id},
        "presentation_id": overlay.presentation_id,
        "presentation_key": overlay.presentation_key,
        "trigger": overlay.trigger,
        "dynamic_trigger": overlay.dynamic,
        "content": overlay.content,
        "content_is_literal": literal is not None,
        "content_literal": literal,
        "position": {"x": component_payload(overlay.position_x), "y": component_payload(overlay.position_y), "register": overlay.position_register},
        "size": {"x": component_payload(overlay.size_x), "y": component_payload(overlay.size_y), "register": overlay.size_register},
        "color": component_payload(overlay.color),
        "alpha": component_payload(overlay.alpha),
        "previous_string_writers": list(overlay.previous_string_writers),
    }


def presentation_payload(presentation: Presentation) -> dict[str, Any]:
    return {
        "presentation_id": presentation.id,
        "presentation_key": presentation.key,
        "target_id": presentation.target_id,
        "source": {"path": presentation.path, "line": presentation.line, "section_order": presentation.source_order},
        "trigger_count": len(presentation.triggers),
        "triggers": [
            {"name": trigger.name, "line": trigger.line, "operation_count": trigger.operation_count}
            for trigger in presentation.triggers
        ],
        "overlay_count": len(presentation.overlays),
        "nested_layout_operation_count": presentation.nested_layout_operation_count,
    }


def presentation_summary(index: PresentationLayoutIndex) -> dict[str, Any]:
    static = sum(not overlay.dynamic for overlay in index.overlays)
    positioned = sum(overlay.position_x.static and overlay.position_y.static for overlay in index.overlays)
    return {
        "composer_version": f"devkit.presentation-layout.v{COMPOSER_VERSION}",
        "presentation_count": len(index.presentations),
        "overlay_count": len(index.overlays),
        "load_trigger_overlay_count": static,
        "static_position_count": positioned,
        "warnings": [
            "The canvas models direct trigger operations only; runtime loops, conditionals, and register-derived coordinates stay explicitly unresolved.",
            "All semantic source writes are delegated to the Change Router SHA gate and never write compile/ or _export/.",
        ],
    }


def presentation_find(
    index: PresentationLayoutIndex,
    *,
    query: str,
    limit: int = 20,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    requested_query = require_query(query)
    match_all = requested_query == "*"
    needle = requested_query.casefold()
    matched_presentations = []
    for presentation in index.presentations:
        searchable = "\n".join(
            (
                presentation.id,
                presentation.key,
                presentation.path,
                *(
                    "\n".join(
                        (
                            overlay.identifier,
                            overlay.kind,
                            overlay.trigger,
                            overlay.content or "",
                        )
                    )
                    for overlay in presentation.overlays
                ),
            )
        ).casefold()
        if match_all or needle in searchable:
            matched_presentations.append(presentation)
    matched_presentations.sort(key=lambda item: ((item.source_order or 1_000_000), item.line, item.key))
    return {
        "summary": presentation_summary(index),
        "match_count": len(matched_presentations),
        "returned_count": min(len(matched_presentations), maximum),
        "truncated": len(matched_presentations) > maximum,
        "presentations": [
            {
                **presentation_payload(presentation),
                "overlays": [overlay_payload(overlay) for overlay in presentation.overlays[:80]],
                "overlays_truncated": len(presentation.overlays) > 80,
            }
            for presentation in matched_presentations[:maximum]
        ],
    }


def effective_canvas_box(overlay: Overlay, width: int, height: int) -> dict[str, Any] | None:
    """Approximate a static screen-space box from M&B's 0..1000 coordinate grid."""

    if not (overlay.position_x.static and overlay.position_y.static):
        return None
    assert overlay.position_x.value is not None and overlay.position_y.value is not None
    x = overlay.position_x.value
    y = overlay.position_y.value
    # Overlay size is an engine scale vector, not a pixel rectangle.  A 1/10
    # approximation makes mesh planes and common text sizes legible while
    # remaining clearly labeled as an estimate in the returned canvas model.
    if overlay.size_x.value is not None:
        box_width = max(16.0, min(width * 2.0, overlay.size_x.value / 10.0))
    else:
        box_width = max(72.0, min(width * 0.45, 12.0 * len((overlay.content or overlay.identifier).strip())))
    if overlay.size_y.value is not None:
        box_height = max(16.0, min(height * 2.0, overlay.size_y.value / 10.0))
    else:
        box_height = 30.0 if overlay.kind in TEXTUAL_KINDS else 72.0
    left = (x / 1000.0) * width
    bottom = (y / 1000.0) * height
    top = height - bottom - box_height
    return {
        "x": round(left, 2),
        "y": round(top, 2),
        "width": round(box_width, 2),
        "height": round(box_height, 2),
        "engine_anchor": {"x": x, "y": y},
        "estimated": True,
    }


def boxes_overlap(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return (
        first["x"] < second["x"] + second["width"]
        and first["x"] + first["width"] > second["x"]
        and first["y"] < second["y"] + second["height"]
        and first["y"] + first["height"] > second["y"]
    )


def layout_findings(presentation: Presentation, width: int, height: int) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    by_destination: dict[tuple[str, str], list[Overlay]] = defaultdict(list)
    boxes: list[tuple[Overlay, dict[str, Any]]] = []
    for overlay in presentation.overlays:
        by_destination[(overlay.trigger, overlay.identifier)].append(overlay)
        if not (overlay.position_x.static and overlay.position_y.static):
            findings.append({"severity": "info", "code": "POSITION_UNRESOLVED", "overlay_id": overlay.id, "message": "Position comes from a dynamic or missing register component; no static canvas placement is claimed."})
        else:
            assert overlay.position_x.value is not None and overlay.position_y.value is not None
            if not 0 <= overlay.position_x.value <= 1000 or not 0 <= overlay.position_y.value <= 1000:
                findings.append({"severity": "warning", "code": "ANCHOR_OFFSCREEN", "overlay_id": overlay.id, "message": "The static position anchor is outside the nominal 0..1000 presentation coordinate grid."})
            box = effective_canvas_box(overlay, width, height)
            if box is not None:
                boxes.append((overlay, box))
        if overlay.kind in TEXTUAL_KINDS and overlay.content and re.fullmatch(r"s\d+", overlay.content.strip()) and overlay.content.strip() not in overlay.previous_string_writers:
            findings.append({"severity": "warning", "code": "TEXT_REGISTER_WITHOUT_LOCAL_WRITER", "overlay_id": overlay.id, "message": f"{overlay.content.strip()} is displayed but no preceding string writer was found in this direct trigger block."})
    for (trigger, identifier), overlays in by_destination.items():
        if len(overlays) > 1:
            findings.append({"severity": "info", "code": "REUSED_OVERLAY_DESTINATION", "trigger": trigger, "identifier": identifier, "overlay_ids": [item.id for item in overlays], "message": "The same destination receives more than one create operation in one trigger; this can be intentional but deserves runtime review."})
    overlap_count = 0
    for left in range(len(boxes)):
        first_overlay, first = boxes[left]
        for right in range(left + 1, len(boxes)):
            second_overlay, second = boxes[right]
            if first_overlay.trigger != second_overlay.trigger or not boxes_overlap(first, second):
                continue
            overlap_count += 1
            if overlap_count <= MAX_OVERLAP_FINDINGS:
                findings.append({"severity": "info", "code": "ESTIMATED_OVERLAP", "overlay_ids": [first_overlay.id, second_overlay.id], "message": "Estimated static canvas boxes overlap. Engine anchors/scale can differ at runtime."})
    controls = [overlay for overlay in presentation.overlays if overlay.kind in {"button", "game_button", "slider", "check_box", "combo_button"}]
    trigger_names = {trigger.name for trigger in presentation.triggers}
    if controls and "ti_on_presentation_event_state_change" not in trigger_names:
        findings.append({"severity": "warning", "code": "CONTROL_WITHOUT_EVENT_TRIGGER", "overlay_ids": [overlay.id for overlay in controls], "message": "Static controls exist but no ti_on_presentation_event_state_change trigger was found in this presentation."})
    if presentation.nested_layout_operation_count:
        findings.append({"severity": "info", "code": "NESTED_LAYOUT_UNMODELED", "count": presentation.nested_layout_operation_count, "message": "Nested create-overlay operations were detected inside control flow and are intentionally excluded from the static canvas."})
    if overlap_count > MAX_OVERLAP_FINDINGS:
        findings.append({"severity": "info", "code": "OVERLAP_FINDINGS_TRUNCATED", "count": overlap_count, "message": f"Only the first {MAX_OVERLAP_FINDINGS} estimated overlaps are returned."})
    return findings


def presentation_canvas(
    index: PresentationLayoutIndex,
    presentation_id: str,
    *,
    width: int = 1024,
    height: int = 768,
    overlay_limit: int = 200,
) -> dict[str, Any]:
    presentation = resolve_presentation(index, presentation_id)
    canvas_width = require_limit(width, name="width", maximum=4096)
    canvas_height = require_limit(height, name="height", maximum=4096)
    maximum_overlays = require_limit(overlay_limit, name="overlay_limit", maximum=1_000)
    entries: list[dict[str, Any]] = []
    for overlay in presentation.overlays[:maximum_overlays]:
        entries.append({**overlay_payload(overlay), "canvas_box": effective_canvas_box(overlay, canvas_width, canvas_height)})
    return {
        "presentation": presentation_payload(presentation),
        "canvas": {
            "width": canvas_width,
            "height": canvas_height,
            "coordinate_system": "Mount & Blade presentation anchors are modeled as x/y in a nominal 0..1000 grid with a bottom-left origin; SVG y is inverted.",
            "size_model": "Overlay size is an estimated visual box (engine scale vector divided by 10); it is not a runtime pixel guarantee.",
            "overlay_count": len(presentation.overlays),
            "returned_overlay_count": len(entries),
            "overlays_truncated": len(presentation.overlays) > len(entries),
            "overlays": entries,
        },
        "findings": layout_findings(presentation, canvas_width, canvas_height),
        "warnings": [
            "Static canvas only: dynamic branches, loops, screen ratio behavior, text metrics, and engine-created controls must still be tested in-game.",
        ],
    }


def render_svg(canvas_payload: dict[str, Any]) -> str:
    canvas = canvas_payload["canvas"]
    width = int(canvas["width"])
    height = int(canvas["height"])
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<rect width=\"100%\" height=\"100%\" fill=\"#15191f\"/>",
        "<g stroke=\"#334155\" stroke-width=\"1\" opacity=\"0.65\">",
    ]
    for fraction in range(1, 10):
        x = width * fraction / 10
        y = height * fraction / 10
        pieces.append(f'<path d="M{x:.1f} 0V{height}"/><path d="M0 {y:.1f}H{width}"/>')
    pieces.append("</g><g font-family=\"Consolas, monospace\" font-size=\"12\">")
    colors = {"text": "#7dd3fc", "button": "#fbbf24", "slider": "#c4b5fd", "mesh": "#86efac", "game_button": "#fbbf24"}
    for overlay in canvas["overlays"]:
        box = overlay.get("canvas_box")
        if not box:
            continue
        color = colors.get(overlay["kind"], "#fda4af")
        x, y, box_width, box_height = box["x"], box["y"], box["width"], box["height"]
        label = overlay["identifier"]
        if overlay.get("content"):
            label += " | " + str(overlay["content"]).replace("\n", " ")[:52]
        pieces.append(f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" fill="{color}" fill-opacity="0.19" stroke="{color}"/>')
        pieces.append(f'<text x="{x + 4}" y="{max(13, y + 15)}" fill="{color}">{html.escape(label)}</text>')
    pieces.append("</g>")
    unresolved = sum(1 for overlay in canvas["overlays"] if not overlay.get("canvas_box"))
    if unresolved:
        pieces.append(f'<text x="12" y="{height - 12}" fill="#fbbf24" font-family="Consolas, monospace" font-size="12">{unresolved} dynamic/unresolved overlay(s) omitted from canvas</text>')
    pieces.append("</svg>")
    return "".join(pieces)


def safe_preview_path(root: Path, output_name: str | None, presentation: Presentation) -> Path:
    suggested = output_name or f"presentation-{presentation.id}.svg"
    name = Path(suggested).name
    if name != suggested or not name.lower().endswith(".svg"):
        raise PresentationLayoutError("output_name must be a simple .svg filename; preview artifacts are confined to devkit/output/.")
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-") or "presentation-preview.svg"
    if not safe_name.lower().endswith(".svg"):
        safe_name += ".svg"
    return root / "devkit" / "output" / safe_name


def presentation_preview(
    index: PresentationLayoutIndex,
    presentation_id: str,
    *,
    output_name: str | None = None,
    width: int = 1024,
    height: int = 768,
) -> dict[str, Any]:
    payload = presentation_canvas(index, presentation_id, width=width, height=height, overlay_limit=1_000)
    presentation = resolve_presentation(index, presentation_id)
    path = safe_preview_path(index.root, output_name, presentation)
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = render_svg(payload)
    path.write_text(svg, encoding="utf-8", newline="")
    return {
        "presentation": payload["presentation"],
        "artifact": {"path": path.relative_to(index.root).as_posix(), "format": "svg", "bytes": len(svg.encode("utf-8"))},
        "findings": payload["findings"],
        "warnings": [
            *payload["warnings"],
            "The SVG is a static diagnostic artifact, not a replacement for engine rendering or runtime probes.",
        ],
    }


def parse_expression(value: str, *, name: str) -> ast.AST:
    if not isinstance(value, str) or not value.strip():
        raise PresentationLayoutError(f"{name} must be a non-empty Python expression.")
    if len(value) > MAX_LAYOUT_VALUE_LENGTH:
        raise PresentationLayoutError(f"{name} exceeds the {MAX_LAYOUT_VALUE_LENGTH:,}-character safety limit.")
    try:
        return ast.parse(value.strip(), mode="eval").body
    except SyntaxError as error:
        raise PresentationLayoutError(f"{name} is not a valid Python expression: {error.msg}") from error


def validate_operation_list(value: str, *, name: str) -> str:
    expression = parse_expression(value, name=name)
    if not isinstance(expression, ast.List):
        raise PresentationLayoutError(f"{name} must be a list of operation tuples or zero-argument operation names.")
    for item in expression.elts:
        if not isinstance(item, (ast.Tuple, ast.Name)):
            raise PresentationLayoutError(f"{name} may contain only operation tuples or zero-argument operation names.")
    return value.strip()


def validate_trigger_event(value: str, *, name: str) -> str:
    expression = parse_expression(value, name=name)
    if not isinstance(expression, ast.Name):
        raise PresentationLayoutError(f"{name} must be an event constant such as ti_on_presentation_run.")
    return value.strip()


def quoted(value: str, *, name: str) -> str:
    if not isinstance(value, str) or len(value) > MAX_LAYOUT_VALUE_LENGTH:
        raise PresentationLayoutError(f"{name} must be a string under {MAX_LAYOUT_VALUE_LENGTH:,} characters.")
    return json.dumps(value, ensure_ascii=False)


def require_static_component(component: ComponentBinding, *, axis: str, action: str) -> ComponentBinding:
    if not component.static:
        raise PresentationLayoutError(f"{action} requires a statically anchored {axis} component; this overlay uses a dynamic or missing position register expression.")
    return component


def occurrence_edit(raw: str, start: int, end: int, new_text: str) -> dict[str, Any]:
    if not 0 <= start < end <= len(raw):
        raise PresentationLayoutError("Semantic edit range is outside its source fragment.")
    old_text = raw[start:end]
    occurrences = change_router.all_occurrences(raw, old_text)
    try:
        occurrence = occurrences.index(start) + 1
    except ValueError as error:
        raise PresentationLayoutError("Could not locate a semantic source anchor.") from error
    return {"old_text": old_text, "new_text": new_text, "occurrence": occurrence, "expected_occurrences": len(occurrences)}


def component_edit(document: SourceDocument, component: ComponentBinding, value: float | int, *, action: str) -> dict[str, Any]:
    component = require_static_component(component, axis="coordinate", action=action)
    assert component.start is not None and component.end is not None
    return occurrence_edit(document.raw, component.start, component.end, format_number(value))


def operation_with_separator(document: SourceDocument, start: int, end: int) -> tuple[int, int]:
    raw = document.raw
    line_start = raw.rfind("\n", 0, start) + 1
    if raw[line_start:start].strip() == "":
        start = line_start
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


def line_indent(raw: str, offset: int) -> str:
    line_start = raw.rfind("\n", 0, offset) + 1
    prefix = raw[line_start:offset]
    match = re.match(r"[ \t]*", prefix)
    return match.group(0) if match is not None else ""


def source_variable(value: str, *, name: str) -> str:
    value = require_query(value, name=name)
    if re.fullmatch(r"[$:][A-Za-z_][A-Za-z0-9_]*", value):
        return quoted(value, name=name)
    parse_expression(value, name=name)
    return value


def render_new_overlay(new_overlay: dict[str, Any], indent: str) -> str:
    if not isinstance(new_overlay, dict):
        raise PresentationLayoutError("new_overlay must be an object.")
    kind = require_query(str(new_overlay.get("kind", "")), name="new_overlay.kind")
    if kind not in {"text", "button", "mesh", "slider"}:
        raise PresentationLayoutError("new_overlay.kind must be one of: text, button, mesh, slider.")
    destination = source_variable(str(new_overlay.get("destination", "")), name="new_overlay.destination")
    register = str(new_overlay.get("position_register", "pos1"))
    if not re.fullmatch(r"pos\d+", register):
        raise PresentationLayoutError("new_overlay.position_register must be a position register such as pos1.")
    x = format_number(new_overlay.get("x", 500))
    y = format_number(new_overlay.get("y", 500))
    size_x = new_overlay.get("size_x")
    size_y = new_overlay.get("size_y")
    operations: list[str] = []
    if kind == "text":
        operations.append(f"(create_text_overlay, {destination}, {quoted(new_overlay.get('text', ''), name='new_overlay.text')})")
    elif kind == "button":
        operations.append(f"(create_button_overlay, {destination}, {quoted(new_overlay.get('text', ''), name='new_overlay.text')})")
    elif kind == "mesh":
        mesh = require_query(str(new_overlay.get("mesh", "")), name="new_overlay.mesh")
        operations.append(f"(create_mesh_overlay, {destination}, {quoted(mesh, name='new_overlay.mesh')})")
    else:
        minimum = format_number(new_overlay.get("minimum", 0))
        maximum = format_number(new_overlay.get("maximum", 100))
        operations.append(f"(create_slider_overlay, {destination}, {minimum}, {maximum})")
    operations.extend(
        (
            f"(position_set_x, {register}, {x})",
            f"(position_set_y, {register}, {y})",
            f"(overlay_set_position, {destination}, {register})",
        )
    )
    if size_x is not None or size_y is not None:
        if size_x is None or size_y is None:
            raise PresentationLayoutError("new_overlay.size_x and size_y must be supplied together.")
        operations.extend(
            (
                f"(position_set_x, {register}, {format_number(size_x)})",
                f"(position_set_y, {register}, {format_number(size_y)})",
                f"(overlay_set_size, {destination}, {register})",
            )
        )
    return ",\n".join(indent + operation for operation in operations)


def append_operations(document: SourceDocument, trigger: TriggerBlock, rendered: str) -> dict[str, Any]:
    original = document.raw[trigger.list_start:trigger.list_end]
    if not original.startswith("[") or not original.endswith("]"):
        raise PresentationLayoutError("Selected trigger is no longer a direct operation list.")
    base_indent = line_indent(document.raw, trigger.list_start)
    inner = original[1:-1].rstrip()
    if inner.strip():
        separator = "" if inner.rstrip().endswith(",") else ","
        replacement = "[" + inner + separator + "\n" + rendered + "\n" + base_indent + "]"
    else:
        replacement = "[\n" + rendered + "\n" + base_indent + "]"
    return occurrence_edit(document.raw, trigger.list_start, trigger.list_end, replacement)


def find_trigger(presentation: Presentation, trigger_name: str) -> TriggerBlock:
    for trigger in presentation.triggers:
        if trigger.name == trigger_name:
            return trigger
    raise PresentationLayoutError(f"Presentation {presentation.id!r} has no {trigger_name} trigger.")


def render_trigger(new_trigger: dict[str, Any]) -> str:
    if not isinstance(new_trigger, dict):
        raise PresentationLayoutError("new_trigger must be an object with event and operations.")
    if "event" not in new_trigger:
        raise PresentationLayoutError("new_trigger is missing event.")
    event = validate_trigger_event(str(new_trigger["event"]), name="new_trigger.event")
    operations = validate_operation_list(str(new_trigger.get("operations", "[]")), name="new_trigger.operations")
    return f"({event}, {operations})"


def append_trigger(document: SourceDocument, presentation: Presentation, rendered: str) -> dict[str, Any]:
    if presentation.triggers:
        anchor = presentation.triggers[-1]
        indent = line_indent(document.raw, anchor.start)
        replacement = document.raw[anchor.start:anchor.end] + ",\n" + indent + rendered
        return occurrence_edit(document.raw, anchor.start, anchor.end, replacement)
    original = document.raw[presentation.trigger_list_start:presentation.trigger_list_end]
    if not original.startswith("[") or not original.endswith("]"):
        raise PresentationLayoutError("Presentation trigger collection is no longer a direct list.")
    base_indent = line_indent(document.raw, presentation.trigger_list_start)
    replacement = "[\n" + base_indent + "    " + rendered + "\n" + base_indent + "]"
    return occurrence_edit(document.raw, presentation.trigger_list_start, presentation.trigger_list_end, replacement)


def alignment_coordinates(overlay: Overlay, alignment: str) -> tuple[float | None, float | None]:
    if alignment not in {"left", "center", "right", "top", "middle", "bottom"}:
        raise PresentationLayoutError("alignment must be one of: left, center, right, top, middle, bottom.")
    if alignment == "left":
        return 0.0, None
    if alignment == "center":
        return 500.0, None
    if alignment == "right":
        return 1000.0, None
    if alignment == "top":
        return None, 1000.0
    if alignment == "middle":
        return None, 500.0
    return None, 0.0


def shared_binding_consumers(
    index: PresentationLayoutIndex,
    overlay: Overlay,
    component: ComponentBinding,
    *,
    binding: str,
) -> list[dict[str, Any]]:
    """Expose position-register reuse before a semantic coordinate edit."""

    if component.start is None or component.end is None:
        return []
    consumers: list[dict[str, Any]] = []
    for candidate in index.overlays:
        if candidate.path != overlay.path or candidate.id == overlay.id:
            continue
        candidates = {
            "position_x": candidate.position_x,
            "position_y": candidate.position_y,
            "size_x": candidate.size_x,
            "size_y": candidate.size_y,
        }
        for candidate_binding, value in candidates.items():
            if value.start == component.start and value.end == component.end:
                consumers.append(
                    {
                        "overlay_id": candidate.id,
                        "identifier": candidate.identifier,
                        "presentation_id": candidate.presentation_id,
                        "binding": candidate_binding,
                    }
                )
    return consumers


def shared_binding_impact(index: PresentationLayoutIndex, overlay: Overlay, *, include_size: bool) -> list[dict[str, Any]]:
    fields = [("position_x", overlay.position_x), ("position_y", overlay.position_y)]
    if include_size:
        fields.extend((("size_x", overlay.size_x), ("size_y", overlay.size_y)))
    impacts = []
    for binding, component in fields:
        consumers = shared_binding_consumers(index, overlay, component, binding=binding)
        if consumers:
            impacts.append({"edited_binding": binding, "shared_consumers": consumers})
    return impacts


def semantic_edits(
    index: PresentationLayoutIndex,
    target: str,
    *,
    action: str,
    x: float | int | None = None,
    y: float | int | None = None,
    value: str | None = None,
    alignment: str | None = None,
    new_overlay: dict[str, Any] | None = None,
    new_trigger: dict[str, Any] | None = None,
    trigger: str = "ti_on_presentation_load",
) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    if action not in VALID_ACTIONS:
        raise PresentationLayoutError("action must be one of: " + ", ".join(sorted(VALID_ACTIONS)))
    if action == "add_overlay":
        presentation = resolve_presentation(index, target)
        block = find_trigger(presentation, trigger)
        document = index.documents[presentation.path]
        rendered = render_new_overlay(new_overlay or {}, line_indent(document.raw, block.list_start) + "    ")
        return presentation.target_id, [append_operations(document, block, rendered)], {"action": action, "presentation_key": presentation.key, "trigger": trigger}
    if action == "add_trigger":
        presentation = resolve_presentation(index, target)
        event = validate_trigger_event(str((new_trigger or {}).get("event", "")), name="new_trigger.event")
        if any(block.name == event for block in presentation.triggers):
            raise PresentationLayoutError(f"Presentation {presentation.id!r} already has a {event} trigger; use replace_trigger_operations instead.")
        document = index.documents[presentation.path]
        return presentation.target_id, [append_trigger(document, presentation, render_trigger(new_trigger or {}))], {"action": action, "presentation_key": presentation.key, "event": event}
    if action in {"remove_trigger", "replace_trigger_operations"}:
        presentation = resolve_presentation(index, target)
        block = find_trigger(presentation, trigger)
        document = index.documents[presentation.path]
        if action == "remove_trigger":
            remove_start, remove_end = operation_with_separator(document, block.start, block.end)
            return presentation.target_id, [occurrence_edit(document.raw, remove_start, remove_end, "")], {"action": action, "presentation_key": presentation.key, "trigger": trigger}
        replacement = validate_operation_list(value or "", name="value")
        return presentation.target_id, [occurrence_edit(document.raw, block.list_start, block.list_end, replacement)], {"action": action, "presentation_key": presentation.key, "trigger": trigger}
    overlay = require_overlay(index, target)
    document = index.documents[overlay.path]
    metadata: dict[str, Any] = {"action": action, "overlay_id": overlay.id}
    if action == "move_overlay":
        if x is None or y is None:
            raise PresentationLayoutError("move_overlay requires x and y.")
        return overlay.target_id, [component_edit(document, overlay.position_x, x, action=action), component_edit(document, overlay.position_y, y, action=action)], {
            **metadata,
            "shared_binding_impact": shared_binding_impact(index, overlay, include_size=False),
        }
    if action == "resize_overlay":
        if x is None or y is None:
            raise PresentationLayoutError("resize_overlay requires x and y engine-scale values.")
        return overlay.target_id, [component_edit(document, overlay.size_x, x, action=action), component_edit(document, overlay.size_y, y, action=action)], {
            **metadata,
            "shared_binding_impact": shared_binding_impact(index, overlay, include_size=True),
        }
    if action == "align_overlay":
        horizontal, vertical = alignment_coordinates(overlay, require_query(alignment or "", name="alignment"))
        edits = []
        if horizontal is not None:
            edits.append(component_edit(document, overlay.position_x, horizontal, action=action))
        if vertical is not None:
            edits.append(component_edit(document, overlay.position_y, vertical, action=action))
        return overlay.target_id, edits, {
            **metadata,
            "alignment": alignment,
            "anchor_semantics": "Sets the overlay's position anchor to the selected nominal grid edge/center; it does not infer text or mesh dimensions.",
            "shared_binding_impact": shared_binding_impact(index, overlay, include_size=False),
        }
    if action == "set_text":
        if overlay.kind not in TEXTUAL_KINDS or overlay.content_start is None or overlay.content_end is None:
            raise PresentationLayoutError("set_text requires a text/button-like overlay with a statically editable content expression.")
        return overlay.target_id, [occurrence_edit(document.raw, overlay.content_start, overlay.content_end, quoted(value or "", name="value"))], metadata
    if action == "set_mesh":
        if overlay.kind not in MESH_KINDS or overlay.content_start is None or overlay.content_end is None:
            raise PresentationLayoutError("set_mesh requires a mesh/image-like overlay with a statically editable mesh expression.")
        mesh = require_query(value or "", name="value")
        return overlay.target_id, [occurrence_edit(document.raw, overlay.content_start, overlay.content_end, quoted(mesh, name="value"))], metadata
    if action in {"set_color", "set_alpha"}:
        component = overlay.color if action == "set_color" else overlay.alpha
        if component.start is None or component.end is None:
            raise PresentationLayoutError(f"{action} requires an existing overlay_set_{'color' if action == 'set_color' else 'alpha'} operation for this overlay.")
        replacement = value or ""
        parse_expression(replacement, name="value")
        return overlay.target_id, [occurrence_edit(document.raw, component.start, component.end, replacement.strip())], metadata
    if action == "remove_overlay":
        unique_spans = sorted(set(overlay.operation_spans), reverse=True)
        if not unique_spans:
            raise PresentationLayoutError("The overlay has no removable direct operations.")
        edits = []
        for start, end in unique_spans:
            remove_start, remove_end = operation_with_separator(document, start, end)
            edits.append(occurrence_edit(document.raw, remove_start, remove_end, ""))
        return overlay.target_id, edits, {**metadata, "removed_operation_count": len(edits), "preserved_position_register_writes": True}
    raise PresentationLayoutError(f"Unhandled presentation action: {action}")


def presentation_patch(
    index: PresentationLayoutIndex,
    target: str,
    *,
    action: str,
    x: float | int | None = None,
    y: float | int | None = None,
    value: str | None = None,
    alignment: str | None = None,
    new_overlay: dict[str, Any] | None = None,
    new_trigger: dict[str, Any] | None = None,
    trigger: str = "ti_on_presentation_load",
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    target_id, edits, semantic = semantic_edits(index, target, action=action, x=x, y=y, value=value, alignment=alignment, new_overlay=new_overlay, new_trigger=new_trigger, trigger=trigger)
    plan = change_router.patch_plan(index.router, target_id, edits, expected_sha256=expected_sha256)
    presentation = (
        resolve_presentation(index, target)
        if action in {"add_overlay", "add_trigger", "remove_trigger", "replace_trigger_operations"}
        else index.by_key[require_overlay(index, target).presentation_key]
    )
    return {
        "semantic_operation": semantic,
        "presentation": presentation_payload(presentation),
        "change_router_plan": plan,
        "static_canvas": presentation_canvas(index, presentation.key),
        "apply_contract": {"tool": "presentation_apply", "target": target, "action": action, "required_expected_sha256": plan["target"]["base_sha256"], "dry_run_default": True, "guarantees": plan["apply_contract"]["guarantees"]},
        "warnings": [
            "Review the unified diff and static canvas findings before a non-dry-run apply.",
            *(
                ["One or more edited position/size expressions are shared by other overlays; the plan names every static consumer in semantic_operation.shared_binding_impact."]
                if semantic.get("shared_binding_impact")
                else []
            ),
        ],
    }


def presentation_apply(
    index: PresentationLayoutIndex,
    target: str,
    *,
    action: str,
    expected_sha256: str,
    dry_run: bool = True,
    x: float | int | None = None,
    y: float | int | None = None,
    value: str | None = None,
    alignment: str | None = None,
    new_overlay: dict[str, Any] | None = None,
    new_trigger: dict[str, Any] | None = None,
    trigger: str = "ti_on_presentation_load",
) -> dict[str, Any]:
    target_id, edits, semantic = semantic_edits(index, target, action=action, x=x, y=y, value=value, alignment=alignment, new_overlay=new_overlay, new_trigger=new_trigger, trigger=trigger)
    result = change_router.apply_source_edits(index.router, target_id, edits, expected_sha256=expected_sha256, dry_run=dry_run)
    if not dry_run:
        invalidate_layout(index.root)
    return {
        "semantic_operation": semantic,
        "result": result,
        "warnings": [
            *result["warnings"],
            "Only source was changed; generated presentations and exports remain untouched until an intentional reviewed build.",
            *(
                ["The edited source expressions are shared by additional static overlays; inspect semantic_operation.shared_binding_impact."]
                if semantic.get("shared_binding_impact")
                else []
            ),
        ],
    }


def presentation_verify(
    index: PresentationLayoutIndex,
    target: str,
    *,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    if target.startswith("overlay:"):
        presentation = index.by_key[require_overlay(index, target).presentation_key]
    else:
        presentation = resolve_presentation(index, target)
    verification = change_router.verify_change(index.router, presentation.target_id, expected_sha256=expected_sha256, run_tests=run_tests, stage_build_check=stage_build_check, max_tests=max_tests, timeout_seconds=timeout_seconds)
    return {"presentation": presentation_payload(presentation), "static_canvas": presentation_canvas(index, presentation.key), "change_router_verification": verification, "warnings": [*verification["warnings"], "Static layout verification cannot prove runtime engine layout, variable text size, or conditional control flow."]}


def write_payload(payload: dict[str, Any], output: str | None, root: Path) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output:
        path = change_router.output_path(output, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def parse_json_argument(value: str | None, *, name: str) -> dict[str, Any] | None:
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise PresentationLayoutError(f"{name} must be JSON: {error}") from error
    if not isinstance(parsed, dict):
        raise PresentationLayoutError(f"{name} must decode to an object.")
    return parsed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static canvas and semantic editing for SoD Modern presentations.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    summary = subparsers.add_parser("summary")
    summary.add_argument("--output")
    find = subparsers.add_parser("find")
    find.add_argument("query")
    find.add_argument("--limit", type=int, default=20)
    find.add_argument("--output")
    canvas = subparsers.add_parser("canvas")
    canvas.add_argument("presentation_id")
    canvas.add_argument("--width", type=int, default=1024)
    canvas.add_argument("--height", type=int, default=768)
    canvas.add_argument("--overlay-limit", type=int, default=200)
    canvas.add_argument("--output")
    preview = subparsers.add_parser("preview")
    preview.add_argument("presentation_id")
    preview.add_argument("--output-name")
    preview.add_argument("--width", type=int, default=1024)
    preview.add_argument("--height", type=int, default=768)
    preview.add_argument("--output")
    for name in ("patch", "apply"):
        command = subparsers.add_parser(name)
        command.add_argument("target")
        command.add_argument("action", choices=sorted(VALID_ACTIONS))
        command.add_argument("--x", type=float)
        command.add_argument("--y", type=float)
        command.add_argument("--value")
        command.add_argument("--alignment")
        command.add_argument("--new-overlay")
        command.add_argument("--new-trigger")
        command.add_argument("--trigger", default="ti_on_presentation_load")
        command.add_argument("--expected-sha256")
        command.add_argument("--output")
        if name == "apply":
            command.add_argument("--apply", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("target")
    verify.add_argument("--expected-sha256")
    verify.add_argument("--run-tests", action="store_true")
    verify.add_argument("--stage-build", action="store_true")
    verify.add_argument("--max-tests", type=int, default=3)
    verify.add_argument("--timeout-seconds", type=int, default=90)
    verify.add_argument("--output")
    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        index = build_presentation_layout(args.root)
        if command == "summary":
            payload = presentation_summary(index)
        elif command == "find":
            payload = presentation_find(index, query=args.query, limit=args.limit)
        elif command == "canvas":
            payload = presentation_canvas(index, args.presentation_id, width=args.width, height=args.height, overlay_limit=args.overlay_limit)
        elif command == "preview":
            payload = presentation_preview(index, args.presentation_id, output_name=args.output_name, width=args.width, height=args.height)
        elif command == "patch":
            payload = presentation_patch(index, args.target, action=args.action, x=args.x, y=args.y, value=args.value, alignment=args.alignment, new_overlay=parse_json_argument(args.new_overlay, name="new_overlay"), new_trigger=parse_json_argument(args.new_trigger, name="new_trigger"), trigger=args.trigger, expected_sha256=args.expected_sha256)
        elif command == "apply":
            if not args.expected_sha256:
                raise PresentationLayoutError("apply requires --expected-sha256 from a presentation patch plan.")
            payload = presentation_apply(index, args.target, action=args.action, expected_sha256=args.expected_sha256, dry_run=not args.apply, x=args.x, y=args.y, value=args.value, alignment=args.alignment, new_overlay=parse_json_argument(args.new_overlay, name="new_overlay"), new_trigger=parse_json_argument(args.new_trigger, name="new_trigger"), trigger=args.trigger)
        elif command == "verify":
            payload = presentation_verify(index, args.target, expected_sha256=args.expected_sha256, run_tests=args.run_tests, stage_build_check=args.stage_build, max_tests=args.max_tests, timeout_seconds=args.timeout_seconds)
        else:
            raise PresentationLayoutError(f"Unknown command: {command}")
        write_payload(payload, getattr(args, "output", None), index.root)
        return 0
    except (PresentationLayoutError, change_router.ChangeRouterError) as error:
        parser.error(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
