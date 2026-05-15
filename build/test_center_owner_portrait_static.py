from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    header = read("compile/headers/header_operations.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_show_center_owner_portrait.py")
    troop_helper = read("src/scripts/ZY_helper_scripts/sod_show_troop_portrait.py")
    walled_center_menu = read("src/menus/centers/castle/castle_castle.py")
    village_menu = read("src/menus/centers/village/recruit_volunteers.py")

    assert_contains(header, "set_game_menu_tableau_mesh             = 2032")
    assert_contains(troop_helper, '("sod_show_troop_portrait"')
    assert_contains(troop_helper, '(is_between, ":troop_no", 0, "trp_last_troop")')
    assert_contains(troop_helper, '(set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":troop_no", pos0)')
    assert_contains(troop_helper, '("sod_show_party_leader_portrait"')
    assert_contains(troop_helper, '(party_is_active, ":party_no")')
    assert_contains(troop_helper, '(gt, ":num_stacks", 0)')
    assert_contains(helper, '("sod_show_center_owner_portrait"')
    assert_contains(helper, '(party_get_slot, ":center_lord", ":center_no", slot_town_lord)')
    assert_contains(helper, '(is_between, ":center_lord", 0, "trp_last_troop")')
    assert_contains(helper, '(call_script, "script_sod_show_troop_portrait", ":center_lord")')

    assert_contains(walled_center_menu, '(call_script, "script_sod_show_center_owner_portrait", "$current_town")')
    assert_contains(village_menu, '(call_script, "script_sod_show_center_owner_portrait", "$current_town")')

    print("[center_owner_portrait_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
