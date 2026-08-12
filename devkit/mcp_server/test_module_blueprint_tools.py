"""Focused MCP coverage for the read-only Module Blueprint Compiler tools."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import Client


SERVER_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVER_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.mcp_server.server import mcp


BLUEPRINT_TOOLS = {
    "blueprint_summary",
    "blueprint_find",
    "blueprint_explain",
    "blueprint_compile",
    "blueprint_verify",
}


def payload(result):
    value = result.structured_content
    assert isinstance(value, dict)
    assert value["contract_version"] == "devkit.tool-result.v1"
    assert value["ok"] is True, value
    assert value["provenance"]["read_only"] is True
    return value["data"]


async def main() -> None:
    async with Client(mcp) as client:
        listed = {tool.name for tool in (await client.list_tools()).tools}
        assert BLUEPRINT_TOOLS <= listed

        catalog = payload(await client.call_tool("devkit_catalog"))
        manifest_tools = {item["name"] for item in catalog["manifest"]["mcp_tools"]}
        assert BLUEPRINT_TOOLS <= manifest_tools

        summary = payload(await client.call_tool("blueprint_summary", {"limit": 5}))
        assert summary["verification"]["state"] == "ready_for_review", summary
        assert summary["coverage"]["blueprint_count"] >= 2

        found = payload(await client.call_tool("blueprint_find", {"query": "black khergit", "limit": 3}))
        assert found["match_count"] >= 1
        assert found["blueprints"][0]["id"] == "black-khergit-camped-horde"

        explained = payload(await client.call_tool("blueprint_explain", {"blueprint_id": "campaign-dispatch"}))
        assert explained["evaluation"]["state"] == "ready"
        assert len(explained["evaluation"]["order_constraints"]) == 2

        plan = payload(await client.call_tool("blueprint_compile", {"blueprint_id": "campaign-dispatch", "limit": 10}))
        assert plan["state"] == "ready_for_review", plan
        assert plan["source_apply"]["available"] is False
        assert "compile/module_game_menus.py" in plan["source_plan"]["generated_modules_affected"]

        verification = payload(await client.call_tool("blueprint_verify", {"blueprint_id": "black-khergit-camped-horde", "limit": 10}))
        assert verification["state"] == "passed", verification


if __name__ == "__main__":
    asyncio.run(main())
    print("test_module_blueprint_tools: OK")
