"""Focused MCP coverage for Feature Authoring Compiler tools."""

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


FEATURE_TOOLS = {
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
        assert FEATURE_TOOLS <= listed
        catalog = payload(await client.call_tool("devkit_catalog"))
        manifest_tools = {item["name"] for item in catalog["manifest"]["mcp_tools"]}
        assert FEATURE_TOOLS <= manifest_tools

        summary = payload(await client.call_tool("feature_summary", {"limit": 5}))
        assert summary["feature_count"] >= 2
        assert summary["engine_entrypoint_count"] > 1_000

        found = payload(await client.call_tool("feature_find", {"query": "campaign dispatch", "limit": 3}))
        assert found["match_count"] >= 1
        assert found["features"][0]["id"] == "campaign-dispatch"

        entrypoints = payload(await client.call_tool("entrypoint_find", {"query": "sod_report_record_event", "family": "script", "limit": 30}))
        assert entrypoints["match_count"] >= 1
        exact = next(item for item in entrypoints["entrypoints"] if item["entrypoint_id"] == "entrypoint:script:sod_report_record_event")
        entrypoint_id = exact["entrypoint_id"]
        explained_entrypoint = payload(await client.call_tool("entrypoint_explain", {"entrypoint_id": entrypoint_id, "limit": 5}))
        assert explained_entrypoint["static_execution_trace"]["kind"] == "script_flow"

        validation = payload(await client.call_tool("feature_intent_validate", {"feature_id": "campaign-dispatch"}))
        assert validation["state"] == "ready"
        explained_feature = payload(await client.call_tool("feature_explain", {"feature_id": "campaign-dispatch", "trace_limit": 2}))
        assert explained_feature["validation"]["state"] == "ready"

        rendered = payload(await client.call_tool("feature_ir_render", {"operation": {"op": "call_script", "args": [{"reference": "script_sod_report_record_event"}]}}))
        assert rendered["source"] == '(call_script, "script_sod_report_record_event")'

        plan = payload(await client.call_tool("feature_plan", {"feature_id": "campaign-dispatch", "trace_limit": 2}))
        assert plan["state"] == "ready_for_review", plan
        assert plan["source_apply"]["available"] is False

        snapshot = payload(await client.call_tool("feature_semantic_snapshot", {"feature_id": "campaign-dispatch"}))
        diff = payload(await client.call_tool("feature_semantic_diff", {"feature_id": "campaign-dispatch", "before": snapshot}))
        assert diff["state"] == "unchanged", diff

        verification = payload(await client.call_tool("feature_verify", {"feature_id": "campaign-dispatch", "run_tests": False}))
        assert verification["state"] == "passed", verification


if __name__ == "__main__":
    asyncio.run(main())
    print("test_feature_authoring_tools: OK")
