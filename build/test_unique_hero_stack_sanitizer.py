# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def require(raw: str, token: str) -> None:
    if token not in raw:
        raise AssertionError(f"Missing expected token: {token}")


def main() -> int:
    script = read("src/scripts/ZC_parties/sod_sanitize_unique_hero_party_stacks.py")
    require(script, '"sod_sanitize_unique_hero_party_stacks"')
    require(script, '(eq, ":stack_troop", "trp_player")')
    require(script, '(neq, ":party_no", "p_main_party")')
    require(script, '(is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end)')
    require(script, '(troop_slot_eq, ":stack_troop", slot_troop_leaded_party, ":party_no")')
    require(script, '(party_remove_members, ":party_no", ":stack_troop", ":stack_size")')

    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    require(trigger_order, "ST02_every_hour/entry_0163.py")
    trigger = read("src/triggers/ST02_every_hour/entry_0163.py")
    require(trigger, '(call_script, "script_sod_sanitize_unique_hero_party_stacks")')

    camp = read("src/menus/camp/camp_action.py")
    require(camp, '("fix_dups", [(eq, "$g_sod_debug", 1), (eq, "$g_fix_dup_troops", 0)]')

    print("[unique_hero_stack_sanitizer] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
