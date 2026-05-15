from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))
sys.path.insert(0, str(COMPILE / "ids"))

from header_items import (  # type: ignore
    itp_type_arrows,
    itp_type_body_armor,
    itp_type_bolts,
    itp_type_book,
    itp_type_bow,
    itp_type_bullets,
    itp_type_crossbow,
    itp_type_foot_armor,
    itp_type_goods,
    itp_type_hand_armor,
    itp_type_head_armor,
    itp_type_horse,
    itp_type_musket,
    itp_type_one_handed_wpn,
    itp_type_pistol,
    itp_type_polearm,
    itp_type_shield,
    itp_type_thrown,
    itp_type_two_handed_wpn,
)
import ID_items  # type: ignore
import module_items  # type: ignore


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def item_id(name: str) -> int:
    return getattr(ID_items, f"itm_{name}")


def item_type(index: int) -> int:
    return module_items.items[index][3] & 0xFF


def assert_item_range(
    label: str,
    begin_name: str,
    end_name: str,
    allowed_types: set[int],
) -> None:
    begin = item_id(begin_name)
    end = item_id(end_name)
    assert begin < end, f"{label} range is inverted: {begin_name} >= {end_name}"
    bad = [
        module_items.items[index][0]
        for index in range(begin, end)
        if item_type(index) not in allowed_types
    ]
    assert not bad, f"{label} range contains wrong item types: {bad[:20]}"


def test_core_item_ranges_match_item_types() -> None:
    constants = read("src/constants/module_constants.py")
    for token in (
        'ranged_weapons_begin = "itm_arrows"',
        'ranged_weapons_end = "itm_wooden_stick"',
        'armors_end = "itm_arrows"',
        'shields_end = "itm_bascinetnasal"',
    ):
        assert token in constants

    assert_item_range("trade goods", "smoked_fish", "tutorial_sword", {itp_type_goods})
    assert_item_range("food", "smoked_fish", "spice", {itp_type_goods})
    assert_item_range("books", "book_tactics", "smoked_fish", {itp_type_book})
    assert_item_range("horses", "sumpter_horse", "leather_gloves", {itp_type_horse})
    assert_item_range(
        "armors",
        "leather_gloves",
        "arrows",
        {itp_type_head_armor, itp_type_body_armor, itp_type_foot_armor, itp_type_hand_armor},
    )
    assert_item_range(
        "ranged weapons",
        "arrows",
        "wooden_stick",
        {
            itp_type_arrows,
            itp_type_bolts,
            itp_type_bullets,
            itp_type_thrown,
            itp_type_bow,
            itp_type_crossbow,
            itp_type_pistol,
            itp_type_musket,
        },
    )
    assert_item_range(
        "melee weapons",
        "wooden_stick",
        "wooden_shield",
        {itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm},
    )
    assert_item_range("shields", "wooden_shield", "bascinetnasal", {itp_type_shield})


def test_horse_range_excludes_armor_block() -> None:
    constants = read("src/constants/module_constants.py")
    assert 'horses_begin = "itm_sumpter_horse"' in constants
    assert 'horses_end = "itm_leather_gloves"' in constants

    begin = item_id("sumpter_horse")
    end = item_id("leather_gloves")
    bad = [
        module_items.items[index][0]
        for index in range(begin, end)
        if item_type(index) != itp_type_horse
    ]
    assert not bad, f"non-horse items inside horses range: {bad[:20]}"


def test_spicy_reported_mounts_are_horse_typed() -> None:
    for name in (
        "warhorse",
        "warhorse_b",
        "warhorse_black",
        "charger",
        "charger_black",
        "anthorse2",
        "legion_horse_4",
        "noble_charger",
        "conquistador_horse_1",
        "serpent_horse_8",
    ):
        assert item_type(item_id(name)) == itp_type_horse, name


def test_horse_supply_scripts_use_item_type_guard() -> None:
    loot_script = read("src/scripts/ZB_economy_and_trade/loot_player_items.py")
    company_script = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    assert '(item_get_type, ":item_type", ":item_id")' in loot_script
    assert '(assign, ":randomness", 0)' in loot_script
    assert "(eq, \":item_type\", itp_type_horse)" in loot_script
    assert "weapons_begin, weapons_end" not in loot_script
    assert "ranged_weapons_begin, ranged_weapons_end" not in loot_script
    assert "armors_begin, armors_end" not in loot_script
    assert "shields_begin, shields_end" not in loot_script
    assert '(try_for_range, ":cur_horse", horses_begin, "itm_items_end")' in company_script
    assert '(item_get_type, ":item_type", ":cur_horse")' in company_script
    assert "(eq, \":item_type\", itp_type_horse)" in company_script


def test_formation_ranged_equipment_scan_uses_full_ranged_range() -> None:
    formation_script = read("src/scripts/ZE_encounters/cf_formation_wedge.py")
    assert formation_script.count(
        '(try_for_range, ":ranged_item", ranged_weapons_begin, ranged_weapons_end)'
    ) == 3
    assert '(try_for_range, ":ranged_item", "itm_jarid", "itm_flintlock_pistol")' not in formation_script


def test_spy_disguise_scans_only_armor_range() -> None:
    spy_script = read("src/scripts/ZD_centers/center_set_walker_to_type.py")
    assert spy_script.count('(try_for_range, ":item_no", armors_begin, armors_end)') == 3
    assert '(try_for_range, ":item_no", "itm_horse_meat", "itm_wooden_stick")' not in spy_script


if __name__ == "__main__":
    test_core_item_ranges_match_item_types()
    test_horse_range_excludes_armor_block()
    test_spicy_reported_mounts_are_horse_typed()
    test_horse_supply_scripts_use_item_type_guard()
    test_formation_ranged_equipment_scan_uses_full_ranged_range()
    test_spy_disguise_scans_only_armor_range()
    print("test_mount_item_type_static: OK")
