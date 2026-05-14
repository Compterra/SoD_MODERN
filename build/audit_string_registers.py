# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reports" / "string_register_usage_report.md"

SOURCE_ROOTS = (
    ROOT / "src" / "scripts",
    ROOT / "src" / "menus",
    ROOT / "src" / "dialogs",
    ROOT / "src" / "triggers",
    ROOT / "src" / "presentations",
    ROOT / "src" / "mission_templates",
    ROOT / "src" / "quests",
)
GENERATED_ROOT = ROOT / "compile"
EXPORT_ROOT = ROOT / "_export"

DIRECT_S_RE = re.compile(r"(?<![A-Za-z0-9_])s(\d+)(?![A-Za-z0-9_])")
FORMAT_S_RE = re.compile(r"\{s(\d+)\}")
STORE_S_RE = re.compile(r"\(\s*(str_store_[A-Za-z0-9_]+|str_clear)\s*,\s*(?:s(\d+)|(\d+))\b")
DEFERRED_STORE_RE = re.compile(
    r"\(\s*str_store_string\s*,\s*(?:s(\d+)|(\d+))\s*,\s*(?:\"@|@|')?[^,\n]*\{(?:s|reg)\d+\}"
)
DISPLAY_SREG_RE = re.compile(r"\(\s*(display_message|display_log_message)\s*,\s*(?:s(\d+)|(\d+))\b")
LIVE_MESSAGE_RE = re.compile(
    r"\(\s*(display_message|display_log_message|add_[A-Za-z0-9_]+_note_from_sreg)\s*,\s*"
    r"(?:@|\"@|')?[^,\n]*\{s(\d+)\}"
)
CONDITIONAL_INNER_PLACEHOLDER_RE = re.compile(r"\{(?:reg|s)\d+\?[^{}]*(?:\{(?:reg|s)\d+)")
MALFORMED_REGISTER_PLACEHOLDER_RE = re.compile(r"\{reg(?:\?|\}|[^A-Za-z0-9_}\d])")
NESTED_STRING_STORE_RE = re.compile(
    r"\(\s*str_store_string\s*,\s*([^,]+)\s*,\s*(?:\"@|@|')?[^,\n]*\{s\d+\}"
)


@dataclass
class Finding:
    scope: str
    path: str
    line_no: int
    kind: str
    register: str
    text: str


@dataclass
class ScanResult:
    label: str
    files: int
    direct: Counter[str]
    stores: Counter[str]
    placeholders: Counter[str]
    live_messages: list[Finding]
    sreg_messages: list[Finding]
    deferred_messages: list[Finding]
    nested_string_stores: list[Finding]
    unsupported_placeholders: list[Finding]
    nested_conditionals: list[Finding]
    malformed_placeholders: list[Finding]
    top_files: Counter[str]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.py") if path.is_file())


def iter_text_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.glob("*.txt") if path.is_file())


def code_part(line: str) -> str:
    """Drop full-line comments while preserving M&B 1.011 string literals enough for regex audit."""
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return ""
    return line.rstrip("\n")


