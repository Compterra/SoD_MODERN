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
    get_hit_points,
    get_speed_rating,
    get_weapon_length,
    get_weight,
    itp_covers_legs,
    itp_merchandise,
    itp_type_shield,
    itp_wooden_parry,
)
from header_troops import tf_hero  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "shield_audit.md"

IMOD_NAMES = {
    "imodbits_none": 0,
    "imodbits_shield": getattr(module_items, "imodbits_shield", None),
}


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact(values: list[str], empty: str = "-") -> str:
    return ", ".join(values) if values else empty


def imod_label(bits: int) -> str:
    matches = [name.replace("imodbits_", "") for name, value in IMOD_NAMES.items() if value == bits]
    return matches[0] if matches else str(bits)


def item_usage() -> dict[int, Counter[str]]:
    usage: dict[int, Counter[str]] = defaultdict(Counter)
    for troop in module_troops.troops:
        troop_id, name, plural, flags, scene, reserved, faction_id, inventory = troop[:8]
        kind = "hero" if flags & tf_hero else "troop"
        for item_id in inventory:
            if isinstance(item_id, int):
                usage[item_id][kind] += 1
    return usage


def shield_flags(flags: int) -> list[str]:
    tags: list[str] = []
    if flags & itp_covers_legs:
        tags.append("covers legs")
    if flags & itp_wooden_parry:
        tags.append("wooden")
    return tags


def shield_score(row: dict[str, object]) -> int:
    return int(row["size"]) + int(row["resistance"]) * 2 + int(row["hit_points"]) // 10 + int(row["speed"]) // 5


def shield_band(score: int) -> str:
    if score >= 210:
        return "wall"
    if score >= 170:
        return "heavy"
    if score >= 130:
        return "military"
    if score >= 90:
        return "light"
    if score > 0:
        return "poor"
    return "zero"


def buyable_shield_tier(row: dict[str, object]) -> str:
    score = int(row["score"])
    if score >= 220:
        return "Tier 4 - Wall"
    if score >= 170:
        return "Tier 3 - Heavy"
    if score >= 125:
        return "Tier 2 - Military"
    return "Tier 1 - Light"


def build_rows() -> list[dict[str, object]]:
    usage = item_usage()
    rows: list[dict[str, object]] = []
    for item_id, item in enumerate(module_items.items):
        item_key, item_name, meshes, flags, capabilities, value, stats, imodbits = item[:8]
        if (flags & 0xFF) != itp_type_shield:
            continue
        row = {
            "index": item_id,
            "id": item_key,
            "name": item_name,
            "buyable": bool(flags & itp_merchandise),
            "value": value,
            "weight": get_weight(stats),
            "difficulty": get_difficulty(stats),
            "hit_points": get_hit_points(stats),
            "speed": get_speed_rating(stats),
            "size": get_weapon_length(stats),
            "resistance": get_body_armor(stats),
            "flags": shield_flags(flags),
            "imod": imod_label(imodbits),
            "troop_uses": usage[item_id]["troop"],
            "hero_uses": usage[item_id]["hero"],
            "warnings": [],
        }
        score = shield_score(row)
        row["score"] = score
        row["band"] = shield_band(score)
        row["buyable_tier"] = buyable_shield_tier(row)
        warnings: list[str] = row["warnings"]  # type: ignore[assignment]
        if int(row["hit_points"]) <= 0:
            warnings.append("zero hit points")
        if int(row["size"]) <= 0:
            warnings.append("zero size")
        if int(row["resistance"]) <= 0:
            warnings.append("zero resistance")
        if int(row["speed"]) <= 0:
            warnings.append("zero speed")
        if value <= 0 and score > 0:
            warnings.append("positive shield with zero value")
        if value > 0 and score > 0:
            value_per_score = value / score
            row["value_per_score"] = round(value_per_score, 1)
            if value_per_score > 35:
                warnings.append("expensive for protection")
            elif value_per_score < 1.5 and score >= 130:
                warnings.append("cheap for protection")
        else:
            row["value_per_score"] = 0
        if int(row["size"]) >= 100 and "covers legs" not in row["flags"]:
            warnings.append("large shield not covering legs")
        rows.append(row)
    return rows


def append_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    scores = [int(row["score"]) for row in rows]
    sizes = [int(row["size"]) for row in rows]
    resistance = [int(row["resistance"]) for row in rows]
    hp = [int(row["hit_points"]) for row in rows]
    bands = Counter(str(row["band"]) for row in rows)
    lines.append("## Global Summary")
    lines.append("")
    lines.append(f"- Shields audited: {len(rows)}")
    lines.append(f"- Buyable shields: {sum(1 for row in rows if row['buyable'])}; non-buyable shields: {sum(1 for row in rows if not row['buyable'])}")
    lines.append(f"- Score range: {min(scores)}-{max(scores)}; average score: {statistics.mean(scores):.1f}")
    lines.append(f"- Size range: {min(sizes)}-{max(sizes)}; resistance range: {min(resistance)}-{max(resistance)}; hit point range: {min(hp)}-{max(hp)}")
    lines.append("- Bands: " + compact([f"{band} {count}" for band, count in bands.most_common()]))
    lines.append(f"- Warning rows: {sum(1 for row in rows if row['warnings'])}")
    lines.append("")


