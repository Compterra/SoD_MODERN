"""Focused fixture tests for the complete Module Atlas control plane.

The Atlas must make a module-system area discoverable and semantically
authorable without touching the live SoD Modern workspace.  This miniature
eight-area module proves the index, graph, integrity scan, plans, and guarded
dry-runs against actual Python source shapes.
"""

from __future__ import annotations

import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.module_atlas import module_atlas


FIXTURES = {
    "constants/fixture_constants.py": '''fixture_value = 1
fixture_other = fixture_value
''',
    "dialogs/0001_fixture/fixture_dialogue.py": '''DIALOGS = [
    [anyone, "fixture_state", [], "@Fixture dialogue", "close_window", []],
]
''',
    "menus/0001_fixture/fixture_menu.py": '''MENUS = [
    ("fixture_menu", 0, "@Fixture menu", "none", [(call_script, "script_fixture_script")], [
        ("continue", [], "@Continue", [(jump_to_menu, "mnu_fixture_menu")]),
    ]),
]
''',
    "mission_templates/0001_fixture/fixture_mission.py": '''MISSION_TEMPLATES = [
    ("fixture_mission", 0, -1, "Fixture mission", [], [
        (ti_before_mission_start, 0, 0, [], [(call_script, "script_fixture_script")]),
    ]),
]
''',
    "presentations/0001_fixture/fixture_presentation.py": '''PRESENTATIONS = [
    ("fixture_presentation", 0, "none", []),
]
''',
    "quests/0001_fixture/fixture_quest.py": '''QUESTS = [
    ("fixture_quest", "Fixture quest", 0, "Fixture description"),
]
''',
    "scripts/0001_fixture/fixture_script.py": '''SCRIPTS = [
    ("fixture_script", [(assign, "$fixture", 1), (jump_to_menu, "mnu_fixture_menu")]),
]
''',
    "triggers/0001_fixture/fixture_trigger.py": '''SIMPLE_TRIGGERS = [
    (1, [(call_script, "script_fixture_script")]),
]
''',
}


def make_workspace(root: Path) -> None:
    for relative, source in FIXTURES.items():
        path = root / "src" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    compile_root = root / "compile"
    compile_root.mkdir()
    for name in (
        "module_constants.py",
        "module_dialogs.py",
        "module_game_menus.py",
        "module_mission_templates.py",
        "module_presentations.py",
        "module_quests.py",
        "module_scripts.py",
        "module_simple_triggers.py",
    ):
        (compile_root / name).write_text("# fixture generated module\n", encoding="utf-8")


def entity(index: module_atlas.ModuleAtlasIndex, kind: str, name: str) -> module_atlas.ModuleEntity:
    return module_atlas.resolve_named_entity(index, kind, name)


