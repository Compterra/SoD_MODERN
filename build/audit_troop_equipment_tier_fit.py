from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))

from audit_item_systems import all_item_rows, compact, md  # type: ignore
from audit_non_hero_troops import build_rows  # type: ignore
import module_troops  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "troop_equipment_tier_fit_audit.md"

TIER_KIT_BANDS = {
    1: (60, 250),
    2: (120, 360),
    3: (200, 470),
    4: (290, 570),
    5: (380, 690),
    6: (460, 760),
}

ROLE_NOTES = {
    "Archer": "ranged kit matters more than shield/mount",
    "Crossbow": "ranged kit matters more than shield/mount",
    "Skirmisher": "ranged and melee both matter",
    "Mounted ranged": "mount, ranged kit, and backup melee all matter",
    "Cavalry": "mount and melee kit drive tier pressure",
    "Infantry": "melee, armor, and shield drive tier pressure",
}

NONCOMBAT_SPEED_PATTERNS = [
    re.compile(r"_messenger$"),
    re.compile(r"^fugitive2?$"),
    re.compile(r"^spy$"),
    re.compile(r"_rep_1$"),
]

SPECIAL_FIT_TIER_FLOORS = {
    "ashkolon_knight": 4,
    "black_army_fresh_blade": 2,
    "boar_clan_warrior": 3,
    "conquistador_seasoned_crossbowman": 3,
    "ief_deserter": 2,
    "ief_velites": 2,
    "jotnar_clan_shield_maiden": 3,
    "sea_raider": 3,
    "sod_zer_1_noble": 3,
    "sod_zer_2_noble": 4,
}


def item_index() -> dict[int, dict[str, object]]:
    return {int(row["index"]): row for row in all_item_rows()}


def troop_inventory_by_id() -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for troop in module_troops.troops:
        troop_id = troop[0]
        inventory = troop[7]
        result[troop_id] = [entry for entry in inventory if isinstance(entry, int)]
    return result


def equipment_scores(inventory: list[int], items: dict[int, dict[str, object]]) -> dict[str, object]:
    entries = [items[item_id] for item_id in inventory if item_id in items]
    best_melee = max([int(e["score"]) for e in entries if e["type"] in {"1H", "2H", "Polearm"}] or [0])
    best_ranged_weapon = max([int(e["score"]) for e in entries if e["type"] in {"Bow", "Crossbow", "Thrown"}] or [0])
    best_ammo = max([int(e["score"]) for e in entries if e["type"] in {"Arrows", "Bolts", "Bullets"}] or [0])
    best_ranged = best_ranged_weapon + best_ammo
    armor = sum(sorted([int(e["score"]) for e in entries if e["type"] in {"Head", "Body", "Foot", "Hands"}], reverse=True)[:4])
    shield = max([int(e["score"]) for e in entries if e["type"] == "Shield"] or [0])
    mount = max([int(e["score"]) for e in entries if e["type"] == "Horse"] or [0])
    kit = best_melee + best_ranged + armor + shield + mount
    top_entries = sorted(entries, key=lambda row: int(row["score"]), reverse=True)[:6]
    item_names = [str(e["id"]) for e in top_entries]
    item_details = [
        {
            "id": str(e["id"]),
            "type": str(e["type"]),
            "score": int(e["score"]),
            "value": int(e["value"]),
            "merchandise": bool(e["merchandise"]),
            "troop_uses": int(e["troop_uses"]),
        }
        for e in top_entries
    ]
    return {
        "melee": best_melee,
        "ranged": best_ranged,
        "armor": armor,
        "shield": shield,
        "mount": mount,
        "kit": kit,
        "top_items": item_names,
        "top_item_details": item_details,
    }


def tier_band(tier: int, level: int, role: str, expects_shield: bool, troop_id: str = "") -> tuple[int, int, str]:
    normalized_tier = fit_tier(tier, level, troop_id)
    low, high = TIER_KIT_BANDS[normalized_tier]
    if level >= 35:
        high += 80
    elif level >= 28:
        high += 45
    if role in {"Cavalry", "Mounted ranged"}:
        low += 40
        high += 70
    elif role == "Archer":
        low -= 50
        high += 35
    elif role in {"Crossbow", "Skirmisher"}:
        low -= 20
        high += 35
    elif role == "Infantry" and not expects_shield:
        low -= 70
        high -= 50
    return max(0, low), high, f"{low}-{high}"


def is_speed_noncombat(troop_id: str) -> bool:
    return any(pattern.search(troop_id) for pattern in NONCOMBAT_SPEED_PATTERNS)


def level_tier(level: int) -> int:
    if level >= 35:
        return 6
    if level >= 30:
        return 5
    if level >= 25:
        return 4
    if level >= 20:
        return 3
    if level >= 12:
        return 2
    return 1


