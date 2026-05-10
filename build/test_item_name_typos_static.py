from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    items = read("compile/module_items.py")

    assert "Breat_Plate" not in items, "misspelled armor name still present"
    assert "Breat Plate" not in items, "misspelled armor display text still present"
    for item_id in [
        "black_army_armor_5",
        "black_army_armor_6",
        "black_army_armor_7",
        "conquistador_breast_plate_1",
        "conquistador_breast_plate_2",
        "conquistador_breast_plate_3",
        "conquistador_breast_plate_4",
        "breast_plate_mail5",
        "slaver_armor_6",
        "slaver_armor_7",
    ]:
        assert f'["{item_id}", "Breast_Plate_with_Mail"' in items, (
            f"{item_id} should use corrected Breast_Plate_with_Mail display name"
        )

    print("Item name typo static checks passed")


if __name__ == "__main__":
    main()
