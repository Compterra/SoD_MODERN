from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "compile" / "module_items.py"


def read_items() -> str:
    return ITEMS.read_text(encoding="utf-8")


def item_block(text: str, item_id: str) -> str:
    pattern = re.compile(rf'\["{re.escape(item_id)}",.*?\],', re.S)
    match = pattern.search(text)
    assert match, f"missing item {item_id}"
    return match.group(0)


def assert_stat(block: str, stat: str, value: int) -> None:
    assert f"{stat}({value}" in block, f"expected {stat}({value}) in:\n{block}"


def test_crossbow_damage_and_range_floor() -> None:
    text = read_items()
    expected = {
        "hunting_crossbow": {"shoot_speed": 65, "thrust_damage": 32},
        "light_crossbow": {"shoot_speed": 78, "thrust_damage": 42},
        "crossbow": {"shoot_speed": 88, "thrust_damage": 48},
        "heavy_crossbow": {"shoot_speed": 96, "thrust_damage": 58},
        "sniper_crossbow": {"shoot_speed": 104, "thrust_damage": 64},
    }
    for item_id, stats in expected.items():
        block = item_block(text, item_id)
        assert_stat(block, "shoot_speed", stats["shoot_speed"])
        assert_stat(block, "thrust_damage", stats["thrust_damage"])


def test_bolts_have_meaningful_piercing_bonus() -> None:
    text = read_items()
    expected = {
        "bolts": 4,
        "steel_bolts": 7,
        "blacksmith_marinian_bolt": 10,
    }
    for item_id, damage in expected.items():
        block = item_block(text, item_id)
        assert_stat(block, "thrust_damage", damage)


def test_marinian_artifact_stays_above_shop_crossbows() -> None:
    text = read_items()
    widowmaker = item_block(text, "blacksmith_marinian_crossbow")
    assert_stat(widowmaker, "shoot_speed", 120)
    assert_stat(widowmaker, "thrust_damage", 72)
