"""Focused in-memory and STDIO MCP regression checks for Campaign State Doctor."""

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
    assert value["provenance"]["read_only"] is True
    return value


async def verify_campaign_state_tools(client: Client) -> None:
    tools = {tool.name for tool in (await client.list_tools()).tools}
    assert {
        "campaign_state_summary",
        "campaign_state_findings",
        "campaign_state_resource",
        "campaign_state_timeline",
        "campaign_state_contracts",
    } <= tools

    summary = payload(await client.call_tool("campaign_state_summary", {"limit": 3}))
    assert summary["data"]["source"]["script_count"] > 1_000
    assert summary["data"]["contracts"]["failed_count"] == 0

    contract = payload(
        await client.call_tool(
            "campaign_state_contracts",
            {"contract_id": "black_khergit_camped_ai_stationary"},
        )
    )
    assert contract["data"]["passed_count"] == 1

    resource = payload(
        await client.call_tool(
            "campaign_state_resource",
            {"resource": "slot_party_black_khergit_origin", "limit": 3},
        )
    )
    assert resource["data"]["resource_count"] > 0

    timeline = payload(
        await client.call_tool(
            "campaign_state_timeline",
            {"resource": "party_ai_behavior::camp_party:behavior", "limit": 5},
        )
    )
    assert timeline["data"]["event_count"] > 0

    findings = payload(
        await client.call_tool(
            "campaign_state_findings",
            {"severity": "warning", "limit": 2},
        )
    )
    assert findings["data"]["finding_count"] >= 0


async def main() -> None:
    async with Client(mcp) as client:
        await verify_campaign_state_tools(client)
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_DIR / "server.py")],
        cwd=REPO_ROOT,
    )
    async with Client(stdio_client(params)) as client:
        await verify_campaign_state_tools(client)


if __name__ == "__main__":
    asyncio.run(main())
    print("test_campaign_state_tools: OK")
