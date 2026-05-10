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

from src.constants.building_registry import BUILDING_REGISTRY, BUILDING_ROLE_LABELS, LEGACY_BUILDING_SCRIPT_EFFECT_EXCEPTIONS, get_building_display_name_text  # type: ignore
from src.constants.center_modifier_registry import BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER, BUILDING_FIELD_TO_CENTER_MODIFIER, CENTER_MODIFIER_BY_KEY  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "building_system_audit.md"


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def center_types(definition: dict[str, object]) -> list[str]:
    return [str(value) for value in definition.get("allowed_center_types", ())]


def effect_notes(definition: dict[str, object]) -> list[str]:
    notes: list[str] = []
    if int(definition.get("population_capacity_bonus", 0) or 0):
        notes.append("population capacity")
    if int(definition.get("weekly_population_growth_bonus", 0) or 0):
        notes.append("weekly population growth")
    if int(definition.get("raid_recovery_bonus", 0) or 0):
        notes.append("raid recovery")
    if int(definition.get("center_health_bonus", 0) or 0):
        notes.append("health cap")
    if int(definition.get("prosperity_cap_bonus", 0) or 0):
        notes.append("prosperity cap")
    if int(definition.get("weekly_income_bonus_percent", 0) or 0):
        notes.append("income")
    return notes


def building_roles(definition: dict[str, object]) -> list[str]:
    return [str(value) for value in definition.get("building_roles", ())]


def center_modifier_notes(definition: dict[str, object]) -> list[str]:
    notes: list[str] = []
    for modifier_key, value, _source in definition.get("center_modifiers", ()):
        modifier = CENTER_MODIFIER_BY_KEY.get(str(modifier_key), {})
        label = modifier.get("label", modifier_key)
        notes.append(f"{label} {int(value):+d}")
    return notes


def unmapped_effect_tags(definition: dict[str, object]) -> list[str]:
    return [
        str(tag)
        for tag in definition.get("effect_tags", ())
        if str(tag) not in BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER
    ]


def legacy_field_notes(definition: dict[str, object]) -> list[str]:
    notes: list[str] = []
    for field_name, modifier_key in BUILDING_FIELD_TO_CENTER_MODIFIER:
        value = int(definition.get(field_name, 0) or 0)
        if value:
            notes.append(f"{field_name} -> {modifier_key} {value:+d}")
    return notes


def main() -> int:
    rows = list(BUILDING_REGISTRY)
    by_center_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_specialization = Counter()
    by_role = Counter()
    by_role_center = defaultdict(Counter)
    for definition in rows:
        by_specialization[str(definition.get("specialization", "none"))] += 1
        for role in building_roles(definition):
            by_role[role] += 1
            for center_type in center_types(definition):
                by_role_center[role][center_type] += 1
        for center_type in center_types(definition):
            by_center_type[center_type].append(definition)

    population_linked = [row for row in rows if effect_notes(row)]
    lines = [
        "# Building System Audit",
        "",
        "This report summarizes building access, upkeep, and economy/population hooks from the building registry.",
        "",
        "## Summary",
        "",
        f"- Buildings registered: {len(rows)}",
        f"- Buildings with economy/population hooks: {len(population_linked)}",
        f"- Village buildings: {len(by_center_type.get('village', []))}",
        f"- Town buildings: {len(by_center_type.get('town', []))}",
        f"- Castle buildings: {len(by_center_type.get('castle', []))}",
        "- Specializations: " + compact([f"{key} {value}" for key, value in by_specialization.most_common()]),
        "- Building roles: " + compact([f"{key} {value}" for key, value in by_role.most_common()]),
        "",
        "## Building Role Matrix",
        "",
        "| Role | Label | Buildings | Village | Town | Castle |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for role, count in sorted(by_role.items()):
        centers = by_role_center[role]
        lines.append(
            f"| {md(role)} | {md(BUILDING_ROLE_LABELS.get(role, role.replace('_', ' ').title()))} | {count} | "
            f"{centers.get('village', 0)} | {centers.get('town', 0)} | {centers.get('castle', 0)} |"
        )
    lines += [
        "",
        "## Economy And Population Hooks",
        "",
        "| Building | Centers | Roles | Spec | Tier | Upkeep | Health | Prosperity cap | Prosperity % | Income % | Pop cap | Pop growth | Raid recovery | Notes |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for definition in sorted(rows, key=lambda row: (str(row.get("ui_category", "")), str(row.get("building_key", "")))):
        lines.append(
            f"| {md(get_building_display_name_text(definition['building_slot']))} | {compact(center_types(definition))} | "
            f"{compact(building_roles(definition))} | {md(definition.get('specialization', '-'))} | {definition.get('tier', 0)} | {definition.get('weekly_upkeep', 0)} | "
            f"{definition.get('center_health_bonus', 0)} | {definition.get('prosperity_cap_bonus', 0)} | "
            f"{definition.get('prosperity_multiplier_bonus_percent', 0)} | {definition.get('weekly_income_bonus_percent', 0)} | "
            f"{definition.get('population_capacity_bonus', 0)} | {definition.get('weekly_population_growth_bonus', 0)} | "
            f"{definition.get('raid_recovery_bonus', 0)} | {compact(effect_notes(definition))} |"
        )

    lines += [
        "",
        "## Design Notes",
        "",
        "- Health buildings raise effective population capacity, reducing crowding pressure in ideal health.",
        "- Civic/economic buildings can add small bounded growth only when health and prosperity are not collapsing.",
        "- Defensive recovery bonuses are modest and only help damaged centers stabilize; they are not prosperity engines.",
        "- Building effects are modifier-first: legacy fields and effect tags must derive center modifiers before any script consumes them.",
        "- Scripted building behavior should be limited to engine-facing exceptions such as messages, rare events, or compatibility wrappers.",
        "",
        "## Modifier Discipline",
        "",
        "| Building | Derived fields | Unmapped effect tags | Script exception policy |",
        "|---|---|---|---|",
    ]
    for definition in sorted(rows, key=lambda row: (str(row.get("ui_category", "")), str(row.get("building_key", "")))):
        lines.append(
            f"| {md(get_building_display_name_text(definition['building_slot']))} | "
            f"{compact(legacy_field_notes(definition))} | {compact(unmapped_effect_tags(definition))} | "
            f"{compact(list(LEGACY_BUILDING_SCRIPT_EFFECT_EXCEPTIONS))} |"
        )
    lines += [
        "",
        "## Center Modifier Sources",
        "",
        "| Building | Modifiers |",
        "|---|---|",
    ]
    for definition in sorted(rows, key=lambda row: (str(row.get("ui_category", "")), str(row.get("building_key", "")))):
        lines.append(
            f"| {md(get_building_display_name_text(definition['building_slot']))} | {compact(center_modifier_notes(definition))} |"
        )
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} buildings).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
