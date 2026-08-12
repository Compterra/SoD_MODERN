#!/usr/bin/env python3
"""Order Control Plane for the Mount & Blade 1.011 module system.

Order is executable behavior in this project: modular manifests determine
assembly order; NPC dialogue is first-match; generated lists yield numeric ID
tables; engine callback scripts use a protected hardcoded slice; and operation
lists execute in sequence.  This module makes those independent order domains
explicit without inventing a generic file sorter.

Primary use is deterministic JSON/MCP.  A human UI may present these results,
but never owns a separate reordering path.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.change_router import change_router
from devkit.dialogue_composer import dialogue_composer
from devkit.module_atlas import module_atlas
from devkit.workspace_audit import workspace_audit


ORDER_CONTROL_VERSION = "0.1.0"
MAX_QUERY_LENGTH = 500
MAX_RESULT_LIMIT = 500
MAX_DIFF_LINES = 1_500
CATALOG_RELATIVE = Path("devkit/order_control/contracts/manifest.json")
BASELINE_RELATIVE = Path("devkit/order_control/baselines")
REPORT_RELATIVE = Path("devkit/order_control/reports")
ID_LINE_RE = re.compile(r"^\s*(?P<symbol>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>-?\d+)\s*$")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
SLUG_RE = re.compile(r"[^a-z0-9]+")
VALID_AREAS = frozenset(workspace_audit.SOURCE_AREAS)
VALID_DOMAINS = frozenset(("all", "source-fragments", "entities", "id-tables", "generated"))
VALID_MOVE_POSITIONS = frozenset(("before", "after"))
ID_SYMBOL_PREFIX_ALIASES = (
    ("mnu_", "menu_"),
    ("menu_", "mnu_"),
    ("mt_", "mst_"),
    ("mst_", "mt_"),
)
_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], "OrderControlIndex"]] = {}


class OrderControlError(RuntimeError):
    """An order request cannot be completed safely or unambiguously."""


@dataclass(frozen=True)
class IdEntry:
    table: str
    symbol: str
    value: int
    line: int


@dataclass(frozen=True)
class ManifestBinding:
    spec_id: str
    area: str
    order_file: str
    path_prefix: str
    policy: str


@dataclass
class OrderControlIndex:
    root: Path
    router: change_router.RouterIndex
    atlas: module_atlas.ModuleAtlasIndex
    dialogues: dialogue_composer.DialogueComposerIndex
    id_tables: dict[str, tuple[IdEntry, ...]]
    id_by_symbol: dict[str, tuple[IdEntry, ...]]
    contracts: dict[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def require_string(value: Any, *, name: str, maximum: int = MAX_QUERY_LENGTH) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OrderControlError(f"{name} must be a non-empty string.")
    value = value.strip()
    if len(value) > maximum:
        raise OrderControlError(f"{name} must be at most {maximum:,} characters.")
    return value


def require_limit(value: int, *, name: str = "limit", maximum: int = MAX_RESULT_LIMIT) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise OrderControlError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_area(value: str) -> str:
    if value not in {"all", *VALID_AREAS}:
        raise OrderControlError("area must be 'all' or one of: " + ", ".join(sorted(VALID_AREAS)))
    return value


def require_domain(value: str) -> str:
    if value not in VALID_DOMAINS:
        raise OrderControlError("domain must be one of: " + ", ".join(sorted(VALID_DOMAINS)))
    return value


def require_position(value: str) -> str:
    if value not in VALID_MOVE_POSITIONS:
        raise OrderControlError("position must be one of: before, after.")
    return value


def require_sha256(value: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value.strip().lower()) is None:
        raise OrderControlError("expected_sha256 must be a 64-character lowercase SHA-256 returned by order_plan_move.")
    return value.strip().lower()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def slugify(value: str) -> str:
    slug = SLUG_RE.sub("-", value.casefold()).strip("-")
    return slug[:80] or "baseline"


def catalog_path(root: Path) -> Path:
    return root / CATALOG_RELATIVE


def order_input_signature(root: Path) -> tuple[tuple[str, int, int], ...]:
    """Return a cheap freshness key for every Order Control evidence layer.

    The specialist indexes already maintain their own deep cache, but calling
    all three builders for every MCP order query still forced three expensive
    whole-workspace signature walks.  One shallow-order cache lets a sequence
    of map/explain/risk/plan calls share the same linked index while retaining
    nanosecond source/generated/catalog freshness checks.
    """

    paths = [
        *root.joinpath("src").rglob("*.py"),
        *root.joinpath("src").rglob("_order*.txt"),
        *root.joinpath("compile").glob("module_*.py"),
        *root.joinpath("compile", "ids").glob("ID_*.py"),
        catalog_path(root),
    ]
    rows: list[tuple[str, int, int]] = []
    for path in sorted(set(paths), key=lambda item: item.as_posix().casefold()):
        try:
            stat = path.stat()
        except OSError:
            continue
        rows.append((path.relative_to(root).as_posix(), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def read_json(path: Path, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise OrderControlError(f"Missing {label}: {project_relative(path, path.parents[3])}") from error
    except (OSError, json.JSONDecodeError) as error:
        raise OrderControlError(f"Could not read {label}: {error}") from error
    if not isinstance(value, dict):
        raise OrderControlError(f"{label} must be a JSON object.")
    return value


def load_contract_catalog(root: Path) -> dict[str, Any]:
    path = catalog_path(root)
    catalog = read_json(path, label="Order Control contract catalog")
    if catalog.get("schema") != "sod-modern.order-control-contract-catalog.v1":
        raise OrderControlError("Order Control contract catalog has an unsupported schema.")
    contracts = catalog.get("contracts")
    if not isinstance(contracts, list):
        raise OrderControlError("Order Control contract catalog must contain a contracts list.")
    identifiers: set[str] = set()
    for item in contracts:
        if not isinstance(item, dict):
            raise OrderControlError("Each Order Control contract must be an object.")
        identifier = require_string(item.get("id"), name="contract.id", maximum=120)
        if identifier in identifiers:
            raise OrderControlError(f"Duplicate Order Control contract id: {identifier}")
        identifiers.add(identifier)
        if item.get("status", "active") not in {"active", "disabled"}:
            raise OrderControlError(f"Contract {identifier!r} status must be active or disabled.")
        require_string(item.get("kind"), name=f"contract {identifier}.kind", maximum=80)
    return catalog


def parse_id_tables(root: Path) -> tuple[dict[str, tuple[IdEntry, ...]], dict[str, tuple[IdEntry, ...]]]:
    """Read generated ID tables without importing their Python source."""

    directory = root / "compile" / "ids"
    tables: dict[str, tuple[IdEntry, ...]] = {}
    by_symbol_raw: dict[str, list[IdEntry]] = defaultdict(list)
    if not directory.is_dir():
        return tables, {}
    for path in sorted(directory.glob("ID_*.py"), key=lambda item: item.name.casefold()):
        try:
            raw, _, _ = change_router.read_text_with_encoding(path)
        except change_router.ChangeRouterError as error:
            raise OrderControlError(str(error)) from error
        relative = project_relative(path, root)
        entries: list[IdEntry] = []
        for line_number, line in enumerate(raw.splitlines(), start=1):
            match = ID_LINE_RE.match(line)
            if match is None:
                continue
            entry = IdEntry(
                table=relative,
                symbol=match.group("symbol"),
                value=int(match.group("value")),
                line=line_number,
            )
            entries.append(entry)
            by_symbol_raw[entry.symbol].append(entry)
        tables[relative] = tuple(entries)
    return tables, {
        symbol: tuple(sorted(entries, key=lambda entry: (entry.table.casefold(), entry.value, entry.line)))
        for symbol, entries in by_symbol_raw.items()
    }


def build_order_control(root: Path = DEFAULT_REPO_ROOT) -> OrderControlIndex:
    """Assemble linked order evidence without importing module fragments or building."""

    root = root.resolve()
    signature = order_input_signature(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == signature:
        return cached[1]
    router = change_router.build_change_router(root)
    atlas = module_atlas.build_module_atlas(root)
    dialogues = dialogue_composer.build_dialogue_composer(root)
    id_tables, id_by_symbol = parse_id_tables(root)
    index = OrderControlIndex(
        root=root,
        router=router,
        atlas=atlas,
        dialogues=dialogues,
        id_tables=id_tables,
        id_by_symbol=id_by_symbol,
        contracts=load_contract_catalog(root),
    )
    _CACHE[root] = (signature, index)
    return index


def invalidate_order_control(root: Path) -> None:
    """Forget one process-local linked order index after a source-order write."""

    _CACHE.pop(root.resolve(), None)


def id_entry_payload(entry: IdEntry) -> dict[str, Any]:
    return {"table": entry.table, "symbol": entry.symbol, "value": entry.value, "line": entry.line}


def id_symbol_variants(symbol: str) -> tuple[str, ...]:
    """Translate source-facing M&B aliases to generated ID-table conventions."""

    values = [symbol]
    for source_prefix, generated_prefix in ID_SYMBOL_PREFIX_ALIASES:
        if symbol.startswith(source_prefix):
            values.append(generated_prefix + symbol[len(source_prefix):])
    return tuple(dict.fromkeys(values))


def id_entries_for_symbols(index: OrderControlIndex, symbols: Iterable[str]) -> list[dict[str, Any]]:
    entries: list[IdEntry] = []
    for symbol in symbols:
        for variant in id_symbol_variants(symbol):
            entries.extend(index.id_by_symbol.get(variant, ()))
    deduplicated = {(entry.table, entry.symbol, entry.value): entry for entry in entries}
    return [id_entry_payload(entry) for entry in sorted(deduplicated.values(), key=lambda entry: (entry.table, entry.value, entry.symbol))]


def fragment_binding(index: OrderControlIndex, fragment: change_router.SourceFragment) -> ManifestBinding | None:
    """Return the exact declared manifest policy that can move this fragment."""

    area_prefix = f"src/{fragment.area}/"
    if not fragment.path.startswith(area_prefix):
        return None
    inside_area = fragment.path[len(area_prefix):]
    candidates: list[ManifestBinding] = []
    for spec in workspace_audit.ORDER_SPECS:
        if spec.get("source_area") != fragment.area:
            continue
        prefix = str(spec.get("path_prefix") or "").replace("\\", "/")
        if prefix and not inside_area.startswith(prefix):
            continue
        candidates.append(
            ManifestBinding(
                spec_id=str(spec["id"]),
                area=fragment.area,
                order_file=str(spec["order_file"]),
                path_prefix=prefix,
                policy=str(spec.get("policy") or ""),
            )
        )
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: len(item.path_prefix), reverse=True)[0]


def fragment_manifest_entry(fragment: change_router.SourceFragment) -> str:
    prefix = f"src/{fragment.area}/"
    if not fragment.path.startswith(prefix):
        raise OrderControlError(f"Fragment {fragment.path!r} is outside its declared source area.")
    return fragment.path[len(prefix):]


def manifest_line_entries(raw: str) -> list[tuple[int, str]]:
    entries: list[tuple[int, str]] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append((line_number, stripped.split()[-1].replace("\\", "/")))
    return entries


def manifest_document(index: OrderControlIndex, binding: ManifestBinding) -> tuple[Path, str, str, bytes, list[tuple[int, str]]]:
    path = (index.root / binding.order_file).resolve()
    source_root = (index.root / "src").resolve()
    try:
        path.relative_to(source_root)
    except ValueError as error:
        raise OrderControlError("Order contract points outside src/.") from error
    if path.name.startswith("_order") is False or path.suffix.casefold() != ".txt":
        raise OrderControlError("Order Control may only change explicit src/**/_order*.txt manifests.")
    try:
        raw, encoding, raw_bytes = change_router.read_text_with_encoding(path)
    except change_router.ChangeRouterError as error:
        raise OrderControlError(str(error)) from error
    return path, raw, encoding, raw_bytes, manifest_line_entries(raw)


def entity_sort_key(entity: module_atlas.ModuleEntity) -> tuple[int, str, int, int, str]:
    return (
        entity.source_order if entity.source_order is not None else 1_000_000,
        entity.path.casefold(),
        entity.line,
        entity.column,
        entity.id,
    )


def entities_in_fragment(index: OrderControlIndex, path: str) -> list[module_atlas.ModuleEntity]:
    return sorted((entity for entity in index.atlas.entities if entity.path == path), key=entity_sort_key)


def entity_ids(index: OrderControlIndex, entity: module_atlas.ModuleEntity) -> list[dict[str, Any]]:
    return id_entries_for_symbols(index, entity.aliases)


def fragment_order_payload(index: OrderControlIndex, fragment: change_router.SourceFragment, *, neighbor_count: int = 5) -> dict[str, Any]:
    order = change_router.order_payload(index.router, fragment, neighbor_count=neighbor_count)
    binding = fragment_binding(index, fragment)
    return {
        "fragment_id": fragment.id,
        "path": fragment.path,
        "area": fragment.area,
        "source_kind": fragment.kind,
        "source_sha256": fragment.sha256,
        "manifest": (
            {
                "contract_id": binding.spec_id,
                "path": binding.order_file,
                "path_prefix": binding.path_prefix,
                "policy": binding.policy,
                "entry": fragment_manifest_entry(fragment),
            }
            if binding
            else None
        ),
        "source_order": order,
        "generated_segments": [
            {
                "compile_path": segment.compile_path,
                "compile_line_start": segment.compile_line_start,
                "compile_line_end": segment.compile_line_end,
            }
            for segment in index.router.generated_by_source.get(fragment.path, ())
        ],
    }


def entity_order_payload(index: OrderControlIndex, entity: module_atlas.ModuleEntity) -> dict[str, Any]:
    peers = sorted(
        (
            candidate
            for candidate in index.atlas.entities
            if candidate.area == entity.area
            and candidate.kind == entity.kind
            and candidate.parent_id == entity.parent_id
        ),
        key=entity_sort_key,
    )
    position = peers.index(entity) + 1
    return {
        "entity_id": entity.id,
        "name": entity.name,
        "kind": entity.kind,
        "area": entity.area,
        "position": position,
        "total": len(peers),
        "previous": [candidate.id for candidate in peers[max(0, position - 4):position - 1]],
        "next": [candidate.id for candidate in peers[position:position + 3]],
        "source": {"path": entity.path, "line": entity.line, "section_order": entity.source_order},
        "id_entries": entity_ids(index, entity),
    }


def route_order_payload(index: OrderControlIndex, route: dialogue_composer.DialogueRoute) -> dict[str, Any]:
    grouped = sorted(
        (
            candidate
            for candidate in index.dialogues.routes
            if candidate.path == route.path
        ),
        key=lambda candidate: (
            candidate.line,
            candidate.column,
            candidate.id,
        ),
    )
    position = grouped.index(route) + 1
    return {
        "route_id": route.id,
        "source_position": position,
        "source_fragment_route_count": len(grouped),
        "previous_route_ids": [candidate.id for candidate in grouped[max(0, position - 4):position - 1]],
        "next_route_ids": [candidate.id for candidate in grouped[position:position + 3]],
        "speaker": route.speaker,
        "input_state": route.input_state,
        "output_state": route.output_state,
        "compiled_order": [
            {"entry_index": item.index, "compile_line": item.compile_line, "is_fallback": item.is_fallback}
            for item in index.dialogues.compiled_by_route.get(route.id, ())
        ],
        "first_match_analysis": dialogue_composer.route_shadow_analysis(index.dialogues, route),
    }


def resolve_target(index: OrderControlIndex, target: str) -> tuple[str, Any]:
    """Resolve one explicit semantic/order target with no broad guesswork."""

    checked = require_string(target, name="target", maximum=2_000)
    if checked.startswith("dialogue:"):
        return "dialogue_route", dialogue_composer.require_route(index.dialogues, checked)
    if checked.startswith("module:"):
        return "module_entity", module_atlas.require_entity(index.atlas, checked)
    if checked.startswith("source:"):
        return "source_fragment", change_router.target_fragment(index.router, checked)
    entries = index.id_by_symbol.get(checked, ())
    if entries:
        if len(entries) > 1:
            raise OrderControlError(f"ID symbol {checked!r} is ambiguous across tables; use an explicit module, dialogue, or source ID.")
        return "id_symbol", entries[0]
    aliases = list(index.atlas.by_alias.get(checked, ()))
    if not aliases:
        aliases = [entity for entity in index.atlas.entities if entity.name == checked]
    if len(aliases) == 1:
        return "module_entity", aliases[0]
    if len(aliases) > 1:
        raise OrderControlError(f"Target {checked!r} resolves to multiple module entities; use module_find and an exact entity_id.")
    raise OrderControlError(f"Unknown order target {checked!r}.")


def manifest_integrity_rows(index: OrderControlIndex) -> dict[str, dict[str, Any]]:
    rows = workspace_audit.ordering_contracts(index.root, maximum=100)
    return {str(row["id"]): row for row in rows}


def prefix_contract_candidates(index: OrderControlIndex, contract: Mapping[str, Any]) -> list[module_atlas.ModuleEntity]:
    area = require_area(str(contract.get("area", "all")))
    if area == "all":
        raise OrderControlError("id-prefix contracts require an exact source area.")
    kind = require_string(contract.get("entity_kind"), name="contract.entity_kind", maximum=80)
    source_prefix = require_string(contract.get("source_prefix"), name="contract.source_prefix", maximum=500).replace("\\", "/")
    name_prefix = str(contract.get("name_prefix", ""))
    candidates = [
        entity
        for entity in index.atlas.entities
        if entity.area == area
        and entity.kind == kind
        and entity.path.startswith(source_prefix)
        and entity.name.startswith(name_prefix)
    ]
    return sorted(candidates, key=entity_sort_key)


def evaluate_id_prefix_contract(index: OrderControlIndex, contract: Mapping[str, Any]) -> dict[str, Any]:
    table = require_string(contract.get("id_table"), name="contract.id_table", maximum=300)
    expected_start = contract.get("expected_start")
    explicit_ids = contract.get("expected_ids")
    if expected_start is not None and explicit_ids is not None:
        raise OrderControlError("id-prefix contract may specify expected_start or expected_ids, not both.")
    if expected_start is not None and (isinstance(expected_start, bool) or not isinstance(expected_start, int) or expected_start < 0):
        raise OrderControlError("id-prefix contract expected_start must be a non-negative integer.")
    if explicit_ids is not None and (
        not isinstance(explicit_ids, list)
        or any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in explicit_ids)
    ):
        raise OrderControlError("id-prefix contract expected_ids must be a list of non-negative integers.")
    if expected_start is None and explicit_ids is None:
        raise OrderControlError("id-prefix contract requires expected_start or expected_ids.")
    candidates = prefix_contract_candidates(index, contract)
    found: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for entity in candidates:
        symbol_candidates = [
            entry
            for alias in entity.aliases
            for variant in id_symbol_variants(alias)
            for entry in index.id_by_symbol.get(variant, ())
            if entry.table == table
        ]
        if len(symbol_candidates) != 1:
            missing.append({"entity_id": entity.id, "aliases": list(entity.aliases), "id_entry_count": len(symbol_candidates)})
            continue
        entry = symbol_candidates[0]
        found.append({"entity_id": entity.id, "name": entity.name, "path": entity.path, "line": entity.line, "symbol": entry.symbol, "id": entry.value})
    expected = (
        list(range(expected_start, expected_start + len(found)))
        if expected_start is not None
        else list(explicit_ids)
    )
    actual = [item["id"] for item in found]
    passed = bool(found) and not missing and len(actual) == len(expected) and actual == expected
    return {
        "passed": passed,
        "table": table,
        "expected_start": expected_start,
        "expected_ids": expected if explicit_ids is not None else None,
        "candidate_count": len(candidates),
        "resolved_count": len(found),
        "missing_id_count": len(missing),
        "entries": found[:120],
        "entries_truncated": len(found) > 120,
        "missing_ids": missing[:60],
        "reason": (
            "All protected entities retain a contiguous generated ID sequence in declared source order."
            if passed
            else "A protected source-order/ID prefix is missing, non-contiguous, or not in declared source order."
        ),
    }


def evaluate_contract(index: OrderControlIndex, contract: Mapping[str, Any], integrity: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    identifier = str(contract["id"])
    status = str(contract.get("status", "active"))
    severity = str(contract.get("severity", "warning"))
    kind = str(contract["kind"])
    if status == "disabled":
        return {"id": identifier, "kind": kind, "severity": severity, "status": status, "passed": None, "detail": "Disabled contract is recorded but not evaluated.", "active_blocker": False}
    if kind == "manifest-integrity":
        spec_ids = contract.get("spec_ids")
        if not isinstance(spec_ids, list) or not spec_ids:
            raise OrderControlError(f"Contract {identifier!r} requires a non-empty spec_ids list.")
        require_complete = bool(contract.get("require_complete", False))
        rows = []
        for spec_id in spec_ids:
            row = integrity.get(str(spec_id))
            if row is None:
                raise OrderControlError(f"Contract {identifier!r} names unknown order spec {spec_id!r}.")
            passed = bool(row["order_file_exists"]) and not row["missing_listed_count"] and not row["duplicate_order_entry_count"]
            if require_complete:
                passed = passed and not row["unlisted_candidate_count"]
            rows.append({"spec_id": spec_id, "passed": passed, "order_file": row["order_file"], "missing_listed_count": row["missing_listed_count"], "duplicate_entry_count": row["duplicate_order_entry_count"], "unlisted_candidate_count": row["unlisted_candidate_count"]})
        passed = all(row["passed"] for row in rows)
        detail: dict[str, Any] = {"require_complete": require_complete, "specs": rows}
    elif kind in {"id-prefix", "engine-callback-sequence"}:
        detail = evaluate_id_prefix_contract(index, contract)
        passed = bool(detail["passed"])
    else:
        raise OrderControlError(f"Contract {identifier!r} has unsupported kind {kind!r}.")
    return {
        "id": identifier,
        "title": str(contract.get("title", identifier)),
        "kind": kind,
        "severity": severity,
        "status": status,
        "passed": passed,
        "active_blocker": severity == "blocker" and not passed,
        "detail": detail,
    }


def order_contracts(index: OrderControlIndex) -> dict[str, Any]:
    integrity = manifest_integrity_rows(index)
    results = [evaluate_contract(index, contract, integrity) for contract in index.contracts["contracts"]]
    active = [result for result in results if result["status"] == "active"]
    blockers = [result for result in active if result["active_blocker"]]
    failed = [result for result in active if result["passed"] is False]
    return {
        "catalog_schema": index.contracts["schema"],
        "summary": {
            "contract_count": len(results),
            "active_contract_count": len(active),
            "failed_contract_count": len(failed),
            "active_blocker_count": len(blockers),
        },
        "contracts": results,
        "manifest_integrity": [integrity[key] for key in sorted(integrity)],
        "warnings": [
            "Order contracts prove declared source/order/ID relationships only; they do not execute engine callbacks or dynamic game branches.",
            "A passing protected prefix does not certify save compatibility; inspect an order diff before accepting generated-ID movement.",
        ],
    }


def source_snapshot(index: OrderControlIndex) -> dict[str, list[str]]:
    return {area: list(index.router.ordering.get(area, ())) for area in sorted(VALID_AREAS)}


def id_snapshot(index: OrderControlIndex) -> dict[str, list[dict[str, Any]]]:
    return {
        table: [{"symbol": entry.symbol, "value": entry.value} for entry in entries]
        for table, entries in sorted(index.id_tables.items())
    }


def order_summary(index: OrderControlIndex) -> dict[str, Any]:
    source = source_snapshot(index)
    contracts = order_contracts(index)
    id_entry_count = sum(len(entries) for entries in index.id_tables.values())
    return {
        "order_control_version": f"devkit.order-control.v{ORDER_CONTROL_VERSION}",
        "source_fragment_order": {
            "area_count": len(source),
            "fragment_count": sum(len(entries) for entries in source.values()),
            "fragment_count_by_area": {area: len(entries) for area, entries in source.items()},
        },
        "authored_order": {
            "entity_count": len(index.atlas.entities),
            "dialogue_route_count": len(index.dialogues.routes),
            "compiled_dialogue_mapping_count": len(index.dialogues.compiled_by_route),
        },
        "generated_ids": {"table_count": len(index.id_tables), "entry_count": id_entry_count},
        "contracts": contracts["summary"],
        "order_domains": [
            {"id": "source-fragments", "meaning": "Explicit modular manifests and the remaining builder ordering policy."},
            {"id": "entities", "meaning": "Authored top-level records, child options/triggers, and sequential operation blocks."},
            {"id": "generated", "meaning": "Compile markers and compiled dialogue order, when generated output is current."},
            {"id": "id-tables", "meaning": "Generated positional numeric IDs; shifts are compatibility-sensitive evidence."},
            {"id": "engine-contracts", "meaning": "Checked-in protected hardcoded callback and legacy prefix contracts."},
        ],
        "warnings": [
            "Order Control does not rename folders, sort files, build, or write generated/export layers.",
            "Only explicit manifest entries and same-fragment dialogue routes have a guarded automatic move path.",
            *contracts["warnings"],
        ],
    }


def text_matches(query: str | None, *values: Any) -> bool:
    if query is None:
        return True
    needle = query.casefold()
    return needle in "\n".join(str(value) for value in values).casefold()


def source_fragment_records(index: OrderControlIndex, area: str, query: str | None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for candidate_area, paths in sorted(index.router.ordering.items()):
        if area != "all" and candidate_area != area:
            continue
        for path in paths:
            fragment = index.router.fragments[path]
            if text_matches(query, path, fragment.order_policy):
                records.append(fragment_order_payload(index, fragment, neighbor_count=2))
    return records


def entity_records(index: OrderControlIndex, area: str, query: str | None) -> list[dict[str, Any]]:
    records = []
    for entity in sorted(index.atlas.entities, key=entity_sort_key):
        if area != "all" and entity.area != area:
            continue
        if text_matches(query, entity.id, entity.name, entity.path, " ".join(entity.aliases)):
            records.append(entity_order_payload(index, entity))
    return records


def id_table_records(index: OrderControlIndex, query: str | None) -> list[dict[str, Any]]:
    records = []
    for table, entries in sorted(index.id_tables.items()):
        for entry in entries:
            if text_matches(query, table, entry.symbol, entry.value):
                records.append(id_entry_payload(entry))
    return records


def generated_records(index: OrderControlIndex, area: str, query: str | None) -> list[dict[str, Any]]:
    records = []
    for source, segments in sorted(index.router.generated_by_source.items()):
        fragment = index.router.fragments.get(source)
        if fragment is None or (area != "all" and fragment.area != area):
            continue
        for segment in segments:
            if text_matches(query, source, segment.compile_path, segment.compile_line_start):
                records.append({"source_fragment_id": fragment.id, "source_path": source, "area": fragment.area, "compile_path": segment.compile_path, "compile_line_start": segment.compile_line_start, "compile_line_end": segment.compile_line_end})
    records.sort(key=lambda item: (item["compile_path"].casefold(), item["compile_line_start"], item["source_path"].casefold()))
    return records


def order_map(
    index: OrderControlIndex,
    *,
    area: str = "all",
    domain: str = "all",
    query: str | None = None,
    limit: int = 60,
) -> dict[str, Any]:
    checked_area = require_area(area)
    checked_domain = require_domain(domain)
    checked_query = require_string(query, name="query") if query is not None else None
    maximum = require_limit(limit)
    if checked_domain == "all" and checked_query is None and checked_area == "all":
        raise OrderControlError("Specify area, domain, or query to keep the order map bounded.")
    groups: list[tuple[str, list[dict[str, Any]]]] = []
    if checked_domain in {"all", "source-fragments"}:
        groups.append(("source-fragments", source_fragment_records(index, checked_area, checked_query)))
    if checked_domain in {"all", "entities"}:
        groups.append(("entities", entity_records(index, checked_area, checked_query)))
    if checked_domain in {"all", "id-tables"}:
        groups.append(("id-tables", id_table_records(index, checked_query)))
    if checked_domain in {"all", "generated"}:
        groups.append(("generated", generated_records(index, checked_area, checked_query)))
    total = sum(len(records) for _, records in groups)
    remaining = maximum
    output = []
    for name, records in groups:
        selected = records[:remaining]
        output.append({"domain": name, "match_count": len(records), "returned_count": len(selected), "truncated": len(records) > len(selected), "records": selected})
        remaining = max(0, remaining - len(selected))
    return {
        "filters": {"area": checked_area, "domain": checked_domain, "query": checked_query},
        "match_count": total,
        "returned_count": sum(item["returned_count"] for item in output),
        "truncated": total > maximum,
        "groups": output,
        "warnings": ["Order map returns bounded static source/generated evidence. Use order_explain for an exact target before proposing a move."],
    }


def relevant_contracts(index: OrderControlIndex, *, area: str | None = None, path: str | None = None, table: str | None = None) -> list[dict[str, Any]]:
    results = []
    for contract in index.contracts["contracts"]:
        if area is not None and contract.get("area") not in {None, area} and "manifest-integrity" != contract.get("kind"):
            continue
        if path is not None and contract.get("source_prefix") and not path.startswith(str(contract["source_prefix"])):
            continue
        if table is not None and contract.get("id_table") not in {None, table}:
            continue
        results.append({"id": contract["id"], "kind": contract["kind"], "severity": contract.get("severity", "warning"), "title": contract.get("title", contract["id"])})
    return results


def order_explain(index: OrderControlIndex, target: str, *, related_limit: int = 40) -> dict[str, Any]:
    maximum = require_limit(related_limit, name="related_limit", maximum=200)
    kind, resolved = resolve_target(index, target)
    if kind == "source_fragment":
        fragment = resolved
        entities = entities_in_fragment(index, fragment.path)
        return {
            "target_kind": kind,
            "fragment": fragment_order_payload(index, fragment),
            "entities": [entity_order_payload(index, entity) for entity in entities[:maximum]],
            "entity_count": len(entities),
            "entities_truncated": len(entities) > maximum,
            "contracts": relevant_contracts(index, area=fragment.area, path=fragment.path),
            "safe_moves": ["manifest_entry_before_after"] if fragment_binding(index, fragment) else [],
            "warnings": ["A fragment move edits only a declared _order manifest line. It does not rename or physically move the fragment file."],
        }
    if kind == "module_entity":
        entity = resolved
        fragment = index.router.fragments[entity.path]
        return {
            "target_kind": kind,
            "entity": entity_order_payload(index, entity),
            "fragment": fragment_order_payload(index, fragment),
            "contracts": relevant_contracts(index, area=entity.area, path=entity.path),
            "delegation": (
                "Use dialogue order target IDs for route first-match ordering."
                if entity.area == "dialogs"
                else "Use source fragment targets to evaluate manifest ordering; generic top-level record reordering has no automatic apply path."
            ),
            "warnings": ["Entity ordering is evidence only unless a specialist semantic mover explicitly supports the selected record type."],
        }
    if kind == "dialogue_route":
        route = resolved
        fragment = index.router.fragments[route.path]
        return {
            "target_kind": kind,
            "route": dialogue_composer.route_payload(index.dialogues, route),
            "route_order": route_order_payload(index, route),
            "fragment": fragment_order_payload(index, fragment),
            "contracts": relevant_contracts(index, area="dialogs", path=route.path),
            "safe_moves": ["same_fragment_route_before_after"],
            "warnings": ["NPC route moves can change first-match behavior. Inspect projected shadows and compiled freshness after any apply."],
        }
    entry: IdEntry = resolved
    definitions = [
        entity
        for symbol in id_symbol_variants(entry.symbol)
        for entity in index.atlas.by_alias.get(symbol, ())
    ]
    definitions = sorted({entity.id: entity for entity in definitions}.values(), key=entity_sort_key)
    return {
        "target_kind": kind,
        "id_entry": id_entry_payload(entry),
        "definitions": [entity_order_payload(index, entity) for entity in definitions[:maximum]],
        "definition_count": len(definitions),
        "contracts": relevant_contracts(index, table=entry.table),
        "warnings": ["Numeric IDs are generated evidence. Do not hand-edit ID files; alter only reviewed source order, then inspect a normal build diff."],
    }


def dialogue_projected_hazards(index: OrderControlIndex, route: dialogue_composer.DialogueRoute, anchor: dialogue_composer.DialogueRoute, position: str) -> dict[str, Any]:
    routes = sorted((candidate for candidate in index.dialogues.routes if candidate.path == route.path), key=lambda candidate: (candidate.line, candidate.column, candidate.id))
    routes.remove(route)
    anchor_index = routes.index(anchor)
    routes.insert(anchor_index + (1 if position == "after" else 0), route)
    group = [candidate for candidate in routes if candidate.speaker == route.speaker and candidate.input_state == route.input_state]
    current = group.index(route)
    preceding = group[:current]
    prior_fallbacks = [candidate for candidate in preceding if not candidate.condition_operations]
    exact = [candidate for candidate in preceding if candidate.conditions_segment.strip() == route.conditions_segment.strip()]
    warnings: list[dict[str, Any]] = []
    player_choice = dialogue_composer.is_player_speaker(route.speaker)
    if not player_choice and prior_fallbacks:
        warnings.append({"severity": "high", "code": "PROJECTED_PRECEDING_NPC_FALLBACK", "route_ids": [candidate.id for candidate in prior_fallbacks], "message": "The move would leave a fallback NPC route before this candidate in the same input state."})
    if not player_choice and exact:
        warnings.append({"severity": "high", "code": "PROJECTED_EXACT_PRECEDING_CONDITION", "route_ids": [candidate.id for candidate in exact], "message": "The move would leave an earlier candidate with the same speaker, state, and condition block."})
    return {"group": {"speaker": route.speaker, "input_state": route.input_state, "projected_position": current + 1, "candidate_count": len(group)}, "warnings": warnings, "static_only": True}


def fragment_move_risk(index: OrderControlIndex, target: change_router.SourceFragment, anchor: change_router.SourceFragment, position: str) -> dict[str, Any]:
    old_position = target.order_position
    anchor_position = anchor.order_position
    new_position = (anchor_position or 0) + (1 if position == "after" else 0)
    categories: list[str] = ["fragment-order"]
    reasons: list[str] = []
    level = "warning"
    if target.area == "dialogs":
        categories.append("npc-first-match")
        level = "high"
        reasons.append("Dialogue fragment order controls the source/compiled candidate sequence; NPC routes select the first matching line.")
    if target.area in {"menus", "scripts", "mission_templates", "presentations", "quests", "constants"}:
        categories.append("generated-id-order")
        level = "high" if level != "critical" else level
        reasons.append("This area contributes ordered generated records and can shift positional IDs after a reviewed build.")
    protected = relevant_contracts(index, area=target.area, path=target.path)
    if any(item["kind"] in {"engine-callback-sequence", "id-prefix"} for item in protected):
        categories.append("protected-engine-or-legacy-prefix")
        level = "critical"
        reasons.append("The target is inside a checked-in protected engine callback or legacy numeric-ID prefix contract.")
    ids = []
    for entity in entities_in_fragment(index, target.path):
        ids.extend(entity_ids(index, entity))
    return {
        "level": level,
        "categories": sorted(dict.fromkeys(categories)),
        "source_positions": {"target": old_position, "anchor": anchor_position, "projected_target_position": new_position},
        "target_generated_ids": ids[:160],
        "target_generated_ids_truncated": len(ids) > 160,
        "reasons": reasons or ["No special static ordering contract was found; generated/export order still requires review after a normal build."],
        "required_follow_up": ["Run order_verify and order_diff against a checked-in baseline after a normal reviewed build.", "Inspect the generated ID-table and export diff before treating the move as compatibility-safe."],
    }


def manifest_move_plan(
    index: OrderControlIndex,
    target: change_router.SourceFragment,
    anchor: change_router.SourceFragment,
    position: str,
    expected_sha256: str | None,
) -> dict[str, Any]:
    target_binding = fragment_binding(index, target)
    anchor_binding = fragment_binding(index, anchor)
    if target_binding is None or anchor_binding is None:
        raise OrderControlError("Both fragment targets must be governed by an explicit _order manifest; implicit folder order is read-only evidence.")
    if target_binding.order_file != anchor_binding.order_file:
        raise OrderControlError("Fragment moves must stay within one declared order manifest.")
    path, raw, encoding, raw_bytes, entries = manifest_document(index, target_binding)
    target_entry = fragment_manifest_entry(target)
    anchor_entry = fragment_manifest_entry(anchor)
    target_lines = [line for line, entry in entries if entry == target_entry]
    anchor_lines = [line for line, entry in entries if entry == anchor_entry]
    if len(target_lines) != 1 or len(anchor_lines) != 1:
        raise OrderControlError("Target and anchor must each occur exactly once in their declared order manifest.")
    lines = raw.splitlines(keepends=True)
    target_index = target_lines[0] - 1
    anchor_index = anchor_lines[0] - 1
    moved_line = lines.pop(target_index)
    if target_index < anchor_index:
        anchor_index -= 1
    insert_index = anchor_index + (1 if position == "after" else 0)
    lines.insert(insert_index, moved_line)
    updated = "".join(lines)
    if updated == raw:
        raise OrderControlError("Target is already in the requested anchored position; no order change was planned.")
    base_sha = sha256_bytes(raw_bytes)
    if expected_sha256 is not None and require_sha256(expected_sha256) != base_sha:
        raise OrderControlError("expected_sha256 does not match the current order manifest; refresh the plan before applying.")
    diff = "".join(
        difflib.unified_diff(
            raw.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"current/{project_relative(path, index.root)}",
            tofile=f"planned/{project_relative(path, index.root)}",
            n=3,
        )
    )
    diff_lines = diff.splitlines()
    if len(diff_lines) > MAX_DIFF_LINES:
        diff = "\n".join(diff_lines[:MAX_DIFF_LINES]) + "\n... diff truncated by Order Control safety limit ...\n"
    plan_identity = json.dumps({"manifest": project_relative(path, index.root), "target": target.id, "anchor": anchor.id, "position": position, "sha": base_sha}, sort_keys=True)
    risk = fragment_move_risk(index, target, anchor, position)
    return {
        "plan_kind": "fragment_manifest_move",
        "target": fragment_order_payload(index, target),
        "anchor": fragment_order_payload(index, anchor),
        "position": position,
        "risk": risk,
        "order_manifest_plan": {
            "path": project_relative(path, index.root),
            "encoding": encoding,
            "base_sha256": base_sha,
            "result_sha256": hashlib.sha256(updated.encode(encoding)).hexdigest(),
            "target_entry": target_entry,
            "anchor_entry": anchor_entry,
            "unified_diff": diff,
            "plan_id": hashlib.sha256(plan_identity.encode("utf-8")).hexdigest()[:24],
        },
        "apply_contract": {
            "tool": "order_apply_move",
            "target": target.id,
            "anchor": anchor.id,
            "position": position,
            "required_expected_sha256": base_sha,
            "dry_run_default": True,
            "protected_contract_override_required": risk["level"] == "critical",
            "scope": "One declared src/**/_order*.txt manifest only; no fragment file, compile module, ID table, or export file is written.",
        },
        "warnings": ["Review the manifest diff, protected-prefix risk, and downstream generated-ID implications before a non-dry-run apply."],
    }


def dialogue_move_plan(index: OrderControlIndex, route: dialogue_composer.DialogueRoute, anchor: dialogue_composer.DialogueRoute, position: str, expected_sha256: str | None) -> dict[str, Any]:
    if route.target_id != anchor.target_id:
        raise OrderControlError("Dialogue route moves must stay inside one source fragment. Move the containing fragment through its explicit order manifest instead.")
    payload = dialogue_composer.dialogue_patch(
        index.dialogues,
        route.id,
        action="move_route",
        anchor_route_id=anchor.id,
        position=position,
        expected_sha256=expected_sha256,
    )
    projected = dialogue_projected_hazards(index, route, anchor, position)
    return {
        "plan_kind": "dialogue_route_move",
        "target": dialogue_composer.route_payload(index.dialogues, route),
        "anchor": dialogue_composer.route_payload(index.dialogues, anchor),
        "position": position,
        "risk": {
            "level": "high" if route.speaker != "plyr" else "warning",
            "categories": ["dialogue-route-order", "npc-first-match" if route.speaker != "plyr" else "player-choice-order"],
            "projected_first_match": projected,
            "reasons": ["NPC dialogue uses first-match selection; player route order changes choice display order."],
            "required_follow_up": ["Run dialogue_verify after apply and inspect compiled order after a normal dialogue build."],
        },
        "change_router_plan": payload["change_router_plan"],
        "apply_contract": {
            "tool": "order_apply_move",
            "target": route.id,
            "anchor": anchor.id,
            "position": position,
            "required_expected_sha256": payload["change_router_plan"]["target"]["base_sha256"],
            "dry_run_default": True,
            "scope": "One same-fragment dialogue route move through the Dialogue Composer and Change Router source SHA gate.",
        },
        "warnings": [*payload["warnings"], "Projected first-match findings are static; dynamic conditions still require an in-game smoke path."],
    }


def order_plan_move(
    index: OrderControlIndex,
    target: str,
    anchor: str,
    *,
    position: str,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    checked_position = require_position(position)
    target_kind, target_value = resolve_target(index, target)
    anchor_kind, anchor_value = resolve_target(index, anchor)
    if target_kind == "dialogue_route" and anchor_kind == "dialogue_route":
        if target_value.id == anchor_value.id:
            raise OrderControlError("target and anchor must be different.")
        return dialogue_move_plan(index, target_value, anchor_value, checked_position, expected_sha256)
    if target_kind == "source_fragment" and anchor_kind == "source_fragment":
        if target_value.id == anchor_value.id:
            raise OrderControlError("target and anchor must be different.")
        if target_value.area != anchor_value.area:
            raise OrderControlError("Fragment moves cannot cross source areas; each area has its own builder/order contract.")
        return manifest_move_plan(index, target_value, anchor_value, checked_position, expected_sha256)
    raise OrderControlError("Automatic order moves require either two dialogue route IDs or two source fragment IDs. Use order_explain for other entity types.")


def order_risk(index: OrderControlIndex, target: str, anchor: str, *, position: str) -> dict[str, Any]:
    plan = order_plan_move(index, target, anchor, position=position)
    return {
        "plan_kind": plan["plan_kind"],
        "target": plan["target"],
        "anchor": plan["anchor"],
        "position": plan["position"],
        "risk": plan["risk"],
        "next_action": "Use order_plan_move to obtain the reviewed unified diff and current SHA-guarded apply contract.",
        "warnings": plan["warnings"],
    }


def atomic_write(path: Path, text: str, encoding: str) -> None:
    """Write one approved order manifest atomically without touching module outputs."""

    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding=encoding, newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except OSError as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise OrderControlError(f"Could not write approved order manifest {path}: {error}") from error


def invalidate_after_order_write(root: Path) -> None:
    invalidate_order_control(root)
    change_router.invalidate_router(root)
    module_atlas.invalidate_atlas(root)
    dialogue_composer.invalidate_composer(root)


def order_apply_move(
    index: OrderControlIndex,
    target: str,
    anchor: str,
    *,
    position: str,
    expected_sha256: str,
    dry_run: bool = True,
    allow_protected_contract_change: bool = False,
) -> dict[str, Any]:
    if not isinstance(dry_run, bool):
        raise OrderControlError("dry_run must be true or false.")
    if not isinstance(allow_protected_contract_change, bool):
        raise OrderControlError("allow_protected_contract_change must be true or false.")
    checked_sha = require_sha256(expected_sha256)
    plan = order_plan_move(index, target, anchor, position=position, expected_sha256=checked_sha)
    protected_override_required = plan["risk"]["level"] == "critical"
    if not dry_run and protected_override_required and not allow_protected_contract_change:
        raise OrderControlError(
            "This move touches a protected engine/legacy order contract. A non-dry apply requires "
            "allow_protected_contract_change=true after reviewing the contract, generated-ID implications, and normal build diff."
        )
    if plan["plan_kind"] == "dialogue_route_move":
        payload = dialogue_composer.dialogue_apply(
            index.dialogues,
            str(plan["target"]["route_id"]),
            action="move_route",
            anchor_route_id=str(plan["anchor"]["route_id"]),
            position=position,
            expected_sha256=checked_sha,
            dry_run=dry_run,
        )
        return {
            "plan_kind": plan["plan_kind"],
            "applied": bool(payload["result"]["applied"]),
            "dry_run": dry_run,
            "protected_contract_override_used": protected_override_required and allow_protected_contract_change,
            "result": payload,
            "verification_required": "Run order_verify and dialogue_verify after a normal reviewed dialogue build; compiled first-match order is a separate evidence layer.",
            "warnings": [*plan["warnings"], *payload["warnings"]],
        }
    manifest = plan["order_manifest_plan"]
    manifest_path = (index.root / str(manifest["path"])).resolve()
    try:
        current_raw, encoding, current_bytes = change_router.read_text_with_encoding(manifest_path)
    except change_router.ChangeRouterError as error:
        raise OrderControlError(str(error)) from error
    current_sha = sha256_bytes(current_bytes)
    if current_sha != checked_sha:
        raise OrderControlError("Order manifest changed after planning; refusing to apply a stale move.")
    target_kind, target_fragment = resolve_target(index, target)
    anchor_kind, anchor_fragment = resolve_target(index, anchor)
    assert target_kind == anchor_kind == "source_fragment"
    binding = fragment_binding(index, target_fragment)
    assert binding is not None
    _, raw, _, _, entries = manifest_document(index, binding)
    lines = raw.splitlines(keepends=True)
    target_entry = fragment_manifest_entry(target_fragment)
    anchor_entry = fragment_manifest_entry(anchor_fragment)
    target_line = next(line for line, entry in entries if entry == target_entry)
    anchor_line = next(line for line, entry in entries if entry == anchor_entry)
    target_index = target_line - 1
    anchor_index = anchor_line - 1
    moved_line = lines.pop(target_index)
    if target_index < anchor_index:
        anchor_index -= 1
    lines.insert(anchor_index + (1 if position == "after" else 0), moved_line)
    updated = "".join(lines)
    if dry_run:
        return {
            "plan_kind": plan["plan_kind"],
            "applied": False,
            "dry_run": True,
            "protected_contract_override_required": protected_override_required,
            "target": {"path": manifest["path"], "base_sha256": current_sha, "result_sha256": hashlib.sha256(updated.encode(encoding)).hexdigest()},
            "plan_id": manifest["plan_id"],
            "warnings": [*plan["warnings"], "Dry run only: no source manifest, fragment, compile module, ID table, or export file was written."],
        }
    atomic_write(manifest_path, updated, encoding)
    invalidate_after_order_write(index.root)
    return {
        "plan_kind": plan["plan_kind"],
        "applied": True,
        "dry_run": False,
        "protected_contract_override_used": protected_override_required and allow_protected_contract_change,
        "target": {"path": manifest["path"], "base_sha256": current_sha, "result_sha256": hashlib.sha256(updated.encode(encoding)).hexdigest()},
        "plan_id": manifest["plan_id"],
        "verification_required": "Only one source order manifest changed. Run order_verify, then perform the normal reviewed build and inspect generated ID/export diffs before gameplay validation.",
        "warnings": [*plan["warnings"], "Only an explicit src/**/_order*.txt manifest was changed. No fragment file, compile module, ID table, or export file was written."],
    }


def baseline_dir(root: Path) -> Path:
    return root / BASELINE_RELATIVE


def baseline_path(root: Path, label: str) -> Path:
    checked = require_string(label, name="baseline", maximum=100)
    if Path(checked).name != checked:
        raise OrderControlError("baseline must be a simple label or filename, not a path.")
    name = checked if checked.casefold().endswith(".json") else f"{slugify(checked)}.json"
    destination = (baseline_dir(root) / name).resolve()
    try:
        destination.relative_to(baseline_dir(root).resolve())
    except ValueError as error:
        raise OrderControlError("Baseline path escaped devkit/order_control/baselines/.") from error
    return destination


def order_baseline(index: OrderControlIndex, *, label: str = "baseline", overwrite: bool = False) -> dict[str, Any]:
    if not isinstance(overwrite, bool):
        raise OrderControlError("overwrite must be true or false.")
    destination = baseline_path(index.root, label)
    if destination.exists() and not overwrite:
        raise OrderControlError(f"Order baseline already exists: {project_relative(destination, index.root)}. Set overwrite=true to replace it deliberately.")
    payload = {
        "schema": "sod-modern.order-control-baseline.v1",
        "created_at_utc": utc_now(),
        "order_control_version": ORDER_CONTROL_VERSION,
        "source_fragment_order": source_snapshot(index),
        "id_tables": id_snapshot(index),
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as error:
        raise OrderControlError(f"Could not write order baseline: {error}") from error
    return {
        "artifact": {"path": project_relative(destination, index.root), "kind": "order-baseline"},
        "baseline": {"source_area_count": len(payload["source_fragment_order"]), "id_table_count": len(payload["id_tables"]), "created_at_utc": payload["created_at_utc"]},
        "warnings": ["Baseline creation writes only an ignored DevKit artifact. It does not alter module source, manifests, generated modules, ID tables, or exports."],
    }


def load_baseline(root: Path, label: str) -> tuple[Path, dict[str, Any]]:
    path = baseline_path(root, label)
    payload = read_json(path, label="Order Control baseline")
    if payload.get("schema") != "sod-modern.order-control-baseline.v1":
        raise OrderControlError("Order baseline has an unsupported schema.")
    if not isinstance(payload.get("source_fragment_order"), dict) or not isinstance(payload.get("id_tables"), dict):
        raise OrderControlError("Order baseline is missing source_fragment_order or id_tables.")
    return path, payload


def sequence_delta(before: Sequence[str], after: Sequence[str], *, category: str, maximum: int) -> dict[str, Any]:
    before_position = {value: index for index, value in enumerate(before)}
    after_position = {value: index for index, value in enumerate(after)}
    added = [value for value in after if value not in before_position]
    removed = [value for value in before if value not in after_position]
    moved = [
        {"value": value, "before": before_position[value] + 1, "after": after_position[value] + 1}
        for value in after
        if value in before_position and before_position[value] != after_position[value]
    ]
    return {
        "category": category,
        "added_count": len(added),
        "removed_count": len(removed),
        "moved_count": len(moved),
        "added": added[:maximum],
        "removed": removed[:maximum],
        "moved": moved[:maximum],
        "truncated": len(added) > maximum or len(removed) > maximum or len(moved) > maximum,
    }


def id_table_delta(before: Sequence[Mapping[str, Any]], after: Sequence[Mapping[str, Any]], table: str, maximum: int) -> dict[str, Any]:
    old = {str(item.get("symbol")): item.get("value") for item in before if isinstance(item, Mapping) and isinstance(item.get("symbol"), str) and isinstance(item.get("value"), int)}
    new = {str(item.get("symbol")): item.get("value") for item in after if isinstance(item, Mapping) and isinstance(item.get("symbol"), str) and isinstance(item.get("value"), int)}
    added = [{"symbol": symbol, "id": new[symbol]} for symbol in new if symbol not in old]
    removed = [{"symbol": symbol, "id": old[symbol]} for symbol in old if symbol not in new]
    shifted = [{"symbol": symbol, "before": old[symbol], "after": new[symbol]} for symbol in new if symbol in old and old[symbol] != new[symbol]]
    protected = [item for item in shifted if item["symbol"].startswith("script_game_")]
    return {
        "table": table,
        "added_count": len(added),
        "removed_count": len(removed),
        "shifted_count": len(shifted),
        "engine_callback_shift_count": len(protected),
        "added": added[:maximum],
        "removed": removed[:maximum],
        "shifted": shifted[:maximum],
        "engine_callback_shifts": protected[:maximum],
        "truncated": len(added) > maximum or len(removed) > maximum or len(shifted) > maximum,
    }


def order_diff(index: OrderControlIndex, *, baseline: str, limit: int = 100) -> dict[str, Any]:
    maximum = require_limit(limit)
    path, prior = load_baseline(index.root, baseline)
    source_before = prior["source_fragment_order"]
    source_after = source_snapshot(index)
    source_rows = []
    for area in sorted(set(source_before) | set(source_after)):
        old = source_before.get(area, [])
        new = source_after.get(area, [])
        if not isinstance(old, list) or not isinstance(new, list):
            raise OrderControlError(f"Baseline source order for {area!r} is invalid.")
        delta = sequence_delta([str(value) for value in old], [str(value) for value in new], category="source-fragment-order", maximum=maximum)
        delta["area"] = area
        source_rows.append(delta)
    ids_before = prior["id_tables"]
    ids_after = id_snapshot(index)
    id_rows = []
    for table in sorted(set(ids_before) | set(ids_after)):
        old = ids_before.get(table, [])
        new = ids_after.get(table, [])
        if not isinstance(old, list) or not isinstance(new, list):
            raise OrderControlError(f"Baseline ID table {table!r} is invalid.")
        id_rows.append(id_table_delta(old, new, table, maximum))
    source_changes = sum(item["added_count"] + item["removed_count"] + item["moved_count"] for item in source_rows)
    id_changes = sum(item["added_count"] + item["removed_count"] + item["shifted_count"] for item in id_rows)
    callback_shifts = sum(item["engine_callback_shift_count"] for item in id_rows)
    severity = "critical" if callback_shifts else "high" if id_changes else "warning" if source_changes else "clean"
    return {
        "baseline": {"path": project_relative(path, index.root), "created_at_utc": prior.get("created_at_utc")},
        "summary": {"source_change_count": source_changes, "id_change_count": id_changes, "engine_callback_shift_count": callback_shifts, "risk_level": severity},
        "source_fragment_deltas": source_rows,
        "id_table_deltas": id_rows,
        "warnings": [
            "Order diff compares checked source-manifest and generated-ID snapshots. It cannot establish live save compatibility or dynamic engine execution.",
            "Any generated-ID shift deserves explicit build/export review; engine callback ID shifts are elevated to critical evidence.",
        ],
    }


def generated_order_parity(index: OrderControlIndex, *, limit: int = 100) -> dict[str, Any]:
    maximum = require_limit(limit)
    rows = []
    for area in sorted(VALID_AREAS):
        expected = list(index.router.ordering.get(area, ()))
        compile_paths = set(change_router.GENERATED_BY_AREA.get(area, ()))
        earliest: dict[str, int] = {}
        for source, segments in index.router.generated_by_source.items():
            fragment = index.router.fragments.get(source)
            if fragment is None or fragment.area != area:
                continue
            values = [segment.compile_line_start for segment in segments if segment.compile_path in compile_paths]
            if values:
                earliest[source] = min(values)
        actual = [source for source, _ in sorted(earliest.items(), key=lambda item: (item[1], item[0].casefold()))]
        common_expected = [source for source in expected if source in earliest]
        common_actual = [source for source in actual if source in set(common_expected)]
        moved = [
            {"source": source, "expected_position": common_expected.index(source) + 1, "generated_position": common_actual.index(source) + 1}
            for source in common_actual
            if common_expected.index(source) != common_actual.index(source)
        ]
        missing_marker = [source for source in expected if source not in earliest]
        rows.append({"area": area, "expected_fragment_count": len(expected), "generated_marker_fragment_count": len(actual), "missing_generated_marker_count": len(missing_marker), "moved_common_fragment_count": len(moved), "missing_generated_marker_sample": missing_marker[:maximum], "moved_common_fragment_sample": moved[:maximum], "truncated": len(missing_marker) > maximum or len(moved) > maximum})
    moved_common_fragment_count = sum(item["moved_common_fragment_count"] for item in rows)
    unmapped_fragment_count = sum(item["missing_generated_marker_count"] for item in rows)
    return {
        "area_count": len(rows),
        "mismatch_count": moved_common_fragment_count,
        "moved_common_fragment_count": moved_common_fragment_count,
        "generated_marker_observability_gap_count": unmapped_fragment_count,
        "areas": rows,
        "warnings": [
            "Generated-marker parity is source provenance, not a proof that generated output is current. Read freshness evidence before treating parity as a build result.",
            "Fragments without generated provenance markers are observability gaps, not proof of source/generated order drift; inspect their generation path before promoting them to a contract.",
        ],
    }


def dialogue_order_hazards(index: OrderControlIndex, *, limit: int = 100) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dialogue_composer.DialogueRoute]] = defaultdict(list)
    for route in index.dialogues.routes:
        groups[(route.speaker, route.input_state)].append(route)
    hazards = []
    for (speaker, state), routes in sorted(groups.items()):
        ordered = sorted(routes, key=lambda route: (route.source_order if route.source_order is not None else 1_000_000, route.line, route.column, route.id))
        previous_fallbacks: list[dialogue_composer.DialogueRoute] = []
        previous_conditions: dict[str, list[dialogue_composer.DialogueRoute]] = defaultdict(list)
        for route in ordered:
            player_choice = dialogue_composer.is_player_speaker(speaker)
            if not player_choice and previous_fallbacks:
                hazards.append({"severity": "high", "code": "PRECEDING_NPC_FALLBACK", "route_id": route.id, "speaker": speaker, "input_state": state, "preceding_route_ids": [candidate.id for candidate in previous_fallbacks[-10:]], "message": "A preceding no-condition NPC route can consume this state before the later candidate."})
            exact = previous_conditions.get(route.conditions_segment.strip(), [])
            if not player_choice and exact:
                hazards.append({"severity": "high", "code": "EXACT_PRECEDING_CONDITION", "route_id": route.id, "speaker": speaker, "input_state": state, "preceding_route_ids": [candidate.id for candidate in exact[-10:]], "message": "A preceding route has the same speaker, input state, and condition block."})
            if not route.condition_operations:
                previous_fallbacks.append(route)
            previous_conditions[route.conditions_segment.strip()].append(route)
    return {"group_count": len(groups), "hazard_count": len(hazards), "returned_hazard_count": min(len(hazards), limit), "hazards_truncated": len(hazards) > limit, "hazards": hazards[:limit], "warnings": ["These are static ordering hazards. They are review candidates, not runtime reachability claims."]}


def order_verify(index: OrderControlIndex, *, baseline: str | None = None, limit: int = 100) -> dict[str, Any]:
    maximum = require_limit(limit)
    contracts = order_contracts(index)
    parity = generated_order_parity(index, limit=maximum)
    hazards = dialogue_order_hazards(index, limit=maximum)
    diff = order_diff(index, baseline=baseline, limit=maximum) if baseline is not None else {"available": False, "reason": "No baseline supplied. Create a confined DevKit baseline with order_baseline before asking for an order-only delta."}
    blockers = [
        {"id": f"contract:{contract['id']}", "message": contract.get("title", contract["id"])}
        for contract in contracts["contracts"]
        if contract["active_blocker"]
    ]
    state = "structural_order_blocked" if blockers else "structural_order_ready_for_review"
    return {
        "state": state,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "contracts": contracts,
        "generated_order_parity": parity,
        "dialogue_order_hazards": hazards,
        "baseline_diff": diff,
        "manual_gates": [
            "Review the exact manifest or dialogue route diff and its SHA before a non-dry-run move.",
            "Run the normal reviewed builder; inspect generated module, ID-table, and export diffs rather than overwriting them blindly.",
            "For dialogue, inspect compiled order and test the intended NPC/player path in-game.",
            "For any generated-ID shift, make a deliberate save-compatibility decision before release.",
        ],
        "evidence_boundary": "Order verification proves declared source manifests, static route order, source-marker parity, generated-ID snapshot deltas, and protected contracts. It never executes engine callbacks, evaluates dynamic conditions, or certifies save compatibility/gameplay.",
        "warnings": [*contracts["warnings"], *parity["warnings"], *hazards["warnings"]],
    }


def safe_report_path(root: Path, name: str) -> Path:
    checked = require_string(name, name="output", maximum=120)
    if Path(checked).name != checked:
        raise OrderControlError("output must be a simple filename under devkit/order_control/reports/.")
    if not checked.casefold().endswith(".json"):
        checked += ".json"
    path = (root / REPORT_RELATIVE / checked).resolve()
    try:
        path.relative_to((root / REPORT_RELATIVE).resolve())
    except ValueError as error:
        raise OrderControlError("output escaped devkit/order_control/reports/.") from error
    return path


def write_payload(root: Path, payload: Mapping[str, Any], output: str | None) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output is None:
        sys.stdout.write(rendered)
        return
    path = safe_report_path(root, output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM-first SoD Modern Order Control Plane: inspect, protect, diff, and safely plan anchored order changes.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    for name in ("summary", "contracts"):
        command = subparsers.add_parser(name)
        command.add_argument("--output")
    mapping = subparsers.add_parser("map")
    mapping.add_argument("--area", default="all")
    mapping.add_argument("--domain", default="all")
    mapping.add_argument("--query")
    mapping.add_argument("--limit", type=int, default=60)
    mapping.add_argument("--output")
    explain = subparsers.add_parser("explain")
    explain.add_argument("target")
    explain.add_argument("--related-limit", type=int, default=40)
    explain.add_argument("--output")
    for name in ("risk", "plan-move"):
        move = subparsers.add_parser(name)
        move.add_argument("target")
        move.add_argument("anchor")
        move.add_argument("--position", choices=tuple(sorted(VALID_MOVE_POSITIONS)), required=True)
        move.add_argument("--expected-sha256")
        move.add_argument("--output")
    apply = subparsers.add_parser("apply-move")
    apply.add_argument("target")
    apply.add_argument("anchor")
    apply.add_argument("--position", choices=tuple(sorted(VALID_MOVE_POSITIONS)), required=True)
    apply.add_argument("--expected-sha256", required=True)
    apply.add_argument("--apply", action="store_true", help="Actually write the reviewed manifest/dialogue source move. Default is dry-run.")
    apply.add_argument(
        "--allow-protected-contract-change",
        action="store_true",
        help="Permit a non-dry move touching a protected engine/legacy order contract after deliberate review.",
    )
    apply.add_argument("--output")
    baseline = subparsers.add_parser("baseline")
    baseline.add_argument("--label", default="baseline")
    baseline.add_argument("--overwrite", action="store_true")
    baseline.add_argument("--output")
    diff = subparsers.add_parser("diff")
    diff.add_argument("--baseline", required=True)
    diff.add_argument("--limit", type=int, default=100)
    diff.add_argument("--output")
    verify = subparsers.add_parser("verify")
    verify.add_argument("--baseline")
    verify.add_argument("--limit", type=int, default=100)
    verify.add_argument("--output")
    args = parser.parse_args(argv)
    command = args.command or "summary"
    root = args.root.resolve()
    try:
        index = build_order_control(root)
        if command == "summary":
            payload = order_summary(index)
        elif command == "contracts":
            payload = order_contracts(index)
        elif command == "map":
            payload = order_map(index, area=args.area, domain=args.domain, query=args.query, limit=args.limit)
        elif command == "explain":
            payload = order_explain(index, args.target, related_limit=args.related_limit)
        elif command == "risk":
            payload = order_risk(index, args.target, args.anchor, position=args.position)
        elif command == "plan-move":
            payload = order_plan_move(index, args.target, args.anchor, position=args.position, expected_sha256=args.expected_sha256)
        elif command == "apply-move":
            payload = order_apply_move(
                index,
                args.target,
                args.anchor,
                position=args.position,
                expected_sha256=args.expected_sha256,
                dry_run=not args.apply,
                allow_protected_contract_change=args.allow_protected_contract_change,
            )
        elif command == "baseline":
            payload = order_baseline(index, label=args.label, overwrite=args.overwrite)
        elif command == "diff":
            payload = order_diff(index, baseline=args.baseline, limit=args.limit)
        else:
            payload = order_verify(index, baseline=args.baseline, limit=args.limit)
        write_payload(root, payload, getattr(args, "output", None))
        return 0
    except (OrderControlError, change_router.ChangeRouterError, module_atlas.ModuleAtlasError, dialogue_composer.DialogueComposerError, workspace_audit.AuditError) as error:
        parser.error(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
