"""Focused fixture tests for static canvas and semantic layout authoring."""

from __future__ import annotations

import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.presentation_layout import presentation_layout


SOURCE = '''PRESENTATIONS = [
    ("fixture_presentation", 0, 0, [
        (ti_on_presentation_load, [
            (str_store_string, s68, "@Fixture label"),
            (create_text_overlay, "$g_fixture_label", s68),
            (position_set_x, pos1, 100),
            (position_set_y, pos1, 200),
            (overlay_set_position, "$g_fixture_label", pos1),
            (position_set_x, pos1, 600),
            (position_set_y, pos1, 800),
            (overlay_set_size, "$g_fixture_label", pos1),
            (overlay_set_color, "$g_fixture_label", 0xFF00FF00),
            (overlay_set_alpha, "$g_fixture_label", 200),
        ]),
        (ti_on_presentation_event_state_change, []),
    ]),
]
'''


def make_workspace(root: Path) -> None:
    source = root / "src" / "presentations" / "0001_fixture" / "fixture_presentation.py"
    source.parent.mkdir(parents=True)
    source.write_text(SOURCE, encoding="utf-8")
    compile_root = root / "compile"
    compile_root.mkdir()
    (compile_root / "module_presentations.py").write_text("presentations = []\n", encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="presentation-layout-") as temporary:
        root = Path(temporary)
        make_workspace(root)
        index = presentation_layout.build_presentation_layout(root)
        assert len(index.presentations) == 1
        presentation = index.presentations[0]
        overlay = presentation.overlays[0]
        assert overlay.position_x.value == 100
        assert overlay.size_y.value == 800

        found = presentation_layout.presentation_find(index, query="fixture")
        assert found["match_count"] == 1
        assert presentation_layout.presentation_find(index, query="*")["match_count"] == 1
        canvas = presentation_layout.presentation_canvas(index, presentation.key)
        canvas_overlay = canvas["canvas"]["overlays"][0]
        assert canvas_overlay["canvas_box"] is not None
        assert canvas_overlay["content"] == "s68"
        assert canvas_overlay["content_is_literal"] is False
        assert canvas_overlay["content_literal"] is None
        assert presentation_layout.content_literal('"@Direct label"') == "@Direct label"

        move_plan = presentation_layout.presentation_patch(
            index,
            overlay.id,
            action="move_overlay",
            x=125,
            y=225,
        )
        assert "125" in move_plan["change_router_plan"]["unified_diff"]
        assert "225" in move_plan["change_router_plan"]["unified_diff"]

        resize_plan = presentation_layout.presentation_patch(
            index,
            overlay.id,
            action="resize_overlay",
            x=650,
            y=850,
        )
        assert "650" in resize_plan["change_router_plan"]["unified_diff"]

        text_plan = presentation_layout.presentation_patch(
            index,
            overlay.id,
            action="set_text",
            value="@Changed label",
        )
        assert "@Changed label" in text_plan["change_router_plan"]["unified_diff"]

        color_plan = presentation_layout.presentation_patch(
            index,
            overlay.id,
            action="set_color",
            value="0xFFFF0000",
        )
        assert "0xFFFF0000" in color_plan["change_router_plan"]["unified_diff"]

        add_plan = presentation_layout.presentation_patch(
            index,
            presentation.key,
            action="add_overlay",
            new_overlay={
                "kind": "button",
                "destination": "$g_fixture_button",
                "text": "@Press",
                "x": 500,
                "y": 500,
            },
        )
        assert "create_button_overlay" in add_plan["change_router_plan"]["unified_diff"]

        add_trigger_plan = presentation_layout.presentation_patch(
            index,
            presentation.key,
            action="add_trigger",
            new_trigger={"event": "ti_on_presentation_run", "operations": "[]"},
        )
        assert "ti_on_presentation_run" in add_trigger_plan["change_router_plan"]["unified_diff"]

        replace_trigger_plan = presentation_layout.presentation_patch(
            index,
            presentation.key,
            action="replace_trigger_operations",
            trigger="ti_on_presentation_event_state_change",
            value='[(assign, "$g_fixture_changed", 1)]',
        )
        assert "$g_fixture_changed" in replace_trigger_plan["change_router_plan"]["unified_diff"]

        remove_trigger_plan = presentation_layout.presentation_patch(
            index,
            presentation.key,
            action="remove_trigger",
            trigger="ti_on_presentation_event_state_change",
        )
        assert remove_trigger_plan["change_router_plan"]["unified_diff"]

        remove_plan = presentation_layout.presentation_patch(index, overlay.id, action="remove_overlay")
        assert remove_plan["change_router_plan"]["unified_diff"]

        rehearsal = presentation_layout.presentation_apply(
            index,
            overlay.id,
            action="move_overlay",
            x=125,
            y=225,
            expected_sha256=move_plan["change_router_plan"]["target"]["base_sha256"],
            dry_run=True,
        )
        assert rehearsal["result"]["applied"] is False
        assert (root / overlay.path).read_text(encoding="utf-8") == SOURCE

        preview = presentation_layout.presentation_preview(index, presentation.key, output_name="fixture-preview.svg")
        assert (root / preview["artifact"]["path"]).is_file()

    print("test_presentation_layout: OK")


if __name__ == "__main__":
    main()
