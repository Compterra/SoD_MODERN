from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import statistics
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))

from header_items import (  # type: ignore
    blunt,
    cut,
    get_difficulty,
    get_leg_armor,
    get_max_ammo,
    get_missile_speed,
    get_speed_rating,
    get_thrust_damage,
    get_weight,
    itp_merchandise,
    itp_cant_reload_on_horseback,
    itp_cant_use_on_horseback,
    itp_type_arrows,
    itp_type_bolts,
    itp_type_bow,
    itp_type_crossbow,
    itp_type_thrown,
    iwf_damage_type_bits,
    pierce,
)
from header_troops import tf_hero  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "ranged_weapon_audit.md"

RANGED_TYPES = {
    itp_type_bow: "Bow",
    itp_type_crossbow: "Crossbow",
    itp_type_thrown: "Thrown",
    itp_type_arrows: "Arrows",
    itp_type_bolts: "Bolts",
}

IMOD_NAMES = {
    "imodbits_none": 0,
    "imodbits_bow": getattr(module_items, "imodbits_bow", None),
    "imodbits_crossbow": getattr(module_items, "imodbits_crossbow", None),
    "imodbits_missile": getattr(module_items, "imodbits_missile", None),
    "imodbits_thrown": getattr(module_items, "imodbits_thrown", None),
}

DAMAGE_TYPE_NAMES = {
    cut: "cut",
    pierce: "pierce",
    blunt: "blunt",
}


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact(values: list[str], empty: str = "-") -> str:
    return ", ".join(values) if values else empty


def imod_label(bits: int) -> str:
    matches = [name.replace("imodbits_", "") for name, value in IMOD_NAMES.items() if value == bits]
    return matches[0] if matches else str(bits)


def damage_amount(raw: int) -> int:
    return raw & 0xFF


def damage_type(raw: int) -> int:
    return (raw >> iwf_damage_type_bits) & 0x03


def damage_label(raw: int) -> str:
    dtype = DAMAGE_TYPE_NAMES.get(damage_type(raw), str(damage_type(raw)))
    return f"{damage_amount(raw)}{dtype[0]}"


def effective_damage(raw: int) -> float:
    amount = float(damage_amount(raw))
    dtype = damage_type(raw)
    if dtype == pierce:
        amount *= 1.5
    elif dtype == blunt:
        amount *= 1.25
    return amount


def item_usage() -> dict[int, Counter[str]]:
    usage: dict[int, Counter[str]] = defaultdict(Counter)
    for troop in module_troops.troops:
        troop_id, name, plural, flags, scene, reserved, faction_id, inventory = troop[:8]
        kind = "hero" if flags & tf_hero else "troop"
        for item_id in inventory:
            if isinstance(item_id, int):
                usage[item_id][kind] += 1
    return usage


def ranged_flags(flags: int) -> list[str]:
    tags: list[str] = []
    if flags & itp_cant_reload_on_horseback:
        tags.append("no reload horseback")
    if flags & itp_cant_use_on_horseback:
        tags.append("no horseback")
    return tags


def ranged_score(row: dict[str, object]) -> int:
    item_type = str(row["type"])
    if item_type in {"Arrows", "Bolts"}:
        return int(row["damage"]) + int(row["ammo"]) // 2
    damage = float(row["effective_damage"])
    accuracy = max(int(row["accuracy"]), 100)
    return int(round(damage * max(int(row["speed"]), 1) * accuracy / 10000 + int(row["missile_speed"]) / 4 + int(row["ammo"]) / 2))


def ranged_band(score: int) -> str:
    if score >= 95:
        return "endgame"
    if score >= 70:
        return "elite"
    if score >= 45:
        return "veteran"
    if score >= 25:
        return "regular"
    if score > 0:
        return "low"
    return "zero"


