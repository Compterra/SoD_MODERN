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
sys.path.insert(0, str(ROOT / "src" / "constants"))

from header_items import (  # type: ignore
    blunt,
    cut,
    food_quality,
    get_abundance,
    get_body_armor,
    get_difficulty,
    get_head_armor,
    get_hit_points,
    get_leg_armor,
    get_max_ammo,
    get_missile_speed,
    get_speed_rating,
    get_swing_damage,
    get_thrust_damage,
    get_weapon_length,
    get_weight,
    iwf_damage_type_bits,
    itp_consumable,
    itp_food,
    itp_merchandise,
    itp_type_arrows,
    itp_type_body_armor,
    itp_type_bolts,
    itp_type_book,
    itp_type_bow,
    itp_type_bullets,
    itp_type_crossbow,
    itp_type_foot_armor,
    itp_type_goods,
    itp_type_hand_armor,
    itp_type_head_armor,
    itp_type_horse,
    itp_type_one_handed_wpn,
    itp_type_polearm,
    itp_type_shield,
    itp_type_thrown,
    itp_type_two_handed_wpn,
    itp_unique,
    pierce,
)
from header_troops import tf_hero  # type: ignore
import module_factions  # type: ignore
import module_items  # type: ignore
import module_troops  # type: ignore


REPORT_DIR = ROOT / "docs" / "reports"
REPORTS = {
    "ammo": REPORT_DIR / "ammo_audit.md",
    "loadouts": REPORT_DIR / "troop_loadout_audit.md",
    "value": REPORT_DIR / "item_value_availability_audit.md",
    "imod": REPORT_DIR / "imod_compatibility_audit.md",
    "goods": REPORT_DIR / "goods_food_audit.md",
    "special": REPORT_DIR / "special_item_audit.md",
}

ITEM_TYPE_NAMES = {
    itp_type_horse: "Horse",
    itp_type_one_handed_wpn: "1H",
    itp_type_two_handed_wpn: "2H",
    itp_type_polearm: "Polearm",
    itp_type_arrows: "Arrows",
    itp_type_bolts: "Bolts",
    itp_type_shield: "Shield",
    itp_type_bow: "Bow",
    itp_type_crossbow: "Crossbow",
    itp_type_thrown: "Thrown",
    itp_type_bullets: "Bullets",
    itp_type_goods: "Goods",
    itp_type_head_armor: "Head",
    itp_type_body_armor: "Body",
    itp_type_foot_armor: "Foot",
    itp_type_hand_armor: "Hands",
    itp_type_book: "Book",
}

IMOD_NAMES = {
    "none": 0,
    "horse_basic": getattr(module_items, "imodbits_horse_basic", None),
    "horse_good": getattr(module_items, "imodbits_horse_good", None),
    "cloth": getattr(module_items, "imodbits_cloth", None),
    "armor": getattr(module_items, "imodbits_armor", None),
    "plate": getattr(module_items, "imodbits_plate", None),
    "shield": getattr(module_items, "imodbits_shield", None),
    "sword": getattr(module_items, "imodbits_sword", None),
    "sword_high": getattr(module_items, "imodbits_sword_high", None),
    "axe": getattr(module_items, "imodbits_axe", None),
    "mace": getattr(module_items, "imodbits_mace", None),
    "pick": getattr(module_items, "imodbits_pick", None),
    "polearm": getattr(module_items, "imodbits_polearm", None),
    "bow": getattr(module_items, "imodbits_bow", None),
    "crossbow": getattr(module_items, "imodbits_crossbow", None),
    "missile": getattr(module_items, "imodbits_missile", None),
    "thrown": getattr(module_items, "imodbits_thrown", None),
}

EXCLUDE_TROOP_PATTERNS = [
    re.compile(r"^cattle$"),
    re.compile(r"^farmer_from_bandit_village$"),
    re.compile(r"^log_array_"),
    re.compile(r"(^.*_begin$|^.*_end$)"),
    re.compile(r"(^|_)walker(_|$)"),
    re.compile(r"^tutorial_"),
    re.compile(r"^(arena_|novice_fighter$|regular_fighter$|veteran_fighter$|champion_fighter$)"),
    re.compile(r"_prisoner_"),
    re.compile(r"^relative_of_merchants"),
    re.compile(r"^(multiplayer_|quick_battle_)"),
    re.compile(r"(^temp_|_temp$|placeholder)"),
]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact(values: list[str], empty: str = "-") -> str:
    return ", ".join(values) if values else empty


