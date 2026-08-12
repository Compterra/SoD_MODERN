"""Focused deterministic tests for RGL Log Sentinel."""

from __future__ import annotations

import tempfile
import sys
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.rgl_log_sentinel import rgl_log_sentinel as sentinel


FIXTURE = TOOL_DIR / "fixtures" / "stale_party_simulation.rgl"


def test_parser_groups_multiple_errors_from_one_rgl_line() -> None:
    events = sentinel.parse_script_errors(FIXTURE.read_text(encoding="utf-8"))
    assert len(events) == 4
    assert [event["resource_kind"] for event in events] == ["party", "faction", "party", "faction"]
    assert [event["resource_id"] for event in events] == [525, 154201176, 523, 154201176]
    assert all(event["script"] == "game_event_simulate_battle" for event in events)


def test_analysis_finds_the_invalid_party_to_faction_cascade() -> None:
    report = sentinel.analyze_log(REPO_ROOT, log_path=FIXTURE, limit=20)
    assert report["summary"]["script_error_count"] == 4
    assert report["summary"]["invalid_party_faction_cascade_count"] == 1
    cluster = report["clusters"][0]
    assert cluster["category"] == "invalid_party_faction_cascade"
    assert cluster["invalid_party_ids"] == [523, 525]
    assert cluster["invalid_faction_ids"] == [154201176]
    assert cluster["engine_operations"] == [
        {"opcode": 2190, "name": "store_relation"},
        {"opcode": 2204, "name": "store_faction_of_party"},
    ]
    assert report["script_errors"][0]["opcode_name"] == "store_faction_of_party"
    assert cluster["provenance"]["source"]["state"] == "found"
    assert cluster["provenance"]["generated"]["state"] == "found"
    assert cluster["provenance"]["export"]["state"] == "found"
    assert cluster["provenance"]["script_id"] == 2
    assert cluster["current_contract"]["state"] == "covered_pass"
    assert report["summary"]["state"] == "runtime_error_observed_source_contract_passes"


def test_warning_classifier_distinguishes_known_startup_noise_and_assets() -> None:
    warnings = sentinel.parse_warnings(FIXTURE.read_text(encoding="utf-8"))
    categories = {warning["category"]: warning for warning in warnings}
    assert categories["mb1011_optional_presentation_mapping"]["actionable"] is False
    assert categories["missing_material"]["actionable"] is True
    assert categories["missing_material"]["subject"] == "cyclo_costumes_lod"
    assert categories["engine_buffer_growth"]["actionable"] is False
    groups, truncated = sentinel.summarize_warnings(warnings + warnings, limit=10)
    assert truncated is False
    material_group = next(group for group in groups if group["category"] == "missing_material")
    assert material_group["count"] == 2


def test_live_export_hash_check_detects_a_stale_deployment() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / "workspace"
        export = root / "_export"
        live = Path(temp) / "live"
        export.mkdir(parents=True)
        live.mkdir()
        (export / "scripts.txt").write_text("new scripts\n", encoding="utf-8")
        (export / "strings.txt").write_text("new strings\n", encoding="utf-8")
        (live / "scripts.txt").write_text("old scripts\n", encoding="utf-8")
        (live / "strings.txt").write_text("new strings\n", encoding="utf-8")
        result = sentinel.compare_live_export(root, live, limit=10)
        assert result["state"] == "mismatch"
        assert result["scripts_txt_state"] == "mismatch"
        assert result["matching_file_count"] == 1
        assert result["mismatch_file_count"] == 1


def test_engine_callback_contract_passes_current_source_and_rejects_missing_guard() -> None:
    report = sentinel.engine_callback_contract_report(REPO_ROOT)
    assert report["passed"] is True, report
    source = REPO_ROOT / "src" / "scripts" / "ZA_hardcoded_game_scripts" / "game_event_simulate_battle.py"
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        target = root / "src" / "scripts" / "ZA_hardcoded_game_scripts" / source.name
        target.parent.mkdir(parents=True)
        target.write_text(
            source.read_text(encoding="utf-8").replace('(party_is_active, ":root_attacker_party"),\n', "", 1),
            encoding="utf-8",
        )
        broken = sentinel.engine_callback_contract_report(root)
        assert broken["passed"] is False
        assert any(finding["check_id"] == "active_guard_before_party_read::root_attacker_party" for finding in broken["findings"])


def main() -> None:
    test_parser_groups_multiple_errors_from_one_rgl_line()
    test_analysis_finds_the_invalid_party_to_faction_cascade()
    test_warning_classifier_distinguishes_known_startup_noise_and_assets()
    test_live_export_hash_check_detects_a_stale_deployment()
    test_engine_callback_contract_passes_current_source_and_rejects_missing_guard()
    print("test_rgl_log_sentinel: OK")


if __name__ == "__main__":
    main()
