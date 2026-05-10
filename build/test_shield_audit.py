from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_shield_audit_generator_exists():
    text = read("build/audit_shield_items.py")
    assert "shield_audit.md" in text
    assert "itp_type_shield" in text
    assert "itp_merchandise" in text
    assert "buyable_shield_tier" in text
    assert "get_hit_points" in text
    assert "get_weapon_length" in text
    assert "get_body_armor" in text
    assert "get_speed_rating" in text
    assert "item_usage" in text


def test_generated_shield_report_shape():
    text = read("docs/reports/shield_audit.md")
    assert "# Shield Audit" in text
    assert "## Global Summary" in text
    assert "## Top Shield Pressure" in text
    assert "## Buyable Shield Tiers" in text
    assert "## Shield Watchlist" in text
    assert "## Full Shield Table" in text


if __name__ == "__main__":
    test_shield_audit_generator_exists()
    test_generated_shield_report_shape()
    print("shield audit checks passed")
