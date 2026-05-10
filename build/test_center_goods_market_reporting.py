from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main() -> None:
    report_path = "src/menus/centers/common/center_goods_market_report.py"
    fief_path = "src/menus/camp/fief_reports.py"
    order_path = "src/menus/_order_game_menus.txt"
    recon_path = "src/scripts/ZD_centers/update_center_recon_notes.py"

    report = read(report_path)
    fief = read(fief_path)
    order = read(order_path)
    recon = read(recon_path)

    for needle in [
        "center_goods_market_report",
        "script_sod_get_center_goods_market_profile",
        ":food_balance",
        ":raw_balance",
        ":strategic_balance",
        ":luxury_flow",
        ":scarcity_pressure",
        ":trade_willingness",
        ":liquidity_pressure",
        ":wealth_delta",
        "town market engine",
        "castle military market",
        "village producer",
        "Trade goods now matter as consumption, caravan flow, and center wealth/liquidity",
    ]:
        assert_contains(report, needle, report_path)

    assert_contains(fief, "mnu_center_goods_market_report", fief_path)
    assert_contains(order, "other/center_goods_market_report.py", order_path)

    for needle in [
        "script_sod_get_center_goods_market_profile",
        "Goods market: food",
        "weekly wealth drift",
        "reg44",
        "reg51",
        "reg34",
        "reg41",
    ]:
        assert_contains(recon, needle, recon_path)

    print("[center_goods_market_reporting] OK")


if __name__ == "__main__":
    main()

