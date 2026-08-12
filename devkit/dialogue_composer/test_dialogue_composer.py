"""Focused fixture tests for semantic dialogue authoring.

These tests intentionally use an isolated miniature module workspace.  They
prove semantic plans and dry-runs without changing this live module source.
"""

from __future__ import annotations

import contextlib
import io
import json
import ast
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.dialogue_composer import dialogue_composer


SOURCE = '''DIALOGS = [
    [anyone, "fixture_start", [], "@First line", "fixture_next", []],
    [anyone, "fixture_start", [(eq, ":gate", 1)], "@Second line", "close_window", [(assign, "$fixture_done", 1)]],
]
'''


def make_workspace(root: Path) -> None:
    dialog = root / "src" / "dialogs" / "0001_fixture" / "fixture_dialogue.py"
    dialog.parent.mkdir(parents=True)
    dialog.write_text(SOURCE, encoding="utf-8")
    compile_root = root / "compile"
    compile_root.mkdir()
    (compile_root / "module_dialogs.py").write_text("dialogs = []\n", encoding="utf-8")


def test_create_contract_schema() -> None:
    schema_path = REPO_ROOT / "devkit" / "dialogue_composer" / "contracts" / "dialogue-create.v1.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    valid = {
        "anchor_route_id": "dialogue:src/dialogs/fixture.py:L2:C0",
        "position": "after",
        "speaker": "plyr",
        "input_state": "fixture_created_choice",
        "text": "@Created through the schema.",
        "output_state": "close_window",
        "conditions": [],
        "consequences": [],
    }
    assert set(schema["required"]) <= set(valid)
    assert schema["additionalProperties"] is False
    assert schema["properties"]["text"]["pattern"] == "^@"
    assert schema["properties"]["position"]["enum"] == ["before", "after"]
    assert schema["properties"]["shadow_acknowledgement"]["const"] == dialogue_composer.SHADOW_ACKNOWLEDGEMENT
    invalid = {**valid, "text": "No inline M&B marker."}
    try:
        dialogue_composer.parse_create_spec(invalid)
    except dialogue_composer.DialogueComposerError as error:
        assert "must start with '@'" in str(error)
    else:
        raise AssertionError("The implementation accepted a schema-invalid inline dialogue text.")


def test_legacy_list_operation_syntax_is_guarded() -> None:
    block = ast.parse('[[eq, ":gate", 1]]').body[0].value
    assert dialogue_composer.direct_operations(block) == ("eq",)

    negated = ast.parse('[neg|party_can_join]').body[0].value
    assert dialogue_composer.direct_operations(negated) == ("neg|party_can_join",)


def test_player_speaker_detection_accepts_or_expressions() -> None:
    assert dialogue_composer.is_player_speaker("plyr") is True
    assert dialogue_composer.is_player_speaker("anyone|plyr") is True
    assert dialogue_composer.is_player_speaker("anyone | plyr") is True
    assert dialogue_composer.is_player_speaker("anyone") is False