def item_type(flags: int) -> int:
    return flags & 0xFF


def type_name(flags: int) -> str:
    return ITEM_TYPE_NAMES.get(item_type(flags), str(item_type(flags)))


def damage_amount(raw: int) -> int:
    return raw & 0xFF


def damage_type(raw: int) -> int:
    return (raw >> iwf_damage_type_bits) & 0x03


def effective_damage(raw: int) -> float:
    amount = float(damage_amount(raw))
    dtype = damage_type(raw)
    if dtype == pierce:
        amount *= 1.5
    elif dtype == blunt:
        amount *= 1.25
    return amount


def damage_label(raw: int) -> str:
    suffix = {cut: "c", pierce: "p", blunt: "b"}.get(damage_type(raw), "?")
    return f"{damage_amount(raw)}{suffix}"


def imod_label(bits: int) -> str:
    exact = [name for name, value in IMOD_NAMES.items() if value == bits]
    if exact:
        return exact[0]
    parts = [name for name, value in IMOD_NAMES.items() if value and bits & value == value]
    return "+".join(parts) if parts else str(bits)


def item_usage() -> dict[int, Counter[str]]:
    usage: dict[int, Counter[str]] = defaultdict(Counter)
    for troop in module_troops.troops:
        flags = troop[3]
        kind = "hero" if flags & tf_hero else "troop"
        for entry in troop[7]:
            if isinstance(entry, int):
                usage[entry][kind] += 1
    return usage


def faction_name(index: int) -> str:
    if isinstance(index, int) and 0 <= index < len(module_factions.factions):
        return module_factions.factions[index][0]
    return str(index)


def should_skip_troop(troop_id: str, flags: int) -> bool:
    return bool(flags & tf_hero) or any(pattern.search(troop_id) for pattern in EXCLUDE_TROOP_PATTERNS)


