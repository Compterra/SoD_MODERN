from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZF_factions" / "player_join_faction.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected player join faction behavior: {needle}"


def assert_absent(source: str, needle: str) -> None:
    assert needle not in source, f"stale player join faction block remains: {needle}"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert_contains(source, '("player_join_faction",')
    assert_contains(source, '(assign, "$players_kingdom", ":faction_no")')
    assert_contains(source, '(faction_set_slot, "fac_player_supporters_faction", slot_faction_ai_state, sfai_default)')
    assert_contains(source, '(assign, "$players_oath_renounced_against_kingdom", 0)')
    assert_contains(source, '(call_script, "script_set_player_relation_with_faction", ":other_kingdom", ":other_kingdom_reln")')
    assert_contains(source, '(party_set_faction, ":cur_center", ":faction_no")')
    assert_contains(source, '(call_script, "script_abort_quest", ":quest_no", 0)')
    assert_contains(source, '(faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive)')
    assert_contains(source, '(call_script, "script_update_all_notes")')
    assert_contains(source, '(assign, "$g_recalculate_ais", 1)')

    assert_absent(source, '":kingdom_hero_faction"')
    assert_absent(source, 'script_change_troop_faction", ":kingdom_hero", ":faction_no"')
    assert_absent(source, '(try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end)')

    print("test_player_join_faction_static: OK")


if __name__ == "__main__":
    main()
