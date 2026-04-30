# -*- coding: utf-8 -*-
"""Build profile handling (dev vs release).

Profiles are used to control generated debug/comment output.
- dev: keep source-mapping markers in generated compile/module_*.py
- release: strip source-mapping markers (cleaner + safer for distribution)

Usage examples:
  python build/build_all.py --profile dev
  python build/build_all.py --profile release
  python build/build_all.py --profile=release
"""

from __future__ import annotations

import sys

VALID_PROFILES = ("dev", "release")


def parse_profile(argv: list[str] | None = None, default: str = "dev") -> str:
    argv = list(sys.argv if argv is None else argv)
    profile = default

    for i, a in enumerate(argv):
        if a.startswith("--profile="):
            profile = a.split("=", 1)[1]
        elif a == "--profile" and i + 1 < len(argv):
            profile = argv[i + 1]

    profile = (profile or default).strip().lower()
    if profile not in VALID_PROFILES:
        raise SystemExit(
            f"[build] Unknown --profile '{profile}'. Valid values: dev, release"
        )
    return profile


def emit_source_map(profile: str) -> bool:
    return profile.strip().lower() != "release"