def fit_tier(tier: int, level: int, troop_id: str = "") -> int:
    special_floor = SPECIAL_FIT_TIER_FLOORS.get(troop_id, 1)
    return min(max(tier, level_tier(level), special_floor, 1), 6)


def fit_status(kit: int, low: int, high: int, ignored: bool = False) -> tuple[str, int]:
    if ignored:
        return "map-speed unit", 0
    if kit < low:
        return "under-equipped", low - kit
    if kit > high:
        return "over-equipped", kit - high
    return "fits", 0


def weakness_notes(row: dict[str, object]) -> list[str]:
    role = str(row["role"])
    notes: list[str] = []
    if int(row["melee"]) < 70 and role in {"Infantry", "Cavalry", "Mounted ranged", "Skirmisher"}:
        notes.append("melee low")
    if int(row["ranged"]) < 55 and role in {"Archer", "Crossbow", "Mounted ranged", "Skirmisher"}:
        notes.append("ranged low")
    if int(row["armor"]) < 170 and role in {"Infantry", "Cavalry", "Mounted ranged"}:
        notes.append("armor low")
    if bool(row["expects_shield"]) and int(row["shield"]) == 0:
        notes.append("shield guaranteed but absent")
    elif bool(row["expects_shield"]) and int(row["shield"]) < 70 and role in {"Infantry", "Cavalry"}:
        notes.append("shield low")
    if int(row["mount"]) < 90 and role in {"Cavalry", "Mounted ranged"}:
        notes.append("mount low")
    return notes


def build_fit_rows() -> list[dict[str, object]]:
    troop_rows, _excluded = build_rows()
    items = item_index()
    inventories = troop_inventory_by_id()
    rows: list[dict[str, object]] = []
    for troop in troop_rows:
        troop_id = str(troop["id"])
        scores = equipment_scores(inventories.get(troop_id, []), items)
        speed_noncombat = is_speed_noncombat(troop_id)
        notes: list[str] = []
        expects_shield = "g_shield" in troop["flag_tags"]
        low, high, band = tier_band(int(troop["tier"]), int(troop["level"]), str(troop["role"]), expects_shield, troop_id)
        status, gap = fit_status(int(scores["kit"]), low, high, speed_noncombat)
        if status not in {"fits", "map-speed unit"}:
            notes.append(status)
        if expects_shield and int(scores["shield"]) == 0:
            notes.append("shield guarantee has no shield item; do not solve with item stats")
        if speed_noncombat:
            notes.append("noncombat/support: judge by mission or world-map role")
        if troop_id in SPECIAL_FIT_TIER_FLOORS:
            notes.append(f"audit fit-tier floor {SPECIAL_FIT_TIER_FLOORS[troop_id]} for standalone/special role")
        if bool(troop["equipment_variant"]):
            notes.append("equipment-upgraded * variant")
        if str(troop["role"]) in ROLE_NOTES:
            notes.append(ROLE_NOTES[str(troop["role"])])
        if int(scores["mount"]) and str(troop["role"]) not in {"Cavalry", "Mounted ranged"}:
            notes.append("mount on non-mounted role")
        rows.append(
            {
                "faction": troop["faction_id"],
                "troop": troop_id,
                "name": troop["name"],
                "tier": troop["tier"],
                "fit_tier": fit_tier(int(troop["tier"]), int(troop["level"]), troop_id),
                "level": troop["level"],
                "role": troop["role"],
                "expects_shield": expects_shield,
                "band": band,
                "status": status,
                "gap": gap,
                "notes": notes,
                **scores,
            }
        )
        if status == "under-equipped":
            rows[-1]["weaknesses"] = weakness_notes(rows[-1])
        else:
            rows[-1]["weaknesses"] = []
    return rows


