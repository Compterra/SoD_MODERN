# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIALOG_ROOT = ROOT / "src" / "dialogs"
REPORT = ROOT / "docs" / "reports" / "dialogue_immersion" / "dialogue_state_inventory.md"
ORDER_DIALOGS = DIALOG_ROOT / "_order_dialogs.txt"


ENTRY_RE = re.compile(r"\[\s*([^,\]]+)\s*,\s*([\"'])([^\"']+)\2\s*,", re.MULTILINE)
ENTRY_WITH_CONDITIONS_RE = re.compile(
    r"\[\s*([^,\]]+)\s*,\s*([\"'])([^\"']+)\2\s*,\s*(\[[\s\S]*?\])\s*,\s*([\"'])([\s\S]*?)\4\s*,\s*([\"'])([^\"']+)\6\s*,\s*(\[[\s\S]*?\])\s*,",
    re.MULTILINE,
)

IMMERSION_FOCUS_STATES = (
    "start",
    "lord_start",
    "member_chat",
    "mayor_pretalk",
    "mayor_friendly_pretalk",
    "merchant_pretalk",
    "village_elder_pretalk",
    "ransom_broker_pretalk",
    "tavernkeeper_pretalk",
    "tavern_traveler_pretalk",
    "goods_merchant_pretalk",
    "gm_pretalk",
)

ENTRY_FALLBACK_NORMALIZED = re.compile(r"\s+")


def classify(path: Path) -> str:
    rel = path.relative_to(DIALOG_ROOT).as_posix()
    if rel.startswith("ZA01_startup_and_dispatch/"):
        return "startup_and_dispatch"
    if rel.startswith("ZB01_lords_politics_and_family/"):
        return "lords_politics_family"
    if rel.startswith("ZC01_centers_and_economy/"):
        return "centers_economy"
    if rel.startswith("ZC02_townsfolk_and_special_npcs/"):
        return "townsfolk_special_npcs"
    if rel.startswith("ZD01_encounters_battles_and_prisoners/"):
        return "encounters_battles_prisoners"
    if rel.startswith("ZE01_companions_and_named_npcs/"):
        return "companions_named_npcs"
    if rel.startswith("ZZ99_misc_dialogs/"):
        return "misc_dialogs"
    return rel.split("/", 1)[0]


def iter_entries() -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for path in sorted(DIALOG_ROOT.rglob("*.py")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        for speaker, _quote, state in ENTRY_RE.findall(raw):
            entries.append((path.relative_to(ROOT).as_posix(), speaker.strip(), state))
    return entries


def _iter_ordered_dialog_files() -> list[Path]:
    lines = []
    for line in ORDER_DIALOGS.read_text(encoding="utf-8", errors="replace").splitlines():
        rel = line.strip()
        if not rel or rel.startswith("#"):
            continue
        lines.append(DIALOG_ROOT / rel)
    return lines


def iter_ordered_entries() -> list[dict[str, str | int | bool | Path]]:
    entries: list[dict[str, str | int | bool | Path]] = []
    for path in _iter_ordered_dialog_files():
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        for match in ENTRY_WITH_CONDITIONS_RE.finditer(raw):
            state = match.group(3)
            conditions = match.group(5)
            target_state = match.group(7)
            line_no = raw.count("\n", 0, match.start()) + 1
            is_fallback = ENTRY_FALLBACK_NORMALIZED.sub("", conditions.strip()) == "[]"
            entries.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "state_in": state,
                    "state_out": target_state,
                    "conditions": conditions,
                    "is_fallback": is_fallback,
                    "line_no": line_no,
                }
            )
    return entries