def scan(label: str, files: list[Path]) -> ScanResult:
    direct: Counter[str] = Counter()
    stores: Counter[str] = Counter()
    placeholders: Counter[str] = Counter()
    live_messages: list[Finding] = []
    sreg_messages: list[Finding] = []
    deferred_messages: list[Finding] = []
    nested_string_stores: list[Finding] = []
    unsupported_placeholders: list[Finding] = []
    nested_conditionals: list[Finding] = []
    malformed_placeholders: list[Finding] = []
    top_files: Counter[str] = Counter()

    for path in files:
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = path.read_text(encoding="latin-1")
        file_hits = 0
        last_deferred_store: dict[str, tuple[int, str]] = {}
        for line_no, line in enumerate(raw.splitlines(), start=1):
            code = code_part(line)
            if not code:
                continue
            if label == "Generated export" and path.name == "quick_strings.txt" and " " in code:
                code = code.split(" ", 1)[1]
            for match in DIRECT_S_RE.finditer(code):
                reg = f"s{match.group(1)}"
                direct[reg] += 1
                file_hits += 1
            for match in STORE_S_RE.finditer(code):
                reg_no = match.group(2) or match.group(3)
                reg = f"s{reg_no}"
                stores[reg] += 1
            for match in FORMAT_S_RE.finditer(code):
                reg = f"s{match.group(1)}"
                placeholders[reg] += 1
                if int(match.group(1)) >= 100:
                    unsupported_placeholders.append(
                        Finding(
                            scope=label,
                            path=rel(path),
                            line_no=line_no,
                            kind="unsupported_direct_s_placeholder",
                            register=reg,
                            text=code.strip(),
                        )
                    )
            deferred_match = DEFERRED_STORE_RE.search(code)
            if deferred_match:
                reg_no = deferred_match.group(1) or deferred_match.group(2)
                last_deferred_store[f"s{reg_no}"] = (line_no, code.strip())
            display_match = DISPLAY_SREG_RE.search(code)
            if display_match:
                reg_no = display_match.group(2) or display_match.group(3)
                reg = f"s{reg_no}"
                sreg_messages.append(
                    Finding(
                        scope=label,
                        path=rel(path),
                        line_no=line_no,
                        kind=f"{display_match.group(1)}_sreg",
                        register=reg,
                        text=code.strip(),
                    )
                )
                if reg in last_deferred_store:
                    store_line_no, store_text = last_deferred_store[reg]
                    deferred_messages.append(
                        Finding(
                            scope=label,
                            path=rel(path),
                            line_no=line_no,
                            kind=f"deferred_{display_match.group(1)}",
                            register=reg,
                            text=f"{store_text} -> {code.strip()}",
                        )
                    )
            for match in LIVE_MESSAGE_RE.finditer(code):
                reg = f"s{match.group(2)}"
                live_messages.append(
                    Finding(
                        scope=label,
                        path=rel(path),
                        line_no=line_no,
                        kind=match.group(1),
                        register=reg,
                        text=code.strip(),
                    )
                )
            for match in CONDITIONAL_INNER_PLACEHOLDER_RE.finditer(code):
                nested_conditionals.append(
                    Finding(
                        scope=label,
                        path=rel(path),
                        line_no=line_no,
                        kind="conditional_inner_placeholder",
                        register="text",
                        text=code.strip(),
                    )
                )
                break
            for match in NESTED_STRING_STORE_RE.finditer(code):
                nested_string_stores.append(
                    Finding(
                        scope=label,
                        path=rel(path),
                        line_no=line_no,
                        kind="nested_string_store",
                        register=match.group(1).strip().strip('"'),
                        text=code.strip(),
                    )
                )
                break
            for match in MALFORMED_REGISTER_PLACEHOLDER_RE.finditer(code):
                malformed_placeholders.append(
                    Finding(
                        scope=label,
                        path=rel(path),
                        line_no=line_no,
                        kind="malformed_register_placeholder",
                        register="text",
                        text=code.strip(),
                    )
                )
                break
        if file_hits:
            top_files[rel(path)] = file_hits

    return ScanResult(
        label=label,
        files=len(files),
        direct=direct,
        stores=stores,
        placeholders=placeholders,
        live_messages=live_messages,
        sreg_messages=sreg_messages,
        deferred_messages=deferred_messages,
        nested_string_stores=nested_string_stores,
        unsupported_placeholders=unsupported_placeholders,
        nested_conditionals=nested_conditionals,
        malformed_placeholders=malformed_placeholders,
        top_files=top_files,
    )


def table(counter: Counter[str], label: str = "Register", limit: int = 30) -> list[str]:
    lines = [f"| {label} | Count |", "| --- | ---: |"]
    for key, count in counter.most_common(limit):
        lines.append(f"| `{key}` | {count} |")
    if not counter:
        lines.append("| none | 0 |")
    return lines


