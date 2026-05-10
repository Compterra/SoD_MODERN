from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))
sys.path.insert(0, str(ROOT / "src" / "constants"))

from header_items import (  # type: ignore
    food_quality,
    get_abundance,
    get_max_ammo,
    get_weight,
    itp_consumable,
    itp_food,
    itp_merchandise,
    itp_type_goods,
)

from audit_item_systems import all_item_rows, item_type, md, write  # type: ignore


OUT = ROOT / "docs" / "reports" / "trade_goods_value_audit.md"


ROLE_BANDS = {
    "staple_food": (25, 95, 95, 140, "Cheap staples should move often and stabilize food stores."),
    "preserved_food": (55, 130, 80, 125, "Preserved foods are denser and more valuable but still common."),
    "livestock_food": (70, 150, 75, 120, "Meat and dairy support health and morale with moderate trade value."),
    "drink_luxury_food": (150, 320, 45, 90, "Ale and wine are food-adjacent luxuries with lower abundance."),
    "raw_material": (90, 320, 70, 130, "Raw inputs should feed production and broad caravan flow."),
    "semi_luxury_raw": (260, 520, 65, 100, "High-value rural exports such as furs bridge raw materials and luxuries."),
    "strategic_material": (240, 520, 45, 95, "Iron, tools, oil, and salt should matter for logistics and production."),
    "luxury": (350, 1200, 20, 70, "Luxury goods should be high-value, lower-volume wealth movers."),
}


ROLE_BY_ITEM = {
    "grain": "staple_food",
    "flour": "staple_food",
    "bread": "staple_food",
    "cabbages": "staple_food",
    "apples": "staple_food",
    "smoked_fish": "preserved_food",
    "dried_meat": "preserved_food",
    "sausages": "preserved_food",
    "cattle_meat": "livestock_food",
    "pork": "livestock_food",
    "chicken": "livestock_food",
    "cheese": "livestock_food",
    "butter": "livestock_food",
    "honey": "livestock_food",
    "ale": "drink_luxury_food",
    "wine": "drink_luxury_food",
    "wool": "raw_material",
    "pottery": "raw_material",
    "linen": "raw_material",
    "furs": "semi_luxury_raw",
    "salt": "strategic_material",
    "iron": "strategic_material",
    "oil": "strategic_material",
    "tools": "strategic_material",
    "spice": "luxury",
    "velvet": "luxury",
}


def role_for(row: dict[str, object]) -> str:
    item_id = str(row["id"])
    if item_id in ROLE_BY_ITEM:
        return ROLE_BY_ITEM[item_id]
    flags = int(row["flags"])
    if flags & itp_food:
        return "staple_food"
    return "raw_material"


def notes_for(row: dict[str, object], role: str) -> list[str]:
    value_min, value_max, abundance_min, abundance_max, _summary = ROLE_BANDS[role]
    value = int(row["value"])
    abundance = get_abundance(int(row["stats"]))
    notes: list[str] = []
    if value < value_min:
        notes.append(f"value below {value_min}")
    if value > value_max:
        notes.append(f"value above {value_max}")
    if abundance < abundance_min:
        notes.append(f"abundance below {abundance_min}")
    if abundance > abundance_max:
        notes.append(f"abundance above {abundance_max}")
    if not bool(row["merchandise"]):
        notes.append("not buyable")
    if bool(int(row["flags"]) & itp_food) and get_max_ammo(int(row["stats"])) <= 0:
        notes.append("food has zero stack")
    return notes


def main() -> None:
    rows = [
        row for row in all_item_rows()
        if item_type(int(row["flags"])) == itp_type_goods and str(row["id"]) != "horse_meat"
    ]
    counts = Counter(role_for(row) for row in rows)
    watch = []
    for row in rows:
        role = role_for(row)
        notes = notes_for(row, role)
        if notes:
            watch.append((row, role, notes))

    lines = [
        "# Trade Goods Value Audit",
        "",
        "This report groups trade goods by economy role so prices, abundance, production, consumption, caravan flow, and center liquidity can be balanced together.",
        "",
        "## Summary",
        "",
        f"- Trade goods audited: {len(rows)}",
        "- Role counts: " + ", ".join(f"{role} {count}" for role, count in sorted(counts.items())),
        f"- Watchlist rows: {len(watch)}",
        "",
        "## Role Bands",
        "",
        "| Role | Value band | Abundance band | Design use |",
        "|---|---:|---:|---|",
    ]
    for role, (value_min, value_max, abundance_min, abundance_max, summary) in ROLE_BANDS.items():
        lines.append(f"| `{role}` | {value_min}-{value_max} | {abundance_min}-{abundance_max} | {summary} |")

    lines += [
        "",
        "## Trade Goods",
        "",
        "| Item | Name | Role | Value | Abundance | Weight | Stack | Food quality | Merchandise | Notes |",
        "|---|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in sorted(rows, key=lambda row: (role_for(row), int(row["value"]), str(row["id"]))):
        stats = int(row["stats"])
        role = role_for(row)
        notes = notes_for(row, role)
        flags = int(row["flags"])
        stack = get_max_ammo(stats) if flags & itp_consumable else 0
        quality = food_quality(stats) if flags & itp_food else 0
        lines.append(
            f"| `{md(row['id'])}` | {md(row['name'])} | `{role}` | {row['value']} | {get_abundance(stats)} | "
            f"{get_weight(stats)} | {stack} | {quality} | {row['merchandise']} | {', '.join(notes) if notes else '-'} |"
        )

    lines += [
        "",
        "## Watchlist",
        "",
        "| Item | Role | Value | Abundance | Notes |",
        "|---|---|---:|---:|---|",
    ]
    for row, role, notes in sorted(watch, key=lambda item: (item[1], str(item[0]["id"]))):
        lines.append(f"| `{md(row['id'])}` | `{role}` | {row['value']} | {get_abundance(int(row['stats']))} | {', '.join(notes)} |")

    lines += [
        "",
        "## Balance Rules",
        "",
        "- Cheap staple goods should move often and stabilize food stores.",
        "- Preserved food should be more valuable than staples because it travels and stores better.",
        "- Raw materials should create steady production and liquidity routes.",
        "- Strategic materials should be valuable enough to matter for military and construction logistics.",
        "- Luxuries should move less often but produce stronger wealth swings in safe, liquid markets.",
        "- Scarcity raises demand; unsafe roads and low liquidity reduce caravan willingness to answer that demand.",
    ]

    write(OUT, lines)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
