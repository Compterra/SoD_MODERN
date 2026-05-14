# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checked_roots = [
        ROOT / "src" / "menus",
        ROOT / "src" / "scripts",
        ROOT / "compile",
    ]
    offenders: list[str] = []
    for root in checked_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            raw = path.read_text(encoding="utf-8", errors="ignore")
            if "no formal standing" in raw:
                offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        raise AssertionError("Player-facing fallback leaked: " + ", ".join(offenders))
    print("[no_formal_standing_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