def append_watchlists(lines: list[str], rows: list[dict[str, object]]) -> None:
    top_rows = sorted(rows, key=lambda row: (int(row["score"]), int(row["value"])), reverse=True)[:40]
    warning_rows = [row for row in rows if row["warnings"]]
    lines.append("## Top Shield Pressure")
    lines.append("")
    lines.append("| Shield | Score | Band | Size | Resistance | HP | Speed | Weight | Value | Flags | Uses | Warnings |")
    lines.append("|---|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for row in top_rows:
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {score} | {band} | {size} | {resistance} | {hp} | {speed} | {weight} | {value} | {flags} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                score=row["score"],
                band=md_escape(row["band"]),
                size=row["size"],
                resistance=row["resistance"],
                hp=row["hit_points"],
                speed=row["speed"],
                weight=row["weight"],
                value=row["value"],
                flags=md_escape(compact(row["flags"])),  # type: ignore[arg-type]
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")
    lines.append("## Shield Watchlist")
    lines.append("")
    if not warning_rows:
        lines.append("No structural shield warnings found.")
        lines.append("")
        return
    lines.append("| Shield | Score | Band | Size/Res/HP/Speed | Value | Uses | Warnings |")
    lines.append("|---|---:|---|---|---:|---:|---|")
    for row in sorted(warning_rows, key=lambda item: (str(item["band"]), str(item["id"]))):
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {score} | {band} | {size}/{resistance}/{hp}/{speed} | {value} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                score=row["score"],
                band=md_escape(row["band"]),
                size=row["size"],
                resistance=row["resistance"],
                hp=row["hit_points"],
                speed=row["speed"],
                value=row["value"],
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")


def append_buyable_tiers(lines: list[str], rows: list[dict[str, object]]) -> None:
    buyable = [row for row in rows if row["buyable"]]
    tier_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in buyable:
        tier_groups[str(row["buyable_tier"])].append(row)
    lines.append("## Buyable Shield Tiers")
    lines.append("")
    lines.append("Only buyable shields are tiered here. Shield score combines size, resistance, HP, and speed.")
    lines.append("")
    lines.append("Tier thresholds: `1-124`, `125-169`, `170-219`, `220+`.")
    lines.append("")
    lines.append("| Tier | Count | Score range | Avg score | Avg value | Example shields |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for tier in ["Tier 1 - Light", "Tier 2 - Military", "Tier 3 - Heavy", "Tier 4 - Wall"]:
        subset = tier_groups.get(tier, [])
        if not subset:
            continue
        scores = [int(row["score"]) for row in subset]
        values = [int(row["value"]) for row in subset]
        examples = [f"`{row['id']}`" for row in sorted(subset, key=lambda item: (int(item["score"]), int(item["value"])), reverse=True)[:6]]
        lines.append(f"| {tier} | {len(subset)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(values):.0f} | {compact(examples)} |")
    lines.append("")
    for tier in ["Tier 1 - Light", "Tier 2 - Military", "Tier 3 - Heavy", "Tier 4 - Wall"]:
        subset = sorted(tier_groups.get(tier, []), key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])), reverse=True)
        if not subset:
            continue
        lines.append(f"### {tier}")
        lines.append("")
        lines.append("| Shield | Score | Size | Resistance | HP | Speed | Weight | Difficulty | Value | Value/score | Uses | Warnings |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for row in subset:
            uses = int(row["troop_uses"]) + int(row["hero_uses"])
            lines.append(
                "| {id} | {score} | {size} | {resistance} | {hp} | {speed} | {weight} | {difficulty} | {value} | {vps} | {uses} | {warnings} |".format(
                    id=md_escape(row["id"]),
                    score=row["score"],
                    size=row["size"],
                    resistance=row["resistance"],
                    hp=row["hit_points"],
                    speed=row["speed"],
                    weight=row["weight"],
                    difficulty=row["difficulty"],
                    value=row["value"],
                    vps=row["value_per_score"],
                    uses=uses,
                    warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
                )
            )
        lines.append("")


def append_full_table(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Full Shield Table")
    lines.append("")
    lines.append("| Shield ID | Name | Buyable | Score | Band | Size | Resistance | HP | Speed | Weight | Difficulty | Value | Value/score | Imods | Flags | Troop uses | Hero uses |")
    lines.append("|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|")
    for row in sorted(rows, key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"]))):
        lines.append(
            "| {id} | {name} | {buyable} | {score} | {band} | {size} | {resistance} | {hp} | {speed} | {weight} | {difficulty} | {value} | {vps} | {imod} | {flags} | {troop_uses} | {hero_uses} |".format(
                id=md_escape(row["id"]),
                name=md_escape(row["name"]),
                buyable="yes" if row["buyable"] else "no",
                score=row["score"],
                band=md_escape(row["band"]),
                size=row["size"],
                resistance=row["resistance"],
                hp=row["hit_points"],
                speed=row["speed"],
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
    lines.append("# Shield Audit")
    lines.append("")
    lines.append("Generated from `compile/module_items.py` and troop inventories. Scores combine shield size, resistance, hit points, and speed for balance review.")
    lines.append("")
    append_summary(lines, rows)
    append_watchlists(lines, rows)
    append_buyable_tiers(lines, rows)
    append_full_table(lines, rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_report(rows)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} shields).")


if __name__ == "__main__":
    main()
