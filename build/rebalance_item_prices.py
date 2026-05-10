from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))

from header_items import (  # type: ignore
    itp_merchandise,
    itp_type_arrows,
    itp_type_body_armor,
    itp_type_bolts,
    itp_type_bow,
    itp_type_crossbow,
    itp_type_foot_armor,
    itp_type_hand_armor,
    itp_type_head_armor,
    itp_type_horse,
    itp_type_one_handed_wpn,
    itp_type_polearm,
    itp_type_shield,
    itp_type_thrown,
    itp_type_two_handed_wpn,
)


DEFAULT_ITEM_KINDS = ROOT / "_export" / "item_kinds1.txt"
DEFAULT_REPORT = ROOT / "docs" / "reports" / "generated_item_price_rebalance.md"


@dataclass
class ItemKind:
    line_index: int
    item_id: str
    name: str
    plural: str
    mesh_count: int
    flags: int
    capabilities: int
    value: int
    imodbits: int
    weight: float
    abundance: int
    head: int
    body: int
    leg: int
    difficulty: int
    hit_points: int
    speed: int
    missile_speed: int
    length: int
    ammo: int
    thrust: int
    swing: int
    tokens: list[str]
    value_token_index: int

    @property
    def item_type(self) -> int:
        return self.flags & 0xFF

    @property
    def buyable(self) -> bool:
        return bool(self.flags & itp_merchandise)


def parse_item_line(line: str, line_index: int) -> ItemKind | None:
    stripped = line.strip()
    if not stripped.startswith("itm_"):
        return None
    tokens = stripped.split()
    if len(tokens) < 7:
        return None
    mesh_count = int(tokens[3])
    base = 4 + mesh_count * 2
    if len(tokens) < base + 17:
        return None
    value_index = base + 2
    return ItemKind(
        line_index=line_index,
        item_id=tokens[0],
        name=tokens[1],
        plural=tokens[2],
        mesh_count=mesh_count,
        flags=int(tokens[base]),
        capabilities=int(tokens[base + 1]),
        value=int(tokens[value_index]),
        imodbits=int(tokens[base + 3]),
        weight=float(tokens[base + 4]),
        abundance=int(tokens[base + 5]),
        head=int(tokens[base + 6]),
        body=int(tokens[base + 7]),
        leg=int(tokens[base + 8]),
        difficulty=int(tokens[base + 9]),
        hit_points=int(tokens[base + 10]),
        speed=int(tokens[base + 11]),
        missile_speed=int(tokens[base + 12]),
        length=int(tokens[base + 13]),
        ammo=int(tokens[base + 14]),
        thrust=int(tokens[base + 15]),
        swing=int(tokens[base + 16]),
        tokens=tokens,
        value_token_index=value_index,
    )


def item_group(item: ItemKind) -> str:
    return item_group_from_flags(item.flags)


def item_group_from_flags(flags: int) -> str:
    item_type = flags & 0xFF
    if item_type == itp_type_horse:
        return "Mount"
    if item_type in {itp_type_head_armor, itp_type_body_armor, itp_type_foot_armor, itp_type_hand_armor}:
        return "Armor"
    if item_type == itp_type_shield:
        return "Shield"
    if item_type in {itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm}:
        return "Melee"
    if item_type in {itp_type_bow, itp_type_crossbow, itp_type_thrown, itp_type_arrows, itp_type_bolts}:
        return "Ranged"
    return "Other"


def decoded_damage(raw: int) -> int:
    return raw & 0xFF


def score_item(item: ItemKind) -> int:
    item_type = item.item_type
    if item_type == itp_type_body_armor:
        return item.body + item.leg + item.head // 2
    if item_type == itp_type_head_armor:
        return item.head
    if item_type == itp_type_foot_armor:
        return item.leg
    if item_type == itp_type_hand_armor:
        return item.body
    if item_type == itp_type_horse:
        hp = item.hit_points or 100
        return item.speed + item.missile_speed + item.body + decoded_damage(item.thrust) * 2 + hp // 5
    if item_type == itp_type_shield:
        return item.length + item.body * 2 + item.hit_points // 10 + item.speed // 5
    if item_type in {itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm}:
        damage = max(decoded_damage(item.swing), decoded_damage(item.thrust))
        return int(round(damage * max(item.speed, 1) / 100 + item.length / 10))
    if item_type in {itp_type_bow, itp_type_crossbow, itp_type_thrown}:
        return decoded_damage(item.thrust) + item.missile_speed // 3 + item.ammo // 2
    if item_type in {itp_type_arrows, itp_type_bolts}:
        return decoded_damage(item.thrust) + item.ammo // 2
    return 0


