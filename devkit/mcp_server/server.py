#!/usr/bin/env python3
"""MCP bridge for SoD Modern LLM-first diagnostics and guarded source editing.

The server exposes deterministic diagnostics plus named semantic and raw
hash-guarded source-edit operations instead of giving an agent a generic shell
or file-write surface. Every source edit delegates to the same Change Router
gate. All tool results share the checked-in
``devkit.tool-result.v1`` envelope and retain source provenance.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from collections import Counter
from functools import wraps
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from threading import RLock
from typing import Any, Callable, Sequence, TypeVar

from mcp.server import MCPServer
from mcp.types import ToolAnnotations


SERVER_VERSION = "1.9.0"
SERVER_DIR = Path(__file__).resolve().parent
DEVKIT_ROOT = SERVER_DIR.parent
REPO_ROOT = DEVKIT_ROOT.parent
MANIFEST_PATH = DEVKIT_ROOT / "manifest.json"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.dialogue_inspector import dialogue_inspector as dialogue  # noqa: E402
from devkit.dialogue_composer import dialogue_composer  # noqa: E402
from devkit.dialogue_model_checker import dialogue_model_checker  # noqa: E402
from devkit.campaign_state_doctor import campaign_state_doctor  # noqa: E402
from devkit.campaign_scenario_fuzzer import campaign_scenario_fuzzer  # noqa: E402
from devkit.change_router import change_router  # noqa: E402
from devkit.module_atlas import module_atlas  # noqa: E402
from devkit.module_blueprint import module_blueprint  # noqa: E402
from devkit.feature_authoring import feature_authoring  # noqa: E402
from devkit.content_forge import content_forge  # noqa: E402
from devkit.order_control import order_control  # noqa: E402
from devkit.presentation_layout import presentation_layout  # noqa: E402
from devkit.release_gate import release_gate  # noqa: E402
from devkit.rgl_log_sentinel import rgl_log_sentinel  # noqa: E402
from devkit.string_integrity import string_integrity  # noqa: E402
from devkit.string_provenance import string_provenance  # noqa: E402
from devkit.slot_lifecycle_lint import slot_lifecycle_lint  # noqa: E402
from devkit.semantic_change_diff import semantic_change_diff  # noqa: E402
from devkit.text_export_parity import text_export_parity  # noqa: E402
from devkit.text_execution_ledger import text_execution_ledger  # noqa: E402
from devkit.troop_item_balance import troop_item_balance  # noqa: E402
from devkit.workbench import workbench  # noqa: E402
from devkit.workspace_audit import workspace_audit  # noqa: E402


LOGGER = logging.getLogger(__name__)
READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)
WRITE_SOURCE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
)
WRITE_ARTIFACT = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)
T = TypeVar("T")

# MCP clients commonly ask several related questions against one unchanged
# workspace.  Rebuilding the same full source index for every tool call makes
# a normal discovery flow impractically slow on this large 1.011 module
# system.  Keep indexes in this server process only, and key them to a cheap
# metadata snapshot of every semantic input.  This is deliberately not a disk
# cache: source, compile, export, or DevKit contract changes are visible to a
# still-running server on its next request.
CACHE_INPUT_DIRECTORIES = ("src", "compile", "_export", "devkit", "build")
CACHE_IGNORED_DIRECTORIES = frozenset({".git", ".venv", "__pycache__", "output", "baselines"})
WorkspaceRevision = tuple[tuple[str, int, int], ...]
INDEX_CACHE: dict[tuple[str, str], tuple[WorkspaceRevision, Any]] = {}
INDEX_CACHE_LOCK = RLock()

SERVER_INSTRUCTIONS = (
    "SoD Modern LLM-first diagnostics and guarded source editing. For an unfamiliar workspace start with workspace_audit; "
    "otherwise start with devkit_health or devkit_catalog, "
    "then use bounded dialogue/string tools. For text in the wrong UI, menu, or dialogue location, "
    "run string_integrity, then text_export_parity when a processor/export mismatch is plausible, then text_explain for execution evidence before proposing a source edit. "
    "For silent campaign behavior problems, use campaign_state_summary, then campaign_state_findings and campaign_state_timeline; turn a confirmed invariant into a reviewed checked-in state contract rather than relying on an in-game surprise. "
    "For a gameplay RGL log, use rgl_log_analyze with the exact rgl_log path and the live module path when available; it clusters engine errors, maps them to source/generated/export evidence, and distinguishes a fixed source tree from a stale deployed export. Use rgl_log_contract before a build or release to verify protected engine callback party-handle guards. "
    "Use campaign_ai_intents for stationary/patrol/escort/raid-return/despawn contracts, slot_lifecycle_summary before reusing durable slots, and campaign_scenario_fuzz for safe bounded counterexample generation. "
    "For dialogue behavior rather than mere ordering, use dialogue_model_summary and dialogue_model_state; it proves only supported branch-free unreachable/shadowed/overlap paths. "
    "For string-register calls, use string_provenance_explain after text_explain to resolve actual nested writer branches. Capture semantic_change_snapshot before a source edit and semantic_change_diff after the reviewed build to see precedence/writer/sink/ID/trigger/export effects. "
    "For an unfamiliar module-system area, start with module_atlas_summary then module_find/module_context; use module_integrity before structural edits. "
    "Use dialogue_find/dialogue_context or presentation_find/presentation_canvas for their dedicated semantic editing, then inspect their patch plans before apply. "
    "For a new dialogue route, use dialogue_create_plan with its anchored JSON contract; apply only with its source SHA and exact plan ID. "
    "Use menu_flow, script_flow, mission_timeline, trigger_timeline, quest_registry, and entity_references for the remaining source areas. "
    "For order-sensitive work, start with order_summary, order_explain, and order_risk; use order_plan_move to review an anchored diff, then only use order_apply_move with its current SHA. "
    "Order Control protects manifest, generated-ID, and engine callback contracts but never writes compile/ or export files. "
    "For troop/item balancing, start with balance_summary then balance_item or balance_troop; use balance_compare, balance_upgrade_tree, and balance_outliers before proposing a change. Use balance_native_kingdoms before changing Native A/B/C templates or direct Native upgrades, and balance_mercenary_guilds before changing guild role fit, contract formation, or mercenary roster composition. "
    "Balance edits are a narrow legacy compile-authoring compatibility gate: they produce a SHA-guarded record diff, dry-run by default, never alter IDs/order/exports, and require an explicit legacy-authoring acknowledgement for non-dry apply. "
    "For a strict release-candidate preflight after a reviewed build, use release_gate; it stages source assembly and all legacy exports without writing the live workspace, requires exact approved intentional blank sinks, and blocks on compiler, dialogue, order, export-parity, or protected engine-callback regressions. "
    "For a coherent feature that spans source fragments, order, durable slots, AI, and focused tests, start with blueprint_summary and blueprint_explain; use blueprint_compile only for its dependency-first no-write impact plan, then make any separately reviewed change through the existing SHA-guarded source editor. "
    "For a new or evolving module-system feature, use feature_summary/feature_explain and entrypoint_find/entrypoint_explain to map actual engine entrypoints first; submit only typed JSON Feature Intent operations to feature_plan, review each exact source diff, then use feature_apply for one SHA-guarded source target at a time and feature_verify afterward. "
    "For authored content spanning dialogue, quest/event, campaign AI, troop/item balancing, and presentations, use content_forge_summary then content_pack_explain; Content Packs bind brief/lore/tone/acceptance criteria to typed specialist slices. Use content_pack_catalog_plan/content_pack_catalog_apply only to persist one reviewed strict pack contract to devkit/content_forge/packs.json; use content_pack_plan and content_pack_review before content_pack_apply, which remains one named SHA-guarded specialist change at a time. "
    "For CBO-style fixed impact, validation, contract, coverage, scenario, and release evidence workflows, use the workbench_* tools. "
    "Use change_impact and patch_plan before raw apply_source_edits. Apply is source-only, SHA-guarded, and dry-run by default. Results include compiled order and "
    "source/export provenance. Never infer a dialogue branch without inspecting "
    "compiled order; NPC dialogue uses the first matching route."
)

mcp = MCPServer(
    "sod-modern-devkit",
    title="SoD Modern DevKit",
    description="LLM-first diagnostics and guarded source editing for SoD Modern module-system content.",
    instructions=SERVER_INSTRUCTIONS,
    version=SERVER_VERSION,
)


def mcp_version() -> str:
    try:
        return version("mcp")
    except PackageNotFoundError:
        return "unavailable"


def require_int(name: str, value: int, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer from {minimum} through {maximum}.")
    return value


def require_query(query: str) -> str:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must not be empty.")
    if len(query) > 500:
        raise ValueError("query must be at most 500 characters.")
    return query


def inventory_warnings(inventory: dialogue.DialogueInventory | None) -> list[str]:
    if inventory is None or not inventory.source_is_newer:
        return []
    newest = inventory.newest_source
    label = dialogue.project_relative(newest, REPO_ROOT) if newest else "unknown"
    return [
        f"Generated dialogue may be stale; {label} is newer than compile/module_dialogs.py.",
        "Run py -3 build\\build_dialogs.py before trusting compiled-order results.",
    ]


def provenance(
    inventory: dialogue.DialogueInventory | None = None,
    *,
    read_only: bool = True,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "repo_root": str(REPO_ROOT),
        "read_only": read_only,
        "server_version": SERVER_VERSION,
        "mcp_sdk_version": mcp_version(),
        "compiled_dialogue": None,
        "source_is_newer": None,
    }
    if inventory is not None:
        result["compiled_dialogue"] = dialogue.project_relative(inventory.compiled_path, REPO_ROOT)
        result["source_is_newer"] = inventory.source_is_newer
    return result


def success(
    tool: str,
    data: dict[str, Any],
    inventory: dialogue.DialogueInventory | None = None,
    extra_warnings: Sequence[str] = (),
    read_only: bool = True,
) -> dict[str, Any]:
    return {
        "contract_version": "devkit.tool-result.v1",
        "tool": tool,
        "ok": True,
        "data": data,
        "provenance": provenance(inventory, read_only=read_only),
        "warnings": list(dict.fromkeys([*inventory_warnings(inventory), *extra_warnings])),
    }


def failure(tool: str, message: str, *, read_only: bool = True) -> dict[str, Any]:
    return {
        "contract_version": "devkit.tool-result.v1",
        "tool": tool,
        "ok": False,
        "data": {"error": message},
        "provenance": provenance(read_only=read_only),
        "warnings": [],
    }


def guarded(
    tool: str,
    action: Callable[[], dict[str, Any]],
    *,
    read_only: bool = True,
) -> dict[str, Any]:
    try:
        return action()
    except (
        dialogue.InspectorError,
        dialogue_composer.DialogueComposerError,
        dialogue_model_checker.DialogueModelError,
        campaign_state_doctor.CampaignStateError,
        campaign_scenario_fuzzer.ScenarioFuzzerError,
        change_router.ChangeRouterError,
        module_atlas.ModuleAtlasError,
        module_blueprint.ModuleBlueprintError,
        feature_authoring.FeatureAuthoringError,
        content_forge.ContentForgeError,
        order_control.OrderControlError,
        presentation_layout.PresentationLayoutError,
        rgl_log_sentinel.RglLogSentinelError,
        string_integrity.StringIntegrityError,
        string_provenance.StringProvenanceError,
        slot_lifecycle_lint.SlotLifecycleError,
        semantic_change_diff.SemanticDiffError,
        text_export_parity.TextExportParityError,
        release_gate.ReleaseGateError,
        text_execution_ledger.LedgerError,
        troop_item_balance.BalanceError,
        workbench.WorkbenchError,
        workspace_audit.AuditError,
        ValueError,
    ) as error:
        # Invalid tool arguments are an expected part of agent exploration.
        # Keep the structured failure visible to the caller without treating it
        # as an operator warning on the stdio server's stderr stream.
        LOGGER.debug("%s rejected: %s", tool, error)
        return failure(tool, str(error), read_only=read_only)


def load_manifest() -> dict[str, Any]:
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not read DevKit manifest: {error}") from error


def workspace_revision(root: Path) -> WorkspaceRevision:
    """Return a bounded metadata revision for files that can affect an index."""

    resolved_root = root.resolve()
    records: list[tuple[str, int, int]] = []
    # Some legacy diagnostics inspect root-level build entry points such as
    # build_module.bat, so include regular root files as semantic inputs too.
    try:
        root_files = tuple(resolved_root.iterdir())
    except OSError:
        root_files = ()
    for path in root_files:
        if not path.is_file():
            continue
        try:
            status = path.stat()
        except OSError:
            continue
        records.append(
            (
                path.relative_to(resolved_root).as_posix(),
                status.st_mtime_ns,
                status.st_size,
            )
        )
    for directory_name in CACHE_INPUT_DIRECTORIES:
        directory = resolved_root / directory_name
        if not directory.is_dir():
            continue
        for current, child_directories, filenames in os.walk(directory):
            child_directories[:] = [
                name for name in child_directories if name not in CACHE_IGNORED_DIRECTORIES
            ]
            current_path = Path(current)
            for filename in filenames:
                path = current_path / filename
                try:
                    status = path.stat()
                except OSError:
                    # A concurrent external edit can briefly remove a file.
                    # The next request will take a new revision and rebuild.
                    continue
                records.append(
                    (
                        path.relative_to(resolved_root).as_posix(),
                        status.st_mtime_ns,
                        status.st_size,
                    )
                )
    return tuple(sorted(records))


def cached_workspace_index(
    cache_name: str,
    root: Path,
    builder: Callable[[Path], T],
) -> T:
    """Build once per stable workspace revision without persisting derived data."""

    resolved_root = root.resolve()
    cache_key = (cache_name, str(resolved_root).casefold())
    with INDEX_CACHE_LOCK:
        before = workspace_revision(resolved_root)
        cached = INDEX_CACHE.get(cache_key)
        if cached is not None and cached[0] == before:
            return cached[1]

        result = builder(resolved_root)
        after = workspace_revision(resolved_root)
        # Never associate an index built during a concurrent edit with the
        # post-edit revision.  The current caller receives the same best-effort
        # result it would have without a cache, while the next request rebuilds.
        if before == after:
            INDEX_CACHE[cache_key] = (after, result)
        return result


def cache_root_builder(cache_name: str, builder: Callable[..., T]) -> Callable[..., T]:
    """Cache only the server's real workspace; temporary test roots stay isolated."""

    @wraps(builder)
    def cached(root: Path = REPO_ROOT, *args: Any, **kwargs: Any) -> T:
        resolved_root = Path(root).resolve()
        if resolved_root != REPO_ROOT.resolve() or args or kwargs:
            return builder(root, *args, **kwargs)
        return cached_workspace_index(cache_name, resolved_root, builder)

    return cached


