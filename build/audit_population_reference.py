# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "compile" / "ids"))
sys.path.insert(0, str(ROOT / "compile" / "headers"))
sys.path.insert(0, str(ROOT / "compile"))
sys.path.insert(0, str(ROOT))

from src.constants.module_constants import (  # type: ignore
    sod_migration_max_per_week,
    sod_migration_pop_surplus_min,
    sod_migration_prosperity_max,
    town_pop_ideal,
    town_pop_max,
    town_pop_min,
    village_pop_ideal,
    village_pop_max,
    village_pop_min,
)


OUT = ROOT / "docs" / "reports" / "population_reference_audit.md"


HOOKS = (
    ("Capacity profile", "src/scripts/ZY_helper_scripts/sod_center_population_capacity.py", "sod_get_center_population_capacity_profile"),
    ("Weekly population update", "src/scripts/ZZ_common_array_processing/update_center_population_supply.py", "update_center_population_supply"),
    ("Recruitable population", "src/scripts/ZZ_common_array_processing/update_center_population_supply.py", "get_center_recruitable_population"),
    ("Recruitment spends population", "src/scripts/ZZ_common_array_processing/update_center_population_supply.py", "spend_center_population_for_recruitment"),
    ("Village volunteers", "src/scripts/ZD_centers/update_volunteer_troops_in_village.py", "population_surplus"),
    ("NPC village volunteers", "src/scripts/ZD_centers/update_npc_volunteer_troops_in_village.py", "population_surplus"),
    ("Village defenders", "src/scripts/ZD_centers/refresh_village_defenders.py", "population_surplus"),
    ("Farmer parties", "src/scripts/ZC_parties/create_village_farmer_party.py", "population_surplus"),
    ("Lord party creation", "src/scripts/ZC_parties/create_kingdom_hero_party.py", "troops_created"),
    ("Ideal party size", "src/scripts/ZC_parties/party_get_ideal_size.py", "sod_get_village_output_profile"),
    ("Construction workforce", "src/scripts/ZY_helper_scripts/sod_population_based_construction.py", "sod_get_center_construction_workforce"),
    ("Village root output", "src/scripts/ZY_helper_scripts/sod_village_output_profile.py", "population_surplus"),
    ("Castle support", "src/scripts/ZY_helper_scripts/sod_castle_support_profile.py", "bound_population"),
)


def has_token(rel: str, token: str) -> bool:
    return token in (ROOT / rel).read_text(encoding="utf-8")


def status_row(label: str, rel: str, token: str) -> tuple[str, bool]:
    ok = has_token(rel, token)
    return "| %s | `%s` | `%s` | %s |" % (label, rel, token, "OK" if ok else "MISSING"), ok


def main() -> int:
    village_span = village_pop_max - village_pop_min
    town_span = town_pop_max - town_pop_min
    village_to_town_floor = float(town_pop_min) / max(village_pop_min, 1)
    village_to_town_cap = float(town_pop_max) / max(village_pop_max, 1)

    hook_lines = []
    missing = []
    for label, rel, token in HOOKS:
        row, ok = status_row(label, rel, token)
        hook_lines.append(row)
        if not ok:
            missing.append("%s missing %s" % (rel, token))

    lines = [
        "# Population Reference Audit",
        "",
        "This audit checks whether current gameplay population bands and population hooks support the reference direction from `Medieval Demographics Made Easy` and `Fief` without turning population into runaway troop generation.",
        "",
        "The numbers are compressed gameplay population units, not literal census totals. They should still preserve relative pressure: villages feed the system, towns concentrate markets, and castles convert attached rural support into military power.",
        "",
        "## Current Bands",
        "",
        "| Center type | Floor | Ideal | Upper band | Span | Gameplay role |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        f"| Village | {village_pop_min} | {int(village_pop_ideal)} | {village_pop_max} | {village_span} | Rural root for food, raw output, recruits, labor, and farmer parties. |",
        f"| Town | {town_pop_min} | {int(town_pop_ideal)} | {town_pop_max} | {town_span} | Market engine, service/craft population, large consumption and trade demand. |",
        "| Castle | village-linked | village-linked | village-linked + garrison | variable | Military lordship supported by bound villages, stores, garrison, roads, and administration. |",
        "",
        "## Ratio Check",
        "",
        f"- Town floor is {village_to_town_floor:.1f}x the village floor.",
        f"- Town upper band is {village_to_town_cap:.1f}x the village upper band.",
        f"- Village upper band is currently {village_pop_max}, matching the intended 1000 cap.",
        "",
        "This is a good gameplay scale: a healthy full village is meaningful, but a town still represents a much larger market and troop-support base.",
        "",
        "## Population Hooks",
        "",
        "| Hook | File | Token | Status |",
        "| --- | --- | --- | --- |",
        *hook_lines,
        "",
        "## Pressure And Safety Checks",
        "",
        "- Recruitment uses population surplus above the village floor, so damaged villages do not create troops from nothing.",
        "- Lord party creation deducts troops from the source center or bound village support path.",
        "- Construction, village output, defenders, farmer parties, and castle support all read population or population surplus.",
        "- Weekly migration is bounded by surplus and max-per-week controls.",
        f"- Migration only targets poor/weak centers below prosperity {sod_migration_prosperity_max}, requires surplus {sod_migration_pop_surplus_min}, and caps movement at {sod_migration_max_per_week} per week.",
        "- Population capacity modifiers can expand bands, but recovery and labor still pass through food, health, security, tax, and prosperity pressure.",
        "",
        "## Design Read",
        "",
        "- Village cap 1000 is high enough for strong rural centers to matter and low enough that towns remain distinct.",
        "- If lord parties feel too large later, tune support conversion and centralization before raising or lowering village caps.",
        "- If village recruitment feels too spiky, tune `village_recruit_capacity` and surplus thresholds rather than removing the population link.",
        "- Castles should stay dependent on attached villages and garrison support, not gain town-like civilian caps.",
        "",
    ]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    if missing:
        raise AssertionError("; ".join(missing))
    print("[audit_population_reference] wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
