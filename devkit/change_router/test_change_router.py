"""Regression checks for LLM-first source discovery and guarded edits."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.change_router import change_router as router_module


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_fixture(root: Path) -> str:
    source_relative = "src/scripts/ZA_demo/demo_fragment.py"
    source = (
        "SCRIPTS = [\n"
        '    ("demo", [(assign, "$demo", 1)]),\n'
        "]\n"
    )
    write(root / source_relative, source)
    generated = (
        "# [src/scripts/ZA_demo/demo_fragment.py:L1-L3] script_demo\n"
        "scripts = [\n"
        '    ("demo", [(assign, "$demo", 1)]),\n'
        "]\n"
    )
    write(root / "compile/module_scripts.py", generated)
    builder = (
        "from pathlib import Path\n"
        "ROOT = Path(__file__).resolve().parents[1]\n"
        "raw = (ROOT / 'src/scripts/ZA_demo/demo_fragment.py').read_text(encoding='utf-8')\n"
        "out = ROOT / 'compile/module_scripts.py'\n"
        "out.parent.mkdir(parents=True, exist_ok=True)\n"
        "out.write_text('# [src/scripts/ZA_demo/demo_fragment.py:L1-L3] script_demo\\n' + raw, encoding='utf-8')\n"
    )
    write(root / "build/build_scripts.py", builder)
    return source_relative


def test_workspace_router() -> None:
    index = router_module.build_change_router(REPO_ROOT)
    summary = router_module.router_summary(index)
    assert summary["source_fragment_count"] > 5_000
    assert summary["generated_segment_count"] > 6_000
    assert summary["source_to_generated_linked_fragment_count"] > 5_000

    found = router_module.code_find(index, "past_life", scope="source", limit=5)
    target_id = next(
        hit["target_id"]
        for hit in found["matches"]
        if hit["path"].endswith("past_life_explanation.py")
    )
    context = router_module.linked_context(
        index,
        target_id,
        focus_line=20,
        max_lines=20,
        related_limit=12,
    )
    assert context["target"]["area"] == "menus"
    assert context["generated_links"][0]["compile_path"] == "compile/module_game_menus.py"
    assert "$current_string_reg" in context["relationships"]["globals"]["reads"]
    assert context["relationships"]["visible_text_sink_count"] >= 1

    impact = router_module.change_impact(index, target_id, related_limit=12)
    assert impact["direct_generated_outputs"] == ["compile/module_game_menus.py"]
    assert impact["expected_stale_layers_after_source_edit"]["exports"] == ["_export/menus.txt"]
    assert impact["risk_level"] in {"medium", "high"}


def test_guarded_edit_and_isolated_build() -> None:
    with tempfile.TemporaryDirectory(prefix="change-router-test-") as temporary:
        root = Path(temporary)
        source_relative = make_fixture(root)
        index = router_module.build_change_router(root)
        target_id = f"source:{source_relative}"
        fragment = router_module.target_fragment(index, target_id)
        edits = [
            {
                "old_text": '"$demo"',
                "new_text": '"$demo_changed"',
                "expected_occurrences": 1,
            }
        ]
        plan = router_module.patch_plan(
            index,
            target_id,
            edits,
            expected_sha256=fragment.sha256,
        )
        assert plan["unified_diff"]
        assert plan["target"]["base_sha256"] == fragment.sha256

        rehearsal = router_module.apply_source_edits(
            index,
            target_id,
            edits,
            expected_sha256=fragment.sha256,
            dry_run=True,
        )
        assert rehearsal["applied"] is False
        assert '"$demo_changed"' not in (root / source_relative).read_text(encoding="utf-8")

        applied = router_module.apply_source_edits(
            index,
            target_id,
            edits,
            expected_sha256=fragment.sha256,
            dry_run=False,
        )
        assert applied["applied"] is True
        assert '"$demo_changed"' in (root / source_relative).read_text(encoding="utf-8")

        verification_index = router_module.build_change_router(root)
        verification = router_module.verify_change(
            verification_index,
            target_id,
            expected_sha256=applied["target"]["result_sha256"],
            stage_build_check=True,
            max_tests=1,
            timeout_seconds=30,
        )
        assert verification["syntax"]["passed"] is True
        assert verification["staged_build"]["passed"] is True
        assert verification["staged_build"]["generated_changed"] is True
        json.dumps(verification)


if __name__ == "__main__":
    test_workspace_router()
    test_guarded_edit_and_isolated_build()
    print("test_change_router: OK")
