#!/usr/bin/env python3
"""Read-only Module Blueprint Compiler front-end for SoD Modern.

Mount & Blade 1.011 source is intentionally modular, but the old compiler
still assembles it as ordered lists.  A feature can therefore be locally
correct while silently missing a trigger, owning a slot somebody else reuses,
or being placed before the state it expects.  This slice gives a feature one
stable, checked-in identity and proves its declared structural contracts before
any legacy source is changed.

The compiler is a *planner*, not a replacement module generator.  Canonical
``src/`` fragments remain authoritative.  ``compile/`` and ``_export/`` are
reported as downstream impact only; this module never writes any of them (or
module source).  A later guarded authoring slice can consume its plan, but it
must still use Change Router's SHA-guarded source-only apply gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.campaign_state_doctor import campaign_state_doctor  # noqa: E402
from devkit.change_router import change_router  # noqa: E402
from devkit.module_atlas import module_atlas  # noqa: E402
from devkit.slot_lifecycle_lint import slot_lifecycle_lint  # noqa: E402


BLUEPRINT_VERSION = "0.1.0"
CATALOG_RELATIVE = Path("devkit/module_blueprint/blueprints.json")
CATALOG_SCHEMA = "sod-modern.module-blueprint-catalog.v1"
MAX_QUERY_LENGTH = 500
MAX_RESULT_LIMIT = 200
MAX_DESCRIPTION_LENGTH = 2_000
MAX_DECLARATIONS_PER_BLUEPRINT = 100
MAX_LINKS_PER_FRAGMENT = 40
MAX_EVIDENCE_ROWS_PER_CONTRACT = 30
BLUEPRINT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,119}$")
VALID_STATUSES = frozenset({"active", "draft", "disabled"})
VALID_ORDER_RELATIONS = frozenset({"before", "after"})
VALID_AREAS = frozenset(change_router.SOURCE_AREAS)
SEVERITY_RANK = {"error": 0, "warning": 1, "info": 2}


class ModuleBlueprintError(RuntimeError):
    """A Blueprint contract or compiler request is malformed or unsafe."""


@dataclass(frozen=True)
class SymbolRequirement:
    symbol: str
    area: str | None
    kind: str | None
    required: bool


@dataclass(frozen=True)
class SourceAssertion:
    id: str
    path: str
    contains: str


@dataclass(frozen=True)
class OrderConstraint:
    id: str
    target: str
    relation: str
    anchor: str
    reason: str


@dataclass(frozen=True)
class Blueprint:
    id: str
    name: str
    status: str
    description: str
    source_fragments: tuple[str, ...]
    required_symbols: tuple[SymbolRequirement, ...]
    source_assertions: tuple[SourceAssertion, ...]
    order_constraints: tuple[OrderConstraint, ...]
    slot_ownership_rules: tuple[str, ...]
    ai_contracts: tuple[str, ...]
    tests: tuple[str, ...]
    depends_on: tuple[str, ...]


@dataclass(frozen=True)
class BlueprintCatalog:
    path: Path
    sha256: str
    blueprints: tuple[Blueprint, ...]


@dataclass
class ModuleBlueprintIndex:
    root: Path
    catalog: BlueprintCatalog
    router: change_router.RouterIndex
    atlas: module_atlas.ModuleAtlasIndex
    by_id: dict[str, Blueprint]
    slot_lifecycle: slot_lifecycle_lint.SlotLifecycleIndex | None
    state_doctor: campaign_state_doctor.StateDoctorIndex | None
    claim_findings: dict[str, tuple[dict[str, Any], ...]]
    warnings: list[str]


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_string(value: Any, *, name: str, maximum: int = MAX_QUERY_LENGTH) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ModuleBlueprintError(f"{name} must be a non-empty string.")
    checked = value.strip()
    if len(checked) > maximum:
        raise ModuleBlueprintError(f"{name} must be at most {maximum:,} characters.")
    return checked


def require_limit(value: Any, *, name: str = "limit", maximum: int = MAX_RESULT_LIMIT) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ModuleBlueprintError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_identifier(value: Any, *, name: str, pattern: re.Pattern[str] = BLUEPRINT_ID_RE) -> str:
    checked = require_string(value, name=name, maximum=120)
    if pattern.fullmatch(checked) is None:
        raise ModuleBlueprintError(f"{name} must use lower-case stable-id syntax (letters, digits, and hyphens).")
    return checked


def normalize_relative_path(
    value: Any,
    *,
    name: str,
    allowed_prefixes: tuple[str, ...],
    suffix: str = ".py",
) -> str:
    """Accept only a safe repository-relative path in an intentional scope."""

    checked = require_string(value, name=name, maximum=500).replace("\\", "/")
    parts = checked.split("/")
    if (
        checked.startswith("/")
        or ":" in parts[0]
        or any(part in {"", ".", ".."} for part in parts)
        or not checked.endswith(suffix)
        or not checked.startswith(allowed_prefixes)
    ):
        prefixes = ", ".join(allowed_prefixes)
        raise ModuleBlueprintError(f"{name} must be a safe {suffix} path under: {prefixes}.")
    return checked


def require_source_target(value: Any, *, name: str) -> str:
    checked = require_string(value, name=name, maximum=540).replace("\\", "/")
    if not checked.startswith("source:"):
        raise ModuleBlueprintError(f"{name} must be a Change Router source target ID (source:src/...).")
    return "source:" + normalize_relative_path(
        checked.removeprefix("source:"),
        name=name,
        allowed_prefixes=("src/",),
    )


def require_string_list(
    value: Any,
    *,
    name: str,
    maximum_items: int = 100,
    item_maximum: int = MAX_QUERY_LENGTH,
) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > maximum_items:
        raise ModuleBlueprintError(f"{name} must be a list with at most {maximum_items} items.")
    result = tuple(require_string(item, name=f"{name} item", maximum=item_maximum) for item in value)
    if len(set(result)) != len(result):
        raise ModuleBlueprintError(f"{name} may not contain duplicate values.")
    return result


def require_keys(raw: Mapping[str, Any], *, name: str, allowed: Iterable[str]) -> None:
    unknown = sorted(set(raw) - set(allowed))
    if unknown:
        raise ModuleBlueprintError(f"{name} contains unsupported field(s): {', '.join(unknown)}.")


def catalog_path(root: Path, explicit_path: Path | None = None) -> Path:
    candidate = (explicit_path or (root / CATALOG_RELATIVE)).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise ModuleBlueprintError("Blueprint catalog must stay inside the workspace.") from error
    return candidate


def parse_symbol_requirements(raw: Any, *, blueprint_id: str) -> tuple[SymbolRequirement, ...]:
    if not isinstance(raw, list) or len(raw) > MAX_DECLARATIONS_PER_BLUEPRINT:
        raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} required_symbols must be a list with at most {MAX_DECLARATIONS_PER_BLUEPRINT} entries.")
    rows: list[SymbolRequirement] = []
    seen: set[tuple[str, str | None, str | None]] = set()
    for position, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} required_symbols entry {position} must be an object.")
        require_keys(item, name=f"Blueprint {blueprint_id!r} required_symbols entry {position}", allowed=("symbol", "area", "kind", "required"))
        symbol = require_string(item.get("symbol"), name=f"Blueprint {blueprint_id!r} symbol", maximum=220)
        area = item.get("area")
        kind = item.get("kind")
        required = item.get("required", True)
        if area is not None:
            area = require_string(area, name=f"Blueprint {blueprint_id!r} symbol.area", maximum=80)
            if area not in VALID_AREAS:
                raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} symbol.area must be one of: {', '.join(sorted(VALID_AREAS))}.")
        if kind is not None:
            kind = require_string(kind, name=f"Blueprint {blueprint_id!r} symbol.kind", maximum=80)
        if not isinstance(required, bool):
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} symbol.required must be boolean.")
        key = (symbol, area, kind)
        if key in seen:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} duplicates required symbol {symbol!r}.")
        seen.add(key)
        rows.append(SymbolRequirement(symbol=symbol, area=area, kind=kind, required=required))
    return tuple(rows)


def parse_source_assertions(
    raw: Any,
    *,
    blueprint_id: str,
    source_fragments: tuple[str, ...],
) -> tuple[SourceAssertion, ...]:
    if not isinstance(raw, list) or len(raw) > MAX_DECLARATIONS_PER_BLUEPRINT:
        raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} source_assertions must be a list with at most {MAX_DECLARATIONS_PER_BLUEPRINT} entries.")
    rows: list[SourceAssertion] = []
    seen: set[str] = set()
    for position, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} source_assertion {position} must be an object.")
        require_keys(item, name=f"Blueprint {blueprint_id!r} source_assertion {position}", allowed=("id", "path", "contains"))
        identifier = require_identifier(item.get("id"), name=f"Blueprint {blueprint_id!r} source_assertion.id")
        path = normalize_relative_path(item.get("path"), name=f"Blueprint {blueprint_id!r} source_assertion.path", allowed_prefixes=("src/",))
        contains = require_string(item.get("contains"), name=f"Blueprint {blueprint_id!r} source_assertion.contains", maximum=1_000)
        if identifier in seen:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} has duplicate source assertion id {identifier!r}.")
        if path not in source_fragments:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} assertion {identifier!r} must target one of its source_fragments.")
        seen.add(identifier)
        rows.append(SourceAssertion(id=identifier, path=path, contains=contains))
    return tuple(rows)


def parse_order_constraints(
    raw: Any,
    *,
    blueprint_id: str,
    source_fragments: tuple[str, ...],
) -> tuple[OrderConstraint, ...]:
    if not isinstance(raw, list) or len(raw) > MAX_DECLARATIONS_PER_BLUEPRINT:
        raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} order_constraints must be a list with at most {MAX_DECLARATIONS_PER_BLUEPRINT} entries.")
    rows: list[OrderConstraint] = []
    seen: set[str] = set()
    for position, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} order constraint {position} must be an object.")
        require_keys(item, name=f"Blueprint {blueprint_id!r} order constraint {position}", allowed=("id", "target", "relation", "anchor", "reason"))
        identifier = require_identifier(item.get("id"), name=f"Blueprint {blueprint_id!r} order_constraint.id")
        target = require_source_target(item.get("target"), name=f"Blueprint {blueprint_id!r} order_constraint.target")
        relation = require_string(item.get("relation"), name=f"Blueprint {blueprint_id!r} order_constraint.relation", maximum=20)
        anchor = require_source_target(item.get("anchor"), name=f"Blueprint {blueprint_id!r} order_constraint.anchor")
        reason = require_string(item.get("reason"), name=f"Blueprint {blueprint_id!r} order_constraint.reason", maximum=1_000)
        if identifier in seen:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} has duplicate order constraint id {identifier!r}.")
        if relation not in VALID_ORDER_RELATIONS:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} order constraint relation must be before or after.")
        if target.removeprefix("source:") not in source_fragments:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} order constraint {identifier!r} target must be a declared source fragment.")
        if target == anchor:
            raise ModuleBlueprintError(f"Blueprint {blueprint_id!r} order constraint {identifier!r} cannot reference itself.")
        seen.add(identifier)
        rows.append(OrderConstraint(id=identifier, target=target, relation=relation, anchor=anchor, reason=reason))
    return tuple(rows)


def parse_blueprint(raw: Any, *, position: int) -> Blueprint:
    if not isinstance(raw, dict):
        raise ModuleBlueprintError(f"Blueprint entry {position} must be an object.")
    require_keys(
        raw,
        name=f"Blueprint entry {position}",
        allowed=(
            "id",
            "name",
            "status",
            "description",
            "source_fragments",
            "required_symbols",
            "source_assertions",
            "order_constraints",
            "slot_ownership_rules",
            "ai_contracts",
            "tests",
            "depends_on",
        ),
    )
    identifier = require_identifier(raw.get("id"), name=f"Blueprint entry {position}.id")
    name = require_string(raw.get("name"), name=f"Blueprint {identifier!r}.name", maximum=160)
    status = raw.get("status", "active")
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ModuleBlueprintError(f"Blueprint {identifier!r}.status must be active, draft, or disabled.")
    description = require_string(raw.get("description"), name=f"Blueprint {identifier!r}.description", maximum=MAX_DESCRIPTION_LENGTH)
    raw_sources = raw.get("source_fragments")
    if not isinstance(raw_sources, list) or not raw_sources or len(raw_sources) > MAX_DECLARATIONS_PER_BLUEPRINT:
        raise ModuleBlueprintError(f"Blueprint {identifier!r}.source_fragments must be a non-empty list with at most {MAX_DECLARATIONS_PER_BLUEPRINT} entries.")
    source_fragments = tuple(
        normalize_relative_path(value, name=f"Blueprint {identifier!r}.source_fragments item", allowed_prefixes=("src/",))
        for value in raw_sources
    )
    if len(set(source_fragments)) != len(source_fragments):
        raise ModuleBlueprintError(f"Blueprint {identifier!r}.source_fragments may not contain duplicates.")
    required_symbols = parse_symbol_requirements(raw.get("required_symbols", []), blueprint_id=identifier)
    source_assertions = parse_source_assertions(raw.get("source_assertions", []), blueprint_id=identifier, source_fragments=source_fragments)
    order_constraints = parse_order_constraints(raw.get("order_constraints", []), blueprint_id=identifier, source_fragments=source_fragments)
    slot_ownership_rules = require_string_list(raw.get("slot_ownership_rules", []), name=f"Blueprint {identifier!r}.slot_ownership_rules", item_maximum=160)
    ai_contracts = require_string_list(raw.get("ai_contracts", []), name=f"Blueprint {identifier!r}.ai_contracts", item_maximum=160)
    raw_tests = raw.get("tests", [])
    if not isinstance(raw_tests, list) or len(raw_tests) > MAX_DECLARATIONS_PER_BLUEPRINT:
        raise ModuleBlueprintError(f"Blueprint {identifier!r}.tests must be a list with at most {MAX_DECLARATIONS_PER_BLUEPRINT} entries.")
    tests = tuple(
        normalize_relative_path(value, name=f"Blueprint {identifier!r}.tests item", allowed_prefixes=("build/", "devkit/"))
        for value in raw_tests
    )
    if len(set(tests)) != len(tests):
        raise ModuleBlueprintError(f"Blueprint {identifier!r}.tests may not contain duplicates.")
    depends_on = require_string_list(raw.get("depends_on", []), name=f"Blueprint {identifier!r}.depends_on", item_maximum=120)
    if identifier in depends_on:
        raise ModuleBlueprintError(f"Blueprint {identifier!r} cannot depend on itself.")
    return Blueprint(
        id=identifier,
        name=name,
        status=status,
        description=description,
        source_fragments=source_fragments,
        required_symbols=required_symbols,
        source_assertions=source_assertions,
        order_constraints=order_constraints,
        slot_ownership_rules=slot_ownership_rules,
        ai_contracts=ai_contracts,
        tests=tests,
        depends_on=depends_on,
    )


def assert_acyclic(blueprints: Mapping[str, Blueprint]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str, stack: list[str]) -> None:
        if identifier in visited:
            return
        if identifier in visiting:
            cycle = " -> ".join([*stack, identifier])
            raise ModuleBlueprintError(f"Blueprint dependency cycle: {cycle}.")
        visiting.add(identifier)
        for dependency in blueprints[identifier].depends_on:
            if dependency not in blueprints:
                raise ModuleBlueprintError(f"Blueprint {identifier!r} depends on unknown blueprint {dependency!r}.")
            visit(dependency, [*stack, identifier])
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in sorted(blueprints):
        visit(identifier, [])


def load_catalog(root: Path, explicit_path: Path | None = None) -> BlueprintCatalog:
    path = catalog_path(root, explicit_path)
    if not path.is_file():
        raise ModuleBlueprintError(f"Blueprint catalog is absent: {project_relative(path, root)}")
    try:
        raw_bytes = path.read_bytes()
        payload = json.loads(raw_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ModuleBlueprintError(f"Could not read Blueprint catalog {project_relative(path, root)}: {error}") from error
    if not isinstance(payload, dict) or payload.get("schema") != CATALOG_SCHEMA:
        raise ModuleBlueprintError(f"Blueprint catalog must use schema {CATALOG_SCHEMA}.")
    require_keys(payload, name="Blueprint catalog", allowed=("schema", "blueprints"))
    raw_blueprints = payload.get("blueprints")
    if not isinstance(raw_blueprints, list) or not raw_blueprints:
        raise ModuleBlueprintError("Blueprint catalog must contain a non-empty blueprints list.")
    if len(raw_blueprints) > 500:
        raise ModuleBlueprintError("Blueprint catalog supports at most 500 blueprints.")
    blueprints = tuple(parse_blueprint(item, position=position) for position, item in enumerate(raw_blueprints, start=1))
    by_id = {blueprint.id: blueprint for blueprint in blueprints}
    if len(by_id) != len(blueprints):
        raise ModuleBlueprintError("Blueprint IDs must be unique.")
    assert_acyclic(by_id)
    return BlueprintCatalog(path=path, sha256=hashlib.sha256(raw_bytes).hexdigest(), blueprints=blueprints)


def source_ref(path: str | None, line: int | None = None) -> dict[str, Any]:
    return {"path": path, "line": line}


def finding(
    blueprint_id: str,
    *,
    severity: str,
    code: str,
    message: str,
    source: Mapping[str, Any] | None = None,
    evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": f"blueprint:{blueprint_id}:{code}",
        "blueprint_id": blueprint_id,
        "severity": severity,
        "code": code,
        "message": message,
        "source": dict(source) if source is not None else source_ref(None),
    }
    if evidence:
        row["evidence"] = dict(evidence)
    return row


def build_claim_findings(blueprints: Sequence[Blueprint]) -> dict[str, tuple[dict[str, Any], ...]]:
    """Surface feature boundary collisions without guessing a shared owner."""

    by_fragment: dict[str, list[str]] = defaultdict(list)
    by_symbol: dict[tuple[str, str | None, str | None], list[str]] = defaultdict(list)
    for blueprint in blueprints:
        if blueprint.status == "disabled":
            continue
        for path in blueprint.source_fragments:
            by_fragment[path].append(blueprint.id)
        for requirement in blueprint.required_symbols:
            if requirement.required:
                by_symbol[(requirement.symbol, requirement.area, requirement.kind)].append(blueprint.id)
    rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path, identifiers in sorted(by_fragment.items()):
        claimed_by = sorted(identifiers)
        if len(claimed_by) < 2:
            continue
        for identifier in claimed_by:
            rows[identifier].append(
                finding(
                    identifier,
                    severity="warning",
                    code="source_fragment_multi_blueprint_claim",
                    message=f"Source fragment {path} is claimed by multiple active/draft Blueprints; make the shared boundary deliberate.",
                    source=source_ref(path),
                    evidence={"claimed_by": claimed_by},
                )
            )
    for key, identifiers in sorted(by_symbol.items(), key=lambda item: str(item[0])):
        claimed_by = sorted(identifiers)
        if len(claimed_by) < 2:
            continue
        symbol, area, kind = key
        for identifier in claimed_by:
            rows[identifier].append(
                finding(
                    identifier,
                    severity="warning",
                    code="required_symbol_multi_blueprint_claim",
                    message=f"Required symbol {symbol} is claimed by multiple active/draft Blueprints; make the ownership split deliberate.",
                    evidence={"symbol": symbol, "area": area, "kind": kind, "claimed_by": claimed_by},
                )
            )
    return {
        identifier: tuple(sorted(values, key=finding_sort_key))
        for identifier, values in rows.items()
    }


def build_module_blueprints(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    catalog: Path | None = None,
) -> ModuleBlueprintIndex:
    """Build linked Blueprint evidence without importing module fragments or writing files."""

    resolved_root = root.resolve()
    blueprint_catalog = load_catalog(resolved_root, catalog)
    router = change_router.build_change_router(resolved_root)
    atlas = module_atlas.build_module_atlas(resolved_root)
    needs_slots = any(blueprint.slot_ownership_rules for blueprint in blueprint_catalog.blueprints)
    needs_state = needs_slots or any(blueprint.ai_contracts for blueprint in blueprint_catalog.blueprints)
    slot_index = slot_lifecycle_lint.build_slot_lifecycle_lint(resolved_root) if needs_slots else None
    state_index = slot_index.state if slot_index is not None else (campaign_state_doctor.build_state_doctor(resolved_root) if needs_state else None)
    warnings = [
        "Module Blueprints are checked-in feature contracts over authoritative src/ fragments; they never generate, reorder, or write legacy module source.",
        "A ready Blueprint plan proves only declared static links and contracts. It does not emulate a save, every engine branch, or live in-game behavior.",
    ]
    return ModuleBlueprintIndex(
        root=resolved_root,
        catalog=blueprint_catalog,
        router=router,
        atlas=atlas,
        by_id={blueprint.id: blueprint for blueprint in blueprint_catalog.blueprints},
        slot_lifecycle=slot_index,
        state_doctor=state_index,
        claim_findings=build_claim_findings(blueprint_catalog.blueprints),
        warnings=warnings,
    )


def finding_sort_key(item: Mapping[str, Any]) -> tuple[int, str, str, int]:
    source = item.get("source") if isinstance(item.get("source"), Mapping) else {}
    line = source.get("line") if isinstance(source.get("line"), int) else -1
    return (
        SEVERITY_RANK.get(str(item.get("severity")), 3),
        str(item.get("code", "")),
        str(source.get("path", "")),
        line,
    )


def blueprint_definition_payload(blueprint: Blueprint) -> dict[str, Any]:
    return {
        "id": blueprint.id,
        "name": blueprint.name,
        "status": blueprint.status,
        "description": blueprint.description,
        "depends_on": list(blueprint.depends_on),
        "source_fragment_count": len(blueprint.source_fragments),
        "source_fragments": list(blueprint.source_fragments),
        "required_symbol_count": len(blueprint.required_symbols),
        "source_assertion_count": len(blueprint.source_assertions),
        "order_constraint_count": len(blueprint.order_constraints),
        "slot_ownership_rule_count": len(blueprint.slot_ownership_rules),
        "ai_contract_count": len(blueprint.ai_contracts),
        "test_count": len(blueprint.tests),
    }


def fragment_payload(index: ModuleBlueprintIndex, fragment: change_router.SourceFragment) -> dict[str, Any]:
    links = change_router.generated_links_payload(index.router, fragment)
    return {
        "target_id": fragment.id,
        "path": fragment.path,
        "area": fragment.area,
        "kind": fragment.kind,
        "source_order": fragment.order_position,
        "order_policy": fragment.order_policy,
        "sha256": fragment.sha256,
        "line_count": fragment.line_count,
        "syntax_error": fragment.syntax_error,
        "generated_link_count": len(links),
        "returned_generated_link_count": min(len(links), MAX_LINKS_PER_FRAGMENT),
        "generated_links_truncated": len(links) > MAX_LINKS_PER_FRAGMENT,
        "generated_links": links[:MAX_LINKS_PER_FRAGMENT],
        "export_layers": change_router.export_layers(fragment),
    }


def compact_entity_payload(entity: module_atlas.ModuleEntity) -> dict[str, Any]:
    return {
        "entity_id": entity.id,
        "target_id": entity.target_id,
        "area": entity.area,
        "kind": entity.kind,
        "name": entity.name,
        "aliases": list(entity.aliases),
        "source": source_ref(entity.path, entity.line),
    }


def requirement_entities(index: ModuleBlueprintIndex, requirement: SymbolRequirement) -> list[module_atlas.ModuleEntity]:
    rows = list(index.atlas.by_alias.get(requirement.symbol, ()))
    if requirement.area is not None:
        rows = [entity for entity in rows if entity.area == requirement.area]
    if requirement.kind is not None:
        rows = [entity for entity in rows if entity.kind == requirement.kind]
    return sorted(rows, key=lambda entity: (entity.path.casefold(), entity.line, entity.id))


def evaluation_summary(evaluation: Mapping[str, Any]) -> dict[str, Any]:
    findings = list(evaluation.get("findings", []))
    counts = Counter(str(item.get("severity", "info")) for item in findings if isinstance(item, Mapping))
    return {
        **blueprint_definition_payload(evaluation["blueprint"]),
        "state": evaluation["state"],
        "finding_count": len(findings),
        "error_count": counts["error"],
        "warning_count": counts["warning"],
    }


def evaluate_blueprint(index: ModuleBlueprintIndex, blueprint: Blueprint) -> dict[str, Any]:
    """Evaluate one feature contract against exact source/contract evidence."""

    if blueprint.status == "disabled":
        disabled = finding(
            blueprint.id,
            severity="info",
            code="blueprint_disabled",
            message="This Blueprint is disabled and intentionally excluded from verification and compile planning.",
        )
        return {
            "blueprint": blueprint,
            "state": "disabled",
            "source_fragments": [],
            "required_symbols": [],
            "source_assertions": [],
            "order_constraints": [],
            "slot_ownership": [],
            "ai_contracts": [],
            "tests": [],
            "findings": [disabled],
            "warnings": index.warnings,
        }

    findings: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    raw_by_path: dict[str, str] = {}
    for path in blueprint.source_fragments:
        fragment = index.router.fragments.get(path)
        if fragment is None:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="declared_source_fragment_missing",
                    message=f"Declared source fragment is absent from the canonical src/ index: {path}.",
                    source=source_ref(path),
                )
            )
            source_rows.append({"path": path, "target_id": f"source:{path}", "present": False})
            continue
        row = {"present": True, **fragment_payload(index, fragment)}
        source_rows.append(row)
        if fragment.syntax_error is not None:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="declared_source_fragment_syntax_error",
                    message=f"Declared source fragment has a Python syntax error: {fragment.syntax_error}.",
                    source=source_ref(path),
                )
            )
        try:
            raw, _, _ = change_router.read_text_with_encoding(index.root / path)
        except change_router.ChangeRouterError as error:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="declared_source_fragment_unreadable",
                    message=f"Could not read declared source fragment: {error}",
                    source=source_ref(path),
                )
            )
        else:
            raw_by_path[path] = raw

    symbol_rows: list[dict[str, Any]] = []
    for requirement in blueprint.required_symbols:
        matches = requirement_entities(index, requirement)
        row = {
            "symbol": requirement.symbol,
            "area": requirement.area,
            "kind": requirement.kind,
            "required": requirement.required,
            "match_count": len(matches),
            "returned_match_count": min(len(matches), MAX_EVIDENCE_ROWS_PER_CONTRACT),
            "matches_truncated": len(matches) > MAX_EVIDENCE_ROWS_PER_CONTRACT,
            "matches": [compact_entity_payload(entity) for entity in matches[:MAX_EVIDENCE_ROWS_PER_CONTRACT]],
        }
        if not matches:
            if requirement.required:
                findings.append(
                    finding(
                        blueprint.id,
                        severity="error",
                        code="required_symbol_missing",
                        message=f"Required module symbol {requirement.symbol!r} has no unambiguous Atlas definition in the declared scope.",
                        evidence={"symbol": requirement.symbol, "area": requirement.area, "kind": requirement.kind},
                    )
                )
                row["state"] = "missing"
            else:
                row["state"] = "not_present_optional"
        elif len(matches) > 1:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="required_symbol_ambiguous",
                    message=f"Required module symbol {requirement.symbol!r} resolves to {len(matches)} Atlas entities; narrow its declared area/kind before editing.",
                    evidence={"symbol": requirement.symbol, "entity_ids": [entity.id for entity in matches]},
                )
            )
            row["state"] = "ambiguous"
        else:
            row["state"] = "resolved"
        symbol_rows.append(row)

    assertion_rows: list[dict[str, Any]] = []
    for assertion in blueprint.source_assertions:
        raw = raw_by_path.get(assertion.path)
        row = {"id": assertion.id, "path": assertion.path, "contains": assertion.contains}
        if raw is None:
            row["state"] = "not_evaluated_source_unavailable"
        elif assertion.contains in raw:
            row["state"] = "passed"
            row["line"] = raw.count("\n", 0, raw.index(assertion.contains)) + 1
        else:
            row["state"] = "failed"
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="source_assertion_failed",
                    message=f"Source assertion {assertion.id!r} no longer found its literal anchor.",
                    source=source_ref(assertion.path),
                    evidence={"assertion_id": assertion.id, "contains": assertion.contains},
                )
            )
        assertion_rows.append(row)

    order_rows: list[dict[str, Any]] = []
    for constraint in blueprint.order_constraints:
        target_path = constraint.target.removeprefix("source:")
        anchor_path = constraint.anchor.removeprefix("source:")
        target = index.router.fragments.get(target_path)
        anchor = index.router.fragments.get(anchor_path)
        row = {
            "id": constraint.id,
            "target": constraint.target,
            "relation": constraint.relation,
            "anchor": constraint.anchor,
            "reason": constraint.reason,
            "target_source": source_ref(target_path),
            "anchor_source": source_ref(anchor_path),
        }
        if target is None or anchor is None:
            row["state"] = "unresolved"
            missing = target_path if target is None else anchor_path
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="order_constraint_source_missing",
                    message=f"Order constraint {constraint.id!r} references a source fragment absent from the router: {missing}.",
                    source=source_ref(missing),
                )
            )
        elif target.area != anchor.area:
            row["state"] = "incomparable_areas"
            row["target_area"] = target.area
            row["anchor_area"] = anchor.area
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="order_constraint_cross_area",
                    message=f"Order constraint {constraint.id!r} compares independent source areas ({target.area} and {anchor.area}).",
                    source=source_ref(target.path),
                    evidence={"anchor": anchor.path},
                )
            )
        elif target.order_position is None or anchor.order_position is None:
            row["state"] = "unproven"
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="order_constraint_position_unproven",
                    message=f"Order constraint {constraint.id!r} has no deterministic router position for both fragments.",
                    source=source_ref(target.path),
                    evidence={"anchor": anchor.path},
                )
            )
        else:
            passed = target.order_position < anchor.order_position if constraint.relation == "before" else target.order_position > anchor.order_position
            row.update(
                {
                    "target_area": target.area,
                    "target_position": target.order_position,
                    "anchor_position": anchor.order_position,
                    "order_policy": target.order_policy,
                    "state": "passed" if passed else "failed",
                }
            )
            if not passed:
                findings.append(
                    finding(
                        blueprint.id,
                        severity="error",
                        code="order_constraint_failed",
                        message=f"Order constraint {constraint.id!r} is violated: target must be {constraint.relation} its anchor.",
                        source=source_ref(target.path),
                        evidence={"target_position": target.order_position, "anchor": anchor.path, "anchor_position": anchor.order_position},
                    )
                )
        order_rows.append(row)

    slot_rows: list[dict[str, Any]] = []
    rules_by_id = {rule.id: rule for rule in index.slot_lifecycle.rules} if index.slot_lifecycle is not None else {}
    for rule_id in blueprint.slot_ownership_rules:
        rule = rules_by_id.get(rule_id)
        if rule is None:
            slot_rows.append({"id": rule_id, "state": "missing"})
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="slot_ownership_rule_missing",
                    message=f"Declared durable-slot ownership rule {rule_id!r} is not present in Slot Lifecycle Lint.",
                )
            )
            continue
        related = [
            item
            for item in index.slot_lifecycle.findings
            if item.get("ownership_rule") == rule_id
        ]
        errors = [item for item in related if item.get("severity") == "error"]
        warnings = [item for item in related if item.get("severity") == "warning"]
        row = {
            "id": rule_id,
            "state": "failed" if errors else "passed",
            "description": rule.description,
            "finding_count": len(related),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "returned_finding_count": min(len(related), MAX_EVIDENCE_ROWS_PER_CONTRACT),
            "findings_truncated": len(related) > MAX_EVIDENCE_ROWS_PER_CONTRACT,
            "findings": related[:MAX_EVIDENCE_ROWS_PER_CONTRACT],
        }
        if errors:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="slot_ownership_contract_failed",
                    message=f"Declared durable-slot ownership rule {rule_id!r} has {len(errors)} blocking lint finding(s).",
                    evidence={"ownership_rule": rule_id, "finding_ids": [item.get("id") for item in errors]},
                )
            )
        elif warnings:
            findings.append(
                finding(
                    blueprint.id,
                    severity="warning",
                    code="slot_ownership_contract_review",
                    message=f"Declared durable-slot ownership rule {rule_id!r} has {len(warnings)} review finding(s).",
                    evidence={"ownership_rule": rule_id, "finding_ids": [item.get("id") for item in warnings]},
                )
            )
        slot_rows.append(row)

    ai_rows: list[dict[str, Any]] = []
    ai_by_id = {row.get("id"): row for row in (index.state_doctor.contract_results if index.state_doctor is not None else [])}
    for contract_id in blueprint.ai_contracts:
        result = ai_by_id.get(contract_id)
        if result is None:
            ai_rows.append({"id": contract_id, "state": "missing"})
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="ai_intent_contract_missing",
                    message=f"Declared AI intent contract {contract_id!r} is not present in Campaign State Doctor.",
                )
            )
            continue
        passed = result.get("passed") is True
        ai_rows.append(
            {
                "id": contract_id,
                "kind": result.get("kind"),
                "state": "passed" if passed else "failed",
                "violation_count": result.get("violation_count", 0),
                "returned_violation_count": min(len(result.get("violations", [])), MAX_EVIDENCE_ROWS_PER_CONTRACT),
                "violations_truncated": len(result.get("violations", [])) > MAX_EVIDENCE_ROWS_PER_CONTRACT,
                "violations": list(result.get("violations", []))[:MAX_EVIDENCE_ROWS_PER_CONTRACT],
            }
        )
        if not passed:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="ai_intent_contract_failed",
                    message=f"Declared AI intent contract {contract_id!r} failed static validation.",
                    evidence={"contract_id": contract_id, "violation_count": result.get("violation_count", 0)},
                )
            )

    test_rows: list[dict[str, Any]] = []
    for test_path in blueprint.tests:
        exists = (index.root / test_path).is_file()
        test_rows.append(
            {
                "path": test_path,
                "exists": exists,
                "recommended_command": f"py -3 -B {test_path.replace('/', '\\\\')}",
                "execution": "not_run_by_blueprint_compiler",
            }
        )
        if not exists:
            findings.append(
                finding(
                    blueprint.id,
                    severity="error",
                    code="declared_test_missing",
                    message=f"Declared focused test is absent: {test_path}.",
                    source=source_ref(test_path),
                )
            )

    findings.extend(index.claim_findings.get(blueprint.id, ()))
    findings.sort(key=finding_sort_key)
    error_count = sum(1 for item in findings if item.get("severity") == "error")
    state = "ready" if error_count == 0 else "blocked"
    return {
        "blueprint": blueprint,
        "state": state,
        "source_fragments": source_rows,
        "required_symbols": symbol_rows,
        "source_assertions": assertion_rows,
        "order_constraints": order_rows,
        "slot_ownership": slot_rows,
        "ai_contracts": ai_rows,
        "tests": test_rows,
        "findings": findings,
        "warnings": index.warnings,
    }


def evaluate_selected(index: ModuleBlueprintIndex, identifiers: Sequence[str]) -> list[dict[str, Any]]:
    return [evaluate_blueprint(index, index.by_id[identifier]) for identifier in identifiers]


def blueprint_summary(index: ModuleBlueprintIndex, *, limit: int = 50) -> dict[str, Any]:
    maximum = require_limit(limit)
    evaluations = evaluate_selected(index, sorted(index.by_id))
    summaries = [evaluation_summary(evaluation) for evaluation in evaluations]
    status_counts = Counter(blueprint.status for blueprint in index.catalog.blueprints)
    state_counts = Counter(str(evaluation["state"]) for evaluation in evaluations)
    active_errors = sum(
        summary["error_count"]
        for summary, blueprint in zip(summaries, sorted(index.catalog.blueprints, key=lambda item: item.id))
        if blueprint.status == "active"
    )
    return {
        "module_blueprint_version": f"devkit.module-blueprint.v{BLUEPRINT_VERSION}",
        "compiler_mode": "read_only_contract_front_end",
        "catalog": {
            "path": project_relative(index.catalog.path, index.root),
            "sha256": index.catalog.sha256,
            "schema": CATALOG_SCHEMA,
        },
        "coverage": {
            "blueprint_count": len(index.catalog.blueprints),
            "blueprint_statuses": dict(sorted(status_counts.items())),
            "evaluation_states": dict(sorted(state_counts.items())),
            "declared_source_fragment_count": sum(len(item.source_fragments) for item in index.catalog.blueprints),
            "declared_symbol_count": sum(len(item.required_symbols) for item in index.catalog.blueprints),
            "declared_order_constraint_count": sum(len(item.order_constraints) for item in index.catalog.blueprints),
            "declared_slot_ownership_rule_count": sum(len(item.slot_ownership_rules) for item in index.catalog.blueprints),
            "declared_ai_contract_count": sum(len(item.ai_contracts) for item in index.catalog.blueprints),
            "declared_test_count": sum(len(item.tests) for item in index.catalog.blueprints),
        },
        "verification": {
            "state": "blocked" if active_errors else "ready_for_review",
            "active_error_count": active_errors,
            "blueprints": summaries[:maximum],
            "returned_blueprint_count": min(len(summaries), maximum),
            "truncated": len(summaries) > maximum,
        },
        "next_steps": [
            "Use blueprint_explain for a feature's exact source/order/contract evidence.",
            "Use blueprint_compile to assemble a dependency-first, no-write source impact plan before a legacy edit.",
            "Use blueprint_verify after a change; then use Change Router or a specialist semantic editor for any separately reviewed source patch.",
        ],
        "warnings": index.warnings,
    }


def blueprint_find(index: ModuleBlueprintIndex, query: str, *, limit: int = 30) -> dict[str, Any]:
    checked_query = require_string(query, name="query")
    maximum = require_limit(limit)
    needle = checked_query.casefold()
    matches: list[Blueprint] = []
    for blueprint in sorted(index.catalog.blueprints, key=lambda item: item.id):
        haystack = "\n".join(
            [
                blueprint.id,
                blueprint.name,
                blueprint.status,
                blueprint.description,
                *blueprint.source_fragments,
                *(requirement.symbol for requirement in blueprint.required_symbols),
                *blueprint.slot_ownership_rules,
                *blueprint.ai_contracts,
                *blueprint.tests,
                *blueprint.depends_on,
            ]
        ).casefold()
        if needle in haystack:
            matches.append(blueprint)
    rows = [blueprint_definition_payload(blueprint) for blueprint in matches[:maximum]]
    return {
        "query": checked_query,
        "match_count": len(matches),
        "returned_count": len(rows),
        "truncated": len(matches) > maximum,
        "blueprints": rows,
        "warnings": index.warnings,
    }


def require_blueprint(index: ModuleBlueprintIndex, blueprint_id: str) -> Blueprint:
    checked = require_identifier(blueprint_id, name="blueprint_id")
    blueprint = index.by_id.get(checked)
    if blueprint is None:
        raise ModuleBlueprintError(f"Unknown Blueprint ID {checked!r}; use blueprint_find or blueprint_summary first.")
    return blueprint


def blueprint_explain(index: ModuleBlueprintIndex, blueprint_id: str) -> dict[str, Any]:
    blueprint = require_blueprint(index, blueprint_id)
    evaluation = evaluate_blueprint(index, blueprint)
    return {
        "definition": blueprint_definition_payload(blueprint),
        "evaluation": {
            "state": evaluation["state"],
            "source_fragments": evaluation["source_fragments"],
            "required_symbols": evaluation["required_symbols"],
            "source_assertions": evaluation["source_assertions"],
            "order_constraints": evaluation["order_constraints"],
            "slot_ownership": evaluation["slot_ownership"],
            "ai_contracts": evaluation["ai_contracts"],
            "tests": evaluation["tests"],
            "findings": evaluation["findings"],
        },
        "warnings": evaluation["warnings"],
    }


def dependency_order(index: ModuleBlueprintIndex, blueprint_id: str) -> list[str]:
    ordered: list[str] = []
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visited:
            return
        visited.add(identifier)
        for dependency in index.by_id[identifier].depends_on:
            visit(dependency)
        ordered.append(identifier)

    visit(blueprint_id)
    return ordered


def unique_preserving_order(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def blueprint_compile(index: ModuleBlueprintIndex, blueprint_id: str, *, limit: int = 80) -> dict[str, Any]:
    """Create a deterministic, no-write dependency/source impact plan."""

    maximum = require_limit(limit)
    blueprint = require_blueprint(index, blueprint_id)
    if blueprint.status == "disabled":
        raise ModuleBlueprintError(f"Blueprint {blueprint.id!r} is disabled and cannot be compiled into an impact plan.")
    closure = dependency_order(index, blueprint.id)
    evaluations = evaluate_selected(index, closure)
    source_plan: list[dict[str, Any]] = []
    source_owner_ids: dict[str, list[str]] = defaultdict(list)
    for identifier in closure:
        for path in index.by_id[identifier].source_fragments:
            source_owner_ids[path].append(identifier)
    for identifier, evaluation in zip(closure, evaluations):
        for row in evaluation["source_fragments"]:
            path = str(row["path"])
            source_plan.append({"blueprint_ids": unique_preserving_order(source_owner_ids[path]), "declared_by": identifier, **row})
    source_plan.sort(
        key=lambda row: (
            closure.index(str(row["declared_by"])),
            str(row.get("area", "")),
            row.get("source_order") if isinstance(row.get("source_order"), int) else 1_000_000,
            str(row["path"]).casefold(),
        )
    )
    source_plan = [
        row
        for position, row in enumerate(source_plan)
        if not any(existing["path"] == row["path"] for existing in source_plan[:position])
    ]

    generated = unique_preserving_order(
        generated_path
        for row in source_plan
        for generated_path in change_router.GENERATED_BY_AREA.get(str(row.get("area")), ())
    )
    exports = unique_preserving_order(
        f"_export/{export_name}"
        for row in source_plan
        for export_name in change_router.EXPORTS_BY_AREA.get(str(row.get("area")), ())
    )
    test_plan = []
    for identifier in closure:
        for test_path in index.by_id[identifier].tests:
            if test_path not in {row["path"] for row in test_plan}:
                test_plan.append(
                    {
                        "path": test_path,
                        "blueprint_id": identifier,
                        "recommended_command": f"py -3 -B {test_path.replace('/', '\\\\')}",
                        "execution": "not_run_by_blueprint_compiler",
                    }
                )
    all_findings = [item for evaluation in evaluations for item in evaluation["findings"]]
    all_findings.sort(key=finding_sort_key)
    errors = [item for item in all_findings if item.get("severity") == "error"]
    return {
        "compiler": {
            "version": f"devkit.module-blueprint.v{BLUEPRINT_VERSION}",
            "mode": "read_only_contract_front_end",
            "source_authority": "canonical src/ modular fragments",
        },
        "blueprint_id": blueprint.id,
        "state": "ready_for_review" if not errors else "blocked",
        "dependency_order": closure,
        "source_plan": {
            "fragment_count": len(source_plan),
            "fragments": source_plan,
            "generated_modules_affected": generated,
            "exports_affected": exports,
        },
        "contract_plan": {
            "order_constraints": [row for evaluation in evaluations for row in evaluation["order_constraints"]],
            "slot_ownership": [row for evaluation in evaluations for row in evaluation["slot_ownership"]],
            "ai_contracts": [row for evaluation in evaluations for row in evaluation["ai_contracts"]],
        },
        "test_plan": test_plan,
        "validation": {
            "finding_count": len(all_findings),
            "error_count": len(errors),
            "returned_finding_count": min(len(all_findings), maximum),
            "findings_truncated": len(all_findings) > maximum,
            "findings": all_findings[:maximum],
        },
        "source_apply": {
            "available": False,
            "reason": "Blueprint Compiler intentionally plans and validates only. Use Change Router or a specialist semantic editor to review a separate SHA-guarded source-only patch.",
        },
        "warnings": index.warnings,
    }


def blueprint_verify(
    index: ModuleBlueprintIndex,
    blueprint_id: str | None = None,
    *,
    limit: int = 80,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    identifiers = [require_blueprint(index, blueprint_id).id] if blueprint_id is not None else sorted(index.by_id)
    evaluations = evaluate_selected(index, identifiers)
    flattened: list[dict[str, Any]] = []
    active_error_count = 0
    blocking_error_count = 0
    for evaluation in evaluations:
        blueprint = evaluation["blueprint"]
        if blueprint.status == "active":
            active_error_count += sum(1 for item in evaluation["findings"] if item.get("severity") == "error")
        if blueprint.status in ({"active", "draft"} if blueprint_id is not None else {"active"}):
            blocking_error_count += sum(1 for item in evaluation["findings"] if item.get("severity") == "error")
        flattened.extend(evaluation["findings"])
    flattened.sort(key=finding_sort_key)
    summaries = [evaluation_summary(evaluation) for evaluation in evaluations]
    return {
        "blueprint_id": blueprint_id,
        "state": "passed" if blocking_error_count == 0 else "blocked",
        "active_error_count": active_error_count,
        "blocking_error_count": blocking_error_count,
        "blueprint_count": len(evaluations),
        "blueprints": summaries,
        "finding_count": len(flattened),
        "returned_finding_count": min(len(flattened), maximum),
        "findings_truncated": len(flattened) > maximum,
        "findings": flattened[:maximum],
        "warnings": index.warnings,
    }


def render_markdown(payload: Mapping[str, Any], command: str) -> str:
    if command == "summary":
        coverage = payload["coverage"]
        verification = payload["verification"]
        lines = [
            "# Module Blueprint Compiler",
            "",
            "Read-only feature contracts over authoritative modular source.",
            "",
            f"- Blueprints: {coverage['blueprint_count']}; declared source fragments: {coverage['declared_source_fragment_count']}; order contracts: {coverage['declared_order_constraint_count']}.",
            f"- Verification: {verification['state']}; active errors: {verification['active_error_count']}.",
        ]
    elif command == "compile":
        lines = [
            f"# Blueprint plan: {payload['blueprint_id']}",
            "",
            f"- State: {payload['state']}",
            f"- Dependency order: {' -> '.join(payload['dependency_order'])}",
            f"- Source fragments: {payload['source_plan']['fragment_count']}; validation errors: {payload['validation']['error_count']}.",
            "- This is a no-write plan; use a separately reviewed SHA-guarded source patch to edit.",
        ]
    else:
        lines = [f"# Module Blueprint Compiler: {command}", "", "Use JSON output for complete source-mapped evidence."]
    warnings = payload.get("warnings")
    if isinstance(warnings, list) and warnings:
        lines.extend(["", "## Boundaries", "", *(f"- {warning}" for warning in warnings)])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM-first read-only feature Blueprint Compiler for the SoD Modern module system.")
    parser.add_argument("command", choices=("summary", "find", "explain", "compile", "verify"), nargs="?", default="summary")
    parser.add_argument("query", nargs="?", help="Blueprint ID for explain/compile/optional verify, or text for find.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--catalog", type=Path, help="Optional workspace-relative Blueprint catalog path for a fixture or alternate contract set.")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        explicit_catalog = (
            args.catalog.resolve()
            if args.catalog and args.catalog.is_absolute()
            else (root / args.catalog).resolve() if args.catalog else None
        )
        index = build_module_blueprints(root, catalog=explicit_catalog)
        if args.command == "summary":
            payload = blueprint_summary(index, limit=args.limit)
        elif args.command == "find":
            payload = blueprint_find(index, require_string(args.query, name="query"), limit=args.limit)
        elif args.command == "explain":
            payload = blueprint_explain(index, require_string(args.query, name="blueprint_id"))
        elif args.command == "compile":
            payload = blueprint_compile(index, require_string(args.query, name="blueprint_id"), limit=args.limit)
        else:
            payload = blueprint_verify(index, args.query, limit=args.limit)
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except (
        ModuleBlueprintError,
        change_router.ChangeRouterError,
        module_atlas.ModuleAtlasError,
        campaign_state_doctor.CampaignStateError,
        slot_lifecycle_lint.SlotLifecycleError,
    ) as error:
        print(f"module_blueprint: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
