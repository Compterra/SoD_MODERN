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

from audit_non_hero_troops import build_rows, compact_list, md_escape, parse_upgrades  # type: ignore
from audit_troop_equipment_tier_fit import build_fit_rows, is_speed_noncombat  # type: ignore


REPORT_DIR = ROOT / "docs" / "reports"
UPGRADE_OUT = REPORT_DIR / "upgrade_path_smoothness_audit.md"
ROLE_OUT = REPORT_DIR / "troop_role_consistency_audit.md"
DOCTRINE_OUT = REPORT_DIR / "faction_doctrine_comparison_audit.md"
KT0_OUT = REPORT_DIR / "kt0_vs_equipment_audit.md"


def row_indexes() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]], dict[str, list[str]]]:
    troop_rows, _excluded = build_rows()
    fit_rows = build_fit_rows()
    rows_by_id = {str(row["id"]): row for row in troop_rows}
    fit_by_id = {str(row["troop"]): row for row in fit_rows}
    return rows_by_id, fit_by_id, parse_upgrades()


def equipment_variant_base(troop_id: str, rows_by_id: dict[str, dict[str, object]]) -> str:
    if troop_id.endswith("1") and troop_id[:-1] in rows_by_id:
        return troop_id[:-1]
    return troop_id


def upgrade_edges(rows_by_id: dict[str, dict[str, object]], upgrades: dict[str, list[str]]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for parent, children in upgrades.items():
        parent_id = equipment_variant_base(parent, rows_by_id)
        if parent_id not in rows_by_id:
            continue
        for child in children:
            child_id = equipment_variant_base(child, rows_by_id)
            if child_id in rows_by_id:
                edges.append((parent_id, child_id))
    return sorted(set(edges))


def edge_notes(parent: dict[str, object], child: dict[str, object], parent_fit: dict[str, object], child_fit: dict[str, object]) -> list[str]:
    notes: list[str] = []
    level_delta = int(child["level"]) - int(parent["level"])
    kit_delta = int(child_fit["kit"]) - int(parent_fit["kit"])
    kt0_delta = int(child["kt0"]["open"]) - int(parent["kt0"]["open"])  # type: ignore[index]
    if level_delta < 0:
        notes.append("level drops")
    if level_delta > 12:
        notes.append("large level jump")
    if kit_delta < -35:
        notes.append("kit drops")
    elif kit_delta > 220:
        notes.append("large kit jump")
    if kt0_delta < -15:
        notes.append("KT0 drops")
    elif kt0_delta > 55:
        notes.append("large KT0 jump")
    if str(parent["role"]) != str(child["role"]):
        notes.append(f"role shift {parent['role']} -> {child['role']}")
    return notes


def write_upgrade_smoothness(rows_by_id: dict[str, dict[str, object]], fit_by_id: dict[str, dict[str, object]], upgrades: dict[str, list[str]]) -> None:
    rows: list[dict[str, object]] = []
    for parent_id, child_id in upgrade_edges(rows_by_id, upgrades):
        parent = rows_by_id[parent_id]
        child = rows_by_id[child_id]
        parent_fit = fit_by_id.get(parent_id)
        child_fit = fit_by_id.get(child_id)
        if not parent_fit or not child_fit:
            continue
        notes = edge_notes(parent, child, parent_fit, child_fit)
        rows.append(
            {
                "parent": parent_id,
                "child": child_id,
                "faction": child["faction_id"],
                "parent_level": parent["level"],
                "child_level": child["level"],
                "level_delta": int(child["level"]) - int(parent["level"]),
                "parent_kit": parent_fit["kit"],
                "child_kit": child_fit["kit"],
                "kit_delta": int(child_fit["kit"]) - int(parent_fit["kit"]),
                "parent_kt0": parent["kt0"]["open"],  # type: ignore[index]
                "child_kt0": child["kt0"]["open"],  # type: ignore[index]
                "kt0_delta": int(child["kt0"]["open"]) - int(parent["kt0"]["open"]),  # type: ignore[index]
                "parent_role": parent["role"],
                "child_role": child["role"],
                "notes": notes,
            }
        )
    flagged = [row for row in rows if row["notes"]]
    lines = [
        "# Upgrade Path Smoothness Audit",
        "",
        "This report checks whether upgrade edges improve smoothly in level, equipment kit score, KT0 open-field strength, and battlefield role.",
        "",
        "## Summary",
        "",
        f"- Upgrade edges audited: {len(rows)}",
        f"- Edges with balance notes: {len(flagged)}",
        f"- Kit drops: {sum(1 for row in flagged if 'kit drops' in row['notes'])}",
        f"- KT0 drops: {sum(1 for row in flagged if 'KT0 drops' in row['notes'])}",
        f"- Large jumps: {sum(1 for row in flagged if any('large' in note for note in row['notes']))}",
        "",
        "## Flagged Edges",
        "",
        "| Faction | From | To | Lvl | Kit | KT0 open | Role | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in sorted(flagged, key=lambda item: (len(item["notes"]), abs(int(item["kit_delta"]))), reverse=True):
        lines.append(
            f"| {md_escape(row['faction'])} | `{md_escape(row['parent'])}` | `{md_escape(row['child'])}` | "
            f"{row['parent_level']} -> {row['child_level']} ({row['level_delta']:+}) | "
            f"{row['parent_kit']} -> {row['child_kit']} ({row['kit_delta']:+}) | "
            f"{row['parent_kt0']} -> {row['child_kt0']} ({row['kt0_delta']:+}) | "
            f"{md_escape(row['parent_role'])} -> {md_escape(row['child_role'])} | {compact_list(row['notes'])} |"
        )
    lines += [
        "",
        "## All Edges",
        "",
        "| Faction | From | To | Lvl delta | Kit delta | KT0 delta | Role shift | Notes |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        role_shift = "-" if row["parent_role"] == row["child_role"] else f"{row['parent_role']} -> {row['child_role']}"
        lines.append(
            f"| {md_escape(row['faction'])} | `{md_escape(row['parent'])}` | `{md_escape(row['child'])}` | "
            f"{row['level_delta']} | {row['kit_delta']} | {row['kt0_delta']} | {md_escape(role_shift)} | {compact_list(row['notes'])} |"
        )
    UPGRADE_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def role_notes(row: dict[str, object], fit: dict[str, object]) -> list[str]:
    troop_id = str(row["id"])
    role = str(row["role"])
    gear = set(row["gear"])  # type: ignore[arg-type]
    flags = set(row["flag_tags"])  # type: ignore[arg-type]
    notes: list[str] = []
    if is_speed_noncombat(troop_id):
        return ["support/noncombat role; combat kit intentionally secondary"]
    if role in {"Cavalry", "Mounted ranged"} and "g_horse" not in flags and "tf_mounted" not in flags:
        notes.append("mounted role lacks horse guarantee")
    if "g_horse" in flags and int(fit["mount"]) == 0:
        notes.append("horse guaranteed but no horse item")
    if "g_shield" in flags and int(fit["shield"]) == 0:
        notes.append("shield guaranteed but no shield item")
    if role == "Archer" and not ({"Bow", "Arrows"} & gear):
        notes.append("archer role lacks bow or arrows")
    if role == "Mounted ranged" and not ({"Bow", "Arrows", "Xbow", "Bolts", "Throw"} & gear):
        notes.append("mounted ranged role lacks ranged weapon")
    if role == "Crossbow" and not ({"Xbow", "Bolts"} & gear):
        notes.append("crossbow role lacks crossbow or bolts")
    if role == "Skirmisher" and "Throw" not in gear:
        notes.append("skirmisher role lacks thrown weapon")
    if role == "Infantry" and "g_shield" in flags and int(fit["shield"]) < 55:
        notes.append("shield infantry has weak shield profile")
    if int(fit["mount"]) > 0 and role not in {"Cavalry", "Mounted ranged"}:
        notes.append("mount present on non-mounted role")
    if "Throw" in gear and role == "Archer":
        notes.append("bow role also carries thrown weapons; ensure doctrine is intentional")
    return notes


def write_role_consistency(rows_by_id: dict[str, dict[str, object]], fit_by_id: dict[str, dict[str, object]]) -> None:
    rows = []
    for troop_id, row in rows_by_id.items():
        fit = fit_by_id.get(troop_id)
        if not fit:
            continue
        notes = role_notes(row, fit)
        rows.append({"id": troop_id, "row": row, "fit": fit, "notes": notes})
    flagged = [row for row in rows if row["notes"] and "support/noncombat role; combat kit intentionally secondary" not in row["notes"]]
    support = [row for row in rows if row["notes"] == ["support/noncombat role; combat kit intentionally secondary"]]
    lines = [
        "# Troop Role Consistency Audit",
        "",
        "This report checks whether troop flags, equipment guarantees, and detected battlefield roles agree.",
        "",
        "## Summary",
        "",
        f"- Troops audited: {len(rows)}",
        f"- Role consistency flags: {len(flagged)}",
        f"- Support/noncombat exceptions: {len(support)}",
        "",
        "## Flagged Roles",
        "",
        "| Faction | Troop | Lvl | Role | Gear | Flags | Kit | Notes |",
        "|---|---|---:|---|---|---|---:|---|",
    ]
    for item in flagged:
        row = item["row"]
        fit = item["fit"]
        lines.append(
            f"| {md_escape(row['faction_id'])} | `{md_escape(item['id'])}` | {row['level']} | {md_escape(row['role'])} | "
            f"{compact_list(row['gear'])} | {compact_list(row['flag_tags'])} | {fit['kit']} | {compact_list(item['notes'])} |"
        )
    lines += [
        "",
        "## Support Exceptions",
        "",
        "| Troop | Faction | Role | Note |",
        "|---|---|---|---|",
    ]
    for item in support:
        row = item["row"]
        lines.append(f"| `{md_escape(item['id'])}` | {md_escape(row['faction_id'])} | {md_escape(row['role'])} | {compact_list(item['notes'])} |")
    ROLE_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def average(values: list[int]) -> float:
    return statistics.mean(values) if values else 0.0


def write_faction_doctrine(rows_by_id: dict[str, dict[str, object]], fit_by_id: dict[str, dict[str, object]]) -> None:
    by_faction: dict[str, list[dict[str, object]]] = defaultdict(list)
    for troop_id, row in rows_by_id.items():
        fit = fit_by_id.get(troop_id)
        if fit:
            merged = dict(row)
            merged.update({f"fit_{key}": value for key, value in fit.items()})
            by_faction[str(row["faction_id"])].append(merged)
    lines = [
        "# Faction Doctrine Comparison Audit",
        "",
        "This report compares faction troop identities using role mix, equipment score components, and KT0 open-field strength.",
        "",
        "## Faction Summary",
        "",
        "| Faction | Troops | Top roles | Avg lvl | Avg kit | Avg melee | Avg ranged | Avg armor | Avg shield | Avg mount | Avg KT0 open | Doctrine notes |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for faction, rows in sorted(by_faction.items()):
        roles = Counter(str(row["role"]) for row in rows)
        avg_kit = average([int(row["fit_kit"]) for row in rows])
        avg_melee = average([int(row["fit_melee"]) for row in rows])
        avg_ranged = average([int(row["fit_ranged"]) for row in rows])
        avg_armor = average([int(row["fit_armor"]) for row in rows])
        avg_shield = average([int(row["fit_shield"]) for row in rows])
        avg_mount = average([int(row["fit_mount"]) for row in rows])
        avg_kt0 = average([int(row["kt0"]["open"]) for row in rows])  # type: ignore[index]
        notes = []
        if avg_ranged > avg_melee * 0.9:
            notes.append("ranged-forward")
        if avg_mount > 55:
            notes.append("mobile/mounted emphasis")
        if avg_shield > 65 and avg_armor > 150:
            notes.append("defensive line")
        if avg_kt0 > 95:
            notes.append("high autoresolve pressure")
        if faction.startswith("sod_merc_guild"):
            notes.append("mini-faction doctrine; compare to contract role")
        lines.append(
            f"| {md_escape(faction)} | {len(rows)} | {compact_list([f'{role} {count}' for role, count in roles.most_common(3)])} | "
            f"{average([int(row['level']) for row in rows]):.1f} | {avg_kit:.1f} | {avg_melee:.1f} | {avg_ranged:.1f} | "
            f"{avg_armor:.1f} | {avg_shield:.1f} | {avg_mount:.1f} | {avg_kt0:.1f} | {compact_list(notes)} |"
        )
    lines += [
        "",
        "## Watch Groups",
        "",
        "- Player culture lines should keep distinct doctrine while staying inside tier-fit bands.",
        "- Faith and Imperial troops may exceed normal faction averages, but their advantage should be visible here and in KT0 audits.",
        "- Mercenary mini-factions should express contract identity without looking like full kingdom rosters.",
    ]
    DOCTRINE_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def kt0_notes(row: dict[str, object], fit: dict[str, object]) -> list[str]:
    kt0 = row["kt0"]  # type: ignore[assignment]
    notes: list[str] = []
    kit = int(fit["kit"])
    open_value = int(kt0["open"])
    if kit >= 500 and open_value < 65:
        notes.append("high kit but low KT0")
    if kit <= 220 and open_value > 95:
        notes.append("low kit but high KT0")
    if int(fit["mount"]) > 0 and kt0["type"] not in {"Cavalry", "Mounted ranged"}:
        notes.append("mount not reflected in KT0 type")
    if str(row["role"]) in {"Archer", "Crossbow", "Mounted ranged"} and int(fit["ranged"]) > 0 and kt0["type"] not in {"Archer", "Mounted ranged"}:
        notes.append("ranged role not reflected in KT0 type")
    warnings = kt0.get("warnings", [])
    notes.extend(str(warning) for warning in warnings)
    return notes


def write_kt0_vs_equipment(rows_by_id: dict[str, dict[str, object]], fit_by_id: dict[str, dict[str, object]]) -> None:
    rows = []
    for troop_id, row in rows_by_id.items():
        fit = fit_by_id.get(troop_id)
        if not fit:
            continue
        notes = kt0_notes(row, fit)
        rows.append({"id": troop_id, "row": row, "fit": fit, "notes": notes})
    flagged = [row for row in rows if row["notes"]]
    lines = [
        "# KT0 vs Equipment Audit",
        "",
        "This report compares KT0 autoresolve classification and open-field strength against actual equipment kit scores.",
        "",
        "## Summary",
        "",
        f"- Troops audited: {len(rows)}",
        f"- KT0/equipment flags: {len(flagged)}",
        "",
        "## Flagged KT0 Rows",
        "",
        "| Faction | Troop | Role | KT0 type | Kit | Melee | Ranged | Armor | Shield | Mount | KT0 O/D/H/Open | Notes |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for item in sorted(flagged, key=lambda value: (len(value["notes"]), int(value["fit"]["kit"])), reverse=True):
        row = item["row"]
        fit = item["fit"]
        kt0 = row["kt0"]
        lines.append(
            f"| {md_escape(row['faction_id'])} | `{md_escape(item['id'])}` | {md_escape(row['role'])} | {md_escape(kt0['type'])} | "
            f"{fit['kit']} | {fit['melee']} | {fit['ranged']} | {fit['armor']} | {fit['shield']} | {fit['mount']} | "
            f"O{kt0['offense']}/D{kt0['defense']}/H{kt0['horse']}/F{kt0['open']} | {compact_list(item['notes'])} |"
        )
    KT0_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows_by_id, fit_by_id, upgrades = row_indexes()
    write_upgrade_smoothness(rows_by_id, fit_by_id, upgrades)
    write_role_consistency(rows_by_id, fit_by_id)
    write_faction_doctrine(rows_by_id, fit_by_id)
    write_kt0_vs_equipment(rows_by_id, fit_by_id)
    for path in [UPGRADE_OUT, ROLE_OUT, DOCTRINE_OUT, KT0_OUT]:
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
