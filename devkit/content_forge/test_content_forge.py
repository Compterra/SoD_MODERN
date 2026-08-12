"""Focused coverage for the Content Forge typed authoring compiler."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.content_forge import content_forge as forge


def full_slice_pack(index: forge.ContentForgeIndex) -> dict:
    dialogue_entry = next(entry.id for entry in index.features.entrypoints if entry.family == "dialogue-state")
    presentation_entry = next(entry.id for entry in index.features.entrypoints if entry.family == "presentation")
    return {
        "schema": forge.CONTENT_PACK_SCHEMA,
        "id": "content-forge-slice-smoke",
        "title": "Content Forge Slice Smoke",
        "status": "draft",
        "description": "No-write compiler coverage for every authored-content slice.",
        "brief": {
            "summary": "Exercise every typed Content Forge slice without modifying the workspace.",
            "lore_constraints": ["The probe is never applied."],
            "tone": ["technical"],
            "acceptance_criteria": ["Every slice reaches its intended specialist compiler."],
        },
        "slices": {
            "dialogue": {
                "changes": [],
                "beats": [
                    {"id": "opening-beat", "title": "Opening", "purpose": "Establish a narrative beat.", "entrypoint": dialogue_entry}
                ],
            },
            "quest_event": {
                "changes": [],
                "timeline": [
                    {
                        "id": "event-hook",
                        "title": "Event hook",
                        "phase": "setup",
                        "description": "Associate a quest/event lifecycle step with a real script.",
                        "entrypoint": "entrypoint:script:sod_black_khergits_lock_camped_ai",
                    }
                ],
            },
            "campaign_ai": {
                "changes": [],
                "contracts": [
                    {
                        "id": "stationary-proof",
                        "intent": "stationary_camp",
                        "entrypoint": "entrypoint:script:sod_black_khergits_lock_camped_ai",
                        "required_markers": ["party_set_ai_behavior", "ai_bhvr_hold"],
                        "description": "Reuse the checked-in stationary camp proof for compiler coverage.",
                        "state_contract_id": "black_khergit_camped_ai_stationary",
                    }
                ],
                "scenarios": [],
            },
            "troop_item": {
                "records": [
                    {
                        "id": "unapplied-item-probe",
                        "entity_kind": "item",
                        "entity_id": "itm_no_item",
                        "changes": {"name": "No Item (unapplied content forge probe)"},
                        "rationale": "Compiler-only record descriptor coverage; this plan is never applied.",
                    }
                ]
            },
            "presentation": {
                "changes": [],
                "screens": [
                    {"id": "screen-proof", "title": "Existing screen", "description": "Render the existing presentation canvas in a preview.", "entrypoint": presentation_entry}
                ],
                "new_presentations": [
                    {
                        "anchor": presentation_entry,
                        "id": "content_forge_smoke_presentation",
                        "flags": 0,
                        "mesh": {"symbol": "mesh_load_window"},
                        "triggers": [{"event": {"symbol": "ti_on_presentation_load"}, "operations": []}],
                        "description": "A typed new-presentation plan used only for no-write compiler coverage.",
                    }
                ],
            },
        },
        "verification": {
            "tests": ["build/test_black_khergit_horde_presence.py"],
            "require_blueprint": False,
            "scenarios": [],
        },
    }


def main() -> None:
    index = forge.build_content_forge(REPO_ROOT)
    summary = forge.content_forge_summary(index)
    assert summary["pack_count"] >= 1
    found = forge.content_pack_find(index, "black khergit")
    assert found["match_count"] >= 1
    assert found["packs"][0]["id"] == "black-khergit-camp-runtime"

    validation = forge.content_pack_validate(index, pack_id="black-khergit-camp-runtime")
    assert validation["state"] == "ready", validation
    compiled = forge.content_pack_compile(index, pack_id="black-khergit-camp-runtime")
    assert compiled["state"] == "ready", compiled
    plan = forge.content_pack_plan(index, pack_id="black-khergit-camp-runtime", trace_limit=2)
    assert plan["state"] == "ready_for_review", plan
    assert plan["ai_intent_evidence"]["passed_count"] == 1
    review = forge.content_pack_review(index, pack_id="black-khergit-camp-runtime", trace_limit=2)
    assert review["review_canvas"]["mermaid"].startswith("flowchart TD")
    preview = forge.content_pack_preview(index, pack_id="black-khergit-camp-runtime", trace_limit=2)
    assert preview["state"] == "ready_for_review"
    snapshot = forge.content_pack_snapshot(index, pack_id="black-khergit-camp-runtime")
    delta = forge.content_pack_semantic_diff(index, snapshot, pack_id="black-khergit-camp-runtime")
    assert delta["state"] == "unchanged", delta
    verification = forge.content_pack_verify(
        index,
        pack_id="black-khergit-camp-runtime",
        run_scenarios=True,
        scenario_iterations=2,
        scenario_seed=3,
    )
    assert verification["state"] == "passed", verification
    assert verification["scenarios"]["state"] == "passed", verification

    inline = full_slice_pack(index)
    inline_validation = forge.content_pack_validate(index, pack_value=inline)
    assert inline_validation["state"] == "ready", inline_validation
    inline_compiled = forge.content_pack_compile(index, pack_value=inline)
    assert {row["slice"] for row in inline_compiled["apply_sequence"]} >= {"presentation", "troop_item"}
    inline_plan = forge.content_pack_plan(index, pack_value=inline, trace_limit=1)
    assert inline_plan["state"] == "ready_for_review", inline_plan
    assert {row["backend"] for row in inline_plan["changes"]} == {"feature_authoring", "troop_item_balance"}
    source_change = next(row for row in inline_plan["changes"] if row["backend"] == "feature_authoring")
    source_rehearsal = forge.content_pack_apply(
        index,
        pack_value=inline,
        change_id=source_change["change_id"],
        expected_content_plan_id=inline_plan["plan_id"],
        expected_sha256=source_change["expected_sha256"],
        dry_run=True,
    )
    assert source_rehearsal["result"]["result"]["applied"] is False
    balance_change = next(row for row in inline_plan["changes"] if row["backend"] == "troop_item_balance")
    balance_rehearsal = forge.content_pack_apply(
        index,
        pack_value=inline,
        change_id=balance_change["change_id"],
        expected_content_plan_id=inline_plan["plan_id"],
        expected_sha256=balance_change["expected_sha256"],
        expected_balance_plan_sha256=balance_change["expected_balance_plan_sha256"],
        dry_run=True,
    )
    assert balance_rehearsal["result"]["applied"] is False

    unsafe = full_slice_pack(index)
    unsafe["slices"]["dialogue"]["changes"] = [{"kind": "dialogue", "target": next(entry.id for entry in index.features.entrypoints if entry.family == "dialogue-state"), "action": "replace_text"}]
    try:
        forge.content_pack_validate(index, pack_value=unsafe)
    except forge.ContentForgeError as error:
        assert "inferred" in str(error)
    else:
        raise AssertionError("Content Forge accepted a caller-supplied source kind.")

    # The visual Studio may persist a typed pack draft, but only through this
    # exact catalog plan/SHA/confirmation gate. Keep that write coverage in a
    # temp workspace so the live checked-in packs.json remains untouched.
    with tempfile.TemporaryDirectory(prefix="content-forge-catalog-") as temporary:
        temporary_root = Path(temporary)
        catalog_path = temporary_root / forge.CONTENT_PACKS_RELATIVE
        catalog_path.parent.mkdir(parents=True)
        catalog_path.write_text(
            '{\n  "schema": "sod-modern.content-pack-catalog.v1",\n  "packs": []\n}\n',
            encoding="utf-8",
        )
        catalog_index = forge.ContentForgeIndex(
            root=temporary_root,
            features=index.features,
            packs=(),
            packs_by_id={},
            warnings=[],
        )
        draft = full_slice_pack(index)
        draft["id"] = "content-forge-catalog-save"
        catalog_plan = forge.content_pack_catalog_plan(catalog_index, pack_value=draft, mode="create")
        assert catalog_plan["operation"] == "created"
        assert "content-forge-catalog-save" in catalog_plan["unified_diff"]
        rehearsal = forge.content_pack_catalog_apply(
            catalog_index,
            pack_value=draft,
            mode="create",
            expected_catalog_plan_id=catalog_plan["catalog_plan_id"],
            expected_catalog_sha256=catalog_plan["catalog_target"]["base_sha256"],
            dry_run=True,
        )
        assert rehearsal["applied"] is False
        try:
            forge.content_pack_catalog_apply(
                catalog_index,
                pack_value=draft,
                mode="create",
                expected_catalog_plan_id=catalog_plan["catalog_plan_id"],
                expected_catalog_sha256=catalog_plan["catalog_target"]["base_sha256"],
                dry_run=False,
            )
        except forge.ContentForgeError as error:
            assert "confirmation" in str(error)
        else:
            raise AssertionError("Content Forge saved a catalog pack without the explicit confirmation phrase.")
        saved = forge.content_pack_catalog_apply(
            catalog_index,
            pack_value=draft,
            mode="create",
            expected_catalog_plan_id=catalog_plan["catalog_plan_id"],
            expected_catalog_sha256=catalog_plan["catalog_target"]["base_sha256"],
            dry_run=False,
            confirmation=forge.CONTENT_CATALOG_SAVE_CONFIRMATION,
        )
        assert saved["applied"] is True
        assert forge.load_pack_catalog(temporary_root)[0].id == draft["id"]
        draft["title"] = "Content Forge Catalog Replacement"
        replacement = forge.content_pack_catalog_plan(catalog_index, pack_value=draft, mode="replace")
        assert replacement["operation"] == "replaced"


if __name__ == "__main__":
    main()
    print("test_content_forge: OK")
