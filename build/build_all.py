# -*- coding: utf-8 -*-
from __future__ import annotations

import json
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

ROOT = Path(__file__).resolve().parents[1]
COMPILE_DIR = ROOT / "compile"
BACKUP_ROOT = ROOT / "_export" / "compile_backups"


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

    _backup_successful_compile(profile)


if __name__ == "__main__":
    main()
