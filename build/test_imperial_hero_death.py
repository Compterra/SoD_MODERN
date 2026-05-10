# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    raw = read("src/scripts/ZE_encounters/cf_check_hero_can_die_in_battle.py")

    assert_contains(raw, '"cf_check_hero_can_die_in_battle"')
    assert_contains(raw, '(eq, ":faction", "fac_kingdom_6")')
    assert_contains(raw, '":living_imperial_vassals"')
    assert_contains(raw, '(neq, ":cur_troop", ":troop_no")')
    assert_contains(raw, '(eq, ":cur_faction", "fac_kingdom_6")')
    assert_contains(raw, '(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero)')
    assert_contains(raw, '(eq, ":living_imperial_vassals", 0)')
    assert_contains(raw, 'king_death_after_defeat_chance')
    assert_contains(raw, 'hero_death_after_defeat_chance')
    expedition = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    assert_contains(expedition, '"sod_imperial_expedition_count_living_vassals"')
    assert_contains(expedition, "living Centurions")
    assert_contains(expedition, "Gaius Marius cannot be slain while any Centurion command remains alive")

    if '(eq, ":troop_no", "trp_kingdom_6_lord")' in raw and '(assign, ":chance", 0)' in raw:
        raise AssertionError("Imperial ruler is still hard-coded as unkillable.")

    print("[imperial_hero_death] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
