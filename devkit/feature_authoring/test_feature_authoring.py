"""Focused fixture coverage for the Feature Authoring Compiler."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.feature_authoring import feature_authoring as compiler


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def blueprint_catalog() -> dict[str, object]:
    return {
        "schema": "sod-modern.module-blueprint-catalog.v1",
        "blueprints": [
            {
                "id": "fixture-feature",
                "name": "Fixture Feature",
                "status": "active",
                "description": "Fixture ownership contract for the Feature Authoring Compiler.",
                "source_fragments": [
                    "src/scripts/feature.py",
                    "src/menus/feature.py",
                    "src/dialogs/feature.py",
                    "src/presentations/feature.py",
                ],
                "required_symbols": [
                    {"symbol": "script_feature_anchor", "area": "scripts", "kind": "script"},
                    {"symbol": "mnu_feature_menu", "area": "menus", "kind": "menu"},
                ],
                "source_assertions": [
                    {"id": "feature-script", "path": "src/scripts/feature.py", "contains": "feature_anchor"},
                ],
                "order_constraints": [],
                "slot_ownership_rules": [],
                "ai_contracts": [],
                "tests": ["build/test_fixture_feature.py"],
                "depends_on": [],
            }
        ],
    }


def feature_catalog() -> dict[str, object]:
    return {
        "schema": compiler.FEATURE_CATALOG_SCHEMA,
        "features": [
            {
                "schema": compiler.FEATURE_INTENT_SCHEMA,
                "id": "fixture-feature",
                "title": "Fixture Feature",
                "status": "active",
                "description": "Typed source edits spanning module scripts, dialogue, and presentation layout.",
                "blueprint_id": "fixture-feature",
                "entrypoints": [
                    "entrypoint:script:feature_anchor",
                    "entrypoint:menu:feature_menu",
                    "entrypoint:dialogue-state:start",
                    "entrypoint:presentation:feature_presentation",
                ],
                "changes": [
                    {
                        "kind": "module",
                        "target": "entrypoint:script:feature_anchor",
                        "action": "insert_operation",
                        "block": "operations",
                        "position": "end",
                        "operation": {
                            "op": "assign",
                            "args": [{"local": "feature_added"}, 2],
                        },
                    },
                    {
                        "kind": "dialogue",
                        "target": "entrypoint:dialogue-state:start",
                        "action": "replace_text",
                        "route": {"text": "@Hello"},
                        "text": "@Updated",
                    },
                    {
                        "kind": "presentation",
                        "target": "entrypoint:presentation:feature_presentation",
                        "action": "set_text",
                        "overlay": {"identifier": "$g_feature_overlay"},
                        "text": "@Updated overlay",
                    },
                ],
                "verification": {
                    "tests": ["build/test_fixture_feature.py"],
                    "require_blueprint": True,
                },
            }
        ],
    }


def make_fixture(root: Path) -> None:
    (root / "compile").mkdir(parents=True, exist_ok=True)
    write(
        root / "src/scripts/feature.py",
        "SCRIPTS = [\n"
        "  (\"feature_anchor\", [\n"
        "    (assign, \":value\", 1),\n"
        "  ]),\n"
        "]\n",
    )
    write(
        root / "src/menus/feature.py",
        "MENUS = [\n"
        "  (\"feature_menu\", 0, \"@Feature\", \"none\", [], [\n"
        "    (\"feature_menu_option\", [], \"@Option\", []),\n"
        "  ]),\n"
        "]\n",
    )
    write(
        root / "src/dialogs/feature.py",
        "DIALOGS = [\n"
        "  [anyone, \"start\", [], \"@Hello\", \"close_window\", []],\n"
        "]\n",
    )
    write(
        root / "src/presentations/feature.py",
        "PRESENTATIONS = [\n"
        "  (\"feature_presentation\", 0, mesh_load_window, [\n"
        "    (ti_on_presentation_load, [\n"
        "      (create_text_overlay, \"$g_feature_overlay\", \"@Old\"),\n"
        "      (position_set_x, pos1, 100),\n"
        "      (position_set_y, pos1, 200),\n"
        "      (overlay_set_position, \"$g_feature_overlay\", pos1),\n"
        "    ]),\n"
        "  ]),\n"
        "]\n",
    )
    write(root / "build/test_fixture_feature.py", "# Feature Authoring fixture test.\n")
    write(root / compiler.ENTRYPOINT_CATALOG_RELATIVE, (TOOL_DIR / "entrypoints.json").read_text(encoding="utf-8"))
    write(root / compiler.FEATURE_CATALOG_RELATIVE, json.dumps(feature_catalog(), indent=2) + "\n")
    write(root / "devkit/module_blueprint/blueprints.json", json.dumps(blueprint_catalog(), indent=2) + "\n")


def test_registry_plan_and_source_apply() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        make_fixture(root)
        index = compiler.build_feature_authoring(root)
        summary = compiler.feature_summary(index)
        assert summary["feature_count"] == 1
        found = compiler.entrypoint_find(index, "feature_anchor", family="script")
        assert found["match_count"] == 1
        explained = compiler.entrypoint_explain(index, "entrypoint:script:feature_anchor")
        assert explained["static_execution_trace"]["kind"] == "script_flow"
        validation = compiler.feature_intent_validate(index, feature_id="fixture-feature")
        assert validation["state"] == "ready", validation
        plan = compiler.feature_plan(index, feature_id="fixture-feature", trace_limit=2)
        assert plan["state"] == "ready_for_review", plan
        assert plan["change_count"] == 3
        assert {item["kind"] for item in plan["change_plans"]} == {"module", "dialogue", "presentation"}
        before = compiler.feature_semantic_snapshot(index, feature_id="fixture-feature")
        script_change = next(item for item in plan["change_plans"] if item["kind"] == "module")
        applied = compiler.feature_apply(
            index,
            feature_id="fixture-feature",
            change_id=script_change["change_id"],
            expected_feature_plan_id=plan["plan_id"],
            expected_sha256=script_change["change_router_plan"]["target"]["base_sha256"],
            dry_run=False,
        )
        assert applied["result"]["applied"] is True
        assert "feature_added" in (root / "src/scripts/feature.py").read_text(encoding="utf-8")
        refreshed = compiler.build_feature_authoring(root)
        changed = compiler.feature_semantic_diff(refreshed, before, feature_id="fixture-feature")
        assert changed["state"] == "changed"


def test_deterministic_dialogue_creation_and_presentation_addition_plan() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        make_fixture(root)
        index = compiler.build_feature_authoring(root)
        dialogue_intent = {
            "schema": compiler.FEATURE_INTENT_SCHEMA,
            "id": "fixture-dialogue-create",
            "title": "Fixture dialogue create",
            "status": "draft",
            "description": "A deterministic player choice anchored after one known route.",
            "entrypoints": ["entrypoint:dialogue-state:start"],
            "changes": [
                {
                    "kind": "dialogue",
                    "target": "entrypoint:dialogue-state:start",
                    "action": "create_route",
                    "anchor": {"text": "@Hello"},
                    "position": "after",
                    "speaker": {"symbol": "plyr"},
                    "text": "@A deterministic feature choice.",
                    "output_state": "close_window",
                    "conditions": [],
                    "consequences": [],
                }
            ],
            "verification": {"tests": ["build/test_fixture_feature.py"], "require_blueprint": False},
        }
        dialogue_plan = compiler.feature_plan(index, intent_value=dialogue_intent)
        assert dialogue_plan["state"] == "ready_for_review", dialogue_plan
        safety = dialogue_plan["change_plans"][0]["semantic_operation"]["static_creation_safety"]
        assert any(item["code"] == "PLAYER_CHOICE_GROUP" for item in safety["warnings"])

        presentation_intent = {
            "schema": compiler.FEATURE_INTENT_SCHEMA,
            "id": "fixture-presentation-add",
            "title": "Fixture presentation add",
            "status": "draft",
            "description": "Add a typed text overlay to a known presentation load callback.",
            "entrypoints": ["entrypoint:presentation:feature_presentation"],
            "changes": [
                {
                    "kind": "presentation",
                    "target": "entrypoint:presentation:feature_presentation",
                    "action": "add_overlay",
                    "trigger": "ti_on_presentation_load",
                    "new_overlay": {
                        "kind": "text",
                        "destination": {"global": "feature_added_overlay"},
                        "position_register": "pos2",
                        "x": 500,
                        "y": 600,
                        "text": "@Feature overlay",
                    },
                }
            ],
            "verification": {"tests": ["build/test_fixture_feature.py"], "require_blueprint": False},
        }
        presentation_plan = compiler.feature_plan(index, intent_value=presentation_intent)
        assert presentation_plan["state"] == "ready_for_review", presentation_plan
        assert "create_text_overlay" in presentation_plan["change_plans"][0]["change_router_plan"]["unified_diff"]


def test_typed_ir_rejects_raw_python_and_renders_safe_operations() -> None:
    assert compiler.render_operation({"op": "call_script", "args": [{"reference": "script_feature_anchor"}]}) == '(call_script, "script_feature_anchor")'
    assert compiler.render_operation({"op": "eq", "negated": True, "args": [{"global": "feature_flag"}, 1]}) == '(neg|eq, "$feature_flag", 1)'
    try:
        compiler.render_operation({"op": "assign", "args": [{"symbol": "__import__('os')"}, 1]})
    except compiler.FeatureAuthoringError as error:
        assert "identifier" in str(error)
    else:
        raise AssertionError("Raw Python expression escaped typed IR validation.")


if __name__ == "__main__":
    test_registry_plan_and_source_apply()
    test_deterministic_dialogue_creation_and_presentation_addition_plan()
    test_typed_ir_rejects_raw_python_and_renders_safe_operations()
    print("test_feature_authoring: OK")
