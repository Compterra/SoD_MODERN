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
    get_missile_speed,
    get_speed_rating,
    get_thrust_damage,
    get_weight,
    itp_merchandise,
    itp_type_horse,
)
from header_troops import tf_hero  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore


OUT_PATH = ROOT / "docs" / "reports" / "mount_audit.md"
DEFAULT_HORSE_HIT_POINTS = 100

IMOD_NAMES = {
    "imodbits_none": 0,
    "imodbits_horse_basic": getattr(module_items, "imodbits_horse_basic", None),
    "imodbits_horse_good": getattr(module_items, "imodbits_horse_good", None),
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


def mount_score(row: dict[str, object]) -> int:
    return (
        int(row["speed"])
        + int(row["maneuver"])
        + int(row["charge"]) * 2
        + int(row["armor"])
        + int(row["hit_points"]) // 5
    )


def mount_band(score: int) -> str:
    if score >= 190:
        return "endgame"
    if score >= 160:
        return "elite"
    if score >= 130:
        return "warhorse"
    if score >= 100:
        return "riding"
    if score > 0:
        return "light"
    return "zero"


def mount_tier(row: dict[str, object]) -> str:
    score = int(row["score"])
    difficulty = int(row["difficulty"])
    if score >= 215 or difficulty >= 5:
        return "Tier 5 - Endgame / specialist"
    if score >= 190:
        return "Tier 4 - Elite heavy"
    if score >= 160:
        return "Tier 3 - Warhorse"
    if score >= 135:
        return "Tier 2 - Hunter / military riding"
    if score >= 100:
        return "Tier 1 - Riding horse"
    return "Tier 0 - Practice / weak"


def mount_hp_label(row: dict[str, object]) -> str:
    hp = int(row["hit_points"])
    return f"{hp}*" if row["implicit_hit_points"] else str(hp)


def build_rows() -> list[dict[str, object]]:
    usage = item_usage()
    rows: list[dict[str, object]] = []
    for item_id, item in enumerate(module_items.items):
        item_key, item_name, meshes, flags, capabilities, value, stats, imodbits = item[:8]
        if (flags & 0xFF) != itp_type_horse:
            continue
        raw_hit_points = get_hit_points(stats)
        row = {
            "index": item_id,
            "id": item_key,
            "name": item_name,
            "buyable": bool(flags & itp_merchandise),
            "value": value,
            "weight": get_weight(stats),
            "difficulty": get_difficulty(stats),
            "raw_hit_points": raw_hit_points,
            "hit_points": raw_hit_points or DEFAULT_HORSE_HIT_POINTS,
            "implicit_hit_points": raw_hit_points == 0,
            "speed": get_missile_speed(stats),
            "maneuver": get_speed_rating(stats),
            "charge": get_thrust_damage(stats) & 0xFF,
            "armor": get_body_armor(stats),
            "imod": imod_label(imodbits),
            "troop_uses": usage[item_id]["troop"],
            "hero_uses": usage[item_id]["hero"],
            "warnings": [],
        }
        score = mount_score(row)
        row["score"] = score
        row["band"] = mount_band(score)
        row["tier"] = mount_tier(row)
        warnings: list[str] = row["warnings"]  # type: ignore[assignment]
        if int(row["speed"]) <= 0:
            warnings.append("zero speed")
        if row["implicit_hit_points"]:
            warnings.append("implicit/default hit points")
        if int(row["armor"]) <= 0 and score >= 120:
            warnings.append("strong mount with zero armor")
        if value <= 0 and score > 0:
            warnings.append("positive mount with zero value")
        if value > 0 and score > 0:
            value_per_score = value / score
            row["value_per_score"] = round(value_per_score, 1)
            if value_per_score > 90:
                warnings.append("expensive for performance")
            elif value_per_score < 5 and score >= 120:
                warnings.append("cheap for performance")
        else:
            row["value_per_score"] = 0
        if int(row["difficulty"]) >= 5 and score < 120:
            warnings.append("high riding requirement for modest mount")
        rows.append(row)
    return rows


def append_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    scores = [int(row["score"]) for row in rows]
    speeds = [int(row["speed"]) for row in rows]
    armor = [int(row["armor"]) for row in rows]
    charges = [int(row["charge"]) for row in rows]
    bands = Counter(str(row["band"]) for row in rows)
    lines.append("## Global Summary")
    lines.append("")
    lines.append(f"- Mount items audited: {len(rows)}")
    lines.append(f"- Buyable mounts: {sum(1 for row in rows if row['buyable'])}; non-buyable mounts: {sum(1 for row in rows if not row['buyable'])}")
    lines.append(f"- Mounts with implicit/default HP: {sum(1 for row in rows if row['implicit_hit_points'])} (shown as {DEFAULT_HORSE_HIT_POINTS}* in tables)")
    lines.append(f"- Score range: {min(scores)}-{max(scores)}; average score: {statistics.mean(scores):.1f}")
    lines.append(f"- Speed range: {min(speeds)}-{max(speeds)}; armor range: {min(armor)}-{max(armor)}; charge range: {min(charges)}-{max(charges)}")
    lines.append("- Bands: " + compact([f"{band} {count}" for band, count in bands.most_common()]))
    lines.append(f"- Warning rows: {sum(1 for row in rows if row['warnings'])}")
    lines.append("")


def append_watchlists(lines: list[str], rows: list[dict[str, object]]) -> None:
    top_rows = sorted(rows, key=lambda row: (int(row["score"]), int(row["value"])), reverse=True)[:35]
    warning_rows = [row for row in rows if row["warnings"]]
    lines.append("## Top Mount Pressure")
    lines.append("")
    lines.append("| Mount | Score | Band | HP | Speed | Maneuver | Armor | Charge | Riding | Value | Imods | Uses | Warnings |")
    lines.append("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for row in top_rows:
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {score} | {band} | {hp} | {speed} | {maneuver} | {armor} | {charge} | {difficulty} | {value} | {imod} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                score=row["score"],
                band=md_escape(row["band"]),
                hp=mount_hp_label(row),
                speed=row["speed"],
                maneuver=row["maneuver"],
                armor=row["armor"],
                charge=row["charge"],
                difficulty=row["difficulty"],
                value=row["value"],
                imod=md_escape(row["imod"]),
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")
    lines.append("## Mount Watchlist")
    lines.append("")
    if not warning_rows:
        lines.append("No structural mount warnings found.")
        lines.append("")
        return
    lines.append("| Mount | Score | Band | HP/Speed/Maneuver/Armor/Charge | Riding | Value | Uses | Warnings |")
    lines.append("|---|---:|---|---|---:|---:|---:|---|")
    for row in sorted(warning_rows, key=lambda item: (str(item["band"]), str(item["id"]))):
        uses = int(row["troop_uses"]) + int(row["hero_uses"])
        lines.append(
            "| {id} | {score} | {band} | {hp}/{speed}/{maneuver}/{armor}/{charge} | {difficulty} | {value} | {uses} | {warnings} |".format(
                id=md_escape(row["id"]),
                score=row["score"],
                band=md_escape(row["band"]),
                hp=mount_hp_label(row),
                speed=row["speed"],
                maneuver=row["maneuver"],
                armor=row["armor"],
                charge=row["charge"],
                difficulty=row["difficulty"],
                value=row["value"],
                uses=uses,
                warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
            )
        )
    lines.append("")


def append_buyable_outliers(lines: list[str], rows: list[dict[str, object]]) -> None:
    buyable = [row for row in rows if row["buyable"]]
    by_tier: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in buyable:
        by_tier[str(row["tier"])].append(row)
    singleton_top_tiers = [
        row
        for tier, tier_rows in by_tier.items()
        if len(tier_rows) == 1 and ("Tier 5" in tier or "Tier 4" in tier)
        for row in tier_rows
    ]
    score_sorted = sorted(buyable, key=lambda row: int(row["score"]), reverse=True)
    gap_rows = []
    for index, row in enumerate(score_sorted[:-1]):
        next_row = score_sorted[index + 1]
        score_gap = int(row["score"]) - int(next_row["score"])
        value_gap = int(row["value"]) - int(next_row["value"])
        if score_gap >= 10 or abs(value_gap) >= 400:
            gap_rows.append((row, next_row, score_gap, value_gap))

    lines.append("## Buyable Mount Outliers")
    lines.append("")
    lines.append("These are the mounts most likely to need manual review before broad tier rebalancing.")
    lines.append("")
    if singleton_top_tiers:
        lines.append("### Singleton Top Tiers")
        lines.append("")
        lines.append("| Mount | Tier | Score | Next lower score | Score gap | HP | Speed | Maneuver | Armor | Charge | Riding | Value | Notes |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for row in singleton_top_tiers:
            lower = next((candidate for candidate in score_sorted if int(candidate["score"]) < int(row["score"])), None)
            lower_score = int(lower["score"]) if lower else 0
            notes = ["alone in buyable top tier"]
            if lower:
                notes.append(f"next lower `{lower['id']}`")
            lines.append(
                "| {id} | {tier} | {score} | {lower_score} | {score_gap} | {hp} | {speed} | {maneuver} | {armor} | {charge} | {difficulty} | {value} | {notes} |".format(
                    id=md_escape(row["id"]),
                    tier=md_escape(row["tier"]),
                    score=row["score"],
                    lower_score=lower_score,
                    score_gap=int(row["score"]) - lower_score,
                    hp=mount_hp_label(row),
                    speed=row["speed"],
                    maneuver=row["maneuver"],
                    armor=row["armor"],
                    charge=row["charge"],
                    difficulty=row["difficulty"],
                    value=row["value"],
                    notes=md_escape(compact(notes)),
                )
            )
        lines.append("")
    if gap_rows:
        lines.append("### Largest Buyable Step Gaps")
        lines.append("")
        lines.append("| Higher mount | Lower mount | Score gap | Value gap | Higher tier | Lower tier |")
        lines.append("|---|---|---:|---:|---|---|")
        for high, low, score_gap, value_gap in gap_rows[:20]:
            lines.append(
                f"| `{md_escape(high['id'])}` ({high['score']}, {high['value']}g) | `{md_escape(low['id'])}` ({low['score']}, {low['value']}g) | {score_gap} | {value_gap} | {md_escape(high['tier'])} | {md_escape(low['tier'])} |"
            )
        lines.append("")


def append_tier_summary(lines: list[str], rows: list[dict[str, object]]) -> None:
    sections = [
        ("Buyable Mounts", [row for row in rows if row["buyable"]]),
        ("Non-Buyable / Troop-Only Mounts", [row for row in rows if not row["buyable"]]),
    ]
    lines.append("## Mount Tier Groups")
    lines.append("")
    lines.append(f"Use these tiers as the first balancing pass. Buyable mounts are economy-facing and should have coherent prices; non-buyable mounts are troop-only, quest, heraldic, blacksmith, or special-purpose mounts and should be balanced primarily by access and troop role. HP values marked `{DEFAULT_HORSE_HIT_POINTS}*` were not explicitly set in module_items and are scored with the audit default.")
    lines.append("")
    lines.append("Tier thresholds after default HP normalization: Tier 1 `100-134`, Tier 2 `135-159`, Tier 3 `160-189`, Tier 4 `190-214`, Tier 5 `215+` or riding requirement `5+`.")
    lines.append("")
    for title, section_rows in sections:
        lines.append(f"### {title}")
        lines.append("")
        if not section_rows:
            lines.append("No mounts in this group.")
            lines.append("")
            continue
        by_tier: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in section_rows:
            by_tier[str(row["tier"])].append(row)
        lines.append("| Tier | Count | Score range | Avg score | Avg value | Avg riding | Example mounts |")
        lines.append("|---|---:|---:|---:|---:|---:|---|")
        for tier in sorted(by_tier):
            subset = by_tier[tier]
            scores = [int(row["score"]) for row in subset]
            values = [int(row["value"]) for row in subset]
            difficulties = [int(row["difficulty"]) for row in subset]
            examples = [f"`{row['id']}`" for row in sorted(subset, key=lambda item: int(item["score"]), reverse=True)[:6]]
            lines.append(
                f"| {tier} | {len(subset)} | {min(scores)}-{max(scores)} | {statistics.mean(scores):.1f} | {statistics.mean(values):.0f} | {statistics.mean(difficulties):.1f} | {compact(examples)} |"
            )
        lines.append("")
    lines.append("## Mounts by Tier")
    lines.append("")
    for title, section_rows in sections:
        lines.append(f"### {title}")
        lines.append("")
        by_tier = defaultdict(list)
        for row in section_rows:
            by_tier[str(row["tier"])].append(row)
        for tier in sorted(by_tier):
            subset = sorted(by_tier[tier], key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])), reverse=True)
            lines.append(f"#### {tier}")
            lines.append("")
            lines.append("| Mount | Score | HP | Speed | Maneuver | Armor | Charge | Riding | Value | Uses | Warnings |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
            for row in subset:
                uses = int(row["troop_uses"]) + int(row["hero_uses"])
                lines.append(
                    "| {id} | {score} | {hp} | {speed} | {maneuver} | {armor} | {charge} | {difficulty} | {value} | {uses} | {warnings} |".format(
                        id=md_escape(row["id"]),
                        score=row["score"],
                        hp=mount_hp_label(row),
                        speed=row["speed"],
                        maneuver=row["maneuver"],
                        armor=row["armor"],
                        charge=row["charge"],
                        difficulty=row["difficulty"],
                        value=row["value"],
                        uses=uses,
                        warnings=md_escape(compact(row["warnings"])),  # type: ignore[arg-type]
                    )
                )
            lines.append("")


def append_full_table(lines: list[str], rows: list[dict[str, object]]) -> None:
    lines.append("## Full Mount Table")
    lines.append("")
    lines.append("| Mount ID | Name | Buyable | Tier | Score | Band | HP | Raw HP | Speed | Maneuver | Armor | Charge | Riding | Value | Value/score | Imods | Troop uses | Hero uses |")
    lines.append("|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|")
    for row in sorted(rows, key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"]))):
        lines.append(
            "| {id} | {name} | {buyable} | {tier} | {score} | {band} | {hp} | {raw_hp} | {speed} | {maneuver} | {armor} | {charge} | {difficulty} | {value} | {vps} | {imod} | {troop_uses} | {hero_uses} |".format(
                id=md_escape(row["id"]),
                name=md_escape(row["name"]),
                buyable="yes" if row["buyable"] else "no",
                tier=md_escape(row["tier"]),
                score=row["score"],
                band=md_escape(row["band"]),
                hp=mount_hp_label(row),
                raw_hp=row["raw_hit_points"],
                speed=row["speed"],
                maneuver=row["maneuver"],
                armor=row["armor"],
                charge=row["charge"],
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
    lines.append("# Mount Audit")
    lines.append("")
    lines.append(f"Generated from `compile/module_items.py` and troop inventories. Mount speed follows the existing item scoring convention: horse speed is stored in the missile-speed field; maneuver is stored in the speed-rating field. Horses without explicit `hit_points(...)` are treated as implicit/default HP and displayed as `{DEFAULT_HORSE_HIT_POINTS}*`.")
    lines.append("")
    append_summary(lines, rows)
    append_watchlists(lines, rows)
    append_buyable_outliers(lines, rows)
    append_tier_summary(lines, rows)
    append_full_table(lines, rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_report(rows)
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(rows)} mount items).")


if __name__ == "__main__":
    main()