def buyable_ranged_tier(row: dict[str, object]) -> str:
    score = int(row["score"])
    ranged_type = str(row["type"])
    thresholds = {
        "Bow": (25, 40, 55),
        "Crossbow": (28, 45, 65),
        "Thrown": (25, 40, 55),
        "Arrows": (16, 22, 28),
        "Bolts": (16, 22, 28),
    }.get(ranged_type, (25, 40, 55))
    if score >= thresholds[2]:
        return "Tier 4 - Elite"
    if score >= thresholds[1]:
        return "Tier 3 - Veteran"
    if score >= thresholds[0]:
        return "Tier 2 - Regular"
    return "Tier 1 - Light"


def build_rows() -> list[dict[str, object]]:
    usage = item_usage()
    rows: list[dict[str, object]] = []
    for item_id, item in enumerate(module_items.items):
        item_key, item_name, meshes, flags, capabilities, value, stats, imodbits = item[:8]
        item_type_id = flags & 0xFF
        if item_type_id not in RANGED_TYPES:
            continue
        raw_damage = get_thrust_damage(stats)
        accuracy = get_leg_armor(stats)
        if accuracy == 0:
            accuracy = 100
        row = {
            "index": item_id,
            "id": item_key,
            "name": item_name,
            "type": RANGED_TYPES[item_type_id],
            "buyable": bool(flags & itp_merchandise),
            "value": value,
            "weight": get_weight(stats),
            "difficulty": get_difficulty(stats),
            "damage": damage_amount(raw_damage),
            "damage_type": DAMAGE_TYPE_NAMES.get(damage_type(raw_damage), str(damage_type(raw_damage))),
            "damage_profile": damage_label(raw_damage),
            "effective_damage": round(effective_damage(raw_damage), 1),
            "speed": get_speed_rating(stats),
            "missile_speed": get_missile_speed(stats),
            "accuracy": accuracy,
            "ammo": get_max_ammo(stats),
            "flags": ranged_flags(flags),
            "imod": imod_label(imodbits),
            "troop_uses": usage[item_id]["troop"],
            "hero_uses": usage[item_id]["hero"],
            "warnings": [],
        }
        score = ranged_score(row)
        row["score"] = score
        row["band"] = ranged_band(score)
        row["buyable_tier"] = buyable_ranged_tier(row)
        warnings: list[str] = row["warnings"]  # type: ignore[assignment]
        if int(row["damage"]) <= 0 and row["type"] not in {"Arrows", "Bolts"}:
            warnings.append("zero weapon damage")
        if int(row["speed"]) <= 0 and row["type"] not in {"Arrows", "Bolts"}:
            warnings.append("zero speed")
        if int(row["ammo"]) <= 0 and row["type"] in {"Thrown", "Arrows", "Bolts"}:
            warnings.append("zero ammo")
        if value <= 0 and score > 0:
            warnings.append("positive ranged item with zero value")
        if value > 0 and score > 0:
            value_per_score = value / score
            row["value_per_score"] = round(value_per_score, 1)
            if value_per_score > 90:
                warnings.append("expensive for performance")
            elif value_per_score < 3 and score >= 35:
                warnings.append("cheap for performance")
        else:
            row["value_per_score"] = 0
        if row["type"] == "Crossbow" and "no reload horseback" not in row["flags"]:
            warnings.append("crossbow reloads on horseback")
        rows.append(row)
    return rows


def append_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    scores = [int(row["score"]) for row in rows]
    type_counts = Counter(str(row["type"]) for row in rows)
    bands = Counter(str(row["band"]) for row in rows)
    damage_types = Counter(str(row["damage_type"]) for row in rows if str(row["type"]) not in {"Arrows", "Bolts"})
    lines.append("## Global Summary")
    lines.append("")
    lines.append(f"- Ranged items audited: {len(rows)}")
    lines.append(f"- Buyable ranged items: {sum(1 for row in rows if row['buyable'])}; non-buyable ranged items: {sum(1 for row in rows if not row['buyable'])}")
    lines.append("- Type counts: " + compact([f"{name} {count}" for name, count in type_counts.most_common()]))
    lines.append("- Bands: " + compact([f"{band} {count}" for band, count in bands.most_common()]))
    lines.append("- Weapon damage types: " + compact([f"{name} {count}" for name, count in damage_types.most_common()]))
    lines.append(f"- Score range: {min(scores)}-{max(scores)}")
    lines.append(f"- Warning rows: {sum(1 for row in rows if row['warnings'])}")
    lines.append("")


