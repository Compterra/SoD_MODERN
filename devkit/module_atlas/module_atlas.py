#!/usr/bin/env python3
"""The SoD Modern Module Atlas.

This is the control plane for the complete Mount & Blade 1.011 module-system
surface.  It turns the eight modular source areas into one static semantic
index while deliberately preserving their engine-specific shapes:

* constants are named assignments;
* dialogues are first-match routes (the Dialogue Composer remains authoritative);
* menus own enter operations and selectable options;
* mission templates own timed/event trigger blocks;
* presentations are delegated to the Presentation Layout Composer;
* quests are structured data records;
* scripts are callable operation blocks; and
* simple triggers are interval/event operation blocks.

The Atlas is not a generic file editor.  Semantic actions compile into exact
Change Router anchors, and every real write goes through its existing
source-only, SHA-guarded, dry-run-by-default gate.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.change_router import change_router


ATLAS_VERSION = "0.2.0"
MAX_QUERY_LENGTH = 500
MAX_TEXT_LENGTH = 30_000
MAX_RESULT_LIMIT = 500
SOURCE_AREAS = tuple(sorted(change_router.SOURCE_AREAS))
ASSIGNMENTS_BY_AREA = {
    "dialogs": "DIALOGS",
    "menus": "MENUS",
    "mission_templates": "MISSION_TEMPLATES",
    "presentations": "PRESENTATIONS",
    "quests": "QUESTS",
    "scripts": "SCRIPTS",
    "triggers": "SIMPLE_TRIGGERS",
}
FIELD_NAMES = {
    "dialogue_route": ("speaker", "input_state", "conditions", "text", "output_state", "consequences"),
    "menu": ("id", "flags", "text", "mesh", "on_enter", "options"),
    "menu_option": ("id", "conditions", "text", "consequences"),
    "mission_template": ("id", "flags", "scene", "description", "spawn_records", "triggers"),
    "mission_trigger": ("event", "interval", "repeat", "conditions", "consequences"),
    "presentation": ("id", "flags", "mesh", "triggers"),
    "quest": ("id", "title", "flags", "description"),
    "script": ("id", "operations"),
    "simple_trigger": ("interval", "operations"),
    "constant": ("name", "value"),
}
AREA_PRIMARY_TOOLS = {
    "constants": "entity_references / module_patch",
    "dialogs": "dialogue_find / dialogue_context / dialogue_patch",
    "menus": "menu_flow / module_patch",
    "mission_templates": "mission_timeline / module_patch",
    "presentations": "presentation_find / presentation_canvas / presentation_patch",
    "quests": "quest_registry / module_patch",
    "scripts": "script_flow / module_patch",
    "triggers": "trigger_timeline / module_patch",
}
PREFIX_BY_KIND = {
    "menu": "mnu_",
    "mission_template": "mt_",
    "presentation": "prsnt_",
    "quest": "qst_",
    "script": "script_",
}
VALID_ACTIONS = frozenset(
    {
        "set_text",
        "set_expression",
        "replace_operations",
        "insert_operation",
        "remove_operation",
        "add_constant",
        "add_quest",
        "add_script",
        "add_menu",
        "add_menu_option",
        "add_mission_template",
        "remove_menu_option",
        "add_mission_trigger",
        "remove_mission_trigger",
        "set_trigger_interval",
        "add_simple_trigger",
        "remove_entity",
    }
)
REFERENCE_PREFIX_RE = re.compile(
    r"^(?:script_|mnu_|mt_|prsnt_|qst_|str_|trp_|pt_|fac_|itm_|slot_|sod_)"
)
KNOWN_ENTITY_REFERENCE_PREFIXES = ("script_", "mnu_", "mt_", "prsnt_", "qst_")
TEXT_FIELDS_BY_KIND = {
    "menu": frozenset({"text"}),
    "menu_option": frozenset({"text"}),
    "quest": frozenset({"title", "description"}),
}
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ModuleAtlasError(RuntimeError):
    """A module-system semantic request cannot be safely performed."""


@dataclass(frozen=True)
class SourceDocument:
    path: str
    raw: str
    encoding: str
    offsets: tuple[int, ...]


@dataclass(frozen=True)
class FieldAnchor:
    name: str
    index: int
    start: int
    end: int
    source: str
    value: str


@dataclass(frozen=True)
class OperationAnchor:
    index: int
    name: str
    line: int
    start: int
    end: int
    source: str
    arguments: tuple[str, ...]
    symbols: tuple[str, ...]


@dataclass(frozen=True)
class OperationBlock:
    name: str
    field_index: int
    line: int
    start: int
    end: int
    operations: tuple[OperationAnchor, ...]


@dataclass(frozen=True)
class ModuleEntity:
    id: str
    target_id: str
    area: str
    kind: str
    name: str
    aliases: tuple[str, ...]
    path: str
    line: int
    column: int
    source_order: int | None
    parent_id: str | None
    entry_start: int
    entry_end: int
    entry_source: str
    container_start: int
    container_end: int
    fields: tuple[FieldAnchor, ...]
    blocks: tuple[OperationBlock, ...]
    symbols: tuple[str, ...]


@dataclass(frozen=True)
class AtlasEdge:
    source_id: str
    target_id: str
    reference: str
    relation: str


@dataclass
class ModuleAtlasIndex:
    root: Path
    router: change_router.RouterIndex
    documents: dict[str, SourceDocument]
    entities: tuple[ModuleEntity, ...]
    by_id: dict[str, ModuleEntity]
    by_target: dict[str, tuple[ModuleEntity, ...]]
    by_alias: dict[str, tuple[ModuleEntity, ...]]
    engine_id_aliases: frozenset[str]
    edges: tuple[AtlasEdge, ...]
    outgoing: dict[str, tuple[AtlasEdge, ...]]
    incoming: dict[str, tuple[AtlasEdge, ...]]


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], ModuleAtlasIndex]] = {}


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
        raise ModuleAtlasError("A module entity is missing exact source positions.")
    start_line, end_line, start_column, end_column = values
    if start_line < 1 or end_line < start_line or start_line > len(offsets) or end_line > len(offsets):
        raise ModuleAtlasError("A module entity has an invalid source span.")
    return offsets[start_line - 1] + start_column, offsets[end_line - 1] + end_column


def node_source(raw: str, node: ast.AST, offsets: Sequence[int]) -> str:
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


def operation_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Tuple) and node.elts:
        return expression_symbol(node.elts[0])
    if isinstance(node, ast.Name):
        return node.id
    return None


def operation_arguments(node: ast.AST) -> list[ast.AST]:
    return list(node.elts[1:]) if isinstance(node, ast.Tuple) else []


def ast_symbols(node: ast.AST) -> set[str]:
    """Keep symbolic engine references without evaluating legacy module code."""

    result: set[str] = set()
    for item in ast.walk(node):
        if isinstance(item, ast.Name):
            result.add(item.id)
        elif isinstance(item, ast.Constant) and isinstance(item.value, str):
            value = item.value
            if REFERENCE_PREFIX_RE.match(value):
                result.add(value)
    return result


def relation_for_reference(reference: str) -> str:
    if reference.startswith("script_"):
        return "calls_script"
    if reference.startswith("mnu_"):
        return "jumps_to_menu"
    if reference.startswith("mt_"):
        return "starts_mission"
    if reference.startswith("prsnt_"):
        return "starts_presentation"
    if reference.startswith("qst_"):
        return "uses_quest"
    if reference.startswith("str_"):
        return "uses_string"
    return "uses_symbol"


def source_document(router: change_router.RouterIndex, relative: str) -> SourceDocument:
    fragment = router.fragments[relative]
    raw, encoding, _ = change_router.read_text_with_encoding(change_router.source_path(router, fragment))
    return SourceDocument(relative, raw, encoding, line_offsets(raw))


def find_assignment(tree: ast.Module, name: str) -> ast.List | None:
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == name for target in statement.targets):
            continue
        if isinstance(statement.value, ast.List):
            return statement.value
        raise ModuleAtlasError(f"{name} must be assigned a list literal.")
    return None


def make_field(document: SourceDocument, index: int, name: str, node: ast.AST) -> FieldAnchor:
    start, end = node_bounds(node, document.offsets)
    return FieldAnchor(
        name=name,
        index=index,
        start=start,
        end=end,
        source=document.raw[start:end],
        value=literal_string(node),
    )


def make_operation_block(
    document: SourceDocument,
    *,
    name: str,
    field_index: int,
    node: ast.AST,
) -> OperationBlock | None:
    if not isinstance(node, ast.List):
        return None
    start, end = node_bounds(node, document.offsets)
    operations: list[OperationAnchor] = []
    for index, item in enumerate(node.elts):
        operation = operation_name(item)
        if operation is None:
            continue
        operation_start, operation_end = node_bounds(item, document.offsets)
        operations.append(
            OperationAnchor(
                index=index,
                name=operation,
                line=getattr(item, "lineno", 0),
                start=operation_start,
                end=operation_end,
                source=document.raw[operation_start:operation_end],
                arguments=tuple(expression_symbol(argument) for argument in operation_arguments(item)),
                symbols=tuple(sorted(ast_symbols(item))),
            )
        )
    return OperationBlock(
        name=name,
        field_index=field_index,
        line=getattr(node, "lineno", 0),
        start=start,
        end=end,
        operations=tuple(operations),
    )


def aliases_for(kind: str, name: str) -> tuple[str, ...]:
    aliases = {name}
    prefix = PREFIX_BY_KIND.get(kind)
    if prefix and name and not name.startswith(prefix):
        aliases.add(prefix + name)
    return tuple(sorted(alias for alias in aliases if alias))


def entity_id(area: str, kind: str, path: str, node: ast.AST) -> str:
    return f"module:{area}:{kind}:{path}:L{getattr(node, 'lineno', 0)}:C{getattr(node, 'col_offset', 0)}"


def field_name(kind: str, index: int) -> str:
    names = FIELD_NAMES.get(kind, ())
    return names[index] if index < len(names) else f"field_{index}"


def make_entity(
    router: change_router.RouterIndex,
    document: SourceDocument,
    *,
    area: str,
    kind: str,
    node: ast.AST,
    name: str,
    parent_id: str | None,
    container_start: int,
    container_end: int,
    blocks: Iterable[OperationBlock] = (),
) -> ModuleEntity:
    fragment = router.fragments[document.path]
    start, end = node_bounds(node, document.offsets)
    elements = list(node.elts) if isinstance(node, (ast.List, ast.Tuple)) else []
    fields = tuple(make_field(document, index, field_name(kind, index), field) for index, field in enumerate(elements))
    return ModuleEntity(
        id=entity_id(area, kind, document.path, node),
        target_id=fragment.id,
        area=area,
        kind=kind,
        name=name,
        aliases=aliases_for(kind, name),
        path=document.path,
        line=getattr(node, "lineno", 0),
        column=getattr(node, "col_offset", 0),
        source_order=fragment.order_position,
        parent_id=parent_id,
        entry_start=start,
        entry_end=end,
        entry_source=document.raw[start:end],
        container_start=container_start,
        container_end=container_end,
        fields=fields,
        blocks=tuple(blocks),
        symbols=tuple(sorted(ast_symbols(node))),
    )


def entity_sort_key(entity: ModuleEntity) -> tuple[int, str, int, int, str]:
    return (
        entity.source_order if entity.source_order is not None else 1_000_000,
        entity.path.casefold(),
        entity.line,
        entity.column,
        entity.id,
    )


def list_field(entry: ast.AST, index: int) -> ast.AST | None:
    if not isinstance(entry, (ast.List, ast.Tuple)) or index >= len(entry.elts):
        return None
    return entry.elts[index]


def parse_dialogue_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for ordinal, entry in enumerate(assignment.elts, start=1):
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 6:
            continue
        input_state = literal_string(entry.elts[1])
        blocks = [
            block
            for block in (
                make_operation_block(document, name="conditions", field_index=2, node=entry.elts[2]),
                make_operation_block(document, name="consequences", field_index=5, node=entry.elts[5]),
            )
            if block is not None
        ]
        entities.append(
            make_entity(
                router,
                document,
                area="dialogs",
                kind="dialogue_route",
                node=entry,
                name=f"{input_state}:{ordinal}",
                parent_id=None,
                container_start=container_start,
                container_end=container_end,
                blocks=blocks,
            )
        )
    return entities


def parse_menu_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for entry in assignment.elts:
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 6:
            continue
        name = literal_string(entry.elts[0])
        on_enter = make_operation_block(document, name="on_enter", field_index=4, node=entry.elts[4])
        menu = make_entity(
            router,
            document,
            area="menus",
            kind="menu",
            node=entry,
            name=name,
            parent_id=None,
            container_start=container_start,
            container_end=container_end,
            blocks=() if on_enter is None else (on_enter,),
        )
        entities.append(menu)
        options = list_field(entry, 5)
        if not isinstance(options, ast.List):
            continue
        option_start, option_end = node_bounds(options, document.offsets)
        for ordinal, option in enumerate(options.elts, start=1):
            if not isinstance(option, (ast.List, ast.Tuple)) or len(option.elts) < 4:
                continue
            option_id = literal_string(option.elts[0])
            blocks = [
                block
                for block in (
                    make_operation_block(document, name="conditions", field_index=1, node=option.elts[1]),
                    make_operation_block(document, name="consequences", field_index=3, node=option.elts[3]),
                )
                if block is not None
            ]
            entities.append(
                make_entity(
                    router,
                    document,
                    area="menus",
                    kind="menu_option",
                    node=option,
                    name=f"{name}:{option_id or ordinal}",
                    parent_id=menu.id,
                    container_start=option_start,
                    container_end=option_end,
                    blocks=blocks,
                )
            )
    return entities


def parse_mission_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for entry in assignment.elts:
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 6:
            continue
        name = literal_string(entry.elts[0])
        triggers = entry.elts[-1]
        mission = make_entity(
            router,
            document,
            area="mission_templates",
            kind="mission_template",
            node=entry,
            name=name,
            parent_id=None,
            container_start=container_start,
            container_end=container_end,
        )
        entities.append(mission)
        if not isinstance(triggers, ast.List):
            continue
        trigger_start, trigger_end = node_bounds(triggers, document.offsets)
        for ordinal, trigger in enumerate(triggers.elts, start=1):
            if not isinstance(trigger, (ast.List, ast.Tuple)) or len(trigger.elts) < 5:
                continue
            event = expression_symbol(trigger.elts[0])
            blocks = [
                block
                for block in (
                    make_operation_block(document, name="conditions", field_index=3, node=trigger.elts[3]),
                    make_operation_block(document, name="consequences", field_index=4, node=trigger.elts[4]),
                )
                if block is not None
            ]
            entities.append(
                make_entity(
                    router,
                    document,
                    area="mission_templates",
                    kind="mission_trigger",
                    node=trigger,
                    name=f"{name}:{event}:{ordinal}",
                    parent_id=mission.id,
                    container_start=trigger_start,
                    container_end=trigger_end,
                    blocks=blocks,
                )
            )
    return entities


def parse_presentation_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for entry in assignment.elts:
        if not isinstance(entry, (ast.List, ast.Tuple)) or not entry.elts:
            continue
        name = literal_string(entry.elts[0])
        entities.append(
            make_entity(
                router,
                document,
                area="presentations",
                kind="presentation",
                node=entry,
                name=name,
                parent_id=None,
                container_start=container_start,
                container_end=container_end,
            )
        )
    return entities


def parse_quest_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for entry in assignment.elts:
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 4:
            continue
        entities.append(
            make_entity(
                router,
                document,
                area="quests",
                kind="quest",
                node=entry,
                name=literal_string(entry.elts[0]),
                parent_id=None,
                container_start=container_start,
                container_end=container_end,
            )
        )
    return entities


def parse_script_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for entry in assignment.elts:
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 2:
            continue
        operations = make_operation_block(document, name="operations", field_index=1, node=entry.elts[1])
        entities.append(
            make_entity(
                router,
                document,
                area="scripts",
                kind="script",
                node=entry,
                name=literal_string(entry.elts[0]),
                parent_id=None,
                container_start=container_start,
                container_end=container_end,
                blocks=() if operations is None else (operations,),
            )
        )
    return entities


def parse_simple_trigger_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    assignment: ast.List,
) -> list[ModuleEntity]:
    container_start, container_end = node_bounds(assignment, document.offsets)
    entities: list[ModuleEntity] = []
    for ordinal, entry in enumerate(assignment.elts, start=1):
        if not isinstance(entry, (ast.List, ast.Tuple)) or len(entry.elts) < 2:
            continue
        operations = make_operation_block(document, name="operations", field_index=1, node=entry.elts[1])
        entities.append(
            make_entity(
                router,
                document,
                area="triggers",
                kind="simple_trigger",
                node=entry,
                name=f"{document.path}:trigger:{ordinal}",
                parent_id=None,
                container_start=container_start,
                container_end=container_end,
                blocks=() if operations is None else (operations,),
            )
        )
    return entities


def parse_constant_entities(
    router: change_router.RouterIndex,
    document: SourceDocument,
    tree: ast.Module,
) -> list[ModuleEntity]:
    fragment = router.fragments[document.path]
    entities: list[ModuleEntity] = []
    for statement in tree.body:
        targets: list[ast.Name] = []
        value: ast.AST | None = None
        if isinstance(statement, ast.Assign):
            targets = [target for target in statement.targets if isinstance(target, ast.Name)]
            value = statement.value
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            targets = [statement.target]
            value = statement.value
        if value is None:
            continue
        statement_start, statement_end = node_bounds(statement, document.offsets)
        value_start, value_end = node_bounds(value, document.offsets)
        for target in targets:
            target_start, target_end = node_bounds(target, document.offsets)
            name = target.id
            entities.append(
                ModuleEntity(
                    id=f"module:constants:constant:{document.path}:L{getattr(target, 'lineno', 0)}:C{getattr(target, 'col_offset', 0)}:{name}",
                    target_id=fragment.id,
                    area="constants",
                    kind="constant",
                    name=name,
                    aliases=(name,),
                    path=document.path,
                    line=getattr(target, "lineno", 0),
                    column=getattr(target, "col_offset", 0),
                    source_order=fragment.order_position,
                    parent_id=None,
                    entry_start=statement_start,
                    entry_end=statement_end,
                    entry_source=document.raw[statement_start:statement_end],
                    container_start=statement_start,
                    container_end=statement_end,
                    fields=(
                        FieldAnchor("name", 0, target_start, target_end, document.raw[target_start:target_end], name),
                        FieldAnchor("value", 1, value_start, value_end, document.raw[value_start:value_end], expression_text(value)),
                    ),
                    blocks=(),
                    symbols=tuple(sorted(ast_symbols(value))),
                )
            )
    return entities


def parse_area_document(
    router: change_router.RouterIndex,
    document: SourceDocument,
    area: str,
) -> list[ModuleEntity]:
    try:
        tree = ast.parse(document.raw, filename=str(router.root / document.path))
    except SyntaxError as error:
        raise ModuleAtlasError(f"Cannot parse {document.path} at line {error.lineno}: {error.msg}") from error
    if area == "constants":
        return parse_constant_entities(router, document, tree)
    assignment_name = ASSIGNMENTS_BY_AREA.get(area)
    if assignment_name is None:
        return []
    assignment = find_assignment(tree, assignment_name)
    if assignment is None:
        return []
    parsers = {
        "dialogs": parse_dialogue_entities,
        "menus": parse_menu_entities,
        "mission_templates": parse_mission_entities,
        "presentations": parse_presentation_entities,
        "quests": parse_quest_entities,
        "scripts": parse_script_entities,
        "triggers": parse_simple_trigger_entities,
    }
    return parsers[area](router, document, assignment)


def area_paths(router: change_router.RouterIndex, area: str) -> list[str]:
    ordered = [
        path
        for path in router.ordering.get(area, [])
        if path in router.fragments and router.fragments[path].area == area
    ]
    listed = set(ordered)
    remaining = sorted(
        (
            path
            for path, fragment in router.fragments.items()
            if fragment.area == area and path not in listed
        ),
        key=str.lower,
    )
    return [*ordered, *remaining]


def generated_engine_id_aliases(root: Path) -> frozenset[str]:
    """Read generated ID declarations as static fallback definitions.

    The modular slice intentionally owns only the source areas under `src/`.
    Native/base-module IDs can therefore be valid references even when their
    authored record does not appear in the Atlas.  Reading generated IDs lets
    integrity distinguish that normal legacy boundary from an actually missing
    direct script/menu/mission/presentation/quest reference.
    """

    aliases: set[str] = set()
    ids_root = root / "compile" / "ids"
    if not ids_root.is_dir():
        return frozenset()
    for path in sorted(ids_root.glob("ID_*.py"), key=lambda candidate: candidate.name.casefold()):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        for statement in tree.body:
            if not isinstance(statement, ast.Assign):
                continue
            for target in statement.targets:
                if not isinstance(target, ast.Name):
                    continue
                name = target.id
                aliases.add(name)
                if name.startswith("menu_"):
                    aliases.add("mnu_" + name.removeprefix("menu_"))
                elif name.startswith("mst_"):
                    aliases.add("mt_" + name.removeprefix("mst_"))
    return frozenset(aliases)


def build_module_atlas(root: Path = DEFAULT_REPO_ROOT) -> ModuleAtlasIndex:
    """Index every modular source area without importing legacy module code."""

    root = root.resolve()
    router = change_router.build_change_router(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == router.signature:
        return cached[1]
    documents: dict[str, SourceDocument] = {}
    entities: list[ModuleEntity] = []
    for area in SOURCE_AREAS:
        for relative in area_paths(router, area):
            fragment = router.fragments[relative]
            if fragment.syntax_error is not None:
                continue
            document = source_document(router, relative)
            documents[relative] = document
            entities.extend(parse_area_document(router, document, area))
    entities.sort(key=entity_sort_key)
    by_target_raw: dict[str, list[ModuleEntity]] = defaultdict(list)
    by_alias_raw: dict[str, list[ModuleEntity]] = defaultdict(list)
    for entity in entities:
        by_target_raw[entity.target_id].append(entity)
        for alias in entity.aliases:
            by_alias_raw[alias].append(entity)
    by_alias = {
        alias: tuple(sorted(values, key=entity_sort_key))
        for alias, values in by_alias_raw.items()
    }
    edge_set: set[tuple[str, str, str, str]] = set()
    for entity in entities:
        for symbol in entity.symbols:
            for target in by_alias.get(symbol, ()):
                if target.id == entity.id:
                    continue
                edge_set.add((entity.id, target.id, symbol, relation_for_reference(symbol)))
    edges = tuple(
        AtlasEdge(source_id, target_id, reference, relation)
        for source_id, target_id, reference, relation in sorted(edge_set)
    )
    outgoing_raw: dict[str, list[AtlasEdge]] = defaultdict(list)
    incoming_raw: dict[str, list[AtlasEdge]] = defaultdict(list)
    for edge in edges:
        outgoing_raw[edge.source_id].append(edge)
        incoming_raw[edge.target_id].append(edge)
    index = ModuleAtlasIndex(
        root=root,
        router=router,
        documents=documents,
        entities=tuple(entities),
        by_id={entity.id: entity for entity in entities},
        by_target={target: tuple(sorted(values, key=entity_sort_key)) for target, values in by_target_raw.items()},
        by_alias=by_alias,
        engine_id_aliases=generated_engine_id_aliases(root),
        edges=edges,
        outgoing={key: tuple(value) for key, value in outgoing_raw.items()},
        incoming={key: tuple(value) for key, value in incoming_raw.items()},
    )
    _CACHE[root] = (router.signature, index)
    return index


def invalidate_atlas(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def compact(value: str, maximum: int = 280) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip()
    return cleaned if len(cleaned) <= maximum else cleaned[: maximum - 3] + "..."


def field_payload(field: FieldAnchor) -> dict[str, Any]:
    return {
        "name": field.name,
        "index": field.index,
        "value": compact(field.value),
        "source": compact(field.source),
        "line": None,
    }


def block_payload(block: OperationBlock, *, operation_limit: int = 40) -> dict[str, Any]:
    operations = block.operations[:operation_limit]
    return {
        "name": block.name,
        "field_index": block.field_index,
        "line": block.line,
        "operation_count": len(block.operations),
        "returned_operation_count": len(operations),
        "operations_truncated": len(block.operations) > len(operations),
        "operations": [
            {
                "index": operation.index,
                "name": operation.name,
                "line": operation.line,
                "arguments": list(operation.arguments),
                "symbols": list(operation.symbols),
                "source": compact(operation.source),
            }
            for operation in operations
        ],
    }


def generated_payload(index: ModuleAtlasIndex, entity: ModuleEntity) -> list[dict[str, Any]]:
    return [
        {
            "compile_path": segment.compile_path,
            "compile_line_start": segment.compile_line_start,
            "compile_line_end": segment.compile_line_end,
            "source_line_start": segment.source_line_start,
            "source_line_end": segment.source_line_end,
        }
        for segment in index.router.generated_by_source.get(entity.path, [])
    ]


def entity_payload(
    index: ModuleAtlasIndex,
    entity: ModuleEntity,
    *,
    include_fields: bool = True,
    block_operation_limit: int = 40,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "entity_id": entity.id,
        "target_id": entity.target_id,
        "area": entity.area,
        "kind": entity.kind,
        "name": entity.name,
        "aliases": list(entity.aliases),
        "parent_id": entity.parent_id,
        "source": {
            "path": entity.path,
            "line": entity.line,
            "column": entity.column,
            "section_order": entity.source_order,
        },
        "symbol_count": len(entity.symbols),
        "symbols": list(entity.symbols[:100]),
        "symbols_truncated": len(entity.symbols) > 100,
        "block_count": len(entity.blocks),
        "blocks": [block_payload(block, operation_limit=block_operation_limit) for block in entity.blocks],
        "generated_links": generated_payload(index, entity),
    }
    if include_fields:
        result["fields"] = [field_payload(field) for field in entity.fields]
    return result


def require_query(value: str, *, name: str = "query") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ModuleAtlasError(f"{name} must not be empty.")
    if len(value) > MAX_QUERY_LENGTH:
        raise ModuleAtlasError(f"{name} must be at most {MAX_QUERY_LENGTH} characters.")
    return value.strip()


def require_limit(value: int, *, name: str = "limit", maximum: int = MAX_RESULT_LIMIT) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ModuleAtlasError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_area(value: str) -> str:
    if value not in {"all", *SOURCE_AREAS}:
        raise ModuleAtlasError("area must be 'all' or one of: " + ", ".join(SOURCE_AREAS))
    return value


def require_entity(index: ModuleAtlasIndex, entity_id: str) -> ModuleEntity:
    if not isinstance(entity_id, str) or not entity_id.startswith("module:"):
        raise ModuleAtlasError("entity_id must be a Module Atlas ID returned by module_find or a specialist view.")
    entity = index.by_id.get(entity_id)
    if entity is None:
        raise ModuleAtlasError("Unknown Module Atlas entity; refresh module_find before editing.")
    return entity


def entity_search_text(entity: ModuleEntity) -> str:
    return "\n".join(
        (
            entity.area,
            entity.kind,
            entity.name,
            *entity.aliases,
            entity.path,
            *(field.value for field in entity.fields),
            *(field.source for field in entity.fields),
            *entity.symbols,
        )
    ).casefold()


def module_summary(index: ModuleAtlasIndex) -> dict[str, Any]:
    by_area = Counter(entity.area for entity in index.entities)
    by_kind = Counter(entity.kind for entity in index.entities)
    return {
        "atlas_version": f"devkit.module-atlas.v{ATLAS_VERSION}",
        "source_area_count": len(SOURCE_AREAS),
        "entity_count": len(index.entities),
        "edge_count": len(index.edges),
        "generated_engine_id_alias_count": len(index.engine_id_aliases),
        "entity_count_by_area": dict(sorted(by_area.items())),
        "entity_count_by_kind": dict(sorted(by_kind.items())),
        "coverage": [
            {
                "area": area,
                "entity_count": by_area.get(area, 0),
                "generated_modules": list(change_router.GENERATED_BY_AREA.get(area, ())),
                "exports": list(change_router.EXPORTS_BY_AREA.get(area, ())),
                "primary_tools": AREA_PRIMARY_TOOLS[area],
            }
            for area in SOURCE_AREAS
        ],
        "warnings": [
            "The Atlas is static source/compile provenance, not a runtime simulator.",
            "Dialogue first-match behavior and presentation geometry have dedicated specialist composers; the Atlas routes to them rather than flattening their semantics.",
            "Every semantic apply delegates to the Change Router source-only SHA gate.",
        ],
    }


def module_integrity(index: ModuleAtlasIndex, *, limit: int = 100) -> dict[str, Any]:
    """Surface high-signal static structural risks across the whole module.

    This deliberately limits itself to references whose prefix maps to an Atlas
    entity kind.  Troops, items, parties, strings, and dynamically chosen IDs
    are not treated as missing definitions because they have distinct source
    systems or runtime resolution paths.
    """

    maximum = require_limit(limit)
    duplicate_definitions: list[dict[str, Any]] = []
    for alias, entities in sorted(index.by_alias.items(), key=lambda item: item[0].casefold()):
        kinds = {entity.kind for entity in entities}
        if len(entities) > 1 and len(kinds) == 1 and next(iter(kinds)) in PREFIX_BY_KIND:
            duplicate_definitions.append(
                {
                    "alias": alias,
                    "kind": next(iter(kinds)),
                    "definition_count": len(entities),
                    "definitions": [
                        {
                            "entity_id": entity.id,
                            "path": entity.path,
                            "line": entity.line,
                        }
                        for entity in entities
                    ],
                }
            )
    unresolved: list[dict[str, Any]] = []
    generated_fallbacks: list[dict[str, Any]] = []
    for entity in index.entities:
        direct_references = sorted(
            symbol
            for symbol in entity.symbols
            if symbol.startswith(KNOWN_ENTITY_REFERENCE_PREFIXES)
        )
        missing = [
            symbol
            for symbol in direct_references
            if not index.by_alias.get(symbol) and symbol not in index.engine_id_aliases
        ]
        if missing:
            unresolved.append(
                {
                    "entity_id": entity.id,
                    "area": entity.area,
                    "kind": entity.kind,
                    "name": entity.name,
                    "path": entity.path,
                    "line": entity.line,
                    "unresolved_references": missing,
                }
            )
        fallback_references = [
            symbol
            for symbol in direct_references
            if not index.by_alias.get(symbol) and symbol in index.engine_id_aliases
        ]
        if fallback_references:
            generated_fallbacks.append(
                {
                    "entity_id": entity.id,
                    "area": entity.area,
                    "kind": entity.kind,
                    "name": entity.name,
                    "path": entity.path,
                    "line": entity.line,
                    "generated_id_references": fallback_references,
                }
            )
    duplicate_definitions.sort(key=lambda item: (item["kind"], item["alias"].casefold()))
    unresolved.sort(key=lambda item: (item["path"].casefold(), item["line"], item["name"]))
    generated_fallbacks.sort(key=lambda item: (item["path"].casefold(), item["line"], item["name"]))
    syntax_errors = [
        {
            "path": fragment.path,
            "area": fragment.area,
            "error": fragment.syntax_error,
        }
        for fragment in sorted(index.router.fragments.values(), key=lambda fragment: fragment.path.casefold())
        if fragment.syntax_error
    ]
    finding_count = len(duplicate_definitions) + len(unresolved) + len(syntax_errors)
    return {
        "static_only": True,
        "finding_count": finding_count,
        "duplicate_definition_count": len(duplicate_definitions),
        "returned_duplicate_definition_count": min(len(duplicate_definitions), maximum),
        "duplicate_definitions_truncated": len(duplicate_definitions) > maximum,
        "duplicate_definitions": duplicate_definitions[:maximum],
        "unresolved_reference_entity_count": len(unresolved),
        "returned_unresolved_reference_entity_count": min(len(unresolved), maximum),
        "unresolved_references_truncated": len(unresolved) > maximum,
        "unresolved_references": unresolved[:maximum],
        "generated_id_fallback_entity_count": len(generated_fallbacks),
        "returned_generated_id_fallback_entity_count": min(len(generated_fallbacks), maximum),
        "generated_id_fallbacks_truncated": len(generated_fallbacks) > maximum,
        "generated_id_fallbacks": generated_fallbacks[:maximum],
        "syntax_error_count": len(syntax_errors),
        "syntax_errors": syntax_errors[:maximum],
        "warnings": [
            "Only direct script/menu/mission/presentation/quest identifiers are checked for unresolved references.",
            "Generated-ID fallbacks are valid known engine/base data but are outside the current modular Atlas ownership; they are reported separately, not as failures.",
            "Dynamic identifiers, string IDs, and non-Atlas engine data types remain explicit unknowns rather than false-positive failures.",
        ],
    }


def module_find(
    index: ModuleAtlasIndex,
    *,
    query: str | None = None,
    area: str = "all",
    kind: str | None = None,
    limit: int = 30,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    checked_area = require_area(area)
    needle = require_query(query).casefold() if query is not None else None
    if needle is None and kind is None and checked_area == "all":
        raise ModuleAtlasError("Specify query, area, or kind to keep the Atlas result bounded.")
    if kind is not None:
        kind = require_query(kind, name="kind")
    matches = []
    for entity in index.entities:
        if checked_area != "all" and entity.area != checked_area:
            continue
        if kind is not None and entity.kind != kind:
            continue
        if needle is not None and needle not in entity_search_text(entity):
            continue
        matches.append(entity)
    return {
        "summary": module_summary(index),
        "filters": {"query": query, "area": checked_area, "kind": kind},
        "match_count": len(matches),
        "returned_count": min(len(matches), maximum),
        "truncated": len(matches) > maximum,
        "entities": [entity_payload(index, entity, block_operation_limit=15) for entity in matches[:maximum]],
    }


def edge_payload(index: ModuleAtlasIndex, edge: AtlasEdge) -> dict[str, Any]:
    source = index.by_id[edge.source_id]
    target = index.by_id[edge.target_id]
    return {
        "source_id": edge.source_id,
        "source": {"name": source.name, "kind": source.kind, "path": source.path, "line": source.line},
        "target_id": edge.target_id,
        "target": {"name": target.name, "kind": target.kind, "path": target.path, "line": target.line},
        "reference": edge.reference,
        "relation": edge.relation,
    }


def supported_actions(entity: ModuleEntity) -> list[str]:
    if entity.area == "dialogs":
        return ["delegate_to_dialogue_composer"]
    if entity.area == "presentations":
        return ["delegate_to_presentation_layout_composer"]
    actions = ["set_expression"]
    if entity.kind in {"menu", "menu_option", "quest"}:
        actions.append("set_text")
    if entity.blocks:
        actions.extend(("replace_operations", "insert_operation", "remove_operation"))
    if entity.kind == "menu":
        actions.extend(("add_menu", "add_menu_option"))
    if entity.kind == "menu_option":
        actions.append("remove_menu_option")
    if entity.kind == "mission_template":
        actions.extend(("add_mission_template", "add_mission_trigger"))
    if entity.kind == "mission_trigger":
        actions.extend(("remove_mission_trigger", "set_trigger_interval"))
    if entity.kind == "simple_trigger":
        actions.extend(("add_simple_trigger", "set_trigger_interval", "remove_entity"))
    if entity.kind == "constant":
        return ["set_expression", "add_constant", "remove_entity"]
    if entity.kind == "quest":
        actions.extend(("add_quest", "remove_entity"))
    if entity.kind == "script":
        actions.extend(("add_script", "remove_entity"))
    if entity.kind in {"menu", "mission_template"}:
        actions.append("remove_entity")
    return sorted(dict.fromkeys(actions))


def module_context(
    index: ModuleAtlasIndex,
    entity_id: str,
    *,
    max_lines: int = 120,
    related_limit: int = 30,
) -> dict[str, Any]:
    entity = require_entity(index, entity_id)
    maximum_lines = require_limit(max_lines, name="max_lines", maximum=400)
    maximum_related = require_limit(related_limit, name="related_limit", maximum=100)
    router_context = change_router.linked_context(
        index.router,
        entity.target_id,
        focus_line=entity.line,
        max_lines=maximum_lines,
        related_limit=maximum_related,
    )
    outgoing = index.outgoing.get(entity.id, ())
    incoming = index.incoming.get(entity.id, ())
    children = [candidate for candidate in index.entities if candidate.parent_id == entity.id]
    return {
        "entity": entity_payload(index, entity),
        "semantic_actions": supported_actions(entity),
        "relationships": {
            "outbound_count": len(outgoing),
            "outbound": [edge_payload(index, edge) for edge in outgoing[:maximum_related]],
            "outbound_truncated": len(outgoing) > maximum_related,
            "inbound_count": len(incoming),
            "inbound": [edge_payload(index, edge) for edge in incoming[:maximum_related]],
            "inbound_truncated": len(incoming) > maximum_related,
            "child_count": len(children),
            "children": [entity_payload(index, child, include_fields=False, block_operation_limit=10) for child in children[:maximum_related]],
            "children_truncated": len(children) > maximum_related,
        },
        "source_context": router_context,
        "delegation": (
            "Use dialogue_context/dialogue_patch for exact route semantics."
            if entity.area == "dialogs"
            else "Use presentation_canvas/presentation_patch for overlay and trigger layout semantics."
            if entity.area == "presentations"
            else None
        ),
    }


def module_graph(
    index: ModuleAtlasIndex,
    entity_id: str,
    *,
    direction: str = "both",
    depth: int = 2,
    max_nodes: int = 100,
) -> dict[str, Any]:
    root = require_entity(index, entity_id)
    if direction not in {"outgoing", "incoming", "both"}:
        raise ModuleAtlasError("direction must be one of: outgoing, incoming, both.")
    if isinstance(depth, bool) or not isinstance(depth, int) or not 1 <= depth <= 8:
        raise ModuleAtlasError("depth must be an integer from 1 through 8.")
    maximum = require_limit(max_nodes, name="max_nodes", maximum=500)
    nodes: dict[str, int] = {root.id: 0}
    selected_edges: dict[tuple[str, str, str, str], AtlasEdge] = {}
    queue: deque[str] = deque((root.id,))
    while queue:
        current = queue.popleft()
        current_depth = nodes[current]
        if current_depth >= depth:
            continue
        candidates: list[AtlasEdge] = []
        if direction in {"outgoing", "both"}:
            candidates.extend(index.outgoing.get(current, ()))
        if direction in {"incoming", "both"}:
            candidates.extend(index.incoming.get(current, ()))
        for edge in candidates:
            neighbor = edge.target_id if edge.source_id == current else edge.source_id
            selected_edges[(edge.source_id, edge.target_id, edge.reference, edge.relation)] = edge
            if neighbor not in nodes and len(nodes) < maximum:
                nodes[neighbor] = current_depth + 1
                queue.append(neighbor)
    selected = [index.by_id[node_id] for node_id in nodes]
    edges = [
        edge
        for edge in selected_edges.values()
        if edge.source_id in nodes and edge.target_id in nodes
    ]
    edges.sort(key=lambda item: (item.source_id, item.target_id, item.reference, item.relation))
    return {
        "root_entity_id": root.id,
        "direction": direction,
        "depth": depth,
        "node_count": len(selected),
        "node_limit": maximum,
        "truncated": len(nodes) >= maximum and bool(queue),
        "nodes": [entity_payload(index, entity, include_fields=False, block_operation_limit=8) for entity in selected],
        "edge_count": len(edges),
        "edges": [edge_payload(index, edge) for edge in edges],
    }


def resolve_named_entity(index: ModuleAtlasIndex, kind: str, name: str) -> ModuleEntity:
    checked = require_query(name, name="name")
    aliases = [checked]
    prefix = PREFIX_BY_KIND.get(kind)
    if prefix and not checked.startswith(prefix):
        aliases.append(prefix + checked)
    matches: dict[str, ModuleEntity] = {}
    for alias in aliases:
        for entity in index.by_alias.get(alias, ()):
            if entity.kind == kind:
                matches[entity.id] = entity
    values = sorted(matches.values(), key=entity_sort_key)
    if not values:
        raise ModuleAtlasError(f"No {kind} named {name!r} was found.")
    if len(values) > 1:
        raise ModuleAtlasError(f"{kind} name {name!r} is ambiguous; use module_find and an exact entity_id.")
    return values[0]


def menu_flow(index: ModuleAtlasIndex, menu_id: str, *, depth: int = 2, max_nodes: int = 100) -> dict[str, Any]:
    menu = resolve_named_entity(index, "menu", menu_id)
    options = sorted((entity for entity in index.entities if entity.parent_id == menu.id), key=entity_sort_key)
    return {
        "menu": entity_payload(index, menu),
        "options": [entity_payload(index, option, block_operation_limit=30) for option in options],
        "flow_graph": module_graph(index, menu.id, direction="outgoing", depth=depth, max_nodes=max_nodes),
        "warnings": [
            "Menu flow is static: condition execution and dynamic string/register values remain explicit source evidence rather than simulated game state.",
        ],
    }


def script_flow(index: ModuleAtlasIndex, script_name: str, *, direction: str = "both", depth: int = 2, max_nodes: int = 120) -> dict[str, Any]:
    script = resolve_named_entity(index, "script", script_name)
    graph = module_graph(index, script.id, direction=direction, depth=depth, max_nodes=max_nodes)
    operations = next((block for block in script.blocks if block.name == "operations"), None)
    return {
        "script": entity_payload(index, script, block_operation_limit=80),
        "call_graph": graph,
        "operation_summary": {
            "operation_count": len(operations.operations) if operations else 0,
            "call_script_count": sum(1 for operation in (operations.operations if operations else ()) if operation.name == "call_script"),
            "writes_globals": sorted({symbol for operation in (operations.operations if operations else ()) for symbol in operation.symbols if symbol.startswith("$")})[:100],
        },
        "warnings": [
            "Call edges are static symbol links. Dynamic script selectors and condition reachability are not executed by the Atlas.",
        ],
    }


def mission_timeline(index: ModuleAtlasIndex, mission_id: str, *, depth: int = 2, max_nodes: int = 120) -> dict[str, Any]:
    mission = resolve_named_entity(index, "mission_template", mission_id)
    triggers = sorted(
        (entity for entity in index.entities if entity.parent_id == mission.id and entity.kind == "mission_trigger"),
        key=entity_sort_key,
    )
    timeline = []
    for trigger in triggers:
        field_values = {field.name: field.value for field in trigger.fields}
        timeline.append(
            {
                "trigger_entity_id": trigger.id,
                "event": field_values.get("event"),
                "interval": field_values.get("interval"),
                "repeat": field_values.get("repeat"),
                "conditions": next((block_payload(block, operation_limit=30) for block in trigger.blocks if block.name == "conditions"), None),
                "consequences": next((block_payload(block, operation_limit=30) for block in trigger.blocks if block.name == "consequences"), None),
            }
        )
    return {
        "mission_template": entity_payload(index, mission, block_operation_limit=20),
        "trigger_count": len(triggers),
        "timeline": timeline,
        "flow_graph": module_graph(index, mission.id, direction="outgoing", depth=depth, max_nodes=max_nodes),
        "warnings": [
            "Trigger timing is represented from authored interval/repeat fields. Engine events, common trigger symbols, and runtime condition reachability are not simulated.",
        ],
    }


def trigger_timeline(
    index: ModuleAtlasIndex,
    *,
    query: str | None = None,
    entity_id: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    if entity_id is not None:
        entity = require_entity(index, entity_id)
        if entity.kind != "simple_trigger":
            raise ModuleAtlasError("entity_id must identify a simple_trigger.")
        selected = [entity]
    else:
        needle = require_query(query).casefold() if query is not None else None
        selected = [
            entity
            for entity in index.entities
            if entity.kind == "simple_trigger" and (needle is None or needle in entity_search_text(entity))
        ]
    selected.sort(key=entity_sort_key)
    return {
        "match_count": len(selected),
        "returned_count": min(len(selected), maximum),
        "truncated": len(selected) > maximum,
        "triggers": [
            {
                "trigger": entity_payload(index, entity, block_operation_limit=60),
                "interval": next((field.value for field in entity.fields if field.name == "interval"), None),
                "outbound": [edge_payload(index, edge) for edge in index.outgoing.get(entity.id, ())[:30]],
            }
            for entity in selected[:maximum]
        ],
        "warnings": ["Simple trigger interval values are source evidence; the runtime scheduler and state guards are not simulated."],
    }


def quest_registry(index: ModuleAtlasIndex, *, query: str | None = None, limit: int = 50) -> dict[str, Any]:
    maximum = require_limit(limit)
    needle = require_query(query).casefold() if query is not None else None
    quests = [
        entity
        for entity in index.entities
        if entity.kind == "quest" and (needle is None or needle in entity_search_text(entity))
    ]
    quests.sort(key=entity_sort_key)
    return {
        "match_count": len(quests),
        "returned_count": min(len(quests), maximum),
        "truncated": len(quests) > maximum,
        "quests": [
            {
                "quest": entity_payload(index, entity),
                "inbound_reference_count": len(index.incoming.get(entity.id, ())),
                "outbound_reference_count": len(index.outgoing.get(entity.id, ())),
            }
            for entity in quests[:maximum]
        ],
    }


def entity_references(index: ModuleAtlasIndex, symbol: str, *, limit: int = 80) -> dict[str, Any]:
    checked = require_query(symbol, name="symbol")
    maximum = require_limit(limit)
    definitions = list(index.by_alias.get(checked, ()))
    if not definitions:
        definitions = [entity for entity in index.entities if entity.name == checked]
    references = [entity for entity in index.entities if checked in entity.symbols and entity not in definitions]
    definitions.sort(key=entity_sort_key)
    references.sort(key=entity_sort_key)
    return {
        "symbol": checked,
        "definition_count": len(definitions),
        "definitions": [entity_payload(index, entity, block_operation_limit=20) for entity in definitions[:maximum]],
        "reference_count": len(references),
        "returned_reference_count": min(len(references), maximum),
        "references_truncated": len(references) > maximum,
        "references": [entity_payload(index, entity, include_fields=False, block_operation_limit=15) for entity in references[:maximum]],
        "source_search_fallback": change_router.code_find(index.router, checked, scope="source", limit=min(maximum, 100)),
    }


def parse_expression(value: str, *, name: str) -> ast.AST:
    if not isinstance(value, str) or not value.strip():
        raise ModuleAtlasError(f"{name} must be a non-empty Python expression.")
    if len(value) > MAX_TEXT_LENGTH:
        raise ModuleAtlasError(f"{name} exceeds the {MAX_TEXT_LENGTH:,}-character safety limit.")
    try:
        return ast.parse(value.strip(), mode="eval").body
    except SyntaxError as error:
        raise ModuleAtlasError(f"{name} is not a valid Python expression: {error.msg}") from error


def validate_operation(value: str, *, name: str = "operation") -> str:
    expression = parse_expression(value, name=name)
    if not isinstance(expression, (ast.Tuple, ast.Name)):
        raise ModuleAtlasError(f"{name} must be an operation tuple or zero-argument operation name.")
    return value.strip()


def validate_operation_list(value: str, *, name: str) -> str:
    expression = parse_expression(value, name=name)
    if not isinstance(expression, ast.List):
        raise ModuleAtlasError(f"{name} must be a list of operation tuples or zero-argument operation names.")
    for item in expression.elts:
        if not isinstance(item, (ast.Tuple, ast.Name)):
            raise ModuleAtlasError(f"{name} may contain only operation tuples or zero-argument operation names.")
    return value.strip()


def quoted(value: str, *, name: str) -> str:
    if not isinstance(value, str):
        raise ModuleAtlasError(f"{name} must be a string.")
    if len(value) > MAX_TEXT_LENGTH:
        raise ModuleAtlasError(f"{name} exceeds the {MAX_TEXT_LENGTH:,}-character safety limit.")
    return json.dumps(value, ensure_ascii=False)


def require_identifier(value: Any, *, name: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER_RE.fullmatch(value):
        raise ModuleAtlasError(f"{name} must be a Python-style identifier (letters, numbers, underscores; no spaces).")
    return value


def require_field(entity: ModuleEntity, name: str | None, *, default: str | None = None) -> FieldAnchor:
    field_name_value = name or default
    if not field_name_value:
        raise ModuleAtlasError("field is required for this action.")
    for field in entity.fields:
        if field.name == field_name_value:
            return field
    available = ", ".join(field.name for field in entity.fields)
    raise ModuleAtlasError(f"{entity.kind} has no field {field_name_value!r}; available fields: {available}.")


def require_block(entity: ModuleEntity, name: str | None) -> OperationBlock:
    if not name:
        available = ", ".join(block.name for block in entity.blocks) or "<none>"
        raise ModuleAtlasError(f"block is required; available operation blocks: {available}.")
    for block in entity.blocks:
        if block.name == name:
            return block
    available = ", ".join(block.name for block in entity.blocks) or "<none>"
    raise ModuleAtlasError(f"{entity.kind} has no operation block {name!r}; available blocks: {available}.")


def occurrence_edit(raw: str, start: int, end: int, new_text: str) -> dict[str, Any]:
    if not 0 <= start < end <= len(raw):
        raise ModuleAtlasError("Semantic edit range is outside its source fragment.")
    old_text = raw[start:end]
    occurrences = change_router.all_occurrences(raw, old_text)
    try:
        occurrence = occurrences.index(start) + 1
    except ValueError as error:
        raise ModuleAtlasError("Could not locate a semantic source anchor.") from error
    return {
        "old_text": old_text,
        "new_text": new_text,
        "occurrence": occurrence,
        "expected_occurrences": len(occurrences),
    }


def line_indent(raw: str, offset: int) -> str:
    line_start = raw.rfind("\n", 0, offset) + 1
    match = re.match(r"[ \t]*", raw[line_start:offset])
    return match.group(0) if match is not None else ""


def item_with_separator(document: SourceDocument, start: int, end: int) -> tuple[int, int]:
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


def list_item_sources(segment: str, *, name: str) -> list[str]:
    expression = parse_expression(segment, name=name)
    if not isinstance(expression, ast.List):
        raise ModuleAtlasError(f"{name} is no longer a list; refresh the entity before editing.")
    offsets = line_offsets(segment)
    return [node_source(segment, item, offsets) for item in expression.elts]


def rebuilt_list(items: Sequence[str]) -> str:
    if not items:
        return "[]"
    return "[\n    " + ",\n    ".join(item.strip() for item in items) + ",\n]"


def append_list_item(document: SourceDocument, field: FieldAnchor, item: str) -> dict[str, Any]:
    original = document.raw[field.start:field.end]
    expression = parse_expression(original, name=field.name)
    if not isinstance(expression, ast.List):
        raise ModuleAtlasError(f"{field.name} must be a direct list before an item can be appended.")
    if not original.startswith("[") or not original.endswith("]"):
        raise ModuleAtlasError(f"{field.name} no longer has a direct source list anchor.")
    base_indent = line_indent(document.raw, field.start)
    child_indent = base_indent + "    "
    inner = original[1:-1].rstrip()
    if inner.strip():
        separator = "" if inner.rstrip().endswith(",") else ","
        replacement = "[" + inner + separator + "\n" + child_indent + item + "\n" + base_indent + "]"
    else:
        replacement = "[\n" + child_indent + item + "\n" + base_indent + "]"
    return occurrence_edit(document.raw, field.start, field.end, replacement)


def assignment_container(document: SourceDocument, entity: ModuleEntity, *, name: str) -> FieldAnchor:
    return FieldAnchor(
        name=name,
        index=-1,
        start=entity.container_start,
        end=entity.container_end,
        source=document.raw[entity.container_start:entity.container_end],
        value=name,
    )


def insert_after_entity(document: SourceDocument, entity: ModuleEntity, item: str) -> dict[str, Any]:
    """Add a top-level constant after the explicitly selected definition.

    Constants are assignments rather than a list literal.  Anchoring the
    insertion to a concrete definition is more reviewable than guessing an
    arbitrary end-of-file location and keeps legacy grouping intentional.
    """

    newline = "\r\n" if "\r\n" in document.raw else "\n"
    original = document.raw[entity.entry_start:entity.entry_end]
    return occurrence_edit(document.raw, entity.entry_start, entity.entry_end, original + newline + item)


def render_menu_option(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_menu_option.")
    option_id = item.get("id")
    text = item.get("text")
    if not isinstance(option_id, str) or not option_id:
        raise ModuleAtlasError("new_item.id must be a non-empty menu option id.")
    if not isinstance(text, str):
        raise ModuleAtlasError("new_item.text must be a string.")
    conditions = validate_operation_list(str(item.get("conditions", "[]")), name="new_item.conditions")
    consequences = validate_operation_list(str(item.get("consequences", "[]")), name="new_item.consequences")
    return f"({quoted(option_id, name='new_item.id')}, {conditions}, {quoted(text, name='new_item.text')}, {consequences})"


def render_constant(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_constant.")
    name = require_identifier(item.get("name"), name="new_item.name")
    value = item.get("value")
    if not isinstance(value, str):
        raise ModuleAtlasError("new_item.value must be a Python expression string.")
    parse_expression(value, name="new_item.value")
    return f"{name} = {value.strip()}"


def render_quest(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_quest.")
    quest_id = require_identifier(item.get("id"), name="new_item.id")
    title = item.get("title")
    description = item.get("description")
    if not isinstance(title, str) or not isinstance(description, str):
        raise ModuleAtlasError("new_item.title and new_item.description must be strings.")
    flags = str(item.get("flags", "0"))
    parse_expression(flags, name="new_item.flags")
    return f"({quoted(quest_id, name='new_item.id')}, {quoted(title, name='new_item.title')}, {flags.strip()}, {quoted(description, name='new_item.description')})"


def render_script(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_script.")
    script_id = require_identifier(item.get("id"), name="new_item.id")
    operations = item.get("operations", "[]")
    if not isinstance(operations, str):
        raise ModuleAtlasError("new_item.operations must be a list-expression string.")
    return f"({quoted(script_id, name='new_item.id')}, {validate_operation_list(operations, name='new_item.operations')})"


def render_menu(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_menu.")
    menu_id = require_identifier(item.get("id"), name="new_item.id")
    text = item.get("text")
    if not isinstance(text, str):
        raise ModuleAtlasError("new_item.text must be a string.")
    flags = str(item.get("flags", "0"))
    mesh = item.get("mesh", "none")
    on_enter = item.get("on_enter", "[]")
    options = item.get("options", [])
    parse_expression(flags, name="new_item.flags")
    if not isinstance(mesh, str):
        raise ModuleAtlasError("new_item.mesh must be a string.")
    if not isinstance(on_enter, str):
        raise ModuleAtlasError("new_item.on_enter must be a list-expression string.")
    checked_on_enter = validate_operation_list(on_enter, name="new_item.on_enter")
    if not isinstance(options, list):
        raise ModuleAtlasError("new_item.options must be a list of menu option objects.")
    rendered_options = [render_menu_option(option) for option in options]
    return "(" + ", ".join(
        (
            quoted(menu_id, name="new_item.id"),
            flags.strip(),
            quoted(text, name="new_item.text"),
            quoted(mesh, name="new_item.mesh"),
            checked_on_enter,
            rebuilt_list(rendered_options),
        )
    ) + ")"


def render_mission_trigger(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_mission_trigger.")
    event = item.get("event")
    if not isinstance(event, str):
        raise ModuleAtlasError("new_item.event must be an event expression such as ti_before_mission_start.")
    expression = parse_expression(event, name="new_item.event")
    if not isinstance(expression, ast.Name):
        raise ModuleAtlasError("new_item.event must be an event constant name.")
    interval = str(item.get("interval", "0"))
    repeat = str(item.get("repeat", "0"))
    parse_expression(interval, name="new_item.interval")
    parse_expression(repeat, name="new_item.repeat")
    conditions = validate_operation_list(str(item.get("conditions", "[]")), name="new_item.conditions")
    consequences = validate_operation_list(str(item.get("consequences", "[]")), name="new_item.consequences")
    return f"({event.strip()}, {interval.strip()}, {repeat.strip()}, {conditions}, {consequences})"


def render_mission_template(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_mission_template.")
    mission_id = require_identifier(item.get("id"), name="new_item.id")
    description = item.get("description", "")
    if not isinstance(description, str):
        raise ModuleAtlasError("new_item.description must be a string.")
    flags = str(item.get("flags", "0"))
    scene = str(item.get("scene", "-1"))
    spawn_records = item.get("spawn_records", "[]")
    triggers = item.get("triggers", [])
    parse_expression(flags, name="new_item.flags")
    parse_expression(scene, name="new_item.scene")
    if not isinstance(spawn_records, str):
        raise ModuleAtlasError("new_item.spawn_records must be a Python list-expression string.")
    parsed_spawn_records = parse_expression(spawn_records, name="new_item.spawn_records")
    if not isinstance(parsed_spawn_records, ast.List):
        raise ModuleAtlasError("new_item.spawn_records must be a Python list-expression string.")
    if not isinstance(triggers, list):
        raise ModuleAtlasError("new_item.triggers must be a list of mission trigger objects.")
    rendered_triggers = [render_mission_trigger(trigger) for trigger in triggers]
    return "(" + ", ".join(
        (
            quoted(mission_id, name="new_item.id"),
            flags.strip(),
            scene.strip(),
            quoted(description, name="new_item.description"),
            spawn_records.strip(),
            rebuilt_list(rendered_triggers),
        )
    ) + ")"


def render_simple_trigger(item: dict[str, Any]) -> str:
    if not isinstance(item, dict):
        raise ModuleAtlasError("new_item must be an object for add_simple_trigger.")
    interval = str(item.get("interval", "1"))
    parse_expression(interval, name="new_item.interval")
    operations = validate_operation_list(str(item.get("operations", "[]")), name="new_item.operations")
    return f"({interval.strip()}, {operations})"


def document_for(index: ModuleAtlasIndex, entity: ModuleEntity) -> SourceDocument:
    document = index.documents.get(entity.path)
    if document is None:
        raise ModuleAtlasError("The entity's source document is no longer available; rebuild the Atlas.")
    return document


def semantic_edits(
    index: ModuleAtlasIndex,
    entity: ModuleEntity,
    *,
    action: str,
    field: str | None = None,
    block: str | None = None,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_item: dict[str, Any] | None = None,
    allow_referenced_removal: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if action not in VALID_ACTIONS:
        raise ModuleAtlasError("action must be one of: " + ", ".join(sorted(VALID_ACTIONS)))
    if entity.area == "dialogs":
        raise ModuleAtlasError("Dialogue route semantics belong to dialogue_patch; it preserves first-match analysis.")
    if entity.area == "presentations":
        raise ModuleAtlasError("Presentation semantics belong to presentation_patch; it preserves layout/register analysis.")
    document = document_for(index, entity)
    metadata: dict[str, Any] = {"action": action, "entity_id": entity.id, "kind": entity.kind}
    if action == "set_text":
        defaults = {"menu": "text", "menu_option": "text", "quest": "description"}
        anchor = require_field(entity, field, default=defaults.get(entity.kind))
        allowed_fields = TEXT_FIELDS_BY_KIND.get(entity.kind, frozenset())
        if anchor.name not in allowed_fields:
            raise ModuleAtlasError(
                f"set_text is limited to {entity.kind} text fields: {', '.join(sorted(allowed_fields)) or '<none>'}."
            )
        return [occurrence_edit(document.raw, anchor.start, anchor.end, quoted(value, name="value"))], {**metadata, "field": anchor.name}
    if action == "set_expression":
        default = "value" if entity.kind == "constant" else None
        anchor = require_field(entity, field, default=default)
        if anchor.name == "id":
            raise ModuleAtlasError("Stable entity IDs cannot be renamed by a generic expression edit; add a replacement entity and migrate references deliberately.")
        replacement = value or ""
        parse_expression(replacement, name="value")
        return [occurrence_edit(document.raw, anchor.start, anchor.end, replacement.strip())], {**metadata, "field": anchor.name}
    if action == "replace_operations":
        operation_block = require_block(entity, block)
        replacement = validate_operation_list(value or "", name="value")
        return [occurrence_edit(document.raw, operation_block.start, operation_block.end, replacement)], {**metadata, "block": operation_block.name}
    if action in {"insert_operation", "remove_operation"}:
        operation_block = require_block(entity, block)
        items = list_item_sources(document.raw[operation_block.start:operation_block.end], name=operation_block.name)
        if action == "insert_operation":
            checked_operation = validate_operation(operation or "")
            if position == "start":
                items.insert(0, checked_operation)
            elif position == "end":
                items.append(checked_operation)
            else:
                raise ModuleAtlasError("position must be 'start' or 'end'.")
            metadata.update({"block": operation_block.name, "operation": checked_operation, "position": position})
        else:
            if isinstance(operation_index, bool) or not isinstance(operation_index, int) or operation_index < 0:
                raise ModuleAtlasError("operation_index must be a zero-based non-negative integer.")
            if operation_index >= len(items):
                raise ModuleAtlasError(f"operation_index={operation_index} is outside the {len(items)} operation(s) in {operation_block.name}.")
            del items[operation_index]
            metadata.update({"block": operation_block.name, "operation_index": operation_index})
        return [occurrence_edit(document.raw, operation_block.start, operation_block.end, rebuilt_list(items))], metadata
    if action == "add_constant":
        if entity.kind != "constant":
            raise ModuleAtlasError("add_constant requires a constant entity that anchors the intended source grouping.")
        return [insert_after_entity(document, entity, render_constant(new_item or {}))], metadata
    if action == "add_quest":
        if entity.kind != "quest":
            raise ModuleAtlasError("add_quest requires a quest entity that anchors the intended source fragment.")
        return [append_list_item(document, assignment_container(document, entity, name="QUESTS"), render_quest(new_item or {}))], metadata
    if action == "add_script":
        if entity.kind != "script":
            raise ModuleAtlasError("add_script requires a script entity that anchors the intended source fragment.")
        return [append_list_item(document, assignment_container(document, entity, name="SCRIPTS"), render_script(new_item or {}))], metadata
    if action == "add_menu":
        if entity.kind != "menu":
            raise ModuleAtlasError("add_menu requires a menu entity that anchors the intended source fragment.")
        return [append_list_item(document, assignment_container(document, entity, name="MENUS"), render_menu(new_item or {}))], metadata
    if action == "add_menu_option":
        if entity.kind != "menu":
            raise ModuleAtlasError("add_menu_option requires a menu entity.")
        options = require_field(entity, "options")
        return [append_list_item(document, options, render_menu_option(new_item or {}))], metadata
    if action == "remove_menu_option":
        if entity.kind != "menu_option":
            raise ModuleAtlasError("remove_menu_option requires a menu_option entity.")
        start, end = item_with_separator(document, entity.entry_start, entity.entry_end)
        return [occurrence_edit(document.raw, start, end, "")], metadata
    if action == "add_mission_trigger":
        if entity.kind != "mission_template":
            raise ModuleAtlasError("add_mission_trigger requires a mission_template entity.")
        triggers = require_field(entity, "triggers")
        return [append_list_item(document, triggers, render_mission_trigger(new_item or {}))], metadata
    if action == "add_mission_template":
        if entity.kind != "mission_template":
            raise ModuleAtlasError("add_mission_template requires a mission template that anchors the intended source fragment.")
        return [append_list_item(document, assignment_container(document, entity, name="MISSION_TEMPLATES"), render_mission_template(new_item or {}))], metadata
    if action == "remove_mission_trigger":
        if entity.kind != "mission_trigger":
            raise ModuleAtlasError("remove_mission_trigger requires a mission_trigger entity.")
        start, end = item_with_separator(document, entity.entry_start, entity.entry_end)
        return [occurrence_edit(document.raw, start, end, "")], metadata
    if action == "set_trigger_interval":
        if entity.kind not in {"mission_trigger", "simple_trigger"}:
            raise ModuleAtlasError("set_trigger_interval requires a mission_trigger or simple_trigger entity.")
        interval = require_field(entity, "interval")
        replacement = value or ""
        parse_expression(replacement, name="value")
        return [occurrence_edit(document.raw, interval.start, interval.end, replacement.strip())], metadata
    if action == "add_simple_trigger":
        if entity.kind != "simple_trigger":
            raise ModuleAtlasError("add_simple_trigger requires an existing simple_trigger in the target source fragment.")
        container = FieldAnchor(
            name="simple_triggers",
            index=-1,
            start=entity.container_start,
            end=entity.container_end,
            source=document.raw[entity.container_start:entity.container_end],
            value="SIMPLE_TRIGGERS",
        )
        return [append_list_item(document, container, render_simple_trigger(new_item or {}))], metadata
    if action == "remove_entity":
        removable = {"constant", "quest", "script", "menu", "mission_template", "simple_trigger"}
        if entity.kind not in removable:
            raise ModuleAtlasError(
                "remove_entity supports only a top-level constant, quest, script, menu, mission_template, or simple_trigger; use area-specific remove actions for children."
            )
        inbound = index.incoming.get(entity.id, ())
        if inbound and not allow_referenced_removal:
            raise ModuleAtlasError(
                f"Refusing to remove {entity.kind} {entity.name!r}: {len(inbound)} static inbound reference(s) exist. "
                "Inspect module_graph/entity_references and set allow_referenced_removal=true only after deliberately migrating them."
            )
        start, end = item_with_separator(document, entity.entry_start, entity.entry_end)
        return [occurrence_edit(document.raw, start, end, "")], {
            **metadata,
            "static_inbound_reference_count": len(inbound),
            "allow_referenced_removal": allow_referenced_removal,
        }
    raise ModuleAtlasError(f"Unhandled Atlas action: {action}")


def module_patch(
    index: ModuleAtlasIndex,
    entity_id: str,
    *,
    action: str,
    field: str | None = None,
    block: str | None = None,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_item: dict[str, Any] | None = None,
    allow_referenced_removal: bool = False,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    entity = require_entity(index, entity_id)
    edits, semantic = semantic_edits(
        index,
        entity,
        action=action,
        field=field,
        block=block,
        value=value,
        operation=operation,
        position=position,
        operation_index=operation_index,
        new_item=new_item,
        allow_referenced_removal=allow_referenced_removal,
    )
    plan = change_router.patch_plan(index.router, entity.target_id, edits, expected_sha256=expected_sha256)
    return {
        "semantic_operation": semantic,
        "entity": entity_payload(index, entity),
        "relationships": {
            "outbound": [edge_payload(index, edge) for edge in index.outgoing.get(entity.id, ())[:40]],
            "inbound": [edge_payload(index, edge) for edge in index.incoming.get(entity.id, ())[:40]],
        },
        "change_router_plan": plan,
        "apply_contract": {
            "tool": "module_apply",
            "entity_id": entity.id,
            "action": action,
            "required_expected_sha256": plan["target"]["base_sha256"],
            "dry_run_default": True,
            "guarantees": plan["apply_contract"]["guarantees"],
        },
        "warnings": ["Review the unified diff, graph links, and area-specific engine semantics before a non-dry-run apply."],
    }


def module_apply(
    index: ModuleAtlasIndex,
    entity_id: str,
    *,
    action: str,
    expected_sha256: str,
    dry_run: bool = True,
    field: str | None = None,
    block: str | None = None,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_item: dict[str, Any] | None = None,
    allow_referenced_removal: bool = False,
) -> dict[str, Any]:
    entity = require_entity(index, entity_id)
    edits, semantic = semantic_edits(
        index,
        entity,
        action=action,
        field=field,
        block=block,
        value=value,
        operation=operation,
        position=position,
        operation_index=operation_index,
        new_item=new_item,
        allow_referenced_removal=allow_referenced_removal,
    )
    result = change_router.apply_source_edits(index.router, entity.target_id, edits, expected_sha256=expected_sha256, dry_run=dry_run)
    if not dry_run:
        invalidate_atlas(index.root)
    return {
        "semantic_operation": semantic,
        "entity_id": entity.id,
        "result": result,
        "warnings": [*result["warnings"], "Only modular source was changed; compile/ and _export/ remain untouched until an intentional reviewed build."],
    }


def module_verify(
    index: ModuleAtlasIndex,
    entity_id: str,
    *,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    entity = require_entity(index, entity_id)
    verification = change_router.verify_change(index.router, entity.target_id, expected_sha256=expected_sha256, run_tests=run_tests, stage_build_check=stage_build_check, max_tests=max_tests, timeout_seconds=timeout_seconds)
    return {
        "entity": entity_payload(index, entity),
        "relationships": {
            "outbound_count": len(index.outgoing.get(entity.id, ())),
            "inbound_count": len(index.incoming.get(entity.id, ())),
        },
        "change_router_verification": verification,
        "warnings": [*verification["warnings"], "Verification proves static source/build evidence; dynamic game state remains outside the Atlas."],
    }


def write_payload(payload: dict[str, Any], output: str | None, root: Path) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output:
        path = change_router.output_path(output, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def parse_json_object(value: str | None, *, name: str) -> dict[str, Any] | None:
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise ModuleAtlasError(f"{name} must be JSON: {error}") from error
    if not isinstance(parsed, dict):
        raise ModuleAtlasError(f"{name} must decode to an object.")
    return parsed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM-first semantic control plane for every SoD Modern module-system area.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    summary = subparsers.add_parser("summary")
    summary.add_argument("--output")
    find = subparsers.add_parser("find")
    find.add_argument("--query")
    find.add_argument("--area", default="all", choices=("all", *SOURCE_AREAS))
    find.add_argument("--kind")
    find.add_argument("--limit", type=int, default=30)
    find.add_argument("--output")
    context = subparsers.add_parser("context")
    context.add_argument("entity_id")
    context.add_argument("--max-lines", type=int, default=120)
    context.add_argument("--related-limit", type=int, default=30)
    context.add_argument("--output")
    graph = subparsers.add_parser("graph")
    graph.add_argument("entity_id")
    graph.add_argument("--direction", default="both", choices=("outgoing", "incoming", "both"))
    graph.add_argument("--depth", type=int, default=2)
    graph.add_argument("--max-nodes", type=int, default=100)
    graph.add_argument("--output")
    menu = subparsers.add_parser("menu-flow")
    menu.add_argument("menu_id")
    menu.add_argument("--depth", type=int, default=2)
    menu.add_argument("--max-nodes", type=int, default=100)
    menu.add_argument("--output")
    script = subparsers.add_parser("script-flow")
    script.add_argument("script_name")
    script.add_argument("--direction", default="both", choices=("outgoing", "incoming", "both"))
    script.add_argument("--depth", type=int, default=2)
    script.add_argument("--max-nodes", type=int, default=120)
    script.add_argument("--output")
    mission = subparsers.add_parser("mission-timeline")
    mission.add_argument("mission_id")
    mission.add_argument("--depth", type=int, default=2)
    mission.add_argument("--max-nodes", type=int, default=120)
    mission.add_argument("--output")
    trigger = subparsers.add_parser("trigger-timeline")
    trigger.add_argument("--query")
    trigger.add_argument("--entity-id")
    trigger.add_argument("--limit", type=int, default=50)
    trigger.add_argument("--output")
    quests = subparsers.add_parser("quest-registry")
    quests.add_argument("--query")
    quests.add_argument("--limit", type=int, default=50)
    quests.add_argument("--output")
    references = subparsers.add_parser("references")
    references.add_argument("symbol")
    references.add_argument("--limit", type=int, default=80)
    references.add_argument("--output")
    integrity = subparsers.add_parser("integrity")
    integrity.add_argument("--limit", type=int, default=100)
    integrity.add_argument("--output")
    for name in ("patch", "apply"):
        command = subparsers.add_parser(name)
        command.add_argument("entity_id")
        command.add_argument("action", choices=sorted(VALID_ACTIONS))
        command.add_argument("--field")
        command.add_argument("--block")
        command.add_argument("--value")
        command.add_argument("--operation")
        command.add_argument("--position", default="end")
        command.add_argument("--operation-index", type=int)
        command.add_argument("--new-item")
        command.add_argument("--allow-referenced-removal", action="store_true")
        command.add_argument("--expected-sha256")
        command.add_argument("--output")
        if name == "apply":
            command.add_argument("--apply", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("entity_id")
    verify.add_argument("--expected-sha256")
    verify.add_argument("--run-tests", action="store_true")
    verify.add_argument("--stage-build", action="store_true")
    verify.add_argument("--max-tests", type=int, default=3)
    verify.add_argument("--timeout-seconds", type=int, default=90)
    verify.add_argument("--output")
    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        index = build_module_atlas(args.root)
        if command == "summary":
            payload = module_summary(index)
        elif command == "find":
            payload = module_find(index, query=args.query, area=args.area, kind=args.kind, limit=args.limit)
        elif command == "context":
            payload = module_context(index, args.entity_id, max_lines=args.max_lines, related_limit=args.related_limit)
        elif command == "graph":
            payload = module_graph(index, args.entity_id, direction=args.direction, depth=args.depth, max_nodes=args.max_nodes)
        elif command == "menu-flow":
            payload = menu_flow(index, args.menu_id, depth=args.depth, max_nodes=args.max_nodes)
        elif command == "script-flow":
            payload = script_flow(index, args.script_name, direction=args.direction, depth=args.depth, max_nodes=args.max_nodes)
        elif command == "mission-timeline":
            payload = mission_timeline(index, args.mission_id, depth=args.depth, max_nodes=args.max_nodes)
        elif command == "trigger-timeline":
            payload = trigger_timeline(index, query=args.query, entity_id=args.entity_id, limit=args.limit)
        elif command == "quest-registry":
            payload = quest_registry(index, query=args.query, limit=args.limit)
        elif command == "references":
            payload = entity_references(index, args.symbol, limit=args.limit)
        elif command == "integrity":
            payload = module_integrity(index, limit=args.limit)
        elif command == "patch":
            payload = module_patch(index, args.entity_id, action=args.action, field=args.field, block=args.block, value=args.value, operation=args.operation, position=args.position, operation_index=args.operation_index, new_item=parse_json_object(args.new_item, name="new_item"), allow_referenced_removal=args.allow_referenced_removal, expected_sha256=args.expected_sha256)
        elif command == "apply":
            if not args.expected_sha256:
                raise ModuleAtlasError("apply requires --expected-sha256 from a module patch plan.")
            payload = module_apply(index, args.entity_id, action=args.action, expected_sha256=args.expected_sha256, dry_run=not args.apply, field=args.field, block=args.block, value=args.value, operation=args.operation, position=args.position, operation_index=args.operation_index, new_item=parse_json_object(args.new_item, name="new_item"), allow_referenced_removal=args.allow_referenced_removal)
        elif command == "verify":
            payload = module_verify(index, args.entity_id, expected_sha256=args.expected_sha256, run_tests=args.run_tests, stage_build_check=args.stage_build, max_tests=args.max_tests, timeout_seconds=args.timeout_seconds)
        else:
            raise ModuleAtlasError(f"Unknown command: {command}")
        write_payload(payload, getattr(args, "output", None), index.root)
        return 0
    except (ModuleAtlasError, change_router.ChangeRouterError) as error:
        parser.error(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
