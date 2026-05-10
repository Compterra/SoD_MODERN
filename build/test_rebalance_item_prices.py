from pathlib import Path
import tempfile

import rebalance_item_prices as rebalance


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_rebalance_script_shape():
    text = read("build/rebalance_item_prices.py")
    assert "item_kinds1.txt" in text
    assert "parse_item_line" in text
    assert "target_value" in text
    assert "clamp_change" in text
    assert "--apply" in text
    assert "--groups" in text
    assert "pre_price_rebalance" in text


def test_parse_item_line_value_token():
    line = " itm_saddle_horse Saddle_Horse Saddle_Horse 1 saddle_horse 0 65537 0 112 123 0.000000 90 0 14 0 1 0 39 0 0 0 8 0"
    item = rebalance.parse_item_line(line, 0)
    assert item is not None
    assert item.item_id == "itm_saddle_horse"
    assert item.value == 112
    assert item.imodbits == 123
    assert item.buyable
    assert item.tokens[item.value_token_index] == "112"


def test_report_only_does_not_rewrite_item_file():
    source = ROOT / "_export" / "item_kinds1.txt"
    original = source.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as temp:
        item_path = Path(temp) / "item_kinds1.txt"
        report_path = Path(temp) / "report.md"
        item_path.write_text(original, encoding="utf-8")
        rebalance.main([str(item_path), "--report", str(report_path)])
        assert item_path.read_text(encoding="utf-8") == original
        report = report_path.read_text(encoding="utf-8")
        assert "# Generated Item Price Rebalance" in report
        assert "## Largest Changes" in report
        assert "Selected groups: Mount" in report


def test_group_filter_can_select_mounts_only():
    source = ROOT / "_export" / "item_kinds1.txt"
    with tempfile.TemporaryDirectory() as temp:
        item_path = Path(temp) / "item_kinds1.txt"
        report_path = Path(temp) / "report.md"
        item_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        rebalance.main([str(item_path), "--report", str(report_path), "--groups", "Mount"])
        report = report_path.read_text(encoding="utf-8")
        assert "| Mount |" in report
        assert "| Armor |" not in report
        assert "| Melee |" not in report


def test_build_hook_is_opt_in():
    text = read("build_module.bat")
    assert "rebalance_item_prices.py" not in text
    assert "SOD_REBALANCE_ITEM_PRICES" not in text


if __name__ == "__main__":
    test_rebalance_script_shape()
    test_parse_item_line_value_token()
    test_report_only_does_not_rewrite_item_file()
    test_build_hook_is_opt_in()
    print("item price rebalance checks passed")
