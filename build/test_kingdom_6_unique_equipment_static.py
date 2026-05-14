from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LEGION_ITEMS = (
    "legion_helm_01",
    "legion_helm_02",
    "legion_helm_03",
    "legion_helm_04",
    "legion_helm_05",
    "legion_helm_06",
    "legion_helm_07",
    "legion_helm_08",
    "legion_helm_09",
    "legion_helm_10",
    "legion_helm_11",
    "legion_helm_12",
    "legion_armor_1",
    "legion_armor_2",
    "legion_armor_3",
    "legion_armor_4",
    "legion_chiton_red",
    "legion_chiton_half_red",
    "legion_greaves",
    "legion_shield_1",
    "legion_shield_2",
    "legion_horse_1",
    "legion_horse_2",
    "legion_horse_3",
    "legion_horse_4",
    "legion_horse_5",
    "legion_horse_6",
    "legion_horse_7",
    "legion_dagger",
    "legion_sword_centurion",
    "legion_sword_sica",
    "legion_sword_hoplite",
    "legion_sword_kopis",
    "legion_spear_kamax",
    "legion_spear_palton",
    "legion_axe",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def item_entry(raw: str, item_id: str) -> str:
    marker = f'["{item_id}",'
    start = raw.index(marker)
    next_item = raw.find('\n["', start + len(marker))
    next_section = raw.find("\n#", start + len(marker))
    candidates = [pos for pos in (next_item, next_section) if pos != -1]
    end = min(candidates) if candidates else len(raw)
    return raw[start:end]


def test_kingdom_6_unique_equipment_is_not_merchandise() -> None:
    items = read("compile/module_items.py")
    for item_id in LEGION_ITEMS:
        entry = item_entry(items, item_id)
        assert "itp_merchandise" not in entry, f"{item_id} should not show up in merchant stores"


def test_kingdom_6_troops_still_use_legion_equipment() -> None:
    troops = read("compile/module_troops.py")
    assert_contains(troops, "fac_kingdom_6")
    for token in (
        "itm_legion_helm_01",
        "itm_legion_armor_1",
        "itm_legion_shield_1",
        "itm_legion_horse_6",
        "itm_legion_sword_centurion",
        "itm_legion_spear_kamax",
    ):
        assert_contains(troops, token)


if __name__ == "__main__":
    test_kingdom_6_unique_equipment_is_not_merchandise()
    test_kingdom_6_troops_still_use_legion_equipment()
    print("test_kingdom_6_unique_equipment_static: OK")
