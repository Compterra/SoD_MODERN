from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICE_SCRIPT = ROOT / "src" / "scripts" / "ZB_economy_and_trade" / "update_trade_good_price_for_party.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing expected text: {needle}")


def main() -> None:
    text = read(PRICE_SCRIPT)

    assert_contains(text, 'script_sod_get_center_goods_market_profile')
    for name in [
        'goods_food_balance',
        'goods_raw_balance',
        'goods_strategic_balance',
        'goods_luxury_flow',
        'goods_scarcity_pressure',
        'goods_trade_willingness',
        'goods_liquidity_pressure',
        'profile_price_shift',
    ]:
        assert_contains(text, name)

    for good in ['itm_grain', 'itm_wool', 'itm_salt', 'itm_spice']:
        assert_contains(text, good)

    assert_contains(text, 'val_clamp, ":profile_price_shift", -18, 31')
    assert_contains(text, 'val_add, ":new_price", ":profile_price_shift"')

    print("Trade-good price pressure static checks passed.")


if __name__ == "__main__":
    main()
