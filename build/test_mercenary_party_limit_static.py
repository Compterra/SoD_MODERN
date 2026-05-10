from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


MERC_CAPTAIN_GUARD = [
    '(gt, "$players_kingdom", 0)',
    '(neq, "$players_kingdom", "fac_player_supporters_faction")',
    '(eq, "$player_has_homage", 0)',
    '(store_current_day, ":cur_day")',
    '(gt, "$mercenary_service_next_renew_day", ":cur_day")',
    '(val_mul, ":skill", 2)',
]


def main():
    limit = read("src/scripts/ZA_hardcoded_game_scripts/game_get_party_companion_limit.py")
    assert '(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player")' in limit
    for token in MERC_CAPTAIN_GUARD:
        assert token in limit, f"missing mercenary captain party-limit guard: {token}"

    report = read("src/menus/camp/party_size_report.py")
    for token in [
        '(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player")',
        '(gt, "$mercenary_service_next_renew_day", ":cur_day")',
        '(val_mul, ":leadership", 2)',
    ]:
        assert token in report, f"party size report should mirror limit formula: {token}"

    merc = read("src/scripts/ZY_helper_scripts/merc_begin_service.py")
    assert '(store_add, "$mercenary_service_next_renew_day", ":cur_day", ":renew_days")' in merc
    assert '(call_script, "script_player_join_faction", ":faction_no")' in merc

    print("Mercenary party limit static checks passed")


if __name__ == "__main__":
    main()
