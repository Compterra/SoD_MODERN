# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))

from src.constants.building_registry import BUILDING_REGISTRY, get_building_display_name_text  # type: ignore
from src.constants.center_modifier_registry import (  # type: ignore
    CENTER_MODIFIER_BY_KEY,
    CENTER_MODIFIER_REGISTRY,
    validate_center_modifier_registry,
)


OUT_PATH = ROOT / "docs" / "reports" / "center_modifier_system_audit.md"


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def main() -> int:
    issues = validate_center_modifier_registry()
    source_counts = Counter()
    modifier_totals = defaultdict(int)
    modifier_building_counts = Counter()
    building_rows = []

    for building in BUILDING_REGISTRY:
        modifiers = list(building.get("center_modifiers", ()))
        display_name = get_building_display_name_text(building["building_slot"])
        if not modifiers:
            building_rows.append((display_name, "-", "-", "-"))
            continue
        notes = []
        for modifier_key, value, source in modifiers:
            source_counts[source] += 1
            modifier_totals[modifier_key] += int(value)
            modifier_building_counts[modifier_key] += 1
            definition = CENTER_MODIFIER_BY_KEY.get(modifier_key, {})
            notes.append("%s %+d" % (definition.get("label", modifier_key), int(value)))
        building_rows.append((
            display_name,
            compact([str(value) for value in building.get("allowed_center_types", ())]),
            compact([str(value) for value in building.get("building_roles", ())]),
            compact(notes),
        ))

    lines = [
        "# Center Modifier System Audit",
        "",
        "This report summarizes the canonical center modifiers and the building-source contributions currently feeding them.",
        "",
        "## Summary",
        "",
        "- Modifiers registered: %d" % len(CENTER_MODIFIER_REGISTRY),
        "- Buildings registered: %d" % len(list(BUILDING_REGISTRY)),
        "- Registry validation issues: %d" % len(issues),
        "- Source entries: " + compact(["%s %d" % (key, value) for key, value in source_counts.most_common()]),
        "",
        "## Modifier Registry",
        "",
        "| ID | Modifier | Category | Type | Default | Bounds | Building sources | Building total |",
        "|---:|---|---|---|---:|---|---:|---:|",
    ]
    for definition in CENTER_MODIFIER_REGISTRY:
        key = str(definition["key"])
        lines.append(
            "| %s | %s | %s | %s | %s | %s..%s | %s | %s |"
            % (
                definition["id"],
                md(key),
                md(definition["category"]),
                md(definition["value_type"]),
                definition["default"],
                definition["min"],
                definition["max"],
                modifier_building_counts.get(key, 0),
                modifier_totals.get(key, 0),
            )
        )

    lines += [
        "",
        "## Building Modifier Sources",
        "",
        "| Building | Centers | Roles | Modifiers |",
        "|---|---|---|---|",
    ]
    for display_name, centers, roles, modifiers in sorted(building_rows):
        lines.append("| %s | %s | %s | %s |" % (md(display_name), md(centers), md(roles), md(modifiers)))

    if issues:
        lines += ["", "## Validation Issues", ""]
        lines.extend("- %s" % issue for issue in issues)

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote %s." % OUT_PATH.relative_to(ROOT))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
