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
    get_body_armor,
    get_difficulty,
    get_head_armor,
    get_leg_armor,
    get_weight,
    itp_merchandise,
    itp_type_body_armor,
    itp_type_foot_armor,
    itp_type_hand_armor,
    itp_type_head_armor,
)
from header_troops import tf_hero  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "armor_audit.md"

ARMOR_TYPES = {
    itp_type_head_armor: "Head",
    itp_type_body_armor: "Body",
    itp_type_foot_armor: "Foot",
    itp_type_hand_armor: "Hands",
}

IMOD_NAMES = {
    "imodbits_none": 0,
    "imodbits_cloth": getattr(module_items, "imodbits_cloth", None),
    "imodbits_armor": getattr(module_items, "imodbits_armor", None),
    "imodbits_plate": getattr(module_items, "imodbits_plate", None),
    "imodbits_good": getattr(module_items, "imodbits_good", None),
    "imodbits_bad": getattr(module_items, "imodbits_bad", None),
}


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact(values: list[str], empty: str = "-") -> str:
    return ", ".join(values) if values else empty


def imod_label(bits: int) -> str:
    matches = [name.replace("imodbits_", "") for name, value in IMOD_NAMES.items() if value == bits]
    return matches[0] if matches else str(bits)


def armor_score(row: dict[str, object]) -> int:
    armor_type = str(row["type"])
    if armor_type == "Body":
        return int(row["body"]) + int(row["leg"]) + int(row["head"]) // 2
    if armor_type == "Head":
        return int(row["head"])
    if armor_type == "Foot":
        return int(row["leg"])
    if armor_type == "Hands":
        return int(row["body"])
    return 0


def value_band(score: int) -> str:
    if score >= 80:
        return "endgame"
    if score >= 55:
        return "elite"
    if score >= 35:
        return "veteran"
    if score >= 18:
        return "regular"
    if score > 0:
        return "light"
    return "zero"


def buyable_armor_tier(row: dict[str, object]) -> str:
    score = int(row["score"])
    slot = str(row["type"])
    thresholds = {
        "Body": (25, 45, 65),
        "Head": (18, 32, 46),
        "Foot": (12, 22, 32),
        "Hands": (3, 5, 8),
    }.get(slot, (20, 40, 60))
    if score >= thresholds[2]:
        return "Tier 4 - Elite"
    if score >= thresholds[1]:
        return "Tier 3 - Heavy"
    if score >= thresholds[0]:
        return "Tier 2 - Regular"
    return "Tier 1 - Light"


def item_usage() -> dict[int, Counter[str]]:
    usage: dict[int, Counter[str]] = defaultdict(Counter)
    for troop in module_troops.troops:
        troop_id, name, plural, flags, scene, reserved, faction_id, inventory = troop[:8]
        kind = "hero" if flags & tf_hero else "troop"
        for item_id in inventory:
            if isinstance(item_id, int):
                usage[item_id][kind] += 1
    return usage


def build_rows() -> list[dict[str, object]]:
    usage = item_usage()
    rows: list[dict[str, object]] = []
    for item_id, item in enumerate(module_items.items):
        item_key, item_name, meshes, flags, capabilities, value, stats, imodbits = item[:8]
        item_type = flags & 0xFF
        if item_type not in ARMOR_TYPES:
            continue
        head = get_head_armor(stats)
        body = get_body_armor(stats)
        leg = get_leg_armor(stats)
        weight = get_weight(stats)
        difficulty = get_difficulty(stats)
        row = {
            "index": item_id,
            "id": item_key,
            "name": item_name,
            "type": ARMOR_TYPES[item_type],
            "buyable": bool(flags & itp_merchandise),
            "value": value,
            "weight": weight,
            "difficulty": difficulty,
            "head": head,
            "body": body,
            "leg": leg,
            "imod": imod_label(imodbits),
            "troop_uses": usage[item_id]["troop"],
            "hero_uses": usage[item_id]["hero"],
            "warnings": [],
        }
        score = armor_score(row)
        row["score"] = score
        row["band"] = value_band(score)
        row["buyable_tier"] = buyable_armor_tier(row)
        warnings: list[str] = row["warnings"]  # type: ignore[assignment]
        if score <= 0:
            warnings.append("zero armor")
        if value <= 0 and score > 0:
            warnings.append("positive armor with zero value")
        if row["type"] == "Body" and body <= 0:
            warnings.append("body armor item with no body armor")
        if row["type"] == "Head" and head <= 0:
            warnings.append("head armor item with no head armor")
        if row["type"] == "Foot" and leg <= 0:
            warnings.append("foot armor item with no leg armor")
        if weight <= 0 and score >= 25:
            warnings.append("substantial armor with zero weight")
        if value > 0 and score > 0:
            value_per_score = value / score
            row["value_per_score"] = round(value_per_score, 1)
            if value_per_score > 250:
                warnings.append("expensive for protection")
            elif value_per_score < 8 and score >= 25:
                warnings.append("cheap for protection")
        else:
            row["value_per_score"] = 0
        rows.append(row)
    return rows


