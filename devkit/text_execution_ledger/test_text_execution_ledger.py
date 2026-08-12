"""Regression checks for the LLM-first text execution ledger."""

from __future__ import annotations

import sys
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.text_execution_ledger import text_execution_ledger as ledger


def test_workspace_ledger() -> None:
    index = ledger.build_ledger(REPO_ROOT)
    summary = ledger.ledger_summary(index)

    assert summary["generated_module_count"] == 8
    assert summary["operation_count"] > 150_000
    assert summary["visible_sink_count"] > 8_000
    assert summary["menu_transition_count"] > 1_000
    assert summary["known_script_effect_count"] > 1_000

    bandit = ledger.explain(
        index,
        query="bandit_attack",
        kind="dialogue",
        limit=1,
        max_steps=30,
    )
    explanation = bandit["explanations"][0]
    assert explanation["execution_context"]["type"] == "dialogue"
    substitution = explanation["possible_text"]["substitutions"][0]
    assert substitution["dynamic_selector"]["bounds"] == [11, 14]
    assert len(substitution["dynamic_selector"]["candidates"]) == 4
    assert explanation["sink"]["compile_column"] == 0

    past_life = ledger.explain(
        index,
        query="past_life",
        kind="menu",
        limit=1,
        max_steps=30,
    )
    menu_explanation = past_life["explanations"][0]
    assert menu_explanation["execution_context"]["menu"]["menu_id"] == "past_life_explanation"
    operations = [
        event["name"]
        for section in menu_explanation["display_timeline"]["sections"]
        for event in section["events"]
    ]
    assert {"try_begin", "else_try", "try_end"} <= set(operations)
    global_dependency = menu_explanation["global_state_dependencies"][0]
    assert global_dependency["symbol"] == "$current_string_reg"
    assert global_dependency["workspace_writer_count"] >= 3

    history = ledger.register_history(index, "$current_string_reg", limit=20)
    assert history["symbol_kind"] == "global"
    assert history["workspace_writer_count"] >= 3
    assert history["events"]

    possible = ledger.possible_texts(
        index,
        query="bandit_attack",
        kind="dialogue",
        limit=1,
    )
    assert possible["entries"][0]["possible_text"]["substitutions"]

    markdown = ledger.render_markdown(bandit)
    assert "Text Execution Ledger" in markdown


if __name__ == "__main__":
    test_workspace_ledger()
    print("test_text_execution_ledger: OK")