def write_report(rows: list[dict[str, object]]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    by_faction: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_faction[str(row["faction"])].append(row)

    flagged = [row for row in rows if row["status"] not in {"fits", "map-speed unit"}]
    ignored = [row for row in rows if row["status"] == "map-speed unit"]
    lines = [
        "# Troop Equipment Tier Fit Audit",
        "",
        "This report checks whether fixed thematic troop inventories are broadly appropriate for each troop's upgrade-tree tier. It is for balance triage only; it does not suggest changing troop inventories.",
        "",
        "## Summary",
        "",
        f"- Non-hero troops audited: {len(rows)}",
        f"- Factions represented: {len(by_faction)}",
        f"- Rows outside tier kit band: {len(flagged)}",
        f"- Over-equipped rows: {sum(1 for row in flagged if row['status'] == 'over-equipped')}",
        f"- Under-equipped rows: {sum(1 for row in flagged if row['status'] == 'under-equipped')}",
        f"- Map-speed/noncombat rows ignored by kit fit: {len(ignored)}",
        "",
        "## Reading Notes",
        "",
        "- `Tier` comes from upgrade-tree depth in the non-hero troop audit.",
        "- `Fit tier` is the higher of upgrade-tree tier and a broad level-derived tier, so standalone elite troops are not compared against recruits.",
        "- `Kit` is the sum of best melee, best ranged, armor, shield, and mount scores from the item audits.",
        "- Bands are intentionally broad because faction doctrine and thematic gear should survive the audit.",
        "- A flag means the item values may need adjustment, the troop may be an intentional elite/outlier, or the troop's tier classification may need a note.",
        "- Messengers are treated as map-speed units; their combat kit is not judged as long as their world role is courier movement.",
        "",
        "## Faction Summary",
        "",
        "| Faction | Troops | Avg kit | Over | Under | Map-speed | Biggest gap |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for faction, subset in sorted(by_faction.items()):
        over = sum(1 for row in subset if row["status"] == "over-equipped")
        under = sum(1 for row in subset if row["status"] == "under-equipped")
        speed = sum(1 for row in subset if row["status"] == "map-speed unit")
        biggest = max([int(row["gap"]) for row in subset] or [0])
        avg = sum(int(row["kit"]) for row in subset) / len(subset)
        lines.append(f"| {md(faction)} | {len(subset)} | {avg:.1f} | {over} | {under} | {speed} | {biggest} |")

    lines += [
        "",
        "## Gear Weakness Breakdown",
        "",
        "| Weakness | Rows | Examples |",
        "|---|---:|---|",
    ]
    weakness_counts: Counter[str] = Counter()
    weakness_examples: dict[str, list[str]] = defaultdict(list)
    for row in flagged:
        for weakness in row["weaknesses"]:
            weakness_counts[str(weakness)] += 1
            if len(weakness_examples[str(weakness)]) < 8:
                weakness_examples[str(weakness)].append(str(row["troop"]))
    for weakness, count in weakness_counts.most_common():
        lines.append(f"| {md(weakness)} | {count} | {compact([f'`{example}`' for example in weakness_examples[weakness]])} |")
    lines += [
        "",
        "## Flagged Item Detail",
        "",
        "Use this section before changing stats. Prefer items with low troop-use counts or clear faction ownership; shared common items should be changed only if the wider audit supports it.",
        "",
        "| Troop | Item | Type | Score | Value | Buyable | Troop uses |",
        "|---|---|---|---:|---:|---|---:|",
    ]
    for row in sorted(flagged, key=lambda item: int(item["gap"]), reverse=True)[:30]:
        for item in row["top_item_details"]:
            lines.append(
                f"| `{md(row['troop'])}` | `{md(item['id'])}` | {md(item['type'])} | {item['score']} | "
                f"{item['value']} | {item['merchandise']} | {item['troop_uses']} |"
            )
    lines += [
        "",
        "## Highest Priority Flags",
        "",
        "| Faction | Troop | Tree tier | Fit tier | Lvl | Role | Kit | Band | Status | Gap | Weaknesses | Top items | Notes |",
        "|---|---|---:|---:|---:|---|---:|---|---|---:|---|---|---|",
    ]
    for row in sorted(flagged, key=lambda item: int(item["gap"]), reverse=True)[:120]:
        lines.append(
            f"| {md(row['faction'])} | `{md(row['troop'])}` | {row['tier']} | {row['fit_tier']} | {row['level']} | {md(row['role'])} | "
            f"{row['kit']} | {row['band']} | {row['status']} | {row['gap']} | {compact(row['weaknesses'])} | {compact(row['top_items'])} | {compact(row['notes'])} |"
        )

    lines += ["", "## Full Faction Tables", ""]
    for faction, subset in sorted(by_faction.items()):
        lines += [
            f"### {md(faction)}",
            "",
            "| Troop | Tree tier | Fit tier | Lvl | Role | Melee | Ranged | Armor | Shield | Mount | Kit | Band | Status | Weaknesses | Notes |",
            "|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|---|",
        ]
        for row in sorted(subset, key=lambda item: (int(item["tier"]), int(item["level"]), str(item["troop"]))):
            lines.append(
                f"| `{md(row['troop'])}` | {row['tier']} | {row['fit_tier']} | {row['level']} | {md(row['role'])} | {row['melee']} | {row['ranged']} | "
                f"{row['armor']} | {row['shield']} | {row['mount']} | {row['kit']} | {row['band']} | {row['status']} | {compact(row['weaknesses'])} | {compact(row['notes'])} |"
            )
        lines.append("")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_fit_rows()
    write_report(rows)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} troops).")


if __name__ == "__main__":
    main()