def top_file_table(counter: Counter[str], limit: int = 25) -> list[str]:
    lines = ["| File | Direct `s*` refs |", "| --- | ---: |"]
    for path, count in counter.most_common(limit):
        lines.append(f"| `{path}` | {count} |")
    if not counter:
        lines.append("| none | 0 |")
    return lines


def severity(finding: Finding) -> str:
    if "debug_color" in finding.text:
        if finding.scope == "Source":
            return "Low"
        return "Generated low"
    if finding.scope == "Source" and finding.kind == "display_message_sreg":
        return "High"
    if finding.scope == "Source" and finding.kind == "unsupported_direct_s_placeholder":
        return "High"
    if finding.scope == "Source" and finding.kind == "display_log_message_sreg":
        return "Low"
    if finding.scope == "Source" and finding.kind == "display_message":
        reg_no = int(finding.register[1:])
        return "Medium" if reg_no >= 50 else "Native"
    if finding.scope == "Source" and finding.kind == "deferred_display_message":
        return "High"
    if finding.scope == "Source" and finding.kind.startswith("add_"):
        return "Medium"
    if finding.scope == "Source" and finding.kind in ("display_log_message", "deferred_display_log_message"):
        return "Low"
    if finding.kind == "display_message":
        return "Generated mirror"
    return "Generated low"


def finding_table(findings: list[Finding], limit: int = 80, include_text: bool = False) -> list[str]:
    if include_text:
        lines = ["| Severity | Scope | File | Kind | Register | Line | Text |", "| --- | --- | --- | --- | --- | ---: | --- |"]
    else:
        lines = ["| Severity | Scope | File | Kind | Register | Line |", "| --- | --- | --- | --- | --- | ---: |"]
    for finding in findings[:limit]:
        sev = severity(finding)
        if include_text:
            text = finding.text.replace("|", "\\|")
            if len(text) > 120:
                text = text[:117] + "..."
            lines.append(f"| {sev} | {finding.scope} | `{finding.path}` | `{finding.kind}` | `{finding.register}` | {finding.line_no} | `{text}` |")
        else:
            lines.append(f"| {sev} | {finding.scope} | `{finding.path}` | `{finding.kind}` | `{finding.register}` | {finding.line_no} |")
    if not findings:
        if include_text:
            lines.append("| none | none | none | none | none | 0 | none |")
        else:
            lines.append("| none | none | none | none | none | 0 |")
    return lines


def high_risk_file_table(findings: list[Finding], limit: int = 20) -> list[str]:
    grouped: dict[str, list[Finding]] = {}
    for finding in findings:
        grouped.setdefault(finding.path, []).append(finding)
    ordered = sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0].lower()))
    lines = ["| File | High risks | First line |", "| --- | ---: | ---: |"]
    for path, file_findings in ordered[:limit]:
        first_line = min(finding.line_no for finding in file_findings)
        lines.append(f"| `{path}` | {len(file_findings)} | {first_line} |")
    if not ordered:
        lines.append("| none | 0 | 0 |")
    return lines


