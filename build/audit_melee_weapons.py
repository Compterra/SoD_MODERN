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
    get_speed_rating,
    get_swing_damage,
    get_thrust_damage,
    get_weapon_length,
    get_weight,
    itp_bonus_against_shield,
    itp_cant_use_on_horseback,
    itp_merchandise,
    itp_penalty_with_shield,
    itp_two_handed,
    itp_type_one_handed_wpn,
    itp_type_polearm,
    itp_type_two_handed_wpn,
    iwf_damage_type_bits,
    pierce,
)
from header_troops import tf_hero  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "melee_weapon_audit.md"

WEAPON_TYPES = {
    itp_type_one_handed_wpn: "One-handed",
    itp_type_two_handed_wpn: "Two-handed",
    itp_type_polearm: "Polearm",
}

IMOD_NAMES = {
    "imodbits_none": 0,
    "imodbits_sword": getattr(module_items, "imodbits_sword", None),
    "imodbits_sword_high": getattr(module_items, "imodbits_sword_high", None),
    "imodbits_axe": getattr(module_items, "imodbits_axe", None),
    "imodbits_mace": getattr(module_items, "imodbits_mace", None),
    "imodbits_pick": getattr(module_items, "imodbits_pick", None),
    "imodbits_polearm": getattr(module_items, "imodbits_polearm", None),
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
    amount = damage_amount(raw)
    dtype = DAMAGE_TYPE_NAMES.get(damage_type(raw), str(damage_type(raw)))
    return f"{amount}{dtype[0]}"


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


def weapon_flags(flags: int) -> list[str]:
    tags: list[str] = []
    if flags & itp_two_handed:
        tags.append("two-handed")
    if flags & itp_bonus_against_shield:
        tags.append("shield bonus")
    if flags & itp_penalty_with_shield:
        tags.append("shield penalty")
    if flags & itp_cant_use_on_horseback:
        tags.append("no horseback")
    return tags


def weapon_score(row: dict[str, object]) -> int:
    best_damage = max(float(row["swing_effective"]), float(row["thrust_effective"]))
    return int(round(best_damage * max(int(row["speed"]), 1) / 100 + int(row["length"]) / 10))


def weapon_band(score: int) -> str:
    if score >= 80:
        return "endgame"
    if score >= 60:
        return "elite"
    if score >= 42:
        return "veteran"
    if score >= 25:
        return "regular"
    if score > 0:
        return "low"
    return "zero"


def buyable_weapon_tier(row: dict[str, object]) -> str:
    score = int(row["score"])
    weapon_type = str(row["type"])
    thresholds = {
        "One-handed": (35, 50, 65),
        "Two-handed": (42, 58, 72),
        "Polearm": (42, 58, 72),
    }.get(weapon_type, (35, 50, 65))
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
        item_type = flags & 0xFF
        if item_type not in WEAPON_TYPES:
            continue
        swing_raw = get_swing_damage(stats)
        thrust_raw = get_thrust_damage(stats)
        row = {
            "index": item_id,
            "id": item_key,
            "name": item_name,
            "type": WEAPON_TYPES[item_type],
            "buyable": bool(flags & itp_merchandise),
            "value": value,
            "weight": get_weight(stats),
            "difficulty": get_difficulty(stats),
            "speed": get_speed_rating(stats),
            "length": get_weapon_length(stats),
            "swing": damage_amount(swing_raw),
            "swing_type": DAMAGE_TYPE_NAMES.get(damage_type(swing_raw), str(damage_type(swing_raw))),
            "swing_effective": round(effective_damage(swing_raw), 1),
            "thrust": damage_amount(thrust_raw),
            "thrust_type": DAMAGE_TYPE_NAMES.get(damage_type(thrust_raw), str(damage_type(thrust_raw))),
            "thrust_effective": round(effective_damage(thrust_raw), 1),
            "damage_profile": f"{damage_label(swing_raw)}/{damage_label(thrust_raw)}",
            "flags": weapon_flags(flags),
            "imod": imod_label(imodbits),
            "troop_uses": usage[item_id]["troop"],
            "hero_uses": usage[item_id]["hero"],
            "warnings": [],
        }
        score = weapon_score(row)
        row["score"] = score
        row["band"] = weapon_band(score)
        row["buyable_tier"] = buyable_weapon_tier(row)
        warnings: list[str] = row["warnings"]  # type: ignore[assignment]
        if int(row["swing"]) <= 0 and int(row["thrust"]) <= 0:
            warnings.append("zero damage")
        if int(row["speed"]) <= 0:
            warnings.append("zero speed")
        if int(row["length"]) <= 0:
            warnings.append("zero length")
        if value <= 0 and score > 0:
            warnings.append("positive weapon with zero value")
        if value > 0 and score > 0:
            value_per_score = value / score
            row["value_per_score"] = round(value_per_score, 1)
            if value_per_score > 160:
                warnings.append("expensive for performance")
            elif value_per_score < 4 and score >= 35:
                warnings.append("cheap for performance")
        else:
            row["value_per_score"] = 0
        if row["type"] == "Polearm" and int(row["length"]) < 90:
            warnings.append("short polearm")
        if row["type"] != "Polearm" and int(row["length"]) > 160:
            warnings.append("very long non-polearm")
        rows.append(row)
    return rows


def append_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    scores = [int(row["score"]) for row in rows]
    speeds = [int(row["speed"]) for row in rows]
    lengths = [int(row["length"]) for row in rows]
    type_counts = Counter(str(row["type"]) for row in rows)
    bands = Counter(str(row["band"]) for row in rows)
    damage_types = Counter(
        str(row["swing_type"]) if int(row["swing"]) >= int(row["thrust"]) else str(row["thrust_type"])
        for row in rows
    )
    lines.append("## Global Summary")
    lines.append("")
    lines.append(f"- Melee weapons audited: {len(rows)}")
    lines.append(f"- Buyable melee weapons: {sum(1 for row in rows if row['buyable'])}; non-buyable melee weapons: {sum(1 for row in rows if not row['buyable'])}")
    lines.append("- Type counts: " + compact([f"{name} {count}" for name, count in type_counts.most_common()]))
    lines.append("- Bands: " + compact([f"{band} {count}" for band, count in bands.most_common()]))
    lines.append("- Dominant damage types: " + compact([f"{name} {count}" for name, count in damage_types.most_common()]))
    lines.append(f"- Score range: {min(scores)}-{max(scores)}; speed range: {min(speeds)}-{max(speeds)}; length range: {min(lengths)}-{max(lengths)}")
    lines.append(f"- Warning rows: {sum(1 for row in rows if row['warnings'])}")
    lines.append("")


def append_type_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_type[str(row["type"])].append(row)
    lines.append("## Summary by Weapon Type")
    lines.append("")
    lines.append("| Type | Count | Score range | Avg score | Avg speed | Avg length | Warning rows |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for weapon_type in ["One-handed", "Two-handed", "Polearm"]:
        subset = by_type.get(weapon_type, [])
        if not subset:
            continue
        scores = [int(row["score"]) for row in subset]
        speeds = [int(row["speed"]) for row in subset]
        lengths = [int(row["length"]) for row in subset]
        lines.append(
            f"| {weapon_type} | {len(subset)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(speeds):.1f} | {statistics.mean(lengths):.1f} | {sum(1 for row in subset if row['warnings'])} |"
        )
    lines.append("")


def append_buyable_tiers(lines: list[str], rows: list[dict[str, object]]) -> None:
    buyable = [row for row in rows if row["buyable"]]
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in buyable:
        by_type[str(row["type"])].append(row)
    lines.append("## Buyable Melee Tiers")
    lines.append("")
    lines.append("Only buyable melee weapons are tiered here. Thresholds are type-specific so one-handed weapons are not compared too directly against two-handed weapons and polearms.")
    lines.append("")
    lines.append("Tier thresholds: One-handed `1-34`, `35-49`, `50-64`, `65+`; Two-handed/Polearm `1-41`, `42-57`, `58-71`, `72+`.")
    lines.append("")
    for weapon_type in ["One-handed", "Two-handed", "Polearm"]:
        subset = by_type.get(weapon_type, [])
        if not subset:
            continue
        tier_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in subset:
            tier_groups[str(row["buyable_tier"])].append(row)
        lines.append(f"### {weapon_type}")
        lines.append("")
        lines.append("| Tier | Count | Score range | Avg score | Avg value | Example weapons |")
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
            lines.append(f"#### {weapon_type} - {tier}")
            lines.append("")
            lines.append("| Weapon | Score | Damage | Speed | Length | Weight | Difficulty | Value | Value/score | Uses | Warnings |")
            lines.append("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|")
            for row in tier_rows:
                uses = int(row["troop_uses"]) + int(row["hero_uses"])
                lines.append(
                    "| {id} | {score} | {damage} | {speed} | {length} | {weight} | {difficulty} | {value} | {vps} | {uses} | {warnings} |".format(
                        id=md_escape(row["id"]),
                        score=row["score"],
                        damage=md_escape(row["damage_profile"]),
                        speed=row["speed"],
                        length=row["length"],
                        weight=row["weight"],
                        difficulty=row["difficulty"],
                        value=row["value"],
                        vps=row["value_per_score"],
                        uses=uses,
                        warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
                    )
                )
            lines.append("")


def append_watchlists(lines: list[str], rows: list[dict[str, object]]) -> None:
    top_rows = sorted(rows, key=lambda row: (int(row["score"]), int(row["value"])), reverse=True)[:50]
    warning_rows = [row for row in rows if row["warnings"]]
    lines.append("## Top Melee Pressure")
    lines.append("")
    lines.append("| Weapon | Type | Score | Band | Dmg S/T | Speed | Length | Weight | Value | Flags | Uses | Warnings |")
    lines.append("|---|---|---:|---|---|---:|---:|---:|---:|---|---:|---|")
    for row in top_rows:
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {type} | {score} | {band} | {damage} | {speed} | {length} | {weight} | {value} | {flags} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                type=md_escape(row["type"]),
                score=row["score"],
                band=md_escape(row["band"]),
                damage=md_escape(row["damage_profile"]),
                speed=row["speed"],
                length=row["length"],
                weight=row["weight"],
                value=row["value"],
                flags=md_escape(compact(row["flags"])),  # type: ignore[arg-type]
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")
    lines.append("## Melee Watchlist")
    lines.append("")
    if not warning_rows:
        lines.append("No structural melee weapon warnings found.")
        lines.append("")
        return
    lines.append("| Weapon | Type | Score | Dmg S/T | Speed | Length | Value | Uses | Warnings |")
    lines.append("|---|---|---:|---|---:|---:|---:|---:|---|")
    for row in sorted(warning_rows, key=lambda item: (str(item["type"]), str(item["id"]))):
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {type} | {score} | {damage} | {speed} | {length} | {value} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                type=md_escape(row["type"]),
                score=row["score"],
                damage=md_escape(row["damage_profile"]),
                speed=row["speed"],
                length=row["length"],
                value=row["value"],
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")


def append_full_tables(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Full Melee Tables")
    lines.append("")
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_type[str(row["type"])].append(row)
    for weapon_type in ["One-handed", "Two-handed", "Polearm"]:
        subset = sorted(by_type.get(weapon_type, []), key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])))
        if not subset:
            continue
        lines.append(f"### {weapon_type}")
        lines.append("")
        lines.append("| Weapon ID | Name | Score | Band | Swing | Thrust | Speed | Length | Weight | Difficulty | Value | Value/score | Imods | Flags | Troop uses | Hero uses |")
        lines.append("|---|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|")
        for row in subset:
            lines.append(
                "| {id} | {name} | {score} | {band} | {swing}{swing_type} | {thrust}{thrust_type} | {speed} | {length} | {weight} | {difficulty} | {value} | {vps} | {imod} | {flags} | {troop_uses} | {hero_uses} |".format(
                    id=md_escape(row["id"]),
                    name=md_escape(row["name"]),
                    score=row["score"],
                    band=md_escape(row["band"]),
                    swing=row["swing"],
                    swing_type=str(row["swing_type"])[0],
                    thrust=row["thrust"],
                    thrust_type=str(row["thrust_type"])[0],
                    speed=row["speed"],
                    length=row["length"],
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
    lines.append("# Melee Weapon Audit")
    lines.append("")
    lines.append("Generated from `compile/module_items.py` and troop inventories. Scores estimate melee pressure from effective damage, damage type, speed, and reach; they are balance aids, not exact combat DPS.")
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
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} melee weapons).")


if __name__ == "__main__":
    main()
