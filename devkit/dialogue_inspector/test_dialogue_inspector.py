"""Small self-contained checks for the standalone Dialogue Inspector."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "dialogue_inspector.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("devkit_dialogue_inspector", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RAW = '''\
dialogs = [
# [ src/dialogs/ZA_test/anyone_start.py:L1-L2 ] anyone::start->branch [] {fallback}
[anyone, "start", [], "Fallback", "branch", []],
# [ src/dialogs/ZA_test/anyone_start.py:L3-L4 ] anyone::start->branch [eq] {specific}
[anyone, "start", [(eq, "$flag", 1)], "Specific {s68}", "branch", [(str_store_string_reg, s2, s68)]],
# [ src/dialogs/ZA_test/anyone_branch.py:L1-L2 ] anyone|plyr::branch->close_window [] {reply}
[anyone|plyr, "branch", [], "Reply", "close_window", []],
]
'''


LIST_OPERATION_RAW = '''\
dialogs = [
# [ src/dialogs/ZA_test/anyone_start.py:L1-L2 ] anyone::start->close_window [eq] {guarded list syntax}
[anyone, "start", [[eq, "$flag", 1]], "Guarded", "close_window", [[str_store_string, s68, "str_guarded"]]],
]
'''


NEGATED_OPERATION_RAW = '''\
dialogs = [
# [ src/dialogs/ZA_test/anyone_start.py:L1-L2 ] anyone::start->close_window [neg|party_can_join] {guarded zero argument}
[anyone, "start", [neg|party_can_join], "Guarded", "close_window", []],
]
'''


def test_parser_preserves_order_and_source_provenance() -> None:
    tool = load_tool()
    entries = tool.parse_dialogue_entries(RAW)

    assert len(entries) == 3
    assert entries[0].index == 1
    assert entries[0].source.path == "src/dialogs/ZA_test/anyone_start.py"
    assert entries[1].condition_operations == ("eq",)
    assert entries[1].string_registers == ("s2", "s68")
    assert entries[1].string_stores[0].operation == "str_store_string_reg"
    assert entries[2].is_player


def test_fallback_shadow_detection_only_considers_npc_order() -> None:
    tool = load_tool()
    entries = tool.parse_dialogue_entries(RAW)
    findings = tool.ordering_sensitive_fallbacks(entries)

    assert len(findings) == 1
    assert findings[0][0].index == 1
    assert findings[0][1].index == 2


def test_legacy_list_operations_are_not_misclassified_as_fallbacks() -> None:
    tool = load_tool()
    entry = tool.parse_dialogue_entries(LIST_OPERATION_RAW)[0]

    assert entry.condition_operations == ("eq",)
    assert entry.consequence_operations == ("str_store_string",)
    assert entry.is_fallback is False
    assert entry.string_stores[0].target == "s68"


def test_negated_zero_argument_operations_are_not_fallbacks() -> None:
    tool = load_tool()
    entry = tool.parse_dialogue_entries(NEGATED_OPERATION_RAW)[0]

    assert entry.condition_operations == ("neg|party_can_join",)
    assert entry.is_fallback is False


def test_dot_is_a_state_graph() -> None:
    tool = load_tool()
    entries = tool.parse_dialogue_entries(RAW)
    rendered = tool.render_dot(tool.graph_selection(entries, "start", 2), "start")

    assert "digraph sod_modern_dialogue" in rendered
    assert '"start" -> "branch"' in rendered
    assert '"branch" -> "close_window"' in rendered


if __name__ == "__main__":
    test_parser_preserves_order_and_source_provenance()
    test_fallback_shadow_detection_only_considers_npc_order()
    test_legacy_list_operations_are_not_misclassified_as_fallbacks()
    test_negated_zero_argument_operations_are_not_fallbacks()
    test_dot_is_a_state_graph()
    print("test_dialogue_inspector: OK")
