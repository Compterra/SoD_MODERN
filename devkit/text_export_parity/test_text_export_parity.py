"""Regression checks for the isolated text-export parity staging boundary."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.text_export_parity import text_export_parity as parity


FAKE_PROCESSOR = '''from pathlib import Path
from module_info import export_dir

Path(export_dir).mkdir(parents=True, exist_ok=True)
(Path(export_dir) / "strings.txt").write_bytes(b"stringsfile version 1\\n1\\nstr_safe staged_text\\n")
'''

WARNING_PROCESSOR = FAKE_PROCESSOR + "\nprint('WARNING: fixture staged warning')\n"


def fixture_root(base: Path) -> Path:
    root = base / "module"
    (root / "compile" / "ids").mkdir(parents=True)
    (root / "compile" / "process").mkdir(parents=True)
    (root / "_export").mkdir(parents=True)
    (root / "compile" / "module_strings.py").write_text("strings = []\n", encoding="utf-8")
    (root / "compile" / "process" / "process_fixture.py").write_text(FAKE_PROCESSOR, encoding="utf-8")
    return root


def test_isolated_processor_does_not_touch_live_export() -> None:
    with tempfile.TemporaryDirectory(prefix="text-export-parity-test-") as temporary:
        root = fixture_root(Path(temporary))
        live = root / "_export" / "strings.txt"
        live.write_text("stringsfile version 1\n1\nstr_safe live_text\n", encoding="utf-8")

        report = parity.build_export_parity_report(
            root,
            max_diffs=3,
            timeout_seconds=10,
            _processors=("process_fixture.py",),
            _files=("strings.txt",),
        )

        assert report["scope"]["read_only"] is True
        assert report["safety"]["live_workspace_unchanged"] is True
        assert report["summary"]["state"] == "mismatch"
        assert live.read_text(encoding="utf-8").endswith("live_text\n")
        strings = report["compile_to_export"]["files"][0]
        assert strings["status"] == "mismatch"
        assert strings["first_difference"]["first_different_line"] == 3


def test_matching_output_and_line_endings_are_semantic_parity() -> None:
    with tempfile.TemporaryDirectory(prefix="text-export-parity-test-") as temporary:
        root = fixture_root(Path(temporary))
        live = root / "_export" / "strings.txt"
        live.write_bytes(b"stringsfile version 1\r\n1\r\nstr_safe staged_text\r\n")

        report = parity.build_export_parity_report(
            root,
            max_diffs=3,
            timeout_seconds=10,
            _processors=("process_fixture.py",),
            _files=("strings.txt",),
        )

        assert report["safety"]["live_workspace_unchanged"] is True
        assert report["summary"]["matched_file_count"] == 1
        strings = report["compile_to_export"]["files"][0]
        assert strings["status"] == "match_normalized_line_endings"
        assert strings["raw_byte_match"] is False
        assert strings["normalized_text_match"] is True


def test_quick_string_delta_separates_stale_records_from_order() -> None:
    staged = b"2\nqstr_alpha Alpha\nqstr_beta Beta\n"
    live = b"3\nqstr_beta Beta\nqstr_stale Stale\nqstr_alpha Alpha\n"

    delta = parity.quick_string_delta(staged, live, limit=5)

    assert delta == {
        "parseable": True,
        "live_entry_count": 3,
        "staged_entry_count": 2,
        "same_entry_multiset": False,
        "live_only_count": 1,
        "staged_only_count": 0,
        "live_only": ["qstr_stale Stale"],
        "staged_only": [],
        "truncated": False,
    }


def test_stage_command_retains_warning_count_when_output_is_clipped() -> None:
    with tempfile.TemporaryDirectory(prefix="text-export-parity-warning-test-") as temporary:
        root = fixture_root(Path(temporary))
        (root / "compile" / "process" / "process_warning.py").write_text(WARNING_PROCESSOR, encoding="utf-8")
        (root / "_export" / "strings.txt").write_bytes(b"stringsfile version 1\n1\nstr_safe staged_text\n")

        report = parity.build_export_parity_report(
            root,
            max_diffs=3,
            timeout_seconds=10,
            _processors=("process_warning.py",),
            _files=("strings.txt",),
        )

        diagnostics = report["compile_to_export"]["processor_results"][0]["diagnostics"]
        assert diagnostics["warning_count"] == 1
        assert diagnostics["error_count"] == 0
        assert diagnostics["items"] == [{"severity": "warning", "line": "WARNING: fixture staged warning"}]


if __name__ == "__main__":
    test_isolated_processor_does_not_touch_live_export()
    test_matching_output_and_line_endings_are_semantic_parity()
    test_quick_string_delta_separates_stale_records_from_order()
    test_stage_command_retains_warning_count_when_output_is_clipped()
    print("test_text_export_parity: OK")