def install_workspace_index_cache() -> None:
    """Apply the revision-aware cache to expensive server-side index builders."""

    builders = (
        ("dialogue_inventory", dialogue, "load_inventory"),
        ("dialogue_composer", dialogue_composer, "build_dialogue_composer"),
        ("dialogue_model", dialogue_model_checker, "build_dialogue_model"),
        ("campaign_state", campaign_state_doctor, "build_state_doctor"),
        ("campaign_scenarios", campaign_scenario_fuzzer, "build_scenario_fuzzer"),
        ("change_router", change_router, "build_change_router"),
        ("module_atlas", module_atlas, "build_module_atlas"),
        ("module_blueprint", module_blueprint, "build_module_blueprints"),
        ("feature_authoring", feature_authoring, "build_feature_authoring"),
        ("content_forge", content_forge, "build_content_forge"),
        ("order_control", order_control, "build_order_control"),
        ("presentation_layout", presentation_layout, "build_presentation_layout"),
        ("semantic_snapshot", semantic_change_diff, "build_snapshot"),
        ("slot_lifecycle", slot_lifecycle_lint, "build_slot_lifecycle_lint"),
        ("string_integrity", string_integrity, "build_integrity_report"),
        ("string_provenance", string_provenance, "build_string_provenance"),
        ("text_ledger", text_execution_ledger, "build_ledger"),
        ("troop_item_balance", troop_item_balance, "build_balance_index"),
    )
    for cache_name, module, attribute in builders:
        original = getattr(module, attribute)
        setattr(module, attribute, cache_root_builder(cache_name, original))


install_workspace_index_cache()


def load_inventory() -> dialogue.DialogueInventory:
    return dialogue.load_inventory(REPO_ROOT)


def clipped_summary(payload: dict[str, Any], maximum: int) -> dict[str, Any]:
    """Keep agent responses bounded without hiding the total evidence count."""
    result = dict(payload)
    for key in (
        "top_states",
        "exact_fallback_shadow_candidates",
        "target_only_states_to_review",
        "unsupported_direct_string_placeholders",
    ):
        values = list(result.get(key, []))
        result[key] = values[:maximum]
        result[f"{key}_total"] = len(values)
        result[f"{key}_truncated"] = len(values) > maximum
    return result


def graph_edges(entries: Sequence[dialogue.DialogueEntry]) -> list[dict[str, Any]]:
    counts = Counter((entry.start_state, entry.end_state) for entry in entries)
    return [
        {"from_state": source, "to_state": target, "route_count": count}
        for (source, target), count in sorted(counts.items())
    ]


@mcp.tool(
    name="devkit_catalog",
    description="Discover the LLM-first DevKit interfaces, safety rules, and available MCP tools.",
    annotations=READ_ONLY,
    structured_output=True,
)
def devkit_catalog() -> dict[str, Any]:
    return guarded(
        "devkit_catalog",
        lambda: success(
            "devkit_catalog",
            {
                "manifest": load_manifest(),
                "server_instructions": SERVER_INSTRUCTIONS,
                "activation": (
                    "This server is diagnostic-first. dialogue_apply, presentation_apply, module_apply, and apply_source_edits "
                    "all use the same source-only, SHA-guarded, dry-run-by-default Change Router gate; content_pack_catalog_apply separately persists only one reviewed strict devkit/content_forge/packs.json contract with its own SHA/confirmation gate; content_pack_apply delegates one named change to those same specialist gates; balance_apply is a separate, narrower SHA-gated legacy compile-authoring compatibility path for direct troop/item records only; Workbench tools provide fixed evidence workflows and disabled DevKit drafts. "
                    "Configure it in a local Codex client to make its tools callable there."
                ),
            },
        ),
    )


@mcp.tool(
    name="devkit_health",
    description="Check DevKit runtime, dialogue freshness, and generated export-layer availability before diagnosis.",
    annotations=READ_ONLY,
    structured_output=True,
)
def devkit_health() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        inventory = load_inventory()
        exports = {
            filename: (REPO_ROOT / "_export" / filename).exists()
            for filename in ("strings.txt", "quick_strings.txt", "conversation.txt", "dialog_states.txt")
        }
        return success(
            "devkit_health",
            {
                "dialogue_entry_count": len(inventory.entries),
                "dialogue_state_count": len({entry.start_state for entry in inventory.entries}),
                "source_marker_count": sum(entry.source is not None for entry in inventory.entries),
                "exports": exports,
                "mcp_sdk_version": mcp_version(),
            },
            inventory,
        )

    return guarded("devkit_health", action)


