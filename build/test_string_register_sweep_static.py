"""Reject runtime triggers that sweep a broad range of engine string registers.

String register inspection belongs in the external DevKit.  A recurring M&B
1.011 trigger that writes a broad register range can corrupt whatever screen
the engine is composing, even when it looks like a harmless debug utility.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SWEEP_THRESHOLD = 16
STRING_DESTINATION_RE = re.compile(
    r"\(\s*(?:str_store_string|str_clear|str_store_string_reg)\s*,\s*"
    r"(?:s(?P<string_register>\d+)|(?P<numeric_register>\d+))\b"
)


def active_string_register_sweeps() -> list[str]:
    findings: list[str] = []
    for path in sorted((ROOT / "src" / "triggers").rglob("*.py")):
        if path.name == "__init__.py" or "_preamble" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        destinations = {
            int(match.group("string_register") or match.group("numeric_register"))
            for match in STRING_DESTINATION_RE.finditer(raw)
        }
        if len(destinations) >= SWEEP_THRESHOLD:
            findings.append(
                f"{path.relative_to(ROOT).as_posix()} writes {len(destinations)} distinct string registers"
            )
    return findings


def main() -> int:
    sweeps = active_string_register_sweeps()
    if sweeps:
        raise AssertionError("Timed trigger string-register sweep(s):\n" + "\n".join(sweeps))
    print("test_string_register_sweep_static: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
