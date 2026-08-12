"""Regression checks for the read-only string/register integrity analyzer."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.string_integrity import string_integrity as integrity


def test_register_model() -> None:
    assert integrity.operation_name(ast.parse("try_begin").body[0].value) == "try_begin"
    assert integrity.operation_name(ast.parse("neg|party_can_join").body[0].value) == "neg|party_can_join"
    assert integrity.operation_name(ast.parse("anyone").body[0].value) is None
    assert integrity.operation_name(ast.parse("assign").body[0].value) is None
    assert integrity.string_register(ast.parse("100").body[0].value, allow_numeric=True) == "s100"
    assert integrity.register_band("s67") == "legacy_volatile"
    assert integrity.register_band("s68") == "feature_scratch"
    assert integrity.register_band("s100") == "engine_extended_not_placeholder"
    assert integrity.register_band("s128") == "unsupported"

    direct_copy = integrity.writer_contract_issues(
        "str_store_string_reg", "s100", "s100", "direct"
    )
    assert direct_copy == []
    indirect_copy = integrity.writer_contract_issues(
        "str_store_string_reg", None, ":selector", "indirect"
    )
    assert indirect_copy[0]["code"] == "DYNAMIC_STRING_REGISTER_SOURCE_NOT_PROVEN"
    selector_ops = ast.parse(
        '[(store_random_in_range, ":selector", 11, 15)]'
    ).body[0].value.elts
    selectors: dict[str, integrity.SelectorBounds] = {}
    integrity.apply_selector_operation(selector_ops[0], selectors)
    assert (selectors[":selector"].minimum, selectors[":selector"].maximum) == (11, 14)
    bounded_copy = integrity.writer_contract_issues(
        "str_store_string_reg", None, ":selector", "indirect_bounded", (11, 14)
    )
    assert bounded_copy[0]["code"] == "DYNAMIC_STRING_REGISTER_SOURCE_BOUNDED"
    wrong_copy = integrity.writer_contract_issues(
        "str_store_string", "s4", "s4", None
    )
    assert wrong_copy[0]["code"] == "STR_STORE_STRING_REGISTER_COPY"

    legacy_list_operation = ast.parse(
        '[[str_store_string, s68, "str_guarded"]]'
    ).body[0].value.elts[0]
    assert integrity.operation_name(legacy_list_operation) == "str_store_string"
    assert integrity.writer_register_from_operation(legacy_list_operation) == "s68"


def test_workspace_report() -> None:
    report = integrity.build_integrity_report(REPO_ROOT)
    summary = report["summary"]

    assert report["scope"]["read_only"] is True
    assert report["module_errors"] == []
    assert summary["text_sink_count"] > 8_000
    assert summary["source_mapped_sink_count"] > 8_000
    assert summary["sink_count_by_category"]["dialogue"] > 4_000
    assert summary["sink_count_by_category"]["menu"] > 2_000
    assert summary["sink_count_by_category"]["message"] > 1_000

    past_life = next(
        sink for sink in report["sinks"] if sink["context"] == "past_life_explanation"
    )
    assert past_life["control_flow_present"] is True
    assert past_life["compile_column"] == 0
    assert past_life["status"] in {"clean", "info"}
    assert all(
        issue["code"] != "DYNAMIC_STRING_REGISTER_SOURCE_NOT_PROVEN"
        for assessment in past_life["register_assessments"]
        for issue in assessment["issues"]
    )

    result = integrity.query_sinks(
        report,
        kind="dialogue",
        register=5,
        include_clean=True,
        limit=2,
    )
    assert result["filters"]["register"] == "s5"
    assert result["match_count"] >= result["returned_count"] > 0
    assert result["returned_count"] <= 2

    payload = integrity.summary_payload(report, limit=3)
    assert payload["summary"] == summary
    assert "String Integrity Summary" in integrity.render_markdown(payload)


def test_generated_builder_script_effects_are_visible() -> None:
    modules, errors = integrity.load_modules(REPO_ROOT)
    assert errors == []
    script_module = next(
        module for module in modules if module.relative_path == "compile/module_scripts.py"
    )
    effects = integrity.script_effects_from_module(script_module)

    # This is emitted as ``_build_get_center_modifier_ops()`` inside the
    # generated scripts list.  It is real runtime script content, not a
    # missing symbol or an unconstrained script-clobber boundary.
    modifier = effects["script_sod_get_center_modifier"]
    assert modifier.direct_writes == set()
    assert modifier.transitive_writes == set()
    assert modifier.transitive_unknown is False


if __name__ == "__main__":
    test_register_model()
    test_workspace_report()
    test_generated_builder_script_effects_are_visible()
    print("test_string_integrity: OK")
