from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_lord_faction_change_trigger_filters_invalid_or_stale_defection_slots() -> None:
    raw = read("src/triggers/ST02_every_hour/entry_0087.py")
    assert '(troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1)' in raw
    assert '(this_or_next|neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero)' in raw
    assert '(this_or_next|neg|is_between, ":faction_no", kingdoms_begin, rebel_factions_end)' in raw
    assert '(neg|is_between, ":new_faction_no", kingdoms_begin, rebel_factions_end)' in raw
    assert '(troop_set_slot, ":troop_no", slot_troop_change_to_faction, 0)' in raw


def test_lord_faction_change_message_is_after_living_lord_filter() -> None:
    raw = read("src/triggers/ST02_every_hour/entry_0087.py")
    filter_idx = raw.find("slto_kingdom_hero")
    message_idx = raw.find("has switched from")
    assert filter_idx >= 0
    assert message_idx > filter_idx
    assert '(call_script, "script_store_troop_name_link", s1, ":troop_no")' in raw[filter_idx:message_idx]
