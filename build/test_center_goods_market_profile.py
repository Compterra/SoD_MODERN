from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main() -> None:
    profile_path = "src/scripts/ZY_helper_scripts/sod_center_goods_market_profile.py"
    trigger_path = "src/triggers/ST04_weekly/entry_0160.py"
    order_path = "src/triggers/_order_simple_triggers.txt"
    report_path = "docs/reports/center_goods_market_audit.md"

    profile = read(profile_path)
    trigger = read(trigger_path)
    order = read(order_path)
    report = read(report_path)

    for needle in [
        "sod_get_center_goods_market_profile",
        "script_sod_get_center_trade_demand_profile",
        "slot_town_trade_good_productions_begin",
        "trade_goods_begin",
        "trade_goods_end",
        "itm_grain",
        "itm_wool",
        "itm_salt",
        "itm_spice",
        ":food_balance",
        ":raw_balance",
        ":strategic_balance",
        ":luxury_flow",
        ":scarcity_pressure",
        ":trade_willingness",
        ":liquidity_pressure",
        ":wealth_delta",
        "val_clamp, \":wealth_delta\", -500, 1801",
    ]:
        assert_contains(profile, needle, profile_path)

    for needle in [
        "script_sod_get_center_goods_market_profile",
        "script_sod_change_center_wealth",
        "script_change_center_prosperity",
        "script_sod_change_center_local_prosperity",
        ":trade_willingness",
        ":scarcity_pressure",
        ":food_balance",
        ":strategic_balance",
    ]:
        assert_contains(trigger, needle, trigger_path)

    assert_contains(order, "ST04_weekly/entry_0160.py", order_path)

    for needle in [
        "# Center Goods Market Audit",
        "food balance",
        "raw balance",
        "strategic balance",
        "luxury flow",
        "wealth delta",
        "Weekly goods-market drift",
    ]:
        assert_contains(report, needle, report_path)

    print("[center_goods_market_profile] OK")


if __name__ == "__main__":
    main()
