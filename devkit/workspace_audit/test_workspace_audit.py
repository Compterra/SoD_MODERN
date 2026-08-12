"""Read-only regression checks for the workspace architecture audit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.workspace_audit import workspace_audit


def test_worktree_status_scopes_safe_directory() -> None:
    calls: list[tuple[list[str], dict[str, object]]] = []

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout=" M src/example.py\n", stderr="")

    original_run = workspace_audit.subprocess.run
    workspace_audit.subprocess.run = fake_run
    try:
        result = workspace_audit.worktree_status(REPO_ROOT, maximum=2)
    finally:
        workspace_audit.subprocess.run = original_run

    expected_root = REPO_ROOT.resolve()
    assert calls == [
        (
            [
                "git",
                "-c",
                f"safe.directory={expected_root}",
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            {
                "cwd": expected_root,
                "check": False,
                "capture_output": True,
                "text": True,
                "encoding": "utf-8",
                "errors": "replace",
                "timeout": 15,
            },
        )
    ]
    assert result["available"] is True
    assert result["dirty_entry_count"] == 1


def main() -> None:
    test_worktree_status_scopes_safe_directory()
    report = workspace_audit.audit_workspace(REPO_ROOT, max_items=4)

    assert report["scope"]["read_only"] is True
    assert report["source"]["file_count"] > 5000
    assert report["source"]["physical_line_count"] > 200000
    assert report["generated_compile"]["module_file_count"] >= 25
    assert report["exports"]["live_root_file_count"] >= 25
    assert report["pipeline"]["legacy_processor_count"] >= 20
    assert report["validation_surface"]["standalone_build_test_file_count"] >= 200

    contracts = {item["id"]: item for item in report["ordering"]["contracts"]}
    assert contracts["dialogs"]["candidate_fragment_count"] > 4000
    assert contracts["dialogs"]["missing_listed_count"] == 0
    assert contracts["dialogs"]["unlisted_candidate_count"] == 0

    entities = {item["id"]: item for item in report["entities"]}
    assert entities["dialogs"]["static_assignment_element_count"] > 4000
    assert entities["scripts"]["static_assignment_element_count"] > 1000
    assert entities["dialogs"]["source_marker_comment_count"] > 4000

    markdown = workspace_audit.render_markdown(report)
    assert "# SoD Modern Workspace Audit" in markdown
    assert "compiled_order_controls_dialogue_flow" in markdown
    print("test_workspace_audit: OK")


if __name__ == "__main__":
    main()