def detect_immersion_coverage_gaps(
    state_focus: tuple[str, ...] = IMMERSION_FOCUS_STATES,
) -> tuple[
    list[tuple[str, str, int, str, int]],
    list[tuple[str, str, str]],
]:
    entries = iter_ordered_entries()
    by_state: dict[str, list[dict[str, str | int | bool | Path]]] = defaultdict(list)
    for entry in entries:
        by_state[str(entry["state_in"])].append(entry)

    shadowing: list[tuple[str, str, int, str, int]] = []
    missing: list[tuple[str, str, str]] = []

    for state in state_focus:
        state_entries = by_state.get(state, [])
        if not state_entries:
            missing.append((state, "state_missing_from_order", "no entries in ordered dialogue graph"))
            continue

        has_fallback = any(bool(entry["is_fallback"]) for entry in state_entries)
        has_specific = any(not bool(entry["is_fallback"]) for entry in state_entries)
        if has_specific and not has_fallback:
            first_specific = state_entries[0]
            missing.append(
                (
                    state,
                    "specific_only",
                    f"missing no-condition fallback in {first_specific['path']}:{first_specific['line_no']}",
                )
            )

        fallback_entry = None
        for entry in state_entries:
            if bool(entry["is_fallback"]):
                if fallback_entry is None:
                    fallback_entry = entry
                continue
            if fallback_entry is not None:
                shadowing.append(
                    (
                        state,
                        str(fallback_entry["path"]),
                        int(fallback_entry["line_no"]),
                        str(entry["path"]),
                        int(entry["line_no"]),
                    )
                )

    return shadowing, missing


def render() -> str:
    entries = iter_entries()
    by_state = Counter(state for _path, _speaker, state in entries)
    by_category = Counter(classify(ROOT / path) for path, _speaker, _state in entries)
    by_category_state = Counter((classify(ROOT / path), state) for path, _speaker, state in entries)

    lines: list[str] = [
        "# Dialogue State Inventory",
        "",
        "Generated by `build/dialogue_immersion_report.py`.",
        "",
        f"Total parsed dialogue entries: {len(entries)}",
        "",
        "## Top States",
        "",
        "| State | Entries |",
        "| --- | ---: |",
    ]
    for state, count in by_state.most_common(30):
        lines.append(f"| `{state}` | {count} |")

    lines.extend([
        "",
        "## Categories",
        "",
        "| Category | Entries |",
        "| --- | ---: |",
    ])
    for category, count in by_category.most_common():
        lines.append(f"| `{category}` | {count} |")

    lines.extend([
        "",
        "## High-Traffic Category States",
        "",
        "| Category | State | Entries |",
        "| --- | --- | ---: |",
    ])
    for (category, state), count in by_category_state.most_common(50):
        if count >= 5:
            lines.append(f"| `{category}` | `{state}` | {count} |")

    lines.extend([
        "",
        "## Notes",
        "",
        "- High-traffic states are the most likely places for broad fallback entries to shadow specific immersion entries.",
        "- Use this inventory when adding ambient lines to `start`, `lord_start`, `member_chat`, `mayor_pretalk`, `mayor_friendly_pretalk`, `merchant_pretalk`, `village_elder_pretalk`, `ransom_broker_pretalk`, `tavernkeeper_pretalk`, `tavern_traveler_pretalk`, `goods_merchant_pretalk`, `gm_pretalk`, and encounter states.",
        "",
    ])

    shadowing, missing_coverage = detect_immersion_coverage_gaps()

    lines.extend([
        "## High-Traffic Immersion Shadowing",
        "",
        "| State | Fallback Branch | Shadowed Entry |",
        "| --- | --- | --- |",
    ])
    if shadowing:
        for state, fallback_path, fallback_line, shadowed_path, shadowed_line in shadowing:
            lines.append(
                f"| `{state}` | `{fallback_path}:{fallback_line}` | `{shadowed_path}:{shadowed_line}` |"
            )
    else:
        lines.append("| `start` | `none` | `none` |")

    lines.extend([
        "",
        "## High-Traffic Immersion Coverage Gaps",
        "",
        "| State | Gap Type | Detail |",
        "| --- | --- | --- |",
    ])
    if missing_coverage:
        for state, gap_type, detail in missing_coverage:
            lines.append(f"| `{state}` | `{gap_type}` | {detail} |")
    else:
        lines.append("| `start` | `none` | no gaps detected |")

    return "\n".join(lines)


def main() -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render(), encoding="utf-8")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