def append_type_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Summary by Armor Slot")
    lines.append("")
    lines.append("Buyable armor is economy-facing and should be price-consistent. Non-buyable armor is troop-only, faction, blacksmith, reward, or special-purpose gear and should be balanced primarily by access.")
    lines.append("")
    for title, subset_rows in [
        ("Buyable Armor", [row for row in rows if row["buyable"]]),
        ("Non-Buyable / Troop-Only Armor", [row for row in rows if not row["buyable"]]),
    ]:
        lines.append(f"### {title}")
        lines.append("")
        if not subset_rows:
            lines.append("No armor in this group.")
            lines.append("")
            continue
        by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in subset_rows:
            by_type[str(row["type"])].append(row)
        lines.append("| Slot | Count | Score range | Avg score | Avg weight | Avg value | Warning rows |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for armor_type in ["Head", "Body", "Foot", "Hands"]:
            subset = by_type.get(armor_type, [])
            if not subset:
                continue
            scores = [int(row["score"]) for row in subset]
            weights = [float(row["weight"]) for row in subset]
            values = [int(row["value"]) for row in subset]
            warning_count = sum(1 for row in subset if row["warnings"])
            lines.append(
                f"| {armor_type} | {len(subset)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(weights):.1f} | {statistics.mean(values):.0f} | {warning_count} |"
            )
        lines.append("")


def append_watchlists(lines: list[str], rows: list[dict[str, object]]) -> None:
    top_rows = sorted(rows, key=lambda row: (int(row["score"]), int(row["value"])), reverse=True)[:40]
    warning_rows = [row for row in rows if row["warnings"]]
    lines.append("## Top Armor Pressure")
    lines.append("")
    lines.append("| Item | Slot | Score | H/B/L | Weight | Value | Imods | Uses | Warnings |")
    lines.append("|---|---|---:|---|---:|---:|---|---:|---|")
    for row in top_rows:
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {slot} | {score} | {h}/{b}/{l} | {weight} | {value} | {imod} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                slot=md_escape(row["type"]),
                score=row["score"],
                h=row["head"],
                b=row["body"],
                l=row["leg"],
                weight=row["weight"],
                value=row["value"],
                imod=md_escape(row["imod"]),
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")
    lines.append("## Armor Watchlist")
    lines.append("")
    if not warning_rows:
        lines.append("No structural armor warnings found.")
        lines.append("")
        return
    lines.append("| Item | Slot | Score | Weight | Value | Uses | Warnings |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for row in sorted(warning_rows, key=lambda item: (str(item["type"]), str(item["id"]))):
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            f"| {md_escape(row['id'])} | {md_escape(row['type'])} | {row['score']} | {row['weight']} | {row['value']} | {uses} | {md_escape(compact(row['warnings']))} |"  # type: ignore[arg-type]
        )
    lines.append("")


def append_buyability_pressure(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Armor by Buyability")
    lines.append("")
    for title, subset in [
        ("Buyable Armor Pressure", [row for row in rows if row["buyable"]]),
        ("Non-Buyable / Troop-Only Armor Pressure", [row for row in rows if not row["buyable"]]),
    ]:
        top_rows = sorted(subset, key=lambda row: (int(row["score"]), int(row["value"])), reverse=True)[:40]
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| Item | Slot | Score | Band | H/B/L | Weight | Value | Uses | Warnings |")
        lines.append("|---|---|---:|---|---|---:|---:|---:|---|")
        for row in top_rows:
            uses = int(row["troop_uses"]) + int(row["hero_uses"])
            lines.append(
                "| {id} | {slot} | {score} | {band} | {h}/{b}/{l} | {weight} | {value} | {uses} | {warnings} |".format(
                    id=md_escape(row["id"]),
                    slot=md_escape(row["type"]),
                    score=row["score"],
                    band=md_escape(row["band"]),
                    h=row["head"],
                    b=row["body"],
                    l=row["leg"],
                    weight=row["weight"],
                    value=row["value"],
                    uses=uses,
                    warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
                )
            )
        lines.append("")


def append_buyable_tiers(lines: list[str], rows: list[dict[str, object]]) -> None:
    buyable = [row for row in rows if row["buyable"]]
    by_slot: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in buyable:
        by_slot[str(row["type"])].append(row)
    lines.append("## Buyable Armor Tiers")
    lines.append("")
    lines.append("Only buyable armor is tiered here. Thresholds are slot-specific: body armor uses higher score bands than helmets, boots, and gloves.")
    lines.append("")
    lines.append("Tier thresholds: Body `1-24`, `25-44`, `45-64`, `65+`; Head `1-17`, `18-31`, `32-45`, `46+`; Foot `1-11`, `12-21`, `22-31`, `32+`; Hands `1-2`, `3-4`, `5-7`, `8+`.")
    lines.append("")
    for slot in ["Body", "Head", "Foot", "Hands"]:
        slot_rows = by_slot.get(slot, [])
        if not slot_rows:
            continue
        tier_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in slot_rows:
            tier_groups[str(row["buyable_tier"])].append(row)
        lines.append(f"### {slot}")
        lines.append("")
        lines.append("| Tier | Count | Score range | Avg score | Avg value | Example items |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for tier in ["Tier 1 - Light", "Tier 2 - Regular", "Tier 3 - Heavy", "Tier 4 - Elite"]:
            subset = tier_groups.get(tier, [])
            if not subset:
                continue
            scores = [int(row["score"]) for row in subset]
            values = [int(row["value"]) for row in subset]
            examples = [f"`{row['id']}`" for row in sorted(subset, key=lambda item: (int(item["score"]), int(item["value"])), reverse=True)[:6]]
            lines.append(f"| {tier} | {len(subset)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(values):.0f} | {compact(examples)} |")
        lines.append("")
        for tier in ["Tier 1 - Light", "Tier 2 - Regular", "Tier 3 - Heavy", "Tier 4 - Elite"]:
            subset = sorted(tier_groups.get(tier, []), key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])), reverse=True)
            if not subset:
                continue
            lines.append(f"#### {slot} - {tier}")
            lines.append("")
            lines.append("| Item | Score | H/B/L | Weight | Difficulty | Value | Value/score | Uses | Warnings |")
            lines.append("|---|---:|---|---:|---:|---:|---:|---:|---|")
            for row in subset:
                uses = int(row["troop_uses"]) + int(row["hero_uses"])
                lines.append(
                    "| {id} | {score} | {h}/{b}/{l} | {weight} | {difficulty} | {value} | {vps} | {uses} | {warnings} |".format(
                        id=md_escape(row["id"]),
                        score=row["score"],
                        h=row["head"],
                        b=row["body"],
                        l=row["leg"],
                        weight=row["weight"],
                        difficulty=row["difficulty"],
                        value=row["value"],
                        vps=row["value_per_score"],
                        uses=uses,
                        warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
                    )
                )
            lines.append("")


