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
    sod_castle_construction_bound_pop_divisor,
    sod_castle_construction_garrison_divisor,
    sod_castle_construction_min_garrison_labor,
    sod_castle_construction_support_divisor,
    sod_castle_construction_workforce_cap,
    sod_town_construction_pop_divisor,
    sod_town_construction_workforce_cap,
    sod_village_construction_pop_divisor,
    sod_village_construction_workforce_cap,
    town_pop_ideal,
    town_pop_max,
    town_pop_min,
    village_pop_ideal,
    village_pop_max,
    village_pop_min,
)


OUT = ROOT / "docs" / "reports" / "population_construction_reference_audit.md"


def workforce(population: int, divisor: int, cap: int) -> int:
    return min(cap, max(0, population // divisor))


def main() -> int:
    village_min_workforce = workforce(village_pop_min, sod_village_construction_pop_divisor, sod_village_construction_workforce_cap)
    village_ideal_workforce = workforce(int(village_pop_ideal), sod_village_construction_pop_divisor, sod_village_construction_workforce_cap)
    village_max_workforce = workforce(village_pop_max, sod_village_construction_pop_divisor, sod_village_construction_workforce_cap)
    town_min_workforce = workforce(town_pop_min, sod_town_construction_pop_divisor, sod_town_construction_workforce_cap)
    town_ideal_workforce = workforce(int(town_pop_ideal), sod_town_construction_pop_divisor, sod_town_construction_workforce_cap)
    town_max_workforce = workforce(town_pop_max, sod_town_construction_pop_divisor, sod_town_construction_workforce_cap)

    lines = [
        "# Population And Construction Reference Audit",
        "",
        "This audit compares the current population bands and labor-driven construction settings against the reference direction from `Medieval Demographics Made Easy` and `Fief`.",
        "",
        "The module still uses compressed gameplay population units, not a literal census. The important balance rule is relative scale: villages are the rural root, towns are larger market engines, and castles depend on attached villages plus limited garrison labor.",
        "",
        "## Settlement Bands",
        "",
        "| Center type | Floor | Ideal | Capacity | Design read |",
        "|---|---:|---:|---:|---|",
        f"| Village | {village_pop_min} | {int(village_pop_ideal)} | {village_pop_max} | Rural settlement with enough households for food, recruits, and labor but fragile under raids. |",
        f"| Town | {town_pop_min} | {int(town_pop_ideal)} | {town_pop_max} | Market center consuming rural surplus and supporting services/crafts. |",
        "| Castle | local civilian base is small | village-linked | village-linked + garrison | Military lordship drawing support from bound villages, stores, garrison, and administration. |",
        "",
        "## Weekly Construction Labor",
        "",
        "| Source | Divisor/cap | At floor | At ideal | At capacity | Notes |",
        "|---|---|---:|---:|---:|---|",
        f"| Village population | pop / {sod_village_construction_pop_divisor}, cap {sod_village_construction_workforce_cap} | {village_min_workforce} | {village_ideal_workforce} | {village_max_workforce} | Fast local labor, but small absolute cap. |",
        f"| Town population | pop / {sod_town_construction_pop_divisor}, cap {sod_town_construction_workforce_cap} | {town_min_workforce} | {town_ideal_workforce} | {town_max_workforce} | Larger labor pool with urban overhead. |",
        f"| Castle bound villages | bound pop / {sod_castle_construction_bound_pop_divisor} | - | - | - | Main civilian support path. |",
        f"| Castle support score | support / {sod_castle_construction_support_divisor} | - | - | - | Administration, roads, stores, villages, commander, and security. |",
        f"| Castle garrison | garrison / {sod_castle_construction_garrison_divisor}, min {sod_castle_construction_min_garrison_labor}, cap {sod_castle_construction_workforce_cap} | - | - | - | Limited military labor keeps zero-pop castles from magically building without a garrison. |",
        "",
        "## Design Checks",
        "",
        "- Population-based construction remains weekly and labor-driven.",
        "- Zero-population villages and towns produce no construction labor.",
        "- Zero-population castles only progress from attached-village support, castle support systems, and limited garrison labor.",
        "- Construction speed modifiers still apply after population, health, prosperity, food, security, and unrest shape the labor pool.",
        "",
        "## Future Tuning Questions",
        "",
        "- Should towns above the ideal population suffer stronger food and unrest pressure before they reach the capacity cap?",
        "- Should castles with no bound villages require a minimum garrison before any construction progress is possible?",
        "- Should high-quality roads or contracted security increase castle access to bound-village labor?",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
