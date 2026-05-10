# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_order(raw: str, first: str, second: str) -> None:
    first_at = raw.find(first)
    second_at = raw.find(second)
    if first_at < 0:
        raise AssertionError(f"Missing expected token: {first}")
    if second_at < 0:
        raise AssertionError(f"Missing expected token: {second}")
    if first_at >= second_at:
        raise AssertionError(f"Expected {first!r} before {second!r}")


def main() -> int:
    raw = read("src/scripts/ZC_parties/total_victory_try_enemy_hero_resolution.py")

    assert_order(
        raw,
        '(call_script, "script_kill_kingdom_hero", ":stack_troop")',
        '(jump_to_menu, "mnu_enemy_slipped_away")',
    )
    after_kill = raw.split('(call_script, "script_kill_kingdom_hero", ":stack_troop")', 1)[1]
    before_popup = after_kill.split('(jump_to_menu, "mnu_enemy_slipped_away")', 1)[0]

    expected = [
        '(call_script, "script_store_troop_name", s1, ":stack_troop")',
        '(str_store_faction_name, s3, ":defeated_faction")',
        '(str_store_string, s17, "@{s1} of {s3} has died in battle.")',
    ]
    for token in expected:
        if token not in before_popup:
            raise AssertionError(f"Death popup text is not restored after kill script: {token}")

    print("[hero_death_popup_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
