from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JESTER = ROOT / "src" / "dialogs" / "ZA02_sod_court_and_strategy"


def read(name):
    return (JESTER / name).read_text(encoding="utf-8", errors="replace")


def main():
    horses = read("trp_sod_jester_plyr_jester_cheatc1_02.py")
    ranged = read("trp_sod_jester_plyr_jester_cheatc1_03.py")
    armors = read("trp_sod_jester_plyr_jester_cheatc1_04.py")
    custom_melee = read("trp_sod_jester_plyr_jester_cheatc1_07.py")
    shields = read("trp_sod_jester_plyr_jester_cheatc1_08.py")
    custom_ranged = read("trp_sod_jester_plyr_jester_cheatc1_09.py")
    war_all = read("trp_sod_jester_plyr_jester_faction_choice_03.py")
    peace_all = read("trp_sod_jester_plyr_jester_faction_choice_04.py")

    assert '(try_for_range, ":item_no", horses_begin, horses_end)' in horses
    assert '(try_for_range, ":item_no", "itm_sumpter_horse", "itm_arrows")' not in horses

    assert "ADD RANGED WEAPONS" in ranged
    assert '(try_for_range, ":item_no", ranged_weapons_begin, ranged_weapons_end)' in ranged
    assert '(try_for_range, ":item_no", "itm_arrows", "itm_lady_dress_ruby")' not in ranged

    assert '(try_for_range, ":item_no", armors_begin, armors_end)' in armors
    assert '(try_for_range, ":item_no", "itm_leather_vest", "itm_turret_hat_ruby")' not in armors

    assert "ADD CUSTOM MELEE WEAPONS" in custom_melee
    assert '(item_get_type, ":item_type", ":item_no")' in custom_melee
    for item_type in ("itp_type_one_handed_wpn", "itp_type_two_handed_wpn", "itp_type_polearm"):
        assert item_type in custom_melee

    assert '(try_for_range, ":item_no", shields_begin, shields_end)' in shields
    assert '(try_for_range, ":item_no", "itm_wooden_shield", "itm_jarid")' not in shields

    assert "ADD CUSTOM RANGED WEAPONS" in custom_ranged
    assert '(item_get_type, ":item_type", ":item_no")' in custom_ranged
    for item_type in (
        "itp_type_arrows",
        "itp_type_bolts",
        "itp_type_bullets",
        "itp_type_thrown",
        "itp_type_bow",
        "itp_type_crossbow",
        "itp_type_pistol",
        "itp_type_musket",
    ):
        assert item_type in custom_ranged
    assert '(try_for_range, ":item_no", "itm_jarid", "itm_talak_warhammer")' not in custom_ranged

    for raw in (war_all, peace_all):
        assert raw.count("native_kingdoms_begin, native_kingdoms_end") == 2
        assert "(try_for_range, \":kingdom_1\", kingdoms_begin, kingdoms_end)" not in raw
        assert "(try_for_range, \":kingdom_2\", kingdoms_begin, kingdoms_end)" not in raw
        assert '(faction_slot_eq, ":kingdom_2", slot_faction_state, sfs_active)' in raw

    print("test_jester_item_cheat_ranges_static: OK")


if __name__ == "__main__":
    main()
