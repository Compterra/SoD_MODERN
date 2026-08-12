"""Focused MCP regression coverage for deterministic dialogue creation.

The full server suite deliberately exercises every DevKit slice and can exceed
interactive command limits.  This narrow test proves the new creation contract
through both in-memory and real STDIO MCP transports without writing source.
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


def payload(result):
    value = result.structured_content
    assert isinstance(value, dict)
    assert value["contract_version"] == "devkit.tool-result.v1"
    assert value["ok"] is True
    assert isinstance(value["data"], dict)
    return value


async def verify_creator(client: Client) -> None:
    tools = {tool.name for tool in (await client.list_tools()).tools}
    assert {"dialogue_create_plan", "dialogue_create_apply"} <= tools

    found = payload(
        await client.call_tool("dialogue_find", {"input_state": "bandit_attack", "limit": 1})
    )
    anchor_route_id = found["data"]["routes"][0]["route_id"]
    spec = {
        "anchor_route_id": anchor_route_id,
        "position": "after",
        "speaker": "plyr",
        "input_state": "devkit_deterministic_creator_test",
        "text": "@Deterministic creation transport rehearsal.",
        "output_state": "close_window",
        "conditions": [],
        "consequences": [],
    }
    plan = payload(await client.call_tool("dialogue_create_plan", {"spec": spec}))
    assert plan["tool"] == "dialogue_create_plan"
    plan_data = plan["data"]
    assert plan_data["prospective_route"]["input_state"] == spec["input_state"]
    assert plan_data["change_router_plan"]["unified_diff"]

    rehearsal = payload(
        await client.call_tool(
            "dialogue_create_apply",
            {
                "spec": spec,
                "expected_sha256": plan_data["change_router_plan"]["target"]["base_sha256"],
                "expected_plan_id": plan_data["change_router_plan"]["plan_id"],
                "dry_run": True,
            },
        )
    )
    assert rehearsal["tool"] == "dialogue_create_apply"
    assert rehearsal["provenance"]["read_only"] is True
    assert rehearsal["data"]["result"]["applied"] is False


async def main() -> None:
    async with Client(mcp) as client:
        await verify_creator(client)
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_DIR / "server.py")],
        cwd=REPO_ROOT,
    )
    async with Client(stdio_client(params)) as client:
        await verify_creator(client)


if __name__ == "__main__":
    asyncio.run(main())
    print("test_dialogue_create_tools: OK")
