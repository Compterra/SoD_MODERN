"""Loopback-only viewer and guarded semantic editor for the SoD Modern DevKit.

This module is intentionally an optional *last-mile* human interface.  MCP
and deterministic JSON CLIs remain the primary interfaces.  The Studio calls
the same specialist indexes and SHA-guarded semantic apply functions used by
those interfaces; it never offers a generic filesystem editor, shell runner,
build button, or export writer.

Run from the repository root:

    py -3 -B devkit/module_studio/module_studio.py serve

Then browse to http://127.0.0.1:8797 .  The server refuses all non-loopback
bind addresses and does not open a browser automatically.
"""

from __future__ import annotations

import argparse
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import parse_qs, unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.dialogue_composer import dialogue_composer
from devkit.module_atlas import module_atlas
from devkit.order_control import order_control
from devkit.presentation_layout import presentation_layout
from devkit.troop_item_balance import troop_item_balance
from devkit.workbench import workbench


STUDIO_VERSION = "0.3.0"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8797
MAX_BODY_BYTES = 1_000_000
MAX_QUERY_BYTES = 8_192
APPLY_CONFIRMATION = "APPLY SOURCE"
REFERENCED_REMOVAL_CONFIRMATION = "REMOVE REFERENCED ENTITY"
WEB_ROOT = Path(__file__).resolve().parent / "web"


class StudioError(RuntimeError):
    """A bounded, user-actionable Studio request error."""


class StudioNotFound(StudioError):
    """A known but unavailable local Studio API path."""


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def require_loopback_host(value: str) -> str:
    """Permit one explicit IPv4 loopback bind only.

    Accepting arbitrary interfaces would turn this intentionally local tool
    into an unauthenticated editor service.  ``localhost`` is deliberately
    not accepted because it can resolve through host-specific configuration.
    """

    if value != DEFAULT_HOST:
        raise StudioError("Module Studio is loopback-only; --host must be exactly 127.0.0.1.")
    return value


