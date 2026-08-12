#!/usr/bin/env python3
"""LLM-first Content Forge for the SoD Modern M&B 1.011 module system.

Content Forge is a typed *authoring pack* compiler.  It deliberately does not
invent a second source writer: dialogue routes remain owned by Dialogue
Composer, presentation layout remains owned by Presentation Layout, module
entities remain owned by Module Atlas/Feature Authoring, and legacy troop/item
records remain owned by Balance Lab.  A pack adds the missing content-level
view: brief, lore constraints, tone, acceptance criteria, linked slices,
intent contracts, deterministic review, and one guarded apply boundary.

There is no prose-to-Python or raw tuple field.  Typed operations are compiled
by Feature Authoring and every real write remains source-only, SHA-guarded,
and dry-run by default.  Packs also never write generated modules, IDs, or
exports.  The human-facing review canvas is data returned by this compiler;
the MCP/JSON contract remains the primary interface.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.campaign_scenario_fuzzer import campaign_scenario_fuzzer  # noqa: E402
from devkit.campaign_state_doctor import campaign_state_doctor  # noqa: E402
from devkit.change_router import change_router  # noqa: E402
from devkit.feature_authoring import feature_authoring  # noqa: E402
from devkit.presentation_layout import presentation_layout  # noqa: E402
from devkit.troop_item_balance import troop_item_balance  # noqa: E402


CONTENT_FORGE_VERSION = "0.2.0"
CONTENT_PACK_SCHEMA = "sod-modern.content-pack.v1"
CONTENT_PACK_CATALOG_SCHEMA = "sod-modern.content-pack-catalog.v1"
CONTENT_SNAPSHOT_SCHEMA = "sod-modern.content-forge-snapshot.v1"
CONTENT_PACKS_RELATIVE = Path("devkit/content_forge/packs.json")
CONTENT_CATALOG_SAVE_CONFIRMATION = "SAVE CONTENT PACK"
MAX_PACKS = 200
MAX_SLICE_ROWS = 64
MAX_SOURCE_CHANGES = 64
MAX_MARKERS = 32
MAX_SCENARIOS = 24
MAX_RESULT_LIMIT = 200
MAX_TEXT_LENGTH = 30_000
MAX_DESCRIPTION_LENGTH = 2_000
PACK_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,119}$")
TOKEN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SAFE_TEST_RE = re.compile(r"^build/test_[A-Za-z0-9_]+\.py$")
ENTRYPOINT_RE = re.compile(r"^entrypoint:[A-Za-z0-9_:/.-]+$")
SCENARIO_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,119}$")
VALID_STATUSES = frozenset({"active", "draft", "disabled"})
VALID_CATALOG_MODES = frozenset({"create", "replace"})
SLICE_ORDER = ("quest_event", "campaign_ai", "dialogue", "presentation", "troop_item")
VALID_SLICES = frozenset(SLICE_ORDER)
VALID_AI_INTENTS = frozenset({"stationary_camp", "patrol_radius", "escort_attachment", "raid_return", "despawn"})
AI_INTENT_MAP = {
    "stationary_camp": "stationary",
    "patrol_radius": "patrol",
    "escort_attachment": "escort",
    "raid_return": "raid_return",
    "despawn": "despawn",
}


class ContentForgeError(RuntimeError):
    """A content pack or its guarded application is unsafe or incomplete."""


@dataclass(frozen=True)
class ContentPack:
    id: str
    title: str
    status: str
    description: str
    brief: Mapping[str, Any]
    blueprint_id: str | None
    slices: Mapping[str, Mapping[str, Any]]
    verification: Mapping[str, Any]
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class SourceChange:
    content_change_id: str
    slice_id: str
    feature_change_id: str
    target: str
    action: str
    kind: str
    source: Mapping[str, Any]


@dataclass(frozen=True)
class BalanceChange:
    content_change_id: str
    slice_id: str
    record_id: str
    entity_kind: str
    entity_id: str
    changes: Mapping[str, Any]
    rationale: str


@dataclass(frozen=True)
class ContentCompilation:
    pack: ContentPack
    feature_intent: Mapping[str, Any] | None
    source_changes: tuple[SourceChange, ...]
    balance_changes: tuple[BalanceChange, ...]
    entrypoints: tuple[str, ...]


@dataclass
class ContentForgeIndex:
    root: Path
    features: feature_authoring.FeatureAuthoringIndex
    packs: tuple[ContentPack, ...]
    packs_by_id: dict[str, ContentPack]
    warnings: list[str]


_CACHE: dict[Path, tuple[tuple[Any, ...], ContentForgeIndex]] = {}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any, *, length: int = 20) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:length]


def require_object(value: Any, *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContentForgeError(f"{name} must be a JSON object.")
    return dict(value)


def reject_unknown_fields(value: Mapping[str, Any], *, name: str, allowed: Iterable[str]) -> None:
    extra = sorted(set(value) - set(allowed))
    if extra:
        raise ContentForgeError(f"{name} has unsupported field(s): " + ", ".join(extra))


def require_string(value: Any, *, name: str, maximum: int = MAX_TEXT_LENGTH, allow_blank: bool = False) -> str:
    if not isinstance(value, str):
        raise ContentForgeError(f"{name} must be a string.")
    if len(value) > maximum:
        raise ContentForgeError(f"{name} exceeds the {maximum}-character safety limit.")
    if not allow_blank and not value.strip():
        raise ContentForgeError(f"{name} must not be blank.")
    return value


def require_identifier(value: Any, *, name: str, pattern: re.Pattern[str] = PACK_ID_RE) -> str:
    result = require_string(value, name=name, maximum=180)
    if pattern.fullmatch(result) is None:
        raise ContentForgeError(f"{name} has an invalid identifier shape.")
    return result


def require_boolean(value: Any, *, name: str) -> bool:
    if not isinstance(value, bool):
        raise ContentForgeError(f"{name} must be a boolean.")
    return value


def require_limit(value: Any, *, name: str, maximum: int = MAX_RESULT_LIMIT, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise ContentForgeError(f"{name} must be an integer from {minimum} through {maximum}.")
    return value


def require_string_list(
    value: Any,
    *,
    name: str,
    maximum: int,
    item_pattern: re.Pattern[str] | None = None,
    allow_empty: bool = True,
) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value) or len(value) > maximum:
        range_text = f"at most {maximum}" if allow_empty else f"from 1 through {maximum}"
        raise ContentForgeError(f"{name} must be an array containing {range_text} strings.")
    result = [require_string(item, name=f"{name}[{position}]", maximum=MAX_TEXT_LENGTH) for position, item in enumerate(value)]
    if len(set(result)) != len(result):
        raise ContentForgeError(f"{name} may not repeat a value.")
    if item_pattern is not None:
        invalid = [item for item in result if item_pattern.fullmatch(item) is None]
        if invalid:
            raise ContentForgeError(f"{name} contains an invalid value: {invalid[0]!r}.")
    return result


def deep_copy_json(value: Any) -> Any:
    """Return JSON-shaped data without retaining caller-owned mutable objects."""

    try:
        return json.loads(json.dumps(value, ensure_ascii=False))
    except (TypeError, ValueError) as error:
        raise ContentForgeError(f"Content pack must contain JSON data only: {error}") from error


def normalize_brief(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"summary", "lore_constraints", "tone", "acceptance_criteria"})
    required = ("summary", "lore_constraints", "tone", "acceptance_criteria")
    missing = [field for field in required if field not in item]
    if missing:
        raise ContentForgeError(f"{name} is missing required field(s): " + ", ".join(missing))
    return {
        "summary": require_string(item["summary"], name=f"{name}.summary", maximum=MAX_DESCRIPTION_LENGTH),
        "lore_constraints": require_string_list(item["lore_constraints"], name=f"{name}.lore_constraints", maximum=MAX_SLICE_ROWS),
        "tone": require_string_list(item["tone"], name=f"{name}.tone", maximum=MAX_SLICE_ROWS),
        "acceptance_criteria": require_string_list(
            item["acceptance_criteria"],
            name=f"{name}.acceptance_criteria",
            maximum=MAX_SLICE_ROWS,
            allow_empty=False,
        ),
    }


def normalize_source_changes(value: Any, *, name: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) > MAX_SOURCE_CHANGES:
        raise ContentForgeError(f"{name} must be an array with at most {MAX_SOURCE_CHANGES} typed source changes.")
    rows: list[dict[str, Any]] = []
    for position, raw in enumerate(value):
        item = require_object(raw, name=f"{name}[{position}]")
        if "kind" in item:
            raise ContentForgeError(f"{name}[{position}].kind is inferred from its Content Forge slice and must not be supplied.")
        if "target" not in item or "action" not in item:
            raise ContentForgeError(f"{name}[{position}] must name target and action.")
        require_identifier(item["target"], name=f"{name}[{position}].target", pattern=ENTRYPOINT_RE)
        require_string(item["action"], name=f"{name}[{position}].action", maximum=80)
        rows.append(deep_copy_json(item))
    return rows


def normalize_beat_rows(value: Any, *, name: str, purpose_name: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) > MAX_SLICE_ROWS:
        raise ContentForgeError(f"{name} must be an array with at most {MAX_SLICE_ROWS} rows.")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for position, raw in enumerate(value):
        item = require_object(raw, name=f"{name}[{position}]")
        reject_unknown_fields(item, name=f"{name}[{position}]", allowed={"id", "title", purpose_name, "entrypoint", "description", "phase"})
        identifier = require_identifier(item.get("id"), name=f"{name}[{position}].id")
        if identifier in seen:
            raise ContentForgeError(f"{name} repeats id {identifier!r}.")
        seen.add(identifier)
        row = {
            "id": identifier,
            "title": require_string(item.get("title"), name=f"{name}[{position}].title", maximum=200),
            purpose_name: require_string(item.get(purpose_name), name=f"{name}[{position}].{purpose_name}", maximum=MAX_DESCRIPTION_LENGTH),
        }
        if "entrypoint" in item:
            row["entrypoint"] = require_identifier(item["entrypoint"], name=f"{name}[{position}].entrypoint", pattern=ENTRYPOINT_RE)
        if "description" in item:
            row["description"] = require_string(item["description"], name=f"{name}[{position}].description", maximum=MAX_DESCRIPTION_LENGTH)
        if "phase" in item:
            row["phase"] = require_identifier(item["phase"], name=f"{name}[{position}].phase", pattern=TOKEN_RE)
        rows.append(row)
    return rows


def normalize_dialogue_slice(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"changes", "beats"})
    return {
        "changes": normalize_source_changes(item.get("changes", []), name=f"{name}.changes"),
        "beats": normalize_beat_rows(item.get("beats", []), name=f"{name}.beats", purpose_name="purpose"),
    }


def normalize_quest_event_slice(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"changes", "timeline"})
    timeline = normalize_beat_rows(item.get("timeline", []), name=f"{name}.timeline", purpose_name="description")
    return {"changes": normalize_source_changes(item.get("changes", []), name=f"{name}.changes"), "timeline": timeline}


def normalize_ai_contract(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    allowed = {
        "id", "intent", "entrypoint", "required_markers", "description", "state_contract_id",
        "party_template", "party_selector", "additional_scope_scripts", "expected_behavior",
        "forbidden_behaviors", "allowed_when", "minimum_radius", "maximum_radius",
        "attach_to", "require_detach", "return_behavior", "return_target", "return_when", "despawn_when",
    }
    reject_unknown_fields(item, name=name, allowed=allowed)
    required = ("id", "intent", "entrypoint", "required_markers", "description")
    missing = [field for field in required if field not in item]
    if missing:
        raise ContentForgeError(f"{name} is missing required field(s): " + ", ".join(missing))
    identifier = require_identifier(item["id"], name=f"{name}.id")
    intent = require_identifier(item["intent"], name=f"{name}.intent", pattern=TOKEN_RE)
    if intent not in VALID_AI_INTENTS:
        raise ContentForgeError(f"{name}.intent must be one of: " + ", ".join(sorted(VALID_AI_INTENTS)))
    result: dict[str, Any] = {
        "id": identifier,
        "intent": intent,
        "entrypoint": require_identifier(item["entrypoint"], name=f"{name}.entrypoint", pattern=ENTRYPOINT_RE),
        "required_markers": require_string_list(item["required_markers"], name=f"{name}.required_markers", maximum=MAX_MARKERS, allow_empty=False),
        "description": require_string(item["description"], name=f"{name}.description", maximum=MAX_DESCRIPTION_LENGTH),
    }
    if "state_contract_id" in item:
        result["state_contract_id"] = require_identifier(item["state_contract_id"], name=f"{name}.state_contract_id", pattern=TOKEN_RE)
    if "party_template" in item:
        template = require_string(item["party_template"], name=f"{name}.party_template", maximum=180)
        if not template.startswith("pt_"):
            raise ContentForgeError(f"{name}.party_template must be an M&B party-template symbol beginning pt_.")
        result["party_template"] = template
    elif "state_contract_id" not in result:
        raise ContentForgeError(f"{name}.party_template is required unless state_contract_id selects a checked-in AI contract.")
    if "party_selector" in item:
        result["party_selector"] = require_string(item["party_selector"], name=f"{name}.party_selector", maximum=180)
    if "additional_scope_scripts" in item:
        scripts = require_string_list(item["additional_scope_scripts"], name=f"{name}.additional_scope_scripts", maximum=16)
        if any(not script.startswith("script_") for script in scripts):
            raise ContentForgeError(f"{name}.additional_scope_scripts must contain script_* symbols.")
        result["additional_scope_scripts"] = scripts
    for text_field in ("expected_behavior", "allowed_when", "attach_to", "return_behavior", "return_target", "return_when", "despawn_when"):
        if text_field in item:
            result[text_field] = require_string(item[text_field], name=f"{name}.{text_field}", maximum=180)
    if "forbidden_behaviors" in item:
        result["forbidden_behaviors"] = require_string_list(item["forbidden_behaviors"], name=f"{name}.forbidden_behaviors", maximum=16)
    if "require_detach" in item:
        result["require_detach"] = require_boolean(item["require_detach"], name=f"{name}.require_detach")
    for field in ("minimum_radius", "maximum_radius"):
        if field in item:
            number = item[field]
            if isinstance(number, bool) or not isinstance(number, int) or not 0 <= number <= 1_000_000:
                raise ContentForgeError(f"{name}.{field} must be an integer from 0 through 1,000,000.")
            result[field] = number
    if "minimum_radius" in result and "maximum_radius" in result and result["minimum_radius"] > result["maximum_radius"]:
        raise ContentForgeError(f"{name}.minimum_radius may not exceed maximum_radius.")
    return result


def normalize_campaign_ai_slice(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"changes", "contracts", "scenarios"})
    contracts_raw = item.get("contracts", [])
    if not isinstance(contracts_raw, list) or len(contracts_raw) > MAX_SLICE_ROWS:
        raise ContentForgeError(f"{name}.contracts must be an array with at most {MAX_SLICE_ROWS} contracts.")
    contracts = [normalize_ai_contract(contract, name=f"{name}.contracts[{position}]") for position, contract in enumerate(contracts_raw)]
    ids = [contract["id"] for contract in contracts]
    if len(set(ids)) != len(ids):
        raise ContentForgeError(f"{name}.contracts may not repeat an id.")
    return {
        "changes": normalize_source_changes(item.get("changes", []), name=f"{name}.changes"),
        "contracts": contracts,
        "scenarios": require_string_list(item.get("scenarios", []), name=f"{name}.scenarios", maximum=MAX_SCENARIOS, item_pattern=SCENARIO_ID_RE),
    }


def normalize_troop_item_slice(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"records"})
    records_raw = item.get("records", [])
    if not isinstance(records_raw, list) or len(records_raw) > MAX_SLICE_ROWS:
        raise ContentForgeError(f"{name}.records must be an array with at most {MAX_SLICE_ROWS} direct legacy records.")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for position, raw in enumerate(records_raw):
        record = require_object(raw, name=f"{name}.records[{position}]")
        reject_unknown_fields(record, name=f"{name}.records[{position}]", allowed={"id", "entity_kind", "entity_id", "changes", "rationale"})
        required = ("id", "entity_kind", "entity_id", "changes", "rationale")
        missing = [field for field in required if field not in record]
        if missing:
            raise ContentForgeError(f"{name}.records[{position}] is missing required field(s): " + ", ".join(missing))
        record_id = require_identifier(record["id"], name=f"{name}.records[{position}].id")
        if record_id in seen:
            raise ContentForgeError(f"{name}.records repeats id {record_id!r}.")
        seen.add(record_id)
        entity_kind = require_string(record["entity_kind"], name=f"{name}.records[{position}].entity_kind", maximum=20).casefold()
        if entity_kind not in {"item", "troop"}:
            raise ContentForgeError(f"{name}.records[{position}].entity_kind must be item or troop.")
        entity_id = require_string(record["entity_id"], name=f"{name}.records[{position}].entity_id", maximum=180)
        expected_prefix = "itm_" if entity_kind == "item" else "trp_"
        if not entity_id.startswith(expected_prefix):
            raise ContentForgeError(f"{name}.records[{position}].entity_id must begin {expected_prefix}.")
        changes = require_object(record["changes"], name=f"{name}.records[{position}].changes")
        if not changes:
            raise ContentForgeError(f"{name}.records[{position}].changes must not be empty.")
        records.append(
            {
                "id": record_id,
                "entity_kind": entity_kind,
                "entity_id": entity_id,
                "changes": deep_copy_json(changes),
                "rationale": require_string(record["rationale"], name=f"{name}.records[{position}].rationale", maximum=MAX_DESCRIPTION_LENGTH),
            }
        )
    return {"records": records}


def normalize_presentation_slice(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"changes", "new_presentations", "screens"})
    new_raw = item.get("new_presentations", [])
    if not isinstance(new_raw, list) or len(new_raw) > MAX_SLICE_ROWS:
        raise ContentForgeError(f"{name}.new_presentations must be an array with at most {MAX_SLICE_ROWS} entries.")
    new_presentations: list[dict[str, Any]] = []
    ids: set[str] = set()
    for position, raw in enumerate(new_raw):
        presentation = require_object(raw, name=f"{name}.new_presentations[{position}]")
        reject_unknown_fields(presentation, name=f"{name}.new_presentations[{position}]", allowed={"anchor", "id", "flags", "mesh", "triggers", "description"})
        anchor = require_identifier(presentation.get("anchor"), name=f"{name}.new_presentations[{position}].anchor", pattern=ENTRYPOINT_RE)
        identifier = require_identifier(presentation.get("id"), name=f"{name}.new_presentations[{position}].id", pattern=TOKEN_RE)
        if identifier in ids:
            raise ContentForgeError(f"{name}.new_presentations repeats id {identifier!r}.")
        ids.add(identifier)
        row: dict[str, Any] = {"anchor": anchor, "id": identifier}
        if "flags" in presentation:
            row["flags"] = deep_copy_json(presentation["flags"])
        if "mesh" in presentation:
            row["mesh"] = deep_copy_json(presentation["mesh"])
        if "triggers" in presentation:
            if not isinstance(presentation["triggers"], list) or len(presentation["triggers"]) > 100:
                raise ContentForgeError(f"{name}.new_presentations[{position}].triggers must be an array with at most 100 typed callback blocks.")
            row["triggers"] = deep_copy_json(presentation["triggers"])
        if "description" in presentation:
            row["description"] = require_string(presentation["description"], name=f"{name}.new_presentations[{position}].description", maximum=MAX_DESCRIPTION_LENGTH)
        new_presentations.append(row)
    screens = normalize_beat_rows(item.get("screens", []), name=f"{name}.screens", purpose_name="description")
    for position, screen in enumerate(screens):
        if screen.get("entrypoint") is None:
            raise ContentForgeError(f"{name}.screens[{position}].entrypoint must name the existing presentation entrypoint that owns this screen.")
    return {
        "changes": normalize_source_changes(item.get("changes", []), name=f"{name}.changes"),
        "new_presentations": new_presentations,
        "screens": screens,
    }


def normalize_verification(value: Any, *, name: str) -> dict[str, Any]:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"tests", "require_blueprint", "scenarios"})
    required = ("tests", "require_blueprint")
    missing = [field for field in required if field not in item]
    if missing:
        raise ContentForgeError(f"{name} is missing required field(s): " + ", ".join(missing))
    tests = require_string_list(item["tests"], name=f"{name}.tests", maximum=24, item_pattern=SAFE_TEST_RE)
    return {
        "tests": tests,
        "require_blueprint": require_boolean(item["require_blueprint"], name=f"{name}.require_blueprint"),
        "scenarios": require_string_list(item.get("scenarios", []), name=f"{name}.scenarios", maximum=MAX_SCENARIOS, item_pattern=SCENARIO_ID_RE),
    }


def normalize_content_pack(value: Any, *, name: str = "pack") -> ContentPack:
    item = require_object(value, name=name)
    reject_unknown_fields(item, name=name, allowed={"schema", "id", "title", "status", "description", "brief", "blueprint_id", "slices", "verification"})
    required = ("schema", "id", "title", "status", "description", "brief", "slices", "verification")
    missing = [field for field in required if field not in item]
    if missing:
        raise ContentForgeError(f"{name} is missing required field(s): " + ", ".join(missing))
    if item["schema"] != CONTENT_PACK_SCHEMA:
        raise ContentForgeError(f"{name}.schema must be {CONTENT_PACK_SCHEMA!r}.")
    identifier = require_identifier(item["id"], name=f"{name}.id")
    status = require_string(item["status"], name=f"{name}.status", maximum=20)
    if status not in VALID_STATUSES:
        raise ContentForgeError(f"{name}.status must be one of: " + ", ".join(sorted(VALID_STATUSES)))
    blueprint_id = item.get("blueprint_id")
    if blueprint_id is not None:
        blueprint_id = require_identifier(blueprint_id, name=f"{name}.blueprint_id")
    slices_raw = require_object(item["slices"], name=f"{name}.slices")
    reject_unknown_fields(slices_raw, name=f"{name}.slices", allowed=VALID_SLICES)
    if not slices_raw:
        raise ContentForgeError(f"{name}.slices must contain at least one authoring slice.")
    normalizers = {
        "dialogue": normalize_dialogue_slice,
        "quest_event": normalize_quest_event_slice,
        "campaign_ai": normalize_campaign_ai_slice,
        "troop_item": normalize_troop_item_slice,
        "presentation": normalize_presentation_slice,
    }
    slices = {slice_id: normalizers[slice_id](slices_raw[slice_id], name=f"{name}.slices.{slice_id}") for slice_id in SLICE_ORDER if slice_id in slices_raw}
    raw: dict[str, Any] = {
        "schema": CONTENT_PACK_SCHEMA,
        "id": identifier,
        "title": require_string(item["title"], name=f"{name}.title", maximum=200),
        "status": status,
        "description": require_string(item["description"], name=f"{name}.description", maximum=MAX_DESCRIPTION_LENGTH),
        "brief": normalize_brief(item["brief"], name=f"{name}.brief"),
        "slices": slices,
        "verification": normalize_verification(item["verification"], name=f"{name}.verification"),
    }
    if blueprint_id is not None:
        raw["blueprint_id"] = blueprint_id
    return ContentPack(
        id=identifier,
        title=raw["title"],
        status=status,
        description=raw["description"],
        brief=raw["brief"],
        blueprint_id=blueprint_id,
        slices=raw["slices"],
        verification=raw["verification"],
        raw=raw,
    )


def catalog_signature(root: Path) -> tuple[Any, ...]:
    path = root / CONTENT_PACKS_RELATIVE
    try:
        status = path.stat()
    except OSError:
        return (str(path), -1, -1)
    return (str(path), status.st_mtime_ns, status.st_size)


def content_catalog_path(root: Path) -> Path:
    """Return the one checked-in catalog Content Forge may persist.

    This is deliberately not a caller-controlled path. The optional human
    Studio and the MCP tool may save a strict pack contract, but neither gets
    a generic file-write capability or a route into module source/output
    layers.
    """

    resolved_root = root.resolve()
    path = (resolved_root / CONTENT_PACKS_RELATIVE).resolve()
    try:
        path.relative_to(resolved_root)
    except ValueError as error:  # pragma: no cover - constant defensive guard
        raise ContentForgeError("Content Forge catalog path must stay inside the workspace.") from error
    return path


def read_pack_catalog_document(root: Path) -> tuple[Path, str, dict[str, Any], tuple[ContentPack, ...]]:
    """Read and validate the catalog while retaining its stable JSON ordering.

    Retaining the parsed document lets a catalog save replace or append exactly
    one normalized pack while keeping all unrelated pack object order and
    fields intact in the planned JSON diff.
    """

    path = content_catalog_path(root)
    try:
        text = path.read_text(encoding="utf-8")
        raw = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise ContentForgeError(f"Could not read Content Forge catalog {path}: {error}") from error
    catalog = require_object(raw, name="content pack catalog")
    reject_unknown_fields(catalog, name="content pack catalog", allowed={"schema", "packs"})
    if catalog.get("schema") != CONTENT_PACK_CATALOG_SCHEMA:
        raise ContentForgeError(f"Content Forge catalog schema must be {CONTENT_PACK_CATALOG_SCHEMA!r}.")
    rows = catalog.get("packs")
    if not isinstance(rows, list) or len(rows) > MAX_PACKS:
        raise ContentForgeError(f"Content Forge catalog must contain an array of at most {MAX_PACKS} packs.")
    packs = [normalize_content_pack(row, name=f"packs[{position}]") for position, row in enumerate(rows)]
    ids = [pack.id for pack in packs]
    if len(set(ids)) != len(ids):
        raise ContentForgeError("Content Forge catalog repeats a pack ID.")
    return path, text, catalog, tuple(packs)


def load_pack_catalog(root: Path) -> tuple[ContentPack, ...]:
    return read_pack_catalog_document(root)[3]


def catalog_mode(value: Any) -> str:
    checked = require_string(value, name="mode", maximum=20).casefold()
    if checked not in VALID_CATALOG_MODES:
        raise ContentForgeError("mode must be one of: " + ", ".join(sorted(VALID_CATALOG_MODES)))
    return checked


def catalog_text(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def catalog_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def catalog_unified_diff(path: Path, root: Path, before: str, after: str) -> str:
    relative = project_relative(path, root)
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{relative}",
            tofile=f"b/{relative}",
            n=3,
        )
    )


def _catalog_update_plan(
    index: ContentForgeIndex,
    *,
    pack_value: Any,
    mode: str,
) -> tuple[ContentPack, Path, str, str, str]:
    """Construct a strict, one-pack catalog update without writing it."""

    pack = normalize_content_pack(pack_value, name="pack")
    checked_mode = catalog_mode(mode)
    path, before, catalog, packs = read_pack_catalog_document(index.root)
    existing_index = next((position for position, item in enumerate(packs) if item.id == pack.id), None)
    if checked_mode == "create" and existing_index is not None:
        raise ContentForgeError(
            f"Content pack {pack.id!r} already exists. Use mode='replace' after reviewing the existing pack."
        )
    if checked_mode == "replace" and existing_index is None:
        raise ContentForgeError(
            f"Content pack {pack.id!r} does not exist. Use mode='create' for a new catalog pack."
        )

    updated = deep_copy_json(catalog)
    rows = updated["packs"]
    if not isinstance(rows, list):  # read_pack_catalog_document already proves this; retain a narrow guard.
        raise ContentForgeError("Content Forge catalog packs must be an array.")
    if checked_mode == "create":
        rows.append(deep_copy_json(pack.raw))
        operation = "created"
    else:
        assert existing_index is not None
        rows[existing_index] = deep_copy_json(pack.raw)
        operation = "replaced"
    after = catalog_text(updated)
    if after == before:
        raise ContentForgeError("The proposed Content Pack is already identical to the checked-in catalog entry.")
    return pack, path, before, after, operation


def content_pack_catalog_plan(
    index: ContentForgeIndex,
    *,
    pack_value: Any,
    mode: str,
) -> dict[str, Any]:
    """Plan a strict Content Forge catalog create/replace operation.

    The catalog is an authoring contract, not module source. This is the one
    persistence path used by the visual pack editor and is intentionally
    narrower than a generic JSON/file editor.
    """

    pack, path, before, after, operation = _catalog_update_plan(index, pack_value=pack_value, mode=mode)
    base_sha = catalog_sha256(before)
    proposed_sha = catalog_sha256(after)
    identity = {
        "path": project_relative(path, index.root),
        "mode": mode,
        "pack": pack.raw,
        "base_sha256": base_sha,
        "proposed_sha256": proposed_sha,
    }
    plan_id = f"content-catalog-plan:{digest(identity)}"
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": "ready_for_review",
        "catalog_plan_id": plan_id,
        "operation": operation,
        "mode": catalog_mode(mode),
        "pack": pack_payload(pack),
        "catalog_target": {
            "path": project_relative(path, index.root),
            "base_sha256": base_sha,
            "proposed_sha256": proposed_sha,
        },
        "unified_diff": catalog_unified_diff(path, index.root, before, after),
        "apply_contract": {
            "tool": "content_pack_catalog_apply",
            "dry_run_default": True,
            "required_catalog_plan_id": plan_id,
            "required_catalog_sha256": base_sha,
            "non_dry_confirmation": CONTENT_CATALOG_SAVE_CONFIRMATION,
            "writes": [project_relative(path, index.root)],
            "never_writes": ["src/**", "compile/**", "compile/ids/**", "_export/**", "*.txt exports"],
        },
        "warnings": [
            *index.warnings,
            "This plan persists only the strict DevKit Content Forge catalog entry. It does not create module source, generated modules, IDs, or exports.",
        ],
    }


def _atomic_write_catalog(path: Path, text: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except OSError as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise ContentForgeError(f"Could not atomically save the Content Forge catalog: {error}") from error


def content_pack_catalog_apply(
    index: ContentForgeIndex,
    *,
    pack_value: Any,
    mode: str,
    expected_catalog_plan_id: str,
    expected_catalog_sha256: str,
    dry_run: bool = True,
    confirmation: str | None = None,
) -> dict[str, Any]:
    """Rehearse or persist one reviewed strict Content Forge catalog change."""

    if not isinstance(dry_run, bool):
        raise ContentForgeError("dry_run must be a boolean.")
    checked_plan_id = require_string(expected_catalog_plan_id, name="expected_catalog_plan_id", maximum=160)
    try:
        checked_sha = change_router.require_sha256(expected_catalog_sha256, name="expected_catalog_sha256")
    except change_router.ChangeRouterError as error:
        raise ContentForgeError(str(error)) from error
    if not dry_run and confirmation != CONTENT_CATALOG_SAVE_CONFIRMATION:
        raise ContentForgeError(
            "A non-dry catalog save requires confirmation exactly equal to "
            f"{CONTENT_CATALOG_SAVE_CONFIRMATION!r}."
        )
    plan = content_pack_catalog_plan(index, pack_value=pack_value, mode=mode)
    if plan["catalog_plan_id"] != checked_plan_id:
        raise ContentForgeError("expected_catalog_plan_id does not match the current catalog plan; refresh and review it.")
    target = plan["catalog_target"]
    if target["base_sha256"] != checked_sha:
        raise ContentForgeError("expected_catalog_sha256 does not match the current packs.json content; refresh and review the catalog plan.")
    if dry_run:
        return {
            "applied": False,
            "dry_run": True,
            "catalog_plan": plan,
            "warnings": [
                "Dry-run proves the current catalog SHA and strict pack contract without writing.",
                "A real save writes only devkit/content_forge/packs.json after the exact confirmation phrase.",
            ],
        }
    _pack, path, before, after, _operation = _catalog_update_plan(index, pack_value=pack_value, mode=mode)
    if catalog_sha256(before) != checked_sha:
        raise ContentForgeError("Content Forge catalog changed after planning; refusing to save a stale pack draft.")
    _atomic_write_catalog(path, after)
    invalidate_content_forge(index.root)
    return {
        "applied": True,
        "dry_run": False,
        "catalog_plan_id": checked_plan_id,
        "catalog_target": {
            "path": project_relative(path, index.root),
            "base_sha256": checked_sha,
            "result_sha256": catalog_sha256(after),
        },
        "follow_up": {
            "tool": "content_pack_explain",
            "pack_id": str(plan["pack"]["id"]),
            "note": "The checked-in pack contract changed. Re-explain, validate, plan, and review it before any source change.",
        },
        "warnings": [
            "Saved only the strict Content Forge catalog. No module source, generated module, ID table, or export was written.",
        ],
    }


def build_content_forge(root: Path = DEFAULT_REPO_ROOT) -> ContentForgeIndex:
    """Build the pack registry and shared Feature Authoring index without writing."""

    resolved_root = root.resolve()
    features = feature_authoring.build_feature_authoring(resolved_root)
    signature = (features.router.signature, catalog_signature(resolved_root))
    cached = _CACHE.get(resolved_root)
    if cached is not None and cached[0] == signature:
        return cached[1]
    packs = load_pack_catalog(resolved_root)
    index = ContentForgeIndex(
        root=resolved_root,
        features=features,
        packs=packs,
        packs_by_id={pack.id: pack for pack in packs},
        warnings=[
            "Content Forge packs are typed orchestration contracts. Canonical modular src/ fragments remain authoritative and preserve their existing top-to-bottom assembly order.",
            "Dialogue, presentation, module, campaign, and balance edits remain delegated to their specialist semantic compilers; a pack has no raw source or tuple escape hatch.",
            "Each apply is one named change. A multi-slice pack is intentionally not presented as a fake transaction; re-plan after every non-dry source edit.",
            "Human review is returned as a deterministic review canvas, but JSON CLI/MCP planning and evidence remain the primary interface.",
        ],
    )
    _CACHE[resolved_root] = (signature, index)
    return index


def invalidate_content_forge(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def require_pack(index: ContentForgeIndex, pack_id: Any) -> ContentPack:
    identifier = require_identifier(pack_id, name="pack_id")
    pack = index.packs_by_id.get(identifier)
    if pack is None:
        raise ContentForgeError("Unknown content pack; use content_forge_summary or content_pack_find.")
    return pack


def resolve_pack(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
) -> ContentPack:
    if (pack_id is None) == (pack_value is None):
        raise ContentForgeError("Supply exactly one of pack_id or pack.")
    if pack_id is not None:
        return require_pack(index, pack_id)
    return normalize_content_pack(pack_value, name="pack")


def slice_summary(pack: ContentPack, slice_id: str) -> dict[str, Any]:
    value = pack.slices[slice_id]
    if slice_id == "dialogue":
        return {"id": slice_id, "source_change_count": len(value["changes"]), "beat_count": len(value["beats"])}
    if slice_id == "quest_event":
        return {"id": slice_id, "source_change_count": len(value["changes"]), "timeline_step_count": len(value["timeline"])}
    if slice_id == "campaign_ai":
        return {"id": slice_id, "source_change_count": len(value["changes"]), "contract_count": len(value["contracts"]), "scenario_count": len(value["scenarios"])}
    if slice_id == "presentation":
        return {"id": slice_id, "source_change_count": len(value["changes"]), "new_presentation_count": len(value["new_presentations"]), "screen_count": len(value["screens"])}
    return {"id": slice_id, "record_count": len(value["records"]), "legacy_authoring_only": True}


def pack_payload(pack: ContentPack) -> dict[str, Any]:
    return {
        "schema": CONTENT_PACK_SCHEMA,
        "id": pack.id,
        "title": pack.title,
        "status": pack.status,
        "description": pack.description,
        "brief": copy.deepcopy(dict(pack.brief)),
        "blueprint_id": pack.blueprint_id,
        "slice_count": len(pack.slices),
        "slices": [slice_summary(pack, slice_id) for slice_id in SLICE_ORDER if slice_id in pack.slices],
        "verification": copy.deepcopy(dict(pack.verification)),
        "pack_fingerprint": digest(pack.raw),
    }


def collect_entrypoints(pack: ContentPack, source_changes: Sequence[SourceChange]) -> tuple[str, ...]:
    values = [change.target for change in source_changes]
    dialogue = pack.slices.get("dialogue")
    if dialogue:
        values.extend(row["entrypoint"] for row in dialogue["beats"] if "entrypoint" in row)
    quest_event = pack.slices.get("quest_event")
    if quest_event:
        values.extend(row["entrypoint"] for row in quest_event["timeline"] if "entrypoint" in row)
    campaign_ai = pack.slices.get("campaign_ai")
    if campaign_ai:
        values.extend(contract["entrypoint"] for contract in campaign_ai["contracts"])
    presentation = pack.slices.get("presentation")
    if presentation:
        values.extend(screen["entrypoint"] for screen in presentation["screens"])
    return tuple(dict.fromkeys(values))


def compile_content_pack(index: ContentForgeIndex, pack: ContentPack) -> ContentCompilation:
    """Compile pack slices into a Feature Intent plus narrow Balance Lab records."""

    source_changes: list[SourceChange] = []
    source_rows: list[dict[str, Any]] = []
    ordinal_by_slice: Counter[str] = Counter()

    def add_source(slice_id: str, kind: str, value: Mapping[str, Any]) -> None:
        ordinal_by_slice[slice_id] += 1
        number = len(source_changes) + 1
        body = deep_copy_json(value)
        body["kind"] = kind
        content_change_id = f"content-change:{slice_id}:{ordinal_by_slice[slice_id]:02d}"
        source_changes.append(
            SourceChange(
                content_change_id=content_change_id,
                slice_id=slice_id,
                feature_change_id=f"feature-change:{number:02d}",
                target=str(body["target"]),
                action=str(body["action"]),
                kind=kind,
                source=body,
            )
        )
        source_rows.append(body)

    for slice_id, kind in (("quest_event", "module"), ("campaign_ai", "module"), ("dialogue", "dialogue"), ("presentation", "presentation")):
        value = pack.slices.get(slice_id)
        if value is None:
            continue
        for change in value["changes"]:
            add_source(slice_id, kind, change)
    presentation = pack.slices.get("presentation")
    if presentation is not None:
        for new_presentation in presentation["new_presentations"]:
            new_item = {key: deep_copy_json(value) for key, value in new_presentation.items() if key in {"id", "flags", "mesh", "triggers"}}
            add_source(
                "presentation",
                "module",
                {
                    "target": new_presentation["anchor"],
                    "action": "add_presentation",
                    "new_item": new_item,
                },
            )
    balance_changes: list[BalanceChange] = []
    troop_item = pack.slices.get("troop_item")
    if troop_item is not None:
        for position, record in enumerate(troop_item["records"], start=1):
            balance_changes.append(
                BalanceChange(
                    content_change_id=f"content-change:troop_item:{position:02d}",
                    slice_id="troop_item",
                    record_id=record["id"],
                    entity_kind=record["entity_kind"],
                    entity_id=record["entity_id"],
                    changes=record["changes"],
                    rationale=record["rationale"],
                )
            )
    entrypoints = collect_entrypoints(pack, source_changes)
    feature_intent: Mapping[str, Any] | None = None
    if entrypoints or source_rows:
        feature_intent = {
            "schema": feature_authoring.FEATURE_INTENT_SCHEMA,
            "id": pack.id,
            "title": pack.title,
            "status": pack.status,
            "description": pack.description,
            "entrypoints": list(entrypoints),
            "changes": source_rows,
            "verification": {
                "tests": list(pack.verification["tests"]),
                "require_blueprint": bool(pack.verification["require_blueprint"]),
            },
        }
        if pack.blueprint_id is not None:
            feature_intent["blueprint_id"] = pack.blueprint_id
    if source_rows and not entrypoints:
        raise ContentForgeError("Source content changes must resolve at least one engine entrypoint.")
    return ContentCompilation(
        pack=pack,
        feature_intent=feature_intent,
        source_changes=tuple(source_changes),
        balance_changes=tuple(balance_changes),
        entrypoints=entrypoints,
    )


def content_forge_summary(index: ContentForgeIndex, *, limit: int = 30) -> dict[str, Any]:
    maximum = require_limit(limit, name="limit")
    packs = sorted(index.packs, key=lambda item: (item.status != "active", item.id))
    slice_counts = Counter(slice_id for pack in index.packs for slice_id in pack.slices)
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "pack_count": len(packs),
        "returned_pack_count": min(len(packs), maximum),
        "packs_truncated": len(packs) > maximum,
        "packs": [pack_payload(pack) for pack in packs[:maximum]],
        "slice_coverage": {slice_id: slice_counts[slice_id] for slice_id in SLICE_ORDER},
        "capabilities": {
            "dialogue": "First-match-aware dialogue changes and authored narrative beats through the existing Dialogue Composer.",
            "quest_event": "Typed scripts, quests, menus, mission callbacks, and timeline review through Feature Authoring/Module Atlas.",
            "campaign_ai": "Typed source changes plus declared stationary/patrol/escort/raid-return/despawn intent evidence and bounded scenario obligations.",
            "troop_item": "Direct existing legacy item/troop record edits through Balance Lab; record insertion/reordering stays deliberately outside this order-sensitive slice.",
            "presentation": "Existing layout edits through Presentation Layout plus typed creation of a new presentation at a named presentation anchor.",
            "catalog": "Strict checked-in Content Pack create/replace planning through an exact packs.json diff and separate SHA/confirmation gate; it does not apply module content.",
        },
        "simple_workflow": [
            "content_pack_explain: inspect the brief, tone, acceptance criteria, slices, real entrypoints, and declared order dependencies.",
            "content_pack_plan and content_pack_review: compile exact independent source/balance plans and inspect the deterministic review canvas.",
            "content_pack_catalog_plan: optionally review a strict create/replace diff for the checked-in authoring contract itself before saving it through its separate catalog SHA gate.",
            "content_pack_apply: rehearse or apply exactly one named plan change with the current pack-plan and SHA guards.",
            "content_pack_verify: re-check specialist evidence, AI contracts, declared scenarios, and optional focused tests after reviewed edits.",
        ],
        "warnings": index.warnings,
    }


def content_pack_find(index: ContentForgeIndex, query: str, *, slice_name: str = "all", limit: int = 30) -> dict[str, Any]:
    needle = require_string(query, name="query", maximum=500).casefold()
    maximum = require_limit(limit, name="limit")
    selected = require_string(slice_name, name="slice", maximum=40).casefold().replace("-", "_")
    if selected != "all" and selected not in VALID_SLICES:
        raise ContentForgeError("slice must be all or one of: " + ", ".join(SLICE_ORDER))
    matched = []
    for pack in index.packs:
        if selected != "all" and selected not in pack.slices:
            continue
        haystack = canonical_json(pack.raw).casefold()
        if needle in haystack:
            matched.append(pack)
    matched.sort(key=lambda item: (item.status != "active", item.id))
    return {
        "query": query,
        "slice": selected,
        "match_count": len(matched),
        "returned_count": min(len(matched), maximum),
        "truncated": len(matched) > maximum,
        "packs": [pack_payload(pack) for pack in matched[:maximum]],
        "warnings": index.warnings,
    }


def feature_validation(index: ContentForgeIndex, compilation: ContentCompilation) -> dict[str, Any] | None:
    if compilation.feature_intent is None:
        return None
    try:
        return feature_authoring.feature_intent_validate(index.features, intent_value=compilation.feature_intent)
    except feature_authoring.FeatureAuthoringError as error:
        return {
            "state": "blocked",
            "errors": [{"code": "feature_intent_invalid", "message": str(error)}],
            "warnings": [],
        }


def declared_scenario_ids(pack: ContentPack) -> tuple[str, ...]:
    values = list(pack.verification["scenarios"])
    campaign_ai = pack.slices.get("campaign_ai")
    if campaign_ai is not None:
        values.extend(campaign_ai["scenarios"])
    return tuple(dict.fromkeys(values))


def scenario_validation(index: ContentForgeIndex, pack: ContentPack) -> dict[str, Any]:
    ids = declared_scenario_ids(pack)
    if not ids:
        return {"declared": [], "available": [], "errors": [], "warnings": []}
    try:
        scenarios = campaign_scenario_fuzzer.build_scenario_fuzzer(index.root)
    except campaign_scenario_fuzzer.ScenarioFuzzerError as error:
        return {"declared": list(ids), "available": [], "errors": [{"code": "scenario_catalog_unavailable", "message": str(error)}], "warnings": []}
    available: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for scenario_id in ids:
        try:
            row = campaign_scenario_fuzzer.scenario_catalog_payload(scenarios, scenario_id=scenario_id)
        except campaign_scenario_fuzzer.ScenarioFuzzerError as error:
            errors.append({"code": "unknown_scenario", "scenario_id": scenario_id, "message": str(error)})
        else:
            available.extend(row["scenarios"])
    return {"declared": list(ids), "available": available, "errors": errors, "warnings": scenarios.warnings}


def entrypoint_payloads(index: ContentForgeIndex, entrypoints: Sequence[str], *, trace_limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    maximum = require_limit(trace_limit, name="trace_limit", maximum=30)
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for entrypoint_id in entrypoints[:maximum]:
        entry = index.features.by_entrypoint_id.get(entrypoint_id)
        if entry is None:
            errors.append(f"Unknown engine entrypoint: {entrypoint_id}")
            continue
        rows.append(feature_authoring.entrypoint_payload(index.features, entry))
    return rows, errors


def content_pack_explain(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    compilation = compile_content_pack(index, pack)
    validation = feature_validation(index, compilation)
    entrypoints, trace_errors = entrypoint_payloads(index, compilation.entrypoints, trace_limit=trace_limit)
    scenarios = scenario_validation(index, pack)
    errors: list[dict[str, Any]] = []
    if validation is not None:
        errors.extend(validation.get("errors", []))
    errors.extend(scenarios["errors"])
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": "blocked" if errors else "ready",
        "pack": pack_payload(pack),
        "pack_source": copy.deepcopy(dict(pack.raw)),
        "compiled_feature_intent": copy.deepcopy(compilation.feature_intent),
        "source_change_count": len(compilation.source_changes),
        "balance_change_count": len(compilation.balance_changes),
        "engine_entrypoints": entrypoints,
        "engine_entrypoint_count": len(compilation.entrypoints),
        "engine_entrypoints_truncated": len(compilation.entrypoints) > len(entrypoints),
        "feature_validation": validation,
        "scenario_validation": scenarios,
        "errors": errors,
        "warnings": [
            *index.warnings,
            *trace_errors,
            *scenarios["warnings"],
            "A content pack describes authoring intent and evidence. It does not claim that all engine branches, saves, or in-game UI rendering have been emulated.",
        ],
    }


def content_pack_validate(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    compilation = compile_content_pack(index, pack)
    feature = feature_validation(index, compilation)
    scenarios = scenario_validation(index, pack)
    errors: list[dict[str, Any]] = []
    if feature is not None:
        errors.extend(feature.get("errors", []))
    errors.extend(scenarios["errors"])
    if pack.status == "disabled" and (compilation.source_changes or compilation.balance_changes):
        errors.append({"code": "disabled_pack_has_changes", "message": "Disabled content packs may be reviewed but cannot produce an apply plan."})
    if (compilation.source_changes or compilation.balance_changes) and not pack.verification["tests"]:
        errors.append({"code": "changes_require_tests", "message": "A content pack with source or legacy-record changes must declare at least one existing build/test_*.py test."})
    missing_tests = [test for test in pack.verification["tests"] if not (index.root / test).is_file()]
    for test in missing_tests:
        errors.append({"code": "missing_declared_test", "path": test, "message": f"Declared focused test is missing: {test}"})
    if pack.verification["require_blueprint"] and pack.blueprint_id is None:
        errors.append({"code": "blueprint_required", "message": "verification.require_blueprint is true but blueprint_id is not declared."})
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": "blocked" if errors else "ready",
        "pack": pack_payload(pack),
        "compiled_feature_intent": copy.deepcopy(compilation.feature_intent),
        "source_changes": [
            {"change_id": change.content_change_id, "slice": change.slice_id, "feature_change_id": change.feature_change_id, "kind": change.kind, "target": change.target, "action": change.action}
            for change in compilation.source_changes
        ],
        "balance_changes": [
            {"change_id": change.content_change_id, "slice": change.slice_id, "record_id": change.record_id, "entity_kind": change.entity_kind, "entity_id": change.entity_id, "rationale": change.rationale}
            for change in compilation.balance_changes
        ],
        "feature_validation": feature,
        "scenario_validation": scenarios,
        "errors": errors,
        "warnings": [
            *index.warnings,
            *scenarios["warnings"],
            "Validation checks the typed pack contract and known specialist constraints before planning. It does not write source or run a build/export.",
        ],
    }


def content_pack_compile(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    compilation = compile_content_pack(index, pack)
    validation = content_pack_validate(index, pack_value=pack.raw)
    source_order = [
        {
            "sequence": position,
            "change_id": change.content_change_id,
            "slice": change.slice_id,
            "backend": "feature_authoring",
            "feature_change_id": change.feature_change_id,
            "target": change.target,
            "action": change.action,
            "kind": change.kind,
        }
        for position, change in enumerate(compilation.source_changes, start=1)
    ]
    balance_order = [
        {
            "sequence": len(source_order) + position,
            "change_id": change.content_change_id,
            "slice": change.slice_id,
            "backend": "troop_item_balance",
            "record_id": change.record_id,
            "entity_kind": change.entity_kind,
            "entity_id": change.entity_id,
            "rationale": change.rationale,
        }
        for position, change in enumerate(compilation.balance_changes, start=1)
    ]
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": validation["state"],
        "pack": pack_payload(pack),
        "compiled_feature_intent": copy.deepcopy(compilation.feature_intent),
        "apply_sequence": [*source_order, *balance_order],
        "order_policy": {
            "slice_compilation_order": list(SLICE_ORDER),
            "source_apply_boundary": "One named source change at a time. Re-plan after every non-dry apply because modular ordering and text anchors can change.",
            "legacy_record_boundary": "Existing direct troop/item records only. New records and record reordering remain outside Content Forge so generated IDs and legacy ordering are never silently shifted.",
        },
        "validation": validation,
        "warnings": [
            *validation["warnings"],
            "Compile is read-only and produces a typed route into specialist compilers. Use content_pack_plan for exact diff/SHA evidence.",
        ],
    }


def prospective_sources(
    index: ContentForgeIndex,
    compiled_changes: Sequence[feature_authoring.CompiledChange],
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    """Reconstruct proposed source text solely from already-validated change edits."""

    by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for change in compiled_changes:
        by_path[change.source_path].extend(change.edits)
    sources: dict[str, str] = {}
    errors: list[dict[str, Any]] = []
    for relative, edits in sorted(by_path.items()):
        path = index.root / relative
        try:
            raw, _encoding, _raw_bytes = change_router.read_text_with_encoding(path)
            updated, _planned = change_router.prepare_edits(raw, edits)
        except (OSError, change_router.ChangeRouterError) as error:
            errors.append({"code": "prospective_source_unavailable", "path": relative, "message": str(error)})
            continue
        sources[relative] = updated
    return sources, errors


def generic_ai_contract(pack: ContentPack, contract: Mapping[str, Any], entry: feature_authoring.Entrypoint) -> dict[str, Any] | None:
    if entry.family != "script":
        return None
    result: dict[str, Any] = {
        "id": f"content-pack:{pack.id}:{contract['id']}",
        "kind": "party_ai_intent",
        "intent": AI_INTENT_MAP[str(contract["intent"])],
        "description": contract["description"],
        "scope_scripts": [f"script_{entry.name}", *contract.get("additional_scope_scripts", [])],
    }
    for field in (
        "party_template", "party_selector", "expected_behavior", "forbidden_behaviors", "allowed_when",
        "minimum_radius", "maximum_radius", "attach_to", "require_detach", "return_behavior",
        "return_target", "return_when", "despawn_when",
    ):
        if field in contract:
            result[field] = copy.deepcopy(contract[field])
    return result


def contract_state_result(
    doctor: campaign_state_doctor.StateDoctorIndex,
    pack: ContentPack,
    contract: Mapping[str, Any],
    entry: feature_authoring.Entrypoint | None,
) -> dict[str, Any]:
    contract_id = contract.get("state_contract_id")
    if isinstance(contract_id, str):
        matched = next((row for row in doctor.contract_results if row.get("id") == contract_id), None)
        if matched is None:
            return {"passed": False, "state": "missing", "message": f"Checked-in state contract {contract_id!r} was not found.", "result": None}
        return {"passed": bool(matched.get("passed")), "state": "checked_in", "message": "Evaluated checked-in state/AI contract.", "result": matched}
    if entry is None:
        return {"passed": False, "state": "missing_entrypoint", "message": "AI contract entrypoint is not in the engine registry.", "result": None}
    generated = generic_ai_contract(pack, contract, entry)
    if generated is None:
        return {"passed": False, "state": "unsupported_entrypoint", "message": "Inline AI intent contracts require an entrypoint:script:* target or a checked-in state_contract_id.", "result": None}
    try:
        result = campaign_state_doctor.evaluate_party_ai_intent(generated, doctor)
    except campaign_state_doctor.CampaignStateError as error:
        return {"passed": False, "state": "evaluation_error", "message": str(error), "result": None}
    return {"passed": bool(result.get("passed")), "state": "inline", "message": "Evaluated the pack's derived generic party-AI contract against current source.", "result": result}


def compact_contract_result(value: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        "id": value.get("id"),
        "kind": value.get("kind"),
        "intent": value.get("intent"),
        "passed": value.get("passed"),
        "check_count": value.get("check_count"),
        "violation_count": value.get("violation_count"),
        "violations": list(value.get("violations", []))[:8] if isinstance(value.get("violations"), list) else [],
        "checks": list(value.get("checks", []))[:12] if isinstance(value.get("checks"), list) else [],
    }


def ai_contract_evidence(
    index: ContentForgeIndex,
    pack: ContentPack,
    *,
    proposed: Mapping[str, str] | None = None,
    compiled_changes: Sequence[feature_authoring.CompiledChange] = (),
    allow_pending_source_change: bool = False,
) -> dict[str, Any]:
    campaign_ai = pack.slices.get("campaign_ai")
    if campaign_ai is None or not campaign_ai["contracts"]:
        return {"contract_count": 0, "passed_count": 0, "blocked_count": 0, "pending_count": 0, "contracts": [], "errors": [], "warnings": []}
    try:
        doctor = campaign_state_doctor.build_state_doctor(index.root)
    except campaign_state_doctor.CampaignStateError as error:
        return {"contract_count": len(campaign_ai["contracts"]), "passed_count": 0, "blocked_count": len(campaign_ai["contracts"]), "pending_count": 0, "contracts": [], "errors": [{"code": "ai_state_doctor_unavailable", "message": str(error)}], "warnings": []}
    changed_entrypoints = {change.target_entrypoint_id for change in compiled_changes}
    changed_source_paths = {change.source_path for change in compiled_changes}
    rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for contract in campaign_ai["contracts"]:
        entry = index.features.by_entrypoint_id.get(contract["entrypoint"])
        source_paths = list(entry.source_paths) if entry is not None else []
        marker_rows = []
        all_found = True
        for marker in contract["required_markers"]:
            locations: list[dict[str, Any]] = []
            for relative in source_paths:
                try:
                    source = proposed.get(relative) if proposed is not None and relative in proposed else (index.root / relative).read_text(encoding="utf-8")
                except OSError as error:
                    errors.append({"code": "ai_contract_source_unavailable", "contract_id": contract["id"], "path": relative, "message": str(error)})
                    continue
                if marker in source:
                    locations.append({"path": relative, "basis": "proposed" if proposed is not None and relative in proposed else "current"})
            found = bool(locations)
            all_found = all_found and found
            marker_rows.append({"marker": marker, "found": found, "locations": locations})
        state_evidence = contract_state_result(doctor, pack, contract, entry)
        relevant_source_change = bool(
            entry
            and (
                entry.id in changed_entrypoints
                or any(path in changed_source_paths for path in entry.source_paths)
            )
        )
        state_passed = bool(state_evidence["passed"])
        if all_found and state_passed:
            state = "passed"
        elif all_found and allow_pending_source_change and relevant_source_change:
            state = "pending_post_apply_verification"
        else:
            state = "blocked"
        rows.append(
            {
                "id": contract["id"],
                "intent": contract["intent"],
                "entrypoint": contract["entrypoint"],
                "state": state,
                "required_markers": marker_rows,
                "state_contract_evidence": {
                    "state": state_evidence["state"],
                    "passed": state_passed,
                    "message": state_evidence["message"],
                    "result": compact_contract_result(state_evidence["result"]),
                },
                "relevant_planned_source_change": relevant_source_change,
            }
        )
    return {
        "contract_count": len(rows),
        "passed_count": sum(row["state"] == "passed" for row in rows),
        "blocked_count": sum(row["state"] == "blocked" for row in rows),
        "pending_count": sum(row["state"] == "pending_post_apply_verification" for row in rows),
        "contracts": rows,
        "errors": errors,
        "warnings": [
            *doctor.warnings,
            "AI intent evidence is static. Proposed source markers are useful plan evidence, but only post-apply state-contract evaluation can prove the modeled control-flow contract against current source.",
        ],
    }


def build_content_plan(index: ContentForgeIndex, pack: ContentPack, *, trace_limit: int = 12) -> tuple[dict[str, Any], ContentCompilation]:
    compilation = compile_content_pack(index, pack)
    validation = content_pack_validate(index, pack_value=pack.raw)
    if validation["state"] == "blocked":
        body = {
            "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
            "state": "blocked",
            "pack": pack_payload(pack),
            "validation": validation,
            "changes": [],
            "warnings": [*validation["warnings"], "No content plan was produced because the pack has unresolved structural validation errors."],
        }
        return body, compilation

    feature_plan: dict[str, Any] | None = None
    compiled: tuple[feature_authoring.CompiledChange, ...] = ()
    errors: list[dict[str, Any]] = []
    if compilation.feature_intent is not None:
        try:
            intent = feature_authoring.normalize_feature_intent(compilation.feature_intent)
            feature_plan, compiled = feature_authoring.build_feature_plan(index.features, intent, trace_limit=trace_limit)
        except feature_authoring.FeatureAuthoringError as error:
            errors.append({"code": "feature_plan_failed", "message": str(error)})
        else:
            if feature_plan.get("state") != "ready_for_review":
                errors.append({"code": "feature_plan_blocked", "message": "Feature Authoring could not produce a ready source plan.", "evidence": feature_plan.get("validation")})

    prospective, prospective_errors = prospective_sources(index, compiled) if compiled else ({}, [])
    errors.extend(prospective_errors)
    ai = ai_contract_evidence(
        index,
        pack,
        proposed=prospective,
        compiled_changes=compiled,
        allow_pending_source_change=True,
    )
    errors.extend(ai["errors"])
    if ai["blocked_count"]:
        errors.append({"code": "ai_intent_blocked", "message": "One or more declared AI contracts are not proven by current/proposed static evidence.", "blocked_contract_count": ai["blocked_count"]})

    balance_index: troop_item_balance.BalanceIndex | None = None
    balance_plans: dict[str, dict[str, Any]] = {}
    if compilation.balance_changes:
        try:
            balance_index = troop_item_balance.build_balance_index(index.root)
        except troop_item_balance.BalanceError as error:
            errors.append({"code": "balance_index_unavailable", "message": str(error)})
        else:
            for change in compilation.balance_changes:
                try:
                    balance_plans[change.content_change_id] = troop_item_balance.balance_patch(
                        balance_index,
                        change.entity_kind,
                        change.entity_id,
                        changes=change.changes,
                    )
                except troop_item_balance.BalanceError as error:
                    errors.append({"code": "balance_patch_failed", "change_id": change.content_change_id, "record_id": change.record_id, "message": str(error)})

    source_rows_by_feature_id: dict[str, Mapping[str, Any]] = {}
    if feature_plan is not None:
        source_rows_by_feature_id = {str(row["change_id"]): row for row in feature_plan.get("change_plans", [])}
    changes: list[dict[str, Any]] = []
    for position, change in enumerate(compilation.source_changes, start=1):
        row = source_rows_by_feature_id.get(change.feature_change_id)
        if row is None:
            changes.append(
                {
                    "sequence": position,
                    "change_id": change.content_change_id,
                    "slice": change.slice_id,
                    "backend": "feature_authoring",
                    "feature_change_id": change.feature_change_id,
                    "target": change.target,
                    "action": change.action,
                    "state": "blocked",
                    "apply_available": False,
                    "reason": "No exact Feature Authoring patch plan is available; inspect feature_plan evidence.",
                }
            )
            continue
        router_plan = row["change_router_plan"]
        changes.append(
            {
                "sequence": position,
                "change_id": change.content_change_id,
                "slice": change.slice_id,
                "backend": "feature_authoring",
                "feature_change_id": change.feature_change_id,
                "target": change.target,
                "action": change.action,
                "kind": change.kind,
                "state": "ready_for_review" if not errors else "blocked",
                "apply_available": not errors,
                "expected_sha256": router_plan["target"]["base_sha256"],
                "source_plan": row,
            }
        )
    offset = len(changes)
    for position, change in enumerate(compilation.balance_changes, start=1):
        balance_plan = balance_plans.get(change.content_change_id)
        if balance_plan is None:
            changes.append(
                {
                    "sequence": offset + position,
                    "change_id": change.content_change_id,
                    "slice": change.slice_id,
                    "backend": "troop_item_balance",
                    "record_id": change.record_id,
                    "entity_kind": change.entity_kind,
                    "entity_id": change.entity_id,
                    "rationale": change.rationale,
                    "state": "blocked",
                    "apply_available": False,
                }
            )
            continue
        changes.append(
            {
                "sequence": offset + position,
                "change_id": change.content_change_id,
                "slice": change.slice_id,
                "backend": "troop_item_balance",
                "record_id": change.record_id,
                "entity_kind": change.entity_kind,
                "entity_id": change.entity_id,
                "rationale": change.rationale,
                "state": "ready_for_review" if not errors else "blocked",
                "apply_available": not errors,
                "expected_sha256": balance_plan["target"]["base_sha256"],
                "expected_balance_plan_sha256": balance_plan["plan_sha256"],
                "balance_plan": balance_plan,
            }
        )
    identity = {
        "pack": pack.raw,
        "feature_plan_id": feature_plan.get("plan_id") if feature_plan is not None else None,
        "changes": [
            {
                "change_id": row["change_id"],
                "backend": row["backend"],
                "expected_sha256": row.get("expected_sha256"),
                "feature_change_id": row.get("feature_change_id"),
                "balance_plan": row.get("expected_balance_plan_sha256"),
            }
            for row in changes
        ],
        "ai": [{"id": row["id"], "state": row["state"]} for row in ai["contracts"]],
    }
    plan_id = f"content-plan:{digest(identity)}"
    state = "ready_for_review" if not errors else "blocked"
    return (
        {
            "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
            "state": state,
            "plan_id": plan_id,
            "pack": pack_payload(pack),
            "validation": validation,
            "feature_plan": feature_plan,
            "ai_intent_evidence": ai,
            "change_count": len(changes),
            "changes": changes,
            "source_apply": {
                "available": bool(changes) and state == "ready_for_review",
                "scope": "one named Content Forge change / one source or direct legacy record target at a time",
                "required_content_plan_id": plan_id,
                "dry_run_default": True,
                "why": "The 1.011 module system is order-sensitive. Content Forge preserves individual specialist SHA gates instead of pretending a multi-slice apply is atomic.",
            },
            "verification_plan": {
                "focused_tests": list(pack.verification["tests"]),
                "scenarios": list(declared_scenario_ids(pack)),
                "recommended_next_tool": "content_pack_verify",
            },
            "errors": errors,
            "warnings": [
                *index.warnings,
                *(feature_plan.get("warnings", []) if feature_plan is not None else []),
                *ai["warnings"],
                "Review every exact unified diff and all ordering impact before any non-dry apply. Content Forge never writes compile/, generated ID tables, or _export/.",
            ],
        },
        compilation,
    )


def content_pack_plan(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    payload, _compilation = build_content_plan(index, pack, trace_limit=trace_limit)
    return payload


def review_label(value: str) -> str:
    return value.replace('"', "'").replace("\n", " ")[:100]


def build_review_canvas(
    pack: ContentPack,
    compilation: ContentCompilation,
    plan: Mapping[str, Any] | None,
) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = [
        {"id": "pack", "kind": "content_pack", "title": pack.title, "status": plan.get("state") if plan else pack.status, "detail": pack.brief["summary"]}
    ]
    edges: list[dict[str, Any]] = []
    mermaid = ["flowchart TD", f'    pack["{review_label(pack.title)}"]']
    for slice_id in SLICE_ORDER:
        if slice_id not in pack.slices:
            continue
        node_id = f"slice_{slice_id}"
        summary = slice_summary(pack, slice_id)
        nodes.append({"id": node_id, "kind": "slice", "title": slice_id.replace("_", " ").title(), "status": "declared", "detail": summary})
        edges.append({"from": "pack", "to": node_id, "kind": "owns"})
        mermaid.append(f'    pack --> {node_id}["{review_label(slice_id.replace("_", " ").title())}"]')
    change_rows = plan.get("changes", []) if isinstance(plan, Mapping) else []
    if isinstance(change_rows, list):
        for change in change_rows:
            if not isinstance(change, Mapping):
                continue
            change_id = str(change.get("change_id", "change"))
            safe_id = re.sub(r"[^A-Za-z0-9_]", "_", change_id)
            title = f"{change.get('slice', 'slice')}: {change.get('backend', 'backend')}"
            nodes.append({"id": safe_id, "kind": "change", "title": title, "status": change.get("state"), "detail": {"change_id": change_id, "target": change.get("target") or change.get("entity_id"), "action": change.get("action")}})
            parent = f"slice_{change.get('slice', 'unknown')}"
            edges.append({"from": parent, "to": safe_id, "kind": "compiles_to"})
            mermaid.append(f'    {parent} --> {safe_id}["{review_label(title)}"]')
    campaign_ai = pack.slices.get("campaign_ai")
    if campaign_ai:
        for contract in campaign_ai["contracts"]:
            node_id = "ai_" + re.sub(r"[^A-Za-z0-9_]", "_", contract["id"])
            nodes.append({"id": node_id, "kind": "ai_contract", "title": contract["id"], "status": "declared", "detail": {"intent": contract["intent"], "entrypoint": contract["entrypoint"]}})
            edges.append({"from": "slice_campaign_ai", "to": node_id, "kind": "requires"})
            mermaid.append(f'    slice_campaign_ai -.-> {node_id}["{review_label(contract["intent"])}"]')
    acceptance = [
        {"criterion": criterion, "state": "manual_and_static_review_required"}
        for criterion in pack.brief["acceptance_criteria"]
    ]
    return {
        "format": "sod-modern.content-review-canvas.v1",
        "nodes": nodes,
        "edges": edges,
        "mermaid": "\n".join(mermaid),
        "brief_card": copy.deepcopy(dict(pack.brief)),
        "acceptance_review": acceptance,
        "human_ui_boundary": "This review canvas is intentionally structured return data. It can be rendered by Module Studio or another local UI, but it does not become an unguarded file editor.",
    }


def presentation_preview(index: ContentForgeIndex, pack: ContentPack) -> dict[str, Any]:
    presentation = pack.slices.get("presentation")
    if presentation is None:
        return {"canvas_count": 0, "canvases": [], "planned_new_presentations": [], "warnings": []}
    canvases: list[dict[str, Any]] = []
    warnings: list[str] = []
    targets = [screen["entrypoint"] for screen in presentation["screens"]]
    targets.extend(str(change["target"]) for change in presentation["changes"])
    for target in dict.fromkeys(targets):
        entry = index.features.by_entrypoint_id.get(target)
        if entry is None or entry.family != "presentation":
            warnings.append(f"Presentation preview target is not a known presentation entrypoint: {target}")
            continue
        key = entry.metadata.get("presentation_key")
        if not isinstance(key, str):
            warnings.append(f"Presentation preview target lacks a static layout key: {target}")
            continue
        try:
            canvas = presentation_layout.presentation_canvas(index.features.layouts, key)
        except presentation_layout.PresentationLayoutError as error:
            warnings.append(f"{target}: {error}")
        else:
            canvases.append({"entrypoint": target, "canvas": canvas})
    planned = [
        {
            "id": row["id"],
            "anchor": row["anchor"],
            "description": row.get("description", ""),
            "trigger_count": len(row.get("triggers", [])),
            "canvas_state": "planned_new_presentation_no_current_static_canvas",
        }
        for row in presentation["new_presentations"]
    ]
    return {"canvas_count": len(canvases), "canvases": canvases, "planned_new_presentations": planned, "warnings": warnings}


def content_pack_preview(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    plan, compilation = build_content_plan(index, pack, trace_limit=trace_limit)
    canvases = presentation_preview(index, pack)
    dialogue = pack.slices.get("dialogue")
    dialogue_beats = [] if dialogue is None else copy.deepcopy(dialogue["beats"])
    quest_event = pack.slices.get("quest_event")
    timeline = [] if quest_event is None else copy.deepcopy(quest_event["timeline"])
    balance = [
        {
            "change_id": change["change_id"],
            "record_id": change.get("record_id"),
            "entity_id": change.get("entity_id"),
            "rationale": change.get("rationale"),
            "state": change.get("state"),
            "plan": change.get("balance_plan"),
        }
        for change in plan.get("changes", [])
        if isinstance(change, Mapping) and change.get("backend") == "troop_item_balance"
    ]
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": plan["state"],
        "pack": pack_payload(pack),
        "narrative_preview": {"dialogue_beats": dialogue_beats, "quest_event_timeline": timeline},
        "campaign_ai_preview": plan.get("ai_intent_evidence"),
        "presentation_preview": canvases,
        "troop_item_preview": balance,
        "review_canvas": build_review_canvas(pack, compilation, plan),
        "plan": plan,
        "warnings": [
            *plan["warnings"],
            *canvases["warnings"],
            "Preview is deterministic static evidence, not an engine-rendered screenshot or a save-state simulation. Use the returned canvas to guide review before an intentional in-game test.",
        ],
    }


def content_pack_review(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    plan, compilation = build_content_plan(index, pack, trace_limit=trace_limit)
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": plan["state"],
        "pack": pack_payload(pack),
        "review_canvas": build_review_canvas(pack, compilation, plan),
        "plan_summary": {
            "plan_id": plan.get("plan_id"),
            "change_count": plan.get("change_count", 0),
            "source_apply": plan.get("source_apply"),
            "ai_intent_evidence": plan.get("ai_intent_evidence"),
            "errors": plan.get("errors", []),
        },
        "warnings": [
            *plan["warnings"],
            "The review canvas makes dependency/order relationships easy to inspect, but it remains secondary to the exact typed plan and SHA contract required for apply.",
        ],
    }


def content_pack_apply(
    index: ContentForgeIndex,
    *,
    change_id: str,
    expected_content_plan_id: str,
    expected_sha256: str,
    expected_balance_plan_sha256: str | None = None,
    pack_id: str | None = None,
    pack_value: Any | None = None,
    dry_run: bool = True,
    allow_legacy_compile_authoring: bool = False,
    allow_protected_legacy_record_change: bool = False,
) -> dict[str, Any]:
    if not isinstance(dry_run, bool):
        raise ContentForgeError("dry_run must be a boolean.")
    if not isinstance(allow_legacy_compile_authoring, bool) or not isinstance(allow_protected_legacy_record_change, bool):
        raise ContentForgeError("legacy acknowledgement flags must be booleans.")
    selected_id = require_string(change_id, name="change_id", maximum=160)
    checked_plan = require_string(expected_content_plan_id, name="expected_content_plan_id", maximum=160)
    try:
        checked_sha = change_router.require_sha256(expected_sha256)
    except change_router.ChangeRouterError as error:
        raise ContentForgeError(str(error)) from error
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    plan, compilation = build_content_plan(index, pack)
    if plan.get("state") != "ready_for_review":
        raise ContentForgeError("Content plan is not ready for apply; refresh content_pack_plan and repair its blocking evidence first.")
    if plan.get("plan_id") != checked_plan:
        raise ContentForgeError("expected_content_plan_id does not match the current deterministic content plan; refresh and review content_pack_plan.")
    selected = next((row for row in plan.get("changes", []) if row.get("change_id") == selected_id), None)
    if not isinstance(selected, Mapping):
        raise ContentForgeError("change_id is not part of the current content plan.")
    if selected.get("expected_sha256") != checked_sha:
        raise ContentForgeError("expected_sha256 must equal this selected change's current base SHA-256.")
    backend = selected.get("backend")
    if backend == "feature_authoring":
        feature_plan = plan.get("feature_plan")
        if not isinstance(feature_plan, Mapping) or not isinstance(compilation.feature_intent, Mapping):
            raise ContentForgeError("Selected source change has no current Feature Authoring plan.")
        try:
            result = feature_authoring.feature_apply(
                index.features,
                intent_value=compilation.feature_intent,
                change_id=str(selected["feature_change_id"]),
                expected_feature_plan_id=str(feature_plan["plan_id"]),
                expected_sha256=checked_sha,
                dry_run=dry_run,
            )
        except feature_authoring.FeatureAuthoringError as error:
            raise ContentForgeError(str(error)) from error
    elif backend == "troop_item_balance":
        if expected_balance_plan_sha256 is None:
            raise ContentForgeError("expected_balance_plan_sha256 is required when applying a troop/item Content Forge change.")
        try:
            checked_balance_plan = troop_item_balance.require_sha256(expected_balance_plan_sha256, name="expected_balance_plan_sha256")
        except troop_item_balance.BalanceError as error:
            raise ContentForgeError(str(error)) from error
        if selected.get("expected_balance_plan_sha256") != checked_balance_plan:
            raise ContentForgeError("expected_balance_plan_sha256 does not match this selected Balance Lab patch plan.")
        descriptor = next((item for item in compilation.balance_changes if item.content_change_id == selected_id), None)
        if descriptor is None:
            raise ContentForgeError("Selected balance change is no longer represented by this content pack.")
        try:
            balance_index = troop_item_balance.build_balance_index(index.root)
            result = troop_item_balance.balance_apply(
                balance_index,
                descriptor.entity_kind,
                descriptor.entity_id,
                changes=descriptor.changes,
                expected_sha256=checked_sha,
                expected_plan_sha256=checked_balance_plan,
                dry_run=dry_run,
                allow_legacy_compile_authoring=allow_legacy_compile_authoring,
                allow_protected_legacy_record_change=allow_protected_legacy_record_change,
            )
        except troop_item_balance.BalanceError as error:
            raise ContentForgeError(str(error)) from error
    else:
        raise ContentForgeError("Selected content change has an unsupported backend.")
    if not dry_run:
        invalidate_content_forge(index.root)
        troop_item_balance.invalidate_balance_index(index.root)
    return {
        "content_plan_id": checked_plan,
        "pack": pack_payload(pack),
        "change": copy.deepcopy(dict(selected)),
        "result": result,
        "follow_up": {
            "tool": "content_pack_verify",
            "pack_id": pack.id,
            "note": "After a non-dry apply, re-plan all remaining sibling changes, verify the pack, then intentionally run the normal reviewed build and inspect generated/ID/export diffs. Content Forge itself did not write those layers.",
        },
        "warnings": [
            *result.get("warnings", []),
            "Content Forge applied only the selected named specialist change when dry_run=false; it never writes generated modules, generated IDs, or exports.",
        ],
    }


def content_pack_verify(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    run_scenarios: bool = False,
    scenario_iterations: int = 8,
    scenario_seed: int = 1,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    if not all(isinstance(value, bool) for value in (run_tests, stage_build_check, run_scenarios)):
        raise ContentForgeError("run_tests, stage_build_check, and run_scenarios must be booleans.")
    iterations = require_limit(scenario_iterations, name="scenario_iterations", maximum=50)
    if isinstance(scenario_seed, bool) or not isinstance(scenario_seed, int):
        raise ContentForgeError("scenario_seed must be an integer.")
    timeout = require_limit(timeout_seconds, name="timeout_seconds", maximum=300, minimum=10)
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    compilation = compile_content_pack(index, pack)
    validation = content_pack_validate(index, pack_value=pack.raw)
    errors = list(validation["errors"])
    feature_result: dict[str, Any] | None = None
    if compilation.feature_intent is not None:
        try:
            feature_result = feature_authoring.feature_verify(
                index.features,
                intent_value=compilation.feature_intent,
                run_tests=run_tests,
                stage_build_check=stage_build_check,
                timeout_seconds=timeout,
            )
        except feature_authoring.FeatureAuthoringError as error:
            errors.append({"code": "feature_verify_failed", "message": str(error)})
        else:
            if feature_result.get("state") != "passed":
                errors.append({"code": "feature_verify_blocked", "message": "Specialist Feature Authoring verification did not pass."})
    ai = ai_contract_evidence(index, pack)
    errors.extend(ai["errors"])
    if ai["blocked_count"]:
        errors.append({"code": "ai_intent_not_proven", "message": "One or more Content Forge AI intent contracts are not proven against current source.", "blocked_contract_count": ai["blocked_count"]})
    balance_result: dict[str, Any] | None = None
    if compilation.balance_changes:
        try:
            balance_result = troop_item_balance.balance_verify(troop_item_balance.build_balance_index(index.root))
        except troop_item_balance.BalanceError as error:
            errors.append({"code": "balance_verify_failed", "message": str(error)})
        else:
            if balance_result.get("state") != "ready_for_build_review":
                errors.append({"code": "balance_verify_blocked", "message": "Balance Lab verification did not reach ready_for_build_review."})
    scenario_rows: list[dict[str, Any]] = []
    scenario_state = "not_requested"
    scenario_ids = declared_scenario_ids(pack)
    if scenario_ids:
        try:
            scenarios = campaign_scenario_fuzzer.build_scenario_fuzzer(index.root)
        except campaign_scenario_fuzzer.ScenarioFuzzerError as error:
            errors.append({"code": "scenario_fuzzer_unavailable", "message": str(error)})
        else:
            if run_scenarios:
                for offset, scenario_id in enumerate(scenario_ids):
                    try:
                        result = campaign_scenario_fuzzer.fuzz_payload(
                            scenarios,
                            scenario_id,
                            iterations=iterations,
                            seed=scenario_seed + offset * iterations,
                        )
                    except campaign_scenario_fuzzer.ScenarioFuzzerError as error:
                        errors.append({"code": "scenario_run_failed", "scenario_id": scenario_id, "message": str(error)})
                    else:
                        scenario_rows.append(result)
                statuses = {str(row.get("status")) for row in scenario_rows}
                if "failed" in statuses:
                    scenario_state = "blocked"
                    errors.append({"code": "scenario_counterexample", "message": "A declared scenario produced a modeled counterexample; inspect first_counterexample before editing further."})
                elif "inconclusive" in statuses:
                    scenario_state = "inconclusive"
                elif scenario_rows:
                    scenario_state = "passed"
            else:
                scenario_state = "declared_not_run"
                for scenario_id in scenario_ids:
                    try:
                        scenario_rows.extend(campaign_scenario_fuzzer.scenario_catalog_payload(scenarios, scenario_id=scenario_id)["scenarios"])
                    except campaign_scenario_fuzzer.ScenarioFuzzerError as error:
                        errors.append({"code": "unknown_scenario", "scenario_id": scenario_id, "message": str(error)})
    state = "blocked" if errors else "inconclusive" if scenario_state == "inconclusive" else "passed"
    return {
        "content_forge_version": f"devkit.content-forge.v{CONTENT_FORGE_VERSION}",
        "state": state,
        "pack": pack_payload(pack),
        "validation": validation,
        "feature_verification": feature_result,
        "ai_intent_evidence": ai,
        "balance_verification": balance_result,
        "scenarios": {
            "declared": list(scenario_ids),
            "run": run_scenarios,
            "iterations": iterations if run_scenarios else None,
            "seed": scenario_seed if run_scenarios else None,
            "state": scenario_state,
            "results": scenario_rows,
        },
        "errors": errors,
        "warnings": [
            *index.warnings,
            *ai["warnings"],
            "Verification proves declared static/specialist evidence and optional bounded scenario execution. It cannot emulate every save, engine callback timing, UI metric, or gameplay branch.",
            "No normal build or export is run by Content Forge verification. Run the established reviewed build only after source evidence is accepted.",
        ],
    }


def compact_plan_bases(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for change in plan.get("changes", []):
        if not isinstance(change, Mapping):
            continue
        rows.append(
            {
                "change_id": change.get("change_id"),
                "backend": change.get("backend"),
                "state": change.get("state"),
                "target": change.get("target") or change.get("entity_id"),
                "action": change.get("action"),
                "expected_sha256": change.get("expected_sha256"),
                "feature_change_id": change.get("feature_change_id"),
                "balance_plan_sha256": change.get("expected_balance_plan_sha256"),
            }
        )
    return rows


def content_pack_snapshot(
    index: ContentForgeIndex,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
) -> dict[str, Any]:
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    plan, compilation = build_content_plan(index, pack)
    feature_snapshot: dict[str, Any] | None = None
    if compilation.feature_intent is not None:
        try:
            feature_snapshot = feature_authoring.feature_semantic_snapshot(index.features, intent_value=compilation.feature_intent)
        except feature_authoring.FeatureAuthoringError as error:
            feature_snapshot = {"state": "unavailable", "error": str(error)}
    body = {
        "schema": CONTENT_SNAPSHOT_SCHEMA,
        "pack": pack_payload(pack),
        "pack_source_fingerprint": digest(pack.raw),
        "plan_state": plan.get("state"),
        "plan_bases": compact_plan_bases(plan),
        "feature_snapshot": feature_snapshot,
        "ai_intent_evidence": plan.get("ai_intent_evidence"),
    }
    return {
        **body,
        "snapshot_id": f"content-snapshot:{digest(body)}",
        "warnings": [
            *index.warnings,
            "This is an in-memory content semantic baseline. It writes no snapshot file and captures only declared pack/source/balance/AI evidence.",
        ],
    }


def indexed_rows(value: Any, key: str) -> dict[str, Mapping[str, Any]]:
    if not isinstance(value, list):
        return {}
    result: dict[str, Mapping[str, Any]] = {}
    for row in value:
        if isinstance(row, Mapping) and isinstance(row.get(key), str):
            result[str(row[key])] = row
    return result


def changed_entries(before: Any, after: Any, key: str) -> list[dict[str, Any]]:
    prior = indexed_rows(before, key)
    current = indexed_rows(after, key)
    rows: list[dict[str, Any]] = []
    for identifier in sorted(set(prior) | set(current), key=str.casefold):
        left = prior.get(identifier)
        right = current.get(identifier)
        if canonical_json(left) == canonical_json(right):
            continue
        rows.append({"id": identifier, "before": left, "after": right})
    return rows


def content_pack_semantic_diff(
    index: ContentForgeIndex,
    before: Any,
    *,
    pack_id: str | None = None,
    pack_value: Any | None = None,
) -> dict[str, Any]:
    baseline = require_object(before, name="before")
    if baseline.get("schema") != CONTENT_SNAPSHOT_SCHEMA:
        raise ContentForgeError("before must be a content_pack_snapshot payload.")
    pack = resolve_pack(index, pack_id=pack_id, pack_value=pack_value)
    prior_pack = require_object(baseline.get("pack"), name="before.pack")
    if prior_pack.get("id") != pack.id:
        raise ContentForgeError("before snapshot belongs to a different content pack.")
    current = content_pack_snapshot(index, pack_value=pack.raw)
    plan_changes = changed_entries(baseline.get("plan_bases"), current.get("plan_bases"), "change_id")
    prior_ai = baseline.get("ai_intent_evidence", {})
    current_ai = current.get("ai_intent_evidence", {})
    ai_changes = changed_entries(
        prior_ai.get("contracts") if isinstance(prior_ai, Mapping) else [],
        current_ai.get("contracts") if isinstance(current_ai, Mapping) else [],
        "id",
    )
    feature_before = baseline.get("feature_snapshot")
    feature_after = current.get("feature_snapshot")
    feature_changed = canonical_json(feature_before) != canonical_json(feature_after)
    pack_changed = baseline.get("pack_source_fingerprint") != current.get("pack_source_fingerprint")
    state = "changed" if plan_changes or ai_changes or feature_changed or pack_changed else "unchanged"
    return {
        "state": state,
        "before_snapshot_id": baseline.get("snapshot_id"),
        "after_snapshot_id": current.get("snapshot_id"),
        "pack_changed": pack_changed,
        "plan_changes": plan_changes,
        "ai_intent_changes": ai_changes,
        "feature_snapshot_changed": feature_changed,
        "current_snapshot": current,
        "warnings": [
            *index.warnings,
            "This diff reports changed pack contract, source/balance plan bases, and AI intent evidence. Use semantic_change_diff as well when a broad workspace/export comparison is required after a reviewed build.",
        ],
    }


def parse_json(value: str, *, name: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise ContentForgeError(f"{name} must contain valid JSON: {error}") from error


def parse_pack_file(root: Path, value: str, *, name: str) -> Any:
    raw = require_string(value, name=name, maximum=1_000)
    candidate = Path(raw)
    path = candidate if candidate.is_absolute() else root / candidate
    try:
        resolved = path.resolve()
        resolved.relative_to(TOOL_DIR.resolve())
    except ValueError as error:
        raise ContentForgeError(f"{name} must be a JSON file inside devkit/content_forge/.") from error
    if resolved.suffix.casefold() != ".json":
        raise ContentForgeError(f"{name} must name a .json file.")
    try:
        return parse_json(resolved.read_text(encoding="utf-8"), name=name)
    except OSError as error:
        raise ContentForgeError(f"Could not read {name}: {error}") from error


def cli_pack(index: ContentForgeIndex, args: argparse.Namespace) -> ContentPack:
    selected = [args.pack_id is not None, args.pack is not None, args.pack_file is not None]
    if sum(selected) != 1:
        raise ContentForgeError("Supply exactly one of --pack-id, --pack, or --pack-file.")
    if args.pack_id is not None:
        return require_pack(index, args.pack_id)
    value = parse_json(args.pack, name="--pack") if args.pack is not None else parse_pack_file(index.root, args.pack_file, name="--pack-file")
    return normalize_content_pack(value, name="pack")


def add_pack_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pack-id")
    group.add_argument("--pack")
    group.add_argument("--pack-file")


def write_stdout(payload: Mapping[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM-first typed Content Forge for ordered SoD Modern module-system content.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    summary = subparsers.add_parser("summary", help="Summarize checked-in Content Forge packs and slice coverage.")
    summary.add_argument("--limit", type=int, default=30)
    find = subparsers.add_parser("find", help="Find a content pack by brief, slice, entrypoint, or acceptance language.")
    find.add_argument("query")
    find.add_argument("--slice", default="all")
    find.add_argument("--limit", type=int, default=30)
    for command, help_text in (
        ("explain", "Explain a content pack, its typed source compilation, real entrypoints, and scenario declarations."),
        ("validate", "Validate a content pack and its typed slice contracts without planning or writing."),
        ("compile", "Compile a content pack into ordered specialist change descriptors without writing."),
        ("plan", "Produce exact independent source/balance diff plans, SHA guards, and AI evidence without writing."),
        ("preview", "Return narrative, campaign, balance, and presentation static preview data plus a review canvas."),
        ("review", "Return a deterministic human-readable review canvas backed by the exact content plan."),
        ("snapshot", "Capture an in-memory content semantic baseline JSON without writing an artifact."),
    ):
        command_parser = subparsers.add_parser(command, help=help_text)
        add_pack_arguments(command_parser)
        if command in {"explain", "plan", "preview", "review"}:
            command_parser.add_argument("--trace-limit", type=int, default=12)
    catalog_plan = subparsers.add_parser(
        "catalog-plan",
        help="Plan a strict create/replace of one checked-in Content Forge pack contract without writing.",
    )
    add_pack_arguments(catalog_plan)
    catalog_plan.add_argument("--mode", choices=sorted(VALID_CATALOG_MODES), required=True)
    catalog_apply = subparsers.add_parser(
        "catalog-apply",
        help="Rehearse or save one reviewed strict Content Forge catalog change; dry-run is the default.",
    )
    add_pack_arguments(catalog_apply)
    catalog_apply.add_argument("--mode", choices=sorted(VALID_CATALOG_MODES), required=True)
    catalog_apply.add_argument("--expected-catalog-plan-id", required=True)
    catalog_apply.add_argument("--expected-catalog-sha256", required=True)
    catalog_apply.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=True)
    catalog_apply.add_argument("--confirmation")
    apply = subparsers.add_parser("apply", help="Rehearse or apply one reviewed content change; dry-run is the default.")
    add_pack_arguments(apply)
    apply.add_argument("--change-id", required=True)
    apply.add_argument("--expected-content-plan-id", required=True)
    apply.add_argument("--expected-sha256", required=True)
    apply.add_argument("--expected-balance-plan-sha256")
    apply.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=True)
    apply.add_argument("--allow-legacy-compile-authoring", action=argparse.BooleanOptionalAction, default=False)
    apply.add_argument("--allow-protected-legacy-record-change", action=argparse.BooleanOptionalAction, default=False)
    verify = subparsers.add_parser("verify", help="Re-check content specialist evidence and optionally tests/staged checks/scenarios.")
    add_pack_arguments(verify)
    verify.add_argument("--run-tests", action=argparse.BooleanOptionalAction, default=False)
    verify.add_argument("--stage-build-check", action=argparse.BooleanOptionalAction, default=False)
    verify.add_argument("--run-scenarios", action=argparse.BooleanOptionalAction, default=False)
    verify.add_argument("--scenario-iterations", type=int, default=8)
    verify.add_argument("--scenario-seed", type=int, default=1)
    verify.add_argument("--timeout-seconds", type=int, default=90)
    difference = subparsers.add_parser("diff", help="Compare a prior in-memory content snapshot with current pack evidence.")
    add_pack_arguments(difference)
    before = difference.add_mutually_exclusive_group(required=True)
    before.add_argument("--before")
    before.add_argument("--before-file")
    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        index = build_content_forge(args.root.resolve())
        if command == "summary":
            payload = content_forge_summary(index, limit=args.limit)
        elif command == "find":
            payload = content_pack_find(index, args.query, slice_name=args.slice, limit=args.limit)
        else:
            pack = cli_pack(index, args)
            if command == "catalog-plan":
                payload = content_pack_catalog_plan(index, pack_value=pack.raw, mode=args.mode)
            elif command == "catalog-apply":
                payload = content_pack_catalog_apply(
                    index,
                    pack_value=pack.raw,
                    mode=args.mode,
                    expected_catalog_plan_id=args.expected_catalog_plan_id,
                    expected_catalog_sha256=args.expected_catalog_sha256,
                    dry_run=args.dry_run,
                    confirmation=args.confirmation,
                )
            elif command == "explain":
                payload = content_pack_explain(index, pack_value=pack.raw, trace_limit=args.trace_limit)
            elif command == "validate":
                payload = content_pack_validate(index, pack_value=pack.raw)
            elif command == "compile":
                payload = content_pack_compile(index, pack_value=pack.raw)
            elif command == "plan":
                payload = content_pack_plan(index, pack_value=pack.raw, trace_limit=args.trace_limit)
            elif command == "preview":
                payload = content_pack_preview(index, pack_value=pack.raw, trace_limit=args.trace_limit)
            elif command == "review":
                payload = content_pack_review(index, pack_value=pack.raw, trace_limit=args.trace_limit)
            elif command == "apply":
                payload = content_pack_apply(
                    index,
                    pack_value=pack.raw,
                    change_id=args.change_id,
                    expected_content_plan_id=args.expected_content_plan_id,
                    expected_sha256=args.expected_sha256,
                    expected_balance_plan_sha256=args.expected_balance_plan_sha256,
                    dry_run=args.dry_run,
                    allow_legacy_compile_authoring=args.allow_legacy_compile_authoring,
                    allow_protected_legacy_record_change=args.allow_protected_legacy_record_change,
                )
            elif command == "verify":
                payload = content_pack_verify(
                    index,
                    pack_value=pack.raw,
                    run_tests=args.run_tests,
                    stage_build_check=args.stage_build_check,
                    run_scenarios=args.run_scenarios,
                    scenario_iterations=args.scenario_iterations,
                    scenario_seed=args.scenario_seed,
                    timeout_seconds=args.timeout_seconds,
                )
            elif command == "snapshot":
                payload = content_pack_snapshot(index, pack_value=pack.raw)
            else:
                prior = parse_json(args.before, name="--before") if args.before is not None else parse_pack_file(index.root, args.before_file, name="--before-file")
                payload = content_pack_semantic_diff(index, prior, pack_value=pack.raw)
        write_stdout(payload)
    except (
        ContentForgeError,
        feature_authoring.FeatureAuthoringError,
        campaign_scenario_fuzzer.ScenarioFuzzerError,
        campaign_state_doctor.CampaignStateError,
        change_router.ChangeRouterError,
        presentation_layout.PresentationLayoutError,
        troop_item_balance.BalanceError,
    ) as error:
        print(f"content_forge: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
