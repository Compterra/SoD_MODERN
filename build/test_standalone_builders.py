# -*- coding: utf-8 -*-
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_builder(name: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "build" / name)], cwd=str(ROOT), check=True)


def main() -> None:
    for builder in (
        "build_simple_triggers.py",
        "build_mission_templates.py",
        "build_presentations.py",
    ):
        run_builder(builder)
    print("test_standalone_builders: OK")


if __name__ == "__main__":
    main()
