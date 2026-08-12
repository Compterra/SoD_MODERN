"""Focused MCP coverage for Content Forge tools."""

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


CONTENT_FORGE_TOOLS = {
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
}


def payload(result):
    value = result.structured_content
    assert isinstance(value, dict)
    assert value["contract_version"] == "devkit.tool-result.v1"
    assert value["ok"] is True, value
    return value["data"]


async def main() -> None:
    async with Client(mcp) as client:
        listed = {tool.name for tool in (await client.list_tools()).tools}
        assert CONTENT_FORGE_TOOLS <= listed
        catalog = payload(await client.call_tool("devkit_catalog"))
        manifest_tools = {item["name"] for item in catalog["manifest"]["mcp_tools"]}
        assert CONTENT_FORGE_TOOLS <= manifest_tools

        summary = payload(await client.call_tool("content_forge_summary", {"limit": 5}))
        assert summary["pack_count"] >= 1
        found = payload(await client.call_tool("content_pack_find", {"query": "black khergit", "slice": "campaign_ai", "limit": 5}))
        assert found["match_count"] >= 1
        assert found["packs"][0]["id"] == "black-khergit-camp-runtime"

        common = {"pack_id": "black-khergit-camp-runtime"}
        explained = payload(await client.call_tool("content_pack_explain", {**common, "trace_limit": 2}))
        assert explained["state"] == "ready", explained
        validation = payload(await client.call_tool("content_pack_validate", common))
        assert validation["state"] == "ready", validation
        compiled = payload(await client.call_tool("content_pack_compile", common))
        assert compiled["state"] == "ready", compiled
        plan = payload(await client.call_tool("content_pack_plan", {**common, "trace_limit": 2}))
        assert plan["state"] == "ready_for_review", plan
        review = payload(await client.call_tool("content_pack_review", {**common, "trace_limit": 2}))
        assert review["review_canvas"]["mermaid"].startswith("flowchart TD")
        preview = payload(await client.call_tool("content_pack_preview", {**common, "trace_limit": 2}))
        assert preview["state"] == "ready_for_review", preview
        snapshot = payload(await client.call_tool("content_pack_snapshot", common))
        difference = payload(await client.call_tool("content_pack_semantic_diff", {**common, "before": snapshot}))
        assert difference["state"] == "unchanged", difference
        catalog_draft = dict(explained["pack_source"])
        catalog_draft["description"] = catalog_draft["description"] + " [MCP catalog-plan coverage]"
        catalog_plan = payload(await client.call_tool("content_pack_catalog_plan", {"pack": catalog_draft, "mode": "replace"}))
        assert catalog_plan["catalog_target"]["path"] == "devkit/content_forge/packs.json"
        catalog_rehearsal = payload(
            await client.call_tool(
                "content_pack_catalog_apply",
                {
                    "pack": catalog_draft,
                    "mode": "replace",
                    "expected_catalog_plan_id": catalog_plan["catalog_plan_id"],
                    "expected_catalog_sha256": catalog_plan["catalog_target"]["base_sha256"],
                    "dry_run": True,
                },
            )
        )
        assert catalog_rehearsal["applied"] is False
        verification = payload(await client.call_tool("content_pack_verify", {**common, "run_scenarios": False}))
        assert verification["state"] == "passed", verification


if __name__ == "__main__":
    asyncio.run(main())
    print("test_content_forge_tools: OK")