def main() -> None:
    test_create_contract_schema()
    test_legacy_list_operation_syntax_is_guarded()
    test_player_speaker_detection_accepts_or_expressions()
    with tempfile.TemporaryDirectory(prefix="dialogue-composer-") as temporary:
        root = Path(temporary)
        make_workspace(root)
        index = dialogue_composer.build_dialogue_composer(root)
        assert len(index.routes) == 2
        first, second = index.routes

        found = dialogue_composer.dialogue_find(index, input_state="fixture_start")
        assert found["match_count"] == 2
        context = dialogue_composer.dialogue_context(index, first.id, max_lines=30, related_limit=5)
        assert context["route"]["route_id"] == first.id

        text_plan = dialogue_composer.dialogue_patch(
            index,
            first.id,
            action="replace_text",
            value="@Changed first line",
        )
        assert "@Changed first line" in text_plan["change_router_plan"]["unified_diff"]
        assert "@Changed first line" not in (root / first.path).read_text(encoding="utf-8")

        condition_plan = dialogue_composer.dialogue_patch(
            index,
            first.id,
            action="insert_condition",
            operation='(eq, ":gate", 2)',
        )
        assert "(eq, \":gate\", 2)" in condition_plan["change_router_plan"]["unified_diff"]

        bridge_plan = dialogue_composer.dialogue_patch(
            index,
            first.id,
            action="bridge_menu",
            value="mnu_fixture_menu",
        )
        assert "jump_to_menu" in bridge_plan["change_router_plan"]["unified_diff"]

        add_plan = dialogue_composer.dialogue_patch(
            index,
            first.id,
            action="add_route",
            position="after",
            new_route={
                "speaker": "plyr",
                "input_state": "fixture_next",
                "conditions": "[]",
                "text": "@Continue",
                "output_state": "close_window",
                "consequences": "[]",
            },
        )
        assert "@Continue" in add_plan["change_router_plan"]["unified_diff"]

        create_spec = {
            "anchor_route_id": first.id,
            "position": "after",
            "speaker": "plyr",
            "input_state": "fixture_created_choice",
            "text": "@Created through the deterministic contract.",
            "output_state": "close_window",
            "conditions": [],
            "consequences": ['(assign, "$fixture_created", 1)'],
        }
        create_plan = dialogue_composer.dialogue_create_plan(index, create_spec)
        assert create_plan["anchor_route"]["route_id"] == first.id
        assert create_plan["change_router_plan"]["plan_id"].startswith("change-plan:")
        assert "Created through the deterministic contract" in create_plan["change_router_plan"]["unified_diff"]
        create_rehearsal = dialogue_composer.dialogue_create_apply(
            index,
            create_spec,
            expected_sha256=create_plan["change_router_plan"]["target"]["base_sha256"],
            expected_plan_id=create_plan["change_router_plan"]["plan_id"],
            dry_run=True,
        )
        assert create_rehearsal["result"]["applied"] is False
        changed_create_spec = {**create_spec, "text": "@A different unreviewed route."}
        try:
            dialogue_composer.dialogue_create_apply(
                index,
                changed_create_spec,
                expected_sha256=create_plan["change_router_plan"]["target"]["base_sha256"],
                expected_plan_id=create_plan["change_router_plan"]["plan_id"],
                dry_run=True,
            )
        except dialogue_composer.DialogueComposerError as error:
            assert "expected_plan_id" in str(error)
        else:
            raise AssertionError("Creation apply accepted a different unreviewed plan.")

        request_path = root / "create-route.json"
        request_path.write_text(json.dumps(create_spec), encoding="utf-8")
        cli_output = io.StringIO()
        with contextlib.redirect_stdout(cli_output):
            cli_exit = dialogue_composer.main(
                ["--root", str(root), "create-plan", "--spec-file", "create-route.json"]
            )
        assert cli_exit == 0
        assert "change-plan:" in cli_output.getvalue()

        duplicate_spec = {
            "anchor_route_id": first.id,
            "position": "after",
            "speaker": "anyone",
            "input_state": "fixture_start",
            "text": "@Duplicate fallback.",
            "output_state": "close_window",
            "conditions": [],
            "consequences": [],
        }
        try:
            dialogue_composer.dialogue_create_plan(index, duplicate_spec)
        except dialogue_composer.DialogueComposerError as error:
            assert "duplicates an existing" in str(error)
        else:
            raise AssertionError("A duplicate dialogue route was accepted.")

        shadowed_spec = {
            "anchor_route_id": first.id,
            "position": "after",
            "speaker": "anyone",
            "input_state": "fixture_start",
            "text": "@Shadowed condition.",
            "output_state": "close_window",
            "conditions": ['(eq, ":gate", 3)'],
            "consequences": [],
        }
        try:
            dialogue_composer.dialogue_create_plan(index, shadowed_spec)
        except dialogue_composer.DialogueComposerError as error:
            assert "static first-match risk" in str(error)
        else:
            raise AssertionError("A statically shadowed NPC route was accepted without acknowledgement.")

        shadowed_spec["allow_static_shadow"] = True
        shadowed_spec["shadow_acknowledgement"] = dialogue_composer.SHADOW_ACKNOWLEDGEMENT
        acknowledged_plan = dialogue_composer.dialogue_create_plan(index, shadowed_spec)
        assert any(
            warning["code"] == "PRECEDING_NPC_FALLBACK"
            for warning in acknowledged_plan["static_creation_safety"]["warnings"]
        )

        move_plan = dialogue_composer.dialogue_patch(
            index,
            second.id,
            action="move_route",
            anchor_route_id=first.id,
            position="before",
        )
        assert move_plan["change_router_plan"]["unified_diff"]

        rehearsal = dialogue_composer.dialogue_apply(
            index,
            first.id,
            action="replace_text",
            value="@Changed first line",
            expected_sha256=text_plan["change_router_plan"]["target"]["base_sha256"],
            dry_run=True,
        )
        assert rehearsal["result"]["applied"] is False
        assert (root / first.path).read_text(encoding="utf-8") == SOURCE

    print("test_dialogue_composer: OK")


if __name__ == "__main__":
    main()
