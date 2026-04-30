# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from slot_alias_config import ALIAS_GROUPS, EXPLICIT_ALIAS_BY_OWNER_VALUE

ROOT = Path(__file__).resolve().parents[1]
SRC_CONSTANTS = ROOT / "src" / "constants"
DEFAULT_REPORT_PATH = ROOT / "docs" / "reports" / "slot_allocation_report.txt"
IDS_DIR = ROOT / "compile" / "ids"

SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_ERROR = "error"

SLOT_NAME_RE = re.compile(r"^slot_[A-Za-z0-9_]+$")


@dataclass
class SlotDescriptor:
    name: str
    value: int
    path: Path
    line: int
    owner_prefix: str

    @property
    def location(self) -> str:
        return f"{self.path.relative_to(ROOT).as_posix()}:{self.line}"


def owner_prefix(name: str) -> str:
    parts = name.split("_")
    if len(parts) >= 3 and parts[1]:
        return f"slot_{parts[1]}_"
    return "slot_"


def safe_eval_int(expr: ast.AST, known: Dict[str, int]) -> Optional[int]:
    if isinstance(expr, ast.Constant) and isinstance(expr.value, int):
        return int(expr.value)
    if isinstance(expr, ast.Name):
        return known.get(expr.id)
    if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.USub):
        inner = safe_eval_int(expr.operand, known)
        return None if inner is None else -inner
    if isinstance(expr, ast.BinOp):
        left = safe_eval_int(expr.left, known)
        right = safe_eval_int(expr.right, known)
        if left is None or right is None:
            return None
        if isinstance(expr.op, ast.Add):
            return left + right
        if isinstance(expr.op, ast.Sub):
            return left - right
        if isinstance(expr.op, ast.Mult):
            return left * right
        if isinstance(expr.op, ast.FloorDiv):
            return left // right
        if isinstance(expr.op, ast.Mod):
            return left % right
    return None


def load_imported_id_constants() -> Dict[str, int]:
    known: Dict[str, int] = {}
    if not IDS_DIR.exists():
        return known
    for path in sorted(IDS_DIR.glob("ID_*.py"), key=lambda p: p.name.lower()):
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(raw, filename=path.as_posix())
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            value = safe_eval_int(node.value, known)
            if value is not None:
                known[target.id] = value
    return known


def scan_constant_slots() -> List[dict]:
    findings: List[dict] = []
    descriptors: List[SlotDescriptor] = []
    known_values: Dict[str, int] = load_imported_id_constants()

    if not SRC_CONSTANTS.exists():
        findings.append(
            {
                "severity": SEVERITY_ERROR,
                "message": f"Missing constants directory: {SRC_CONSTANTS}",
            }
        )
        return findings

    for path in sorted(SRC_CONSTANTS.glob("*.py"), key=lambda p: p.name.lower()):
        if path.name.startswith("_"):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(raw, filename=path.as_posix())
        except SyntaxError as exc:
            findings.append(
                {
                    "severity": SEVERITY_ERROR,
                    "message": f"Could not parse constants file {path.relative_to(ROOT).as_posix()}:{exc.lineno}",
                }
            )
            continue

        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue

            value = safe_eval_int(node.value, known_values)
            if value is not None:
                known_values[target.id] = value

            if not SLOT_NAME_RE.match(target.id):
                continue

            if value is None:
                findings.append(
                    {
                        "severity": SEVERITY_WARNING,
                        "message": (
                            f"Could not statically evaluate slot constant '{target.id}' "
                            f"in {path.relative_to(ROOT).as_posix()}:{getattr(node, 'lineno', 0)}"
                        ),
                    }
                )
                continue

            descriptors.append(
                SlotDescriptor(
                    name=target.id,
                    value=value,
                    path=path,
                    line=getattr(node, "lineno", 0),
                    owner_prefix=owner_prefix(target.id),
                )
            )

    findings.extend(detect_slot_conflicts(descriptors))
    return findings


def detect_slot_conflicts(descriptors: List[SlotDescriptor]) -> List[dict]:
    findings: List[dict] = []
    by_value: Dict[tuple[str, int], List[SlotDescriptor]] = {}

    for descriptor in descriptors:
        by_value.setdefault((descriptor.owner_prefix, descriptor.value), []).append(descriptor)

    for (prefix, value), items in sorted(by_value.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if len(items) < 2:
            continue
        items = sorted(items, key=lambda item: item.location.lower())
        unique_names = {item.name for item in items}
        explicit_aliases = EXPLICIT_ALIAS_BY_OWNER_VALUE.get((prefix, value))
        if len(unique_names) == 1:
            severity = SEVERITY_INFO
            label = "Mirrored slot value"
        elif explicit_aliases and unique_names.issubset(explicit_aliases):
            severity = SEVERITY_INFO
            label = "Intentional shared slot value"
        else:
            normalized = {_normalize_alias_name(item.name) for item in items}
            if len(normalized) == 1:
                severity = SEVERITY_INFO
                label = "Alias slot value"
            else:
                severity = SEVERITY_WARNING
                label = "Duplicate slot value"
        findings.append(
            {
                "severity": severity,
                "message": f"{label} {value} for owner group {prefix}",
                "locations": [f"{item.name} @ {item.location}" for item in items],
            }
        )

    return findings


def _normalize_alias_name(name: str) -> str:
    normalized = name
    replacements = (
        ("_begin", "_range_edge"),
        ("_end", "_range_edge"),
        ("_base", "_range_edge"),
        ("_first_", "_indexed_"),
        ("_last_", "_indexed_"),
    )
    for old, new in replacements:
        normalized = normalized.replace(old, new)

    parts = normalized.split("_", 2)
    if len(parts) >= 3:
        owner_prefix = f"{parts[0]}_{parts[1]}_"
        suffix = parts[2]
        for group in ALIAS_GROUPS:
            if suffix in group:
                suffix = sorted(group)[0]
                break
        normalized = f"{owner_prefix}{suffix}"
    return normalized


def write_slot_allocation_report(findings: List[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = ["Slot Allocation Verification Report", ""]
    if not findings:
        lines.append("No slot allocation findings.")
    else:
        grouped: Dict[str, List[dict]] = {}
        for finding in findings:
            grouped.setdefault(finding["severity"], []).append(finding)
        for severity in (SEVERITY_ERROR, SEVERITY_WARNING, SEVERITY_INFO):
            items = grouped.get(severity, [])
            if not items:
                continue
            lines.append(f"[{severity.upper()}] {len(items)} finding(s)")
            for item in items:
                lines.append(f"- {item['message']}")
                for extra in item.get("locations", []):
                    lines.append(f"    {extra}")
            lines.append("")
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def run_slot_allocation_verification(report_path: Path = DEFAULT_REPORT_PATH) -> dict:
    findings = scan_constant_slots()
    write_slot_allocation_report(findings, report_path)
    counts = {severity: 0 for severity in (SEVERITY_INFO, SEVERITY_WARNING, SEVERITY_ERROR)}
    for finding in findings:
        counts[finding["severity"]] = counts.get(finding["severity"], 0) + 1
    return {"findings": findings, "counts": counts, "report_path": report_path}


def main(argv: Optional[Iterable[str]] = None) -> int:
    result = run_slot_allocation_verification()
    counts = result["counts"]
    print(
        "[verify_slot_allocations] "
        f"error={counts.get(SEVERITY_ERROR, 0)} "
        f"warning={counts.get(SEVERITY_WARNING, 0)} "
        f"info={counts.get(SEVERITY_INFO, 0)} "
        f"report={result['report_path']}"
    )
    return 1 if counts.get(SEVERITY_ERROR, 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