def plan(index: module_atlas.ModuleAtlasIndex, entity_id: str, action: str, **kwargs: object) -> dict[str, object]:
    payload = module_atlas.module_patch(index, entity_id, action=action, **kwargs)
    assert payload["change_router_plan"]["unified_diff"]
    return payload


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="module-atlas-") as temporary:
        root = Path(temporary)
        make_workspace(root)
        index = module_atlas.build_module_atlas(root)

        summary = module_atlas.module_summary(index)
        assert summary["source_area_count"] == 8
        assert set(summary["entity_count_by_area"]) == set(module_atlas.SOURCE_AREAS)
        assert summary["entity_count"] == 11  # top-level plus one menu option and one mission trigger

        found = module_atlas.module_find(index, query="fixture", area="all", limit=30)
        assert found["match_count"] >= 11
        integrity = module_atlas.module_integrity(index, limit=20)
        assert integrity["duplicate_definition_count"] == 0
        assert integrity["unresolved_reference_entity_count"] == 0

        menu = entity(index, "menu", "fixture_menu")
        option = next(candidate for candidate in index.entities if candidate.parent_id == menu.id)
        script = entity(index, "script", "fixture_script")
        mission = entity(index, "mission_template", "fixture_mission")
        mission_trigger = next(candidate for candidate in index.entities if candidate.parent_id == mission.id)
        quest = entity(index, "quest", "fixture_quest")
        constant = entity(index, "constant", "fixture_value")
        spare_constant = entity(index, "constant", "fixture_other")
        trigger = next(candidate for candidate in index.entities if candidate.kind == "simple_trigger")

        context = module_atlas.module_context(index, menu.id, max_lines=30, related_limit=10)
        assert context["entity"]["name"] == "fixture_menu"
        assert context["relationships"]["child_count"] == 1
        graph = module_atlas.module_graph(index, script.id, depth=2, max_nodes=30)
        assert graph["node_count"] >= 3
        assert module_atlas.menu_flow(index, "fixture_menu")["options"][0]["name"].endswith(":continue")
        assert module_atlas.script_flow(index, "fixture_script")["operation_summary"]["operation_count"] == 2
        assert module_atlas.mission_timeline(index, "fixture_mission")["trigger_count"] == 1
        assert module_atlas.trigger_timeline(index)["match_count"] == 1
        assert module_atlas.quest_registry(index)["match_count"] == 1
        references = module_atlas.entity_references(index, "fixture_value")
        assert references["definition_count"] == 1
        assert references["reference_count"] == 1

        text_plan = plan(index, menu.id, "set_text", value="@Changed fixture menu")
        assert "@Changed fixture menu" in text_plan["change_router_plan"]["unified_diff"]
        option_plan = plan(
            index,
            menu.id,
            "add_menu_option",
            new_item={"id": "new_option", "text": "@New option", "conditions": "[]", "consequences": "[]"},
        )
        assert "new_option" in option_plan["change_router_plan"]["unified_diff"]
        menu_plan = plan(
            index,
            menu.id,
            "add_menu",
            new_item={"id": "new_menu", "text": "@New menu", "on_enter": "[]", "options": []},
        )
        assert "new_menu" in menu_plan["change_router_plan"]["unified_diff"]
        assert plan(index, option.id, "remove_menu_option")["change_router_plan"]["unified_diff"]

        operation_plan = plan(index, script.id, "insert_operation", block="operations", operation="(assign, \"$fixture_new\", 1)")
        assert "$fixture_new" in operation_plan["change_router_plan"]["unified_diff"]
        script_plan = plan(index, script.id, "add_script", new_item={"id": "new_script", "operations": "[]"})
        assert "new_script" in script_plan["change_router_plan"]["unified_diff"]
        assert plan(index, script.id, "remove_operation", block="operations", operation_index=0)["change_router_plan"]["unified_diff"]

        constant_plan = plan(index, constant.id, "add_constant", new_item={"name": "new_constant", "value": "fixture_value + 1"})
        assert "new_constant" in constant_plan["change_router_plan"]["unified_diff"]
        assert plan(index, constant.id, "set_expression", value="2")["change_router_plan"]["unified_diff"]
        try:
            module_atlas.module_patch(index, constant.id, action="remove_entity")
        except module_atlas.ModuleAtlasError as error:
            assert "inbound reference" in str(error)
        else:
            raise AssertionError("Referenced constant removal must require explicit acknowledgement.")
        assert plan(index, spare_constant.id, "remove_entity")["change_router_plan"]["unified_diff"]

        quest_plan = plan(
            index,
            quest.id,
            "add_quest",
            new_item={"id": "new_quest", "title": "New quest", "description": "New description", "flags": "0"},
        )
        assert "new_quest" in quest_plan["change_router_plan"]["unified_diff"]
        assert plan(index, quest.id, "set_text", field="title", value="Changed title")["change_router_plan"]["unified_diff"]

        mission_trigger_plan = plan(
            index,
            mission.id,
            "add_mission_trigger",
            new_item={"event": "ti_on_agent_spawned", "interval": "0", "repeat": "0", "conditions": "[]", "consequences": "[]"},
        )
        assert "ti_on_agent_spawned" in mission_trigger_plan["change_router_plan"]["unified_diff"]
        mission_plan = plan(
            index,
            mission.id,
            "add_mission_template",
            new_item={"id": "new_mission", "description": "New mission", "triggers": []},
        )
        assert "new_mission" in mission_plan["change_router_plan"]["unified_diff"]
        assert plan(index, mission_trigger.id, "set_trigger_interval", value="2")["change_router_plan"]["unified_diff"]
        assert plan(index, mission_trigger.id, "remove_mission_trigger")["change_router_plan"]["unified_diff"]

        simple_plan = plan(index, trigger.id, "add_simple_trigger", new_item={"interval": "2", "operations": "[]"})
        assert "(2, [])" in simple_plan["change_router_plan"]["unified_diff"]
        assert plan(index, trigger.id, "set_trigger_interval", value="3")["change_router_plan"]["unified_diff"]
        assert plan(index, trigger.id, "remove_entity")["change_router_plan"]["unified_diff"]

        rehearsal = module_atlas.module_apply(
            index,
            menu.id,
            action="set_text",
            value="@Changed fixture menu",
            expected_sha256=text_plan["change_router_plan"]["target"]["base_sha256"],
            dry_run=True,
        )
        assert rehearsal["result"]["applied"] is False
        assert (root / menu.path).read_text(encoding="utf-8") == FIXTURES["menus/0001_fixture/fixture_menu.py"]

    print("test_module_atlas: OK")


if __name__ == "__main__":
    main()
