# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRATEGIC_MAP = ROOT / "src" / "presentations" / "0016_strategic_map" / "strategic_map.py"


def read() -> str:
    return STRATEGIC_MAP.read_text(encoding="utf-8", errors="replace")


def assert_block_has(raw: str, start: str, end: str, tokens: list[str]) -> None:
    start_at = raw.find(start)
    if start_at < 0:
        raise AssertionError(f"Missing block start: {start}")
    end_at = raw.find(end, start_at + len(start))
    if end_at < 0:
        raise AssertionError(f"Missing block end after {start}: {end}")
    block = raw[start_at:end_at]
    for token in tokens:
        if token not in block:
            raise AssertionError(f"Missing {token!r} in block starting {start!r}")


def main() -> int:
    raw = read()

    guarded_order_tokens = [
        '(is_between, "$sod_sm_selected_lord", kingdom_heroes_begin, kingdom_heroes_end)',
        '(troop_get_slot, ":party", "$sod_sm_selected_lord", slot_troop_leaded_party)',
        '(party_is_active, ":party")',
    ]
    assert_block_has(
        raw,
        '(eq, ":object", "$resmod_tac_map_order_follow")',
        '(eq, ":object", "$resmod_tac_map_order_stop")',
        guarded_order_tokens,
    )
    assert_block_has(
        raw,
        '(eq, ":object", "$resmod_tac_map_order_stop")',
        '(eq, ":object", "$resmod_tac_map_order_go_button")',
        guarded_order_tokens,
    )
    assert_block_has(
        raw,
        '(is_between, ":object", "$sod_sm_center_buttons_begin", "$sod_sm_center_buttons_end")',
        '(is_between, ":object", "$sod_sm_lord_buttons_begin", "$sod_sm_lord_buttons_end")',
        guarded_order_tokens,
    )

    visual_tokens = [
        '(overlay_set_color, "$resmod_tac_map_order_follow", 0x777777)',
        '(overlay_set_color, "$resmod_tac_map_order_stop", 0x777777)',
    ]
    for token in visual_tokens:
        if token not in raw:
            raise AssertionError(f"Missing inactive-button visual guard: {token}")

    print("[strategic_map_order_guards] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
