from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VILLAGE_TRIGGER = ROOT / "src" / "triggers" / "ST99_other" / "entry_0036.py"
TOWN_TRIGGER = ROOT / "src" / "triggers" / "ST04_weekly" / "entry_0019.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing expected text: {needle}")


def main() -> None:
    village = read(VILLAGE_TRIGGER)
    town = read(TOWN_TRIGGER)

    assert_contains(village, 'script_sod_get_center_goods_market_profile')
    assert_contains(village, 'production_feedback_pct')
    assert_contains(village, 'goods_trade_willingness')
    assert_contains(village, 'goods_scarcity_pressure')
    assert_contains(village, 'goods_food_balance')
    assert_contains(village, 'goods_raw_balance')
    assert_contains(village, 'script_center_change_trade_good_production')
    for good in ['itm_grain', 'itm_flour', 'itm_wool', 'itm_oil', 'itm_iron']:
        assert_contains(village, good)

    assert_contains(town, 'script_sod_get_center_goods_market_profile')
    assert_contains(town, 'finished_output')
    assert_contains(town, 'workshop_output')
    assert_contains(town, 'luxury_output')
    for good in ['itm_tools', 'itm_linen', 'itm_pottery', 'itm_velvet']:
        assert_contains(town, good)

    assert_contains(town, 'castles_begin')
    assert_contains(town, 'script_sod_get_castle_support_profile')
    assert_contains(town, 'castle_food_consumption')
    assert_contains(town, 'castle_store_consumption')
    for good in ['itm_grain', 'itm_flour', 'itm_salt', 'itm_iron', 'itm_tools']:
        assert_contains(town, good)

    print("Trade-good production feedback static checks passed.")


if __name__ == "__main__":
    main()
