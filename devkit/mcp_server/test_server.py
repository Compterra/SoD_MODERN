"""Integration tests for the local DevKit MCP server.

The first test uses the SDK's in-memory client; the second opens the same
server through real stdio so an accidental stdout print corrupting the protocol
is caught before Codex is asked to launch it.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


SERVER_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVER_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.mcp_server.server import mcp


EXPECTED_TOOLS = {
    "devkit_catalog",
    "devkit_health",
    "dialogue_summary",
    "dialogue_routes",
    "dialogue_entry",
    "dialogue_model_summary",
    "dialogue_model_findings",
    "dialogue_model_state",
    "dialogue_model_route",
    "dialogue_composer_summary",
    "dialogue_find",
    "dialogue_context",
    "dialogue_create_plan",
    "dialogue_create_apply",
    "dialogue_patch",
    "dialogue_apply",
    "dialogue_verify",
    "string_trace",
    "string_integrity",
    "text_export_parity",
    "rgl_log_analyze",
    "rgl_log_contract",
    "release_gate",
    "blueprint_summary",
    "blueprint_find",
    "blueprint_explain",
    "blueprint_compile",
    "blueprint_verify",
    "feature_summary",
    "feature_find",
    "entrypoint_find",
    "entrypoint_explain",
    "feature_explain",
    "feature_intent_validate",
    "feature_ir_render",
    "feature_plan",
    "feature_apply",
    "feature_verify",
    "feature_semantic_snapshot",
    "feature_semantic_diff",
    "content_forge_summary",
    "content_pack_find",
    "content_pack_explain",
    "content_pack_validate",
    "content_pack_compile",
    "content_pack_plan",
    "content_pack_preview",
    "content_pack_review",
    "content_pack_apply",
    "content_pack_verify",
    "content_pack_snapshot",
    "content_pack_semantic_diff",
    "content_pack_catalog_plan",
    "content_pack_catalog_apply",
    "campaign_state_summary",
    "campaign_state_findings",
    "campaign_state_resource",
    "campaign_state_timeline",
    "campaign_state_contracts",
    "campaign_ai_intents",
    "slot_lifecycle_summary",
    "slot_lifecycle_findings",
    "slot_lifecycle_ownership",
    "slot_lifecycle_slot",
    "campaign_scenario_summary",
    "campaign_scenario_catalog",
    "campaign_scenario_fuzz",
    "text_explain",
    "register_history",
    "possible_texts",
    "string_provenance_summary",
    "string_provenance_paths",
    "string_provenance_explain",
    "semantic_change_snapshot",
    "semantic_change_diff",
    "presentation_layout_summary",
    "presentation_find",
    "presentation_canvas",
    "presentation_preview",
    "presentation_patch",
    "presentation_apply",
    "presentation_verify",
    "module_atlas_summary",
    "module_integrity",
    "module_find",
    "module_context",
    "module_graph",
    "menu_flow",
    "script_flow",
    "mission_timeline",
    "trigger_timeline",
    "quest_registry",
    "entity_references",
    "module_patch",
    "module_apply",
    "module_verify",
    "order_summary",
    "order_map",
    "order_explain",
    "order_risk",
    "order_plan_move",
    "order_apply_move",
    "order_contracts",
    "order_baseline",
    "order_diff",
    "order_verify",
    "balance_summary",
    "balance_find_items",
    "balance_item",
    "balance_find_troops",
    "balance_troop",
    "balance_upgrade_tree",
    "balance_roster_inventory",
    "balance_progression",
    "balance_campaign_cohorts",
    "balance_imperial_invasion",
    "balance_player_start_factions",
    "balance_player_start_progression",
    "balance_native_kingdoms",
    "balance_mercenary_guilds",
    "balance_faith_ascensions",
    "balance_compare",
    "balance_outliers",
    "balance_patch",
    "balance_apply",
    "balance_verify",
    "workbench_summary",
    "workbench_doctor",
    "workbench_impact",
    "workbench_scope_check",
    "workbench_text_lint",
    "workbench_order_report",
    "workbench_contract_drift",
    "workbench_contract_baseline",
    "workbench_coverage",
    "workbench_scenarios",
    "workbench_scenario_run",
    "workbench_release_readiness",
    "workbench_draft",
    "change_router_summary",
    "code_find",
    "linked_context",
    "change_impact",
    "patch_plan",
    "apply_source_edits",
    "verify_change",
    "dialogue_graph",
    "workspace_audit",
}
RESULT_SCHEMA = json.loads(
    (REPO_ROOT / "devkit" / "contracts" / "tool-result.v1.schema.json").read_text(encoding="utf-8")
)


def validate_result_envelope(payload) -> None:
    """Validate the checked-in envelope without an undeclared test dependency."""

    assert isinstance(payload, dict)
    properties = RESULT_SCHEMA["properties"]
    assert set(payload) <= set(properties)
    assert set(RESULT_SCHEMA["required"]) <= set(payload)
    assert payload["contract_version"] == properties["contract_version"]["const"]
    assert isinstance(payload["tool"], str) and payload["tool"]
    assert isinstance(payload["ok"], bool)
    assert isinstance(payload["data"], dict)
    assert isinstance(payload["warnings"], list)
    assert all(isinstance(warning, str) for warning in payload["warnings"])
    provenance = payload["provenance"]
    provenance_schema = properties["provenance"]
    assert isinstance(provenance, dict)
    assert set(provenance) <= set(provenance_schema["properties"])
    assert set(provenance_schema["required"]) <= set(provenance)
    assert isinstance(provenance["repo_root"], str)
    assert isinstance(provenance["read_only"], bool)
    assert isinstance(provenance["server_version"], str)


def structured(result):
    payload = result.structured_content
    validate_result_envelope(payload)
    return payload


async def verify_client(client: Client) -> None:
    listed = await client.list_tools()
    assert EXPECTED_TOOLS <= {tool.name for tool in listed.tools}

    catalog = structured(await client.call_tool("devkit_catalog"))
    assert catalog["ok"] is True
    assert catalog["data"]["manifest"]["name"] == "sod-modern-devkit"

    health = structured(await client.call_tool("devkit_health"))
    assert health["ok"] is True
    assert health["tool"] == "devkit_health"
    assert health["data"]["dialogue_entry_count"] > 1000

    summary = structured(await client.call_tool("dialogue_summary", {"max_findings": 3}))
    assert summary["ok"] is True
    assert summary["data"]["top_states_total"] >= 3

    routes = structured(
        await client.call_tool(
            "dialogue_routes",
            {"start_state": "sod_company_spokesperson_response", "limit": 2},
        )
    )
    assert routes["ok"] is True
    assert routes["data"]["match_count"] >= 2
    assert len(routes["data"]["entries"]) == 2

    entry = structured(await client.call_tool("dialogue_entry", {"entry_index": 3}))
    assert entry["ok"] is True
    assert entry["data"]["entry"]["index"] == 3

    composer_summary = structured(await client.call_tool("dialogue_composer_summary"))
    assert composer_summary["ok"] is True
    assert composer_summary["data"]["route_count"] > 4_000

    authored_routes = structured(
        await client.call_tool(
            "dialogue_find",
            {"input_state": "bandit_attack", "limit": 2},
        )
    )
    assert authored_routes["ok"] is True
    authored_route = authored_routes["data"]["routes"][0]
    authored_route_id = authored_route["route_id"]

    authored_context = structured(
        await client.call_tool(
            "dialogue_context",
            {"route_id": authored_route_id, "max_lines": 24, "related_limit": 5},
        )
    )
    assert authored_context["ok"] is True
    assert authored_context["data"]["first_match_analysis"]["static_only"] is True

    create_spec = {
        "anchor_route_id": authored_route_id,
        "position": "after",
        "speaker": "plyr",
        "input_state": "devkit_mcp_created_choice",
        "text": "@Deterministic MCP creation rehearsal.",
        "output_state": "close_window",
        "conditions": [],
        "consequences": [],
    }
    create_plan = structured(
        await client.call_tool("dialogue_create_plan", {"spec": create_spec})
    )
    assert create_plan["ok"] is True
    assert create_plan["data"]["prospective_route"]["input_state"] == "devkit_mcp_created_choice"
    create_sha = create_plan["data"]["change_router_plan"]["target"]["base_sha256"]
    create_plan_id = create_plan["data"]["change_router_plan"]["plan_id"]
    create_rehearsal = structured(
        await client.call_tool(
            "dialogue_create_apply",
            {
                "spec": create_spec,
                "expected_sha256": create_sha,
                "expected_plan_id": create_plan_id,
                "dry_run": True,
            },
        )
    )
    assert create_rehearsal["ok"] is True
    assert create_rehearsal["provenance"]["read_only"] is True
    assert create_rehearsal["data"]["result"]["applied"] is False

    authored_patch = structured(
        await client.call_tool(
            "dialogue_patch",
            {
                "route_id": authored_route_id,
                "action": "replace_text",
                "value": "{s5} [semantic rehearsal]",
            },
        )
    )
    assert authored_patch["ok"] is True
    authored_sha = authored_patch["data"]["change_router_plan"]["target"]["base_sha256"]
    assert "semantic rehearsal" in authored_patch["data"]["change_router_plan"]["unified_diff"]

    authored_rehearsal = structured(
        await client.call_tool(
            "dialogue_apply",
            {
                "route_id": authored_route_id,
                "action": "replace_text",
                "value": "{s5} [semantic rehearsal]",
                "expected_sha256": authored_sha,
                "dry_run": True,
            },
        )
    )
    assert authored_rehearsal["ok"] is True
    assert authored_rehearsal["provenance"]["read_only"] is True
    assert authored_rehearsal["data"]["result"]["applied"] is False

    authored_verified = structured(
        await client.call_tool(
            "dialogue_verify",
            {"route_id": authored_route_id, "expected_sha256": authored_sha, "max_tests": 1},
        )
    )
    assert authored_verified["ok"] is True
    assert authored_verified["data"]["change_router_verification"]["syntax"]["passed"] is True

    trace = structured(
        await client.call_tool(
            "string_trace",
            {"query": "Then the company will be paid now.", "limit_per_layer": 2},
        )
    )
    assert trace["ok"] is True
    layers = {hit["layer"] for hit in trace["data"]["hits"]}
    assert {"modular source", "generated dialogue module", "exported conversation"} <= layers

    integrity = structured(
        await client.call_tool(
            "string_integrity",
            {"kind": "dialogue", "register": 5, "include_clean": True, "limit": 2},
        )
    )
    assert integrity["ok"] is True
    assert integrity["data"]["summary"]["text_sink_count"] > 8_000
    assert integrity["data"]["filters"]["register"] == "s5"
    assert integrity["data"]["returned_count"] <= 2

    export_parity = structured(
        await client.call_tool(
            "text_export_parity",
            {"scope": "text", "max_diffs": 2, "timeout_seconds": 90},
        )
    )
    assert export_parity["ok"] is True
    assert export_parity["provenance"]["read_only"] is True
    assert export_parity["data"]["summary"]["checked_file_count"] >= 10
    assert export_parity["data"]["safety"]["live_workspace_unchanged"] is True

    rgl_contract = structured(await client.call_tool("rgl_log_contract", {"limit": 3}))
    assert rgl_contract["ok"] is True
    assert rgl_contract["data"]["passed"] is True

    rgl_log = structured(
        await client.call_tool(
            "rgl_log_analyze",
            {
                "log_path": str(REPO_ROOT / "devkit" / "rgl_log_sentinel" / "fixtures" / "stale_party_simulation.rgl"),
                "limit": 3,
            },
        )
    )
    assert rgl_log["ok"] is True
    assert rgl_log["data"]["summary"]["invalid_party_faction_cascade_count"] == 1
    assert rgl_log["data"]["clusters"][0]["current_contract"]["state"] == "covered_pass"

    campaign_state = structured(
        await client.call_tool("campaign_state_summary", {"limit": 3})
    )
    assert campaign_state["ok"] is True
    assert campaign_state["data"]["source"]["script_count"] > 1_000
    assert campaign_state["data"]["contracts"]["failed_count"] == 0

    state_contract = structured(
        await client.call_tool(
            "campaign_state_contracts",
            {"contract_id": "black_khergit_camped_ai_stationary"},
        )
    )
    assert state_contract["ok"] is True
    assert state_contract["data"]["passed_count"] == 1

    state_resource = structured(
        await client.call_tool(
            "campaign_state_resource",
            {"resource": "slot_party_black_khergit_origin", "limit": 3},
        )
    )
    assert state_resource["ok"] is True
    assert state_resource["data"]["resource_count"] > 0

    state_timeline = structured(
        await client.call_tool(
            "campaign_state_timeline",
            {"resource": "party_ai_behavior::camp_party:behavior", "limit": 5},
        )
    )
    assert state_timeline["ok"] is True
    assert state_timeline["data"]["event_count"] > 0

    state_findings = structured(
        await client.call_tool(
            "campaign_state_findings",
            {"severity": "warning", "query": "temporal", "limit": 2},
        )
    )
    assert state_findings["ok"] is True

    explained = structured(
        await client.call_tool(
            "text_explain",
            {"query": "past_life", "kind": "menu", "limit": 1, "max_steps": 30},
        )
    )
    assert explained["ok"] is True
    ledger_entry = explained["data"]["explanations"][0]
    assert ledger_entry["execution_context"]["menu"]["menu_id"] == "past_life_explanation"
    assert ledger_entry["global_state_dependencies"][0]["symbol"] == "$current_string_reg"

    history = structured(
        await client.call_tool(
            "register_history",
            {"symbol": "$current_string_reg", "limit": 10},
        )
    )
    assert history["ok"] is True
    assert history["data"]["workspace_writer_count"] >= 3

    possible = structured(
        await client.call_tool(
            "possible_texts",
            {"query": "bandit_attack", "kind": "dialogue", "limit": 1},
        )
    )
    assert possible["ok"] is True
    assert possible["data"]["entries"][0]["possible_text"]["substitutions"]

    presentation_summary = structured(await client.call_tool("presentation_layout_summary"))
    assert presentation_summary["ok"] is True
    assert presentation_summary["data"]["presentation_count"] >= 20

    presentation_matches = structured(
        await client.call_tool("presentation_find", {"query": "sliders", "limit": 2})
    )
    assert presentation_matches["ok"] is True
    presentation = presentation_matches["data"]["presentations"][0]
    presentation_key = presentation["presentation_key"]
    overlay_id = presentation["overlays"][0]["overlay_id"]

    canvas = structured(
        await client.call_tool(
            "presentation_canvas",
            {"presentation_id": presentation_key, "overlay_limit": 20},
        )
    )
    assert canvas["ok"] is True
    assert canvas["data"]["canvas"]["returned_overlay_count"] > 0

    preview = structured(
        await client.call_tool(
            "presentation_preview",
            {"presentation_id": presentation_key, "output_name": "mcp-sliders-preview.svg"},
        )
    )
    assert preview["ok"] is True
    assert preview["provenance"]["read_only"] is False
    assert (REPO_ROOT / preview["data"]["artifact"]["path"]).is_file()

    presentation_patch = structured(
        await client.call_tool(
            "presentation_patch",
            {"target": overlay_id, "action": "move_overlay", "x": 601, "y": 201},
        )
    )
    assert presentation_patch["ok"] is True
    presentation_sha = presentation_patch["data"]["change_router_plan"]["target"]["base_sha256"]
    assert presentation_patch["data"]["semantic_operation"]["shared_binding_impact"]

    presentation_rehearsal = structured(
        await client.call_tool(
            "presentation_apply",
            {
                "target": overlay_id,
                "action": "move_overlay",
                "x": 601,
                "y": 201,
                "expected_sha256": presentation_sha,
                "dry_run": True,
            },
        )
    )
    assert presentation_rehearsal["ok"] is True
    assert presentation_rehearsal["provenance"]["read_only"] is True
    assert presentation_rehearsal["data"]["result"]["applied"] is False

    presentation_verified = structured(
        await client.call_tool(
            "presentation_verify",
            {"target": overlay_id, "expected_sha256": presentation_sha, "max_tests": 1},
        )
    )
    assert presentation_verified["ok"] is True
    assert presentation_verified["data"]["change_router_verification"]["syntax"]["passed"] is True

    atlas_summary = structured(await client.call_tool("module_atlas_summary"))
    assert atlas_summary["ok"] is True
    assert atlas_summary["data"]["source_area_count"] == 8
    assert atlas_summary["data"]["entity_count"] > 13_000

    atlas_integrity = structured(await client.call_tool("module_integrity", {"limit": 3}))
    assert atlas_integrity["ok"] is True
    assert atlas_integrity["data"]["syntax_error_count"] == 0
    assert atlas_integrity["data"]["generated_id_fallback_entity_count"] > 100

    atlas_found = structured(
        await client.call_tool(
            "module_find",
            {"query": "past_life_explanation", "area": "menus", "limit": 3},
        )
    )
    assert atlas_found["ok"] is True
    atlas_menu = next(
        entity
        for entity in atlas_found["data"]["entities"]
        if entity["kind"] == "menu"
    )
    atlas_menu_id = atlas_menu["entity_id"]

    atlas_context = structured(
        await client.call_tool(
            "module_context",
            {"entity_id": atlas_menu_id, "max_lines": 24, "related_limit": 5},
        )
    )
    assert atlas_context["ok"] is True
    assert atlas_context["data"]["entity"]["name"] == "past_life_explanation"

    atlas_graph = structured(
        await client.call_tool(
            "module_graph",
            {"entity_id": atlas_menu_id, "direction": "outgoing", "depth": 1, "max_nodes": 20},
        )
    )
    assert atlas_graph["ok"] is True
    assert atlas_graph["data"]["node_count"] >= 1

    atlas_menu_flow = structured(
        await client.call_tool("menu_flow", {"menu_id": "past_life_explanation", "depth": 1, "max_nodes": 20})
    )
    assert atlas_menu_flow["ok"] is True
    assert atlas_menu_flow["data"]["options"]

    atlas_script_flow = structured(
        await client.call_tool("script_flow", {"script_name": "sod_battle_xp_log_start", "depth": 1, "max_nodes": 20})
    )
    assert atlas_script_flow["ok"] is True
    assert atlas_script_flow["data"]["operation_summary"]["operation_count"] > 0

    atlas_mission_timeline = structured(
        await client.call_tool("mission_timeline", {"mission_id": "bandits_at_night", "depth": 1, "max_nodes": 20})
    )
    assert atlas_mission_timeline["ok"] is True
    assert atlas_mission_timeline["data"]["trigger_count"] > 0

    atlas_trigger_timeline = structured(
        await client.call_tool("trigger_timeline", {"limit": 3})
    )
    assert atlas_trigger_timeline["ok"] is True
    assert atlas_trigger_timeline["data"]["returned_count"] <= 3

    atlas_quests = structured(await client.call_tool("quest_registry", {"limit": 3}))
    assert atlas_quests["ok"] is True
    assert atlas_quests["data"]["match_count"] > 50

    atlas_references = structured(
        await client.call_tool("entity_references", {"symbol": "sod_migration_prosperity_max", "limit": 3})
    )
    assert atlas_references["ok"] is True
    assert atlas_references["data"]["definition_count"] == 1

    atlas_patch = structured(
        await client.call_tool(
            "module_patch",
            {
                "entity_id": atlas_menu_id,
                "action": "set_text",
                "value": "{s3} [atlas semantic rehearsal]",
            },
        )
    )
    assert atlas_patch["ok"] is True
    atlas_sha = atlas_patch["data"]["change_router_plan"]["target"]["base_sha256"]
    assert "atlas semantic rehearsal" in atlas_patch["data"]["change_router_plan"]["unified_diff"]

    atlas_rehearsal = structured(
        await client.call_tool(
            "module_apply",
            {
                "entity_id": atlas_menu_id,
                "action": "set_text",
                "value": "{s3} [atlas semantic rehearsal]",
                "expected_sha256": atlas_sha,
                "dry_run": True,
            },
        )
    )
    assert atlas_rehearsal["ok"] is True
    assert atlas_rehearsal["provenance"]["read_only"] is True
    assert atlas_rehearsal["data"]["result"]["applied"] is False

    atlas_verified = structured(
        await client.call_tool(
            "module_verify",
            {"entity_id": atlas_menu_id, "expected_sha256": atlas_sha, "max_tests": 1},
        )
    )
    assert atlas_verified["ok"] is True
    assert atlas_verified["data"]["change_router_verification"]["syntax"]["passed"] is True

    order_summary = structured(await client.call_tool("order_summary"))
    assert order_summary["ok"] is True
    assert order_summary["data"]["contracts"]["active_blocker_count"] == 0

    order_map = structured(
        await client.call_tool(
            "order_map",
            {"area": "menus", "domain": "source-fragments", "query": "past_life_explanation", "limit": 5},
        )
    )
    assert order_map["ok"] is True
    order_target = order_map["data"]["groups"][0]["records"][0]["fragment_id"]
    order_explained = structured(await client.call_tool("order_explain", {"target": order_target, "related_limit": 5}))
    assert order_explained["ok"] is True
    assert order_explained["data"]["fragment"]["path"].endswith("past_life_explanation.py")

    protected_target = "source:src/menus/0000_hardcoded_mb1011/tutorial.py"
    protected_anchor = "source:src/menus/0000_hardcoded_mb1011/start_game_1.py"
    order_risk = structured(
        await client.call_tool(
            "order_risk",
            {"target": protected_target, "anchor": protected_anchor, "position": "before"},
        )
    )
    assert order_risk["ok"] is True
    assert order_risk["data"]["risk"]["level"] == "critical"
    order_plan = structured(
        await client.call_tool(
            "order_plan_move",
            {"target": protected_target, "anchor": protected_anchor, "position": "before"},
        )
    )
    assert order_plan["ok"] is True
    assert order_plan["data"]["plan_kind"] == "fragment_manifest_move"
    order_sha = order_plan["data"]["order_manifest_plan"]["base_sha256"]
    order_rehearsal = structured(
        await client.call_tool(
            "order_apply_move",
            {
                "target": protected_target,
                "anchor": protected_anchor,
                "position": "before",
                "expected_sha256": order_sha,
                "dry_run": True,
            },
        )
    )
    assert order_rehearsal["ok"] is True
    assert order_rehearsal["provenance"]["read_only"] is True
    assert order_rehearsal["data"]["applied"] is False

    order_contracts = structured(await client.call_tool("order_contracts"))
    assert order_contracts["ok"] is True
    assert order_contracts["data"]["summary"]["active_blocker_count"] == 0
    order_baseline = structured(await client.call_tool("order_baseline", {"label": "mcp-order", "overwrite": True}))
    assert order_baseline["ok"] is True
    assert order_baseline["provenance"]["read_only"] is False
    assert (REPO_ROOT / order_baseline["data"]["artifact"]["path"]).is_file()
    order_diff = structured(await client.call_tool("order_diff", {"baseline": "mcp-order", "limit": 3}))
    assert order_diff["ok"] is True
    assert order_diff["data"]["summary"]["source_change_count"] == 0
    order_verify = structured(await client.call_tool("order_verify", {"baseline": "mcp-order", "limit": 3}))
    assert order_verify["ok"] is True
    assert order_verify["data"]["state"] == "structural_order_ready_for_review"

    balance_summary = structured(await client.call_tool("balance_summary"))
    assert balance_summary["ok"] is True
    assert balance_summary["data"]["authoring"]["confirmed"] is True
    assert balance_summary["data"]["items"]["count"] > 900
    assert balance_summary["data"]["troops"]["id_contract"]["passed"] is True

    balance_items = structured(
        await client.call_tool("balance_find_items", {"query": "khergit bow", "limit": 3})
    )
    assert balance_items["ok"] is True
    assert balance_items["data"]["match_count"] >= 1
    balance_item = structured(
        await client.call_tool("balance_item", {"item_id": "itm_khergit_bow", "troop_limit": 3})
    )
    assert balance_item["ok"] is True
    assert balance_item["data"]["item"]["editable_stat_calls"]

    balance_troops = structured(
        await client.call_tool("balance_find_troops", {"query": "swadian recruit", "include_heroes": False, "limit": 3})
    )
    assert balance_troops["ok"] is True
    assert balance_troops["data"]["match_count"] >= 1
    balance_troop = structured(
        await client.call_tool("balance_troop", {"troop_id": "trp_swadian_recruit", "item_limit": 3})
    )
    assert balance_troop["ok"] is True
    assert balance_troop["data"]["troop"]["kit_analysis"]["role"]
    balance_tree = structured(
        await client.call_tool("balance_upgrade_tree", {"troop_id": "trp_swadian_recruit", "depth": 2, "limit": 20})
    )
    assert balance_tree["ok"] is True
    assert balance_tree["data"]["node_count"] >= 2
    balance_rosters = structured(await client.call_tool("balance_roster_inventory", {"roster_limit": 1}))
    assert balance_rosters["ok"] is True
    assert balance_rosters["data"]["mode"] == "catalog"
    assert balance_rosters["data"]["returned_roster_count"] == 1
    assert balance_rosters["data"]["rosters_truncated"] is True
    balance_antarian_inventory = structured(
        await client.call_tool("balance_roster_inventory", {"roster": "Antarian", "troop_limit": 3, "item_limit": 3})
    )
    assert balance_antarian_inventory["ok"] is True
    assert balance_antarian_inventory["data"]["mode"] == "inventory"
    assert balance_antarian_inventory["data"]["roster"]["name"] == "Antarian"
    balance_antarian_progression = structured(
        await client.call_tool("balance_progression", {"roster": "Antarian", "troop_limit": 3, "edge_limit": 3})
    )
    assert balance_antarian_progression["ok"] is True
    assert balance_antarian_progression["data"]["mode"] == "progression"
    assert balance_antarian_progression["data"]["rank_evidence"]["faith_ascension_mapping"]
    balance_antarian_cohort = structured(
        await client.call_tool("balance_campaign_cohorts", {"cohort": "Player start: Antarian", "troop_limit": 3})
    )
    assert balance_antarian_cohort["ok"] is True
    assert balance_antarian_cohort["data"]["mode"] == "cohort"
    assert balance_antarian_cohort["data"]["cohort"]["campaign_role"] == "mutually_exclusive_player_start"
    balance_imperial = structured(await client.call_tool("balance_imperial_invasion", {"include_auxiliaries": True}))
    assert balance_imperial["ok"] is True
    assert balance_imperial["data"]["mode"] == "imperial_invasion_profile"
    assert balance_imperial["data"]["core_wave_count"] == 3
    balance_player_starts = structured(await client.call_tool("balance_player_start_factions"))
    assert balance_player_starts["ok"] is True
    assert balance_player_starts["data"]["state"] == "within_static_balance_targets"
    assert balance_player_starts["data"]["player_start_culture_count"] == 5
    balance_player_progression = structured(await client.call_tool("balance_player_start_progression"))
    assert balance_player_progression["ok"] is True
    assert balance_player_progression["data"]["state"] == "within_static_progression_targets"
    assert balance_player_progression["data"]["route_count"] == 52
    balance_native_kingdoms = structured(await client.call_tool("balance_native_kingdoms"))
    assert balance_native_kingdoms["ok"] is True
    assert balance_native_kingdoms["data"]["state"] == "within_static_balance_targets"
    assert balance_native_kingdoms["data"]["kingdom_count"] == 5
    balance_mercenary_guilds = structured(await client.call_tool("balance_mercenary_guilds"))
    assert balance_mercenary_guilds["ok"] is True
    assert balance_mercenary_guilds["data"]["state"] == "within_static_niche_targets"
    assert balance_mercenary_guilds["data"]["guild_count"] == 7
    balance_faith = structured(await client.call_tool("balance_faith_ascensions"))
    assert balance_faith["ok"] is True
    assert balance_faith["data"]["state"] == "within_static_tier_targets"
    assert balance_faith["data"]["route_count"] == 25
    balance_compare = structured(
        await client.call_tool("balance_compare", {"entity_ids": ["itm_khergit_bow", "itm_strong_bow"]})
    )
    assert balance_compare["ok"] is True
    assert len(balance_compare["data"]["item_comparison"]) == 2
    balance_outliers = structured(await client.call_tool("balance_outliers", {"domain": "items", "limit": 3}))
    assert balance_outliers["ok"] is True
    assert balance_outliers["data"]["finding_count"] >= 1
    balance_patch = structured(
        await client.call_tool("balance_patch", {"entity_kind": "item", "entity_id": "itm_khergit_bow", "changes": {"price": 1234}})
    )
    assert balance_patch["ok"] is True
    assert balance_patch["data"]["unified_diff"]
    balance_rehearsal = structured(
        await client.call_tool(
            "balance_apply",
            {
                "entity_kind": "item",
                "entity_id": "itm_khergit_bow",
                "changes": {"price": 1234},
                "expected_sha256": balance_patch["data"]["target"]["base_sha256"],
                "expected_plan_sha256": balance_patch["data"]["plan_sha256"],
                "dry_run": True,
            },
        )
    )
    assert balance_rehearsal["ok"] is True
    assert balance_rehearsal["provenance"]["read_only"] is True
    assert balance_rehearsal["data"]["applied"] is False
    balance_verify = structured(await client.call_tool("balance_verify", {"limit": 3}))
    assert balance_verify["ok"] is True
    assert balance_verify["data"]["state"] == "ready_for_build_review"

    workbench_doctor = structured(await client.call_tool("workbench_doctor"))
    assert workbench_doctor["ok"] is True
    assert workbench_doctor["data"]["ready"] is True

    workbench_summary = structured(await client.call_tool("workbench_summary"))
    assert workbench_summary["ok"] is True
    assert workbench_summary["data"]["atlas"]["entity_count"] > 13_000
    assert workbench_summary["data"]["contracts"]["contract_count"] >= 4

    workbench_impact = structured(
        await client.call_tool("workbench_impact", {"target": "past_life_explanation", "limit": 4})
    )
    assert workbench_impact["ok"] is True
    assert workbench_impact["data"]["target"]["primary_entity_id"] == atlas_menu_id
    assert workbench_impact["data"]["change_impact"]["direct_generated_outputs"] == ["compile/module_game_menus.py"]

    workbench_scope = structured(
        await client.call_tool(
            "workbench_scope_check",
            {"entity_id": atlas_menu_id, "depth": "fast"},
        )
    )
    assert workbench_scope["ok"] is True
    assert workbench_scope["data"]["verification"]["syntax"]["passed"] is True

    workbench_lint = structured(
        await client.call_tool("workbench_text_lint", {"kind": "menu", "severity": "warning", "limit": 2})
    )
    assert workbench_lint["ok"] is True
    assert workbench_lint["data"]["summary"]["text_sink_count"] > 8_000

    workbench_order = structured(await client.call_tool("workbench_order_report", {"baseline": "mcp-order", "limit": 3}))
    assert workbench_order["ok"] is True
    assert workbench_order["data"]["state"] == "structural_order_ready_for_review"

    workbench_contracts = structured(await client.call_tool("workbench_contract_drift"))
    assert workbench_contracts["ok"] is True
    assert workbench_contracts["data"]["summary"]["contract_count"] >= 4

    workbench_baseline = structured(
        await client.call_tool("workbench_contract_baseline", {"label": "mcp-contract"})
    )
    assert workbench_baseline["ok"] is True
    assert workbench_baseline["provenance"]["read_only"] is False
    assert (REPO_ROOT / workbench_baseline["data"]["artifact"]["path"]).is_file()

    workbench_coverage = structured(
        await client.call_tool("workbench_coverage", {"area": "menus", "query": "past_life_explanation", "limit": 5})
    )
    assert workbench_coverage["ok"] is True
    assert workbench_coverage["data"]["match_count"] >= 1

    workbench_scenarios = structured(await client.call_tool("workbench_scenarios"))
    assert workbench_scenarios["ok"] is True
    assert workbench_scenarios["data"]["summary"]["scenario_count"] >= 3

    workbench_scenario = structured(
        await client.call_tool("workbench_scenario_run", {"scenario_id": "atlas-structure-sentinel", "timeout_seconds": 90})
    )
    assert workbench_scenario["ok"] is True
    assert workbench_scenario["data"]["passed"] is True

    workbench_release = structured(await client.call_tool("workbench_release_readiness"))
    assert workbench_release["ok"] is True
    assert "never certifies" in workbench_release["data"]["evidence_boundary"]

    workbench_draft = structured(
        await client.call_tool(
            "workbench_draft",
            {"kind": "menu", "title": "MCP Workbench Draft", "output_name": "mcp-workbench-draft.json", "overwrite": True},
        )
    )
    assert workbench_draft["ok"] is True
    assert workbench_draft["provenance"]["read_only"] is False
    assert (REPO_ROOT / workbench_draft["data"]["artifact"]["path"]).is_file()

    router_summary = structured(await client.call_tool("change_router_summary"))
    assert router_summary["ok"] is True
    assert router_summary["data"]["summary"]["source_fragment_count"] > 5_000

    found = structured(
        await client.call_tool(
            "code_find",
            {"query": "past_life", "scope": "source", "limit": 5},
        )
    )
    assert found["ok"] is True
    router_target = next(
        match["target_id"]
        for match in found["data"]["matches"]
        if match["path"].endswith("past_life_explanation.py")
    )

    linked = structured(
        await client.call_tool(
            "linked_context",
            {
                "target_id": router_target,
                "focus_line": 12,
                "max_lines": 20,
                "related_limit": 10,
            },
        )
    )
    assert linked["ok"] is True
    assert linked["data"]["target"]["area"] == "menus"
    assert "$current_string_reg" in linked["data"]["relationships"]["globals"]["reads"]

    impact = structured(
        await client.call_tool(
            "change_impact",
            {"target_id": router_target, "related_limit": 10},
        )
    )
    assert impact["ok"] is True
    assert impact["data"]["direct_generated_outputs"] == ["compile/module_game_menus.py"]

    edits = [
        {
            "old_text": "mnf_disable_all_keys",
            "new_text": "mnf_disable_all_keys | 0",
            "expected_occurrences": 1,
        }
    ]
    planned = structured(
        await client.call_tool(
            "patch_plan",
            {"target_id": router_target, "edits": edits},
        )
    )
    assert planned["ok"] is True
    plan = planned["data"]
    assert plan["unified_diff"]

    rehearsed = structured(
        await client.call_tool(
            "apply_source_edits",
            {
                "target_id": router_target,
                "edits": edits,
                "expected_sha256": plan["target"]["base_sha256"],
                "dry_run": True,
            },
        )
    )
    assert rehearsed["ok"] is True
    assert rehearsed["provenance"]["read_only"] is True
    assert rehearsed["data"]["applied"] is False

    verified = structured(
        await client.call_tool(
            "verify_change",
            {
                "target_id": router_target,
                "expected_sha256": plan["target"]["base_sha256"],
                "max_tests": 1,
            },
        )
    )
    assert verified["ok"] is True
    assert verified["data"]["syntax"]["passed"] is True

    graph = structured(
        await client.call_tool(
            "dialogue_graph",
            {"start_state": "sod_company_spokesperson_response", "depth": 1},
        )
    )
    assert graph["ok"] is True
    assert graph["data"]["route_count"] >= 15
    assert graph["data"]["edges"]

    rejected_graph = structured(await client.call_tool("dialogue_graph"))
    assert rejected_graph["ok"] is False
    assert "start_state" in rejected_graph["data"]["error"]

    audit = structured(await client.call_tool("workspace_audit", {"max_items": 3}))
    assert audit["ok"] is True
    report = audit["data"]["audit"]
    assert report["scope"]["read_only"] is True
    assert report["source"]["file_count"] > 5000
    assert report["pipeline"]["legacy_processor_count"] >= 20


async def test_in_memory_server() -> None:
    async with Client(mcp) as client:
        await verify_client(client)


async def verify_stdio_smoke(client: Client) -> None:
    """Keep real-STDIO coverage fast while the in-memory pass owns deep scans."""

    listed = await client.list_tools()
    assert EXPECTED_TOOLS <= {tool.name for tool in listed.tools}

    catalog = structured(await client.call_tool("devkit_catalog"))
    assert catalog["ok"] is True

    routes = structured(
        await client.call_tool(
            "dialogue_find",
            {"input_state": "bandit_attack", "limit": 1},
        )
    )
    assert routes["ok"] is True
    anchor_route_id = routes["data"]["routes"][0]["route_id"]
    spec = {
        "anchor_route_id": anchor_route_id,
        "position": "after",
        "speaker": "plyr",
        "input_state": "devkit_stdio_created_choice",
        "text": "@Deterministic STDIO creation rehearsal.",
        "output_state": "close_window",
        "conditions": [],
        "consequences": [],
    }
    plan = structured(await client.call_tool("dialogue_create_plan", {"spec": spec}))
    assert plan["ok"] is True
    rehearsal = structured(
        await client.call_tool(
            "dialogue_create_apply",
            {
                "spec": spec,
                "expected_sha256": plan["data"]["change_router_plan"]["target"]["base_sha256"],
                "expected_plan_id": plan["data"]["change_router_plan"]["plan_id"],
                "dry_run": True,
            },
        )
    )
    assert rehearsal["ok"] is True
    assert rehearsal["provenance"]["read_only"] is True


async def test_stdio_server() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_DIR / "server.py")],
        cwd=REPO_ROOT,
    )
    async with Client(stdio_client(params)) as client:
        await verify_stdio_smoke(client)


if __name__ == "__main__":
    asyncio.run(test_in_memory_server())
    asyncio.run(test_stdio_server())
    print("test_server: OK")