def append_full_tables(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Full Armor Tables")
    lines.append("")
    for title, group_rows in [
        ("Buyable Armor", [row for row in rows if row["buyable"]]),
        ("Non-Buyable / Troop-Only Armor", [row for row in rows if not row["buyable"]]),
    ]:
        lines.append(f"### {title}")
        lines.append("")
        by_type: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in group_rows:
            by_type[str(row["type"])].append(row)
        for armor_type in ["Head", "Body", "Foot", "Hands"]:
            subset = sorted(by_type.get(armor_type, []), key=lambda row: (int(row["score"]), int(row["value"]), str(row["id"])))
            if not subset:
                continue
            lines.append(f"#### {armor_type}")
            lines.append("")
            lines.append("| Item ID | Name | Score | Band | H/B/L | Weight | Difficulty | Value | Value/score | Imods | Troop uses | Hero uses |")
            lines.append("|---|---|---:|---|---|---:|---:|---:|---:|---|---:|---:|")
            for row in subset:
                lines.append(
                    "| {id} | {name} | {score} | {band} | {h}/{b}/{l} | {weight} | {difficulty} | {value} | {vps} | {imod} | {troop_uses} | {hero_uses} |".format(
                        id=md_escape(row["id"]),
                        name=md_escape(row["name"]),
                        score=row["score"],
                        band=md_escape(row["band"]),
                        h=row["head"],
                        b=row["body"],
                        l=row["leg"],
                        weight=row["weight"],
                        difficulty=row["difficulty"],
                        value=row["value"],
                        vps=row["value_per_score"],
                        imod=md_escape(row["imod"]),
                        troop_uses=row["troop_uses"],
                        hero_uses=row["hero_uses"],
                    )
                )
            lines.append("")


def write_report(rows: list[dict[str, object]]) -> None:
    lines: list[str] = []
    lines.append("# Armor Audit")
    lines.append("")
    lines.append(
        "Generated from `compile/module_items.py` and troop inventories. Scores are balancing aids: body armor score uses body + leg + half head; other slots use their primary armor value."
    )
    lines.append("")
    lines.append("## Global Summary")
    lines.append("")
    lines.append(f"- Armor items audited: {len(rows)}")
    lines.append(f"- Buyable armor: {sum(1 for row in rows if row['buyable'])}; non-buyable armor: {sum(1 for row in rows if not row['buyable'])}")
    lines.append("- Slot counts: " + compact([f"{slot} {count}" for slot, count in Counter(str(row["type"]) for row in rows).most_common()]))
    lines.append(f"- Warning rows: {sum(1 for row in rows if row['warnings'])}")
    lines.append("")
    append_type_summary(lines, rows)
    append_watchlists(lines, rows)
    append_buyability_pressure(lines, rows)
    append_buyable_tiers(lines, rows)
    append_full_tables(lines, rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_report(rows)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} armor items).")


if __name__ == "__main__":
    main()
