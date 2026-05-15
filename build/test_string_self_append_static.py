from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF_APPEND_RE = re.compile(r'str_store_string,\s*s(\d+),\s*"@\{s\1(?:\}|\^|,|\s)')


def iter_guarded_files() -> list[Path]:
    return sorted((ROOT / "src").rglob("*.py"))


def test_sod_reports_copy_before_appending_visible_strings() -> None:
    offenders: list[str] = []
    for path in iter_guarded_files():
        raw = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(raw.splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            if SELF_APPEND_RE.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()}")

    assert not offenders, "self-appending str_store_string calls:\n" + "\n".join(offenders)
