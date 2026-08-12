#!/usr/bin/env python3
"""Read-only, evidence-oriented architecture audit for this module system.

The report deliberately inspects source, generated compile modules, and live
exports without importing legacy module code or running the build. It is meant
to give an LLM a bounded, repeatable map of the system before it diagnoses or
changes gameplay content.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


AUDIT_VERSION = "1.0.0"
TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]

SOURCE_AREAS = (
    "constants",
    "dialogs",
    "menus",
    "mission_templates",
    "presentations",
    "quests",
    "scripts",
    "triggers",
)

ORDER_SPECS: tuple[dict[str, Any], ...] = (
    {
        "id": "constants",
        "source_area": "constants",
        "order_file": "src/constants/_order_constants.txt",
        "policy": "Manifest entries lead; remaining top-level constant modules append alphabetically.",
        "builder_validation": "Listed files must exist; unlisted modules still compile after the manifest.",
        "recursive": False,
        "exclude_private": True,
        "unlisted_requires_review": False,
    },
    {
        "id": "dialogs",
        "source_area": "dialogs",
        "order_file": "src/dialogs/_order_dialogs.txt",
        "policy": "Manifest is the complete generated order. NPC dialogue evaluation is order-sensitive.",
        "builder_validation": "Listed paths must exist. The audit independently checks reverse coverage.",
        "recursive": True,
        "unlisted_requires_review": True,
    },
    {
        "id": "menus",
        "source_area": "menus",
        "order_file": "src/menus/_order_game_menus.txt",
        "policy": "Strict manifest order.",
        "builder_validation": "Builder rejects missing and unlisted fragment files.",
        "recursive": True,
        "unlisted_requires_review": True,
    },
    {
        "id": "triggers",
        "source_area": "triggers",
        "order_file": "src/triggers/_order_simple_triggers.txt",
        "policy": "Strict manifest order.",
        "builder_validation": "Builder rejects missing and unlisted fragment files.",
        "recursive": True,
        "unlisted_requires_review": True,
    },
    {
        "id": "presentations",
        "source_area": "presentations",
        "order_file": "src/presentations/_order_presentations.txt",
        "policy": "Manifest is the generated order.",
        "builder_validation": "Listed paths must exist. The audit independently checks reverse coverage.",
        "recursive": True,
        "unlisted_requires_review": True,
    },
    {
        "id": "mission_templates",
        "source_area": "mission_templates",
        "order_file": "src/mission_templates/_order_mission_templates.txt",
        "policy": "Manifest is the generated order.",
        "builder_validation": "Listed paths must exist. The audit independently checks reverse coverage.",
        "recursive": True,
        "unlisted_requires_review": True,
    },
    {
        "id": "quests",
        "source_area": "quests",
        "order_file": "src/quests/_order_quests.txt",
        "policy": "Folder-sorted files compile by default; manifest entries are promoted ahead of the remainder.",
        "builder_validation": "Unlisted valid files still compile after manifest-listed files.",
        "recursive": True,
        "unlisted_requires_review": False,
    },
    {
        "id": "scripts_za_hardcoded",
        "source_area": "scripts",
        "order_file": "src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt",
        "policy": "All script fragments are folder-sorted; this manifest reorders only the hardcoded game callback slice.",
        "builder_validation": "Unlisted hardcoded callback files still compile after listed files.",
        "recursive": True,
        "path_prefix": "ZA_hardcoded_game_scripts/",
        "unlisted_requires_review": False,
    },
)

FRESHNESS_SPECS: tuple[dict[str, str], ...] = (
    {"source_area": "constants", "builder": "build/build_constants.py", "compile": "compile/module_constants.py"},
    {"source_area": "dialogs", "builder": "build/build_dialogs.py", "compile": "compile/module_dialogs.py"},
    {"source_area": "menus", "builder": "build/build_game_menus.py", "compile": "compile/module_game_menus.py"},
    {
        "source_area": "mission_templates",
        "builder": "build/build_mission_templates.py",
        "compile": "compile/module_mission_templates.py",
    },
    {
        "source_area": "presentations",
        "builder": "build/build_presentations.py",
        "compile": "compile/module_presentations.py",
    },
    {"source_area": "quests", "builder": "build/build_quests.py", "compile": "compile/module_quests.py"},
    {"source_area": "scripts", "builder": "build/build_scripts.py", "compile": "compile/module_scripts.py"},
    {
        "source_area": "triggers",
        "builder": "build/build_simple_triggers.py",
        "compile": "compile/module_simple_triggers.py",
    },
)

ENTITY_SPECS: tuple[dict[str, str], ...] = (
    {
        "id": "dialogs",
        "source_area": "dialogs",
        "compile": "compile/module_dialogs.py",
        "assignment": "dialogs",
        "export": "conversation.txt",
    },
    {
        "id": "game_menus",
        "source_area": "menus",
        "compile": "compile/module_game_menus.py",
        "assignment": "game_menus",
        "export": "menus.txt",
    },
    {
        "id": "mission_templates",
        "source_area": "mission_templates",
        "compile": "compile/module_mission_templates.py",
        "assignment": "mission_templates",
        "export": "mission_templates.txt",
    },
    {
        "id": "presentations",
        "source_area": "presentations",
        "compile": "compile/module_presentations.py",
        "assignment": "presentations",
        "export": "presentations.txt",
    },
    {
        "id": "quests",
        "source_area": "quests",
        "compile": "compile/module_quests.py",
        "assignment": "quests",
        "export": "quests.txt",
    },
    {
        "id": "scripts",
        "source_area": "scripts",
        "compile": "compile/module_scripts.py",
        "assignment": "scripts",
        "export": "scripts.txt",
    },
    {
        "id": "simple_triggers",
        "source_area": "triggers",
        "compile": "compile/module_simple_triggers.py",
        "assignment": "simple_triggers",
        "export": "simple_triggers.txt",
    },
    {
        "id": "strings",
        "source_area": "legacy_compile",
        "compile": "compile/module_strings.py",
        "assignment": "strings",
        "export": "strings.txt",
    },
)

EXPORT_SPECS: tuple[dict[str, Any], ...] = (
    {"filename": "strings.txt", "declared_count_line": 1},
    {"filename": "quick_strings.txt", "declared_count_line": 0},
    {"filename": "conversation.txt", "declared_count_line": 1},
    {"filename": "dialog_states.txt", "declared_count_line": None},
    {"filename": "scripts.txt", "declared_count_line": 1},
    {"filename": "menus.txt", "declared_count_line": 1},
    {"filename": "simple_triggers.txt", "declared_count_line": 1},
    {"filename": "mission_templates.txt", "declared_count_line": 1},
    {"filename": "presentations.txt", "declared_count_line": 1},
    {"filename": "quests.txt", "declared_count_line": 1},
)

SOURCE_MARKER_RE = re.compile(
    r"(?m)^\s*#\s*\[\s*src/[^\]\r\n]+\.py(?::L\d+(?:-L\d+)?)?\s*\]"
)
PROCESS_REFERENCE_RE = re.compile(r"\bprocess_[A-Za-z0-9_]+\.py\b")
CHECK_FUNCTION_RE = re.compile(r"(?m)^def _check_[A-Za-z0-9_]+\(")
SCRIPT_SYMBOL_RE = re.compile(r"\bscript_[A-Za-z0-9_]+\b")
OPERATION_PATTERNS = {
    "call_script": re.compile(r"\bcall_script\b"),
    "jump_to_menu": re.compile(r"\bjump_to_menu\b"),
    "start_presentation": re.compile(r"\bstart_presentation\b"),
    "set_jump_mission": re.compile(r"\bset_jump_mission\b"),
    "str_store_string": re.compile(r"\bstr_store_string\b"),
    "str_store_string_reg": re.compile(r"\bstr_store_string_reg\b"),
}


class AuditError(RuntimeError):
    """An audit input could not be safely read or interpreted."""


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text_compatible(path: Path) -> str:
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error
    raise AuditError(f"Could not decode {path}: {last_error}")


def sorted_python_files(path: Path, recursive: bool = True) -> list[Path]:
    if not path.is_dir():
        return []
    iterator: Iterable[Path] = path.rglob("*.py") if recursive else path.glob("*.py")
    return sorted((item for item in iterator if item.is_file()), key=lambda item: item.as_posix().lower())


def is_fragment_candidate(path: Path, source_root: Path, exclude_private: bool = False) -> bool:
    try:
        relative = path.relative_to(source_root)
    except ValueError:
        return False
    if path.name == "__init__.py" or "_preamble" in relative.parts:
        return False
    if exclude_private and path.name.startswith("_"):
        return False
    return True


def file_statistics(paths: Sequence[Path]) -> dict[str, int]:
    byte_count = 0
    physical_lines = 0
    nonblank_lines = 0
    for path in paths:
        byte_count += path.stat().st_size
        raw = read_text_compatible(path)
        lines = raw.splitlines()
        physical_lines += len(lines)
        nonblank_lines += sum(bool(line.strip()) for line in lines)
    return {
        "file_count": len(paths),
        "byte_count": byte_count,
        "physical_line_count": physical_lines,
        "nonblank_line_count": nonblank_lines,
    }


def read_order_entries(path: Path) -> list[str]:
    if not path.is_file():
        return []
    entries: list[str] = []
    for line in read_text_compatible(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append(stripped.split()[-1].replace("\\", "/"))
    return entries


def compact(values: Iterable[str], maximum: int) -> list[str]:
    return list(sorted(values, key=str.lower))[:maximum]


def ordering_contracts(root: Path, maximum: int) -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    for spec in ORDER_SPECS:
        source_root = root / "src" / spec["source_area"]
        order_path = root / spec["order_file"]
        candidates = [
            path
            for path in sorted_python_files(source_root, recursive=bool(spec.get("recursive", True)))
            if is_fragment_candidate(path, source_root, bool(spec.get("exclude_private", False)))
        ]
        relative_candidates = [path.relative_to(source_root).as_posix() for path in candidates]
        prefix = spec.get("path_prefix")
        if prefix:
            relative_candidates = [item for item in relative_candidates if item.startswith(prefix)]
        listed = read_order_entries(order_path)
        listed_set = set(listed)
        candidate_set = set(relative_candidates)
        duplicate_entries = sorted(
            entry for entry, count in Counter(listed).items() if count > 1
        )
        unlisted = candidate_set - listed_set
        missing = listed_set - candidate_set
        contracts.append(
            {
                "id": spec["id"],
                "source_area": spec["source_area"],
                "order_file": spec["order_file"],
                "order_file_exists": order_path.is_file(),
                "policy": spec["policy"],
                "builder_validation": spec["builder_validation"],
                "unlisted_requires_review": bool(spec.get("unlisted_requires_review", True)),
                "listed_entry_count": len(listed),
                "candidate_fragment_count": len(relative_candidates),
                "missing_listed_count": len(missing),
                "unlisted_candidate_count": len(unlisted),
                "duplicate_order_entry_count": len(duplicate_entries),
                "missing_listed_sample": compact(missing, maximum),
                "unlisted_candidate_sample": compact(unlisted, maximum),
                "duplicate_order_entry_sample": compact(duplicate_entries, maximum),
            }
        )
    return contracts


def utc_timestamp(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat().replace("+00:00", "Z")


def freshness(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in FRESHNESS_SPECS:
        source_root = root / "src" / spec["source_area"]
        source_files = sorted_python_files(source_root)
        direct_inputs = source_files + [root / spec["builder"]]
        order_file = next(
            (root / item["order_file"] for item in ORDER_SPECS if item["source_area"] == spec["source_area"]),
            None,
        )
        if order_file is not None:
            direct_inputs.append(order_file)
        existing_inputs = [path for path in direct_inputs if path.is_file()]
        newest_input = max(existing_inputs, key=lambda path: path.stat().st_mtime) if existing_inputs else None
        compile_path = root / spec["compile"]
        compile_exists = compile_path.is_file()
        rows.append(
            {
                "source_area": spec["source_area"],
                "builder": spec["builder"],
                "compile_module": spec["compile"],
                "compile_exists": compile_exists,
                "newest_direct_input": project_relative(newest_input, root) if newest_input else None,
                "newest_direct_input_mtime_utc": utc_timestamp(newest_input),
                "compile_mtime_utc": utc_timestamp(compile_path if compile_exists else None),
                "direct_input_is_newer": bool(
                    newest_input is not None and compile_exists and newest_input.stat().st_mtime > compile_path.stat().st_mtime
                ),
            }
        )
    return rows


def assignment_structure(path: Path, assignment: str) -> tuple[int | None, int | None, str | None]:
    try:
        tree = ast.parse(read_text_compatible(path), filename=str(path))
    except SyntaxError as error:
        return None, None, f"Parse failed at line {error.lineno}: {error.msg}"
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == assignment for target in statement.targets):
            continue
        if isinstance(statement.value, (ast.List, ast.Tuple)):
            starred = sum(isinstance(element, ast.Starred) for element in statement.value.elts)
            return len(statement.value.elts), starred, None
        return None, None, f"Assignment '{assignment}' is not a list or tuple."
    return None, None, f"Could not find assignment '{assignment}'."


def entity_metrics(root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for spec in ENTITY_SPECS:
        path = root / spec["compile"]
        if not path.is_file():
            results.append(
                {
                    **spec,
                    "compile_exists": False,
                    "static_assignment_element_count": None,
                    "top_level_starred_expression_count": None,
                    "source_marker_comment_count": 0,
                    "parse_error": "Generated module is absent.",
                }
            )
            continue
        raw = read_text_compatible(path)
        item_count, starred_count, parse_error = assignment_structure(path, spec["assignment"])
        results.append(
            {
                **spec,
                "compile_exists": True,
                "static_assignment_element_count": item_count,
                "top_level_starred_expression_count": starred_count,
                "source_marker_comment_count": len(SOURCE_MARKER_RE.findall(raw)),
                "physical_line_count": len(raw.splitlines()),
                "byte_count": path.stat().st_size,
                "parse_error": parse_error,
            }
        )
    return results


def export_metrics(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    export_root = root / "_export"
    root_files = sorted((path for path in export_root.glob("*") if path.is_file()), key=lambda path: path.name.lower())
    recursive_files = sorted(
        (path for path in export_root.rglob("*") if path.is_file()),
        key=lambda path: path.as_posix().lower(),
    )
    summary = {
        "root_directory_exists": export_root.is_dir(),
        "live_root_file_count": len(root_files),
        "live_root_byte_count": sum(path.stat().st_size for path in root_files),
        "recursive_file_count_including_backups": len(recursive_files),
        "recursive_byte_count_including_backups": sum(path.stat().st_size for path in recursive_files),
    }
    records: list[dict[str, Any]] = []
    for spec in EXPORT_SPECS:
        path = export_root / spec["filename"]
        if not path.is_file():
            records.append(
                {
                    "filename": spec["filename"],
                    "exists": False,
                    "declared_entry_count": None,
                    "nonblank_line_count": 0,
                }
            )
            continue
        raw = read_text_compatible(path)
        lines = raw.splitlines()
        declared_count: int | None = None
        declared_line = spec["declared_count_line"]
        if declared_line is not None and len(lines) > declared_line:
            candidate = lines[declared_line].strip()
            if candidate.isdigit():
                declared_count = int(candidate)
        records.append(
            {
                "filename": spec["filename"],
                "exists": True,
                "declared_entry_count": declared_count,
                "physical_line_count": len(lines),
                "nonblank_line_count": sum(bool(line.strip()) for line in lines),
                "byte_count": path.stat().st_size,
            }
        )
    return summary, records


def generated_export_parity(
    entities: Sequence[dict[str, Any]],
    exports: Sequence[dict[str, Any]],
    root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    export_by_name = {item["filename"]: item for item in exports}
    parity: list[dict[str, Any]] = []
    freshness_rows: list[dict[str, Any]] = []
    for entity in entities:
        export = export_by_name.get(entity["export"])
        export_count = export.get("declared_entry_count") if export else None
        static_count = entity.get("static_assignment_element_count")
        starred_count = entity.get("top_level_starred_expression_count")
        directly_comparable = static_count is not None and starred_count == 0
        parity.append(
            {
                "entity": entity["id"],
                "compile_module": entity["compile"],
                "export_file": entity["export"],
                "static_assignment_element_count": static_count,
                "top_level_starred_expression_count": starred_count,
                "export_declared_count": export_count,
                "count_comparison": (
                    "exact_static"
                    if directly_comparable
                    else "requires_module_evaluation"
                    if static_count is not None
                    else "unavailable"
                ),
                "counts_match": (
                    static_count == export_count
                    if directly_comparable and export_count is not None
                    else None
                ),
            }
        )
        compile_path = root / entity["compile"]
        export_path = root / "_export" / entity["export"]
        freshness_rows.append(
            {
                "entity": entity["id"],
                "compile_module": entity["compile"],
                "export_file": project_relative(export_path, root),
                "both_exist": compile_path.is_file() and export_path.is_file(),
                "compile_is_newer_than_export": bool(
                    compile_path.is_file()
                    and export_path.is_file()
                    and compile_path.stat().st_mtime > export_path.stat().st_mtime
                ),
                "compile_mtime_utc": utc_timestamp(compile_path if compile_path.is_file() else None),
                "export_mtime_utc": utc_timestamp(export_path if export_path.is_file() else None),
            }
        )
    return parity, freshness_rows


def processor_pipeline(root: Path) -> dict[str, Any]:
    batch_path = root / "build_module.bat"
    batch_raw = read_text_compatible(batch_path) if batch_path.is_file() else ""
    dispatched: list[str] = []
    for match in PROCESS_REFERENCE_RE.finditer(batch_raw):
        name = match.group(0)
        if name not in dispatched:
            dispatched.append(name)
    build_all_path = root / "build" / "build_all.py"
    build_all_raw = read_text_compatible(build_all_path) if build_all_path.is_file() else ""
    builders = re.findall(r"(?m)^\s*(build_[a-z_]+)\(", build_all_raw)
    return {
        "entrypoint": "build_module.bat",
        "fragment_build_orchestrator": "build/build_all.py",
        "fragment_builder_call_count": len(builders),
        "fragment_builder_calls": builders,
        "legacy_processor_count": len(dispatched),
        "legacy_processor_sequence": dispatched,
        "processor_implementation_file_count": len(
            [
                path
                for path in sorted_python_files(root / "compile" / "process", recursive=False)
                if path.name.startswith("process_")
            ]
        ),
        "post_build_string_register_audit_referenced": "audit_string_registers.py" in batch_raw,
        "post_build_doctor_referenced": "doctor.py" in batch_raw,
        "source_map_profiles": {
            "dev": "Generated fragment source markers are retained.",
            "release": "Generated fragment source markers are deliberately stripped.",
        },
    }


def source_operation_metrics(source_files: Sequence[Path]) -> dict[str, Any]:
    counts = {name: 0 for name in OPERATION_PATTERNS}
    script_symbols: set[str] = set()
    lexical_occurrences = 0
    for path in source_files:
        raw = read_text_compatible(path)
        for name, pattern in OPERATION_PATTERNS.items():
            counts[name] += len(pattern.findall(raw))
        matches = SCRIPT_SYMBOL_RE.findall(raw)
        lexical_occurrences += len(matches)
        script_symbols.update(matches)
    return {
        "source_python_files_scanned": len(source_files),
        "operation_occurrences": counts,
        "lexical_script_symbol_occurrence_count": lexical_occurrences,
        "unique_script_symbol_count": len(script_symbols),
    }


def validation_surface(root: Path) -> dict[str, Any]:
    build_root = root / "build"
    doctor_path = build_root / "doctor.py"
    doctor_raw = read_text_compatible(doctor_path) if doctor_path.is_file() else ""
    test_files = [
        path for path in sorted_python_files(build_root, recursive=False) if path.name.startswith("test_")
    ]
    return {
        "build_python_file_count": len(sorted_python_files(build_root, recursive=False)),
        "standalone_build_test_file_count": len(test_files),
        "doctor_exists": doctor_path.is_file(),
        "doctor_physical_line_count": len(doctor_raw.splitlines()),
        "doctor_check_function_count": len(CHECK_FUNCTION_RE.findall(doctor_raw)),
        "doctor_writes_report_artifacts": "write_text(" in doctor_raw,
        "audit_execution_note": "This workspace audit does not run doctor.py or rebuild/export files.",
    }


def worktree_status(root: Path, maximum: int) -> dict[str, Any]:
    # Codex and other isolated hosts can inspect a user-owned workspace under a
    # different Windows identity. Scope this exception to the one read-only
    # status command instead of requiring a global Git configuration change.
    resolved_root = root.resolve()
    try:
        completed = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={resolved_root}",
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            cwd=resolved_root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return {
            "available": False,
            "error": str(error),
            "dirty_entry_count": None,
            "generated_or_export_dirty_entry_count": None,
            "sample": [],
        }
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    generated_or_export = [
        line
        for line in lines
        if len(line) >= 4
        and (line[3:].replace("\\", "/").startswith("compile/") or line[3:].replace("\\", "/").startswith("_export/"))
    ]
    return {
        "available": completed.returncode == 0,
        "git_exit_code": completed.returncode,
        "git_stderr": completed.stderr.strip() or None,
        "dirty_entry_count": len(lines),
        "generated_or_export_dirty_entry_count": len(generated_or_export),
        "sample": lines[:maximum],
    }


def diagnostic_priorities(
    entities: Sequence[dict[str, Any]],
    exports: Sequence[dict[str, Any]],
    contracts: Sequence[dict[str, Any]],
    worktree: dict[str, Any],
) -> list[dict[str, Any]]:
    by_id = {item["id"]: item for item in entities}
    by_export = {item["filename"]: item for item in exports}
    dialog_count = by_id.get("dialogs", {}).get("static_assignment_element_count")
    dialog_fragments = next(
        (item.get("candidate_fragment_count") for item in contracts if item["id"] == "dialogs"),
        None,
    )
    return [
        {
            "id": "compiled_order_controls_dialogue_flow",
            "priority": "highest",
            "evidence": {
                "dialogue_fragment_count": dialog_fragments,
                "compiled_dialogue_entry_count": dialog_count,
                "ordering_contract": "src/dialogs/_order_dialogs.txt",
            },
            "implication": "Trace a suspect dialogue in compiled order before editing source; a preceding matching NPC route can win.",
        },
        {
            "id": "text_exists_in_multiple_runtime_layers",
            "priority": "highest",
            "evidence": {
                "strings_declared_count": by_export.get("strings.txt", {}).get("declared_entry_count"),
                "quick_strings_declared_count": by_export.get("quick_strings.txt", {}).get("declared_entry_count"),
                "conversation_declared_count": by_export.get("conversation.txt", {}).get("declared_entry_count"),
            },
            "implication": "A text diagnosis must inspect modular source, generated modules, strings.txt, quick_strings.txt, and conversation.txt as applicable.",
        },
        {
            "id": "generation_and_export_are_separate_semantic_boundaries",
            "priority": "high",
            "evidence": {
                "fragment_builder_stage": "build/build_all.py",
                "legacy_processor_stage": "build_module.bat",
            },
            "implication": "A source edit can be correct while generated compile output or the live export remains stale.",
        },
        {
            "id": "source_provenance_depends_on_profile",
            "priority": "medium",
            "evidence": {
                "dev_profile": "Source markers retained",
                "release_profile": "Source markers stripped",
            },
            "implication": "Preserve or regenerate a development-profile compile snapshot when detailed fragment provenance is needed.",
        },
        {
            "id": "current_worktree_requires_build_caution",
            "priority": "medium",
            "evidence": {
                "dirty_entry_count": worktree.get("dirty_entry_count"),
                "generated_or_export_dirty_entry_count": worktree.get("generated_or_export_dirty_entry_count"),
            },
            "implication": "Do not regenerate compile or export artifacts as part of diagnosis without first isolating the intended diff.",
        },
    ]


def audit_workspace(root: Path = DEFAULT_REPO_ROOT, max_items: int = 12) -> dict[str, Any]:
    """Return a bounded, entirely read-only workspace topology report."""
    if isinstance(max_items, bool) or not isinstance(max_items, int) or not 1 <= max_items <= 100:
        raise AuditError("max_items must be an integer from 1 through 100.")
    root = root.resolve()
    if not (root / "src").is_dir() or not (root / "compile").is_dir():
        raise AuditError(f"Not a recognizable SoD Modern module workspace: {root}")

    source_area_rows: list[dict[str, Any]] = []
    all_source_files: list[Path] = []
    for area in SOURCE_AREAS:
        files = sorted_python_files(root / "src" / area)
        all_source_files.extend(files)
        row = {"area": area, **file_statistics(files)}
        source_area_rows.append(row)
    source_area_rows.sort(key=lambda row: (-row["physical_line_count"], row["area"]))

    generated_files = sorted(
        (path for path in (root / "compile").glob("module_*.py") if path.is_file()),
        key=lambda path: path.name.lower(),
    )
    contracts = ordering_contracts(root, max_items)
    entities = entity_metrics(root)
    export_summary, exports = export_metrics(root)
    parity, compile_to_export = generated_export_parity(entities, exports, root)
    source_to_compile = freshness(root)
    pipeline = processor_pipeline(root)
    validation = validation_surface(root)
    worktree = worktree_status(root, max_items)

    warnings: list[str] = []
    for contract in contracts:
        if not contract["order_file_exists"]:
            warnings.append(f"Missing ordering contract: {contract['order_file']}.")
        if contract["missing_listed_count"] or (
            contract["unlisted_requires_review"] and contract["unlisted_candidate_count"]
        ):
            warnings.append(
                f"Ordering coverage drift in {contract['id']}: "
                f"{contract['missing_listed_count']} missing listed, "
                f"{contract['unlisted_candidate_count']} unlisted candidate(s)."
            )
    for row in source_to_compile:
        if not row["compile_exists"]:
            warnings.append(f"Missing generated compile module: {row['compile_module']}.")
        elif row["direct_input_is_newer"]:
            warnings.append(
                f"Direct input is newer than generated module for {row['source_area']}: {row['compile_module']}."
            )
    for row in compile_to_export:
        if row["both_exist"] and row["compile_is_newer_than_export"]:
            warnings.append(f"Generated module is newer than its export for {row['entity']}.")
    if worktree.get("dirty_entry_count"):
        warnings.append(
            f"Workspace has {worktree['dirty_entry_count']} pending Git status entries; audit did not rebuild or export."
        )
    if not worktree.get("available"):
        warnings.append("Git worktree status could not be read.")

    return {
        "audit_version": f"devkit.workspace-audit.v{AUDIT_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {
            "repo_root": str(root),
            "read_only": True,
            "excluded_actions": [
                "No fragment builder was run.",
                "No legacy processor was run.",
                "No live export was rewritten.",
                "No doctor report was regenerated.",
            ],
        },
        "source": {
            **file_statistics(all_source_files),
            "areas": source_area_rows,
        },
        "generated_compile": {
            **file_statistics(generated_files),
            "module_file_count": len(generated_files),
            "module_files_sample": [project_relative(path, root) for path in generated_files[:max_items]],
        },
        "exports": {
            **export_summary,
            "key_files": exports,
        },
        "pipeline": pipeline,
        "ordering": {"contracts": contracts},
        "entities": entities,
        "consistency": {
            "generated_export_count_parity": parity,
            "source_to_compile_freshness": source_to_compile,
            "compile_to_export_freshness": compile_to_export,
        },
        "cross_references": source_operation_metrics(all_source_files),
        "validation_surface": validation,
        "worktree": worktree,
        "diagnostic_priorities": diagnostic_priorities(entities, exports, contracts, worktree),
        "warnings": list(dict.fromkeys(warnings)),
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render a compact human-readable convenience report from the JSON model."""
    source = report["source"]
    pipeline = report["pipeline"]
    exports = report["exports"]
    worktree = report["worktree"]
    lines = [
        "# SoD Modern Workspace Audit",
        "",
        f"Read-only DevKit snapshot generated {report['generated_at_utc']}.",
        "",
        "## Scale",
        "",
        f"- Modular source: {source['file_count']:,} Python files, {source['physical_line_count']:,} physical lines.",
        f"- Generated compile: {report['generated_compile']['module_file_count']:,} module files, {report['generated_compile']['physical_line_count']:,} physical lines.",
        f"- Live export root: {exports['live_root_file_count']:,} files; recursive export tree (including compile backups): {exports['recursive_file_count_including_backups']:,} files.",
        f"- Build pipeline: {pipeline['fragment_builder_call_count']} fragment builders followed by {pipeline['legacy_processor_count']} dispatched legacy processors.",
        f"- Validation surface: {report['validation_surface']['standalone_build_test_file_count']:,} standalone build tests and {report['validation_surface']['doctor_check_function_count']:,} doctor checks.",
        "",
        "| Source area | Python files | Physical lines |",
        "| --- | ---: | ---: |",
    ]
    for area in source["areas"]:
        lines.append(
            f"| {area['area']} | {area['file_count']:,} | {area['physical_line_count']:,} |"
        )

    lines.extend(["", "## Runtime entity scale", "", "| Entity | Static list terms | Export items | Comparison |", "| --- | ---: | ---: | --- |"])
    for row in report["consistency"]["generated_export_count_parity"]:
        generated = row["static_assignment_element_count"]
        exported = row["export_declared_count"]
        generated_text = f"{generated:,}" if isinstance(generated, int) else "n/a"
        export_text = f"{exported:,}" if isinstance(exported, int) else "n/a"
        parity = "yes" if row["counts_match"] else row["count_comparison"]
        lines.append(f"| {row['entity']} | {generated_text} | {export_text} | {parity} |")

    lines.extend(["", "## Ordering contracts", ""])
    for contract in report["ordering"]["contracts"]:
        state = "clean"
        if (
            not contract["order_file_exists"]
            or contract["missing_listed_count"]
            or (contract["unlisted_requires_review"] and contract["unlisted_candidate_count"])
            or contract["duplicate_order_entry_count"]
        ):
            state = "review"
        lines.append(
            f"- {contract['id']}: {state}; {contract['listed_entry_count']} listed / "
            f"{contract['candidate_fragment_count']} candidate fragments; "
            f"{contract['missing_listed_count']} missing, {contract['unlisted_candidate_count']} unlisted."
        )

    lines.extend(["", "## Current consistency", ""])
    for row in report["consistency"]["source_to_compile_freshness"]:
        state = "stale" if row["direct_input_is_newer"] else "current by direct mtime"
        if not row["compile_exists"]:
            state = "missing compile module"
        lines.append(f"- {row['source_area']}: {state} ({row['compile_module']}).")
    for row in report["consistency"]["compile_to_export_freshness"]:
        if row["both_exist"] and row["compile_is_newer_than_export"]:
            lines.append(f"- {row['entity']}: compile is newer than {row['export_file']}.")

    lines.extend(["", "## Diagnostic priorities", ""])
    for priority in report["diagnostic_priorities"]:
        lines.append(f"- {priority['id']} ({priority['priority']}): {priority['implication']}")

    lines.extend(["", "## Worktree safety", ""])
    dirty = worktree.get("dirty_entry_count")
    if dirty is None:
        lines.append("- Git worktree status was unavailable.")
    else:
        lines.append(
            f"- {dirty} pending Git status entries; {worktree.get('generated_or_export_dirty_entry_count', 0)} touch compile or export paths."
        )
    lines.append("- No builder, processor, export, or doctor action was run by this audit.")

    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def output_path(path_arg: str, root: Path) -> Path:
    path = Path(path_arg)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    export_root = (root / "_export").resolve()
    try:
        path.relative_to(export_root)
    except ValueError:
        return path
    raise AuditError("Refusing to write an audit artifact under _export/.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only SoD Modern workspace architecture audit.")
    parser.add_argument("command", nargs="?", choices=("summary",), default="summary")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--max-items", type=int, default=12, help="Bound path samples to 1..100 items.")
    parser.add_argument("--output", help="Optional report file path, relative to the module root by default.")
    args = parser.parse_args(argv)

    try:
        report = audit_workspace(DEFAULT_REPO_ROOT, args.max_items)
        payload = json.dumps(report, indent=2, sort_keys=True) if args.format == "json" else render_markdown(report)
        if args.output:
            path = output_path(args.output, DEFAULT_REPO_ROOT)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload + ("" if payload.endswith("\n") else "\n"), encoding="utf-8")
        else:
            sys.stdout.write(payload + ("" if payload.endswith("\n") else "\n"))
    except AuditError as error:
        print(f"workspace_audit: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
