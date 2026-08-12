#!/usr/bin/env python3
"""Feature Authoring Compiler for the SoD Modern Mount & Blade 1.011 module system.

This is intentionally a *control plane*, not a replacement compiler.  The
legacy source fragments remain authoritative, including their top-to-bottom
ordering rules.  A feature intent is structured JSON which names real engine
entrypoints and uses a small typed operation IR.  The compiler resolves that
intent through the existing Atlas/Dialogue/Presentation specialists, produces
anchored Change Router plans, and delegates every actual write to the shared
source-only SHA gate.

There is no raw Python/tuple escape hatch in the IR.  This keeps an LLM from
silently turning a prose request into arbitrary source code while preserving
the full semantic editors that already understand M&B's unusual data shapes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.change_router import change_router  # noqa: E402
from devkit.dialogue_composer import dialogue_composer  # noqa: E402
from devkit.dialogue_model_checker import dialogue_model_checker  # noqa: E402
from devkit.module_atlas import module_atlas  # noqa: E402
from devkit.module_blueprint import module_blueprint  # noqa: E402
from devkit.order_control import order_control  # noqa: E402
from devkit.presentation_layout import presentation_layout  # noqa: E402


FEATURE_AUTHORING_VERSION = "0.1.0"
ENTRYPOINT_CATALOG_RELATIVE = Path("devkit/feature_authoring/entrypoints.json")
FEATURE_CATALOG_RELATIVE = Path("devkit/feature_authoring/features.json")
FEATURE_INTENT_SCHEMA = "sod-modern.feature-intent.v1"
FEATURE_CATALOG_SCHEMA = "sod-modern.feature-authoring-catalog.v1"
ENTRYPOINT_CATALOG_SCHEMA = "sod-modern.engine-entrypoint-catalog.v1"
MAX_QUERY_LENGTH = 500
MAX_DESCRIPTION_LENGTH = 2_000
MAX_FEATURES = 200
MAX_ENTRYPOINTS = 64
MAX_CHANGES = 32
MAX_OPERATIONS = 256
MAX_OPERANDS_PER_OPERATION = 64
MAX_RESULT_LIMIT = 200
MAX_TRACE_ENTRIES = 30
MAX_TESTS = 24
MAX_TEXT_LENGTH = 30_000
FEATURE_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,119}$")
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
OPERATION_RE = re.compile(r"^[a-z][a-z0-9_]*$")
REGISTER_RE = re.compile(r"^(?:s[0-9]{1,3}|reg[0-9]{1,3}|pos[0-9]{1,3})$")
REFERENCE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
STATE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SAFE_TEST_RE = re.compile(r"^build/test_[A-Za-z0-9_]+\.py$")
VALID_FEATURE_STATUSES = frozenset({"active", "draft", "disabled"})
VALID_ENTRYPOINT_KINDS = frozenset(
    {
        "script",
        "simple_trigger",
        "menu",
        "dialogue_route",
        "presentation",
        "mission_template",
        "mission_trigger",
        "quest",
        "constant",
    }
)
VALID_OPERAND_KEYS = frozenset(
    {"symbol", "reference", "local", "global", "register", "string", "list", "tuple", "combine"}
)
COMBINE_OPERATORS = {
    "or": "|",
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
}


class FeatureAuthoringError(RuntimeError):
    """A feature intent, entrypoint request, or guarded plan is unsafe."""


@dataclass(frozen=True)
class EntrypointFamily:
    id: str
    title: str
    description: str
    source_area: str
    entity_kind: str
    trace: str
    path_prefix: str | None
    name_prefix: str | None


@dataclass(frozen=True)
class Entrypoint:
    id: str
    family: str
    title: str
    description: str
    name: str
    entity_id: str | None
    target_ids: tuple[str, ...]
    source_paths: tuple[str, ...]
    line: int | None
    source_order: int | None
    symbols: tuple[str, ...]
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class FeatureIntent:
    id: str
    title: str
    status: str
    description: str
    blueprint_id: str | None
    entrypoints: tuple[str, ...]
    changes: tuple[dict[str, Any], ...]
    tests: tuple[str, ...]
    require_blueprint: bool
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class CompiledChange:
    id: str
    kind: str
    target_entrypoint_id: str
    target_id: str
    edits: tuple[dict[str, Any], ...]
    semantic: Mapping[str, Any]
    source_path: str


@dataclass
class FeatureAuthoringIndex:
    root: Path
    router: change_router.RouterIndex
    atlas: module_atlas.ModuleAtlasIndex
    dialogues: dialogue_composer.DialogueComposerIndex
    layouts: presentation_layout.PresentationLayoutIndex
    blueprints: module_blueprint.ModuleBlueprintIndex
    families: dict[str, EntrypointFamily]
    entrypoints: tuple[Entrypoint, ...]
    by_entrypoint_id: dict[str, Entrypoint]
    features: tuple[FeatureIntent, ...]
    features_by_id: dict[str, FeatureIntent]
    id_by_symbol: dict[str, tuple[order_control.IdEntry, ...]]
    warnings: list[str]


_CACHE: dict[Path, tuple[tuple[Any, ...], FeatureAuthoringIndex]] = {}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any, *, length: int = 20) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:length]


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_string(value: Any, *, name: str, maximum: int = MAX_QUERY_LENGTH) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FeatureAuthoringError(f"{name} must be a non-empty string.")
    checked = value.strip()
    if len(checked) > maximum:
        raise FeatureAuthoringError(f"{name} must be at most {maximum:,} characters.")
    return checked


def require_text(value: Any, *, name: str, maximum: int = MAX_TEXT_LENGTH) -> str:
    if not isinstance(value, str):
        raise FeatureAuthoringError(f"{name} must be a string.")
    if len(value) > maximum:
        raise FeatureAuthoringError(f"{name} exceeds the {maximum:,}-character safety limit.")
    return value


def require_identifier(value: Any, *, name: str, pattern: re.Pattern[str] = IDENTIFIER_RE) -> str:
    checked = require_string(value, name=name, maximum=160)
    if pattern.fullmatch(checked) is None:
        raise FeatureAuthoringError(f"{name} must be an identifier using letters, digits, and underscores.")
    return checked


def require_feature_id(value: Any, *, name: str = "feature_id") -> str:
    checked = require_string(value, name=name, maximum=120)
    if FEATURE_ID_RE.fullmatch(checked) is None:
        raise FeatureAuthoringError(f"{name} must use lower-case feature-id syntax (letters, digits, and hyphens).")
    return checked


def require_limit(value: Any, *, name: str = "limit", maximum: int = MAX_RESULT_LIMIT) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise FeatureAuthoringError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_object(value: Any, *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FeatureAuthoringError(f"{name} must be a JSON object.")
    return dict(value)


def reject_unknown_fields(value: Mapping[str, Any], *, name: str, allowed: Iterable[str]) -> None:
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise FeatureAuthoringError(f"{name} has unsupported field(s): " + ", ".join(unknown))


def require_safe_relative_path(value: Any, *, name: str, prefix: str, suffix: str = ".py") -> str:
    checked = require_string(value, name=name, maximum=500).replace("\\", "/")
    parts = checked.split("/")
    if (
        checked.startswith("/")
        or ":" in parts[0]
        or any(part in {"", ".", ".."} for part in parts)
        or not checked.startswith(prefix)
        or not checked.endswith(suffix)
    ):
        raise FeatureAuthoringError(f"{name} must be a safe repository-relative {suffix} path under {prefix}.")
    return checked


def load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise FeatureAuthoringError(f"Missing {label}: {path}") from error
    except (OSError, json.JSONDecodeError) as error:
        raise FeatureAuthoringError(f"Could not read {label}: {error}") from error
    if not isinstance(value, dict):
        raise FeatureAuthoringError(f"{label} must be a JSON object.")
    return value


def catalog_signature(root: Path) -> tuple[Any, ...]:
    rows: list[Any] = []
    for relative in (ENTRYPOINT_CATALOG_RELATIVE, FEATURE_CATALOG_RELATIVE):
        path = root / relative
        try:
            stat = path.stat()
        except OSError:
            rows.append((relative.as_posix(), None, None))
        else:
            rows.append((relative.as_posix(), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def load_families(root: Path) -> dict[str, EntrypointFamily]:
    path = root / ENTRYPOINT_CATALOG_RELATIVE
    catalog = load_json_object(path, label="engine entrypoint catalog")
    if catalog.get("schema") != ENTRYPOINT_CATALOG_SCHEMA:
        raise FeatureAuthoringError("Engine entrypoint catalog has an unsupported schema.")
    rows = catalog.get("families")
    if not isinstance(rows, list) or not rows:
        raise FeatureAuthoringError("Engine entrypoint catalog must contain a non-empty families array.")
    if len(rows) > 40:
        raise FeatureAuthoringError("Engine entrypoint catalog exceeds the 40-family safety limit.")
    families: dict[str, EntrypointFamily] = {}
    for position, raw in enumerate(rows, start=1):
        item = require_object(raw, name=f"families[{position}]")
        reject_unknown_fields(
            item,
            name=f"families[{position}]",
            allowed={"id", "title", "description", "source_area", "entity_kind", "trace", "path_prefix", "name_prefix"},
        )
        identifier = require_identifier(item.get("id"), name=f"families[{position}].id", pattern=FEATURE_ID_RE)
        if identifier in families:
            raise FeatureAuthoringError(f"Duplicate engine entrypoint family id: {identifier}")
        area = require_string(item.get("source_area"), name=f"families[{position}].source_area")
        if area not in change_router.SOURCE_AREAS:
            raise FeatureAuthoringError(f"families[{position}].source_area is not a Module System source area.")
        kind = require_string(item.get("entity_kind"), name=f"families[{position}].entity_kind")
        if kind not in VALID_ENTRYPOINT_KINDS:
            raise FeatureAuthoringError(f"families[{position}].entity_kind is unsupported: {kind}")
        path_prefix = item.get("path_prefix")
        if path_prefix is not None:
            path_prefix = require_string(path_prefix, name=f"families[{position}].path_prefix", maximum=500).replace("\\", "/")
            if not path_prefix.startswith("src/") or ".." in path_prefix.split("/"):
                raise FeatureAuthoringError(f"families[{position}].path_prefix must be a safe src/ prefix.")
        name_prefix = item.get("name_prefix")
        if name_prefix is not None:
            name_prefix = require_string(name_prefix, name=f"families[{position}].name_prefix", maximum=120)
        families[identifier] = EntrypointFamily(
            id=identifier,
            title=require_string(item.get("title"), name=f"families[{position}].title", maximum=200),
            description=require_text(item.get("description"), name=f"families[{position}].description", maximum=MAX_DESCRIPTION_LENGTH),
            source_area=area,
            entity_kind=kind,
            trace=require_identifier(item.get("trace"), name=f"families[{position}].trace"),
            path_prefix=path_prefix,
            name_prefix=name_prefix,
        )
    return families


def source_fragment_payload(router: change_router.RouterIndex, path: str) -> dict[str, Any]:
    fragment = router.fragments.get(path)
    if fragment is None:
        return {"path": path, "missing": True}
    return {
        "target_id": fragment.id,
        "path": fragment.path,
        "area": fragment.area,
        "sha256": fragment.sha256,
        "section_order": fragment.order_position,
        "ordering_policy": fragment.order_policy,
    }


def entrypoint_id_for_entity(family: str, entity: module_atlas.ModuleEntity, atlas: module_atlas.ModuleAtlasIndex) -> str:
    if family == "simple-trigger":
        ordinal = entity.name.rsplit(":", 1)[-1]
        return f"entrypoint:simple-trigger:{entity.path}:{ordinal}"
    if family == "mission-callback":
        parent = atlas.by_id.get(entity.parent_id or "")
        if parent is None:
            raise FeatureAuthoringError("A mission callback has no resolvable mission-template parent.")
        event = next((field.value for field in entity.fields if field.name == "event"), "event")
        siblings = sorted(
            (
                candidate
                for candidate in atlas.entities
                if candidate.kind == "mission_trigger" and candidate.parent_id == parent.id
            ),
            key=lambda item: (item.line, item.column, item.id),
        )
        ordinal = siblings.index(entity) + 1
        return f"entrypoint:mission-callback:{parent.name}:{event}:{ordinal}"
    return f"entrypoint:{family}:{entity.name}"


def entity_matches_family(entity: module_atlas.ModuleEntity, family: EntrypointFamily) -> bool:
    return (
        entity.area == family.source_area
        and entity.kind == family.entity_kind
        and (family.path_prefix is None or entity.path.startswith(family.path_prefix))
        and (family.name_prefix is None or entity.name.startswith(family.name_prefix))
    )


def build_entrypoints(
    router: change_router.RouterIndex,
    atlas: module_atlas.ModuleAtlasIndex,
    dialogues: dialogue_composer.DialogueComposerIndex,
    layouts: presentation_layout.PresentationLayoutIndex,
    families: Mapping[str, EntrypointFamily],
) -> tuple[tuple[Entrypoint, ...], list[str]]:
    entries: list[Entrypoint] = []
    warnings: list[str] = []
    seen: set[str] = set()
    ambiguous: set[str] = set()

    def add(entry: Entrypoint) -> None:
        if entry.id in seen:
            if entry.id not in ambiguous:
                warnings.append(f"Ambiguous engine entrypoint id omitted from registry: {entry.id}")
                ambiguous.add(entry.id)
            return
        seen.add(entry.id)
        entries.append(entry)

    for family in families.values():
        if family.id in {"dialogue-state", "presentation"}:
            continue
        for entity in sorted(atlas.entities, key=lambda item: (item.path.casefold(), item.line, item.column, item.id)):
            if not entity_matches_family(entity, family):
                continue
            identifier = entrypoint_id_for_entity(family.id, entity, atlas)
            symbols = tuple(dict.fromkeys((entity.name, *entity.aliases, *entity.symbols)))
            metadata: dict[str, Any] = {}
            if family.id == "mission-callback":
                parent = atlas.by_id.get(entity.parent_id or "")
                metadata["mission_template"] = parent.name if parent is not None else None
                metadata["event"] = next((field.value for field in entity.fields if field.name == "event"), None)
            add(
                Entrypoint(
                    id=identifier,
                    family=family.id,
                    title=f"{family.title}: {entity.name}",
                    description=family.description,
                    name=entity.name,
                    entity_id=entity.id,
                    target_ids=(entity.target_id,),
                    source_paths=(entity.path,),
                    line=entity.line,
                    source_order=entity.source_order,
                    symbols=symbols,
                    metadata=metadata,
                )
            )

    dialogue_family = families.get("dialogue-state")
    if dialogue_family is not None:
        grouped: dict[str, list[dialogue_composer.DialogueRoute]] = defaultdict(list)
        for route in dialogues.routes:
            grouped[route.input_state].append(route)
        for state, routes in sorted(grouped.items(), key=lambda item: item[0].casefold()):
            ordered = sorted(routes, key=dialogue_composer.route_sort_key)
            target_ids = tuple(dict.fromkeys(route.target_id for route in ordered))
            paths = tuple(dict.fromkeys(route.path for route in ordered))
            add(
                Entrypoint(
                    id=f"entrypoint:dialogue-state:{state}",
                    family="dialogue-state",
                    title=f"{dialogue_family.title}: {state}",
                    description=dialogue_family.description,
                    name=state,
                    entity_id=None,
                    target_ids=target_ids,
                    source_paths=paths,
                    line=ordered[0].line if ordered else None,
                    source_order=ordered[0].source_order if ordered else None,
                    symbols=(state,),
                    metadata={"route_ids": tuple(route.id for route in ordered), "route_count": len(ordered)},
                )
            )

    presentation_family = families.get("presentation")
    if presentation_family is not None:
        for presentation in sorted(layouts.presentations, key=lambda item: (item.path.casefold(), item.line, item.key)):
            add(
                Entrypoint(
                    id=f"entrypoint:presentation:{presentation.id}",
                    family="presentation",
                    title=f"{presentation_family.title}: {presentation.id}",
                    description=presentation_family.description,
                    name=presentation.id,
                    entity_id=None,
                    target_ids=(presentation.target_id,),
                    source_paths=(presentation.path,),
                    line=presentation.line,
                    source_order=presentation.source_order,
                    symbols=(presentation.id, f"prsnt_{presentation.id}"),
                    metadata={"presentation_key": presentation.key},
                )
            )

    entries.sort(key=lambda item: (item.family, item.name.casefold(), item.id))
    return tuple(entries), warnings


def normalize_ir_operand(value: Any, *, name: str = "operand", depth: int = 0) -> str:
    """Render one deliberately small typed expression, never raw Python source."""

    if depth > 12:
        raise FeatureAuthoringError(f"{name} exceeds the nested IR depth limit.")
    if isinstance(value, bool):
        raise FeatureAuthoringError(f"{name} must not be a boolean; use 0 or 1 explicitly.")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise FeatureAuthoringError(f"{name} must be a finite number.")
        return format(value, ".15g")
    item = require_object(value, name=name)
    if len(item) != 1:
        raise FeatureAuthoringError(f"{name} must contain exactly one typed operand key.")
    key, raw = next(iter(item.items()))
    if key not in VALID_OPERAND_KEYS:
        raise FeatureAuthoringError(f"{name} has unsupported typed operand key: {key}")
    if key == "symbol":
        return require_identifier(raw, name=f"{name}.symbol")
    if key == "reference":
        return json.dumps(require_identifier(raw, name=f"{name}.reference", pattern=REFERENCE_RE), ensure_ascii=False)
    if key in {"local", "global"}:
        prefix = ":" if key == "local" else "$"
        raw_value = require_string(raw, name=f"{name}.{key}", maximum=160)
        if raw_value.startswith(prefix):
            raw_value = raw_value[1:]
        if IDENTIFIER_RE.fullmatch(raw_value) is None:
            raise FeatureAuthoringError(f"{name}.{key} must name an identifier, with or without its {prefix} prefix.")
        return json.dumps(prefix + raw_value, ensure_ascii=False)
    if key == "register":
        register = require_string(raw, name=f"{name}.register", maximum=20)
        if REGISTER_RE.fullmatch(register) is None:
            raise FeatureAuthoringError(f"{name}.register must be s#, reg#, or pos#.")
        return register
    if key == "string":
        return json.dumps(require_text(raw, name=f"{name}.string"), ensure_ascii=False)
    if key in {"list", "tuple"}:
        if not isinstance(raw, list) or len(raw) > MAX_OPERANDS_PER_OPERATION:
            raise FeatureAuthoringError(f"{name}.{key} must be a JSON array with at most {MAX_OPERANDS_PER_OPERATION} entries.")
        values = [normalize_ir_operand(child, name=f"{name}.{key}[{position}]", depth=depth + 1) for position, child in enumerate(raw)]
        if key == "list":
            return "[" + ", ".join(values) + "]"
        if len(values) == 1:
            return "(" + values[0] + ",)"
        return "(" + ", ".join(values) + ")"
    combine = require_object(raw, name=f"{name}.combine")
    reject_unknown_fields(combine, name=f"{name}.combine", allowed={"operator", "items"})
    operator = require_string(combine.get("operator"), name=f"{name}.combine.operator")
    token = COMBINE_OPERATORS.get(operator)
    if token is None:
        raise FeatureAuthoringError(f"{name}.combine.operator must be one of: " + ", ".join(sorted(COMBINE_OPERATORS)))
    values = combine.get("items")
    if not isinstance(values, list) or not 2 <= len(values) <= MAX_OPERANDS_PER_OPERATION:
        raise FeatureAuthoringError(f"{name}.combine.items must contain from 2 through {MAX_OPERANDS_PER_OPERATION} typed operands.")
    rendered = [normalize_ir_operand(child, name=f"{name}.combine.items[{position}]", depth=depth + 1) for position, child in enumerate(values)]
    return "(" + f" {token} ".join(rendered) + ")"


def render_operation(value: Any, *, name: str = "operation") -> str:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"op", "args", "negated"})
    operation = require_identifier(item.get("op"), name=f"{name}.op", pattern=OPERATION_RE)
    if operation.startswith("__"):
        raise FeatureAuthoringError(f"{name}.op may not use a Python dunder name.")
    negated = item.get("negated", False)
    if not isinstance(negated, bool):
        raise FeatureAuthoringError(f"{name}.negated must be a boolean when supplied.")
    args = item.get("args", [])
    if not isinstance(args, list) or len(args) > MAX_OPERANDS_PER_OPERATION:
        raise FeatureAuthoringError(f"{name}.args must be an array with at most {MAX_OPERANDS_PER_OPERATION} entries.")
    rendered_args = [normalize_ir_operand(argument, name=f"{name}.args[{position}]") for position, argument in enumerate(args)]
    op_source = f"neg|{operation}" if negated else operation
    if not rendered_args:
        return op_source
    return "(" + ", ".join((op_source, *rendered_args)) + ")"


def render_operations(value: Any, *, name: str = "operations") -> str:
    if not isinstance(value, list):
        raise FeatureAuthoringError(f"{name} must be an array of typed operation objects.")
    if len(value) > MAX_OPERATIONS:
        raise FeatureAuthoringError(f"{name} contains too many operations; maximum is {MAX_OPERATIONS}.")
    if not value:
        return "[]"
    rendered = [render_operation(operation, name=f"{name}[{position}]") for position, operation in enumerate(value)]
    return "[\n    " + ",\n    ".join(rendered) + ",\n]"


def normalize_feature_intent(value: Any, *, name: str = "intent") -> FeatureIntent:
    item = require_object(value, name=name)
    reject_unknown_fields(
        item,
        name=name,
        allowed={"schema", "id", "title", "status", "description", "blueprint_id", "entrypoints", "changes", "verification"},
    )
    required = ("schema", "id", "title", "status", "description", "entrypoints", "changes", "verification")
    missing = [field for field in required if field not in item]
    if missing:
        raise FeatureAuthoringError(f"{name} is missing required field(s): " + ", ".join(missing))
    if item["schema"] != FEATURE_INTENT_SCHEMA:
        raise FeatureAuthoringError(f"{name}.schema must be {FEATURE_INTENT_SCHEMA!r}.")
    identifier = require_feature_id(item["id"], name=f"{name}.id")
    status = require_string(item["status"], name=f"{name}.status")
    if status not in VALID_FEATURE_STATUSES:
        raise FeatureAuthoringError(f"{name}.status must be one of: " + ", ".join(sorted(VALID_FEATURE_STATUSES)))
    blueprint_id = item.get("blueprint_id")
    if blueprint_id is not None:
        blueprint_id = require_feature_id(blueprint_id, name=f"{name}.blueprint_id")
    entrypoints_raw = item["entrypoints"]
    if not isinstance(entrypoints_raw, list) or not 1 <= len(entrypoints_raw) <= MAX_ENTRYPOINTS:
        raise FeatureAuthoringError(f"{name}.entrypoints must contain from 1 through {MAX_ENTRYPOINTS} entrypoint IDs.")
    entrypoints = tuple(require_string(entrypoint, name=f"{name}.entrypoints[{position}]", maximum=600) for position, entrypoint in enumerate(entrypoints_raw))
    if any(not entrypoint.startswith("entrypoint:") for entrypoint in entrypoints):
        raise FeatureAuthoringError(f"{name}.entrypoints must contain entrypoint IDs returned by entrypoint_find.")
    if len(set(entrypoints)) != len(entrypoints):
        raise FeatureAuthoringError(f"{name}.entrypoints may not repeat an engine entrypoint.")
    changes_raw = item["changes"]
    if not isinstance(changes_raw, list) or len(changes_raw) > MAX_CHANGES:
        raise FeatureAuthoringError(f"{name}.changes must be an array with at most {MAX_CHANGES} entries.")
    changes: list[dict[str, Any]] = []
    for position, change in enumerate(changes_raw):
        changes.append(require_object(change, name=f"{name}.changes[{position}]"))
    verification = require_object(item["verification"], name=f"{name}.verification")
    reject_unknown_fields(verification, name=f"{name}.verification", allowed={"tests", "require_blueprint"})
    if "tests" not in verification or "require_blueprint" not in verification:
        raise FeatureAuthoringError(f"{name}.verification must contain tests and require_blueprint.")
    tests_raw = verification["tests"]
    if not isinstance(tests_raw, list) or len(tests_raw) > MAX_TESTS:
        raise FeatureAuthoringError(f"{name}.verification.tests must be an array with at most {MAX_TESTS} paths.")
    tests: list[str] = []
    for position, test in enumerate(tests_raw):
        checked = require_string(test, name=f"{name}.verification.tests[{position}]", maximum=500).replace("\\", "/")
        if SAFE_TEST_RE.fullmatch(checked) is None:
            raise FeatureAuthoringError(f"{name}.verification.tests[{position}] must be a safe build/test_*.py path.")
        tests.append(checked)
    if len(set(tests)) != len(tests):
        raise FeatureAuthoringError(f"{name}.verification.tests may not repeat a test path.")
    requires_blueprint = verification["require_blueprint"]
    if not isinstance(requires_blueprint, bool):
        raise FeatureAuthoringError(f"{name}.verification.require_blueprint must be a boolean.")
    raw = {
        "schema": FEATURE_INTENT_SCHEMA,
        "id": identifier,
        "title": require_string(item["title"], name=f"{name}.title", maximum=200),
        "status": status,
        "description": require_text(item["description"], name=f"{name}.description", maximum=MAX_DESCRIPTION_LENGTH),
        "entrypoints": list(entrypoints),
        "changes": changes,
        "verification": {"tests": tests, "require_blueprint": requires_blueprint},
    }
    if blueprint_id is not None:
        raw["blueprint_id"] = blueprint_id
    return FeatureIntent(
        id=identifier,
        title=raw["title"],
        status=status,
        description=raw["description"],
        blueprint_id=blueprint_id,
        entrypoints=entrypoints,
        changes=tuple(changes),
        tests=tuple(tests),
        require_blueprint=requires_blueprint,
        raw=raw,
    )


def load_feature_catalog(root: Path) -> tuple[FeatureIntent, ...]:
    path = root / FEATURE_CATALOG_RELATIVE
    catalog = load_json_object(path, label="feature authoring catalog")
    if catalog.get("schema") != FEATURE_CATALOG_SCHEMA:
        raise FeatureAuthoringError("Feature authoring catalog has an unsupported schema.")
    rows = catalog.get("features")
    if not isinstance(rows, list):
        raise FeatureAuthoringError("Feature authoring catalog must contain a features array.")
    if len(rows) > MAX_FEATURES:
        raise FeatureAuthoringError(f"Feature authoring catalog exceeds the {MAX_FEATURES}-feature safety limit.")
    features: list[FeatureIntent] = []
    seen: set[str] = set()
    for position, row in enumerate(rows):
        intent = normalize_feature_intent(row, name=f"features[{position}]")
        if intent.id in seen:
            raise FeatureAuthoringError(f"Feature authoring catalog repeats feature id: {intent.id}")
        seen.add(intent.id)
        features.append(intent)
    return tuple(features)


def build_feature_authoring(root: Path = DEFAULT_REPO_ROOT) -> FeatureAuthoringIndex:
    """Build the linked Feature Authoring registry without importing module source."""

    resolved_root = root.resolve()
    router = change_router.build_change_router(resolved_root)
    signature = (router.signature, catalog_signature(resolved_root))
    cached = _CACHE.get(resolved_root)
    if cached is not None and cached[0] == signature:
        return cached[1]
    atlas = module_atlas.build_module_atlas(resolved_root)
    dialogues = dialogue_composer.build_dialogue_composer(resolved_root)
    layouts = presentation_layout.build_presentation_layout(resolved_root)
    blueprints = module_blueprint.build_module_blueprints(resolved_root)
    families = load_families(resolved_root)
    entrypoints, registry_warnings = build_entrypoints(router, atlas, dialogues, layouts, families)
    _, id_by_symbol = order_control.parse_id_tables(resolved_root)
    features = load_feature_catalog(resolved_root)
    index = FeatureAuthoringIndex(
        root=resolved_root,
        router=router,
        atlas=atlas,
        dialogues=dialogues,
        layouts=layouts,
        blueprints=blueprints,
        families=families,
        entrypoints=entrypoints,
        by_entrypoint_id={entry.id: entry for entry in entrypoints},
        features=features,
        features_by_id={feature.id: feature for feature in features},
        id_by_symbol=id_by_symbol,
        warnings=[
            "Feature intents are compiled to existing specialist semantic editors; they do not replace canonical src/ fragments or their modular ordering.",
            "Operation JSON has no raw Python expression or tuple field. Typed operands are rendered and revalidated by the target semantic editor.",
            "A feature may describe many source fragments, but each real source apply is deliberately one reviewed SHA-guarded target at a time.",
            *registry_warnings,
        ],
    )
    _CACHE[resolved_root] = (signature, index)
    return index


def invalidate_feature_authoring(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def require_entrypoint(index: FeatureAuthoringIndex, entrypoint_id: Any) -> Entrypoint:
    checked = require_string(entrypoint_id, name="entrypoint_id", maximum=600)
    if not checked.startswith("entrypoint:"):
        raise FeatureAuthoringError("entrypoint_id must be an engine entrypoint ID returned by entrypoint_find.")
    entry = index.by_entrypoint_id.get(checked)
    if entry is None:
        raise FeatureAuthoringError("Unknown engine entrypoint; refresh entrypoint_find before planning a feature change.")
    return entry


def engine_id_symbols(entry: Entrypoint) -> tuple[str, ...]:
    """Return definition symbols, not every referenced symbol in an entrypoint."""

    prefixes = {
        "script": ("script_",),
        "engine-callback": ("script_",),
        "menu": ("mnu_",),
        "mission": ("mt_",),
        "presentation": ("prsnt_",),
        "quest": ("qst_",),
        "constant": ("",),
    }
    values = [entry.name]
    for prefix in prefixes.get(entry.family, ()):
        values.append(prefix + entry.name)
    return tuple(dict.fromkeys(values))


def generated_id_payload(index: FeatureAuthoringIndex, entry: Entrypoint) -> list[dict[str, Any]]:
    values: dict[tuple[str, str, int], order_control.IdEntry] = {}
    for symbol in engine_id_symbols(entry):
        for variant in order_control.id_symbol_variants(symbol):
            for row in index.id_by_symbol.get(variant, ()):
                values[(row.table, row.symbol, row.value)] = row
    return [
        {"table": row.table, "symbol": row.symbol, "value": row.value, "line": row.line}
        for row in sorted(values.values(), key=lambda item: (item.table.casefold(), item.value, item.symbol))
    ]


def entrypoint_metadata_payload(entry: Entrypoint) -> dict[str, Any]:
    metadata = dict(entry.metadata)
    route_ids = metadata.get("route_ids")
    if isinstance(route_ids, tuple):
        metadata["route_ids"] = list(route_ids[:20])
        metadata["route_ids_truncated"] = len(route_ids) > 20
    return metadata


def entrypoint_payload(index: FeatureAuthoringIndex, entry: Entrypoint) -> dict[str, Any]:
    sources = [source_fragment_payload(index.router, path) for path in entry.source_paths]
    semantic_fingerprint = digest(
        {
            "id": entry.id,
            "family": entry.family,
            "name": entry.name,
            "sources": sources,
            "symbols": list(entry.symbols),
            "metadata": entrypoint_metadata_payload(entry),
            "generated_ids": generated_id_payload(index, entry),
        }
    )
    return {
        "entrypoint_id": entry.id,
        "family": entry.family,
        "title": entry.title,
        "description": entry.description,
        "name": entry.name,
        "entity_id": entry.entity_id,
        "target_ids": list(entry.target_ids),
        "source": {
            "paths": sources,
            "line": entry.line,
            "section_order": entry.source_order,
        },
        "symbol_count": len(entry.symbols),
        "symbols": list(entry.symbols[:80]),
        "symbols_truncated": len(entry.symbols) > 80,
        "metadata": entrypoint_metadata_payload(entry),
        "generated_ids": generated_id_payload(index, entry),
        "semantic_fingerprint": semantic_fingerprint,
    }


def feature_payload(intent: FeatureIntent) -> dict[str, Any]:
    return {
        "schema": FEATURE_INTENT_SCHEMA,
        "id": intent.id,
        "title": intent.title,
        "status": intent.status,
        "description": intent.description,
        "blueprint_id": intent.blueprint_id,
        "entrypoint_count": len(intent.entrypoints),
        "entrypoints": list(intent.entrypoints),
        "change_count": len(intent.changes),
        "verification": {"tests": list(intent.tests), "require_blueprint": intent.require_blueprint},
        "intent_fingerprint": digest(intent.raw),
    }


def resolve_intent(
    index: FeatureAuthoringIndex,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
) -> FeatureIntent:
    if (feature_id is None) == (intent_value is None):
        raise FeatureAuthoringError("Supply exactly one of feature_id or intent.")
    if feature_id is not None:
        identifier = require_feature_id(feature_id)
        intent = index.features_by_id.get(identifier)
        if intent is None:
            raise FeatureAuthoringError("Unknown feature id; use feature_summary or feature_find.")
        return intent
    return normalize_feature_intent(intent_value, name="intent")


def feature_summary(index: FeatureAuthoringIndex, *, limit: int = 30) -> dict[str, Any]:
    maximum = require_limit(limit)
    family_counts = Counter(entry.family for entry in index.entrypoints)
    features = sorted(index.features, key=lambda item: (item.status != "active", item.id))
    return {
        "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
        "feature_count": len(index.features),
        "returned_feature_count": min(len(features), maximum),
        "features_truncated": len(features) > maximum,
        "features": [feature_payload(feature) for feature in features[:maximum]],
        "engine_entrypoint_count": len(index.entrypoints),
        "entrypoint_count_by_family": dict(sorted(family_counts.items())),
        "family_catalog": [
            {
                "id": family.id,
                "title": family.title,
                "source_area": family.source_area,
                "entity_kind": family.entity_kind,
                "trace": family.trace,
            }
            for family in sorted(index.families.values(), key=lambda item: item.id)
        ],
        "simple_workflow": [
            "feature_explain or feature_intent_validate: select a feature or submit its structured intent.",
            "feature_plan: inspect exact source diffs, engine traces, ordering, and verification obligations without writing.",
            "feature_apply: rehearse or apply one reviewed plan change using both feature-plan and source-SHA guards.",
            "feature_verify: re-check declared contracts and focused tests after a reviewed source change.",
        ],
        "warnings": index.warnings,
    }


def feature_find(index: FeatureAuthoringIndex, query: str, *, limit: int = 30) -> dict[str, Any]:
    needle = require_string(query, name="query").casefold()
    maximum = require_limit(limit)
    matched = [
        feature
        for feature in index.features
        if needle in "\n".join(
            (
                feature.id,
                feature.title,
                feature.description,
                feature.blueprint_id or "",
                *feature.entrypoints,
                *feature.tests,
            )
        ).casefold()
    ]
    matched.sort(key=lambda item: (item.status != "active", item.id))
    return {
        "query": query,
        "match_count": len(matched),
        "returned_count": min(len(matched), maximum),
        "truncated": len(matched) > maximum,
        "features": [feature_payload(feature) for feature in matched[:maximum]],
        "warnings": index.warnings,
    }


def entrypoint_find(
    index: FeatureAuthoringIndex,
    query: str | None = None,
    *,
    family: str = "all",
    limit: int = 30,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    if family != "all" and family not in index.families:
        raise FeatureAuthoringError("family must be 'all' or a registered engine entrypoint family.")
    needle = require_string(query, name="query").casefold() if query is not None else None
    matched: list[Entrypoint] = []
    for entry in index.entrypoints:
        if family != "all" and entry.family != family:
            continue
        searchable = "\n".join((entry.id, entry.family, entry.title, entry.description, entry.name, *entry.source_paths, *entry.symbols)).casefold()
        if needle is not None and needle not in searchable:
            continue
        matched.append(entry)
    matched.sort(key=lambda item: (item.family, item.name.casefold(), item.id))
    return {
        "query": query,
        "family": family,
        "match_count": len(matched),
        "returned_count": min(len(matched), maximum),
        "truncated": len(matched) > maximum,
        "entrypoints": [entrypoint_payload(index, entry) for entry in matched[:maximum]],
        "warnings": index.warnings,
    }


def compact_entity(value: Mapping[str, Any]) -> dict[str, Any]:
    source = value.get("source") if isinstance(value.get("source"), Mapping) else {}
    return {
        "entity_id": value.get("entity_id"),
        "kind": value.get("kind"),
        "name": value.get("name"),
        "source": {
            "path": source.get("path"),
            "line": source.get("line"),
            "section_order": source.get("section_order"),
        },
    }


def compact_graph(value: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    nodes = value.get("nodes") if isinstance(value.get("nodes"), list) else []
    edges = value.get("edges") if isinstance(value.get("edges"), list) else []
    return {
        "root_entity_id": value.get("root_entity_id"),
        "direction": value.get("direction"),
        "depth": value.get("depth"),
        "node_count": value.get("node_count", len(nodes)),
        "edge_count": value.get("edge_count", len(edges)),
        "truncated": bool(value.get("truncated")) or len(nodes) > limit or len(edges) > limit * 2,
        "nodes": [compact_entity(node) for node in nodes[:limit] if isinstance(node, Mapping)],
        "edges": edges[: limit * 2],
    }


def compact_operation_summary(entity: Mapping[str, Any], *, limit: int) -> dict[str, Any]:
    blocks = entity.get("blocks") if isinstance(entity.get("blocks"), list) else []
    summarized = []
    for block in blocks[:8]:
        if not isinstance(block, Mapping):
            continue
        operations = block.get("operations") if isinstance(block.get("operations"), list) else []
        summarized.append(
            {
                "name": block.get("name"),
                "operation_count": block.get("operation_count", len(operations)),
                "operations_truncated": bool(block.get("operations_truncated")) or len(operations) > limit,
                "operations": [
                    {"index": item.get("index"), "name": item.get("name"), "arguments": item.get("arguments", [])}
                    for item in operations[:limit]
                    if isinstance(item, Mapping)
                ],
            }
        )
    return {"entity": compact_entity(entity), "blocks": summarized}


def entrypoint_trace(index: FeatureAuthoringIndex, entry: Entrypoint, *, limit: int = MAX_TRACE_ENTRIES) -> dict[str, Any]:
    """Return bounded static evidence rather than an unbounded raw graph dump."""

    maximum = require_limit(limit, name="limit", maximum=100)
    graph_limit = min(maximum, 12)
    operation_limit = min(maximum, 12)
    if entry.family in {"script", "engine-callback"}:
        raw = module_atlas.script_flow(index.atlas, entry.name, depth=2, max_nodes=graph_limit)
        script = raw.get("script") if isinstance(raw.get("script"), Mapping) else {}
        graph = raw.get("call_graph") if isinstance(raw.get("call_graph"), Mapping) else {}
        return {
            "kind": "script_flow",
            "script": compact_operation_summary(script, limit=operation_limit),
            "operation_summary": raw.get("operation_summary"),
            "call_graph": compact_graph(graph, limit=graph_limit),
            "warnings": raw.get("warnings", []),
        }
    if entry.family == "menu":
        raw = module_atlas.menu_flow(index.atlas, entry.name, depth=2, max_nodes=graph_limit)
        menu = raw.get("menu") if isinstance(raw.get("menu"), Mapping) else {}
        options = raw.get("options") if isinstance(raw.get("options"), list) else []
        graph = raw.get("flow_graph") if isinstance(raw.get("flow_graph"), Mapping) else {}
        return {
            "kind": "menu_flow",
            "menu": compact_operation_summary(menu, limit=operation_limit),
            "option_count": len(options),
            "options": [compact_operation_summary(option, limit=operation_limit) for option in options[:maximum] if isinstance(option, Mapping)],
            "options_truncated": len(options) > maximum,
            "flow_graph": compact_graph(graph, limit=graph_limit),
            "warnings": raw.get("warnings", []),
        }
    if entry.family == "simple-trigger":
        assert entry.entity_id is not None
        raw = module_atlas.trigger_timeline(index.atlas, entity_id=entry.entity_id, limit=1)
        triggers = raw.get("triggers") if isinstance(raw.get("triggers"), list) else []
        rows = []
        for item in triggers[:1]:
            if not isinstance(item, Mapping):
                continue
            trigger = item.get("trigger") if isinstance(item.get("trigger"), Mapping) else {}
            rows.append({"interval": item.get("interval"), "trigger": compact_operation_summary(trigger, limit=operation_limit), "outbound": item.get("outbound", [])[:maximum]})
        return {"kind": "trigger_timeline", "trigger_count": raw.get("match_count", len(rows)), "triggers": rows, "warnings": raw.get("warnings", [])}
    if entry.family == "mission":
        raw = module_atlas.mission_timeline(index.atlas, entry.name, depth=2, max_nodes=graph_limit)
        mission = raw.get("mission_template") if isinstance(raw.get("mission_template"), Mapping) else {}
        timeline = raw.get("timeline") if isinstance(raw.get("timeline"), list) else []
        return {
            "kind": "mission_timeline",
            "mission_template": compact_operation_summary(mission, limit=operation_limit),
            "trigger_count": raw.get("trigger_count", len(timeline)),
            "timeline": [
                {"trigger_entity_id": item.get("trigger_entity_id"), "event": item.get("event"), "interval": item.get("interval"), "repeat": item.get("repeat")}
                for item in timeline[:maximum]
                if isinstance(item, Mapping)
            ],
            "timeline_truncated": len(timeline) > maximum,
            "flow_graph": compact_graph(raw.get("flow_graph", {}), limit=graph_limit) if isinstance(raw.get("flow_graph"), Mapping) else {},
            "warnings": raw.get("warnings", []),
        }
    if entry.family == "mission-callback":
        mission_id = entry.metadata.get("mission_template")
        if not isinstance(mission_id, str):
            raise FeatureAuthoringError("Mission callback registry entry lacks its mission-template parent.")
        parent = next((candidate for candidate in index.entrypoints if candidate.family == "mission" and candidate.name == mission_id), None)
        parent_trace = entrypoint_trace(index, parent, limit=maximum) if parent is not None else {"available": False}
        return {"kind": "mission_callback", "callback": entrypoint_payload(index, entry), "mission_timeline": parent_trace}
    if entry.family == "dialogue-state":
        route_ids = entry.metadata.get("route_ids", ())
        routes = [index.dialogues.by_id[route_id] for route_id in route_ids if route_id in index.dialogues.by_id]
        model_summary: dict[str, Any]
        try:
            model_index = dialogue_model_checker.build_dialogue_model(index.root)
            model = dialogue_model_checker.state_payload(model_index, entry.name, limit=maximum)
            model_summary = {
                "available": True,
                "state": model.get("state"),
                "mode": model.get("mode"),
                "route_count": model.get("route_count"),
                "finding_count": model.get("finding_count"),
                "finding_codes": [item.get("code") for item in model.get("findings", []) if isinstance(item, Mapping)][:maximum],
            }
        except dialogue_model_checker.DialogueModelError as error:
            model_summary = {"available": False, "reason": str(error)}
        return {
            "kind": "dialogue_state",
            "state": entry.name,
            "route_count": len(routes),
            "returned_route_count": min(len(routes), maximum),
            "routes_truncated": len(routes) > maximum,
            "routes": [
                {
                    "route_id": route.id,
                    "speaker": route.speaker,
                    "text": route.text,
                    "output_state": route.output_state,
                    "source": {"path": route.path, "line": route.line, "section_order": route.source_order},
                    "condition_count": len(route.condition_operations),
                    "consequence_count": len(route.consequence_operations),
                }
                for route in routes[:maximum]
            ],
            "model_checker": model_summary,
            "warnings": ["Dialogue states are first-match for NPC routes and source-order display groups for player choices."],
        }
    if entry.family == "presentation":
        key = entry.metadata.get("presentation_key")
        if not isinstance(key, str):
            raise FeatureAuthoringError("Presentation registry entry lacks a presentation key.")
        raw = presentation_layout.presentation_canvas(index.layouts, key, overlay_limit=maximum)
        overlays = raw.get("overlays") if isinstance(raw.get("overlays"), list) else []
        return {
            "kind": "presentation_canvas",
            "presentation": raw.get("presentation"),
            "canvas": raw.get("canvas"),
            "overlay_count": raw.get("overlay_count", len(overlays)),
            "overlays": overlays[:maximum],
            "overlays_truncated": len(overlays) > maximum,
            "findings": raw.get("findings", [])[:maximum],
            "warnings": raw.get("warnings", []),
        }
    if entry.family in {"quest", "constant"}:
        raw = module_atlas.entity_references(index.atlas, entry.name, limit=maximum)
        definitions = raw.get("definitions") if isinstance(raw.get("definitions"), list) else []
        references = raw.get("references") if isinstance(raw.get("references"), list) else []
        return {
            "kind": "entity_references",
            "symbol": raw.get("symbol"),
            "definition_count": raw.get("definition_count", len(definitions)),
            "definitions": [compact_entity(value) for value in definitions if isinstance(value, Mapping)],
            "reference_count": raw.get("reference_count", len(references)),
            "references": [compact_entity(value) for value in references[:maximum] if isinstance(value, Mapping)],
            "references_truncated": raw.get("references_truncated", False),
        }
    raise FeatureAuthoringError(f"Unsupported engine entrypoint trace family: {entry.family}")


def entrypoint_explain(index: FeatureAuthoringIndex, entrypoint_id: str, *, limit: int = MAX_TRACE_ENTRIES) -> dict[str, Any]:
    entry = require_entrypoint(index, entrypoint_id)
    return {
        "entrypoint": entrypoint_payload(index, entry),
        "static_execution_trace": entrypoint_trace(index, entry, limit=limit),
        "warnings": [
            *index.warnings,
            "This trace is source/static evidence. It makes entrypoint ownership, ordering, and known links explicit but never claims to emulate an in-game save or every engine branch.",
        ],
    }


def require_entrypoint_target(change: Mapping[str, Any], index: FeatureAuthoringIndex, *, name: str) -> Entrypoint:
    target = require_string(change.get("target"), name=f"{name}.target", maximum=600)
    return require_entrypoint(index, target)


def require_number(value: Any, *, name: str) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FeatureAuthoringError(f"{name} must be a finite number.")
    if not math.isfinite(value):
        raise FeatureAuthoringError(f"{name} must be a finite number.")
    if abs(value) > 1_000_000:
        raise FeatureAuthoringError(f"{name} exceeds the engine-layout safety range of +/-1,000,000.")
    return value


def source_reference(value: Any, *, name: str, allowed_prefixes: tuple[str, ...] | None = None) -> str:
    """Extract a literal ID from a typed reference operand for APIs that quote it themselves."""

    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"reference"})
    reference = require_identifier(item.get("reference"), name=f"{name}.reference", pattern=REFERENCE_RE)
    if allowed_prefixes is not None and not reference.startswith(allowed_prefixes):
        raise FeatureAuthoringError(f"{name}.reference must start with one of: " + ", ".join(allowed_prefixes))
    return reference


def require_position(value: Any, *, name: str, values: tuple[str, ...]) -> str:
    checked = require_string(value, name=name, maximum=20)
    if checked not in values:
        raise FeatureAuthoringError(f"{name} must be one of: " + ", ".join(values))
    return checked


def compile_menu_option(spec: Any, *, name: str) -> dict[str, Any]:
    item = require_object(spec, name=name)
    reject_unknown_fields(item, name=name, allowed={"id", "text", "conditions", "consequences"})
    return {
        "id": require_identifier(item.get("id"), name=f"{name}.id"),
        "text": require_text(item.get("text"), name=f"{name}.text"),
        "conditions": render_operations(item.get("conditions", []), name=f"{name}.conditions"),
        "consequences": render_operations(item.get("consequences", []), name=f"{name}.consequences"),
    }


def compile_mission_trigger(spec: Any, *, name: str) -> dict[str, Any]:
    item = require_object(spec, name=name)
    reject_unknown_fields(item, name=name, allowed={"event", "interval", "repeat", "conditions", "consequences"})
    event = item.get("event")
    event_value = normalize_ir_operand(event, name=f"{name}.event")
    if not isinstance(event, dict) or set(event) != {"symbol"}:
        raise FeatureAuthoringError(f"{name}.event must be a {{\"symbol\": \"ti_*\"}} operand.")
    return {
        "event": event_value,
        "interval": normalize_ir_operand(item.get("interval", 0), name=f"{name}.interval"),
        "repeat": normalize_ir_operand(item.get("repeat", 0), name=f"{name}.repeat"),
        "conditions": render_operations(item.get("conditions", []), name=f"{name}.conditions"),
        "consequences": render_operations(item.get("consequences", []), name=f"{name}.consequences"),
    }


def compile_presentation_trigger(spec: Any, *, name: str) -> dict[str, Any]:
    """Compile a top-level presentation callback from typed operation IR."""

    item = require_object(spec, name=name)
    reject_unknown_fields(item, name=name, allowed={"event", "operations"})
    event = item.get("event")
    event_value = normalize_ir_operand(event, name=f"{name}.event")
    if (
        not isinstance(event, dict)
        or set(event) != {"symbol"}
        or not isinstance(event.get("symbol"), str)
        or not event["symbol"].startswith("ti_")
    ):
        raise FeatureAuthoringError(f"{name}.event must be a {{\"symbol\": \"ti_*\"}} operand.")
    return {
        "event": event_value,
        "operations": render_operations(item.get("operations", []), name=f"{name}.operations"),
    }


def compile_module_new_item(action: str, value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    if action == "add_constant":
        reject_unknown_fields(item, name=name, allowed={"name", "expression"})
        return {
            "name": require_identifier(item.get("name"), name=f"{name}.name"),
            "value": normalize_ir_operand(item.get("expression"), name=f"{name}.expression"),
        }
    if action == "add_script":
        reject_unknown_fields(item, name=name, allowed={"id", "operations"})
        return {
            "id": require_identifier(item.get("id"), name=f"{name}.id"),
            "operations": render_operations(item.get("operations", []), name=f"{name}.operations"),
        }
    if action == "add_simple_trigger":
        reject_unknown_fields(item, name=name, allowed={"interval", "operations"})
        return {
            "interval": normalize_ir_operand(item.get("interval", 1), name=f"{name}.interval"),
            "operations": render_operations(item.get("operations", []), name=f"{name}.operations"),
        }
    if action == "add_menu_option":
        return compile_menu_option(item, name=name)
    if action == "add_menu":
        reject_unknown_fields(item, name=name, allowed={"id", "flags", "text", "mesh", "on_enter", "options"})
        options = item.get("options", [])
        if not isinstance(options, list) or len(options) > 100:
            raise FeatureAuthoringError(f"{name}.options must be an array with at most 100 menu options.")
        return {
            "id": require_identifier(item.get("id"), name=f"{name}.id"),
            "flags": normalize_ir_operand(item.get("flags", 0), name=f"{name}.flags"),
            "text": require_text(item.get("text"), name=f"{name}.text"),
            "mesh": require_identifier(item.get("mesh", "none"), name=f"{name}.mesh"),
            "on_enter": render_operations(item.get("on_enter", []), name=f"{name}.on_enter"),
            "options": [compile_menu_option(option, name=f"{name}.options[{position}]") for position, option in enumerate(options)],
        }
    if action == "add_quest":
        reject_unknown_fields(item, name=name, allowed={"id", "title", "flags", "description"})
        return {
            "id": require_identifier(item.get("id"), name=f"{name}.id"),
            "title": require_text(item.get("title"), name=f"{name}.title"),
            "flags": normalize_ir_operand(item.get("flags", 0), name=f"{name}.flags"),
            "description": require_text(item.get("description"), name=f"{name}.description"),
        }
    if action == "add_mission_trigger":
        return compile_mission_trigger(item, name=name)
    if action == "add_mission_template":
        reject_unknown_fields(item, name=name, allowed={"id", "flags", "scene", "description", "spawn_records", "triggers"})
        triggers = item.get("triggers", [])
        if not isinstance(triggers, list) or len(triggers) > 100:
            raise FeatureAuthoringError(f"{name}.triggers must be an array with at most 100 callback blocks.")
        return {
            "id": require_identifier(item.get("id"), name=f"{name}.id"),
            "flags": normalize_ir_operand(item.get("flags", 0), name=f"{name}.flags"),
            "scene": normalize_ir_operand(item.get("scene", -1), name=f"{name}.scene"),
            "description": require_text(item.get("description"), name=f"{name}.description"),
            "spawn_records": normalize_ir_operand(item.get("spawn_records", {"list": []}), name=f"{name}.spawn_records"),
            "triggers": [compile_mission_trigger(trigger, name=f"{name}.triggers[{position}]") for position, trigger in enumerate(triggers)],
        }
    if action == "add_presentation":
        reject_unknown_fields(item, name=name, allowed={"id", "flags", "mesh", "triggers"})
        mesh = item.get("mesh", {"symbol": "mesh_load_window"})
        rendered_mesh = normalize_ir_operand(mesh, name=f"{name}.mesh")
        if (
            not isinstance(mesh, dict)
            or set(mesh) != {"symbol"}
            or not isinstance(mesh.get("symbol"), str)
            or not mesh["symbol"].startswith("mesh_")
        ):
            raise FeatureAuthoringError(f"{name}.mesh must be a {{\"symbol\": \"mesh_*\"}} operand.")
        triggers = item.get("triggers", [])
        if not isinstance(triggers, list) or len(triggers) > 100:
            raise FeatureAuthoringError(f"{name}.triggers must be an array with at most 100 callback blocks.")
        return {
            "id": require_identifier(item.get("id"), name=f"{name}.id"),
            "flags": normalize_ir_operand(item.get("flags", 0), name=f"{name}.flags"),
            "mesh": rendered_mesh,
            "triggers": [compile_presentation_trigger(trigger, name=f"{name}.triggers[{position}]") for position, trigger in enumerate(triggers)],
        }
    raise FeatureAuthoringError(f"Unsupported module new-item action: {action}")


def entity_for_entrypoint(index: FeatureAuthoringIndex, entry: Entrypoint, *, name: str) -> module_atlas.ModuleEntity:
    if entry.entity_id is None:
        raise FeatureAuthoringError(f"{name}.target must resolve to an Atlas-backed engine entrypoint.")
    return module_atlas.require_entity(index.atlas, entry.entity_id)


def compile_module_change(
    index: FeatureAuthoringIndex,
    change: Mapping[str, Any],
    *,
    name: str,
) -> tuple[Entrypoint, str, list[dict[str, Any]], dict[str, Any]]:
    reject_unknown_fields(
        change,
        name=name,
        allowed={"kind", "target", "action", "field", "block", "position", "operation_index", "operation", "operations", "text", "expression", "interval", "new_item"},
    )
    entry = require_entrypoint_target(change, index, name=name)
    action = require_string(change.get("action"), name=f"{name}.action", maximum=80)
    if action not in module_atlas.VALID_ACTIONS:
        raise FeatureAuthoringError(f"{name}.action is not a supported Module Atlas action.")
    if action == "add_presentation":
        # Presentation entrypoints intentionally originate in Presentation
        # Layout, where an existing screen can own several source-level
        # details and therefore has no Atlas entity ID.  New-presentation
        # creation is the narrow exception: resolve the one matching Atlas
        # presentation solely as an append anchor, while keeping every edit of
        # an existing layout in the Presentation Layout specialist.
        if entry.family != "presentation":
            raise FeatureAuthoringError(f"{name}.target must be a presentation entrypoint for add_presentation.")
        candidates = [
            candidate
            for candidate in index.atlas.entities
            if candidate.area == "presentations" and candidate.kind == "presentation" and candidate.name == entry.name and candidate.path in entry.source_paths
        ]
        if len(candidates) != 1:
            raise FeatureAuthoringError(
                f"{name}.target must resolve to one unique Atlas presentation append anchor; found {len(candidates)} candidate(s)."
            )
        entity = candidates[0]
    else:
        entity = entity_for_entrypoint(index, entry, name=name)
    # Deletion and reordering have specialized lifecycle/order controls.  Do
    # not let a feature intent turn a generated plan into a broad migration.
    if action in {"remove_entity", "remove_menu_option", "remove_mission_trigger"}:
        raise FeatureAuthoringError(
            f"{name}.action={action!r} is intentionally outside Feature IR. Use the dedicated Atlas/Order plan after migrating references."
        )
    kwargs: dict[str, Any] = {}
    if action == "set_text":
        kwargs["value"] = require_text(change.get("text"), name=f"{name}.text")
        if "field" in change:
            kwargs["field"] = require_identifier(change["field"], name=f"{name}.field")
    elif action == "set_expression":
        kwargs["value"] = normalize_ir_operand(change.get("expression"), name=f"{name}.expression")
        if "field" in change:
            kwargs["field"] = require_identifier(change["field"], name=f"{name}.field")
    elif action == "replace_operations":
        kwargs["block"] = require_identifier(change.get("block"), name=f"{name}.block")
        kwargs["value"] = render_operations(change.get("operations"), name=f"{name}.operations")
    elif action == "insert_operation":
        kwargs["block"] = require_identifier(change.get("block"), name=f"{name}.block")
        kwargs["operation"] = render_operation(change.get("operation"), name=f"{name}.operation")
        kwargs["position"] = require_position(change.get("position", "end"), name=f"{name}.position", values=("start", "end"))
    elif action == "remove_operation":
        kwargs["block"] = require_identifier(change.get("block"), name=f"{name}.block")
        operation_index = change.get("operation_index")
        if isinstance(operation_index, bool) or not isinstance(operation_index, int) or operation_index < 0:
            raise FeatureAuthoringError(f"{name}.operation_index must be a zero-based non-negative integer.")
        kwargs["operation_index"] = operation_index
    elif action == "set_trigger_interval":
        kwargs["value"] = normalize_ir_operand(change.get("interval"), name=f"{name}.interval")
    elif action.startswith("add_"):
        kwargs["new_item"] = compile_module_new_item(action, change.get("new_item"), name=f"{name}.new_item")
    else:
        raise FeatureAuthoringError(f"{name}.action={action!r} is not available through typed Feature IR.")
    try:
        edits, semantic = module_atlas.semantic_edits(index.atlas, entity, action=action, **kwargs)
    except module_atlas.ModuleAtlasError as error:
        raise FeatureAuthoringError(f"{name}: {error}") from error
    return entry, entity.target_id, edits, {"backend": "module_atlas", **semantic}


def resolve_dialogue_route(
    index: FeatureAuthoringIndex,
    entry: Entrypoint,
    selector_value: Any,
    *,
    name: str,
) -> dialogue_composer.DialogueRoute:
    selector = require_object(selector_value, name=name)
    reject_unknown_fields(selector, name=name, allowed={"route_id", "speaker", "text", "output_state", "path"})
    route_id = selector.get("route_id")
    if route_id is not None:
        try:
            route = dialogue_composer.require_route(index.dialogues, route_id)
        except dialogue_composer.DialogueComposerError as error:
            raise FeatureAuthoringError(f"{name}: {error}") from error
    else:
        if not selector:
            raise FeatureAuthoringError(f"{name} must contain route_id or at least one exact selector field.")
        matches = [route for route in index.dialogues.routes if route.input_state == entry.name]
        for field in ("speaker", "text", "output_state", "path"):
            raw = selector.get(field)
            if raw is None:
                continue
            checked = require_string(raw, name=f"{name}.{field}", maximum=MAX_TEXT_LENGTH)
            matches = [route for route in matches if getattr(route, field if field != "path" else "path") == checked]
        if len(matches) != 1:
            raise FeatureAuthoringError(
                f"{name} resolved to {len(matches)} routes in dialogue state {entry.name!r}; make the selector exact or use dialogue_find's route_id."
            )
        route = matches[0]
    if route.input_state != entry.name:
        raise FeatureAuthoringError(
            f"{name} selected a route in input state {route.input_state!r}, but target {entry.id!r} owns {entry.name!r}."
        )
    return route


def render_dialogue_speaker(value: Any, *, name: str) -> str:
    rendered = normalize_ir_operand(value, name=name)
    # Dialogue speaker is a source expression, not a quoted speaker label.
    if rendered.startswith('"'):
        raise FeatureAuthoringError(f"{name} must be a symbol/combine expression such as {{\"symbol\": \"anyone\"}}, not a quoted string.")
    return rendered


def render_dialogue_operation_sequence(value: Any, *, name: str) -> list[str]:
    if not isinstance(value, list):
        raise FeatureAuthoringError(f"{name} must be an array of typed operations.")
    if len(value) > MAX_OPERATIONS:
        raise FeatureAuthoringError(f"{name} contains too many operations; maximum is {MAX_OPERATIONS}.")
    return [render_operation(operation, name=f"{name}[{position}]") for position, operation in enumerate(value)]


def compile_dialogue_change(
    index: FeatureAuthoringIndex,
    change: Mapping[str, Any],
    *,
    name: str,
) -> tuple[Entrypoint, str, list[dict[str, Any]], dict[str, Any]]:
    reject_unknown_fields(
        change,
        name=name,
        allowed={
            "kind", "target", "action", "route", "anchor", "position", "text", "state", "operations", "operation", "operation_index", "menu", "speaker", "output_state", "conditions", "consequences", "allow_static_shadow", "shadow_acknowledgement",
        },
    )
    entry = require_entrypoint_target(change, index, name=name)
    if entry.family != "dialogue-state":
        raise FeatureAuthoringError(f"{name}.target must be a dialogue-state entrypoint for a dialogue change.")
    action = require_string(change.get("action"), name=f"{name}.action", maximum=80)
    if action in {"remove_route", "move_route", "add_route"}:
        raise FeatureAuthoringError(
            f"{name}.action={action!r} is intentionally outside Feature IR. Use deterministic dialogue_create_plan or the dedicated order-aware Dialogue Composer route workflow."
        )
    if action == "create_route":
        anchor = resolve_dialogue_route(index, entry, change.get("anchor"), name=f"{name}.anchor")
        position = require_position(change.get("position", "after"), name=f"{name}.position", values=("before", "after"))
        allow_shadow = change.get("allow_static_shadow", False)
        if not isinstance(allow_shadow, bool):
            raise FeatureAuthoringError(f"{name}.allow_static_shadow must be a boolean.")
        acknowledgement = change.get("shadow_acknowledgement")
        if acknowledgement is not None and not isinstance(acknowledgement, str):
            raise FeatureAuthoringError(f"{name}.shadow_acknowledgement must be a string when supplied.")
        spec = {
            "anchor_route_id": anchor.id,
            "position": position,
            "speaker": render_dialogue_speaker(change.get("speaker"), name=f"{name}.speaker"),
            "input_state": entry.name,
            "text": require_text(change.get("text"), name=f"{name}.text"),
            "output_state": require_identifier(change.get("output_state"), name=f"{name}.output_state", pattern=STATE_RE),
            "conditions": render_dialogue_operation_sequence(change.get("conditions", []), name=f"{name}.conditions"),
            "consequences": render_dialogue_operation_sequence(change.get("consequences", []), name=f"{name}.consequences"),
            "allow_static_shadow": allow_shadow,
        }
        if acknowledgement is not None:
            spec["shadow_acknowledgement"] = acknowledgement
        try:
            normalized = dialogue_composer.parse_create_spec(spec)
            _, edits, safety = dialogue_composer.create_route_edits(index.dialogues, normalized)
        except dialogue_composer.DialogueComposerError as error:
            raise FeatureAuthoringError(f"{name}: {error}") from error
        return entry, anchor.target_id, edits, {
            "backend": "dialogue_composer",
            "action": "create_route",
            "anchor_route_id": anchor.id,
            "static_creation_safety": safety,
        }
    route = resolve_dialogue_route(index, entry, change.get("route"), name=f"{name}.route")
    if action not in dialogue_composer.VALID_ACTIONS:
        raise FeatureAuthoringError(f"{name}.action is not a supported Dialogue Composer action.")
    kwargs: dict[str, Any] = {}
    if action == "replace_text":
        kwargs["value"] = require_text(change.get("text"), name=f"{name}.text")
    elif action in {"set_input_state", "set_output_state"}:
        kwargs["value"] = require_identifier(change.get("state"), name=f"{name}.state", pattern=STATE_RE)
    elif action in {"replace_conditions", "replace_consequences"}:
        kwargs["value"] = render_operations(change.get("operations"), name=f"{name}.operations")
    elif action in {"insert_condition", "insert_consequence"}:
        kwargs["operation"] = render_operation(change.get("operation"), name=f"{name}.operation")
        kwargs["position"] = require_position(change.get("position", "end"), name=f"{name}.position", values=("start", "end"))
    elif action in {"remove_condition", "remove_consequence"}:
        operation_index = change.get("operation_index")
        if isinstance(operation_index, bool) or not isinstance(operation_index, int) or operation_index < 0:
            raise FeatureAuthoringError(f"{name}.operation_index must be a zero-based non-negative integer.")
        kwargs["operation_index"] = operation_index
    elif action == "bridge_menu":
        kwargs["value"] = source_reference(change.get("menu"), name=f"{name}.menu", allowed_prefixes=("mnu_",))
        kwargs["position"] = require_position(change.get("position", "end"), name=f"{name}.position", values=("start", "end"))
    else:
        raise FeatureAuthoringError(f"{name}.action={action!r} is not available through typed Feature IR.")
    try:
        edits, semantic = dialogue_composer.semantic_edits(index.dialogues, route, action=action, **kwargs)
    except dialogue_composer.DialogueComposerError as error:
        raise FeatureAuthoringError(f"{name}: {error}") from error
    return entry, route.target_id, edits, {
        "backend": "dialogue_composer",
        **semantic,
        "first_match_analysis": dialogue_composer.route_shadow_analysis(index.dialogues, route),
    }


def resolve_presentation_overlay(
    index: FeatureAuthoringIndex,
    presentation: presentation_layout.Presentation,
    value: Any,
    *,
    name: str,
) -> presentation_layout.Overlay:
    selector = require_object(value, name=name)
    reject_unknown_fields(selector, name=name, allowed={"overlay_id", "identifier", "kind", "trigger"})
    overlay_id = selector.get("overlay_id")
    if overlay_id is not None:
        try:
            overlay = presentation_layout.require_overlay(index.layouts, overlay_id)
        except presentation_layout.PresentationLayoutError as error:
            raise FeatureAuthoringError(f"{name}: {error}") from error
    else:
        if not selector:
            raise FeatureAuthoringError(f"{name} must provide overlay_id or an exact overlay selector.")
        matches = [overlay for overlay in presentation.overlays]
        for field in ("identifier", "kind", "trigger"):
            raw = selector.get(field)
            if raw is None:
                continue
            checked = require_string(raw, name=f"{name}.{field}", maximum=200)
            matches = [overlay for overlay in matches if getattr(overlay, field) == checked]
        if len(matches) != 1:
            raise FeatureAuthoringError(f"{name} resolved to {len(matches)} overlays; make the selector exact or use presentation_find's overlay_id.")
        overlay = matches[0]
    if overlay.presentation_key != presentation.key:
        raise FeatureAuthoringError(f"{name} selects an overlay outside presentation {presentation.id!r}.")
    return overlay


def compile_presentation_overlay(spec: Any, *, name: str) -> dict[str, Any]:
    item = require_object(spec, name=name)
    reject_unknown_fields(
        item,
        name=name,
        allowed={"kind", "destination", "position_register", "x", "y", "size_x", "size_y", "text", "mesh", "minimum", "maximum"},
    )
    kind = require_string(item.get("kind"), name=f"{name}.kind")
    if kind not in {"text", "button", "mesh", "slider"}:
        raise FeatureAuthoringError(f"{name}.kind must be text, button, mesh, or slider.")
    result: dict[str, Any] = {
        "kind": kind,
        "destination": normalize_ir_operand(item.get("destination"), name=f"{name}.destination"),
        "position_register": require_string(item.get("position_register", "pos1"), name=f"{name}.position_register", maximum=20),
        "x": require_number(item.get("x", 500), name=f"{name}.x"),
        "y": require_number(item.get("y", 500), name=f"{name}.y"),
    }
    if REGISTER_RE.fullmatch(result["position_register"]) is None or not result["position_register"].startswith("pos"):
        raise FeatureAuthoringError(f"{name}.position_register must be a position register such as pos1.")
    if ("size_x" in item) != ("size_y" in item):
        raise FeatureAuthoringError(f"{name}.size_x and size_y must be supplied together.")
    if "size_x" in item:
        result["size_x"] = require_number(item["size_x"], name=f"{name}.size_x")
        result["size_y"] = require_number(item["size_y"], name=f"{name}.size_y")
    if kind in {"text", "button"}:
        result["text"] = require_text(item.get("text", ""), name=f"{name}.text")
    if kind == "mesh":
        result["mesh"] = require_identifier(item.get("mesh"), name=f"{name}.mesh")
    if kind == "slider":
        result["minimum"] = require_number(item.get("minimum", 0), name=f"{name}.minimum")
        result["maximum"] = require_number(item.get("maximum", 100), name=f"{name}.maximum")
    return result


def compile_presentation_change(
    index: FeatureAuthoringIndex,
    change: Mapping[str, Any],
    *,
    name: str,
) -> tuple[Entrypoint, str, list[dict[str, Any]], dict[str, Any]]:
    reject_unknown_fields(
        change,
        name=name,
        allowed={"kind", "target", "action", "overlay", "x", "y", "text", "mesh", "expression", "alignment", "trigger", "new_overlay", "new_trigger", "operations"},
    )
    entry = require_entrypoint_target(change, index, name=name)
    if entry.family != "presentation":
        raise FeatureAuthoringError(f"{name}.target must be a presentation entrypoint for a presentation change.")
    key = entry.metadata.get("presentation_key")
    if not isinstance(key, str):
        raise FeatureAuthoringError(f"{name}.target is missing a presentation key.")
    presentation = presentation_layout.resolve_presentation(index.layouts, key)
    action = require_string(change.get("action"), name=f"{name}.action", maximum=80)
    if action not in presentation_layout.VALID_ACTIONS:
        raise FeatureAuthoringError(f"{name}.action is not a supported Presentation Layout action.")
    if action in {"remove_overlay", "remove_trigger"}:
        raise FeatureAuthoringError(
            f"{name}.action={action!r} is intentionally outside Feature IR. Use the dedicated Presentation Layout plan after reviewing consumer impact."
        )
    kwargs: dict[str, Any] = {}
    target = key
    if action == "add_overlay":
        kwargs["new_overlay"] = compile_presentation_overlay(change.get("new_overlay"), name=f"{name}.new_overlay")
        kwargs["trigger"] = require_identifier(change.get("trigger", "ti_on_presentation_load"), name=f"{name}.trigger")
    elif action == "add_trigger":
        trigger = require_object(change.get("new_trigger"), name=f"{name}.new_trigger")
        reject_unknown_fields(trigger, name=f"{name}.new_trigger", allowed={"event", "operations"})
        event = trigger.get("event")
        if not isinstance(event, dict) or set(event) != {"symbol"}:
            raise FeatureAuthoringError(f"{name}.new_trigger.event must be a {{\"symbol\": \"ti_*\"}} operand.")
        kwargs["new_trigger"] = {
            "event": normalize_ir_operand(event, name=f"{name}.new_trigger.event"),
            "operations": render_operations(trigger.get("operations", []), name=f"{name}.new_trigger.operations"),
        }
    elif action == "replace_trigger_operations":
        kwargs["trigger"] = require_identifier(change.get("trigger"), name=f"{name}.trigger")
        kwargs["value"] = render_operations(change.get("operations"), name=f"{name}.operations")
    else:
        overlay = resolve_presentation_overlay(index, presentation, change.get("overlay"), name=f"{name}.overlay")
        target = overlay.id
        if action in {"move_overlay", "resize_overlay"}:
            kwargs["x"] = require_number(change.get("x"), name=f"{name}.x")
            kwargs["y"] = require_number(change.get("y"), name=f"{name}.y")
        elif action == "align_overlay":
            kwargs["alignment"] = require_position(change.get("alignment"), name=f"{name}.alignment", values=("left", "center", "right", "top", "middle", "bottom"))
        elif action == "set_text":
            kwargs["value"] = require_text(change.get("text"), name=f"{name}.text")
        elif action == "set_mesh":
            kwargs["value"] = require_identifier(change.get("mesh"), name=f"{name}.mesh")
        elif action in {"set_color", "set_alpha"}:
            kwargs["value"] = normalize_ir_operand(change.get("expression"), name=f"{name}.expression")
        else:
            raise FeatureAuthoringError(f"{name}.action={action!r} is not available through typed Feature IR.")
    try:
        target_id, edits, semantic = presentation_layout.semantic_edits(index.layouts, target, action=action, **kwargs)
    except presentation_layout.PresentationLayoutError as error:
        raise FeatureAuthoringError(f"{name}: {error}") from error
    return entry, target_id, edits, {"backend": "presentation_layout", **semantic}


def compile_change(
    index: FeatureAuthoringIndex,
    intent: FeatureIntent,
    ordinal: int,
    change_value: Any,
) -> CompiledChange:
    name = f"feature {intent.id!r} change[{ordinal}]"
    change = require_object(change_value, name=name)
    kind = require_string(change.get("kind"), name=f"{name}.kind", maximum=40)
    if kind == "module":
        entry, target_id, edits, semantic = compile_module_change(index, change, name=name)
    elif kind == "dialogue":
        entry, target_id, edits, semantic = compile_dialogue_change(index, change, name=name)
    elif kind == "presentation":
        entry, target_id, edits, semantic = compile_presentation_change(index, change, name=name)
    else:
        raise FeatureAuthoringError(f"{name}.kind must be module, dialogue, or presentation.")
    if entry.id not in intent.entrypoints:
        raise FeatureAuthoringError(
            f"{name}.target={entry.id!r} is not declared in feature.entrypoints. Add ownership/trace evidence before planning a source edit."
        )
    fragment = change_router.target_fragment(index.router, target_id)
    return CompiledChange(
        id=f"feature-change:{ordinal + 1:02d}",
        kind=kind,
        target_entrypoint_id=entry.id,
        target_id=target_id,
        edits=tuple(edits),
        semantic=semantic,
        source_path=fragment.path,
    )


def intent_validation_payload(
    index: FeatureAuthoringIndex,
    intent: FeatureIntent,
    *,
    check_changes: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    for entrypoint_id in intent.entrypoints:
        entry = index.by_entrypoint_id.get(entrypoint_id)
        if entry is None:
            errors.append(
                {
                    "code": "unknown_entrypoint",
                    "message": f"Feature declares unknown engine entrypoint: {entrypoint_id}",
                    "entrypoint_id": entrypoint_id,
                }
            )
        else:
            resolved.append(entrypoint_payload(index, entry))
    if intent.require_blueprint and intent.blueprint_id is None:
        errors.append(
            {
                "code": "blueprint_required",
                "message": "verification.require_blueprint is true but the feature intent does not declare blueprint_id.",
            }
        )
    if intent.blueprint_id is not None and intent.blueprint_id not in index.blueprints.by_id:
        errors.append(
            {
                "code": "unknown_blueprint",
                "message": f"Feature declares unknown Module Blueprint: {intent.blueprint_id}",
            }
        )
    missing_tests = [test for test in intent.tests if not (index.root / test).is_file()]
    for test in missing_tests:
        errors.append({"code": "missing_declared_test", "message": f"Feature declares missing focused test: {test}", "path": test})
    if intent.changes and not intent.tests:
        errors.append(
            {
                "code": "changes_require_tests",
                "message": "A feature intent with source changes must declare at least one focused build/test_*.py verification test.",
            }
        )
    if intent.status == "disabled" and intent.changes:
        warnings.append(
            {
                "code": "disabled_feature_has_changes",
                "message": "Disabled feature intent retains changes for documentation only; feature_apply refuses disabled intents.",
            }
        )
    compiled: list[CompiledChange] = []
    if check_changes and not errors:
        for ordinal, change in enumerate(intent.changes):
            try:
                compiled.append(compile_change(index, intent, ordinal, change))
            except FeatureAuthoringError as error:
                errors.append(
                    {
                        "code": "invalid_typed_change",
                        "message": str(error),
                        "change_id": f"feature-change:{ordinal + 1:02d}",
                    }
                )
    target_counts = Counter(change.target_id for change in compiled)
    for target_id, count in sorted(target_counts.items()):
        if count > 1:
            warnings.append(
                {
                    "code": "same_fragment_sequential_changes",
                    "message": "Several change intents target one source fragment. Their anchors are independently reviewed and applied one at a time; re-plan after each non-dry apply.",
                    "target_id": target_id,
                    "change_count": count,
                }
            )
    return {
        "state": "blocked" if errors else "ready",
        "feature": feature_payload(intent),
        "resolved_entrypoints": resolved,
        "resolved_entrypoint_count": len(resolved),
        "compiled_change_count": len(compiled) if check_changes and not errors else None,
        "errors": errors,
        "warnings": warnings,
    }


def feature_intent_validate(
    index: FeatureAuthoringIndex,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
) -> dict[str, Any]:
    intent = resolve_intent(index, feature_id=feature_id, intent_value=intent_value)
    payload = intent_validation_payload(index, intent, check_changes=True)
    return {
        "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
        **payload,
        "warnings": [*index.warnings, *(warning["message"] for warning in payload["warnings"])],
    }


def blueprint_evidence(index: FeatureAuthoringIndex, intent: FeatureIntent, *, limit: int = 60) -> dict[str, Any] | None:
    if intent.blueprint_id is None:
        return None
    return module_blueprint.blueprint_verify(index.blueprints, intent.blueprint_id, limit=limit)


def build_feature_plan(
    index: FeatureAuthoringIndex,
    intent: FeatureIntent,
    *,
    trace_limit: int = 12,
) -> tuple[dict[str, Any], tuple[CompiledChange, ...]]:
    validation = intent_validation_payload(index, intent, check_changes=False)
    if validation["state"] == "blocked":
        return (
            {
                "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
                "state": "blocked",
                "feature": feature_payload(intent),
                "validation": validation,
                "change_plans": [],
                "warnings": [*index.warnings, "No source plan was produced because the feature intent has unresolved structural errors."],
            },
            (),
        )
    if intent.status == "disabled":
        return (
            {
                "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
                "state": "blocked",
                "feature": feature_payload(intent),
                "validation": validation,
                "change_plans": [],
                "warnings": [*index.warnings, "Disabled feature intents may be inspected but cannot produce source apply plans."],
            },
            (),
        )
    compiled: list[CompiledChange] = []
    errors: list[dict[str, Any]] = []
    for ordinal, change in enumerate(intent.changes):
        try:
            compiled.append(compile_change(index, intent, ordinal, change))
        except FeatureAuthoringError as error:
            errors.append({"code": "invalid_typed_change", "change_id": f"feature-change:{ordinal + 1:02d}", "message": str(error)})
    if errors:
        validation = {**validation, "state": "blocked", "errors": [*validation["errors"], *errors]}
        return (
            {
                "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
                "state": "blocked",
                "feature": feature_payload(intent),
                "validation": validation,
                "change_plans": [],
                "warnings": [*index.warnings, "No source plan was produced because one typed change could not be compiled safely."],
            },
            (),
        )
    change_plans: list[dict[str, Any]] = []
    target_counts = Counter(change.target_id for change in compiled)
    for change in compiled:
        try:
            plan = change_router.patch_plan(index.router, change.target_id, change.edits)
        except change_router.ChangeRouterError as error:
            errors.append({"code": "change_plan_failed", "change_id": change.id, "message": str(error)})
            continue
        same_target_count = target_counts[change.target_id]
        change_plans.append(
            {
                "change_id": change.id,
                "kind": change.kind,
                "target_entrypoint_id": change.target_entrypoint_id,
                "source_path": change.source_path,
                "semantic_operation": dict(change.semantic),
                "change_router_plan": plan,
                "apply_available": True,
                "apply_boundary": (
                    "This is one independently anchored source change. Re-plan after applying any sibling change in the same fragment."
                    if same_target_count > 1
                    else "This is one independently anchored source change."
                ),
            }
        )
    if errors:
        validation = {**validation, "state": "blocked", "errors": [*validation["errors"], *errors]}
        return (
            {
                "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
                "state": "blocked",
                "feature": feature_payload(intent),
                "validation": validation,
                "change_plans": change_plans,
                "warnings": [*index.warnings, "One or more exact source patch plans could not be prepared; do not apply this feature until re-planned cleanly."],
            },
            tuple(compiled),
        )
    traces: list[dict[str, Any]] = []
    trace_errors: list[str] = []
    maximum_trace = require_limit(trace_limit, name="trace_limit", maximum=MAX_TRACE_ENTRIES)
    for entrypoint_id in intent.entrypoints[:maximum_trace]:
        entry = index.by_entrypoint_id[entrypoint_id]
        try:
            traces.append({"entrypoint_id": entrypoint_id, "trace": entrypoint_trace(index, entry, limit=12)})
        except (FeatureAuthoringError, module_atlas.ModuleAtlasError, dialogue_model_checker.DialogueModelError, presentation_layout.PresentationLayoutError) as error:
            trace_errors.append(f"{entrypoint_id}: {error}")
    blueprint = blueprint_evidence(index, intent)
    blueprint_blocked = bool(blueprint and blueprint.get("state") == "blocked" and intent.require_blueprint)
    state = "blocked" if blueprint_blocked else "ready_for_review"
    identity = {
        "intent": intent.raw,
        "plans": [
            {
                "change_id": item["change_id"],
                "plan_id": item["change_router_plan"]["plan_id"],
                "target": item["change_router_plan"]["target"],
            }
            for item in change_plans
        ],
    }
    plan_id = f"feature-plan:{digest(identity)}"
    involved_paths = sorted({change.source_path for change in compiled}, key=str.casefold)
    return (
        {
            "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
            "state": state,
            "plan_id": plan_id,
            "feature": feature_payload(intent),
            "validation": validation,
            "blueprint_evidence": blueprint,
            "change_count": len(change_plans),
            "change_plans": change_plans,
            "source_apply": {
                "available": bool(change_plans) and state == "ready_for_review",
                "scope": "one named change / one modular source target at a time",
                "why": "The legacy module system has order-sensitive source assembly. Independent SHA anchors are safer than pretending a multi-file feature apply is transactional.",
                "required_feature_plan_id": plan_id,
                "dry_run_default": True,
            },
            "source_targets": involved_paths,
            "static_execution_traces": traces,
            "trace_count": len(traces),
            "traces_truncated": len(intent.entrypoints) > maximum_trace,
            "verification_plan": {
                "focused_tests": list(intent.tests),
                "blueprint_required": intent.require_blueprint,
                "recommended_next_tool": "feature_verify",
            },
            "warnings": [
                *index.warnings,
                *(warning["message"] for warning in validation["warnings"]),
                *trace_errors,
                *(
                    ["Blueprint evidence is blocked, so this feature plan cannot be applied until its declared contracts are repaired."]
                    if blueprint_blocked
                    else []
                ),
                "Review each exact unified diff before a non-dry source apply. The Feature Authoring Compiler never writes compile/ or _export/.",
            ],
        },
        tuple(compiled),
    )


def feature_plan(
    index: FeatureAuthoringIndex,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    intent = resolve_intent(index, feature_id=feature_id, intent_value=intent_value)
    payload, _ = build_feature_plan(index, intent, trace_limit=trace_limit)
    return payload


def feature_apply(
    index: FeatureAuthoringIndex,
    *,
    change_id: str,
    expected_feature_plan_id: str,
    expected_sha256: str,
    dry_run: bool = True,
    feature_id: str | None = None,
    intent_value: Any | None = None,
) -> dict[str, Any]:
    """Rehearse or apply one exact change from a reviewed feature plan.

    The one-change boundary is intentional.  A multi-source feature can expose
    many coordinated plans, but a successful file write must never hide a
    partially applied sibling change behind an invented transaction.
    """

    if not isinstance(dry_run, bool):
        raise FeatureAuthoringError("dry_run must be a boolean.")
    checked_change_id = require_string(change_id, name="change_id", maximum=80)
    checked_plan_id = require_string(expected_feature_plan_id, name="expected_feature_plan_id", maximum=120)
    checked_sha = change_router.require_sha256(expected_sha256)
    intent = resolve_intent(index, feature_id=feature_id, intent_value=intent_value)
    payload, compiled = build_feature_plan(index, intent)
    if payload.get("state") != "ready_for_review":
        raise FeatureAuthoringError("Feature plan is not ready for source apply; refresh feature_plan and repair its blocking evidence first.")
    if payload.get("plan_id") != checked_plan_id:
        raise FeatureAuthoringError("expected_feature_plan_id does not match the current deterministic feature plan; refresh and review feature_plan.")
    by_id = {change.id: change for change in compiled}
    selected = by_id.get(checked_change_id)
    if selected is None:
        raise FeatureAuthoringError("change_id is not part of the current feature plan.")
    plan_row = next((row for row in payload["change_plans"] if row["change_id"] == selected.id), None)
    if plan_row is None:
        raise FeatureAuthoringError("Selected change has no current source patch plan; refresh feature_plan.")
    source_plan = plan_row["change_router_plan"]
    if source_plan["target"]["base_sha256"] != checked_sha:
        raise FeatureAuthoringError("expected_sha256 must equal this change plan's current base_sha256.")
    result = change_router.apply_source_edits(
        index.router,
        selected.target_id,
        selected.edits,
        expected_sha256=checked_sha,
        dry_run=dry_run,
    )
    if not dry_run:
        change_router.invalidate_router(index.root)
        module_atlas.invalidate_atlas(index.root)
        dialogue_composer.invalidate_composer(index.root)
        presentation_layout.invalidate_layout(index.root)
        invalidate_feature_authoring(index.root)
    return {
        "feature": feature_payload(intent),
        "feature_plan_id": checked_plan_id,
        "change": {
            "change_id": selected.id,
            "kind": selected.kind,
            "target_entrypoint_id": selected.target_entrypoint_id,
            "source_path": selected.source_path,
            "semantic_operation": dict(selected.semantic),
        },
        "result": result,
        "follow_up": {
            "tool": "feature_verify",
            "feature_id": intent.id,
            "note": "After a non-dry source edit, re-plan any sibling change in the same source fragment, run feature_verify, then intentionally review/build the module. Generated files and exports were not touched here.",
        },
        "warnings": [
            *result["warnings"],
            "Feature apply wrote only the selected canonical src/ fragment when dry_run=false; compile/ and _export/ remain untouched.",
        ],
    }


def run_declared_tests(
    root: Path,
    tests: Sequence[str],
    *,
    timeout_seconds: int,
) -> list[dict[str, Any]]:
    timeout = require_limit(timeout_seconds, name="timeout_seconds", maximum=300)
    rows: list[dict[str, Any]] = []
    for relative in tests:
        path = root / relative
        if not path.is_file():
            rows.append({"path": relative, "passed": False, "reason": "missing declared test"})
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
        except subprocess.TimeoutExpired:
            rows.append({"path": relative, "passed": False, "reason": f"timed out after {timeout} seconds"})
            continue
        output = (completed.stdout + completed.stderr).strip()
        if len(output) > 4_000:
            output = output[:3_997] + "..."
        rows.append(
            {
                "path": relative,
                "passed": completed.returncode == 0,
                "exit_code": completed.returncode,
                "output": output,
            }
        )
    return rows


def feature_verify(
    index: FeatureAuthoringIndex,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    timeout_seconds: int = 90,
    source_limit: int = 24,
) -> dict[str, Any]:
    if not isinstance(run_tests, bool) or not isinstance(stage_build_check, bool):
        raise FeatureAuthoringError("run_tests and stage_build_check must be booleans.")
    intent = resolve_intent(index, feature_id=feature_id, intent_value=intent_value)
    validation = intent_validation_payload(index, intent, check_changes=True)
    blueprint = blueprint_evidence(index, intent)
    errors = list(validation["errors"])
    if blueprint is not None and intent.require_blueprint and blueprint.get("state") == "blocked":
        errors.append({"code": "blueprint_blocked", "message": "Declared Module Blueprint is blocked; inspect blueprint_evidence."})
    source_paths: set[str] = set()
    for entrypoint_id in intent.entrypoints:
        entry = index.by_entrypoint_id.get(entrypoint_id)
        if entry is not None:
            source_paths.update(entry.source_paths)
    source_checks: list[dict[str, Any]] = []
    maximum_sources = require_limit(source_limit, name="source_limit", maximum=80)
    for path in sorted(source_paths, key=str.casefold)[:maximum_sources]:
        fragment = index.router.fragments.get(path)
        if fragment is None:
            errors.append({"code": "missing_source_fragment", "message": f"Entrypoint source fragment is missing: {path}"})
            continue
        verification = change_router.verify_change(
            index.router,
            fragment.id,
            run_tests=False,
            stage_build_check=stage_build_check,
            timeout_seconds=timeout_seconds,
        )
        source_checks.append(
            {
                "path": path,
                "target_id": fragment.id,
                "syntax": verification["syntax"],
                "ordering": verification["ordering"],
                "generated_freshness": verification["generated_freshness"],
                "staged_build": verification["staged_build"],
            }
        )
        if not verification["syntax"].get("passed"):
            errors.append({"code": "source_syntax_failed", "message": f"Source syntax failed for {path}"})
        staged = verification["staged_build"]
        if stage_build_check and staged.get("available") and staged.get("passed") is False:
            errors.append({"code": "staged_build_failed", "message": f"Isolated build failed for {path}"})
    test_results = run_declared_tests(index.root, intent.tests, timeout_seconds=timeout_seconds) if run_tests else []
    if run_tests:
        for result in test_results:
            if not result["passed"]:
                errors.append({"code": "focused_test_failed", "message": f"Focused feature test failed: {result['path']}"})
    return {
        "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
        "state": "passed" if not errors else "blocked",
        "feature": feature_payload(intent),
        "validation": validation,
        "blueprint_evidence": blueprint,
        "source_check_count": len(source_checks),
        "source_checks": source_checks,
        "source_checks_truncated": len(source_paths) > maximum_sources,
        "tests": {
            "declared": list(intent.tests),
            "run": run_tests,
            "results": test_results,
            "passed": all(result["passed"] for result in test_results) if run_tests else None,
        },
        "errors": errors,
        "warnings": [
            *index.warnings,
            "Feature verification proves declared static evidence and optionally isolated builds/focused tests; it does not emulate a save, dynamic engine state, or all runtime branches.",
            "Generated modules and exports are only freshness evidence here. Build them intentionally after reviewing the source change.",
        ],
    }


def feature_semantic_snapshot(
    index: FeatureAuthoringIndex,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
) -> dict[str, Any]:
    """Capture an in-memory feature semantic baseline; it never writes an artifact."""

    intent = resolve_intent(index, feature_id=feature_id, intent_value=intent_value)
    validation = intent_validation_payload(index, intent, check_changes=False)
    entrypoints = [
        entrypoint_payload(index, index.by_entrypoint_id[entrypoint_id])
        for entrypoint_id in intent.entrypoints
        if entrypoint_id in index.by_entrypoint_id
    ]
    plan, _ = build_feature_plan(index, intent, trace_limit=1)
    plan_bases = [
        {
            "change_id": row["change_id"],
            "target": row["change_router_plan"]["target"],
            "plan_id": row["change_router_plan"]["plan_id"],
            "semantic_operation": row["semantic_operation"],
        }
        for row in plan.get("change_plans", [])
    ]
    blueprint = blueprint_evidence(index, intent)
    body = {
        "schema": "sod-modern.feature-semantic-snapshot.v1",
        "feature": feature_payload(intent),
        "validation_state": validation["state"],
        "blueprint": {
            "id": intent.blueprint_id,
            "state": blueprint.get("state") if isinstance(blueprint, dict) else None,
            "fingerprint": digest(blueprint) if blueprint is not None else None,
        },
        "entrypoints": entrypoints,
        "plan_bases": plan_bases,
    }
    return {**body, "snapshot_id": f"feature-snapshot:{digest(body)}", "warnings": index.warnings}


def feature_semantic_diff(
    index: FeatureAuthoringIndex,
    before: Any,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
) -> dict[str, Any]:
    baseline = require_object(before, name="before")
    if baseline.get("schema") != "sod-modern.feature-semantic-snapshot.v1":
        raise FeatureAuthoringError("before must be a feature_semantic_snapshot payload.")
    current = feature_semantic_snapshot(index, feature_id=feature_id, intent_value=intent_value)
    prior_feature = require_object(baseline.get("feature"), name="before.feature")
    if prior_feature.get("id") != current["feature"]["id"]:
        raise FeatureAuthoringError("before snapshot belongs to a different feature intent.")

    def indexed(rows: Any, key: str) -> dict[str, Mapping[str, Any]]:
        if not isinstance(rows, list):
            return {}
        return {str(row.get(key)): row for row in rows if isinstance(row, Mapping) and row.get(key) is not None}

    prior_entries = indexed(baseline.get("entrypoints"), "entrypoint_id")
    current_entries = indexed(current.get("entrypoints"), "entrypoint_id")
    entry_changes: list[dict[str, Any]] = []
    for identifier in sorted(set(prior_entries) | set(current_entries)):
        prior = prior_entries.get(identifier)
        after = current_entries.get(identifier)
        if prior is None:
            entry_changes.append({"kind": "added", "entrypoint_id": identifier, "after": after})
        elif after is None:
            entry_changes.append({"kind": "removed", "entrypoint_id": identifier, "before": prior})
        elif prior.get("semantic_fingerprint") != after.get("semantic_fingerprint"):
            entry_changes.append({"kind": "changed", "entrypoint_id": identifier, "before": prior, "after": after})
    prior_plans = indexed(baseline.get("plan_bases"), "change_id")
    current_plans = indexed(current.get("plan_bases"), "change_id")
    plan_changes: list[dict[str, Any]] = []
    for identifier in sorted(set(prior_plans) | set(current_plans)):
        prior = prior_plans.get(identifier)
        after = current_plans.get(identifier)
        if prior is None:
            plan_changes.append({"kind": "added", "change_id": identifier, "after": after})
        elif after is None:
            plan_changes.append({"kind": "removed", "change_id": identifier, "before": prior})
        elif canonical_json(prior) != canonical_json(after):
            plan_changes.append({"kind": "changed", "change_id": identifier, "before": prior, "after": after})
    blueprint_changed = canonical_json(baseline.get("blueprint")) != canonical_json(current.get("blueprint"))
    return {
        "schema": "sod-modern.feature-semantic-diff.v1",
        "feature_id": current["feature"]["id"],
        "state": "changed" if entry_changes or plan_changes or blueprint_changed else "unchanged",
        "before_snapshot_id": baseline.get("snapshot_id"),
        "after_snapshot_id": current["snapshot_id"],
        "entrypoint_changes": entry_changes,
        "plan_changes": plan_changes,
        "blueprint_changed": blueprint_changed,
        "current_snapshot": current,
        "warnings": [
            *index.warnings,
            "This semantic diff compares declared entrypoint provenance/order/ID evidence and typed patch bases; use semantic_change_diff for a broad cross-workspace comparison.",
        ],
    }


def feature_explain(
    index: FeatureAuthoringIndex,
    *,
    feature_id: str | None = None,
    intent_value: Any | None = None,
    trace_limit: int = 20,
) -> dict[str, Any]:
    intent = resolve_intent(index, feature_id=feature_id, intent_value=intent_value)
    maximum = require_limit(trace_limit, name="trace_limit", maximum=MAX_TRACE_ENTRIES)
    validation = intent_validation_payload(index, intent, check_changes=True)
    traces: list[dict[str, Any]] = []
    trace_errors: list[str] = []
    for entrypoint_id in intent.entrypoints[:maximum]:
        entry = index.by_entrypoint_id.get(entrypoint_id)
        if entry is None:
            continue
        try:
            traces.append({"entrypoint": entrypoint_payload(index, entry), "trace": entrypoint_trace(index, entry, limit=12)})
        except (FeatureAuthoringError, module_atlas.ModuleAtlasError, dialogue_model_checker.DialogueModelError, presentation_layout.PresentationLayoutError) as error:
            trace_errors.append(f"{entrypoint_id}: {error}")
    return {
        "feature_authoring_version": f"devkit.feature-authoring.v{FEATURE_AUTHORING_VERSION}",
        "feature": feature_payload(intent),
        "validation": validation,
        "blueprint_evidence": blueprint_evidence(index, intent),
        "engine_entrypoint_traces": traces,
        "trace_count": len(traces),
        "traces_truncated": len(intent.entrypoints) > maximum,
        "warnings": [*index.warnings, *trace_errors],
    }


def parse_json(value: str, *, name: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise FeatureAuthoringError(f"{name} must contain valid JSON: {error}") from error


def parse_workspace_json_file(root: Path, value: str, *, name: str) -> Any:
    path = Path(require_string(value, name=name, maximum=500))
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise FeatureAuthoringError(f"{name} must be inside this workspace.") from error
    try:
        return parse_json(path.read_text(encoding="utf-8"), name=name)
    except OSError as error:
        raise FeatureAuthoringError(f"Could not read {name}: {error}") from error


def cli_intent(index: FeatureAuthoringIndex, args: argparse.Namespace) -> FeatureIntent:
    values = [args.feature_id is not None, args.intent is not None, args.intent_file is not None]
    if sum(values) != 1:
        raise FeatureAuthoringError("Supply exactly one of --feature-id, --intent, or --intent-file.")
    if args.feature_id is not None:
        return resolve_intent(index, feature_id=args.feature_id)
    value = parse_json(args.intent, name="--intent") if args.intent is not None else parse_workspace_json_file(index.root, args.intent_file, name="--intent-file")
    return resolve_intent(index, intent_value=value)


def write_payload(payload: Mapping[str, Any], output: str | None, root: Path) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output:
        path = change_router.output_path(output, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def add_intent_arguments(parser: argparse.ArgumentParser) -> None:
    intent = parser.add_mutually_exclusive_group(required=True)
    intent.add_argument("--feature-id")
    intent.add_argument("--intent")
    intent.add_argument("--intent-file")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="LLM-first Feature Authoring Compiler for ordered SoD Modern module-system features."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    summary = subparsers.add_parser("summary", help="Summarize feature intents and engine entrypoint coverage.")
    summary.add_argument("--limit", type=int, default=30)
    summary.add_argument("--output")
    find = subparsers.add_parser("find", help="Find a checked-in feature intent.")
    find.add_argument("query")
    find.add_argument("--limit", type=int, default=30)
    find.add_argument("--output")
    entrypoints = subparsers.add_parser("entrypoints", help="Find real engine entrypoints by family/name/source.")
    entrypoints.add_argument("query", nargs="?")
    entrypoints.add_argument("--family", default="all")
    entrypoints.add_argument("--limit", type=int, default=30)
    entrypoints.add_argument("--output")
    entrypoint = subparsers.add_parser("entrypoint", help="Explain one engine entrypoint's static trace.")
    entrypoint.add_argument("entrypoint_id")
    entrypoint.add_argument("--limit", type=int, default=20)
    entrypoint.add_argument("--output")
    explain = subparsers.add_parser("explain", help="Explain a feature's entrypoints, Blueprint, and typed intent validation.")
    add_intent_arguments(explain)
    explain.add_argument("--trace-limit", type=int, default=20)
    explain.add_argument("--output")
    validate = subparsers.add_parser("intent-validate", help="Validate a checked-in or inline feature intent without writing.")
    add_intent_arguments(validate)
    validate.add_argument("--output")
    ir = subparsers.add_parser("ir-render", help="Render a typed operation or operation list to validated M&B source syntax without writing.")
    ir_group = ir.add_mutually_exclusive_group(required=True)
    ir_group.add_argument("--operation")
    ir_group.add_argument("--operations")
    ir.add_argument("--output")
    plan = subparsers.add_parser("plan", help="Compile a feature intent to independent SHA-guarded source patch plans.")
    add_intent_arguments(plan)
    plan.add_argument("--trace-limit", type=int, default=12)
    plan.add_argument("--output")
    apply = subparsers.add_parser("apply", help="Rehearse or apply one reviewed feature change; dry run is the default.")
    add_intent_arguments(apply)
    apply.add_argument("--change-id", required=True)
    apply.add_argument("--expected-feature-plan-id", required=True)
    apply.add_argument("--expected-sha256", required=True)
    apply.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=True)
    apply.add_argument("--output")
    verify = subparsers.add_parser("verify", help="Re-check feature contracts, source syntax, and optional focused tests.")
    add_intent_arguments(verify)
    verify.add_argument("--run-tests", action=argparse.BooleanOptionalAction, default=False)
    verify.add_argument("--stage-build-check", action=argparse.BooleanOptionalAction, default=False)
    verify.add_argument("--timeout-seconds", type=int, default=90)
    verify.add_argument("--source-limit", type=int, default=24)
    verify.add_argument("--output")
    snapshot = subparsers.add_parser("snapshot", help="Capture an in-memory semantic baseline JSON without writing an artifact.")
    add_intent_arguments(snapshot)
    snapshot.add_argument("--output")
    diff = subparsers.add_parser("diff", help="Compare a prior feature snapshot with current semantic evidence.")
    add_intent_arguments(diff)
    before = diff.add_mutually_exclusive_group(required=True)
    before.add_argument("--before")
    before.add_argument("--before-file")
    diff.add_argument("--output")
    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        index = build_feature_authoring(args.root.resolve())
        if command == "summary":
            payload = feature_summary(index, limit=args.limit)
        elif command == "find":
            payload = feature_find(index, args.query, limit=args.limit)
        elif command == "entrypoints":
            payload = entrypoint_find(index, args.query, family=args.family, limit=args.limit)
        elif command == "entrypoint":
            payload = entrypoint_explain(index, args.entrypoint_id, limit=args.limit)
        elif command == "explain":
            intent = cli_intent(index, args)
            payload = feature_explain(index, intent_value=intent.raw, trace_limit=args.trace_limit)
        elif command == "intent-validate":
            intent = cli_intent(index, args)
            payload = feature_intent_validate(index, intent_value=intent.raw)
        elif command == "ir-render":
            if args.operation is not None:
                payload = {"kind": "operation", "source": render_operation(parse_json(args.operation, name="--operation"))}
            else:
                payload = {"kind": "operation_list", "source": render_operations(parse_json(args.operations, name="--operations"))}
        elif command == "plan":
            intent = cli_intent(index, args)
            payload = feature_plan(index, intent_value=intent.raw, trace_limit=args.trace_limit)
        elif command == "apply":
            intent = cli_intent(index, args)
            payload = feature_apply(
                index,
                intent_value=intent.raw,
                change_id=args.change_id,
                expected_feature_plan_id=args.expected_feature_plan_id,
                expected_sha256=args.expected_sha256,
                dry_run=args.dry_run,
            )
        elif command == "verify":
            intent = cli_intent(index, args)
            payload = feature_verify(
                index,
                intent_value=intent.raw,
                run_tests=args.run_tests,
                stage_build_check=args.stage_build_check,
                timeout_seconds=args.timeout_seconds,
                source_limit=args.source_limit,
            )
        elif command == "snapshot":
            intent = cli_intent(index, args)
            payload = feature_semantic_snapshot(index, intent_value=intent.raw)
        else:
            intent = cli_intent(index, args)
            prior = parse_json(args.before, name="--before") if args.before is not None else parse_workspace_json_file(index.root, args.before_file, name="--before-file")
            payload = feature_semantic_diff(index, prior, intent_value=intent.raw)
        write_payload(payload, getattr(args, "output", None), index.root)
    except (
        FeatureAuthoringError,
        change_router.ChangeRouterError,
        module_atlas.ModuleAtlasError,
        module_blueprint.ModuleBlueprintError,
        dialogue_composer.DialogueComposerError,
        dialogue_model_checker.DialogueModelError,
        presentation_layout.PresentationLayoutError,
        order_control.OrderControlError,
    ) as error:
        print(f"feature_authoring: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