def compose(results: list[ScanResult]) -> str:
    total_live = sum(len(result.live_messages) for result in results)
    total_sreg = sum(len(result.sreg_messages) for result in results)
    total_deferred = sum(len(result.deferred_messages) for result in results)
    total_nested_stores = sum(len(result.nested_string_stores) for result in results)
    total_unsupported = sum(len(result.unsupported_placeholders) for result in results)
    total_nested = sum(len(result.nested_conditionals) for result in results)
    total_malformed = sum(len(result.malformed_placeholders) for result in results)
    source = next(result for result in results if result.label == "Source")
    generated = next(result for result in results if result.label == "Generated compile")
    export = next((result for result in results if result.label == "Generated export"), None)

    lines = [
        "# String Register Usage Audit",
        "",
        "This report counts Mount&Blade 1.011 string-register usage (`s*`) so register-heavy systems can be reviewed before placeholder bleed reaches the player.",
        "",
        "## Summary",
        "",
        f"- Source files scanned: {source.files}",
        f"- Generated compile files scanned: {generated.files}",
        f"- Generated export files scanned: {export.files if export else 0}",
        f"- Source direct `s*` references: {sum(source.direct.values())}",
        f"- Generated export direct `s*` references: {sum(export.direct.values()) if export else 0}",
        f"- Source string-register stores/clears: {sum(source.stores.values())}",
        f"- Source `{{s*}}` placeholders: {sum(source.placeholders.values())}",
        f"- Native-style inline display/log placeholders found: {total_live}",
        f"- Non-native string-register display calls found: {total_sreg}",
        f"- Deferred string-register display risks found: {total_deferred}",
        f"- Nested string-register store risks found: {total_nested_stores}",
        f"- Unsupported direct `{{s100+}}` placeholders found: {total_unsupported}",
        f"- Conditional placeholders containing inner placeholders found: {total_nested}",
        f"- Malformed register placeholders found: {total_malformed}",
        "",
        "## How To Read This",
        "",
        "- Native M&B 1.011 uses `display_message, \"@...{sN}...\"` or `display_message, \"str_*\"` directly. It does not use `display_message, sN`.",
        "- `str_store_string, sN, \"@...{sX}...\"` followed by `display_message, sN` is non-native and can leave the recent-message log pointing at a mutable string register.",
        "- `str_store_string` that stores text containing `{sN}` into another string register can leak if that result is displayed after `sN` changes. Prefer direct native store operations for names used in messages.",
        "- Inline `display_message` / `display_log_message` placeholders are counted so high-register uses can be reviewed, but this is the native pattern.",
        "- Direct placeholders work through `{s99}` in M&B 1.011. Registers `s100+` can be stored and copied with operations such as `str_store_string_reg`, but `{s100}` renders as `UNRECOGNIZED TOKEN`.",
        "- High-numbered registers are not automatically wrong, but frequent use of `s50+` deserves care because many report helpers treat that range as scratch space.",
        "- Simple lane policy for new SoD code: use `s68-s99` for new feature text/debug probes when possible; treat `s0-s19` as volatile Native scratch and `s20-s67` as legacy report scratch.",
        "- M&B 1.011 does not reliably parse placeholders inside conditional placeholder arms, such as `{reg1?{reg1}:No}` or `{reg2?...{s2}...:}`. Prefer script branches that store plain final text.",
        "- `process_strings.py` and quick-string export are vanilla-pass-through: they replace spaces with underscores but do not validate placeholder syntax.",
        "",
        "## Simple Register Lanes",
        "",
        "| Range | Use | Rule of thumb |",
        "| --- | --- | --- |",
        "| `s0-s19` | Native/dialog/display scratch | Use only very locally; assume another script may overwrite it. |",
        "| `s20-s49` | Existing report/helper scratch | Reuse only after checking the current feature path. |",
        "| `s50-s67` | Legacy high scratch | Collision-prone because Native notes and older SoD reports use it heavily. |",
        "| `s68-s99` | New SoD feature text | Preferred for new non-Native helpers and debug probes. |",
        "| `s100+` | Copy-only scratch | Never use as direct `{s100}` display text. Copy down first. |",
        "",
    ]

    for result in results:
        high_regs = Counter({reg: count for reg, count in result.direct.items() if int(reg[1:]) >= 50})
        lines += [
            f"## {result.label}",
            "",
            "### Most Used String Registers",
            "",
            *table(result.direct),
            "",
            "### Most Written String Registers",
            "",
            *table(result.stores),
            "",
            "### Most Referenced Placeholders",
            "",
            *table(result.placeholders),
            "",
            "### High Register Usage (`s50+`)",
            "",
            *table(high_regs),
            "",
            "### Top Files By Direct `s*` References",
            "",
            *top_file_table(result.top_files),
            "",
        ]

    live_findings: list[Finding] = []
    for result in results:
        live_findings.extend(result.live_messages)
    live_by_reg = Counter(finding.register for finding in live_findings)
    live_by_kind = Counter(finding.kind for finding in live_findings)
    live_by_severity = Counter(severity(finding) for finding in live_findings)
    source_high = [
        finding for finding in live_findings
        if finding.scope == "Source" and severity(finding) == "High"
    ]
    source_high_by_file = Counter(finding.path for finding in source_high)
    source_high.sort(key=lambda finding: (-source_high_by_file[finding.path], finding.path.lower(), finding.line_no))

    lines += [
        "## Native Inline Display/Log Placeholder Usage",
        "",
        "These follow the native M&B 1.011 style. Review high-numbered registers and long-lived debug text first.",
        "",
        "### Severity Buckets",
        "",
        *table(live_by_severity, label="Severity"),
        "",
        "### Top High-Risk Source Files",
        "",
        *high_risk_file_table(source_high),
        "",
        "### Top 20 High-Risk Source Findings",
        "",
        *finding_table(source_high, limit=20, include_text=True),
        "",
        "### By Register",
        "",
        *table(live_by_reg),
        "",
        "### By Operation",
        "",
        *table(live_by_kind, label="Operation"),
        "",
        "### First Findings",
        "",
        *finding_table(live_findings),
        "",
    ]

    sreg_findings: list[Finding] = []
    for result in results:
        sreg_findings.extend(result.sreg_messages)
    sreg_by_reg = Counter(finding.register for finding in sreg_findings)
    sreg_by_kind = Counter(finding.kind for finding in sreg_findings)
    sreg_by_severity = Counter(severity(finding) for finding in sreg_findings)
    source_sreg_high = [
        finding for finding in sreg_findings
        if finding.scope == "Source" and severity(finding) == "High"
    ]
    source_sreg_high_by_file = Counter(finding.path for finding in source_sreg_high)
    source_sreg_high.sort(key=lambda finding: (-source_sreg_high_by_file[finding.path], finding.path.lower(), finding.line_no))

    lines += [
        "## Non-Native String-Register Display Risks",
        "",
        "These are `display_message, sN` or `display_log_message, sN` calls. Vanilla M&B 1.011 has zero of these in module files.",
        "",
        "### Severity Buckets",
        "",
        *table(sreg_by_severity, label="Severity"),
        "",
        "### Top High-Risk Source Files",
        "",
        *high_risk_file_table(source_sreg_high),
        "",
        "### Top 20 High-Risk Source Findings",
        "",
        *finding_table(source_sreg_high, limit=20, include_text=True),
        "",
        "### By Register",
        "",
        *table(sreg_by_reg),
        "",
        "### By Operation",
        "",
        *table(sreg_by_kind, label="Operation"),
        "",
    ]

    deferred_findings: list[Finding] = []
    for result in results:
        deferred_findings.extend(result.deferred_messages)
    deferred_by_severity = Counter(severity(finding) for finding in deferred_findings)
    source_deferred_high = [
        finding for finding in deferred_findings
        if finding.scope == "Source" and severity(finding) == "High"
    ]
    source_deferred_high_by_file = Counter(finding.path for finding in source_deferred_high)
    source_deferred_high.sort(key=lambda finding: (-source_deferred_high_by_file[finding.path], finding.path.lower(), finding.line_no))

    lines += [
        "## Deferred String-Register Display Risks",
        "",
        "These are `str_store_string` compositions with `{sN}` or `{regN}` that are later displayed through the same string register. In M&B 1.011 message history, these can still resolve against later register values.",
        "",
        "### Severity Buckets",
        "",
        *table(deferred_by_severity, label="Severity"),
        "",
        "### Top High-Risk Source Files",
        "",
        *high_risk_file_table(source_deferred_high),
        "",
        "### Top 20 High-Risk Source Findings",
        "",
        *finding_table(source_deferred_high, limit=20, include_text=True),
        "",
    ]

    nested_store_findings: list[Finding] = []
    for result in results:
        nested_store_findings.extend(result.nested_string_stores)
    nested_store_by_dest = Counter(finding.register for finding in nested_store_findings)
    source_nested_stores = [
        finding for finding in nested_store_findings
        if finding.scope == "Source"
    ]

    lines += [
        "## Nested String-Register Store Risks",
        "",
        "These are `str_store_string` calls that save text containing `{sN}` into another string register or destination parameter. They are common in long report builders, but risky for message-log text and helper return values.",
        "",
        "### By Destination",
        "",
        *table(nested_store_by_dest, label="Destination"),
        "",
        "### First Source Findings",
        "",
        *finding_table(source_nested_stores, limit=80, include_text=True),
        "",
    ]

    unsupported_findings: list[Finding] = []
    for result in results:
        unsupported_findings.extend(result.unsupported_placeholders)
    unsupported_by_reg = Counter(finding.register for finding in unsupported_findings)
    source_unsupported = [
        finding for finding in unsupported_findings
        if finding.scope == "Source"
    ]

    lines += [
        "## Unsupported Direct Placeholder Risks",
        "",
        "These are direct `{s100}` or higher placeholders. M&B 1.011 can store these registers and copy them back to lower string registers, but the formatter does not recognize them directly.",
        "",
        "### By Register",
        "",
        *table(unsupported_by_reg),
        "",
        "### Source Findings",
        "",
        *finding_table(source_unsupported, limit=80, include_text=True),
        "",
    ]

    nested_findings: list[Finding] = []
    malformed_findings: list[Finding] = []
    for result in results:
        nested_findings.extend(result.nested_conditionals)
        malformed_findings.extend(result.malformed_placeholders)

    lines += [
        "## Conditional Placeholder Parse Risks",
        "",
        "These are `{regN?...:...}` or `{sN?...:...}` conditionals whose true/false arm contains another `{regN}` or `{sN}` placeholder. M&B 1.011 can render these literally.",
        "",
        "### Nested Conditional Findings",
        "",
        *finding_table(nested_findings, limit=80, include_text=True),
        "",
        "### Malformed `reg` Placeholder Findings",
        "",
        *finding_table(malformed_findings, limit=80, include_text=True),
        "",
    ]

    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit M&B 1.011 string-register usage and exported placeholder risks."
    )
    parser.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="Exit non-zero when non-native s-register display, deferred display, unsupported direct s100+ placeholders, or malformed register placeholders are found.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args([] if argv is None else argv)
    source_files: list[Path] = []
    for root in SOURCE_ROOTS:
        source_files.extend(iter_files(root))
    generated_files = sorted(GENERATED_ROOT.glob("module_*.py")) if GENERATED_ROOT.exists() else []
    export_files = iter_text_files(EXPORT_ROOT)

    results = [
        scan("Source", source_files),
        scan("Generated compile", generated_files),
        scan("Generated export", export_files),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(compose(results), encoding="utf-8")
    live_count = sum(len(result.live_messages) for result in results)
    sreg_count = sum(len(result.sreg_messages) for result in results)
    deferred_count = sum(len(result.deferred_messages) for result in results)
    nested_store_count = sum(len(result.nested_string_stores) for result in results)
    unsupported_count = sum(len(result.unsupported_placeholders) for result in results)
    nested_count = sum(len(result.nested_conditionals) for result in results)
    malformed_count = sum(len(result.malformed_placeholders) for result in results)
    print(
        "[audit_string_registers] wrote "
        f"{OUT.relative_to(ROOT)} "
        f"({live_count} live placeholder(s), "
        f"{sreg_count} s-register display risk(s), "
        f"{deferred_count} deferred display risk(s), "
        f"{nested_store_count} nested string-store risk(s), "
        f"{unsupported_count} unsupported direct placeholder(s), "
        f"{nested_count} conditional parse risk(s), "
        f"{malformed_count} malformed placeholder(s))"
    )
    critical_count = sreg_count + deferred_count + unsupported_count + malformed_count
    if args.fail_on_critical and critical_count:
        raise SystemExit(
            "[audit_string_registers] critical text export risk(s) found: "
            f"{sreg_count} s-register display, "
            f"{deferred_count} deferred display, "
            f"{unsupported_count} unsupported direct placeholder, "
            f"{malformed_count} malformed placeholder. "
            f"See {OUT.relative_to(ROOT)}."
        )


if __name__ == "__main__":
    main(sys.argv[1:])
