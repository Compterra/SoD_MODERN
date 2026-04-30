# -*- coding: utf-8 -*-
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "build" / "test_sod_law_static.py")], check=True)
    print("test_sod_law_generation_or_static_checks: OK")


if __name__ == "__main__":
    main()
