from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    target = ROOT / rel
    if not target.exists() and rel.startswith("docs/reports/"):
        matches = sorted((ROOT / "docs" / "reports").rglob(Path(rel).name))
        if len(matches) == 1:
            target = matches[0]
    return target.read_text(encoding="utf-8")


def test_armor_audit_generator_exists():
    text = read("build/audit_armor_items.py")
    assert "armor_audit.md" in text
    assert "itp_type_head_armor" in text
    assert "itp_type_body_armor" in text
    assert "itp_type_foot_armor" in text
    assert "itp_type_hand_armor" in text
    assert "itp_merchandise" in text
    assert "get_head_armor" in text
    assert "get_body_armor" in text
    assert "get_leg_armor" in text
    assert "buyable_armor_tier" in text
    assert "item_usage" in text


def test_generated_armor_report_shape():
    text = read("docs/reports/armor_audit.md")
    assert "# Armor Audit" in text
    assert "## Summary by Armor Slot" in text
    assert "## Top Armor Pressure" in text
    assert "## Armor Watchlist" in text
    assert "## Armor by Buyability" in text
    assert "## Buyable Armor Tiers" in text
    assert "Tier 4 - Elite" in text
    assert "Buyable Armor" in text
    assert "Non-Buyable / Troop-Only Armor" in text
    assert "## Full Armor Tables" in text


if __name__ == "__main__":
    test_armor_audit_generator_exists()
    test_generated_armor_report_shape()
    print("armor audit checks passed")
