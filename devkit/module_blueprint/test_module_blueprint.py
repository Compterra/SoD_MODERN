"""Focused fixture tests for the read-only Module Blueprint Compiler."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.change_router import change_router
from devkit.module_atlas import module_atlas
from devkit.module_blueprint import module_blueprint as compiler


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def fixture_catalog(*, broken_assertion: bool = False) -> dict[str, object]:
    assertion = "missing_anchor" if broken_assertion else "script_blueprint_feature"
    return {
        "schema": compiler.CATALOG_SCHEMA,
        "blueprints": [
            {
                "id": "fixture-helper",
                "name": "Fixture Helper",
                "status": "active",
                "description": "Owns the helper and feature script API for a Blueprint fixture.",
                "source_fragments": ["src/scripts/feature.py"],
                "required_symbols": [
                    {"symbol": "script_blueprint_helper", "area": "scripts", "kind": "script"}
                ],
                "source_assertions": [
                    {"id": "helper-api", "path": "src/scripts/feature.py", "contains": "blueprint_helper"}
                ],
                "order_constraints": [],
                "slot_ownership_rules": [],
                "ai_contracts": [],
                "tests": ["build/test_fixture_feature.py"],
                "depends_on": [],
            },
            {
                "id": "fixture-main",
                "name": "Fixture Main",
                "status": "active",
                "description": "Exercises an ordered trigger feature that depends on a declared script API.",
                "source_fragments": ["src/triggers/later.py"],
                "required_symbols": [
                    {"symbol": "script_blueprint_feature", "area": "scripts", "kind": "script"}
                ],
                "source_assertions": [
                    {"id": "trigger-call", "path": "src/triggers/later.py", "contains": assertion}
                ],
                "order_constraints": [
                    {
                        "id": "later-after-early",
                        "target": "source:src/triggers/later.py",
                        "relation": "after",
                        "anchor": "source:src/triggers/early.py",
                        "reason": "The feature trigger consumes state prepared by the early trigger.",
                    }
                ],
                "slot_ownership_rules": [],
                "ai_contracts": [],
                "tests": ["build/test_fixture_feature.py"],
                "depends_on": ["fixture-helper"],
            },
        ],
    }


def make_fixture(root: Path, *, broken_assertion: bool = False) -> Path:
    write(
        root / "src/scripts/feature.py",
        "SCRIPTS = [\n"
        "  (\"blueprint_helper\", [(assign, \":value\", 1)]),\n"
        "  (\"blueprint_feature\", [(call_script, \"script_blueprint_helper\")]),\n"
        "]\n",
    )
    write(
        root / "src/triggers/early.py",
        "SIMPLE_TRIGGERS = [(1, [(assign, \":prepared\", 1)])]\n",
    )
    write(
        root / "src/triggers/later.py",
        "SIMPLE_TRIGGERS = [(1, [(call_script, \"script_blueprint_feature\")])]\n",
    )
    write(root / "src/triggers/_order_simple_triggers.txt", "early.py\nlater.py\n")
    (root / "compile").mkdir(parents=True, exist_ok=True)
    write(root / "build/test_fixture_feature.py", "# Registered fixture test; Blueprint Compiler never executes it.\n")
    catalog_path = root / compiler.CATALOG_RELATIVE
    write(catalog_path, json.dumps(fixture_catalog(broken_assertion=broken_assertion), indent=2) + "\n")
    return catalog_path


def build(root: Path):
    return compiler.build_module_blueprints(root)


def test_ready_dependency_plan() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        make_fixture(root)
        index = build(root)
        summary = compiler.blueprint_summary(index)
        assert summary["verification"]["state"] == "ready_for_review", summary
        plan = compiler.blueprint_compile(index, "fixture-main")
        assert plan["state"] == "ready_for_review", plan
        assert plan["dependency_order"] == ["fixture-helper", "fixture-main"]
        assert [row["path"] for row in plan["source_plan"]["fragments"]] == [
            "src/scripts/feature.py",
            "src/triggers/later.py",
        ]
        assert plan["source_apply"]["available"] is False
        assert all(row["execution"] == "not_run_by_blueprint_compiler" for row in plan["test_plan"])


def test_order_violation_blocks_the_feature() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        make_fixture(root)
        write(root / "src/triggers/_order_simple_triggers.txt", "later.py\nearly.py\n")
        change_router.invalidate_router(root)
        module_atlas.invalidate_atlas(root)
        verification = compiler.blueprint_verify(build(root), "fixture-main")
        assert verification["state"] == "blocked", verification
        assert any(item["code"] == "order_constraint_failed" for item in verification["findings"])


def test_missing_literal_anchor_blocks_the_feature() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        make_fixture(root, broken_assertion=True)
        verification = compiler.blueprint_verify(build(root), "fixture-main")
        assert verification["state"] == "blocked", verification
        assert any(item["code"] == "source_assertion_failed" for item in verification["findings"])


def test_targeted_draft_verification_does_not_hide_its_own_errors() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        catalog_path = make_fixture(root, broken_assertion=True)
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        payload["blueprints"][1]["status"] = "draft"
        write(catalog_path, json.dumps(payload, indent=2) + "\n")
        verification = compiler.blueprint_verify(build(root), "fixture-main")
        assert verification["state"] == "blocked", verification
        assert verification["active_error_count"] == 0
        assert verification["blocking_error_count"] == 1


def test_invalid_dependency_is_rejected_by_catalog_validation() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        catalog_path = make_fixture(root)
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        payload["blueprints"][1]["depends_on"] = ["missing-blueprint"]
        write(catalog_path, json.dumps(payload, indent=2) + "\n")
        try:
            compiler.build_module_blueprints(root)
        except compiler.ModuleBlueprintError as error:
            assert "unknown blueprint" in str(error)
        else:
            raise AssertionError("Expected unknown Blueprint dependency to fail catalog validation.")


if __name__ == "__main__":
    test_ready_dependency_plan()
    test_order_violation_blocks_the_feature()
    test_missing_literal_anchor_blocks_the_feature()
    test_targeted_draft_verification_does_not_hide_its_own_errors()
    test_invalid_dependency_is_rejected_by_catalog_validation()
    print("test_module_blueprint: OK")