def append_type_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_type[str(row["type"])].append(row)
    lines.append("## Summary by Ranged Type")
    lines.append("")
    lines.append("| Type | Count | Score range | Avg score | Avg damage | Avg speed | Avg ammo | Warning rows |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for ranged_type in ["Bow", "Crossbow", "Thrown", "Arrows", "Bolts"]:
        subset = by_type.get(ranged_type, [])
        if not subset:
            continue
        scores = [int(row["score"]) for row in subset]
        damage = [float(row["effective_damage"]) for row in subset]
        speeds = [int(row["speed"]) for row in subset]
        ammo = [int(row["ammo"]) for row in subset]
        lines.append(
            f"| {ranged_type} | {len(subset)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(damage):.1f} | {statistics.mean(speeds):.1f} | {statistics.mean(ammo):.1f} | {sum(1 for row in subset if row['warnings'])} |"
        )
    lines.append("")


def append_buyable_tiers(lines: list[str], rows: list[dict[str, object]]) -> None:
    buyable = [row for row in rows if row["buyable"]]
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in buyable:
        by_type[str(row["type"])].append(row)
    lines.append("## Buyable Ranged Tiers")
    lines.append("")
    lines.append("Only buyable ranged items are tiered here. Bows, crossbows, thrown weapons, arrows, and bolts use separate thresholds because ammo stacks score differently from weapons.")
    lines.append("")
    lines.append("Tier thresholds: Bow/Thrown `1-24`, `25-39`, `40-54`, `55+`; Crossbow `1-27`, `28-44`, `45-64`, `65+`; Arrows/Bolts `1-15`, `16-21`, `22-27`, `28+`.")
    lines.append("")
    for ranged_type in ["Bow", "Crossbow", "Thrown", "Arrows", "Bolts"]:
        subset = by_type.get(ranged_type, [])
        if not subset:
            continue
        tier_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in subset:
            tier_groups[str(row["buyable_tier"])].append(row)
        lines.append(f"### {ranged_type}")
        lines.append("")
        lines.append("| Tier | Count | Score range | Avg score | Avg value | Example items |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for tier in ["Tier 1 - Light", "Tier 2 - Regular", "Tier 3 - Veteran", "Tier 4 - Elite"]:
            tier_rows = tier_groups.get(tier, [])
            if not tier_rows:
                continue
            scores = [int(row["score"]) for row in tier_rows]
            values = [int(row["value"]) for row in tier_rows]
            examples = [f"`{row['id']}`" for row in sorted(tier_rows, key=lambda item: (int(item["score"]), int(item["value"])), reverse=True)[:6]]
            lines.append(f"| {tier} | {len(tier_rows)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(values):.0f} | {compact(examples)} |")
        lines.append("")
        for tier in ["Tier 1 - Light", "Tier 2 - Regular", "Tier 3 - Veteran", "Tier 4 - Elite"]:
            tier_rows = sorted(tier_groups.get(tier, []), key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])), reverse=True)
            if not tier_rows:
                continue
            lines.append(f"#### {ranged_type} - {tier}")
            lines.append("")
            lines.append("| Item | Score | Damage | Speed | Missile speed | Accuracy | Ammo | Difficulty | Value | Value/score | Uses | Warnings |")
            lines.append("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
            for row in tier_rows:
                uses = int(row["troop_uses"]) + int(row["hero_uses"])
                lines.append(
                    "| {id} | {score} | {damage} | {speed} | {missile_speed} | {accuracy} | {ammo} | {difficulty} | {value} | {vps} | {uses} | {warnings} |".format(
                        id=md_escape(row["id"]),
                        score=row["score"],
                        damage=md_escape(row["damage_profile"]),
                        speed=row["speed"],
                        missile_speed=row["missile_speed"],
                        accuracy=row["accuracy"],
                        ammo=row["ammo"],
                        difficulty=row["difficulty"],
                        value=row["value"],
                        vps=row["value_per_score"],
                        uses=uses,
                        warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
                    )
                )
            lines.append("")


def append_watchlists(lines: list[str], rows: list[dict[str, object]]) -> None:
    top_rows = sorted(rows, key=lambda row: (int(row["score"]), int(row["value"])), reverse=True)[:45]
    warning_rows = [row for row in rows if row["warnings"]]
    lines.append("## Top Ranged Pressure")
    lines.append("")
    lines.append("| Item | Type | Score | Band | Damage | Speed | Missile speed | Accuracy | Ammo | Difficulty | Value | Flags | Uses | Warnings |")
    lines.append("|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for row in top_rows:
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {type} | {score} | {band} | {damage} | {speed} | {missile_speed} | {accuracy} | {ammo} | {difficulty} | {value} | {flags} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                type=md_escape(row["type"]),
                score=row["score"],
                band=md_escape(row["band"]),
                damage=md_escape(row["damage_profile"]),
                speed=row["speed"],
                missile_speed=row["missile_speed"],
                accuracy=row["accuracy"],
                ammo=row["ammo"],
                difficulty=row["difficulty"],
                value=row["value"],
                flags=md_escape(compact(row["flags"])),  # type: ignore[arg-type]
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")
    lines.append("## Ranged Watchlist")
    lines.append("")
    if not warning_rows:
        lines.append("No structural ranged warnings found.")
        lines.append("")
        return
    lines.append("| Item | Type | Score | Damage | Speed | Ammo | Value | Uses | Warnings |")
    lines.append("|---|---|---:|---|---:|---:|---:|---:|---|")
    for row in sorted(warning_rows, key=lambda item: (str(item["type"]), str(item["id"]))):
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {type} | {score} | {damage} | {speed} | {ammo} | {value} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                type=md_escape(row["type"]),
                score=row["score"],
                damage=md_escape(row["damage_profile"]),
                speed=row["speed"],
                ammo=row["ammo"],
                value=row["value"],
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")


def append_full_tables(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Full Ranged Tables")
    lines.append("")
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_type[str(row["type"])].append(row)
    for ranged_type in ["Bow", "Crossbow", "Thrown", "Arrows", "Bolts"]:
        subset = sorted(by_type.get(ranged_type, []), key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])))
        if not subset:
            continue
        lines.append(f"### {ranged_type}")
        lines.append("")
        lines.append("| Item ID | Name | Score | Band | Damage | Speed | Missile speed | Accuracy | Ammo | Weight | Difficulty | Value | Value/score | Imods | Flags | Troop uses | Hero uses |")
        lines.append("|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|")
        for row in subset:
            lines.append(
                "| {id} | {name} | {score} | {band} | {damage} | {speed} | {missile_speed} | {accuracy} | {ammo} | {weight} | {difficulty} | {value} | {vps} | {imod} | {flags} | {troop_uses} | {hero_uses} |".format(
                    id=md_escape(row["id"]),
                    name=md_escape(row["name"]),
                    score=row["score"],
                    band=md_escape(row["band"]),
                    damage=md_escape(row["damage_profile"]),
                    speed=row["speed"],
                    missile_speed=row["missile_speed"],
                    accuracy=row["accuracy"],
                    ammo=row["ammo"],
                    weight=row["weight"],
                    difficulty=row["difficulty"],
                    value=row["value"],
                    vps=row["value_per_score"],
                    imod=md_escape(row["imod"]),
                    flags=md_escape(compact(row["flags"])),  # type: ignore[arg-type]
                    troop_uses=row["troop_uses"],
                    hero_uses=row["hero_uses"],
                )
            )
        lines.append("")


def write_report(rows: list[dict[str, object]]) -> None:
    lines: list[str] = []
    lines.append("# Ranged Weapon Audit")
    lines.append("")
    lines.append("Generated from `compile/module_items.py` and troop inventories. Scores estimate ranged pressure from effective damage, speed, missile speed, accuracy, ammo, and item type.")
    lines.append("")
    append_summary(lines, rows)
    append_type_summary(lines, rows)
    append_buyable_tiers(lines, rows)
    append_watchlists(lines, rows)
    append_full_tables(lines, rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_report(rows)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} ranged items).")


if __name__ == "__main__":
    main()
