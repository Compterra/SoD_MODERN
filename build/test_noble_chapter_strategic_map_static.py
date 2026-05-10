from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_noble_gather_target_can_use_player_realm_chapters_not_only_personal_fiefs():
    text = read("src/scripts/ZY_helper_scripts/update_nobles_gather_at.py")
    assert '(store_faction_of_party, ":center_faction", ":center_no")' in text
    assert '(eq, ":center_faction", "fac_player_supporters_faction")' in text
    assert '(party_slot_eq, ":center_no", slot_town_lord, "trp_player")' not in text
    assert '(val_add, ":score", 50)' in text


def test_daily_noble_generation_requires_valid_gather_target():
    text = read("src/triggers/ST03_daily/entry_0107.py")
    assert '(gt, "$g_sod_nobles_gather_at", 0)' in text
    assert '(party_add_members, "$g_sod_nobles_gather_at", ":nobles_id", ":nobles")' in text


def test_marshal_noble_destination_picker_uses_realm_chapters():
    text = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_repeat_for_parties_marshal_nobles_choose.py")
    assert '(store_faction_of_party, ":center_faction", ":center_no")' in text
    assert '(eq, ":center_faction", "fac_player_supporters_faction")' in text
    assert '(party_slot_eq, ":center_no", slot_town_lord, "trp_player")' not in text


def test_strategic_map_lord_list_is_paged():
    text = read("src/presentations/0016_strategic_map/strategic_map.py")
    assert "$sod_sm_lord_page" in text
    assert "$sod_sm_lord_prev_page_button" in text
    assert "$sod_sm_lord_next_page_button" in text
    assert '(store_mul, ":lord_page_offset", "$sod_sm_lord_page", 20)' in text
    assert '(is_between, ":lord_index", ":lord_page_offset", ":lord_page_end")' in text
    assert '(troop_set_slot, "trp_sm_lords", ":lord_button_index", ":cur_lord")' in text
