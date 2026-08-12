#!/usr/bin/env python3
"""Replay the M&B 1.011 text export pipeline safely in temporary staging.

Count parity cannot prove that quick-string indices or inline dialogue/menu
text stayed aligned. This tool copies the legacy compile inputs to a system
temporary directory, reruns the fixed processor order there, and compares the
staged result with the live export. It never invokes the live build or writes
the real ``compile/`` and ``_export/`` directories.

With ``source_build=True`` it first rebuilds the source-derived generated
modules in staging, proving source -> generated -> export parity rather than
only generated -> export parity.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


PARITY_VERSION = "1.2.0"
TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]

# Mirrors build_module.bat except process_global_variables_unused.py. That
# final script writes a report rather than an export, so it is deliberately not
# run in a diagnostic whose safety contract is no live writes.
PROCESSOR_ORDER: tuple[str, ...] = (
    "process_init.py",
    "process_global_variables.py",
    "process_strings.py",
    "process_skills.py",
    "process_music.py",
    "process_animations.py",
    "process_meshes.py",
    "process_sounds.py",
    "process_skins.py",
    "process_map_icons.py",
    "process_factions.py",
    "process_items.py",
    "process_scenes.py",
    "process_troops.py",
    "process_particle_sys.py",
    "process_scene_props.py",
    "process_tableau_materials.py",
    "process_presentations.py",
    "process_party_tmps.py",
    "process_parties.py",
    "process_quests.py",
    "process_scripts.py",
    "process_mission_tmps.py",
    "process_game_menus.py",
    "process_simple_triggers.py",
    "process_dialogs.py",
)

SOURCE_BUILDER_ORDER: tuple[str, ...] = (
    "build/build_constants.py",
    "build/build_quests.py",
    "build/build_scripts.py",
    "build/build_simple_triggers.py",
    "build/build_game_menus.py",
    "build/build_dialogs.py",
    "build/build_presentations.py",
    "build/build_mission_templates.py",
)

# Default target list: every export that directly contains visible text or can
# contain display strings/quick-string references which decide player-visible
# text. Provenance is deliberately explicit instead of implied from a filename.
TEXT_EXPORT_PROVENANCE: dict[str, dict[str, Any]] = {
    "strings.txt": {"compile_modules": ["compile/module_strings.py"], "source_areas": ["legacy_compile"]},
    "quick_strings.txt": {
        "compile_modules": [
            "compile/module_dialogs.py", "compile/module_game_menus.py",
            "compile/module_mission_templates.py", "compile/module_presentations.py",
            "compile/module_quests.py", "compile/module_scripts.py",
            "compile/module_simple_triggers.py", "compile/module_triggers.py",
        ],
        "source_areas": ["dialogs", "menus", "mission_templates", "presentations", "quests", "scripts", "triggers", "legacy_compile"],
    },
    "conversation.txt": {"compile_modules": ["compile/module_dialogs.py"], "source_areas": ["dialogs"]},
    "dialog_states.txt": {"compile_modules": ["compile/module_dialogs.py"], "source_areas": ["dialogs"]},
    "menus.txt": {"compile_modules": ["compile/module_game_menus.py"], "source_areas": ["menus"]},
    "presentations.txt": {"compile_modules": ["compile/module_presentations.py"], "source_areas": ["presentations"]},
    "simple_triggers.txt": {"compile_modules": ["compile/module_simple_triggers.py"], "source_areas": ["triggers"]},
    "scripts.txt": {"compile_modules": ["compile/module_scripts.py"], "source_areas": ["scripts"]},
    "mission_templates.txt": {"compile_modules": ["compile/module_mission_templates.py"], "source_areas": ["mission_templates"]},
    "quests.txt": {"compile_modules": ["compile/module_quests.py"], "source_areas": ["quests"]},
    "triggers.txt": {"compile_modules": ["compile/module_triggers.py", "compile/module_dialogs.py"], "source_areas": ["legacy_compile", "dialogs"]},
}

# ``module.ini`` and ``map.txt`` are copied from external inputs, not generated
# from module records, so they are intentionally absent.
ALL_GENERATED_EXPORTS: tuple[str, ...] = (
    "actions.txt", "conversation.txt", "dialog_states.txt", "factions.txt", "item_kinds1.txt",
    "map_icons.txt", "menus.txt", "meshes.txt", "mission_templates.txt", "music.txt",
    "particle_systems.txt", "parties.txt", "party_templates.txt", "presentations.txt",
    "quests.txt", "quick_strings.txt", "scene_props.txt", "scenes.txt", "scripts.txt",
    "simple_triggers.txt", "skills.txt", "skins.txt", "sounds.txt", "strings.txt",
    "tableau_materials.txt", "tag_uses.txt", "triggers.txt", "troops.txt",
    "variable_uses.txt", "variables.txt",
)

SOURCE_GENERATED_MODULES: tuple[str, ...] = (
    "module_constants.py", "module_quests.py", "module_scripts.py", "module_simple_triggers.py",
    "module_game_menus.py", "module_dialogs.py", "module_presentations.py", "module_mission_templates.py",
)

# Legacy builders and processors sometimes report a non-fatal diagnostic while
# still returning zero.  Preserve a bounded structured count separately from
# the clipped command transcript so higher-level release checks cannot miss a
# warning merely because a command wrote more than the transcript limit.
STAGE_DIAGNOSTIC_RE = re.compile(r"(?im)^\s*(?:\[[^\]\r\n]+\]\s*)?(WARNING|ERROR)\s*:")
MAX_STAGE_DIAGNOSTIC_PREVIEW = 20


class TextExportParityError(RuntimeError):
    """The isolated parity replay cannot be completed safely."""


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def hash_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise TextExportParityError(f"Could not read {path}: {error}") from error


def file_hash(path: Path) -> str | None:
    return hash_bytes(read_bytes(path)) if path.is_file() else None


def normalized_newlines(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def decode_evidence(raw: bytes) -> str:
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    return raw.decode("latin-1", errors="replace")


def clip(value: str | None, maximum: int = 360) -> str | None:
    if value is None:
        return None
    value = value.replace("\t", "\\t")
    return value if len(value) <= maximum else value[: maximum - 3] + "..."


def difference_evidence(expected: bytes, live: bytes, *, max_lines: int) -> dict[str, Any] | None:
    """Return bounded line evidence; expected is the staged processor output."""

    expected_lines = decode_evidence(normalized_newlines(expected)).split("\n")
    live_lines = decode_evidence(normalized_newlines(live)).split("\n")
    first: int | None = None
    for index, (expected_line, live_line) in enumerate(zip(expected_lines, live_lines), start=1):
        if expected_line != live_line:
            first = index
            break
    if first is None and len(expected_lines) != len(live_lines):
        first = min(len(expected_lines), len(live_lines)) + 1
    if first is None:
        return None
    expected_line = expected_lines[first - 1] if first <= len(expected_lines) else None
    live_line = live_lines[first - 1] if first <= len(live_lines) else None
    diff = list(
        difflib.unified_diff(
            [line + "\n" for line in live_lines],
            [line + "\n" for line in expected_lines],
            fromfile="live",
            tofile="staged_expected",
            n=1,
        )
    )
    preview_lines: list[str] = []
    for line in diff[:max_lines]:
        suffix = "\n" if line.endswith("\n") else ""
        preview_lines.append((clip(line.rstrip("\n"), 600) or "") + suffix)
    return {
        "first_different_line": first,
        "live_line": clip(live_line),
        "staged_expected_line": clip(expected_line),
        "unified_diff_preview": "".join(preview_lines),
        "unified_diff_line_count": len(diff),
        "unified_diff_truncated": len(diff) > max_lines,
    }


def quick_string_entries(raw: bytes) -> list[str] | None:
    """Return raw quick-string records, or ``None`` for a malformed export.

    The first line is the record count; preserve each following record exactly
    so a parity report can distinguish stale/extra entries from a simple order
    difference without guessing at the lossy generated quick-string key.
    """
    lines = decode_evidence(normalized_newlines(raw)).splitlines()
    if not lines:
        return None
    try:
        declared_count = int(lines[0].strip())
    except ValueError:
        return None
    entries = lines[1:]
    if declared_count != len(entries):
        return None
    return entries


def quick_string_delta(expected: bytes, live: bytes, *, limit: int) -> dict[str, Any] | None:
    """Provide bounded semantic evidence for a quick-string-table mismatch."""
    expected_entries = quick_string_entries(expected)
    live_entries = quick_string_entries(live)
    if expected_entries is None or live_entries is None:
        return {"parseable": False}

    expected_counts = Counter(expected_entries)
    live_counts = Counter(live_entries)
    live_only = sorted((live_counts - expected_counts).elements())
    expected_only = sorted((expected_counts - live_counts).elements())
    return {
        "parseable": True,
        "live_entry_count": len(live_entries),
        "staged_entry_count": len(expected_entries),
        "same_entry_multiset": not live_only and not expected_only,
        "live_only_count": len(live_only),
        "staged_only_count": len(expected_only),
        "live_only": [clip(entry, 260) for entry in live_only[:limit]],
        "staged_only": [clip(entry, 260) for entry in expected_only[:limit]],
        "truncated": len(live_only) > limit or len(expected_only) > limit,
    }


def selected_export_files(scope: str) -> tuple[str, ...]:
    if scope == "text":
        return tuple(TEXT_EXPORT_PROVENANCE)
    if scope == "all":
        return ALL_GENERATED_EXPORTS
    raise TextExportParityError("scope must be 'text' or 'all'.")


def validate_workspace(root: Path) -> None:
    required = (root / "compile", root / "compile" / "ids", root / "compile" / "process", root / "_export")
    missing = [project_relative(path, root) for path in required if not path.is_dir()]
    if missing:
        raise TextExportParityError("Not a usable M&B 1.011 legacy processor workspace; missing " + ", ".join(missing))


def copy_tree(source: Path, target: Path) -> None:
    if not source.is_dir():
        raise TextExportParityError(f"Required staging input is absent: {source}")
    try:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    except OSError as error:
        raise TextExportParityError(f"Could not prepare temporary staging input from {source}: {error}") from error


def redirect_stage_export(stage_root: Path) -> None:
    export_dir = (stage_root / "_export").resolve().as_posix().rstrip("/") + "/"
    try:
        (stage_root / "compile" / "module_info.py").write_text(
            "# Temporary Text Export Parity staging override.\n"
            f"export_dir = {export_dir!r}\n",
            encoding="utf-8",
        )
    except OSError as error:
        raise TextExportParityError(f"Could not redirect staged module_info.py: {error}") from error


def stage_environment(stage_root: Path) -> dict[str, str]:
    compile_root = stage_root / "compile"
    ordered_paths = [
        str(stage_root), str(compile_root / "ids"), str(compile_root),
        str(compile_root / "headers"), str(compile_root / "process"),
    ]
    inherited = os.environ.get("PYTHONPATH", "")
    if inherited:
        ordered_paths.append(inherited)
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(ordered_paths)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def run_stage_command(label: str, script: Path, *, cwd: Path, environment: Mapping[str, str], timeout_seconds: int) -> dict[str, Any]:
    if not script.is_file():
        return {
            "label": label,
            "path": str(script),
            "passed": False,
            "exit_code": None,
            "output": "Staged command file is absent.",
            "diagnostics": {"warning_count": 0, "error_count": 0, "items": [], "truncated": False},
        }
    try:
        completed = subprocess.run(
            [sys.executable, "-B", str(script)],
            cwd=cwd,
            env=dict(environment),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "label": label,
            "path": script.name,
            "passed": False,
            "exit_code": None,
            "output": f"Timed out after {timeout_seconds} seconds.",
            "diagnostics": {"warning_count": 0, "error_count": 0, "items": [], "truncated": False},
        }
    stdout, stderr = completed.stdout or "", completed.stderr or ""
    if stdout and stderr and not stdout.endswith(("\n", "\r")):
        full_output = stdout + "\n" + stderr
    else:
        full_output = stdout + stderr
    diagnostic_items: list[dict[str, str]] = []
    warning_count = 0
    error_count = 0
    for line in full_output.splitlines():
        match = STAGE_DIAGNOSTIC_RE.match(line)
        if match is None:
            continue
        severity = match.group(1).lower()
        if severity == "warning":
            warning_count += 1
        else:
            error_count += 1
        if len(diagnostic_items) < MAX_STAGE_DIAGNOSTIC_PREVIEW:
            diagnostic_items.append({"severity": severity, "line": clip(line, 500) or ""})
    output = full_output.strip()
    if len(output) > 4000:
        output = output[:3997] + "..."
    return {
        "label": label,
        "path": script.name,
        "passed": completed.returncode == 0,
        "exit_code": completed.returncode,
        "output": output,
        "diagnostics": {
            "warning_count": warning_count,
            "error_count": error_count,
            "items": diagnostic_items,
            "truncated": warning_count + error_count > len(diagnostic_items),
        },
    }


def run_source_builders(stage_root: Path, *, timeout_seconds: int, builders: Sequence[str]) -> list[dict[str, Any]]:
    environment = stage_environment(stage_root)
    results: list[dict[str, Any]] = []
    for relative in builders:
        result = run_stage_command("source_builder", stage_root / relative, cwd=stage_root, environment=environment, timeout_seconds=timeout_seconds)
        result["builder"] = relative
        results.append(result)
        if not result["passed"]:
            break
    return results


def run_processors(stage_root: Path, *, timeout_seconds: int, processors: Sequence[str]) -> list[dict[str, Any]]:
    environment = stage_environment(stage_root)
    cwd = stage_root / "compile" / "ids"
    results: list[dict[str, Any]] = []
    for filename in processors:
        result = run_stage_command("legacy_processor", stage_root / "compile" / "process" / filename, cwd=cwd, environment=environment, timeout_seconds=timeout_seconds)
        result["processor"] = filename
        results.append(result)
        if not result["passed"]:
            break
    return results


def protected_live_fingerprints(root: Path, exports: Iterable[str]) -> dict[str, str | None]:
    """Proof that staging did not mutate a live generated/export surface."""

    paths: list[Path] = sorted((root / "compile").glob("module_*.py"), key=lambda path: path.name.lower())
    ids = root / "compile" / "ids"
    if ids.is_dir():
        paths.extend(sorted(ids.glob("*.py"), key=lambda path: path.name.lower()))
        if (ids / "variables.txt").is_file():
            paths.append(ids / "variables.txt")
    paths.extend(root / "_export" / filename for filename in exports)
    return {project_relative(path, root): file_hash(path) for path in paths}


def generated_changes(root: Path, stage_root: Path, maximum: int) -> dict[str, Any]:
    changes: list[dict[str, Any]] = []
    changed_total = 0
    for filename in SOURCE_GENERATED_MODULES:
        live = root / "compile" / filename
        staged = stage_root / "compile" / filename
        live_hash, staged_hash = file_hash(live), file_hash(staged)
        if live_hash == staged_hash:
            continue
        changed_total += 1
        if len(changes) >= maximum:
            continue
        changes.append({
            "compile_module": f"compile/{filename}",
            "live_sha256": live_hash,
            "staged_sha256": staged_hash,
            "first_difference": difference_evidence(read_bytes(staged), read_bytes(live), max_lines=12) if staged.is_file() and live.is_file() else None,
        })
    return {"changed_count": changed_total, "returned_change_count": len(changes), "truncated": changed_total > len(changes), "changes": changes}


def compare_exports(root: Path, stage_root: Path, files: Sequence[str], *, max_diffs: int) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rows: list[dict[str, Any]] = []
    counts = {"match": 0, "mismatch": 0, "missing_live": 0, "missing_staged": 0}
    remaining_diffs = max_diffs
    for filename in files:
        live, staged = root / "_export" / filename, stage_root / "_export" / filename
        provenance = TEXT_EXPORT_PROVENANCE.get(filename, {"compile_modules": [], "source_areas": ["legacy_processor_output"]})
        row: dict[str, Any] = {
            "filename": filename,
            "live_path": f"_export/{filename}",
            "staged_provenance": {"compile_modules": list(provenance["compile_modules"]), "source_areas": list(provenance["source_areas"])},
            "live_exists": live.is_file(), "staged_exists": staged.is_file(),
            "live_sha256": file_hash(live), "staged_sha256": file_hash(staged),
            "raw_byte_match": None, "normalized_text_match": None, "status": None, "first_difference": None,
            "quick_string_delta": None,
        }
        if not staged.is_file():
            row["status"] = "missing_staged"
            counts["missing_staged"] += 1
        elif not live.is_file():
            row["status"] = "missing_live"
            counts["missing_live"] += 1
        else:
            staged_raw, live_raw = read_bytes(staged), read_bytes(live)
            raw_match = staged_raw == live_raw
            normalized_match = normalized_newlines(staged_raw) == normalized_newlines(live_raw)
            row["raw_byte_match"] = raw_match
            row["normalized_text_match"] = normalized_match
            if normalized_match:
                row["status"] = "match" if raw_match else "match_normalized_line_endings"
                counts["match"] += 1
            else:
                row["status"] = "mismatch"
                counts["mismatch"] += 1
                if filename == "quick_strings.txt":
                    row["quick_string_delta"] = quick_string_delta(
                        staged_raw,
                        live_raw,
                        limit=min(max_diffs, 20),
                    )
                if remaining_diffs:
                    row["first_difference"] = difference_evidence(staged_raw, live_raw, max_lines=24)
                    remaining_diffs -= 1
        rows.append(row)
    return rows, counts


def source_freshness(root: Path) -> list[dict[str, Any]]:
    if str(DEFAULT_REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(DEFAULT_REPO_ROOT))
    from devkit.workspace_audit import workspace_audit

    return workspace_audit.freshness(root)


def build_export_parity_report(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    source_build: bool = False,
    scope: str = "text",
    max_diffs: int = 20,
    timeout_seconds: int = 90,
    _processors: Sequence[str] | None = None,
    _source_builders: Sequence[str] | None = None,
    _files: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Return bounded, no-live-write source/generated/export parity evidence.

    The private sequence arguments exist only for a small isolated fixture test.
    Public calls always use the fixed checked-in pipeline lists above.
    """

    if not isinstance(source_build, bool):
        raise TextExportParityError("source_build must be true or false.")
    if isinstance(max_diffs, bool) or not isinstance(max_diffs, int) or not 1 <= max_diffs <= 200:
        raise TextExportParityError("max_diffs must be an integer from 1 through 200.")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or not 10 <= timeout_seconds <= 300:
        raise TextExportParityError("timeout_seconds must be an integer from 10 through 300.")
    root = root.resolve()
    validate_workspace(root)
    files = tuple(_files if _files is not None else selected_export_files(scope))
    if not files:
        raise TextExportParityError("At least one export file is required for a parity replay.")
    processors = tuple(_processors if _processors is not None else PROCESSOR_ORDER)
    builders = tuple(_source_builders if _source_builders is not None else SOURCE_BUILDER_ORDER)
    if not processors:
        raise TextExportParityError("At least one legacy processor is required for a parity replay.")

    guard_before = protected_live_fingerprints(root, files)
    builder_results: list[dict[str, Any]] = []
    processor_results: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    comparison_counts = {"match": 0, "mismatch": 0, "missing_live": 0, "missing_staged": 0}
    staged_generated_changes: dict[str, Any] | None = None
    failure: str | None = None

    with tempfile.TemporaryDirectory(prefix="sod-text-export-parity-") as temporary_name:
        stage_root = Path(temporary_name)
        try:
            # Staging keeps legacy compile-authoring modules (items, troops,
            # etc.) available while builders replace only modular outputs.
            copy_tree(root / "compile", stage_root / "compile")
            # Some legacy ``module_*.py`` inputs import authored constants
            # directly from src/ at processor-import time. Copying source is
            # therefore required even in generated->export mode, while only
            # source-build mode actually regenerates module_*.py from it.
            if (root / "src").is_dir():
                copy_tree(root / "src", stage_root / "src")
            elif source_build:
                raise TextExportParityError("source_build requires src/ to be present.")
            if source_build:
                copy_tree(root / "build", stage_root / "build")
                if (root / "docs").is_dir():
                    copy_tree(root / "docs", stage_root / "docs")
            (stage_root / "_export").mkdir(parents=True, exist_ok=True)
            redirect_stage_export(stage_root)
            if source_build:
                builder_results = run_source_builders(stage_root, timeout_seconds=timeout_seconds, builders=builders)
                if not all(result["passed"] for result in builder_results):
                    failure = "A staged source builder failed; no export comparison was trusted."
                else:
                    staged_generated_changes = generated_changes(root, stage_root, max_diffs)
            if failure is None:
                processor_results = run_processors(stage_root, timeout_seconds=timeout_seconds, processors=processors)
                if not all(result["passed"] for result in processor_results):
                    failure = "A staged legacy processor failed; no export comparison was trusted."
                else:
                    comparison_rows, comparison_counts = compare_exports(root, stage_root, files, max_diffs=max_diffs)
        except OSError as error:
            raise TextExportParityError(f"Temporary parity staging failed: {error}") from error

    live_unchanged = guard_before == protected_live_fingerprints(root, files)
    if not live_unchanged:
        raise TextExportParityError("Safety boundary violation: staging changed a protected live compile or export surface.")

    freshness = source_freshness(root)
    stale_areas = [row["source_area"] for row in freshness if row["direct_input_is_newer"]]
    mismatches = comparison_counts["mismatch"] + comparison_counts["missing_live"] + comparison_counts["missing_staged"]
    if failure:
        state = "staging_failed"
    elif mismatches:
        state = "mismatch"
    elif source_build:
        state = "source_to_export_parity"
    elif stale_areas:
        state = "generated_to_export_parity_source_stale"
    else:
        state = "generated_to_export_parity"

    warnings: list[str] = []
    if not source_build and stale_areas:
        warnings.append("Some modular source inputs are newer than generated modules (" + ", ".join(stale_areas) + "); this run proves generated-to-export parity only.")
    if failure:
        warnings.append(failure)
    if mismatches:
        warnings.append("Staged processor output differs from live export. Inspect bounded first-difference evidence before replacing any live export.")

    return {
        "parity_version": f"devkit.text-export-parity.v{PARITY_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {"repo_root": str(root), "read_only": True, "comparison_scope": scope, "source_build": source_build, "selected_export_count": len(files)},
        "safety": {
            "live_compile_written": False,
            "live_export_written": False,
            "live_workspace_unchanged": live_unchanged,
            "staging": "A system temporary workspace was deleted before this result was returned.",
            "excluded_legacy_processor": "process_global_variables_unused.py (it writes a report, not an export).",
        },
        "summary": {
            "state": state,
            "checked_file_count": len(comparison_rows),
            "matched_file_count": comparison_counts["match"],
            "mismatch_file_count": mismatches,
            "missing_live_file_count": comparison_counts["missing_live"],
            "missing_staged_file_count": comparison_counts["missing_staged"],
            "source_stale_area_count": len(stale_areas),
        },
        "source_to_compile": {
            "performed": source_build,
            "builder_results": builder_results,
            "staged_generated_changes": staged_generated_changes,
            "live_source_freshness": freshness,
        },
        "compile_to_export": {
            "processor_results": processor_results,
            "processor_count_requested": len(processors),
            "processor_count_completed": len(processor_results),
            "files": comparison_rows,
        },
        "warnings": warnings,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    summary, scope = report["summary"], report["scope"]
    lines = [
        "# Text Export Parity",
        "",
        f"State: **{summary['state']}**.",
        "",
        f"- Mode: {'source -> generated -> export' if scope['source_build'] else 'generated -> export'}",
        f"- Checked exports: {summary['checked_file_count']}",
        f"- Matches: {summary['matched_file_count']}",
        f"- Mismatches/missing: {summary['mismatch_file_count']}",
        f"- Live compile/export unchanged: {report['safety']['live_workspace_unchanged']}",
        "",
        "## File evidence",
        "",
    ]
    for row in report["compile_to_export"]["files"]:
        lines.append(f"- `{row['filename']}`: {row['status']}")
        evidence = row.get("first_difference")
        if evidence:
            lines.append(f"  - line {evidence['first_different_line']}: live `{evidence['live_line']}` / staged `{evidence['staged_expected_line']}`")
        quick_delta = row.get("quick_string_delta")
        if quick_delta and quick_delta.get("parseable"):
            lines.append(
                "  - quick-string records: "
                f"live {quick_delta['live_entry_count']}, staged {quick_delta['staged_entry_count']}; "
                f"live-only {quick_delta['live_only_count']}, staged-only {quick_delta['staged_only_count']}"
            )
    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay M&B 1.011 text exports in isolated staging and compare them with _export/.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    summary = subparsers.add_parser("summary", help="Run generated/export or source/export parity replay.")
    summary.add_argument("--source-build", action="store_true", help="Also rebuild modular source in staging before processing exports.")
    summary.add_argument("--scope", choices=("text", "all"), default="text")
    summary.add_argument("--max-diffs", type=int, default=20)
    summary.add_argument("--timeout-seconds", type=int, default=90)
    summary.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_export_parity_report(
            DEFAULT_REPO_ROOT,
            source_build=bool(args.source_build),
            scope=args.scope,
            max_diffs=args.max_diffs,
            timeout_seconds=args.timeout_seconds,
        )
    except TextExportParityError as error:
        print(f"text_export_parity: {error}", file=sys.stderr)
        return 1
    print(render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2), end="" if args.format == "markdown" else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