def combat_score(item: tuple) -> int:
    flags, value, stats = item[3], item[5], item[6]
    typ = item_type(flags)
    if typ in {itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm}:
        raw = max(effective_damage(get_swing_damage(stats)), effective_damage(get_thrust_damage(stats)))
        return int(raw + get_speed_rating(stats) / 4 + get_weapon_length(stats) / 10)
    if typ in {itp_type_bow, itp_type_crossbow, itp_type_thrown}:
        return int(effective_damage(get_thrust_damage(stats)) + get_missile_speed(stats) / 3 + get_max_ammo(stats) / 2)
    if typ in {itp_type_arrows, itp_type_bolts, itp_type_bullets}:
        return int(damage_amount(get_thrust_damage(stats)) + get_max_ammo(stats) / 2)
    if typ == itp_type_shield:
        return int(get_hit_points(stats) / 12 + get_body_armor(stats) * 3 + get_speed_rating(stats) / 4)
    if typ == itp_type_horse:
        return int(get_hit_points(stats) / 4 + get_body_armor(stats) + get_speed_rating(stats) + get_leg_armor(stats) + get_head_armor(stats))
    if typ == itp_type_body_armor:
        return get_body_armor(stats) + get_leg_armor(stats) + get_head_armor(stats) // 2
    if typ == itp_type_head_armor:
        return get_head_armor(stats)
    if typ == itp_type_foot_armor:
        return get_leg_armor(stats)
    if typ == itp_type_hand_armor:
        return get_body_armor(stats)
    return max(0, value // 100)


def all_item_rows() -> list[dict[str, object]]:
    usage = item_usage()
    rows = []
    for idx, item in enumerate(module_items.items):
        key, name, meshes, flags, caps, value, stats, imodbits = item[:8]
        score = combat_score(item)
        rows.append(
            {
                "index": idx,
                "id": key,
                "name": name,
                "type": type_name(flags),
                "flags": flags,
                "value": value,
                "stats": stats,
                "imodbits": imodbits,
                "imod": imod_label(imodbits),
                "score": score,
                "merchandise": bool(flags & itp_merchandise),
                "unique": bool(flags & itp_unique),
                "troop_uses": usage[idx]["troop"],
                "hero_uses": usage[idx]["hero"],
            }
        )
    return rows


def write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def audit_ammo(rows: list[dict[str, object]]) -> None:
    ammo = [r for r in rows if item_type(int(r["flags"])) in {itp_type_arrows, itp_type_bolts, itp_type_bullets, itp_type_thrown}]
    lines = ["# Ammo Audit", "", "Thrown weapons are included because Warband treats them as self-contained weapon/ammo stacks.", ""]
    counts = Counter(str(r["type"]) for r in ammo)
    lines += [
        "## Summary",
        "",
        f"- Ammo and thrown stacks audited: {len(ammo)}",
        "- Type counts: " + compact([f"{k} {v}" for k, v in counts.most_common()]),
        f"- Merchandise stacks: {sum(1 for r in ammo if r['merchandise'])}",
        f"- Non-buyable stacks: {sum(1 for r in ammo if not r['merchandise'])}",
        f"- Unused by non-hero troops: {sum(1 for r in ammo if not r['troop_uses'])}",
        "",
        "## Buyable Ammo Tiers",
        "",
        "Only buyable ammo and thrown stacks are tiered here. Thresholds use the audit score, which combines stack size and damage.",
        "",
        "Tier thresholds: `1-15`, `16-23`, `24-31`, `32+`.",
        "",
        "| Tier | Count | Score range | Avg score | Avg value | Example stacks |",
        "|---|---:|---:|---:|---:|---|",
    ]
    tier_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in [r for r in ammo if r["merchandise"]]:
        score = int(row["score"])
        if score >= 32:
            tier = "Tier 4 - Elite"
        elif score >= 24:
            tier = "Tier 3 - Veteran"
        elif score >= 16:
            tier = "Tier 2 - Regular"
        else:
            tier = "Tier 1 - Light"
        tier_groups[tier].append(row)
    for tier in ["Tier 1 - Light", "Tier 2 - Regular", "Tier 3 - Veteran", "Tier 4 - Elite"]:
        subset = tier_groups.get(tier, [])
        if not subset:
            continue
        scores = [int(row["score"]) for row in subset]
        values = [int(row["value"]) for row in subset]
        examples = [f"`{row['id']}`" for row in sorted(subset, key=lambda item: (int(item["score"]), int(item["value"])), reverse=True)[:6]]
        lines.append(f"| {tier} | {len(subset)} | {min(scores)}-{max(scores)} | {sum(scores) / len(scores):.1f} | {sum(values) / len(values):.0f} | {compact(examples)} |")
    lines.append("")
    for tier in ["Tier 1 - Light", "Tier 2 - Regular", "Tier 3 - Veteran", "Tier 4 - Elite"]:
        subset = sorted(tier_groups.get(tier, []), key=lambda item: (int(item["score"]), int(item["value"]), str(item["id"])), reverse=True)
        if not subset:
            continue
        lines.append(f"### {tier}")
        lines.append("")
        lines.append("| Item | Type | Score | Ammo | Damage | Speed | Value | Uses | Flags |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
        for row in subset:
            stats = int(row["stats"])
            flags = []
            if not row["troop_uses"]:
                flags.append("unused")
            lines.append(f"| `{md(row['id'])}` | {row['type']} | {row['score']} | {get_max_ammo(stats)} | {damage_label(get_thrust_damage(stats))} | {get_speed_rating(stats)} | {row['value']} | {row['troop_uses']} | {compact(flags)} |")
        lines.append("")
    lines += [
        "## Stack Pressure Watchlist",
        "",
        "| Item | Type | Ammo | Damage | Speed | Value | Uses | Flags |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    watch = sorted(ammo, key=lambda r: (get_max_ammo(int(r["stats"])), int(r["score"])), reverse=True)[:40]
    for row in watch:
        stats = int(row["stats"])
        flags = []
        if not row["merchandise"]:
            flags.append("not shop")
        if not row["troop_uses"]:
            flags.append("unused")
        lines.append(
            f"| `{md(row['id'])}` | {row['type']} | {get_max_ammo(stats)} | {damage_label(get_thrust_damage(stats))} | {get_speed_rating(stats)} | {row['value']} | {row['troop_uses']} | {compact(flags)} |"
        )
    lines += ["", "## Full Ammo Table", "", "| Item | Name | Type | Ammo | Damage | Missile speed | Weight | Value | Imod | Troop uses |", "|---|---|---|---:|---:|---:|---:|---:|---|---:|"]
    for row in sorted(ammo, key=lambda r: (str(r["type"]), str(r["id"]))):
        stats = int(row["stats"])
        lines.append(
            f"| `{md(row['id'])}` | {md(row['name'])} | {row['type']} | {get_max_ammo(stats)} | {damage_label(get_thrust_damage(stats))} | {get_missile_speed(stats)} | {get_weight(stats)} | {row['value']} | {row['imod']} | {row['troop_uses']} |"
        )
    write(REPORTS["ammo"], lines)


def audit_loadouts(rows: list[dict[str, object]]) -> None:
    by_index = {int(r["index"]): r for r in rows}
    troop_rows = []
    for troop in module_troops.troops:
        troop_id, name, plural, flags, scene, reserved, faction_id, inventory = troop[:8]
        if should_skip_troop(troop_id, flags):
            continue
        entries = [by_index[i] for i in inventory if isinstance(i, int) and i in by_index]
        best_melee = max([int(e["score"]) for e in entries if e["type"] in {"1H", "2H", "Polearm"}] or [0])
        best_ranged_weapon = max([int(e["score"]) for e in entries if e["type"] in {"Bow", "Crossbow", "Thrown"}] or [0])
        best_ammo = max([int(e["score"]) for e in entries if e["type"] in {"Arrows", "Bolts", "Bullets"}] or [0])
        best_ranged = best_ranged_weapon + best_ammo
        armor = sum(sorted([int(e["score"]) for e in entries if e["type"] in {"Head", "Body", "Foot", "Hands"}], reverse=True)[:4])
        shield = max([int(e["score"]) for e in entries if e["type"] == "Shield"] or [0])
        mount = max([int(e["score"]) for e in entries if e["type"] == "Horse"] or [0])
        kit = best_melee + best_ranged + armor + shield + mount
        warnings = []
        if best_melee == 0 and best_ranged == 0:
            warnings.append("no weapon")
        if armor == 0:
            warnings.append("no armor")
        if mount and not any(e["type"] in {"1H", "Polearm", "Bow", "Thrown"} for e in entries):
            warnings.append("mounted with awkward weapons")
        troop_rows.append((faction_name(faction_id), troop_id, name, best_melee, best_ranged, armor, shield, mount, kit, warnings))

    lines = ["# Troop Loadout Audit", "", "This combines the individual equipment audits into a troop-facing kit score for balance triage.", ""]
    by_faction = defaultdict(list)
    for row in troop_rows:
        by_faction[row[0]].append(row)
    lines += [
        "## Summary",
        "",
        f"- Non-hero combat troops audited: {len(troop_rows)}",
        f"- Factions represented: {len(by_faction)}",
        f"- Highest kit score: {max(row[8] for row in troop_rows)}",
        f"- Warning rows: {sum(1 for row in troop_rows if row[9])}",
        "",
        "## Faction Summary",
        "",
        "| Faction | Troops | Avg kit | Top kit | Warning rows |",
        "|---|---:|---:|---:|---:|",
    ]
    for faction, subset in sorted(by_faction.items()):
        lines.append(f"| {md(faction)} | {len(subset)} | {sum(r[8] for r in subset) / len(subset):.1f} | {max(r[8] for r in subset)} | {sum(1 for r in subset if r[9])} |")
    lines += ["", "## Top Kit Pressure", "", "| Troop | Faction | Melee | Ranged | Armor | Shield | Mount | Kit | Warnings |", "|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in sorted(troop_rows, key=lambda r: r[8], reverse=True)[:80]:
        lines.append(f"| `{md(row[1])}` | {md(row[0])} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {compact(row[9])} |")
    lines += ["", "## Full Loadout Table", "", "| Faction | Troop | Name | Melee | Ranged | Armor | Shield | Mount | Kit | Warnings |", "|---|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in sorted(troop_rows, key=lambda r: (r[0], r[1])):
        lines.append(f"| {md(row[0])} | `{md(row[1])}` | {md(row[2])} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {compact(row[9])} |")
    write(REPORTS["loadouts"], lines)


def audit_value(rows: list[dict[str, object]]) -> None:
    scored = [r for r in rows if int(r["score"]) > 0]
    watch = []
    for r in scored:
        score = int(r["score"])
        value = int(r["value"])
        notes = []
        if value <= 1 and score >= 40:
            notes.append("strong but near-free")
        if value > 0 and value / score > 300:
            notes.append("very expensive for score")
        if score >= 70 and not r["merchandise"] and not r["unique"]:
            notes.append("high power hidden from shops")
        if score >= 70 and r["merchandise"]:
            notes.append("elite shop item")
        if notes:
            watch.append((r, notes))
    lines = ["# Item Value and Availability Audit", "", "This checks whether combat/economic value, shop availability, uniqueness, and troop usage are pulling in the same direction.", ""]
    lines += ["## Summary", "", f"- Scored items: {len(scored)}", f"- Merchandise scored items: {sum(1 for r in scored if r['merchandise'])}", f"- Unique scored items: {sum(1 for r in scored if r['unique'])}", f"- Watchlist rows: {len(watch)}", ""]
    lines += ["## Watchlist", "", "| Item | Type | Score | Value | Merchandise | Unique | Troop uses | Notes |", "|---|---|---:|---:|---|---|---:|---|"]
    for r, notes in sorted(watch, key=lambda x: (int(x[0]["score"]), int(x[0]["value"])), reverse=True)[:150]:
        lines.append(f"| `{md(r['id'])}` | {r['type']} | {r['score']} | {r['value']} | {r['merchandise']} | {r['unique']} | {r['troop_uses']} | {compact(notes)} |")
    lines += ["", "## Top Scored Items", "", "| Item | Name | Type | Score | Value | Merchandise | Unique | Troop uses |", "|---|---|---|---:|---:|---|---|---:|"]
    for r in sorted(scored, key=lambda r: int(r["score"]), reverse=True)[:120]:
        lines.append(f"| `{md(r['id'])}` | {md(r['name'])} | {r['type']} | {r['score']} | {r['value']} | {r['merchandise']} | {r['unique']} | {r['troop_uses']} |")
    write(REPORTS["value"], lines)


def expected_imod(row: dict[str, object]) -> set[str]:
    typ = row["type"]
    item_id = str(row["id"]).lower()
    if typ == "Horse":
        return {"horse_basic", "horse_good"}
    if typ in {"Head", "Body", "Foot", "Hands"}:
        return {"cloth", "armor", "plate", "good", "none"}
    if typ == "Shield":
        return {"shield"}
    if typ in {"Arrows", "Bolts", "Bullets"}:
        return {"missile", "none"}
    if typ == "Bow":
        return {"bow"}
    if typ == "Crossbow":
        return {"crossbow"}
    if typ == "Thrown":
        return {"thrown"}
    if typ == "Polearm":
        return {"polearm", "sword", "axe", "mace", "pick", "none"}
    if typ in {"1H", "2H"}:
        if "axe" in item_id:
            return {"axe", "none"}
        if "mace" in item_id or "hammer" in item_id or "club" in item_id:
            return {"mace", "none"}
        if "pick" in item_id:
            return {"pick", "none"}
        return {"sword", "sword_high", "axe", "mace", "pick", "none"}
    return {"none"}


def audit_imod(rows: list[dict[str, object]]) -> None:
    rows_with_notes = []
    for r in rows:
        typ = str(r["type"])
        if typ in {"Goods", "Book"}:
            continue
        label = str(r["imod"])
        expected = expected_imod(r)
        notes = []
        if not any(part in expected for part in label.split("+")):
            notes.append(f"expected {compact(sorted(expected))}")
        if label == "none" and int(r["score"]) >= 60 and typ not in {"1H", "2H", "Polearm"}:
            notes.append("strong item has no modifiers")
        if notes:
            rows_with_notes.append((r, notes))
    lines = ["# Item Modifier Compatibility Audit", "", "This report checks item modifier families against broad item roles.", ""]
    lines += ["## Summary", "", f"- Modifier rows with notes: {len(rows_with_notes)}", ""]
    lines += ["## Compatibility Watchlist", "", "| Item | Type | Score | Imod | Expected/Notes |", "|---|---|---:|---|---|"]
    for r, notes in sorted(rows_with_notes, key=lambda x: (str(x[0]["type"]), str(x[0]["id"]))):
        lines.append(f"| `{md(r['id'])}` | {r['type']} | {r['score']} | {r['imod']} | {compact(notes)} |")
    write(REPORTS["imod"], lines)


def parse_game_start_slots(slot_name: str) -> dict[str, int]:
    text = (ROOT / "src" / "scripts" / "ZA_hardcoded_game_scripts" / "game_start.py").read_text(encoding="utf-8")
    pattern = re.compile(r'\(item_set_slot,\s*"itm_([^"]+)",\s*"?%s"?,\s*(-?\d+)\)' % re.escape(slot_name))
    return {item_id: int(value) for item_id, value in pattern.findall(text)}


def audit_goods(rows: list[dict[str, object]]) -> None:
    food_bonuses = parse_game_start_slots("slot_item_food_bonus")
    goods = [r for r in rows if item_type(int(r["flags"])) == itp_type_goods]
    lines = ["# Goods and Food Audit", "", "This focuses on campaign economy inputs: trade goods, food quality, stack size, abundance, and scripted food morale bonuses.", ""]
    lines += ["## Summary", "", f"- Goods rows: {len(goods)}", f"- Food rows: {sum(1 for r in goods if int(r['flags']) & itp_food)}", f"- Consumable rows: {sum(1 for r in goods if int(r['flags']) & itp_consumable)}", f"- Food bonus assignments found: {len(food_bonuses)}", ""]
    lines += ["## Food Balance Table", "", "| Item | Name | Value | Weight | Stack | Quality | Food bonus | Abundance | Merchandise | Notes |", "|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in [r for r in goods if int(r["flags"]) & itp_food]:
        stats = int(r["stats"])
        notes = []
        if str(r["id"]) not in food_bonuses and str(r["id"]) != "horse_meat":
            notes.append("no scripted bonus")
        if get_max_ammo(stats) <= 0:
            notes.append("zero stack")
        lines.append(f"| `{md(r['id'])}` | {md(r['name'])} | {r['value']} | {get_weight(stats)} | {get_max_ammo(stats)} | {food_quality(stats)} | {food_bonuses.get(str(r['id']), 0)} | {get_abundance(stats)} | {r['merchandise']} | {compact(notes)} |")
    lines += ["", "## Trade Goods Table", "", "| Item | Name | Value | Weight | Abundance | Merchandise | Consumable | Notes |", "|---|---|---:|---:|---:|---|---|---|"]
    for r in [r for r in goods if not int(r["flags"]) & itp_food]:
        stats = int(r["stats"])
        notes = []
        if not r["merchandise"]:
            notes.append("not shop")
        if int(r["value"]) <= 0:
            notes.append("zero value")
        lines.append(f"| `{md(r['id'])}` | {md(r['name'])} | {r['value']} | {get_weight(stats)} | {get_abundance(stats)} | {r['merchandise']} | {bool(int(r['flags']) & itp_consumable)} | {compact(notes)} |")
    write(REPORTS["goods"], lines)


def audit_special(rows: list[dict[str, object]]) -> None:
    int_reqs = parse_game_start_slots("slot_item_intelligence_requirement")
    special_patterns = re.compile(r"(book|royal|artifact|unique|blacksmith|banner|crown|regalia|strange|legend|dragon|skull)", re.I)
    special = [r for r in rows if r["unique"] or item_type(int(r["flags"])) == itp_type_book or special_patterns.search(str(r["id"])) or special_patterns.search(str(r["name"]))]
    lines = ["# Special Items Audit", "", "Books, artifacts, royal gear, unique flags, and other special-case items collected for later feature work.", ""]
    counts = Counter(str(r["type"]) for r in special)
    lines += ["## Summary", "", f"- Special rows: {len(special)}", "- Types: " + compact([f"{k} {v}" for k, v in counts.most_common()]), f"- Books with intelligence requirements: {len(int_reqs)}", ""]
    lines += ["## Books", "", "| Item | Name | Value | Intelligence req | Merchandise | Unique | Notes |", "|---|---|---:|---:|---|---|---|"]
    for r in [r for r in special if item_type(int(r["flags"])) == itp_type_book or "book" in str(r["id"]).lower()]:
        notes = []
        if str(r["id"]) not in int_reqs:
            notes.append("no int req")
        lines.append(f"| `{md(r['id'])}` | {md(r['name'])} | {r['value']} | {int_reqs.get(str(r['id']), 0)} | {r['merchandise']} | {r['unique']} | {compact(notes)} |")
    lines += ["", "## Special Gear and Artifacts", "", "| Item | Name | Type | Score | Value | Merchandise | Unique | Troop uses |", "|---|---|---|---:|---:|---|---|---:|"]
    for r in sorted([r for r in special if item_type(int(r["flags"])) != itp_type_book], key=lambda r: int(r["score"]), reverse=True):
        lines.append(f"| `{md(r['id'])}` | {md(r['name'])} | {r['type']} | {r['score']} | {r['value']} | {r['merchandise']} | {r['unique']} | {r['troop_uses']} |")
    write(REPORTS["special"], lines)


def main() -> None:
    rows = all_item_rows()
    audit_ammo(rows)
    audit_loadouts(rows)
    audit_value(rows)
    audit_imod(rows)
    audit_goods(rows)
    audit_special(rows)
    print("generated item system audits:")
    for path in REPORTS.values():
        print(f"  {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