def require_port(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 65_535:
        raise StudioError("port must be an integer from 1 through 65535.")
    return value


def require_object(value: Any, *, name: str = "request body") -> dict[str, Any]:
    if not isinstance(value, dict):
        raise StudioError(f"{name} must be a JSON object.")
    return value


def require_string(value: Any, *, name: str, maximum: int = 4_000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StudioError(f"{name} must be a non-empty string.")
    if len(value) > maximum:
        raise StudioError(f"{name} must be at most {maximum:,} characters.")
    return value.strip()


def require_boolean(value: Any, *, name: str) -> bool:
    if not isinstance(value, bool):
        raise StudioError(f"{name} must be true or false.")
    return value


def optional_int(value: str | None, *, name: str, default: int, minimum: int, maximum: int) -> int:
    if value is None or value == "":
        return default
    try:
        result = int(value)
    except ValueError as error:
        raise StudioError(f"{name} must be an integer.") from error
    if not minimum <= result <= maximum:
        raise StudioError(f"{name} must be from {minimum} through {maximum}.")
    return result


def optional_boolean(value: str | None, *, name: str, default: bool) -> bool:
    if value is None or value == "":
        return default
    if value == "true":
        return True
    if value == "false":
        return False
    raise StudioError(f"{name} must be true or false when supplied.")


def parse_request_target(target: str) -> tuple[str, dict[str, str]]:
    if not isinstance(target, str) or len(target.encode("utf-8")) > MAX_QUERY_BYTES:
        raise StudioError("Request target is invalid or exceeds the 8 KiB safety limit.")
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
        raise StudioError("Request target must be a relative URL path.")
    values = parse_qs(parsed.query, keep_blank_values=True, strict_parsing=False)
    query: dict[str, str] = {}
    for key, entries in values.items():
        if len(entries) != 1:
            raise StudioError(f"Query parameter {key!r} may appear only once.")
        if len(key) > 80 or len(entries[0]) > 4_000:
            raise StudioError("Query parameter exceeds a Studio safety limit.")
        query[key] = entries[0]
    return parsed.path, query


def query_value(query: Mapping[str, str], name: str, *, required: bool = False) -> str | None:
    value = query.get(name)
    if value is None or not value.strip():
        if required:
            raise StudioError(f"Query parameter {name!r} is required.")
        return None
    return require_string(value, name=name)


def select_fields(body: Mapping[str, Any], allowed: set[str]) -> dict[str, Any]:
    unknown = sorted(set(body) - allowed)
    if unknown:
        raise StudioError("Unknown request field(s): " + ", ".join(unknown) + ".")
    return {key: value for key, value in body.items() if key in allowed}


def apply_intent(body: Mapping[str, Any]) -> tuple[bool, str]:
    dry_run = body.get("dry_run", True)
    dry_run = require_boolean(dry_run, name="dry_run")
    expected_sha256 = require_string(body.get("expected_sha256"), name="expected_sha256", maximum=128)
    if not dry_run and body.get("confirmation") != APPLY_CONFIRMATION:
        raise StudioError(
            "A non-dry-run source apply requires confirmation exactly equal to "
            f"{APPLY_CONFIRMATION!r}. Review the current diff and SHA first."
        )
    return dry_run, expected_sha256


class StudioService:
    """Typed HTTP adapter; all domain behavior stays in its specialist tool."""

    def __init__(self, root: Path = REPO_ROOT):
        self.root = root.resolve()

    def atlas(self) -> module_atlas.ModuleAtlasIndex:
        return module_atlas.build_module_atlas(self.root)

    def dialogue(self) -> dialogue_composer.DialogueComposerIndex:
        return dialogue_composer.build_dialogue_composer(self.root)

    def presentations(self) -> presentation_layout.PresentationLayoutIndex:
        return presentation_layout.build_presentation_layout(self.root)

    def order(self) -> order_control.OrderControlIndex:
        return order_control.build_order_control(self.root)

    def balance(self) -> troop_item_balance.BalanceIndex:
        return troop_item_balance.build_balance_index(self.root)

    def catalog(self) -> dict[str, Any]:
        return {
            "studio_version": f"devkit.module-studio.v{STUDIO_VERSION}",
            "interface_priority": "optional-human-ui-last",
            "bind_policy": {"host": DEFAULT_HOST, "network": "loopback-only", "cors": "disabled"},
            "editing_policy": {
                "generic_source_editor": False,
                "plan_before_apply": True,
                "sha_guard_required": True,
                "dry_run_default": True,
                "non_dry_apply_confirmation": APPLY_CONFIRMATION,
                "source_scope": "modular source by default; balance apply may write exactly one confirmed direct legacy compile/module_items.py or compile/module_troops.py record after its separate SHA/plan/acknowledgement gate; _export/ and generated IDs are never written",
            },
            "viewer_endpoints": [
                "/api/summary",
                "/api/atlas/find", "/api/atlas/entity", "/api/atlas/graph",
                "/api/atlas/menu", "/api/atlas/script", "/api/atlas/mission",
                "/api/atlas/triggers", "/api/atlas/quests", "/api/atlas/references",
                "/api/dialogue/find", "/api/dialogue/context",
                "/api/presentation/find", "/api/presentation/canvas",
                "/api/order/summary", "/api/order/map", "/api/order/explain",
                "/api/order/risk", "/api/order/contracts", "/api/order/diff",
                "/api/order/verify",
                "/api/balance/summary", "/api/balance/items", "/api/balance/item",
                "/api/balance/troops", "/api/balance/troop", "/api/balance/upgrade-tree",
                "/api/balance/compare", "/api/balance/outliers", "/api/balance/verify",
                "/api/workbench/summary", "/api/workbench/impact",
                "/api/workbench/text-lint", "/api/workbench/order-report",
                "/api/workbench/release-readiness",
            ],
            "editor_endpoints": [
                "/api/atlas/patch", "/api/atlas/apply",
                "/api/dialogue/patch", "/api/dialogue/apply",
                "/api/presentation/patch", "/api/presentation/apply",
                "/api/order/plan-move", "/api/order/apply-move",
                "/api/balance/patch", "/api/balance/apply",
            ],
            "module_areas": list(module_atlas.SOURCE_AREAS),
        }

    def dispatch(self, method: str, target: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        path, query = parse_request_target(target)
        checked_method = method.upper()
        if checked_method == "GET":
            return self._get(path, query)
        if checked_method == "POST":
            return self._post(path, require_object(body))
        raise StudioError("Only GET viewer requests and POST semantic plan/apply requests are supported.")

    def handle(self, method: str, target: str, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
        """Return an HTTP-ready payload without exposing implementation tracebacks."""

        try:
            result = self.dispatch(method, target, body)
            return HTTPStatus.OK, {"ok": True, "result": result}
        except StudioNotFound as error:
            return HTTPStatus.NOT_FOUND, {"ok": False, "error": str(error)}
        except (
            StudioError,
            module_atlas.ModuleAtlasError,
            dialogue_composer.DialogueComposerError,
            order_control.OrderControlError,
            presentation_layout.PresentationLayoutError,
            troop_item_balance.BalanceError,
            workbench.WorkbenchError,
        ) as error:
            return HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)}
        except Exception as error:  # pragma: no cover - protects the local UI from raw traces
            return HTTPStatus.INTERNAL_SERVER_ERROR, {
                "ok": False,
                "error": "The Studio operation failed unexpectedly; inspect the local server console for details.",
                "error_type": type(error).__name__,
            }

    def _get(self, path: str, query: Mapping[str, str]) -> dict[str, Any]:
        if path == "/api/health":
            return {
                "studio_version": f"devkit.module-studio.v{STUDIO_VERSION}",
                "status": "ready",
                "repository": self.root.name,
                "safety": self.catalog()["editing_policy"],
            }
        if path == "/api/catalog":
            return self.catalog()
        if path == "/api/summary":
            atlas = self.atlas()
            dialogues = self.dialogue()
            presentations = self.presentations()
            ordering = self.order()
            return {
                "studio_version": f"devkit.module-studio.v{STUDIO_VERSION}",
                "module_atlas": module_atlas.module_summary(atlas),
                "dialogue_composer": dialogue_composer.dialogue_summary(dialogues),
                "presentation_layout": presentation_layout.presentation_summary(presentations),
                "order_control": order_control.order_summary(ordering),
                "workbench_doctor": workbench.workbench_doctor(self.root),
                "warnings": [
                    "Studio summaries are static source/generated evidence, not an in-game simulation.",
                    "Use the specialist editor only after inspecting an entity/route/overlay context and a generated patch plan.",
                ],
            }
        if path == "/api/atlas/summary":
            return module_atlas.module_summary(self.atlas())
        if path == "/api/atlas/integrity":
            return module_atlas.module_integrity(self.atlas(), limit=optional_int(query.get("limit"), name="limit", default=100, minimum=1, maximum=500))
        if path == "/api/atlas/find":
            return module_atlas.module_find(
                self.atlas(),
                query=query_value(query, "query"),
                area=query.get("area", "all"),
                kind=query_value(query, "kind"),
                limit=optional_int(query.get("limit"), name="limit", default=30, minimum=1, maximum=200),
            )
        if path == "/api/atlas/entity":
            return module_atlas.module_context(self.atlas(), query_value(query, "id", required=True) or "")
        if path == "/api/atlas/graph":
            return module_atlas.module_graph(
                self.atlas(),
                query_value(query, "id", required=True) or "",
                direction=query.get("direction", "both"),
                depth=optional_int(query.get("depth"), name="depth", default=2, minimum=1, maximum=8),
                max_nodes=optional_int(query.get("max_nodes"), name="max_nodes", default=100, minimum=1, maximum=500),
            )
        if path == "/api/atlas/menu":
            return module_atlas.menu_flow(
                self.atlas(),
                query_value(query, "menu_id", required=True) or "",
                depth=optional_int(query.get("depth"), name="depth", default=2, minimum=1, maximum=8),
                max_nodes=optional_int(query.get("max_nodes"), name="max_nodes", default=100, minimum=1, maximum=500),
            )
        if path == "/api/atlas/script":
            return module_atlas.script_flow(
                self.atlas(),
                query_value(query, "script_name", required=True) or "",
                direction=query.get("direction", "both"),
                depth=optional_int(query.get("depth"), name="depth", default=2, minimum=1, maximum=8),
                max_nodes=optional_int(query.get("max_nodes"), name="max_nodes", default=120, minimum=1, maximum=500),
            )
        if path == "/api/atlas/mission":
            return module_atlas.mission_timeline(
                self.atlas(),
                query_value(query, "mission_id", required=True) or "",
                depth=optional_int(query.get("depth"), name="depth", default=2, minimum=1, maximum=8),
                max_nodes=optional_int(query.get("max_nodes"), name="max_nodes", default=120, minimum=1, maximum=500),
            )
        if path == "/api/atlas/triggers":
            return module_atlas.trigger_timeline(
                self.atlas(),
                query=query_value(query, "query"),
                limit=optional_int(query.get("limit"), name="limit", default=50, minimum=1, maximum=200),
            )
        if path == "/api/atlas/quests":
            return module_atlas.quest_registry(
                self.atlas(),
                query=query_value(query, "query"),
                limit=optional_int(query.get("limit"), name="limit", default=50, minimum=1, maximum=200),
            )
        if path == "/api/atlas/references":
            return module_atlas.entity_references(
                self.atlas(),
                query_value(query, "symbol", required=True) or "",
                limit=optional_int(query.get("limit"), name="limit", default=80, minimum=1, maximum=200),
            )
        if path == "/api/dialogue/summary":
            return dialogue_composer.dialogue_summary(self.dialogue())
        if path == "/api/dialogue/find":
            return dialogue_composer.dialogue_find(
                self.dialogue(),
                query=query_value(query, "query"),
                input_state=query_value(query, "input_state"),
                output_state=query_value(query, "output_state"),
                source=query_value(query, "source"),
                limit=optional_int(query.get("limit"), name="limit", default=30, minimum=1, maximum=200),
            )
        if path == "/api/dialogue/context":
            return dialogue_composer.dialogue_context(self.dialogue(), query_value(query, "route_id", required=True) or "")
        if path == "/api/presentation/summary":
            return presentation_layout.presentation_summary(self.presentations())
        if path == "/api/presentation/find":
            return presentation_layout.presentation_find(
                self.presentations(),
                query=query_value(query, "query", required=True) or "",
                limit=optional_int(query.get("limit"), name="limit", default=20, minimum=1, maximum=200),
            )
        if path == "/api/presentation/canvas":
            return presentation_layout.presentation_canvas(
                self.presentations(),
                query_value(query, "presentation_id", required=True) or "",
                width=optional_int(query.get("width"), name="width", default=1024, minimum=1, maximum=4096),
                height=optional_int(query.get("height"), name="height", default=768, minimum=1, maximum=4096),
                overlay_limit=optional_int(query.get("overlay_limit"), name="overlay_limit", default=200, minimum=1, maximum=1000),
            )
        if path == "/api/order/summary":
            return order_control.order_summary(self.order())
        if path == "/api/order/map":
            return order_control.order_map(
                self.order(),
                area=query.get("area", "all"),
                domain=query.get("domain", "all"),
                query=query_value(query, "query"),
                limit=optional_int(query.get("limit"), name="limit", default=60, minimum=1, maximum=500),
            )
        if path == "/api/order/explain":
            return order_control.order_explain(
                self.order(),
                query_value(query, "target", required=True) or "",
                related_limit=optional_int(query.get("related_limit"), name="related_limit", default=40, minimum=1, maximum=200),
            )
        if path == "/api/order/risk":
            return order_control.order_risk(
                self.order(),
                query_value(query, "target", required=True) or "",
                query_value(query, "anchor", required=True) or "",
                position=query.get("position", "before"),
            )
        if path == "/api/order/contracts":
            return order_control.order_contracts(self.order())
        if path == "/api/order/diff":
            return order_control.order_diff(
                self.order(),
                baseline=query_value(query, "baseline", required=True) or "",
                limit=optional_int(query.get("limit"), name="limit", default=100, minimum=1, maximum=500),
            )
        if path == "/api/order/verify":
            return order_control.order_verify(
                self.order(),
                baseline=query_value(query, "baseline"),
                limit=optional_int(query.get("limit"), name="limit", default=100, minimum=1, maximum=500),
            )
        if path == "/api/balance/summary":
            return troop_item_balance.balance_summary(self.balance())
        if path == "/api/balance/items":
            raw_merchandise = query.get("merchandise")
            if raw_merchandise in {None, "", "all"}:
                merchandise: bool | None = None
            else:
                merchandise = optional_boolean(raw_merchandise, name="merchandise", default=False)
            return troop_item_balance.balance_find_items(
                self.balance(),
                query=query_value(query, "query"),
                item_type=query.get("item_type", "all"),
                merchandise=merchandise,
                min_score=optional_int(query.get("min_score"), name="min_score", default=0, minimum=0, maximum=100_000) if query.get("min_score") not in {None, ""} else None,
                max_score=optional_int(query.get("max_score"), name="max_score", default=100_000, minimum=0, maximum=100_000) if query.get("max_score") not in {None, ""} else None,
                limit=optional_int(query.get("limit"), name="limit", default=60, minimum=1, maximum=500),
            )
        if path == "/api/balance/item":
            return troop_item_balance.balance_item(
                self.balance(),
                query_value(query, "item_id", required=True) or "",
                troop_limit=optional_int(query.get("troop_limit"), name="troop_limit", default=60, minimum=1, maximum=200),
            )
        if path == "/api/balance/troops":
            return troop_item_balance.balance_find_troops(
                self.balance(),
                query=query_value(query, "query"),
                faction=query_value(query, "faction"),
                role=query_value(query, "role"),
                include_heroes=optional_boolean(query.get("include_heroes"), name="include_heroes", default=True),
                min_level=optional_int(query.get("min_level"), name="min_level", default=0, minimum=0, maximum=255) if query.get("min_level") not in {None, ""} else None,
                max_level=optional_int(query.get("max_level"), name="max_level", default=255, minimum=0, maximum=255) if query.get("max_level") not in {None, ""} else None,
                limit=optional_int(query.get("limit"), name="limit", default=60, minimum=1, maximum=500),
            )
        if path == "/api/balance/troop":
            return troop_item_balance.balance_troop(
                self.balance(),
                query_value(query, "troop_id", required=True) or "",
                item_limit=optional_int(query.get("item_limit"), name="item_limit", default=80, minimum=1, maximum=200),
            )
        if path == "/api/balance/upgrade-tree":
            return troop_item_balance.balance_upgrade_tree(
                self.balance(),
                query_value(query, "troop_id", required=True) or "",
                depth=optional_int(query.get("depth"), name="depth", default=3, minimum=1, maximum=8),
                limit=optional_int(query.get("limit"), name="limit", default=120, minimum=1, maximum=300),
            )
        if path == "/api/balance/compare":
            raw_ids = query_value(query, "entity_ids", required=True) or ""
            entity_ids = [value.strip() for value in raw_ids.split(",") if value.strip()]
            return troop_item_balance.balance_compare(self.balance(), entity_ids)
        if path == "/api/balance/outliers":
            return troop_item_balance.balance_outliers(
                self.balance(),
                domain=query.get("domain", "all"),
                include_heroes=optional_boolean(query.get("include_heroes"), name="include_heroes", default=False),
                limit=optional_int(query.get("limit"), name="limit", default=100, minimum=1, maximum=500),
            )
        if path == "/api/balance/verify":
            return troop_item_balance.balance_verify(
                self.balance(),
                limit=optional_int(query.get("limit"), name="limit", default=100, minimum=1, maximum=500),
            )
        if path == "/api/workbench/doctor":
            return workbench.workbench_doctor(self.root)
        if path == "/api/workbench/summary":
            return workbench.workbench_summary(self.root)
        if path == "/api/workbench/impact":
            return workbench.workbench_impact(
                self.root,
                target=query_value(query, "target", required=True) or "",
                limit=optional_int(query.get("limit"), name="limit", default=12, minimum=1, maximum=100),
                include_text_evidence=query.get("include_text_evidence", "false") == "true",
            )
        if path == "/api/workbench/text-lint":
            return workbench.workbench_text_lint(
                self.root,
                query=query_value(query, "query"),
                kind=query.get("kind", "all"),
                severity=query.get("severity", "warning"),
                limit=optional_int(query.get("limit"), name="limit", default=50, minimum=1, maximum=200),
            )
        if path == "/api/workbench/order-report":
            return workbench.workbench_order_report(
                self.root,
                baseline=query_value(query, "baseline"),
                limit=optional_int(query.get("limit"), name="limit", default=100, minimum=1, maximum=500),
            )
        if path == "/api/workbench/release-readiness":
            return workbench.workbench_release_readiness(self.root, write_report=False)
        raise StudioNotFound(f"Unknown Studio viewer endpoint: {path}")

    def _post(self, path: str, body: Mapping[str, Any]) -> dict[str, Any]:
        if path == "/api/atlas/patch":
            return self._atlas_patch(body)
        if path == "/api/atlas/apply":
            return self._atlas_apply(body)
        if path == "/api/dialogue/patch":
            return self._dialogue_patch(body)
        if path == "/api/dialogue/apply":
            return self._dialogue_apply(body)
        if path == "/api/presentation/patch":
            return self._presentation_patch(body)
        if path == "/api/presentation/apply":
            return self._presentation_apply(body)
        if path == "/api/order/plan-move":
            return self._order_plan_move(body)
        if path == "/api/order/apply-move":
            return self._order_apply_move(body)
        if path == "/api/balance/patch":
            return self._balance_patch(body)
        if path == "/api/balance/apply":
            return self._balance_apply(body)
        raise StudioNotFound(f"Unknown Studio editor endpoint: {path}")

    def _atlas_arguments(self, body: Mapping[str, Any], *, include_apply: bool) -> tuple[str, str, dict[str, Any]]:
        allowed = {
            "entity_id", "action", "field", "block", "value", "operation", "position",
            "operation_index", "new_item", "allow_referenced_removal", "expected_sha256",
        }
        if include_apply:
            allowed.update({"dry_run", "confirmation", "removal_acknowledgement"})
        values = select_fields(body, allowed)
        entity_id = require_string(values.pop("entity_id", None), name="entity_id")
        action = require_string(values.pop("action", None), name="action")
        if values.get("allow_referenced_removal") is True and values.get("removal_acknowledgement") != REFERENCED_REMOVAL_CONFIRMATION:
            raise StudioError(
                "allow_referenced_removal=true requires removal_acknowledgement exactly equal to "
                f"{REFERENCED_REMOVAL_CONFIRMATION!r}."
            )
        values.pop("removal_acknowledgement", None)
        if include_apply:
            dry_run, expected_sha256 = apply_intent(values)
            values["dry_run"] = dry_run
            values["expected_sha256"] = expected_sha256
            values.pop("confirmation", None)
        return entity_id, action, values

    def _atlas_patch(self, body: Mapping[str, Any]) -> dict[str, Any]:
        entity_id, action, values = self._atlas_arguments(body, include_apply=False)
        return module_atlas.module_patch(self.atlas(), entity_id, action=action, **values)

    def _atlas_apply(self, body: Mapping[str, Any]) -> dict[str, Any]:
        entity_id, action, values = self._atlas_arguments(body, include_apply=True)
        return module_atlas.module_apply(self.atlas(), entity_id, action=action, **values)

    def _dialogue_arguments(self, body: Mapping[str, Any], *, include_apply: bool) -> tuple[str, str, dict[str, Any]]:
        allowed = {
            "route_id", "action", "value", "operation", "position", "operation_index",
            "new_route", "anchor_route_id", "expected_sha256",
        }
        if include_apply:
            allowed.update({"dry_run", "confirmation"})
        values = select_fields(body, allowed)
        route_id = require_string(values.pop("route_id", None), name="route_id")
        action = require_string(values.pop("action", None), name="action")
        if include_apply:
            dry_run, expected_sha256 = apply_intent(values)
            values["dry_run"] = dry_run
            values["expected_sha256"] = expected_sha256
            values.pop("confirmation", None)
        return route_id, action, values

    def _dialogue_patch(self, body: Mapping[str, Any]) -> dict[str, Any]:
        route_id, action, values = self._dialogue_arguments(body, include_apply=False)
        return dialogue_composer.dialogue_patch(self.dialogue(), route_id, action=action, **values)

    def _dialogue_apply(self, body: Mapping[str, Any]) -> dict[str, Any]:
        route_id, action, values = self._dialogue_arguments(body, include_apply=True)
        return dialogue_composer.dialogue_apply(self.dialogue(), route_id, action=action, **values)

    def _presentation_arguments(self, body: Mapping[str, Any], *, include_apply: bool) -> tuple[str, str, dict[str, Any]]:
        allowed = {
            "target", "action", "x", "y", "value", "alignment", "new_overlay",
            "new_trigger", "trigger", "expected_sha256",
        }
        if include_apply:
            allowed.update({"dry_run", "confirmation"})
        values = select_fields(body, allowed)
        target = require_string(values.pop("target", None), name="target")
        action = require_string(values.pop("action", None), name="action")
        if include_apply:
            dry_run, expected_sha256 = apply_intent(values)
            values["dry_run"] = dry_run
            values["expected_sha256"] = expected_sha256
            values.pop("confirmation", None)
        return target, action, values

    def _presentation_patch(self, body: Mapping[str, Any]) -> dict[str, Any]:
        target, action, values = self._presentation_arguments(body, include_apply=False)
        return presentation_layout.presentation_patch(self.presentations(), target, action=action, **values)

    def _presentation_apply(self, body: Mapping[str, Any]) -> dict[str, Any]:
        target, action, values = self._presentation_arguments(body, include_apply=True)
        return presentation_layout.presentation_apply(self.presentations(), target, action=action, **values)

    def _order_move_arguments(self, body: Mapping[str, Any], *, include_apply: bool) -> tuple[str, str, str, dict[str, Any]]:
        allowed = {"target", "anchor", "position", "expected_sha256", "allow_protected_contract_change"}
        if include_apply:
            allowed.update({"dry_run", "confirmation"})
        values = select_fields(body, allowed)
        target = require_string(values.pop("target", None), name="target")
        anchor = require_string(values.pop("anchor", None), name="anchor")
        position = require_string(values.pop("position", None), name="position", maximum=20)
        if include_apply:
            dry_run, expected_sha256 = apply_intent(values)
            values["dry_run"] = dry_run
            values["expected_sha256"] = expected_sha256
            values.pop("confirmation", None)
        return target, anchor, position, values

    def _order_plan_move(self, body: Mapping[str, Any]) -> dict[str, Any]:
        target, anchor, position, values = self._order_move_arguments(body, include_apply=False)
        return order_control.order_plan_move(self.order(), target, anchor, position=position, **values)

    def _order_apply_move(self, body: Mapping[str, Any]) -> dict[str, Any]:
        target, anchor, position, values = self._order_move_arguments(body, include_apply=True)
        return order_control.order_apply_move(self.order(), target, anchor, position=position, **values)

    def _balance_arguments(self, body: Mapping[str, Any], *, include_apply: bool) -> tuple[str, str, dict[str, Any]]:
        allowed = {"entity_kind", "entity_id", "changes"}
        if include_apply:
            allowed.update(
                {
                    "expected_sha256",
                    "expected_plan_sha256",
                    "dry_run",
                    "confirmation",
                    "allow_legacy_compile_authoring",
                    "allow_protected_legacy_record_change",
                }
            )
        values = select_fields(body, allowed)
        entity_kind = require_string(values.pop("entity_kind", None), name="entity_kind", maximum=40)
        entity_id = require_string(values.pop("entity_id", None), name="entity_id", maximum=180)
        values["changes"] = require_object(values.get("changes"), name="changes")
        if include_apply:
            dry_run, expected_sha256 = apply_intent(values)
            values["dry_run"] = dry_run
            values["expected_sha256"] = expected_sha256
            values["expected_plan_sha256"] = require_string(values.get("expected_plan_sha256"), name="expected_plan_sha256", maximum=128)
            values.pop("confirmation", None)
        return entity_kind, entity_id, values

    def _balance_patch(self, body: Mapping[str, Any]) -> dict[str, Any]:
        entity_kind, entity_id, values = self._balance_arguments(body, include_apply=False)
        return troop_item_balance.balance_patch(self.balance(), entity_kind, entity_id, **values)

    def _balance_apply(self, body: Mapping[str, Any]) -> dict[str, Any]:
        entity_kind, entity_id, values = self._balance_arguments(body, include_apply=True)
        return troop_item_balance.balance_apply(self.balance(), entity_kind, entity_id, **values)


class StudioRequestHandler(BaseHTTPRequestHandler):
    """Serve the optional static UI and JSON service without CORS or uploads."""

    protocol_version = "HTTP/1.1"
    service: StudioService

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("[module-studio] " + format % args + "\n")

    def do_GET(self) -> None:  # noqa: N802 - HTTP handler API
        if not self._loopback_client():
            return
        if urlsplit(self.path).path.startswith("/api/"):
            self._json_response(*self.service.handle("GET", self.path))
            return
        self._static_response()

    def do_POST(self) -> None:  # noqa: N802 - HTTP handler API
        if not self._loopback_client():
            return
        if not urlsplit(self.path).path.startswith("/api/"):
            self._json_response(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Unknown Studio endpoint."})
            return
        content_type = self.headers.get("Content-Type", "")
        if not content_type.lower().startswith("application/json"):
            self._json_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"ok": False, "error": "POST bodies must use application/json."})
            return
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if length < 0 or length > MAX_BODY_BYTES:
            self._json_response(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"ok": False, "error": "JSON body exceeds the 1 MiB Studio safety limit."})
            return
        try:
            decoded = self.rfile.read(length).decode("utf-8")
            body = json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json_response(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "POST body must be valid UTF-8 JSON."})
            return
        self._json_response(*self.service.handle("POST", self.path, body))

    def _loopback_client(self) -> bool:
        if self.client_address[0] == "127.0.0.1":
            return True
        self._json_response(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Module Studio accepts loopback clients only."})
        return False

    def _static_response(self) -> None:
        path = unquote(urlsplit(self.path).path)
        names = {
            "/": "index.html",
            "/index.html": "index.html",
            "/app.js": "app.js",
            "/styles.css": "styles.css",
        }
        name = names.get(path)
        if name is None:
            self._json_response(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Unknown Studio asset."})
            return
        asset = WEB_ROOT / name
        try:
            raw = asset.read_bytes()
        except OSError:
            self._json_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": "Studio static asset is unavailable."})
            return
        content_type = {
            "index.html": "text/html; charset=utf-8",
            "app.js": "text/javascript; charset=utf-8",
            "styles.css": "text/css; charset=utf-8",
        }[name]
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(raw)

    def _json_response(self, status: int | HTTPStatus, payload: Mapping[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(raw)


def make_server(root: Path, *, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    checked_host = require_loopback_host(host)
    checked_port = require_port(port)
    service = StudioService(root)

    class BoundStudioRequestHandler(StudioRequestHandler):
        pass

    BoundStudioRequestHandler.service = service
    return ThreadingHTTPServer((checked_host, checked_port), BoundStudioRequestHandler)


def print_payload(payload: Mapping[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Loopback-only optional visual Studio for the SoD Modern DevKit.")
    parser.add_argument("command", nargs="?", choices=("serve", "catalog", "summary"), default="serve", help="serve (default), catalog, or summary")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Module workspace root (defaults to this repository).")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Must remain exactly 127.0.0.1.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Local TCP port (default: 8797).")
    arguments = parser.parse_args(argv)
    root = Path(arguments.root).resolve()
    if not root.is_dir():
        parser.error(f"Workspace root does not exist: {root}")
    command = arguments.command
    service = StudioService(root)
    if command in {"catalog", "summary"}:
        status, payload = service.handle("GET", f"/api/{command}")
        print_payload(payload)
        return 0 if int(status) < 400 else 2
    try:
        server = make_server(root, host=arguments.host, port=arguments.port)
    except (OSError, StudioError) as error:
        sys.stderr.write(f"Module Studio could not start: {error}\n")
        return 2
    url = f"http://{arguments.host}:{arguments.port}/"
    sys.stdout.write("SoD Module Studio is ready (loopback only).\n")
    sys.stdout.write(f"Open manually: {url}\n")
    sys.stdout.write("Press Ctrl+C to stop. The Studio never builds or exports module data.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.stdout.write("\nModule Studio stopped.\n")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
