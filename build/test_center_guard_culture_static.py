from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    raw = read("src/menus/centers/castle/castle_castle.py")

    assert_contains(raw, '(store_faction_of_party, ":town_faction", "$current_town")')
    assert_contains(raw, '(faction_get_slot, ":troop_prison_guard", ":town_faction", slot_faction_prison_guard_troop)')
    assert_contains(raw, '(faction_get_slot, ":troop_castle_guard", ":town_faction", slot_faction_castle_guard_troop)')
    assert_contains(raw, '(faction_get_slot, ":guard_troop", ":town_faction", slot_faction_guard_troop)')
    assert_contains(raw, '(faction_get_slot, ":castle_guard_troop", ":town_faction", slot_faction_castle_guard_troop)')
    assert_contains(raw, '(assign, reg(0), ":castle_guard_troop")')
    assert_contains(raw, '(assign, reg(2), ":guard_troop")')
    assert_contains(raw, '(store_faction_of_party, ":castle_faction", "$current_town")')
    assert_contains(raw, '(faction_get_slot, ":troop_castle_guard", ":castle_faction", slot_faction_castle_guard_troop)')

    town_center_block = raw.split('("town_center"', 1)[1].split('("town_tavern"', 1)[0]
    if '(neq, ":town_faction", "fac_player_supporters_faction")' in town_center_block:
        raise AssertionError("Player-owned towns still skip current-faction guard visitors.")
    if '(faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop)' not in town_center_block:
        raise AssertionError("Town street troop selection no longer checks faction tier troops.")
    if '(gt, ":guard_troop", 0)' not in town_center_block:
        raise AssertionError("Town street troop selection lacks faction guard fallback.")

    castle_inspect_block = raw.split('("castle_inspect"', 1)[1].split('("upgrade"', 1)[0]
    if '(neq, "$g_encountered_party_faction", "fac_player_supporters_faction")' in castle_inspect_block:
        raise AssertionError("Player-owned castles still skip current-faction prison guard visitors.")

    print("[center_guard_culture_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

