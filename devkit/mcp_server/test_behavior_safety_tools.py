"""Focused MCP checks for the behavior-safety DevKit slices.

The in-memory client exercises every new tool's structured result.  A smaller
real-STDIO pass proves that the server remains protocol-clean when Codex
launches it as a local process.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


SERVER_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVER_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.mcp_server.server import mcp


NEW_TOOLS = {
    "dialogue_model_summary",
    "dialogue_model_findings",
    "dialogue_model_state",
    "dialogue_model_route",
    "campaign_ai_intents",
    "slot_lifecycle_summary",
    "slot_lifecycle_findings",
    "slot_lifecycle_ownership",
    "slot_lifecycle_slot",
    "campaign_scenario_summary",
    "campaign_scenario_catalog",
    "campaign_scenario_fuzz",
    "string_provenance_summary",
    "string_provenance_paths",
    "string_provenance_explain",
    "semantic_change_snapshot",
    "semantic_change_diff",
}


def payload(result):
    value = result.structured_content
    assert isinstance(value, dict)
    assert value["contract_version"] == "devkit.tool-result.v1"
    assert value["ok"] is True, value
    assert isinstance(value["data"], dict)
    assert value["provenance"]["read_only"] is True
    return value["data"]


async def verify_full_surface(client: Client) -> None:
    tools = {tool.name for tool in (await client.list_tools()).tools}
    assert NEW_TOOLS <= tools
    catalog = payload(await client.call_tool("devkit_catalog"))
    assert NEW_TOOLS <= {item["name"] for item in catalog["manifest"]["mcp_tools"]}

    dialogue = payload(await client.call_tool("dialogue_model_summary", {"limit": 2}))
    assert dialogue["coverage"]["route_count"] > 1_000
    assert dialogue["coverage"]["route_statuses"]["model_boundary_unproven"] > 0
    assert "groups" in payload(await client.call_tool("dialogue_model_state", {"state": "start", "limit": 2}))
    assert "route" in payload(await client.call_tool("dialogue_model_route", {"route_index": 1}))
    assert "findings" in payload(await client.call_tool("dialogue_model_findings", {"severity": "error", "limit": 1}))

    intents = payload(await client.call_tool("campaign_ai_intents"))
    assert intents["passed_count"] >= 1
    slots = payload(await client.call_tool("slot_lifecycle_summary", {"limit": 2}))
    assert slots["coverage"]["ownership_rule_count"] >= 1
    assert payload(await client.call_tool("slot_lifecycle_findings", {"severity": "info", "limit": 1}))["finding_count"] >= 0
    owners = payload(await client.call_tool("slot_lifecycle_ownership", {"slot": "black_khergit", "limit": 2}))
    assert owners["rule_count"] >= 1
    assert payload(await client.call_tool("slot_lifecycle_slot", {"slot": "slot_party_black_khergit_origin", "limit": 2}))["slot_count"] >= 1

    scenarios = payload(await client.call_tool("campaign_scenario_summary"))
    assert scenarios["coverage"]["scenario_count"] >= 1
    catalog = payload(await client.call_tool("campaign_scenario_catalog", {"scenario_id": "black-khergit-camped-lock"}))
    assert catalog["scenario_count"] == 1
    fuzz = payload(
        await client.call_tool(
            "campaign_scenario_fuzz",
            {"scenario_id": "black-khergit-camped-lock", "iterations": 2, "seed": 9, "trace_limit": 20},
        )
    )
    assert fuzz["status"] == "passed", fuzz

    provenance = payload(await client.call_tool("string_provenance_summary", {"limit": 2}))
    assert provenance["coverage"]["script_count"] > 1_000
    paths = payload(
        await client.call_tool(
            "string_provenance_paths",
            {"script_symbol": "script_sod_black_khergits_lock_camped_ai", "register": "s68", "limit": 2},
        )
    )
    assert paths["script_symbol"] == "script_sod_black_khergits_lock_camped_ai"
    explained = payload(
        await client.call_tool(
            "string_provenance_explain",
            {"query": "Black Khergit", "kind": "dialogue", "limit": 1, "max_paths": 2},
        )
    )
    assert "explanations" in explained

    snapshot = payload(await client.call_tool("semantic_change_snapshot"))
    assert snapshot["snapshot"]["schema"] == "devkit.semantic-change-snapshot.v1"


async def verify_stdio_surface(client: Client) -> None:
    tools = {tool.name for tool in (await client.list_tools()).tools}
    assert NEW_TOOLS <= tools
    fuzz = payload(
        await client.call_tool(
            "campaign_scenario_fuzz",
            {"scenario_id": "black-khergit-camped-lock", "iterations": 1, "seed": 11, "trace_limit": 10},
        )
    )
    assert fuzz["status"] == "passed", fuzz
    assert payload(await client.call_tool("dialogue_model_summary", {"limit": 1}))["coverage"]["route_count"] > 1_000


async def main() -> None:
    async with Client(mcp) as client:
        await verify_full_surface(client)
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_DIR / "server.py")],
        cwd=REPO_ROOT,
    )
    async with Client(stdio_client(params)) as client:
        await verify_stdio_surface(client)


if __name__ == "__main__":
    asyncio.run(main())
    print("test_behavior_safety_tools: OK")
