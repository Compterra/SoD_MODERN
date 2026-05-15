# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import importlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from build_profile import emit_source_map, parse_profile
from build_constants import build as build_constants
from doctor import check_generated_hardcoded_contract, main as doctor_main

from build_dialogs import build as build_dialogs
from build_game_menus import build as build_game_menus
from build_mission_templates import build as build_mission_templates
from build_presentations import build as build_presentations
from build_quests import build as build_quests
from build_scripts import build as build_scripts
from build_simple_triggers import build as build_simple_triggers
from audit_string_registers import main as audit_string_registers_main

ROOT = Path(__file__).resolve().parents[1]
COMPILE_DIR = ROOT / "compile"
BACKUP_ROOT = ROOT / "_export" / "compile_backups"


def _validate_generated_compile_imports() -> None:
    """
    Catch generated Python name/import errors before the process pipeline.

    The fragment builders can produce syntactically valid files that still fail
    when imported by process_*.py. Validate the highest-risk generated modules
    before marking compile/module_*.py as a successful build snapshot.
    """
    import_paths = [
        COMPILE_DIR / "ids",
        COMPILE_DIR,
        COMPILE_DIR / "headers",
        COMPILE_DIR / "process",
        ROOT,
    ]
    added_paths: list[str] = []
    for path in import_paths:
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
            added_paths.append(path_str)

    module_names = [
        "module_troops",
        "module_scripts",
        "module_dialogs",
        "module_game_menus",
        "module_presentations",
        "module_mission_templates",
        "module_simple_triggers",
    ]
    try:
        for module_name in module_names:
            sys.modules.pop(module_name, None)
            importlib.import_module(module_name)
    except Exception as exc:
        raise SystemExit(f"[build_all] Generated compile import failed: {module_name}: {exc}") from exc
    finally:
        for path_str in added_paths:
            try:
                sys.path.remove(path_str)
            except ValueError:
                pass

    print(f"[build_all] Generated compile import check OK: {len(module_names)} module(s).")


def _backup_successful_compile(profile: str) -> None:
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_dir = BACKUP_ROOT / f"success_{stamp}_{profile}"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for src in sorted(COMPILE_DIR.glob("module_*.py"), key=lambda p: p.name.lower()):
        dst = snapshot_dir / src.name
        shutil.copy2(src, dst)
        copied.append(src.name)

    manifest = {
        "created_utc": stamp,
        "profile": profile,
        "source": "compile/module_*.py",
        "files": copied,
    }
    (snapshot_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    snapshots = sorted([p for p in BACKUP_ROOT.iterdir() if p.is_dir() and p.name.startswith("success_")], key=lambda p: p.name.lower())
    while len(snapshots) > 2:
        old = snapshots.pop(0)
        shutil.rmtree(old)

    print(f"[build_all] Backed up successful compile -> {snapshot_dir}")


def main() -> None:
    profile = parse_profile(sys.argv)
    source_map = emit_source_map(profile)
    use_cache = "--no-cache" not in sys.argv

    doctor_main(argv=list(sys.argv) + ["--doctor-no-generated-contract"])

    print(f"[build_all] Profile: {profile}")
    build_constants()
    build_quests(use_cache=use_cache, emit_source_map=source_map)
    build_scripts(use_cache=use_cache, emit_source_map=source_map)
    build_simple_triggers(use_cache=use_cache, emit_source_map=source_map)
    build_game_menus(use_cache=use_cache, emit_source_map=source_map)
    build_dialogs(use_cache=use_cache, emit_source_map=source_map)
    build_presentations(use_cache=use_cache, emit_source_map=source_map)
    build_mission_templates(use_cache=use_cache, emit_source_map=source_map)

    contract_errors, contract_warnings = check_generated_hardcoded_contract(check_ids=False)
    for warning in contract_warnings:
        print(f"[doctor] WARNING: {warning}")
    if contract_errors:
        for error in contract_errors:
            print(f"[doctor] ERROR: {error}")
        raise SystemExit(1)
    print(f"[doctor] M&B 1.011 compile-source hardcoded contract OK: {len(contract_warnings)} warning(s).")

    audit_string_registers_main()
    _validate_generated_compile_imports()
    _backup_successful_compile(profile)


if __name__ == "__main__":
    main()
