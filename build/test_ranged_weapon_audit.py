from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    target = ROOT / rel
    if not target.exists() and rel.startswith("docs/reports/"):
        matches = sorted((ROOT / "docs" / "reports").rglob(Path(rel).name))
        if len(matches) == 1:
            target = matches[0]
    return target.read_text(encoding="utf-8")


def test_ranged_weapon_audit_generator_exists():
    text = read("build/audit_ranged_weapons.py")
    assert "ranged_weapon_audit.md" in text
    assert "itp_type_bow" in text
    assert "itp_type_crossbow" in text
    assert "itp_type_thrown" in text
    assert "itp_type_arrows" in text
    assert "itp_type_bolts" in text
    assert "itp_merchandise" in text
    assert "buyable_ranged_tier" in text
    assert "get_missile_speed" in text
    assert "get_max_ammo" in text
    assert "item_usage" in text


def test_generated_ranged_weapon_report_shape():
    text = read("docs/reports/ranged_weapon_audit.md")
    assert "# Ranged Weapon Audit" in text
    assert "## Global Summary" in text
    assert "## Summary by Ranged Type" in text
    assert "## Buyable Ranged Tiers" in text
    assert "## Top Ranged Pressure" in text
    assert "## Ranged Watchlist" in text
    assert "## Full Ranged Tables" in text


if __name__ == "__main__":
    test_ranged_weapon_audit_generator_exists()
    test_generated_ranged_weapon_report_shape()
    print("ranged weapon audit checks passed")
