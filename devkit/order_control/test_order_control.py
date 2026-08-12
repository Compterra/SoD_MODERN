"""Fixture tests for the M&B 1.011 Order Control Plane.

The fixtures contain two menu fragments, an NPC dialogue fallback/gated pair,
and a protected game callback.  They prove that Order Control sees source,
route, and generated-ID order separately; only an explicit manifest can move
fragments; all applies stay SHA-guarded and dry-run by default.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.module_atlas.test_module_atlas import make_workspace
from devkit.order_control import order_control


SECOND_MENU = '''MENUS = [
    ("fixture_menu_b", 0, "@Second fixture menu", "none", [], []),
]
'''

DIALOGUES = '''DIALOGS = [
    [anyone, "fixture_start", [], "@Fallback", "close_window", []],
    [anyone, "fixture_start", [(eq, ":gate", 1)], "@Gated", "close_window", []],
    [anyone|plyr, "fixture_player_choice", [], "@First choice", "close_window", []],
    [anyone|plyr, "fixture_player_choice", [], "@Second choice", "close_window", []],
    [anyone, "fixture_capacity", [neg|party_can_join], "@No room", "close_window", []],
    [anyone, "fixture_capacity", [], "@Join", "close_window", []],
]
'''

GAME_START = '''SCRIPTS = [
    ("game_start", []),
]
'''

CONTRACTS = {
    "schema": "sod-modern.order-control-contract-catalog.v1",
    "version": 1,
    "contracts": [
        {
            "id": "fixture-strict-manifests",
            "title": "Fixture strict manifests",
            "kind": "manifest-integrity",
            "status": "active",
            "severity": "blocker",
            "spec_ids": ["dialogs", "menus"],
            "require_complete": True,
        },
        {
            "id": "fixture-menu-prefix",
            "title": "Fixture menu prefix",
            "kind": "id-prefix",
            "status": "active",
            "severity": "blocker",
            "area": "menus",
            "entity_kind": "menu",
            "source_prefix": "src/menus/0001_fixture/",
            "id_table": "compile/ids/ID_menus.py",
            "expected_start": 0,
        },
        {
            "id": "fixture-game-callback",
            "title": "Fixture engine callback",
            "kind": "engine-callback-sequence",
            "status": "active",
            "severity": "blocker",
            "area": "scripts",
            "entity_kind": "script",
            "source_prefix": "src/scripts/ZA_hardcoded_game_scripts/",
            "name_prefix": "game_",
            "id_table": "compile/ids/ID_scripts.py",
            "expected_start": 0,
        },
    ],
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_order_workspace(root: Path) -> None:
    make_workspace(root)
    write(root / "src/menus/0001_fixture/fixture_menu_b.py", SECOND_MENU)
    write(root / "src/dialogs/0001_fixture/fixture_dialogue.py", DIALOGUES)
    write(root / "src/scripts/ZA_hardcoded_game_scripts/game_start.py", GAME_START)
    write(
        root / "src/dialogs/_order_dialogs.txt",
        "0001_fixture/fixture_dialogue.py\n",
    )
    write(
        root / "src/menus/_order_game_menus.txt",
        "# Fixture menu order\n0001_fixture/fixture_menu.py\n0001_fixture/fixture_menu_b.py\n",
    )
    write(
        root / "src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt",
        "ZA_hardcoded_game_scripts/game_start.py\n",
    )
    write(
        root / "compile/ids/ID_menus.py",
        "menu_fixture_menu = 0\nmenu_fixture_menu_b = 1\n",
    )
    write(
        root / "compile/ids/ID_scripts.py",
        "script_game_start = 0\nscript_fixture_script = 1\n",
    )
    write(
        root / "devkit/order_control/contracts/manifest.json",
        json.dumps(CONTRACTS, indent=2) + "\n",
    )
    write(root / "devkit/order_control/baselines/.gitignore", "*\n!.gitignore\n")
    write(root / "devkit/order_control/reports/.gitignore", "*\n!.gitignore\n")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="order-control-") as temporary:
        root = Path(temporary)
        make_order_workspace(root)
        index = order_control.build_order_control(root)
        assert order_control.build_order_control(root) is index  # Repeated agent queries share one fresh linked index.
        source_probe = root / "src/menus/0001_fixture/fixture_menu.py"
        write(source_probe, source_probe.read_text(encoding="utf-8") + "\n# Order Control freshness probe.\n")
        refreshed_index = order_control.build_order_control(root)
        assert refreshed_index is not index  # External source edits invalidate the linked cache through its input signature.
        index = refreshed_index

        summary = order_control.order_summary(index)
        assert summary["contracts"]["active_blocker_count"] == 0
        contracts = order_control.order_contracts(index)
        assert contracts["summary"]["active_blocker_count"] == 0
        assert next(item for item in contracts["contracts"] if item["id"] == "fixture-menu-prefix")["passed"] is True

        mapped = order_control.order_map(index, area="menus", domain="source-fragments", query="fixture", limit=10)
        assert mapped["groups"][0]["match_count"] == 2
        target = "source:src/menus/0001_fixture/fixture_menu_b.py"
        anchor = "source:src/menus/0001_fixture/fixture_menu.py"
        explained = order_control.order_explain(index, target)
        assert explained["fragment"]["source_order"]["position"] == 2
        assert explained["safe_moves"] == ["manifest_entry_before_after"]

        baseline = order_control.order_baseline(index, label="fixture")
        assert (root / baseline["artifact"]["path"]).is_file()
        plan = order_control.order_plan_move(index, target, anchor, position="before")
        assert plan["plan_kind"] == "fragment_manifest_move"
        assert "fixture_menu_b.py" in plan["order_manifest_plan"]["unified_diff"]
        assert plan["apply_contract"]["protected_contract_override_required"] is True
        sha = plan["order_manifest_plan"]["base_sha256"]
        order_file = root / "src/menus/_order_game_menus.txt"
        before = order_file.read_text(encoding="utf-8")
        rehearsal = order_control.order_apply_move(index, target, anchor, position="before", expected_sha256=sha, dry_run=True)
        assert rehearsal["applied"] is False
        assert order_file.read_text(encoding="utf-8") == before

        try:
            order_control.order_apply_move(index, target, anchor, position="before", expected_sha256=sha, dry_run=False)
        except order_control.OrderControlError as error:
            assert "allow_protected_contract_change" in str(error)
        else:
            raise AssertionError("Protected non-dry order move must require an explicit override.")

        applied = order_control.order_apply_move(
            index,
            target,
            anchor,
            position="before",
            expected_sha256=sha,
            dry_run=False,
            allow_protected_contract_change=True,
        )
        assert applied["applied"] is True
        assert applied["protected_contract_override_used"] is True
        after = order_file.read_text(encoding="utf-8")
        assert after.index("fixture_menu_b.py") < after.index("fixture_menu.py")
        moved_index = order_control.build_order_control(root)
        assert moved_index is not index
        moved = order_control.order_explain(moved_index, target)
        assert moved["fragment"]["source_order"]["position"] == 1
        diff = order_control.order_diff(moved_index, baseline="fixture", limit=10)
        assert diff["summary"]["source_change_count"] >= 2
        verification = order_control.order_verify(moved_index, baseline="fixture", limit=10)
        assert verification["state"] == "structural_order_blocked"  # Source was reordered while generated fixture IDs remain old.
        player_hazards = [
            hazard
            for hazard in verification["dialogue_order_hazards"]["hazards"]
            if hazard["input_state"] == "fixture_player_choice"
        ]
        assert player_hazards == []
        capacity_hazards = [
            hazard
            for hazard in verification["dialogue_order_hazards"]["hazards"]
            if hazard["input_state"] == "fixture_capacity"
        ]
        assert capacity_hazards == []

        routes = order_control.dialogue_composer.dialogue_find(moved_index.dialogues, input_state="fixture_start", limit=10)["routes"]
        fallback = next(route for route in routes if route["text"] == "@Fallback")
        gated = next(route for route in routes if route["text"] == "@Gated")
        dialogue_plan = order_control.order_plan_move(
            moved_index,
            gated["route_id"],
            fallback["route_id"],
            position="before",
        )
        assert dialogue_plan["plan_kind"] == "dialogue_route_move"
        assert dialogue_plan["change_router_plan"]["unified_diff"]
        dialogue_sha = dialogue_plan["change_router_plan"]["target"]["base_sha256"]
        dialogue_before = (root / "src/dialogs/0001_fixture/fixture_dialogue.py").read_text(encoding="utf-8")
        dialogue_rehearsal = order_control.order_apply_move(moved_index, gated["route_id"], fallback["route_id"], position="before", expected_sha256=dialogue_sha, dry_run=True)
        assert dialogue_rehearsal["applied"] is False
        assert (root / "src/dialogs/0001_fixture/fixture_dialogue.py").read_text(encoding="utf-8") == dialogue_before

    print("test_order_control: OK")


if __name__ == "__main__":
    main()
