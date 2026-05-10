from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))

import rebalance_item_prices as rebalance  # type: ignore
from header_items import (  # type: ignore
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
)
import module_items  # type: ignore


OUT_PATH = COMPILE / "module_items.py"


def replacement_value(item: tuple, groups: set[str]) -> tuple[int, int] | None:
    item_id, item_name, meshes, flags, capabilities, value, stats, imodbits = item[:8]
    if not (flags & rebalance.itp_merchandise):
        return None
    group = rebalance.item_group_from_flags(flags)
    if group == "Other" or group not in groups:
        return None
    fake = rebalance.ItemKind(
        line_index=0,
        item_id="itm_" + item_id,
        name=item_name,
        plural=item_name,
        mesh_count=len(meshes),
        flags=flags,
        capabilities=capabilities,
        value=value,
        imodbits=imodbits,
        weight=0,
        abundance=0,
        head=get_head_armor(stats),
        body=get_body_armor(stats),
        leg=get_leg_armor(stats),
        difficulty=get_difficulty(stats),
        hit_points=get_hit_points(stats),
        speed=get_speed_rating(stats),
        missile_speed=get_missile_speed(stats),
        length=get_weapon_length(stats),
        ammo=get_max_ammo(stats),
        thrust=get_thrust_damage(stats),
        swing=get_swing_damage(stats),
        tokens=[],
        value_token_index=0,
    )
    score = rebalance.score_item(fake)
    proposed = rebalance.target_value(fake, score)
    if proposed is None:
        return None
    return score, rebalance.clamp_change(value, proposed)


def apply_prices(text: str, groups: set[str]) -> tuple[str, list[tuple[str, int, int, int, str]]]:
    changes: list[tuple[str, int, int, int, str]] = []
    for item in module_items.items:
        result = replacement_value(item, groups)
        if result is None:
            continue
        score, new_value = result
        item_id = item[0]
        old_value = item[5]
        if new_value == old_value:
            continue
        pattern = re.compile(
            r'(\[\s*"'
            + re.escape(item_id)
            + r'"\s*,.*?,\s*)(-?\d+)(\s*,\s*(?:abundance|hit_points|body_armor|difficulty|horse_speed|weight)\()',
            re.S,
        )
        match = pattern.search(text)
        if not match:
            raise RuntimeError(f"could not locate value field for {item_id}")
        text = text[: match.start(2)] + str(new_value) + text[match.end(2) :]
        changes.append((item_id, old_value, new_value, score, rebalance.item_group_from_flags(item[3])))
    return text, changes


def parse_groups(value: str) -> set[str]:
    if value.strip().lower() == "all":
        return {"Armor", "Melee", "Mount", "Ranged", "Shield"}
    return {group.strip() for group in value.split(",") if group.strip()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply formula prices directly to compile/module_items.py.")
    parser.add_argument("--groups", default="Mount", help="Comma-separated groups: Mount, Armor, Shield, Melee, Ranged, or all.")
    args = parser.parse_args(argv)
    groups = parse_groups(args.groups)
    text = OUT_PATH.read_text(encoding="utf-8")
    new_text, changes = apply_prices(text, groups)
    OUT_PATH.write_text(new_text, encoding="utf-8")
    print(f"updated {len(changes)} buyable item values for {','.join(sorted(groups))} in {OUT_PATH.relative_to(ROOT)}")
    for item_id, old_value, new_value, score, group in changes:
        print(f"{item_id}: {old_value} -> {new_value} ({group}, score {score})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
