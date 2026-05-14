from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_store_troop_name_link_handles_invalid_troop_ids() -> None:
    raw = read("src/scripts/ZH_heroes/store_troop_name_link.py")
    assert '(neg|is_between, ":troop", 0, "trp_last_troop")' in raw
    assert '@that commander' in raw
    assert '@an unknown commander' not in raw


def test_lord_defeat_comments_require_valid_troop_object() -> None:
    raw = read("src/scripts/ZJ_notes_and_information/get_relevant_comment_for_log_entry.py")
    assert '(eq, ":entry_type", logent_lord_defeated_by_player)' in raw
    assert '(neg|is_between, ":troop_object", heroes_begin, heroes_end)' in raw
    assert '(assign, ":entry_type", -1)' in raw
    assert '(troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":log_entry_no")' in raw
    assert '(troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":log_entry_no")' in raw
    assert '##     (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":log_entry_no")' not in raw
    helper = read("src/scripts/ZY_helper_scripts/get_relevant_comment_to_s42.py")
    assert '(str_store_string, s54, "@that commander")' in helper
    assert '(is_between, ":troop_object", heroes_begin, heroes_end)' in helper


def test_hostile_merc_attacker_dialog_handles_missing_boss() -> None:
    raw = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_party_encounter_mercs_hostile_attacker.py")
    assert '(party_get_slot, ":troop", ":cur_party", slot_party_boss)' in raw
    assert '(is_between, ":troop", 0, "trp_last_troop")' in raw
    assert '@Our paymaster' in raw


def test_nearby_party_join_reads_party_type_slot_explicitly() -> None:
    raw = read("src/scripts/ZB_economy_and_trade/let_nearby_parties_join_current_battle.py")
    assert '(party_get_slot, ":party_type", ":party_no", slot_party_type)' in raw
    assert '(party_get_slot, ":party_type", ":party_no"),' not in raw
