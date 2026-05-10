from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main() -> None:
    audit_path = "build/audit_trade_goods_value.py"
    report_path = "docs/reports/trade_goods_value_audit.md"
    audit = read(audit_path)
    report = read(report_path)

    for needle in [
        "ROLE_BANDS",
        "ROLE_BY_ITEM",
        '"staple_food"',
        '"preserved_food"',
        '"livestock_food"',
        '"drink_luxury_food"',
        '"raw_material"',
        '"semi_luxury_raw"',
        '"strategic_material"',
        '"luxury"',
        "get_abundance",
        "food_quality",
        "Trade Goods Value Audit",
    ]:
        assert_contains(audit, needle, audit_path)

    for needle in [
        "# Trade Goods Value Audit",
        "## Role Bands",
        "## Trade Goods",
        "## Watchlist",
        "`staple_food`",
        "`strategic_material`",
        "`luxury`",
        "`grain`",
        "`tools`",
        "`velvet`",
        "Scarcity raises demand",
    ]:
        assert_contains(report, needle, report_path)

    print("[trade_goods_value_audit] OK")


if __name__ == "__main__":
    main()
