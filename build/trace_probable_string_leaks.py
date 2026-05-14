# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reports" / "probable_string_leak_trace.md"

SOURCE_ROOTS = (
    ROOT / "src" / "scripts",
    ROOT / "src" / "menus",
    ROOT / "src" / "dialogs",
    ROOT / "src" / "triggers",
    ROOT / "src" / "presentations",
    ROOT / "src" / "mission_templates",
    ROOT / "src" / "quests",
)

PATTERNS: tuple[tuple[str, int, re.Pattern[str]], ...] = (
    (
        "exact symptom: companion-location style message",
        100,
        re.compile(r'display_message\s*,\s*"@[^"\n]*\{s\d+\} is in \{s\d+\}"'),
    ),
    (
        "exact symptom: faction switch notification",
        95,
        re.compile(r"has switched from \{s\d+\} to \{s\d+\}"),
    ),
    (
        "exact symptom: standalone mini-faction standing label",
        90,
        re.compile(r"unsettled account|unproven route friend"),
    ),
    (
        "symptom noun: Boar Clan text",
        45,
        re.compile(r"The Boar Clan"),
    ),
    (
        "single-register display",
        75,
        re.compile(r'\(\s*display_(?:log_)?message\s*,\s*"@\{s(\d+)\}"\s*,?'),
    ),
    (
        "helper return composed from string registers",
        70,
        re.compile(r'\(\s*str_store_string\s*,\s*":string"\s*,\s*"@\{s\d+\}'),
    ),
    (
        "self-appending string register",
        55,
        re.compile(r'\(\s*str_store_string\s*,\s*s(\d+)\s*,\s*"@\{s\1\}'),
    ),
    (
        "low-register nested store",
        35,
        re.compile(r'\(\s*str_store_string\s*,\s*s([0-9]|[1-4][0-9])\s*,\s*"@[^"\n]*\{s\d+\}'),
    ),
    (
        "debug display with string registers",
        30,
        re.compile(r"display_message\s*,\s*\"@[^\"\n]*\{s\d+\}[^\"\n]*\"\s*,\s*debug_color"),
    ),
)


@dataclass
class Finding:
    score: int
    kind: str
    path: Path
    line_no: int
    text: str


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for root in SOURCE_ROOTS:
        if root.exists():
            files.extend(sorted(path for path in root.rglob("*.py") if path.is_file()))
    return files


def code_part(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return ""
    hash_i = line.find("#")
    return (line if hash_i == -1 else line[:hash_i]).rstrip()


def scan() -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_source_files():
        raw = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(raw.splitlines(), start=1):
            code = code_part(line)
            if not code:
                continue
            for kind, score, pattern in PATTERNS:
                if pattern.search(code):
                    if "debug_color" in code and score > 35:
                        score -= 10
                    findings.append(Finding(score, kind, path, line_no, code.strip()))
                    break
    findings.sort(key=lambda item: (-item.score, rel(item.path), item.line_no))
    return findings


def compose(findings: list[Finding]) -> str:
    lines = [
        "# Probable String Leak Trace",
        "",
        "This is a focused trace for string-register bleed symptoms, separate from the broad string-register usage audit.",
        "",
        "## Current Rules",
        "",
        "- Direct display placeholders are safe only through `{s99}` in M&B 1.011.",
        "- `s100+` may be used as numeric scratch storage only, then copied down before display.",
        "- Highest-risk leak shape: display/log text that is only `@{sN}`, or helper-return strings composed from other `{sN}` placeholders.",
        "- The observed `is in The Boar Clan has switched...` trace matches a companion-location debug message adjacent to the faction-switch notification.",
        "",
        "## Top Probable Traces",
        "",
        "| Score | Kind | File | Line | Text |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for finding in findings[:80]:
        text = finding.text.replace("|", "\\|")
        if len(text) > 180:
            text = text[:177] + "..."
        lines.append(
            f"| {finding.score} | {finding.kind} | `{rel(finding.path)}` | {finding.line_no} | `{text}` |"
        )

    lines += [
        "",
        "## First Interpretation",
        "",
        "1. `update_companion_candidates_in_taverns` is the direct source of the `is in {s5}` fragment. It is cheat/debug output and can run near campaign refreshes.",
        "2. `entry_0087` is the direct source of the faction-switch notification. It now uses Native-style `str_store_troop_name_link`, so the earlier titled-name helper leak has been removed.",
        "3. `unsettled account` and `unproven route friend` are mini-faction standing labels stored in `s22`. If they ever appear alone, the likely path is a single-register display or a report string being shown after its scratch registers changed.",
        "4. Remaining high-priority cleanup is to eliminate or label single-register display calls and reduce report builders that self-append through low registers like `s1`.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    findings = scan()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(compose(findings), encoding="utf-8")
    print(f"[trace_probable_string_leaks] wrote {OUT.relative_to(ROOT)} ({len(findings)} finding(s))")


if __name__ == "__main__":
    main()
