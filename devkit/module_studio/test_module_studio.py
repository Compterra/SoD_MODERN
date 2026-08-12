"""Fixture tests for the loopback-only Module Studio adapter.

The Studio must stay a thin UI/API layer over the specialist DevKit tools.  A
small eight-area module lets this test prove viewer routes, patch plans, SHA
dry-runs, and the explicit non-dry confirmation gate without changing the
live SoD source tree.
"""

from __future__ import annotations

import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.module_atlas import module_atlas
from devkit.module_atlas.test_module_atlas import FIXTURES, make_workspace
from devkit.module_studio import module_studio
from devkit.presentation_layout.test_presentation_layout import SOURCE as PRESENTATION_SOURCE
from devkit.presentation_layout.test_presentation_layout import make_workspace as make_presentation_workspace
from devkit.troop_item_balance.test_troop_item_balance import make_workspace as make_balance_workspace
from devkit.workbench.test_workbench import make_workbench_config


def expect_ok(service: module_studio.StudioService, target: str) -> dict[str, object]:
    status, payload = service.handle("GET", target)
    assert int(status) == 200, payload
    assert payload["ok"] is True
    return payload["result"]


def expect_post_ok(service: module_studio.StudioService, target: str, body: dict) -> dict[str, object]:
    status, payload = service.handle("POST", target, body)
    assert int(status) == 200, payload
    assert payload["ok"] is True
    return payload["result"]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="module-studio-") as temporary:
        root = Path(temporary)
        make_workspace(root)
        make_workbench_config(root)
        service = module_studio.StudioService(root)

        health = expect_ok(service, "/api/health")
        assert health["status"] == "ready"
        catalog = expect_ok(service, "/api/catalog")
        assert catalog["bind_policy"]["network"] == "loopback-only"
        assert "/api/atlas/patch" in catalog["editor_endpoints"]
        assert "/api/order/explain" in catalog["viewer_endpoints"]
        assert "/api/order/plan-move" in catalog["editor_endpoints"]
        summary = expect_ok(service, "/api/summary")
        assert summary["module_atlas"]["entity_count"] == 11
        assert summary["order_control"]["contracts"]["active_blocker_count"] == 0

        order_summary = expect_ok(service, "/api/order/summary")
        assert order_summary["source_fragment_order"]["area_count"] == 8

        found = expect_ok(service, "/api/atlas/find?area=menus&query=fixture")
        menu = next(item for item in found["entities"] if item["kind"] == "menu")
        context = expect_ok(service, "/api/atlas/entity?id=" + menu["entity_id"])
        assert context["entity"]["name"] == "fixture_menu"
        graph = expect_ok(service, "/api/atlas/graph?id=" + menu["entity_id"] + "&depth=2")
        assert graph["node_count"] >= 2
        flow = expect_ok(service, "/api/atlas/menu?menu_id=fixture_menu")
        assert flow["options"][0]["name"].endswith(":continue")

        dialogue = expect_ok(service, "/api/dialogue/find?input_state=fixture_state")
        route = dialogue["routes"][0]
        route_context = expect_ok(service, "/api/dialogue/context?route_id=" + route["route_id"])
        assert route_context["route"]["input_state"] == "fixture_state"

        presentations = expect_ok(service, "/api/presentation/find?query=fixture_presentation")
        presentation = presentations["presentations"][0]
        canvas = expect_ok(service, "/api/presentation/canvas?presentation_id=" + presentation["presentation_key"])
        assert canvas["presentation"]["presentation_id"] == "fixture_presentation"

        status, plan_envelope = service.handle(
            "POST",
            "/api/atlas/patch",
            {"entity_id": menu["entity_id"], "action": "set_text", "value": "@Changed through Studio"},
        )
        assert int(status) == 200, plan_envelope
        plan = plan_envelope["result"]
        assert "@Changed through Studio" in plan["change_router_plan"]["unified_diff"]
        sha = plan["change_router_plan"]["target"]["base_sha256"]

        status, rehearsal = service.handle(
            "POST",
            "/api/atlas/apply",
            {
                "entity_id": menu["entity_id"],
                "action": "set_text",
                "value": "@Changed through Studio",
                "expected_sha256": sha,
                "dry_run": True,
            },
        )
        assert int(status) == 200, rehearsal
        assert rehearsal["result"]["result"]["applied"] is False
        assert (root / "src/menus/0001_fixture/fixture_menu.py").read_text(encoding="utf-8") == FIXTURES["menus/0001_fixture/fixture_menu.py"]

        status, refused = service.handle(
            "POST",
            "/api/atlas/apply",
            {
                "entity_id": menu["entity_id"],
                "action": "set_text",
                "value": "@Changed through Studio",
                "expected_sha256": sha,
                "dry_run": False,
            },
        )
        assert int(status) == 400
        assert "confirmation" in refused["error"]

        status, unknown = service.handle("POST", "/api/atlas/patch", {"entity_id": menu["entity_id"], "action": "set_text", "command": "nope"})
        assert int(status) == 400
        assert "Unknown request field" in unknown["error"]
        status, unknown_path = service.handle("GET", "/api/not-a-real-viewer")
        assert int(status) == 404
        assert unknown_path["ok"] is False
        try:
            module_studio.require_loopback_host("0.0.0.0")
        except module_studio.StudioError:
            pass
        else:
            raise AssertionError("Studio must refuse non-loopback binds.")

        # Proves our selected ID really remains one of the Atlas's semantic IDs.
        assert module_atlas.require_entity(module_atlas.build_module_atlas(root), menu["entity_id"]).name == "fixture_menu"

    with tempfile.TemporaryDirectory(prefix="module-studio-balance-") as temporary:
        root = Path(temporary)
        make_balance_workspace(root)
        service = module_studio.StudioService(root)
        catalog = expect_ok(service, "/api/catalog")
        assert "/api/balance/troop" in catalog["viewer_endpoints"]
        assert "/api/balance/patch" in catalog["editor_endpoints"]
        balance_summary = expect_ok(service, "/api/balance/summary")
        assert balance_summary["authoring"]["confirmed"] is True
        balance_items = expect_ok(service, "/api/balance/items?query=fixture&limit=5")
        sword = next(item for item in balance_items["items"] if item["code"] == "fixture_sword")
        item_context = expect_ok(service, "/api/balance/item?item_id=" + sword["item_id"])
        assert item_context["item"]["stats"]["swing_damage"]["amount"] == 40
        troop_context = expect_ok(service, "/api/balance/troop?troop_id=trp_fixture_recruit")
        assert troop_context["troop"]["upgrades_to"] == ["trp_fixture_veteran"]
        outliers = expect_ok(service, "/api/balance/outliers?domain=items&limit=5")
        assert outliers["finding_count"] >= 1

        status, balance_plan_envelope = service.handle(
            "POST",
            "/api/balance/patch",
            {"entity_kind": "item", "entity_id": sword["item_id"], "changes": {"price": 125}},
        )
        assert int(status) == 200, balance_plan_envelope
        balance_plan = balance_plan_envelope["result"]
        assert balance_plan["unified_diff"]
        status, balance_rehearsal = service.handle(
            "POST",
            "/api/balance/apply",
            {
                "entity_kind": "item",
                "entity_id": sword["item_id"],
                "changes": {"price": 125},
                "expected_sha256": balance_plan["target"]["base_sha256"],
                "expected_plan_sha256": balance_plan["plan_sha256"],
                "dry_run": True,
            },
        )
        assert int(status) == 200, balance_rehearsal
        assert balance_rehearsal["result"]["applied"] is False
        status, refused = service.handle(
            "POST",
            "/api/balance/apply",
            {
                "entity_kind": "item",
                "entity_id": sword["item_id"],
                "changes": {"price": 125},
                "expected_sha256": balance_plan["target"]["base_sha256"],
                "expected_plan_sha256": balance_plan["plan_sha256"],
                "dry_run": False,
            },
        )
        assert int(status) == 400
        assert "confirmation" in refused["error"]

    # The visual Presentation Workshop is a thin client over these same
    # source-safe endpoints.  Exercise the direct-overlay data needed by its
    # selectable canvas, drag/move plan, and create-overlay form without
    # needing a browser or touching the real module source.
    with tempfile.TemporaryDirectory(prefix="module-studio-presentation-") as temporary:
        root = Path(temporary)
        make_presentation_workspace(root)
        service = module_studio.StudioService(root)
        catalog = expect_ok(service, "/api/catalog")
        assert "/api/presentation/canvas" in catalog["viewer_endpoints"]
        assert "/api/presentation/patch" in catalog["editor_endpoints"]
        found = expect_ok(service, "/api/presentation/find?query=fixture")
        presentation = found["presentations"][0]
        assert expect_ok(service, "/api/presentation/find?query=*")["match_count"] == 1
        canvas = expect_ok(
            service,
            "/api/presentation/canvas?presentation_id=" + presentation["presentation_key"] + "&overlay_limit=500",
        )
        assert canvas["canvas"]["returned_overlay_count"] == 1
        status, invalid_canvas_limit = service.handle(
            "GET",
            "/api/presentation/canvas?presentation_id=" + presentation["presentation_key"] + "&overlay_limit=0",
        )
        assert int(status) == 400
        assert "overlay_limit" in invalid_canvas_limit["error"]
        overlay = canvas["canvas"]["overlays"][0]
        assert overlay["canvas_box"] is not None
        assert overlay["position"]["x"]["value"] == 100
        # The workshop must retain a register-backed label as provenance, not
        # offer the register name as editable literal presentation text.
        assert overlay["content"] == "s68"
        assert overlay["content_is_literal"] is False
        assert overlay["content_literal"] is None

        status, move_plan_envelope = service.handle(
            "POST",
            "/api/presentation/patch",
            {"target": overlay["overlay_id"], "action": "move_overlay", "x": 125, "y": 225},
        )
        assert int(status) == 200, move_plan_envelope
        move_plan = move_plan_envelope["result"]
        assert "125" in move_plan["change_router_plan"]["unified_diff"]
        sha = move_plan["change_router_plan"]["target"]["base_sha256"]

        status, rehearsal = service.handle(
            "POST",
            "/api/presentation/apply",
            {
                "target": overlay["overlay_id"],
                "action": "move_overlay",
                "x": 125,
                "y": 225,
                "expected_sha256": sha,
                "dry_run": True,
            },
        )
        assert int(status) == 200, rehearsal
        assert rehearsal["result"]["result"]["applied"] is False
        assert (root / "src/presentations/0001_fixture/fixture_presentation.py").read_text(encoding="utf-8") == PRESENTATION_SOURCE

        status, create_plan_envelope = service.handle(
            "POST",
            "/api/presentation/patch",
            {
                "target": presentation["presentation_key"],
                "action": "add_overlay",
                "trigger": "ti_on_presentation_load",
                "new_overlay": {
                    "kind": "text",
                    "destination": "$g_studio_created",
                    "text": "@Studio created",
                    "position_register": "pos2",
                    "x": 480,
                    "y": 520,
                    "size_x": 400,
                    "size_y": 250,
                },
            },
        )
        assert int(status) == 200, create_plan_envelope
        assert "create_text_overlay" in create_plan_envelope["result"]["change_router_plan"]["unified_diff"]

        status, refused = service.handle(
            "POST",
            "/api/presentation/apply",
            {
                "target": overlay["overlay_id"],
                "action": "move_overlay",
                "x": 125,
                "y": 225,
                "expected_sha256": sha,
                "dry_run": False,
            },
        )
        assert int(status) == 400
        assert "confirmation" in refused["error"]

    # Content Forge is intentionally exercised against the real checked-in
    # DevKit contract because its full typed entrypoint catalog is itself the
    # feature under test. These calls remain read-only: the Studio should
    # expose visual-pack data and a catalog *plan*, never a generic writer.
    content_service = module_studio.StudioService(REPO_ROOT)
    content_summary = expect_ok(content_service, "/api/content/summary?limit=5")
    assert content_summary["pack_count"] >= 1
    content_pack_id = content_summary["packs"][0]["id"]
    content_explain = expect_ok(content_service, "/api/content/explain?pack_id=" + content_pack_id)
    assert content_explain["pack_source"]["id"] == content_pack_id
    content_preview = expect_post_ok(content_service, "/api/content/preview", {"pack": content_explain["pack_source"]})
    assert "review_canvas" in content_preview
    content_plan = expect_post_ok(content_service, "/api/content/plan", {"pack": content_explain["pack_source"]})
    assert content_plan["state"] in {"ready_for_review", "blocked"}
    catalog_draft = dict(content_explain["pack_source"])
    catalog_draft["description"] = catalog_draft["description"] + " [Studio catalog-plan coverage]"
    catalog_plan = expect_post_ok(
        content_service,
        "/api/content/catalog-plan",
        {"pack": catalog_draft, "mode": "replace"},
    )
    assert catalog_plan["catalog_target"]["path"] == "devkit/content_forge/packs.json"
    catalog_rehearsal = expect_post_ok(
        content_service,
        "/api/content/catalog-apply",
        {
            "pack": catalog_draft,
            "mode": "replace",
            "expected_catalog_plan_id": catalog_plan["catalog_plan_id"],
            "expected_catalog_sha256": catalog_plan["catalog_target"]["base_sha256"],
            "dry_run": True,
        },
    )
    assert catalog_rehearsal["applied"] is False
    assert catalog_rehearsal["catalog_plan"]["catalog_plan_id"] == catalog_plan["catalog_plan_id"]

    print("test_module_studio: OK")


if __name__ == "__main__":
    main()
