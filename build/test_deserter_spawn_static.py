# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_before(raw: str, first: str, second: str) -> None:
    assert first in raw, f"missing token: {first}"
    assert second in raw, f"missing token: {second}"
    assert raw.index(first) < raw.index(second), f"{first} should appear before {second}"


def test_old_lord_deserter_spawn_uses_real_available_troops() -> None:
    raw = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    assert_contains(raw, '(spawn_around_party, ":party_no", "pt_deserters")')
    assert_contains(raw, '(party_count_members_of_type, ":available_tier_1", ":party_no", ":tier_1_troop")')
    assert_contains(raw, '(gt, ":available_tier_1", 0)')
    assert_contains(raw, '(val_min, ":number_to_add", ":available_tier_1")')
    assert_contains(raw, '(gt, ":number_to_add", 0)')
    assert_before(raw, '(party_count_members_of_type, ":available_tier_1"', '(spawn_around_party, ":party_no", "pt_deserters")')
    assert_before(raw, '(party_remove_members, ":party_no", ":tier_1_troop", ":number_to_add")', '(party_add_members, ":new_party", ":tier_1_troop", ":number_to_add")')


def test_new_lord_and_player_deserter_spawns_clear_and_fill_party() -> None:
    morale = read("src/scripts/ZY_helper_scripts/sod_lord_party_morale.py")
    company = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    for raw in (morale, company):
        assert_contains(raw, '(spawn_around_party')
        assert_contains(raw, '(party_clear, ":deserter_party")')
        assert_contains(raw, '(party_remove_members')
        assert_contains(raw, '(party_add_members, ":deserter_party"')


if __name__ == "__main__":
    test_old_lord_deserter_spawn_uses_real_available_troops()
    test_new_lord_and_player_deserter_spawns_clear_and_fill_party()
    print("test_deserter_spawn_static: OK")