@mcp.tool(
    name="dialogue_summary",
    description="Summarize compiled dialogue states, exact fallback-shadow candidates, target-only states, and unsupported string placeholders.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_summary(max_findings: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("max_findings", max_findings, 1, 200)
        inventory = load_inventory()
        return success(
            "dialogue_summary",
            clipped_summary(dialogue.summary_payload(inventory), maximum),
            inventory,
        )

    return guarded("dialogue_summary", action)


@mcp.tool(
    name="dialogue_routes",
    description="Return dialogue candidates in the exact generated order, with optional state/text/source filters and bounded evidence.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_routes(
    start_state: str | None = None,
    contains: str | None = None,
    source: str | None = None,
    limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        inventory = load_inventory()
        if contains is not None:
            require_query(contains)
        selected = dialogue.filter_entries(
            inventory.entries,
            [start_state] if start_state else [],
            contains,
            source,
        )
        return success(
            "dialogue_routes",
            {
                "match_count": len(selected),
                "returned_count": min(len(selected), maximum),
                "truncated": len(selected) > maximum,
                "entries": [dialogue.entry_dict(entry) for entry in selected[:maximum]],
            },
            inventory,
        )

    return guarded("dialogue_routes", action)


@mcp.tool(
    name="dialogue_entry",
    description="Retrieve one exact compiled dialogue route by its stable one-based index from dialogue_routes or dialogue_summary evidence.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_entry(entry_index: int) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        inventory = load_inventory()
        require_int("entry_index", entry_index, 1, len(inventory.entries))
        entry = inventory.entries[entry_index - 1]
        return success("dialogue_entry", {"entry": dialogue.entry_dict(entry)}, inventory)

    return guarded("dialogue_entry", action)


@mcp.tool(
    name="dialogue_model_summary",
    description=(
        "Build a proof-oriented compiled-dialogue model: proved branch-free unreachable routes, NPC first-match "
        "shadows, conditional overlaps, player-choice ambiguities, terminally dead states, and model boundaries."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_model_summary(limit: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        index = dialogue_model_checker.build_dialogue_model(REPO_ROOT)
        payload = dialogue_model_checker.summary_payload(index, limit=maximum)
        return success("dialogue_model_summary", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_model_summary", action)


@mcp.tool(
    name="dialogue_model_findings",
    description="Filter only proved dialogue reachability/shadow/ambiguity findings, with source-mapped constraint evidence.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_model_findings(severity: str = "all", query: str | None = None, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_query = require_query(query) if query is not None else None
        index = dialogue_model_checker.build_dialogue_model(REPO_ROOT)
        payload = dialogue_model_checker.findings_payload(index, severity=severity, query=checked_query, limit=maximum)
        return success("dialogue_model_findings", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_model_findings", action)


@mcp.tool(
    name="dialogue_model_state",
    description="Inspect one dialogue state in exact compiled order with first-match/player-choice mode and each route's proof status.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_model_state(state: str, limit: int = 80) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        index = dialogue_model_checker.build_dialogue_model(REPO_ROOT)
        payload = dialogue_model_checker.state_payload(index, require_query(state), limit=maximum)
        return success("dialogue_model_state", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_model_state", action)


@mcp.tool(
    name="dialogue_model_route",
    description="Explain one compiled dialogue route's normalized constraints, prior routes, proof status, and related reachability findings.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_model_route(route_index: int) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = dialogue_model_checker.build_dialogue_model(REPO_ROOT)
        checked = require_int("route_index", route_index, 1, len(index.routes))
        payload = dialogue_model_checker.route_payload_by_index(index, checked)
        return success("dialogue_model_route", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_model_route", action)


@mcp.tool(
    name="dialogue_composer_summary",
    description=(
        "Summarize the modular semantic Dialogue Composer: authored route count, source ownership, "
        "compiled-order mapping coverage, and first-match safety rules."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_composer_summary() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_summary(index)
        return success("dialogue_composer_summary", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_composer_summary", action)


@mcp.tool(
    name="dialogue_find",
    description=(
        "Find authored modular dialogue routes by text/state/source and return stable route IDs, exact source ownership, "
        "condition/consequence operations, and compiled-order evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_find(
    query: str | None = None,
    input_state: str | None = None,
    output_state: str | None = None,
    source: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_find(
            index,
            query=query,
            input_state=input_state,
            output_state=output_state,
            source=source,
            limit=limit,
        )
        return success("dialogue_find", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_find", action)


@mcp.tool(
    name="dialogue_context",
    description=(
        "Return one authored dialogue route's first-match/shadow analysis plus linked source, generated, execution, and test context."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_context(
    route_id: str,
    max_lines: int = 100,
    related_limit: int = 20,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_context(
            index,
            route_id,
            max_lines=max_lines,
            related_limit=related_limit,
        )
        return success("dialogue_context", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_context", action)


@mcp.tool(
    name="dialogue_create_plan",
    description=(
        "Plan one deterministic new M&B 1.011 dialogue route from an anchored JSON contract. "
        "Canonicalizes the route, rejects duplicate signatures, and blocks unacknowledged static NPC first-match hazards; never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_create_plan(
    spec: dict[str, Any],
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_create_plan(
            index,
            spec,
            expected_sha256=expected_sha256,
        )
        return success("dialogue_create_plan", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_create_plan", action)


@mcp.tool(
    name="dialogue_create_apply",
    description=(
        "Rehearse or apply exactly one reviewed deterministic dialogue creation plan through the source-only Change Router gate. "
        "Requires the plan's source SHA and exact plan ID; dry_run is true by default."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def dialogue_create_apply(
    spec: dict[str, Any],
    expected_sha256: str,
    expected_plan_id: str,
    dry_run: bool = True,
) -> dict[str, Any]:
    def call() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_create_apply(
            index,
            spec,
            expected_sha256=expected_sha256,
            expected_plan_id=expected_plan_id,
            dry_run=dry_run,
        )
        return success(
            "dialogue_create_apply",
            payload,
            extra_warnings=payload["warnings"],
            read_only=dry_run,
        )

    return guarded("dialogue_create_apply", call, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="dialogue_patch",
    description=(
        "Create a source-only semantic dialogue patch plan for text, states, conditions, consequences, menu bridges, "
        "or route add/remove/reorder actions. Returns an exact unified diff and required SHA-256; never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_patch(
    route_id: str,
    action: str,
    value: str | None = None,
    operation: str | None = None,
    position: str = "end",
    operation_index: int | None = None,
    new_route: dict[str, Any] | None = None,
    anchor_route_id: str | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    def call() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_patch(
            index,
            route_id,
            action=action,
            value=value,
            operation=operation,
            position=position,
            operation_index=operation_index,
            new_route=new_route,
            anchor_route_id=anchor_route_id,
            expected_sha256=expected_sha256,
        )
        return success("dialogue_patch", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_patch", call)


@mcp.tool(
    name="dialogue_apply",
    description=(
        "Apply a semantic dialogue action through the Change Router's SHA-guarded source-only edit gate. "
        "dry_run is true by default; generated modules and exports are never written."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def dialogue_apply(
    route_id: str,
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
    def call() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_apply(
            index,
            route_id,
            action=action,
            expected_sha256=expected_sha256,
            dry_run=dry_run,
            value=value,
            operation=operation,
            position=position,
            operation_index=operation_index,
            new_route=new_route,
            anchor_route_id=anchor_route_id,
        )
        return success(
            "dialogue_apply",
            payload,
            extra_warnings=payload["warnings"],
            read_only=dry_run,
        )

    return guarded("dialogue_apply", call, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="dialogue_verify",
    description=(
        "Verify one dialogue source fragment after semantic authoring: syntax, order, generated freshness, static tests, "
        "optional isolated build, and static first-match hazards."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_verify(
    route_id: str,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = dialogue_composer.build_dialogue_composer(REPO_ROOT)
        payload = dialogue_composer.dialogue_verify(
            index,
            route_id,
            expected_sha256=expected_sha256,
            run_tests=run_tests,
            stage_build_check=stage_build,
            max_tests=max_tests,
            timeout_seconds=timeout_seconds,
        )
        return success("dialogue_verify", payload, extra_warnings=payload["warnings"])

    return guarded("dialogue_verify", action)


@mcp.tool(
    name="string_trace",
    description="Trace text, string IDs, or registers through modular source, generated modules, and string/conversation exports.",
    annotations=READ_ONLY,
    structured_output=True,
)
def string_trace(
    query: str,
    regex: bool = False,
    case_sensitive: bool = False,
    limit_per_layer: int = 25,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_query = require_query(query)
        maximum = require_int("limit_per_layer", limit_per_layer, 1, 200)
        hits, unavailable, truncated = dialogue.search_text(
            REPO_ROOT,
            checked_query,
            regex,
            case_sensitive,
            maximum,
        )
        return success(
            "string_trace",
            {
                "query": checked_query,
                "regex": regex,
                "case_sensitive": case_sensitive,
                "hit_count": len(hits),
                "hits": [
                    {
                        "layer": hit.layer,
                        "path": hit.path,
                        "line": hit.line,
                        "text": hit.text,
                        "normalized_export_match": hit.normalized_export_match,
                    }
                    for hit in hits
                ],
                "unavailable_layers": unavailable,
                "truncated_layers": list(dict.fromkeys(truncated)),
            },
        )

    return guarded("string_trace", action)


@mcp.tool(
    name="string_integrity",
    description=(
        "Statically preflight dialogue, menu, presentation, and message text sinks; "
        "trace s-register writers, dynamic selector boundaries, script clobber risks, and source provenance."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def string_integrity_tool(
    query: str | None = None,
    register: int | None = None,
    kind: str = "all",
    include_clean: bool = False,
    limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_query = require_query(query) if query is not None else None
        checked_register = (
            require_int("register", register, 0, 999) if register is not None else None
        )
        report = string_integrity.build_integrity_report(REPO_ROOT)
        payload = string_integrity.query_sinks(
            report,
            query=checked_query,
            register=checked_register,
            kind=kind,
            include_clean=include_clean,
            limit=maximum,
        )
        return success(
            "string_integrity",
            payload,
            extra_warnings=payload["warnings"],
        )

    return guarded("string_integrity", action)


@mcp.tool(
    name="text_export_parity",
    description=(
        "Replay the fixed M&B 1.011 legacy processor order in a temporary isolated workspace and compare "
        "its text-bearing exports with live _export files. source_build=true also stages modular source assembly; "
        "the real compile/ and _export/ paths are never written."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def text_export_parity_tool(
    source_build: bool = False,
    scope: str = "text",
    max_diffs: int = 20,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("max_diffs", max_diffs, 1, 200)
        timeout = require_int("timeout_seconds", timeout_seconds, 10, 300)
        if not isinstance(source_build, bool):
            raise ValueError("source_build must be true or false.")
        payload = text_export_parity.build_export_parity_report(
            REPO_ROOT,
            source_build=source_build,
            scope=scope,
            max_diffs=maximum,
            timeout_seconds=timeout,
        )
        return success("text_export_parity", payload, extra_warnings=payload["warnings"])

    return guarded("text_export_parity", action)


@mcp.tool(
    name="rgl_log_analyze",
    description=(
        "Read one Mount & Blade RGL gameplay log, cluster related engine errors, map named scripts to source/generated/export evidence, "
        "classify non-script warnings, and optionally prove whether an explicit live Module directory is stale versus workspace _export. "
        "Read-only: it never touches saves, live module files, source, compile, or exports."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def rgl_log_analyze_tool(
    log_path: str,
    live_module_path: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_log = Path(require_query(log_path))
        checked_live = Path(require_query(live_module_path)) if live_module_path is not None else None
        payload = rgl_log_sentinel.analyze_log(
            REPO_ROOT,
            log_path=checked_log,
            live_module=checked_live,
            limit=maximum,
        )
        return success("rgl_log_analyze", payload, extra_warnings=payload["tool_warnings"])

    return guarded("rgl_log_analyze", action)


@mcp.tool(
    name="rgl_log_contract",
    description=(
        "Check protected native engine callback contracts for dynamic party handles before a build or release. "
        "Currently protects game_event_simulate_battle from stale-party reads; read-only."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def rgl_log_contract_tool(limit: int = 50) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        payload = rgl_log_sentinel.engine_callback_contract_report(REPO_ROOT, limit=maximum)
        return success("rgl_log_contract", payload, extra_warnings=payload["warnings"])

    return guarded("rgl_log_contract", action)


@mcp.tool(
    name="release_gate",
    description=(
        "Run the strict, read-only release-candidate preflight: isolated source-to-generated-to-all-export parity, "
        "staged compiler diagnostics, exact approved intentional blank sinks, dialogue-model errors, order/ID contracts, and protected engine callback party-handle contracts. "
        "The tool never writes live compile or export files; data.state is passed or blocked."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def release_gate_tool(timeout_seconds: int = 120, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        timeout = require_int("timeout_seconds", timeout_seconds, 10, 300)
        maximum = require_int("limit", limit, 1, 200)
        payload = release_gate.run_release_gate(
            REPO_ROOT,
            timeout_seconds=timeout,
            limit=maximum,
        )
        return success("release_gate", payload, extra_warnings=payload["warnings"])

    return guarded("release_gate", action)


@mcp.tool(
    name="blueprint_summary",
    description=(
        "Summarize checked-in feature Blueprints and their current source/symbol/order/slot/AI/test contract state. "
        "This is a read-only compiler front-end; it never generates or edits legacy module source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def blueprint_summary_tool(limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        payload = module_blueprint.blueprint_summary(
            module_blueprint.build_module_blueprints(REPO_ROOT),
            limit=maximum,
        )
        return success("blueprint_summary", payload, extra_warnings=payload["warnings"])

    return guarded("blueprint_summary", action)


@mcp.tool(
    name="blueprint_find",
    description=(
        "Find a feature Blueprint by stable ID, description, source fragment, required symbol, external contract, or focused test. "
        "Use blueprint_explain for exact evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def blueprint_find_tool(query: str, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        payload = module_blueprint.blueprint_find(
            module_blueprint.build_module_blueprints(REPO_ROOT),
            require_query(query),
            limit=maximum,
        )
        return success("blueprint_find", payload, extra_warnings=payload["warnings"])

    return guarded("blueprint_find", action)


@mcp.tool(
    name="blueprint_explain",
    description=(
        "Explain one stable feature Blueprint through exact authoritative source fragments, required Atlas entities, literal anchors, "
        "order constraints, slot ownership, AI intent contracts, and focused test declarations."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def blueprint_explain_tool(blueprint_id: str) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = module_blueprint.blueprint_explain(
            module_blueprint.build_module_blueprints(REPO_ROOT),
            blueprint_id,
        )
        return success("blueprint_explain", payload, extra_warnings=payload["warnings"])

    return guarded("blueprint_explain", action)


@mcp.tool(
    name="blueprint_compile",
    description=(
        "Produce a deterministic dependency-first feature impact plan: authoritative source fragments, affected generated/export layers, "
        "checked contracts, and focused tests. It is intentionally no-write and has no source apply path."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def blueprint_compile_tool(blueprint_id: str, limit: int = 80) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        payload = module_blueprint.blueprint_compile(
            module_blueprint.build_module_blueprints(REPO_ROOT),
            blueprint_id,
            limit=maximum,
        )
        return success("blueprint_compile", payload, extra_warnings=payload["warnings"])

    return guarded("blueprint_compile", action)


@mcp.tool(
    name="blueprint_verify",
    description=(
        "Re-evaluate one feature Blueprint or the active catalog after a reviewed source change. "
        "It blocks on missing/ambiguous symbols, broken anchors/order contracts, blocking slot/AI contracts, or missing focused tests."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def blueprint_verify_tool(blueprint_id: str | None = None, limit: int = 80) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        payload = module_blueprint.blueprint_verify(
            module_blueprint.build_module_blueprints(REPO_ROOT),
            blueprint_id,
            limit=maximum,
        )
        return success("blueprint_verify", payload, extra_warnings=payload["warnings"])

    return guarded("blueprint_verify", action)


@mcp.tool(
    name="feature_summary",
    description=(
        "Summarize checked-in Feature Intents and the real engine-entrypoint registry spanning callbacks, scripts, triggers, menus, dialogue, presentations, missions, quests, and constants."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_summary_tool(limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_summary(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            limit=require_int("limit", limit, 1, 200),
        )
        return success("feature_summary", payload, extra_warnings=payload["warnings"])

    return guarded("feature_summary", action)


@mcp.tool(
    name="feature_find",
    description="Find a checked-in Feature Intent by its ID, title, description, Blueprint, engine entrypoint, or focused test.",
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_find_tool(query: str, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_find(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            require_query(query),
            limit=require_int("limit", limit, 1, 200),
        )
        return success("feature_find", payload, extra_warnings=payload["warnings"])

    return guarded("feature_find", action)


@mcp.tool(
    name="entrypoint_find",
    description=(
        "Find real source-derived M&B 1.011 engine entrypoints by family, name, symbol, or source path. "
        "Use entrypoint_explain before authoring a feature change."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def entrypoint_find_tool(query: str | None = None, family: str = "all", limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.entrypoint_find(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            require_query(query) if query is not None else None,
            family=family,
            limit=require_int("limit", limit, 1, 200),
        )
        return success("entrypoint_find", payload, extra_warnings=payload["warnings"])

    return guarded("entrypoint_find", action)


@mcp.tool(
    name="entrypoint_explain",
    description=(
        "Explain one engine entrypoint with bounded static execution evidence: caller/callee graph, menu flow, trigger schedule, dialogue precedence, presentation canvas, mission callbacks, references, source order, and generated IDs where applicable."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def entrypoint_explain_tool(entrypoint_id: str, limit: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.entrypoint_explain(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            entrypoint_id,
            limit=require_int("limit", limit, 1, 100),
        )
        return success("entrypoint_explain", payload, extra_warnings=payload["warnings"])

    return guarded("entrypoint_explain", action)


@mcp.tool(
    name="feature_explain",
    description=(
        "Explain a checked-in or inline Feature Intent through its engine entrypoints, Module Blueprint, typed-change validation, and bounded static traces; never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_explain_tool(
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
    trace_limit: int = 20,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_explain(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            feature_id=feature_id,
            intent_value=intent,
            trace_limit=require_int("trace_limit", trace_limit, 1, 30),
        )
        return success("feature_explain", payload, extra_warnings=payload["warnings"])

    return guarded("feature_explain", action)


@mcp.tool(
    name="feature_intent_validate",
    description=(
        "Validate a checked-in or inline Feature Intent and all typed source-change shapes before producing any patch plan. "
        "Rejects raw Python/tuple escapes, unknown engine entrypoints, missing Blueprints, and missing focused tests."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_intent_validate_tool(
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_intent_validate(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            feature_id=feature_id,
            intent_value=intent,
        )
        return success("feature_intent_validate", payload, extra_warnings=payload["warnings"])

    return guarded("feature_intent_validate", action)


@mcp.tool(
    name="feature_ir_render",
    description="Render one typed Feature Intent operation or operation list to safe M&B source syntax without accepting a raw tuple/expression string or writing source.",
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_ir_render_tool(
    operation: dict[str, Any] | None = None,
    operations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        if (operation is None) == (operations is None):
            raise ValueError("Supply exactly one of operation or operations.")
        if operation is not None:
            payload = {"kind": "operation", "source": feature_authoring.render_operation(operation)}
        else:
            payload = {"kind": "operation_list", "source": feature_authoring.render_operations(operations)}
        return success("feature_ir_render", payload)

    return guarded("feature_ir_render", action)


@mcp.tool(
    name="feature_plan",
    description=(
        "Compile a checked-in or inline typed Feature Intent to exact independent source patch plans, Blueprint evidence, order-aware entrypoint traces, and focused verification obligations. Never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_plan_tool(
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_plan(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            feature_id=feature_id,
            intent_value=intent,
            trace_limit=require_int("trace_limit", trace_limit, 1, 30),
        )
        return success("feature_plan", payload, extra_warnings=payload["warnings"])

    return guarded("feature_plan", action)


@mcp.tool(
    name="feature_apply",
    description=(
        "Rehearse or apply one reviewed Feature Intent change through the shared SHA-guarded source-only gate. "
        "Requires the exact feature plan ID and selected change's current source SHA; dry_run is true by default."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def feature_apply_tool(
    change_id: str,
    expected_feature_plan_id: str,
    expected_sha256: str,
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
    dry_run: bool = True,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_apply(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            feature_id=feature_id,
            intent_value=intent,
            change_id=change_id,
            expected_feature_plan_id=expected_feature_plan_id,
            expected_sha256=expected_sha256,
            dry_run=dry_run,
        )
        return success("feature_apply", payload, extra_warnings=payload["warnings"], read_only=dry_run)

    return guarded("feature_apply", action, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="feature_verify",
    description=(
        "Re-evaluate a Feature Intent's entrypoints, Module Blueprint, source syntax/order/freshness, and optionally its declared focused tests or isolated area builds. Never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_verify_tool(
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    timeout_seconds: int = 90,
    source_limit: int = 24,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_verify(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            feature_id=feature_id,
            intent_value=intent,
            run_tests=run_tests,
            stage_build_check=stage_build_check,
            timeout_seconds=require_int("timeout_seconds", timeout_seconds, 10, 300),
            source_limit=require_int("source_limit", source_limit, 1, 80),
        )
        return success("feature_verify", payload, extra_warnings=payload["warnings"])

    return guarded("feature_verify", action)


@mcp.tool(
    name="feature_semantic_snapshot",
    description=(
        "Return an in-memory Feature Intent semantic baseline with entrypoint provenance/order/ID evidence, Blueprint state, and typed patch bases. It writes no artifact."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_semantic_snapshot_tool(
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_semantic_snapshot(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            feature_id=feature_id,
            intent_value=intent,
        )
        return success("feature_semantic_snapshot", payload, extra_warnings=payload["warnings"])

    return guarded("feature_semantic_snapshot", action)


@mcp.tool(
    name="feature_semantic_diff",
    description=(
        "Compare a previous feature_semantic_snapshot object with current Feature Intent semantics, reporting changed entrypoints, source/order/ID evidence, Blueprint state, and typed patch bases."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def feature_semantic_diff_tool(
    before: dict[str, Any],
    feature_id: str | None = None,
    intent: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = feature_authoring.feature_semantic_diff(
            feature_authoring.build_feature_authoring(REPO_ROOT),
            before,
            feature_id=feature_id,
            intent_value=intent,
        )
        return success("feature_semantic_diff", payload, extra_warnings=payload["warnings"])

    return guarded("feature_semantic_diff", action)


@mcp.tool(
    name="content_forge_summary",
    description=(
        "Summarize checked-in typed Content Forge packs and coverage across dialogue, quest/event, campaign AI, troop/item, and presentation authoring slices."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_forge_summary_tool(limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_forge_summary(
            content_forge.build_content_forge(REPO_ROOT),
            limit=require_int("limit", limit, 1, 200),
        )
        return success("content_forge_summary", payload, extra_warnings=payload["warnings"])

    return guarded("content_forge_summary", action)


@mcp.tool(
    name="content_pack_find",
    description="Find a Content Forge pack by its brief, lore/tone/acceptance criteria, slice, entrypoint, contract, or declared test/scenario.",
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_find_tool(query: str, slice: str = "all", limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_find(
            content_forge.build_content_forge(REPO_ROOT),
            require_query(query),
            slice_name=slice,
            limit=require_int("limit", limit, 1, 200),
        )
        return success("content_pack_find", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_find", action)


@mcp.tool(
    name="content_pack_explain",
    description=(
        "Explain one checked-in or inline typed Content Pack through its brief, source slices, real engine entrypoints, Feature Intent compilation, and declared scenario evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_explain_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_explain(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
            trace_limit=require_int("trace_limit", trace_limit, 1, 30),
        )
        return success("content_pack_explain", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_explain", action)


@mcp.tool(
    name="content_pack_validate",
    description=(
        "Validate one checked-in or inline Content Pack's strict JSON contract, specialist typed-source route, declared tests, Blueprint requirement, and scenario IDs before planning."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_validate_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_validate(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
        )
        return success("content_pack_validate", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_validate", action)


@mcp.tool(
    name="content_pack_compile",
    description=(
        "Compile a Content Pack into an explicit order-aware sequence of Feature Authoring and Balance Lab changes without producing a diff or writing source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_compile_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_compile(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
        )
        return success("content_pack_compile", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_compile", action)


@mcp.tool(
    name="content_pack_plan",
    description=(
        "Compile a Content Pack to exact independently guarded source/balance diffs, current SHAs, planned AI intent evidence, ordering impacts, and verification obligations. Never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_plan_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_plan(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
            trace_limit=require_int("trace_limit", trace_limit, 1, 30),
        )
        return success("content_pack_plan", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_plan", action)


@mcp.tool(
    name="content_pack_preview",
    description=(
        "Return static narrative beats, quest/event timeline, AI evidence, balance patches, existing presentation canvases, planned new-presentation summaries, and a review canvas for one Content Pack."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_preview_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_preview(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
            trace_limit=require_int("trace_limit", trace_limit, 1, 30),
        )
        return success("content_pack_preview", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_preview", action)


@mcp.tool(
    name="content_pack_review",
    description=(
        "Return a deterministic structured/Mermaid human review canvas showing a Content Pack's brief, slices, dependencies, apply sequence, contracts, and acceptance review state."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_review_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
    trace_limit: int = 12,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_review(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
            trace_limit=require_int("trace_limit", trace_limit, 1, 30),
        )
        return success("content_pack_review", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_review", action)


@mcp.tool(
    name="content_pack_apply",
    description=(
        "Rehearse or apply exactly one reviewed Content Pack change through its specialist source or legacy-record gate. Requires exact content-plan ID and current SHA; troop/item changes also require Balance Lab's plan SHA. dry_run is true by default."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def content_pack_apply_tool(
    change_id: str,
    expected_content_plan_id: str,
    expected_sha256: str,
    expected_balance_plan_sha256: str | None = None,
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
    dry_run: bool = True,
    allow_legacy_compile_authoring: bool = False,
    allow_protected_legacy_record_change: bool = False,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_apply(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
            change_id=change_id,
            expected_content_plan_id=expected_content_plan_id,
            expected_sha256=expected_sha256,
            expected_balance_plan_sha256=expected_balance_plan_sha256,
            dry_run=dry_run,
            allow_legacy_compile_authoring=allow_legacy_compile_authoring,
            allow_protected_legacy_record_change=allow_protected_legacy_record_change,
        )
        return success("content_pack_apply", payload, extra_warnings=payload["warnings"], read_only=dry_run)

    return guarded("content_pack_apply", action, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="content_pack_verify",
    description=(
        "Re-evaluate a Content Pack's specialist source/order checks, current AI intent contracts, direct legacy-record integrity, and optionally focused tests, staged builds, or bounded deterministic scenarios. Never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_verify_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    run_scenarios: bool = False,
    scenario_iterations: int = 8,
    scenario_seed: int = 1,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_verify(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
            run_tests=run_tests,
            stage_build_check=stage_build_check,
            run_scenarios=run_scenarios,
            scenario_iterations=require_int("scenario_iterations", scenario_iterations, 1, 50),
            scenario_seed=scenario_seed,
            timeout_seconds=require_int("timeout_seconds", timeout_seconds, 10, 300),
        )
        return success("content_pack_verify", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_verify", action)


@mcp.tool(
    name="content_pack_snapshot",
    description=(
        "Return an in-memory Content Pack semantic baseline: declared pack contract, specialist plan bases, current feature evidence, and AI contract status. It writes no artifact."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_snapshot_tool(
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_snapshot(
            content_forge.build_content_forge(REPO_ROOT),
            pack_id=pack_id,
            pack_value=pack,
        )
        return success("content_pack_snapshot", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_snapshot", action)


@mcp.tool(
    name="content_pack_semantic_diff",
    description=(
        "Compare an earlier content_pack_snapshot object with current pack/source/balance/AI evidence, reporting changed typed plan bases and intent-contract status."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_semantic_diff_tool(
    before: dict[str, Any],
    pack_id: str | None = None,
    pack: dict[str, Any] | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_semantic_diff(
            content_forge.build_content_forge(REPO_ROOT),
            before,
            pack_id=pack_id,
            pack_value=pack,
        )
        return success("content_pack_semantic_diff", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_semantic_diff", action)


@mcp.tool(
    name="content_pack_catalog_plan",
    description=(
        "Plan a strict create or replacement of one checked-in Content Forge pack contract in devkit/content_forge/packs.json. "
        "Returns the exact catalog diff and SHA guard; never writes module source, generated layers, or exports."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def content_pack_catalog_plan_tool(pack: dict[str, Any], mode: str) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_catalog_plan(
            content_forge.build_content_forge(REPO_ROOT),
            pack_value=pack,
            mode=mode,
        )
        return success("content_pack_catalog_plan", payload, extra_warnings=payload["warnings"])

    return guarded("content_pack_catalog_plan", action)


@mcp.tool(
    name="content_pack_catalog_apply",
    description=(
        "Rehearse or save one reviewed strict Content Forge pack contract to devkit/content_forge/packs.json. "
        "Requires the exact catalog-plan ID, current catalog SHA, and SAVE CONTENT PACK confirmation when dry_run=false; it never applies module source or writes generated/export layers."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def content_pack_catalog_apply_tool(
    pack: dict[str, Any],
    mode: str,
    expected_catalog_plan_id: str,
    expected_catalog_sha256: str,
    dry_run: bool = True,
    confirmation: str | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = content_forge.content_pack_catalog_apply(
            content_forge.build_content_forge(REPO_ROOT),
            pack_value=pack,
            mode=mode,
            expected_catalog_plan_id=expected_catalog_plan_id,
            expected_catalog_sha256=expected_catalog_sha256,
            dry_run=dry_run,
            confirmation=confirmation,
        )
        return success(
            "content_pack_catalog_apply",
            payload,
            extra_warnings=payload["warnings"],
            read_only=dry_run,
        )

    return guarded("content_pack_catalog_apply", action, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="campaign_state_summary",
    description=(
        "Build a read-only temporal campaign-state model over canonical scripts and simple triggers: "
        "state readers/writers, trigger paths, contracts, and bounded overwrite findings."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_state_summary(limit: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        index = campaign_state_doctor.build_state_doctor(REPO_ROOT)
        payload = campaign_state_doctor.summary_payload(index, limit=maximum)
        return success("campaign_state_summary", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_state_summary", action)


@mcp.tool(
    name="campaign_state_findings",
    description=(
        "Filter source-mapped temporal state findings by severity or text. Findings preserve uncertainty and include "
        "a compact counterexample timeline instead of claiming runtime certainty."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_state_findings(
    severity: str = "all",
    query: str | None = None,
    limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_query = require_query(query) if query is not None else None
        index = campaign_state_doctor.build_state_doctor(REPO_ROOT)
        payload = campaign_state_doctor.findings_payload(
            index,
            severity=severity,
            query=checked_query,
            limit=maximum,
        )
        return success("campaign_state_findings", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_state_findings", action)


@mcp.tool(
    name="campaign_state_resource",
    description=(
        "Find a party AI field, party/faction/troop slot, lifecycle field, or global state resource and return its "
        "source-mapped readers/writers with trigger reachability evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_state_resource(resource: str, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_resource = require_query(resource)
        index = campaign_state_doctor.build_state_doctor(REPO_ROOT)
        payload = campaign_state_doctor.resource_payload(index, checked_resource, limit=maximum)
        return success("campaign_state_resource", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_state_resource", action)


@mcp.tool(
    name="campaign_state_timeline",
    description=(
        "Return full ordered operation/branch evidence and known trigger call paths for one campaign-state resource. "
        "It keeps separate engine callbacks as explicit scheduler boundaries."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_state_timeline(resource: str, limit: int = 60) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_resource = require_query(resource)
        index = campaign_state_doctor.build_state_doctor(REPO_ROOT)
        payload = campaign_state_doctor.timeline_payload(index, checked_resource, limit=maximum)
        return success("campaign_state_timeline", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_state_timeline", action)


@mcp.tool(
    name="campaign_state_contracts",
    description=(
        "Evaluate checked-in temporal gameplay invariants and return pass/fail checks plus source-mapped counterexample "
        "timelines for every violation."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_state_contracts(contract_id: str | None = None) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_id = require_query(contract_id) if contract_id is not None else None
        index = campaign_state_doctor.build_state_doctor(REPO_ROOT)
        payload = campaign_state_doctor.contracts_payload(index, contract_id=checked_id)
        return success("campaign_state_contracts", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_state_contracts", action)


@mcp.tool(
    name="campaign_ai_intents",
    description=(
        "Inspect stationary-camp and generic party-template AI intent contracts for patrol radii, escort attachment, "
        "raid return, and despawn behavior with source-mapped checks."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_ai_intents(intent: str | None = None) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_intent = require_query(intent) if intent is not None else None
        index = campaign_state_doctor.build_state_doctor(REPO_ROOT)
        payload = campaign_state_doctor.ai_intents_payload(index, intent=checked_intent)
        return success("campaign_ai_intents", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_ai_intents", action)


@mcp.tool(
    name="slot_lifecycle_summary",
    description="Summarize declared durable-slot ownership, lifecycle clearing, approved handoffs, and unowned sharing review candidates.",
    annotations=READ_ONLY,
    structured_output=True,
)
def slot_lifecycle_summary(limit: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        index = slot_lifecycle_lint.build_slot_lifecycle_lint(REPO_ROOT)
        payload = slot_lifecycle_lint.summary_payload(index, limit=maximum)
        return success("slot_lifecycle_summary", payload, extra_warnings=payload["warnings"])

    return guarded("slot_lifecycle_summary", action)


@mcp.tool(
    name="slot_lifecycle_findings",
    description="Filter declared slot-owner violations, lifecycle clear failures, and read-after-clear candidates with source evidence.",
    annotations=READ_ONLY,
    structured_output=True,
)
def slot_lifecycle_findings(severity: str = "all", query: str | None = None, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_query = require_query(query) if query is not None else None
        index = slot_lifecycle_lint.build_slot_lifecycle_lint(REPO_ROOT)
        payload = slot_lifecycle_lint.findings_payload(index, severity=severity, query=checked_query, limit=maximum)
        return success("slot_lifecycle_findings", payload, extra_warnings=payload["warnings"])

    return guarded("slot_lifecycle_findings", action)


@mcp.tool(
    name="slot_lifecycle_ownership",
    description="Return checked-in slot owner prefixes, approved conversion handoffs, clear values, and matched slots.",
    annotations=READ_ONLY,
    structured_output=True,
)
def slot_lifecycle_ownership(slot: str | None = None, limit: int = 40) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        checked_slot = require_query(slot) if slot is not None else None
        index = slot_lifecycle_lint.build_slot_lifecycle_lint(REPO_ROOT)
        payload = slot_lifecycle_lint.ownership_payload(index, slot=checked_slot, limit=maximum)
        return success("slot_lifecycle_ownership", payload, extra_warnings=payload["warnings"])

    return guarded("slot_lifecycle_ownership", action)


@mcp.tool(
    name="slot_lifecycle_slot",
    description="Inspect every modeled reader/writer, namespace, owner rule, and source operation for one durable slot.",
    annotations=READ_ONLY,
    structured_output=True,
)
def slot_lifecycle_slot(slot: str, limit: int = 50) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 200)
        index = slot_lifecycle_lint.build_slot_lifecycle_lint(REPO_ROOT)
        payload = slot_lifecycle_lint.slot_payload(index, require_query(slot), limit=maximum)
        return success("slot_lifecycle_slot", payload, extra_warnings=payload["warnings"])

    return guarded("slot_lifecycle_slot", action)


@mcp.tool(
    name="campaign_scenario_summary",
    description="Summarize checked-in valid-state scenario fuzzing coverage and the supported literal M&B script subset.",
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_scenario_summary() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = campaign_scenario_fuzzer.build_scenario_fuzzer(REPO_ROOT)
        payload = campaign_scenario_fuzzer.summary_payload(index)
        return success("campaign_scenario_summary", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_scenario_summary", action)


@mcp.tool(
    name="campaign_scenario_catalog",
    description="List checked-in campaign state domains, entry scripts, assertions, and modeled-entry availability for the safe scenario fuzzer.",
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_scenario_catalog(scenario_id: str | None = None) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked = require_query(scenario_id) if scenario_id is not None else None
        index = campaign_scenario_fuzzer.build_scenario_fuzzer(REPO_ROOT)
        payload = campaign_scenario_fuzzer.scenario_catalog_payload(index, scenario_id=checked)
        return success("campaign_scenario_catalog", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_scenario_catalog", action)


@mcp.tool(
    name="campaign_scenario_fuzz",
    description="Generate deterministic valid campaign states and run the safe literal script subset; returns a reproducible counterexample or inconclusive boundary.",
    annotations=READ_ONLY,
    structured_output=True,
)
def campaign_scenario_fuzz(scenario_id: str, iterations: int = 50, seed: int = 1, trace_limit: int = 80) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_iterations = require_int("iterations", iterations, 1, 1000)
        checked_seed = require_int("seed", seed, -2_000_000_000, 2_000_000_000)
        checked_trace = require_int("trace_limit", trace_limit, 1, 500)
        index = campaign_scenario_fuzzer.build_scenario_fuzzer(REPO_ROOT)
        payload = campaign_scenario_fuzzer.fuzz_payload(index, require_query(scenario_id), iterations=checked_iterations, seed=checked_seed, trace_limit=checked_trace)
        return success("campaign_scenario_fuzz", payload, extra_warnings=payload["warnings"])

    return guarded("campaign_scenario_fuzz", action)


@mcp.tool(
    name="text_explain",
    description=(
        "Explain why a visible dialogue, menu, presentation, or message sink can show text: "
        "return source-mapped conditions, writer history, dynamic selectors, script effects, globals, and menu transitions."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def text_explain(
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 10,
    max_steps: int = 100,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 100)
        checked_steps = require_int("max_steps", max_steps, 1, 250)
        checked_query = require_query(query) if query is not None else None
        checked_sink_id = require_query(sink_id) if sink_id is not None else None
        ledger = text_execution_ledger.build_ledger(REPO_ROOT)
        payload = text_execution_ledger.explain(
            ledger,
            query=checked_query,
            sink_id=checked_sink_id,
            kind=kind,
            include_clean=include_clean,
            limit=maximum,
            max_steps=checked_steps,
        )
        return success("text_explain", payload, extra_warnings=payload["warnings"])

    return guarded("text_explain", action)


@mcp.tool(
    name="register_history",
    description=(
        "Return source-mapped generated reads and writes for an s-register, reg-register, "
        "local, or global variable so cross-screen text state can be traced."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def register_history_tool(symbol: str, limit: int = 30) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_symbol = require_query(symbol)
        maximum = require_int("limit", limit, 1, 100)
        ledger = text_execution_ledger.build_ledger(REPO_ROOT)
        payload = text_execution_ledger.register_history(
            ledger,
            checked_symbol,
            limit=maximum,
        )
        return success("register_history", payload, extra_warnings=payload["warnings"])

    return guarded("register_history", action)


@mcp.tool(
    name="possible_texts",
    description=(
        "Return a bounded static template and substitution-candidate model for matching visible text sinks."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def possible_texts_tool(
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 10,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 100)
        checked_query = require_query(query) if query is not None else None
        checked_sink_id = require_query(sink_id) if sink_id is not None else None
        ledger = text_execution_ledger.build_ledger(REPO_ROOT)
        payload = text_execution_ledger.possible_texts(
            ledger,
            query=checked_query,
            sink_id=checked_sink_id,
            kind=kind,
            include_clean=include_clean,
            limit=maximum,
        )
        return success("possible_texts", payload, extra_warnings=payload["warnings"])

    return guarded("possible_texts", action)


@mcp.tool(
    name="string_provenance_summary",
    description="Summarize literal generated script-call coverage for interprocedural s-register writer provenance.",
    annotations=READ_ONLY,
    structured_output=True,
)
def string_provenance_summary(limit: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 100)
        index = string_provenance.build_string_provenance(REPO_ROOT)
        payload = string_provenance.summary_payload(index, limit=maximum)
        return success("string_provenance_summary", payload, extra_warnings=payload["warnings"])

    return guarded("string_provenance_summary", action)


@mcp.tool(
    name="string_provenance_paths",
    description="Follow one s-register through a literal script's nested call_script graph and enclosing try/else branch conditions.",
    annotations=READ_ONLY,
    structured_output=True,
)
def string_provenance_paths(script_symbol: str, register: str, limit: int = 40) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 80)
        index = string_provenance.build_string_provenance(REPO_ROOT)
        payload = string_provenance.script_paths_payload(index, require_query(script_symbol), string_provenance.require_register(register), limit=maximum)
        return success("string_provenance_paths", payload, extra_warnings=payload["warnings"])

    return guarded("string_provenance_paths", action)


@mcp.tool(
    name="string_provenance_explain",
    description="Resolve script-clobber evidence for visible text sinks into actual nested writer paths and unresolved boundaries.",
    annotations=READ_ONLY,
    structured_output=True,
)
def string_provenance_explain(
    query: str | None = None,
    sink_id: str | None = None,
    kind: str = "all",
    include_clean: bool = True,
    limit: int = 10,
    max_paths: int = 20,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 100)
        checked_paths = require_int("max_paths", max_paths, 1, 80)
        checked_query = require_query(query) if query is not None else None
        checked_sink = require_query(sink_id) if sink_id is not None else None
        index = string_provenance.build_string_provenance(REPO_ROOT)
        payload = string_provenance.explain(
            index,
            query=checked_query,
            sink_id=checked_sink,
            kind=kind,
            include_clean=include_clean,
            limit=maximum,
            max_paths=checked_paths,
        )
        return success("string_provenance_explain", payload, extra_warnings=payload["warnings"])

    return guarded("string_provenance_explain", action)


@mcp.tool(
    name="semantic_change_snapshot",
    description=(
        "Capture current dialogue precedence, state writers, string sinks, generated IDs, trigger effects, and export hashes. "
        "With a label, writes only a confined DevKit baseline for a later semantic diff."
    ),
    annotations=WRITE_ARTIFACT,
    structured_output=True,
)
def semantic_change_snapshot(label: str | None = None, overwrite: bool = False) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        if not isinstance(overwrite, bool):
            raise ValueError("overwrite must be true or false.")
        checked_label = semantic_change_diff.require_label(label) if label is not None else None
        payload = semantic_change_diff.snapshot_payload(REPO_ROOT, label=checked_label, overwrite=overwrite)
        return success(
            "semantic_change_snapshot",
            payload,
            extra_warnings=payload["snapshot"]["warnings"],
            read_only=checked_label is None,
        )

    return guarded("semantic_change_snapshot", action, read_only=label is None)


@mcp.tool(
    name="semantic_change_diff",
    description="Compare current semantic behavior surfaces to a named pre-edit DevKit snapshot instead of returning only raw file diffs.",
    annotations=READ_ONLY,
    structured_output=True,
)
def semantic_change_diff_tool(baseline: str, limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 300)
        checked = semantic_change_diff.require_label(baseline)
        payload = semantic_change_diff.diff_payload(REPO_ROOT, baseline=checked, limit=maximum)
        return success("semantic_change_diff", payload, extra_warnings=payload["warnings"])

    return guarded("semantic_change_diff", action)


@mcp.tool(
    name="presentation_layout_summary",
    description=(
        "Summarize the static Presentation Layout Composer: presentation/overlay coverage, load-trigger coverage, "
        "and the explicit limits of static engine-layout reconstruction."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def presentation_layout_summary() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_summary(index)
        return success("presentation_layout_summary", payload, extra_warnings=payload["warnings"])

    return guarded("presentation_layout_summary", action)


@mcp.tool(
    name="presentation_find",
    description=(
        "Find authored presentations and direct overlay creation/binding records by id, source, destination, or content. "
        "Returns stable presentation and overlay IDs for canvas, patch, apply, and verify."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def presentation_find(query: str, limit: int = 20) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_find(index, query=query, limit=limit)
        return success("presentation_find", payload, extra_warnings=payload["summary"]["warnings"])

    return guarded("presentation_find", action)


@mcp.tool(
    name="presentation_canvas",
    description=(
        "Build a bounded static canvas for one presentation from create-overlay operations, position/size register bindings, "
        "text/mesh/color state, and layout findings. Dynamic paths remain marked unresolved."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def presentation_canvas(
    presentation_id: str,
    width: int = 1024,
    height: int = 768,
    overlay_limit: int = 200,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_canvas(
            index,
            presentation_id,
            width=width,
            height=height,
            overlay_limit=overlay_limit,
        )
        return success("presentation_canvas", payload, extra_warnings=payload["warnings"])

    return guarded("presentation_canvas", action)


@mcp.tool(
    name="presentation_preview",
    description=(
        "Write a confined devkit/output SVG diagnostic preview of a presentation's static canvas. "
        "It never writes source, generated modules, or exports."
    ),
    annotations=WRITE_ARTIFACT,
    structured_output=True,
)
def presentation_preview(
    presentation_id: str,
    output_name: str | None = None,
    width: int = 1024,
    height: int = 768,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_preview(
            index,
            presentation_id,
            output_name=output_name,
            width=width,
            height=height,
        )
        return success(
            "presentation_preview",
            payload,
            extra_warnings=payload["warnings"],
            read_only=False,
        )

    return guarded("presentation_preview", action, read_only=False)


@mcp.tool(
    name="presentation_patch",
    description=(
        "Create a source-only semantic presentation patch plan: move/resize/align an overlay, alter text/mesh/color/alpha, "
        "add/remove a direct control, or add/remove/replace a presentation trigger block. Returns a unified diff and SHA-256; never writes source."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def presentation_patch(
    target: str,
    action: str,
    x: float | None = None,
    y: float | None = None,
    value: str | None = None,
    alignment: str | None = None,
    new_overlay: dict[str, Any] | None = None,
    new_trigger: dict[str, Any] | None = None,
    trigger: str = "ti_on_presentation_load",
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    def call() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_patch(
            index,
            target,
            action=action,
            x=x,
            y=y,
            value=value,
            alignment=alignment,
            new_overlay=new_overlay,
            new_trigger=new_trigger,
            trigger=trigger,
            expected_sha256=expected_sha256,
        )
        return success("presentation_patch", payload, extra_warnings=payload["warnings"])

    return guarded("presentation_patch", call)


@mcp.tool(
    name="presentation_apply",
    description=(
        "Apply a semantic presentation action through the Change Router's SHA-guarded source-only edit gate. "
        "dry_run is true by default; generated modules and exports are never written."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def presentation_apply(
    target: str,
    action: str,
    expected_sha256: str,
    dry_run: bool = True,
    x: float | None = None,
    y: float | None = None,
    value: str | None = None,
    alignment: str | None = None,
    new_overlay: dict[str, Any] | None = None,
    new_trigger: dict[str, Any] | None = None,
    trigger: str = "ti_on_presentation_load",
) -> dict[str, Any]:
    def call() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_apply(
            index,
            target,
            action=action,
            expected_sha256=expected_sha256,
            dry_run=dry_run,
            x=x,
            y=y,
            value=value,
            alignment=alignment,
            new_overlay=new_overlay,
            new_trigger=new_trigger,
            trigger=trigger,
        )
        return success(
            "presentation_apply",
            payload,
            extra_warnings=payload["warnings"],
            read_only=dry_run,
        )

    return guarded("presentation_apply", call, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="presentation_verify",
    description=(
        "Verify one presentation source target after semantic layout authoring: syntax, ordering, generated freshness, "
        "static tests, optional isolated build, static canvas, and layout findings."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def presentation_verify(
    target: str,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = presentation_layout.build_presentation_layout(REPO_ROOT)
        payload = presentation_layout.presentation_verify(
            index,
            target,
            expected_sha256=expected_sha256,
            run_tests=run_tests,
            stage_build_check=stage_build,
            max_tests=max_tests,
            timeout_seconds=timeout_seconds,
        )
        return success("presentation_verify", payload, extra_warnings=payload["warnings"])

    return guarded("presentation_verify", action)


@mcp.tool(
    name="module_atlas_summary",
    description=(
        "Summarize the complete Module Atlas: semantic coverage across constants, dialogues, menus, mission templates, "
        "presentations, quests, scripts, and simple triggers plus static cross-area link counts."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_atlas_summary() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_summary(index)
        return success("module_atlas_summary", payload, extra_warnings=payload["warnings"])

    return guarded("module_atlas_summary", action)


@mcp.tool(
    name="module_integrity",
    description=(
        "Run a bounded static structural scan for duplicate authored definitions, unresolved direct script/menu/mission/"
        "presentation/quest references, syntax errors, and known generated-ID fallback boundaries."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_integrity_tool(limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("limit", limit, 1, 500)
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_integrity(index, limit=maximum)
        return success("module_integrity", payload, extra_warnings=payload["warnings"])

    return guarded("module_integrity", action)


@mcp.tool(
    name="module_find",
    description=(
        "Find authored semantic entities in any source area by text, identifier, path, kind, or symbol. "
        "Returns stable Module Atlas entity IDs for context, graphs, plans, apply, and verification."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_find_tool(
    query: str | None = None,
    area: str = "all",
    kind: str | None = None,
    limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_find(index, query=query, area=area, kind=kind, limit=limit)
        return success("module_find", payload)

    return guarded("module_find", action)


@mcp.tool(
    name="module_context",
    description=(
        "Explain one Module Atlas entity with exact source/generated provenance, operation blocks, child records, "
        "inbound/outbound semantic links, and its supported guarded authoring actions."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_context_tool(
    entity_id: str,
    max_lines: int = 120,
    related_limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_context(
            index,
            entity_id,
            max_lines=max_lines,
            related_limit=related_limit,
        )
        return success("module_context", payload)

    return guarded("module_context", action)


@mcp.tool(
    name="module_graph",
    description=(
        "Return a bounded static cross-area dependency graph around one Module Atlas entity: callers, menu transitions, "
        "mission/presentation starts, quests, constants, and other direct symbolic links."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_graph_tool(
    entity_id: str,
    direction: str = "both",
    depth: int = 2,
    max_nodes: int = 100,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_graph(
            index,
            entity_id,
            direction=direction,
            depth=depth,
            max_nodes=max_nodes,
        )
        return success("module_graph", payload)

    return guarded("module_graph", action)


@mcp.tool(
    name="menu_flow",
    description=(
        "Inspect one authored game menu, its options and operation blocks, and a bounded static outgoing flow graph. "
        "This is source evidence, not a simulation of conditions or register values."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def menu_flow_tool(menu_id: str, depth: int = 2, max_nodes: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.menu_flow(index, menu_id, depth=depth, max_nodes=max_nodes)
        return success("menu_flow", payload, extra_warnings=payload["warnings"])

    return guarded("menu_flow", action)


@mcp.tool(
    name="script_flow",
    description=(
        "Inspect one authored script's operation block and bounded static call/dependency graph, including direct script, "
        "menu, mission, presentation, quest, constant, register, and global evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def script_flow_tool(
    script_name: str,
    direction: str = "both",
    depth: int = 2,
    max_nodes: int = 120,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.script_flow(
            index,
            script_name,
            direction=direction,
            depth=depth,
            max_nodes=max_nodes,
        )
        return success("script_flow", payload, extra_warnings=payload["warnings"])

    return guarded("script_flow", action)


@mcp.tool(
    name="mission_timeline",
    description=(
        "Inspect one authored mission template's trigger timeline, condition/consequence operation blocks, and static "
        "outgoing dependency graph without pretending to execute engine events."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def mission_timeline_tool(mission_id: str, depth: int = 2, max_nodes: int = 120) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.mission_timeline(index, mission_id, depth=depth, max_nodes=max_nodes)
        return success("mission_timeline", payload, extra_warnings=payload["warnings"])

    return guarded("mission_timeline", action)


@mcp.tool(
    name="trigger_timeline",
    description=(
        "Find authored simple triggers and return their intervals, operation blocks, and direct outbound links. "
        "Use entity_id from module_find for an exact trigger."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def trigger_timeline_tool(
    query: str | None = None,
    entity_id: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.trigger_timeline(index, query=query, entity_id=entity_id, limit=limit)
        return success("trigger_timeline", payload, extra_warnings=payload["warnings"])

    return guarded("trigger_timeline", action)


@mcp.tool(
    name="quest_registry",
    description=(
        "List authored quests with source fields and direct inbound/outbound static link counts, bounded by query and limit."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def quest_registry_tool(query: str | None = None, limit: int = 50) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.quest_registry(index, query=query, limit=limit)
        return success("quest_registry", payload)

    return guarded("quest_registry", action)


@mcp.tool(
    name="entity_references",
    description=(
        "Find an Atlas definition and its direct authored semantic references, with a bounded raw-source fallback search "
        "for symbols that cross the modular boundary."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def entity_references_tool(symbol: str, limit: int = 80) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.entity_references(index, symbol, limit=limit)
        return success("entity_references", payload)

    return guarded("entity_references", action)


@mcp.tool(
    name="module_patch",
    description=(
        "Create a semantic source-only patch plan for constants, menus/options, missions/triggers, quests, scripts, or simple triggers. "
        "Returns a unified diff, graph evidence, and required SHA-256; dialogue and presentations deliberately delegate to their specialist composers."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_patch_tool(
    entity_id: str,
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
    def call() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_patch(
            index,
            entity_id,
            action=action,
            field=field,
            block=block,
            value=value,
            operation=operation,
            position=position,
            operation_index=operation_index,
            new_item=new_item,
            allow_referenced_removal=allow_referenced_removal,
            expected_sha256=expected_sha256,
        )
        return success("module_patch", payload, extra_warnings=payload["warnings"])

    return guarded("module_patch", call)


@mcp.tool(
    name="module_apply",
    description=(
        "Rehearse or apply a reviewed Module Atlas semantic action through the shared SHA-guarded source-only edit gate. "
        "dry_run is true by default; compile/ and _export/ are never written."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def module_apply_tool(
    entity_id: str,
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
    def call() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_apply(
            index,
            entity_id,
            action=action,
            expected_sha256=expected_sha256,
            dry_run=dry_run,
            field=field,
            block=block,
            value=value,
            operation=operation,
            position=position,
            operation_index=operation_index,
            new_item=new_item,
            allow_referenced_removal=allow_referenced_removal,
        )
        return success("module_apply", payload, extra_warnings=payload["warnings"], read_only=dry_run)

    return guarded("module_apply", call, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="module_verify",
    description=(
        "Verify one Module Atlas entity's source fragment after semantic authoring: syntax, ordering, generated freshness, "
        "selected static tests, and optional isolated build evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def module_verify_tool(
    entity_id: str,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        index = module_atlas.build_module_atlas(REPO_ROOT)
        payload = module_atlas.module_verify(
            index,
            entity_id,
            expected_sha256=expected_sha256,
            run_tests=run_tests,
            stage_build_check=stage_build,
            max_tests=max_tests,
            timeout_seconds=timeout_seconds,
        )
        return success("module_verify", payload, extra_warnings=payload["warnings"])

    return guarded("module_verify", action)


@mcp.tool(
    name="order_summary",
    description=(
        "Summarize explicit source manifests, authored/compiled order, generated ID tables, and protected engine-order contracts. "
        "Use this before changing any order-sensitive module-system content."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_summary_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_summary(order_control.build_order_control(REPO_ROOT))
        return success("order_summary", payload, extra_warnings=payload["warnings"])

    return guarded("order_summary", action)


@mcp.tool(
    name="order_map",
    description=(
        "Return bounded order evidence for source fragments, authored entities, generated markers, or generated ID tables. "
        "Specify an area, domain, or query; use order_explain for an exact target."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_map_tool(
    area: str = "all",
    domain: str = "all",
    query: str | None = None,
    limit: int = 60,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_map(
            order_control.build_order_control(REPO_ROOT),
            area=area,
            domain=domain,
            query=query,
            limit=limit,
        )
        return success("order_map", payload, extra_warnings=payload["warnings"])

    return guarded("order_map", action)


@mcp.tool(
    name="order_explain",
    description=(
        "Explain one source fragment, authored entity, dialogue route, or generated ID symbol across order domains and protected contracts. "
        "It reports the exact automatic move path only when one is safely supported."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_explain_tool(target: str, related_limit: int = 40) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_explain(
            order_control.build_order_control(REPO_ROOT),
            target,
            related_limit=related_limit,
        )
        return success("order_explain", payload, extra_warnings=payload["warnings"])

    return guarded("order_explain", action)


@mcp.tool(
    name="order_risk",
    description=(
        "Assess the projected risk of moving one source fragment or same-fragment dialogue route before/after an anchor. "
        "It performs no write and highlights first-match, ID, and protected-prefix consequences."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_risk_tool(target: str, anchor: str, position: str) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_risk(
            order_control.build_order_control(REPO_ROOT),
            target,
            anchor,
            position=position,
        )
        return success("order_risk", payload, extra_warnings=payload["warnings"])

    return guarded("order_risk", action)


@mcp.tool(
    name="order_plan_move",
    description=(
        "Create a deterministic, anchored order-move diff and current SHA apply contract. "
        "Only explicit _order manifests or same-fragment dialogue routes are eligible; nothing is written."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_plan_move_tool(
    target: str,
    anchor: str,
    position: str,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_plan_move(
            order_control.build_order_control(REPO_ROOT),
            target,
            anchor,
            position=position,
            expected_sha256=expected_sha256,
        )
        return success("order_plan_move", payload, extra_warnings=payload["warnings"])

    return guarded("order_plan_move", action)


@mcp.tool(
    name="order_apply_move",
    description=(
        "Rehearse or apply one reviewed anchored order move with its current SHA. "
        "dry_run is true by default; a fragment move writes only one declared src/**/_order*.txt manifest and never writes compile/ or _export/. "
        "A non-dry protected engine/legacy move additionally requires allow_protected_contract_change=true."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def order_apply_move_tool(
    target: str,
    anchor: str,
    position: str,
    expected_sha256: str,
    dry_run: bool = True,
    allow_protected_contract_change: bool = False,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_apply_move(
            order_control.build_order_control(REPO_ROOT),
            target,
            anchor,
            position=position,
            expected_sha256=expected_sha256,
            dry_run=dry_run,
            allow_protected_contract_change=allow_protected_contract_change,
        )
        return success("order_apply_move", payload, extra_warnings=payload["warnings"], read_only=dry_run)

    return guarded("order_apply_move", action, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="order_contracts",
    description=(
        "Evaluate checked-in strict manifest, hardcoded legacy-ID, and engine callback order contracts. "
        "A failure is static structural evidence that should block an order-sensitive release."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_contracts_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_contracts(order_control.build_order_control(REPO_ROOT))
        return success("order_contracts", payload, extra_warnings=payload["warnings"])

    return guarded("order_contracts", action)


@mcp.tool(
    name="order_baseline",
    description=(
        "Write an explicit ignored DevKit snapshot of source-fragment order and generated ID tables. "
        "It never changes module source, manifests, generated modules, ID tables, or exports."
    ),
    annotations=WRITE_ARTIFACT,
    structured_output=True,
)
def order_baseline_tool(label: str = "baseline", overwrite: bool = False) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_baseline(
            order_control.build_order_control(REPO_ROOT),
            label=label,
            overwrite=overwrite,
        )
        return success("order_baseline", payload, extra_warnings=payload["warnings"], read_only=False)

    return guarded("order_baseline", action, read_only=False)


@mcp.tool(
    name="order_diff",
    description=(
        "Compare current explicit source order and generated-ID tables with a named Order Control baseline. "
        "It elevates generated callback-ID shifts to critical evidence."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_diff_tool(baseline: str, limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_diff(
            order_control.build_order_control(REPO_ROOT),
            baseline=baseline,
            limit=limit,
        )
        return success("order_diff", payload, extra_warnings=payload["warnings"])

    return guarded("order_diff", action)


@mcp.tool(
    name="order_verify",
    description=(
        "Run the complete order-only verification: protected contracts, source/generated marker parity, dialogue ordering hazards, and optional baseline drift. "
        "It is static evidence and does not execute engine conditions or certify save compatibility."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def order_verify_tool(baseline: str | None = None, limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = order_control.order_verify(
            order_control.build_order_control(REPO_ROOT),
            baseline=baseline,
            limit=limit,
        )
        return success("order_verify", payload, extra_warnings=payload["warnings"])

    return guarded("order_verify", action)


@mcp.tool(
    name="balance_summary",
    description=(
        "Summarize the authoritative legacy item/troop authoring layer, evaluated record counts, type/role distribution, "
        "upgrade edges, and generated ID-table parity before troop or item balancing."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_summary_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_summary(troop_item_balance.build_balance_index(REPO_ROOT))
        return success("balance_summary", payload, extra_warnings=payload["warnings"])

    return guarded("balance_summary", action)


@mcp.tool(
    name="balance_find_items",
    description=(
        "Find evaluated M&B 1.011 items by text/type/shop availability/score with direct legacy-source provenance. "
        "Rows are bounded and sorted by a deterministic balance score, not combat DPS."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_find_items_tool(
    query: str | None = None,
    item_type: str = "all",
    merchandise: bool | None = None,
    min_score: int | None = None,
    max_score: int | None = None,
    limit: int = 60,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_find_items(
            troop_item_balance.build_balance_index(REPO_ROOT),
            query=query,
            item_type=item_type,
            merchandise=merchandise,
            min_score=min_score,
            max_score=max_score,
            limit=limit,
        )
        return success("balance_find_items", payload, extra_warnings=payload["warnings"])

    return guarded("balance_find_items", action)


@mcp.tool(
    name="balance_item",
    description=(
        "Inspect one evaluated item: decoded bit-packed stats, price/score relationship, direct source record, editable stat constructors, "
        "and bounded troop/hero inventory users."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_item_tool(item_id: str, troop_limit: int = 60) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_item(
            troop_item_balance.build_balance_index(REPO_ROOT),
            item_id,
            troop_limit=troop_limit,
        )
        return success("balance_item", payload, extra_warnings=payload["warnings"])

    return guarded("balance_item", action)


@mcp.tool(
    name="balance_find_troops",
    description=(
        "Find evaluated M&B 1.011 troops by code/name/faction/role/level, with static kit pressure and direct legacy-source provenance. "
        "Set include_heroes=false to focus on regular troop balance."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_find_troops_tool(
    query: str | None = None,
    faction: str | None = None,
    role: str | None = None,
    include_heroes: bool = True,
    min_level: int | None = None,
    max_level: int | None = None,
    limit: int = 60,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_find_troops(
            troop_item_balance.build_balance_index(REPO_ROOT),
            query=query,
            faction=faction,
            role=role,
            include_heroes=include_heroes,
            min_level=min_level,
            max_level=max_level,
            limit=limit,
        )
        return success("balance_find_troops", payload, extra_warnings=payload["warnings"])

    return guarded("balance_find_troops", action)


@mcp.tool(
    name="balance_troop",
    description=(
        "Inspect one evaluated troop: attributes, proficiencies, skills, random inventory pool, role-adjusted kit band, "
        "and direct inbound/outbound upgrade declarations."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_troop_tool(troop_id: str, item_limit: int = 80) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_troop(
            troop_item_balance.build_balance_index(REPO_ROOT),
            troop_id,
            item_limit=item_limit,
        )
        return success("balance_troop", payload, extra_warnings=payload["warnings"])

    return guarded("balance_troop", action)


@mcp.tool(
    name="balance_upgrade_tree",
    description=(
        "Return a bounded direct upgrade-tree neighborhood around a troop, with level/role/kit evidence on each node. "
        "It parses explicit upgrade()/upgrade2() declarations and does not invent runtime tree edges."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_upgrade_tree_tool(troop_id: str, depth: int = 3, limit: int = 120) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_upgrade_tree(
            troop_item_balance.build_balance_index(REPO_ROOT),
            troop_id,
            depth=depth,
            limit=limit,
        )
        return success("balance_upgrade_tree", payload, extra_warnings=payload["warnings"])

    return guarded("balance_upgrade_tree", action)


@mcp.tool(
    name="balance_roster_inventory",
    description=(
        "Catalog theme-preserving troop roster families, or inspect one exact roster's current random equipment pools and item ownership. "
        "The five SoD player cultures remain separate even though they share a runtime faction; item rows identify roster-local versus wider shared use."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_roster_inventory_tool(
    roster: str | None = None,
    include_heroes: bool = False,
    include_derived: bool = False,
    roster_limit: int = 80,
    troop_limit: int = 100,
    item_limit: int = 160,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_roster_inventory(
            troop_item_balance.build_balance_index(REPO_ROOT),
            roster=roster,
            include_heroes=include_heroes,
            include_derived=include_derived,
            roster_limit=roster_limit,
            troop_limit=troop_limit,
            item_limit=item_limit,
        )
        return success("balance_roster_inventory", payload, extra_warnings=payload["warnings"])

    return guarded("balance_roster_inventory", action)


@mcp.tool(
    name="balance_progression",
    description=(
        "Catalog troop roster families, or inspect one roster's normal/noble upgrade trajectory and separate scripted faith ascension routes. "
        "Score deltas are review evidence only and do not override roster theme or access-tier design."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_progression_tool(
    roster: str | None = None,
    include_heroes: bool = False,
    include_derived: bool = False,
    roster_limit: int = 80,
    troop_limit: int = 180,
    edge_limit: int = 220,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_progression(
            troop_item_balance.build_balance_index(REPO_ROOT),
            roster=roster,
            include_heroes=include_heroes,
            include_derived=include_derived,
            roster_limit=roster_limit,
            troop_limit=troop_limit,
            edge_limit=edge_limit,
        )
        return success("balance_progression", payload, extra_warnings=payload["warnings"])

    return guarded("balance_progression", action)


@mcp.tool(
    name="balance_campaign_cohorts",
    description=(
        "Map troop rosters to the campaign forces that can actually coexist. The five SoD player cultures are mutually exclusive "
        "new-game choices, native kingdoms remain a separate world group, and the Imperial Expedition is an endgame invasion cohort."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_campaign_cohorts_tool(
    cohort: str | None = None,
    include_heroes: bool = False,
    include_derived: bool = False,
    cohort_limit: int = 80,
    troop_limit: int = 180,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_campaign_cohorts(
            troop_item_balance.build_balance_index(REPO_ROOT),
            cohort=cohort,
            include_heroes=include_heroes,
            include_derived=include_derived,
            cohort_limit=cohort_limit,
            troop_limit=troop_limit,
        )
        return success("balance_campaign_cohorts", payload, extra_warnings=payload["warnings"])

    return guarded("balance_campaign_cohorts", action)


@mcp.tool(
    name="balance_imperial_invasion",
    description=(
        "Inspect the Imperial Expedition as a delayed invasion rather than a normal faction: core reinforcement-wave composition, "
        "optional advance auxiliaries and staging upper bounds, pressure/supply/coalition source contracts, and static review boundaries."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_imperial_invasion_tool(include_auxiliaries: bool = False) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_imperial_invasion(
            troop_item_balance.build_balance_index(REPO_ROOT),
            include_auxiliaries=include_auxiliaries,
        )
        return success("balance_imperial_invasion", payload, extra_warnings=payload["warnings"])

    return guarded("balance_imperial_invasion", action)


@mcp.tool(
    name="balance_player_start_factions",
    description=(
        "Profile the five mutually exclusive SoD player-start cultures through their live reinforcement bindings. "
        "It weighs center and lord template selection, preserves doctrine differences, and flags only broad static pressure spreads."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_player_start_factions_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_player_start_factions(
            troop_item_balance.build_balance_index(REPO_ROOT),
        )
        return success("balance_player_start_factions", payload, extra_warnings=payload["warnings"])

    return guarded("balance_player_start_factions", action)


@mcp.tool(
    name="balance_player_start_progression",
    description=(
        "Audit direct normal and noble upgrades across all five player cultures. It requires every route to raise level, "
        "preserve rank, retain a complete target loadout, and show a kit or training advance while exposing themed kit trades."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_player_start_progression_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_player_start_progression(
            troop_item_balance.build_balance_index(REPO_ROOT),
        )
        return success("balance_player_start_progression", payload, extra_warnings=payload["warnings"])

    return guarded("balance_player_start_progression", action)


@mcp.tool(
    name="balance_native_kingdoms",
    description=(
        "Profile the five coexisting Native kingdoms through their live culture A/B/C reinforcement bindings and direct upgrade routes. "
        "It bounds bulk campaign pressure while retaining infantry, ranged, cavalry, and mobility doctrine as deliberate differences."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_native_kingdoms_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_native_kingdoms(
            troop_item_balance.build_balance_index(REPO_ROOT),
        )
        return success("balance_native_kingdoms", payload, extra_warnings=payload["warnings"])

    return guarded("balance_native_kingdoms", action)


@mcp.tool(
    name="balance_mercenary_guilds",
    description=(
        "Profile the seven mercenary guilds as asymmetric contract specialists. It verifies role-aware selection, "
        "job-shaped AI company formation, dialogue identity, and themed base/noble roster evidence without treating guilds as territorial factions."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_mercenary_guilds_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_mercenary_guilds(
            troop_item_balance.build_balance_index(REPO_ROOT),
        )
        return success("balance_mercenary_guilds", payload, extra_warnings=payload["warnings"])

    return guarded("balance_mercenary_guilds", action)


@mcp.tool(
    name="balance_faith_ascensions",
    description=(
        "Audit every selected-culture Noble-to-Faith ascension route. It verifies the authored route matrix, "
        "rank transition, elite advantage signals, and target loadout contracts without flattening faith doctrines."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_faith_ascensions_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_faith_ascensions(
            troop_item_balance.build_balance_index(REPO_ROOT),
        )
        return success("balance_faith_ascensions", payload, extra_warnings=payload["warnings"])

    return guarded("balance_faith_ascensions", action)


@mcp.tool(
    name="balance_compare",
    description=(
        "Compare two through eight exact item/troop IDs using normalized evaluated stats, score deltas, kit pressure, and source provenance. "
        "This is a review aid, not a battle simulation."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_compare_tool(entity_ids: list[str]) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_compare(troop_item_balance.build_balance_index(REPO_ROOT), entity_ids)
        return success("balance_compare", payload, extra_warnings=payload["warnings"])

    return guarded("balance_compare", action)


@mcp.tool(
    name="balance_outliers",
    description=(
        "Return bounded static item value/power and troop kit/upgrade outliers for balance triage. "
        "Findings are candidates to inspect, not automatic gameplay prescriptions."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_outliers_tool(domain: str = "all", include_heroes: bool = False, limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_outliers(
            troop_item_balance.build_balance_index(REPO_ROOT),
            domain=domain,
            include_heroes=include_heroes,
            limit=limit,
        )
        return success("balance_outliers", payload, extra_warnings=payload["warnings"])

    return guarded("balance_outliers", action)


@mcp.tool(
    name="balance_patch",
    description=(
        "Plan a narrow semantic troop/item balance change against one direct legacy compile authoring record without writing. "
        "Supported item fields are name, price, and existing stat constructors; supported troop fields are name, plural, attributes, proficiencies, skills, and inventory. "
        "Returns a current source SHA, plan SHA, exact diff, and apply contract."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_patch_tool(entity_kind: str, entity_id: str, changes: dict[str, Any]) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_patch(
            troop_item_balance.build_balance_index(REPO_ROOT),
            entity_kind,
            entity_id,
            changes=changes,
        )
        return success("balance_patch", payload, extra_warnings=payload["warnings"])

    return guarded("balance_patch", action)


@mcp.tool(
    name="balance_apply",
    description=(
        "Rehearse or apply a reviewed troop/item balance record patch. dry_run=true by default. "
        "A non-dry apply writes exactly one confirmed legacy compile authoring file, never IDs/order/exports, and requires both source/plan SHA values plus allow_legacy_compile_authoring=true. "
        "A hardwired engine record additionally needs allow_protected_legacy_record_change=true."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def balance_apply_tool(
    entity_kind: str,
    entity_id: str,
    changes: dict[str, Any],
    expected_sha256: str,
    expected_plan_sha256: str,
    dry_run: bool = True,
    allow_legacy_compile_authoring: bool = False,
    allow_protected_legacy_record_change: bool = False,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_apply(
            troop_item_balance.build_balance_index(REPO_ROOT),
            entity_kind,
            entity_id,
            changes=changes,
            expected_sha256=expected_sha256,
            expected_plan_sha256=expected_plan_sha256,
            dry_run=dry_run,
            allow_legacy_compile_authoring=allow_legacy_compile_authoring,
            allow_protected_legacy_record_change=allow_protected_legacy_record_change,
        )
        return success("balance_apply", payload, extra_warnings=payload["warnings"], read_only=dry_run)

    return guarded("balance_apply", action, read_only=dry_run if isinstance(dry_run, bool) else False)


@mcp.tool(
    name="balance_verify",
    description=(
        "Verify legacy troop/item source evaluation, direct inventory indices, explicit upgrade targets, hardwired IDs, and generated ID-table parity without building or exporting. "
        "Use it after a balance patch rehearsal/apply, then run the normal reviewed builder."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def balance_verify_tool(limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = troop_item_balance.balance_verify(troop_item_balance.build_balance_index(REPO_ROOT), limit=limit)
        return success("balance_verify", payload, extra_warnings=payload["warnings"])

    return guarded("balance_verify", action)


@mcp.tool(
    name="workbench_summary",
    description=(
        "Summarize the CBO-style M&B Workbench: DevKit readiness, Atlas scale, declarative contract state, "
        "registered fixed scenarios, and the recommended impact-to-validation workflow."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_summary_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_summary(REPO_ROOT)
        return success("workbench_summary", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_summary", action)


@mcp.tool(
    name="workbench_doctor",
    description="Check Workbench prerequisites, catalogs, module roots, build entry point, Atlas, and MCP server without building or mutating module data.",
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_doctor_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_doctor(REPO_ROOT)
        return success("workbench_doctor", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_doctor", action)


@mcp.tool(
    name="workbench_impact",
    description=(
        "Build a compact impact packet for an Atlas entity ID, source target, identifier, or query: source owner, generated/export effects, "
        "ordering, semantic graph, coverage maturity, and fixed next validation steps. Set include_text_evidence for a heavier static string/register packet."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_impact_tool(
    target: str,
    limit: int = 12,
    include_text_evidence: bool = False,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_impact(
            REPO_ROOT,
            target=target,
            limit=limit,
            include_text_evidence=include_text_evidence,
        )
        return success("workbench_impact", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_impact", action)


@mcp.tool(
    name="workbench_scope_check",
    description=(
        "Run a fixed M&B validation profile for one exact Module Atlas entity: fast parses/order/freshness, standard adds selected static tests, "
        "and deep adds an isolated area build. It cannot run a caller-supplied command or write live compile/export data."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_scope_check_tool(
    entity_id: str,
    depth: str = "standard",
    expected_sha256: str | None = None,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_scope_check(
            REPO_ROOT,
            entity_id=entity_id,
            depth=depth,
            expected_sha256=expected_sha256,
            timeout_seconds=timeout_seconds,
        )
        return success("workbench_scope_check", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_scope_check", action)


@mcp.tool(
    name="workbench_text_lint",
    description=(
        "Return bounded static player-text and string/register findings by severity, with source/generated provenance. "
        "Use it before changing visible text; it explicitly preserves dynamic/runtime uncertainty."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_text_lint_tool(
    query: str | None = None,
    kind: str = "all",
    severity: str = "warning",
    limit: int = 50,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_text_lint(
            REPO_ROOT,
            query=query,
            kind=kind,
            severity=severity,
            limit=limit,
        )
        return success("workbench_text_lint", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_text_lint", action)


@mcp.tool(
    name="workbench_order_report",
    description=(
        "Run the fixed Workbench packet for order-sensitive changes: protected Order Control contracts, generated-marker parity, "
        "dialogue-order hazards, and optional source/ID baseline drift. It is static evidence, not an in-game simulation."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_order_report_tool(baseline: str | None = None, limit: int = 100) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_order_report(REPO_ROOT, baseline=baseline, limit=limit)
        return success("workbench_order_report", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_order_report", action)


@mcp.tool(
    name="workbench_contract_drift",
    description=(
        "Evaluate the checked-in declarative Workbench contracts against current static M&B evidence. "
        "Active failures are release blockers; legacy/quarantined observations remain explicit rather than silently ignored."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_contract_drift_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.contract_drift(REPO_ROOT)
        return success("workbench_contract_drift", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_contract_drift", action)


@mcp.tool(
    name="workbench_contract_baseline",
    description=(
        "Write an explicit DevKit-only static contract baseline under devkit/workbench/contracts/baselines. "
        "It records current observations but does not change contract expectations, source, generated modules, or exports."
    ),
    annotations=WRITE_ARTIFACT,
    structured_output=True,
)
def workbench_contract_baseline_tool(label: str = "baseline") -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.contract_baseline(REPO_ROOT, label=label)
        return success("workbench_contract_baseline", payload, extra_warnings=payload["warnings"], read_only=False)

    return guarded("workbench_contract_baseline", action, read_only=False)


@mcp.tool(
    name="workbench_coverage",
    description=(
        "Map authored module entities to exact contract targets, registered scenario targets, generated provenance, and selected static-test candidates. "
        "Use gaps_only to find entities whose evidence is still source-only/generated-only."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_coverage_tool(
    area: str = "all",
    kind: str | None = None,
    query: str | None = None,
    gaps_only: bool = False,
    limit: int = 50,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_coverage(
            REPO_ROOT,
            area=area,
            kind=kind,
            query=query,
            gaps_only=gaps_only,
            limit=limit,
        )
        return success("workbench_coverage", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_coverage", action)


@mcp.tool(
    name="workbench_scenarios",
    description="List the checked-in fixed Workbench scenarios, their structural evidence level, targets, proof boundaries, and registered steps.",
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_scenarios_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.scenario_list(REPO_ROOT)
        return success("workbench_scenarios", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_scenarios", action)


@mcp.tool(
    name="workbench_scenario_run",
    description=(
        "Run one named, checked-in Workbench scenario using only registered builtins and registered Python test paths. "
        "It cannot execute arbitrary commands and emits structural/test evidence only."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_scenario_run_tool(scenario_id: str, timeout_seconds: int = 90) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.run_registered_scenario(
            REPO_ROOT,
            scenario_id=scenario_id,
            timeout_seconds=timeout_seconds,
            write_report=False,
        )
        return success("workbench_scenario_run", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_scenario_run", action)


@mcp.tool(
    name="workbench_release_readiness",
    description=(
        "Compose an honest static/manual release-readiness checklist from Workbench doctor, module integrity, contracts, source/compile freshness, "
        "text observability, and worktree evidence. It never certifies an in-game release."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def workbench_release_readiness_tool() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_release_readiness(REPO_ROOT, write_report=False)
        return success("workbench_release_readiness", payload, extra_warnings=payload["warnings"])

    return guarded("workbench_release_readiness", action)


@mcp.tool(
    name="workbench_draft",
    description=(
        "Create a disabled DevKit-only authoring packet for a constant, dialogue, menu, mission, presentation, quest, script, or trigger. "
        "The draft contains evidence/promotion steps but never activates content or edits src/, compile/, or _export/."
    ),
    annotations=WRITE_ARTIFACT,
    structured_output=True,
)
def workbench_draft_tool(
    kind: str,
    title: str,
    output_name: str | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        payload = workbench.workbench_draft(
            REPO_ROOT,
            kind=kind,
            title=title,
            output_name=output_name,
            overwrite=overwrite,
        )
        return success("workbench_draft", payload, extra_warnings=payload["warnings"], read_only=False)

    return guarded("workbench_draft", action, read_only=False)


@mcp.tool(
    name="change_router_summary",
    description=(
        "Summarize the persistent LLM-first source, generated-marker, ordering, and link index "
        "used to route a finding into a safe source edit."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def change_router_summary() -> dict[str, Any]:
    def action() -> dict[str, Any]:
        router = change_router.build_change_router(REPO_ROOT)
        payload = {
            "summary": change_router.router_summary(router),
            "warnings": router.warnings,
        }
        return success("change_router_summary", payload, extra_warnings=payload["warnings"])

    return guarded("change_router_summary", action)


@mcp.tool(
    name="code_find",
    description=(
        "Find source, generated, or export text/symbols and return stable source target IDs "
        "that can be passed to linked_context, change_impact, patch_plan, and verify_change."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def code_find(
    query: str,
    scope: str = "all",
    limit: int = 20,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_query = require_query(query)
        maximum = require_int("limit", limit, 1, 100)
        router = change_router.build_change_router(REPO_ROOT)
        payload = change_router.code_find(
            router,
            checked_query,
            scope=scope,
            limit=maximum,
        )
        return success("code_find", payload, extra_warnings=payload["warnings"])

    return guarded("code_find", action)


@mcp.tool(
    name="linked_context",
    description=(
        "Return a source fragment's excerpt, ordering neighbors, generated marker ranges, exports, "
        "callers/callees, globals, registers, text sinks, related fragments, and narrow test candidates."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def linked_context(
    target_id: str,
    focus_line: int | None = None,
    max_lines: int = 120,
    related_limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_target = require_query(target_id)
        checked_focus = (
            require_int("focus_line", focus_line, 1, 1_000_000)
            if focus_line is not None
            else None
        )
        checked_lines = require_int("max_lines", max_lines, 1, 400)
        checked_related = require_int("related_limit", related_limit, 1, 100)
        router = change_router.build_change_router(REPO_ROOT)
        payload = change_router.linked_context(
            router,
            checked_target,
            focus_line=checked_focus,
            max_lines=checked_lines,
            related_limit=checked_related,
        )
        return success("linked_context", payload, extra_warnings=payload["warnings"])

    return guarded("linked_context", action)


@mcp.tool(
    name="change_impact",
    description=(
        "Explain the downstream source, generated, export, ordering, script, register, menu, and "
        "visible-text impact of editing one source target before the edit is made."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def change_impact(
    target_id: str,
    related_limit: int = 30,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_target = require_query(target_id)
        checked_related = require_int("related_limit", related_limit, 1, 100)
        router = change_router.build_change_router(REPO_ROOT)
        payload = change_router.change_impact(
            router,
            checked_target,
            related_limit=checked_related,
        )
        return success("change_impact", payload, extra_warnings=payload["warnings"])

    return guarded("change_impact", action)


@mcp.tool(
    name="patch_plan",
    description=(
        "Create a deterministic, source-only unified diff from exact anchors. "
        "This is read-only and returns the SHA-256 required by apply_source_edits."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def patch_plan_tool(
    target_id: str,
    edits: list[dict[str, Any]],
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_target = require_query(target_id)
        router = change_router.build_change_router(REPO_ROOT)
        payload = change_router.patch_plan(
            router,
            checked_target,
            edits,
            expected_sha256=expected_sha256,
        )
        return success("patch_plan", payload, extra_warnings=payload["warnings"])

    return guarded("patch_plan", action)


@mcp.tool(
    name="apply_source_edits",
    description=(
        "Apply exact source-fragment edits only after SHA verification. "
        "dry_run is true by default; compile/ and _export/ are never written."
    ),
    annotations=WRITE_SOURCE,
    structured_output=True,
)
def apply_source_edits_tool(
    target_id: str,
    edits: list[dict[str, Any]],
    expected_sha256: str,
    dry_run: bool = True,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_target = require_query(target_id)
        router = change_router.build_change_router(REPO_ROOT)
        payload = change_router.apply_source_edits(
            router,
            checked_target,
            edits,
            expected_sha256=expected_sha256,
            dry_run=dry_run,
        )
        return success(
            "apply_source_edits",
            payload,
            extra_warnings=payload["warnings"],
            read_only=dry_run,
        )

    return guarded(
        "apply_source_edits",
        action,
        read_only=dry_run if isinstance(dry_run, bool) else False,
    )


@mcp.tool(
    name="verify_change",
    description=(
        "Verify a current source target's syntax, ordering, generated freshness, selected static tests, "
        "and optionally one isolated staging build without writing the live compile/export workspace."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def verify_change_tool(
    target_id: str,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_target = require_query(target_id)
        checked_tests = require_int("max_tests", max_tests, 1, 12)
        checked_timeout = require_int("timeout_seconds", timeout_seconds, 1, 300)
        router = change_router.build_change_router(REPO_ROOT)
        payload = change_router.verify_change(
            router,
            checked_target,
            expected_sha256=expected_sha256,
            run_tests=run_tests,
            stage_build_check=stage_build,
            max_tests=checked_tests,
            timeout_seconds=checked_timeout,
        )
        return success("verify_change", payload, extra_warnings=payload["warnings"])

    return guarded("verify_change", action)


@mcp.tool(
    name="dialogue_graph",
    description="Return an agent-readable dialogue-state edge list and optional DOT graph for a bounded state neighborhood or the full graph.",
    annotations=READ_ONLY,
    structured_output=True,
)
def dialogue_graph(
    start_state: str | None = None,
    depth: int = 2,
    include_all: bool = False,
    include_dot: bool = False,
) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        checked_depth = require_int("depth", depth, 1, 8)
        if not include_all and not start_state:
            raise ValueError("Specify start_state or set include_all=true.")
        inventory = load_inventory()
        selected = dialogue.graph_selection(
            inventory.entries,
            None if include_all else start_state,
            checked_depth,
        )
        edges = graph_edges(selected)
        nodes = sorted({edge["from_state"] for edge in edges} | {edge["to_state"] for edge in edges})
        data: dict[str, Any] = {
            "start_state": None if include_all else start_state,
            "depth": checked_depth,
            "include_all": include_all,
            "route_count": len(selected),
            "state_count": len(nodes),
            "edges": edges,
        }
        if include_dot:
            data["dot"] = dialogue.render_dot(selected, None if include_all else start_state)
        return success("dialogue_graph", data, inventory)

    return guarded("dialogue_graph", action)


@mcp.tool(
    name="workspace_audit",
    description="Return a bounded, read-only architecture audit of modular source, generated modules, exports, ordering contracts, freshness, and validation surface.",
    annotations=READ_ONLY,
    structured_output=True,
)
def workspace_audit_tool(max_items: int = 12) -> dict[str, Any]:
    def action() -> dict[str, Any]:
        maximum = require_int("max_items", max_items, 1, 100)
        report = workspace_audit.audit_workspace(REPO_ROOT, maximum)
        return success(
            "workspace_audit",
            {"audit": report},
            extra_warnings=report["warnings"],
        )

    return guarded("workspace_audit", action)


def main() -> None:
    # MCP stdio owns stdout. Do not add print statements here or in import-time
    # code; standard logging remains on stderr.
    mcp.run()


if __name__ == "__main__":
    main()