def target_value(item: ItemKind, score: int) -> int | None:
    if not item.buyable:
        return None
    group = item_group(item)
    if group == "Armor":
        slot_factor = {
            itp_type_body_armor: 2.4,
            itp_type_head_armor: 1.35,
            itp_type_foot_armor: 1.15,
            itp_type_hand_armor: 18.0,
        }.get(item.item_type, 1.0)
        return max(5, int(score * score * slot_factor + item.difficulty * 90 + item.weight * 10))
    if group == "Mount":
        charge = decoded_damage(item.thrust)
        tier_bonus = 0
        if score >= 215 or item.difficulty >= 5:
            tier_bonus = 900
        elif score >= 190:
            tier_bonus = 550
        elif score >= 160:
            tier_bonus = 250
        elif score >= 135:
            tier_bonus = 90
        return max(50, int(score * score * 0.045 + item.difficulty * 115 + charge * 18 + tier_bonus))
    if group == "Shield":
        return max(20, int(score * score * 0.018 + item.body * 12 + item.difficulty * 50))
    if group == "Melee":
        return max(5, int(score * score * 0.55 + item.difficulty * 55 + item.weight * 12))
    if group == "Ranged":
        return max(4, int(score * score * 0.65 + item.difficulty * 70 + item.ammo * 2))
    return None


def clamp_change(current: int, target: int) -> int:
    if current <= 0:
        return target
    lower = max(1, int(current * 0.35))
    upper = max(lower, int(current * 3.0))
    return max(lower, min(upper, target))


def build_report(changes: list[tuple[ItemKind, int, int, int]], groups: set[str]) -> list[str]:
    lines = [
        "# Generated Item Price Rebalance",
        "",
        "Generated from post-Module-System `item_kinds1.txt`. Source `module_items.py` values are not edited by this process.",
        "",
        "Selected groups: " + ", ".join(sorted(groups)),
        "",
        "The proposed value is formula-based from generated stats. The applied value is clamped so one pass cannot move an existing price below 35% or above 300% of its generated value.",
        "",
        "## Summary",
        "",
        f"- Buyable equipment rows with proposed value changes: {len(changes)}",
        "",
    ]
    by_group: dict[str, list[tuple[ItemKind, int, int, int]]] = {}
    for change in changes:
        by_group.setdefault(item_group(change[0]), []).append(change)
    lines.extend(["| Group | Changes | Avg current | Avg proposed | Avg applied |", "|---|---:|---:|---:|---:|"])
    for group in sorted(by_group):
        subset = by_group[group]
        lines.append(
            f"| {group} | {len(subset)} | {sum(c[0].value for c in subset) / len(subset):.0f} | {sum(c[2] for c in subset) / len(subset):.0f} | {sum(c[3] for c in subset) / len(subset):.0f} |"
        )
    lines.extend(["", "## Largest Changes", "", "| Item | Group | Score | Current | Proposed | Applied | Delta |", "|---|---|---:|---:|---:|---:|---:|"])
    for item, score, proposed, applied in sorted(changes, key=lambda c: abs(c[3] - c[0].value), reverse=True)[:200]:
        lines.append(f"| `{item.item_id}` | {item_group(item)} | {score} | {item.value} | {proposed} | {applied} | {applied - item.value} |")
    return lines


def rewrite_item_file(path: Path, changes_by_line: dict[int, int]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_index, new_value in changes_by_line.items():
        item = parse_item_line(lines[line_index], line_index)
        if item is None:
            continue
        item.tokens[item.value_token_index] = str(new_value)
        lines[line_index] = " " + " ".join(item.tokens)
    backup = path.with_suffix(path.suffix + ".pre_price_rebalance")
    shutil.copy2(path, backup)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Post-process generated item_kinds1.txt equipment prices.")
    parser.add_argument("item_kinds", nargs="?", default=str(DEFAULT_ITEM_KINDS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--groups", default="Mount", help="Comma-separated item groups to rebalance: Mount, Armor, Shield, Melee, Ranged, or all.")
    parser.add_argument("--apply", action="store_true", help="Rewrite item_kinds1.txt. Without this, only the report is generated.")
    args = parser.parse_args(argv)
    if args.groups.strip().lower() == "all":
        groups = {"Armor", "Melee", "Mount", "Ranged", "Shield"}
    else:
        groups = {group.strip() for group in args.groups.split(",") if group.strip()}

    item_path = Path(args.item_kinds)
    if not item_path.exists():
        raise SystemExit(f"item_kinds1.txt not found: {item_path}")

    lines = item_path.read_text(encoding="utf-8").splitlines()
    changes: list[tuple[ItemKind, int, int, int]] = []
    for index, line in enumerate(lines):
        item = parse_item_line(line, index)
        if item is None or not item.buyable:
            continue
        group = item_group(item)
        if group == "Other" or group not in groups:
            continue
        score = score_item(item)
        proposed = target_value(item, score)
        if proposed is None:
            continue
        applied = clamp_change(item.value, proposed)
        if applied != item.value:
            changes.append((item, score, proposed, applied))

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(build_report(changes, groups)) + "\n", encoding="utf-8")

    if args.apply:
        rewrite_item_file(item_path, {item.line_index: applied for item, score, proposed, applied in changes})
        print(f"applied {len(changes)} item price changes to {item_path}")
    else:
        print(f"wrote price rebalance report for {len(changes)} proposed changes: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
