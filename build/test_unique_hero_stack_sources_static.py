from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mercenary_lord_spawn_uses_leader_stack():
    text = read("src/triggers/ST03_daily/entry_0129.py")
    assert '(party_add_leader, ":merc_lord_party", ":troop_no")' in text
    assert '(party_add_members, ":merc_lord_party", ":troop_no", 1)' not in text


def test_attached_party_troop_transfer_rejects_heroes():
    text = read("src/triggers/ST02_every_hour/entry_0142.py")
    troop_read = '(party_stack_get_troop_id, ":troop_id", ":attached_to", ":stack_no")'
    hero_guard = '(neg|troop_is_hero, ":troop_id")'
    add_members = '(party_add_members, ":kingdom_hero_party", ":troop_id", ":transfer")'
    assert troop_read in text
    assert hero_guard in text
    assert text.index(troop_read) < text.index(hero_guard) < text.index(add_members)


def test_prisoner_rescue_helper_never_turns_heroes_into_members():
    text = read("src/scripts/ZC_parties/party_add_party_prisoners.py")
    assert '(neg|troop_is_hero, ":stack_troop")' in text
    assert '(eq, "$g_move_heroes", 1)' not in text
    assert '(party_add_members, ":target_party", ":stack_troop", ":stack_size")' in text


def test_kingdom_hero_party_creation_rejects_invalid_unique_troops():
    text = read("src/scripts/ZC_parties/create_kingdom_hero_party.py")
    assert '(assign, "$pout_party", -1)' in text
    assert '(is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end)' in text
    assert '(neq, ":troop_no", "trp_player")' in text
    assert '(neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1)' in text
    assert '(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0)' in text


def test_ratio_member_transfer_rejects_heroes():
    text = read("src/scripts/ZZ_common_array_processing/move_members_with_ratio.py")
    troop_read = '(party_stack_get_troop_id,     ":stack_troop", ":source_party", ":stack_no")'
    hero_guard = '(neg|troop_is_hero, ":stack_troop")'
    add_members = '(party_add_members, ":target_party", ":stack_troop", ":number_moved")'
    assert text.index(troop_read) < text.index(hero_guard) < text.index(add_members)
