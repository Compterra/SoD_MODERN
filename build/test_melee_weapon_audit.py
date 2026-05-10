from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_melee_weapon_audit_generator_exists():
    text = read("build/audit_melee_weapons.py")
    assert "melee_weapon_audit.md" in text
    assert "itp_type_one_handed_wpn" in text
    assert "itp_type_two_handed_wpn" in text
    assert "itp_type_polearm" in text
    assert "itp_merchandise" in text
    assert "buyable_weapon_tier" in text
    assert "get_swing_damage" in text
    assert "get_thrust_damage" in text
    assert "damage_type" in text
    assert "item_usage" in text


def test_generated_melee_weapon_report_shape():
    text = read("docs/reports/melee_weapon_audit.md")
    assert "# Melee Weapon Audit" in text
    assert "## Global Summary" in text
    assert "## Summary by Weapon Type" in text
    assert "## Buyable Melee Tiers" in text
    assert "## Top Melee Pressure" in text
    assert "## Melee Watchlist" in text
    assert "## Full Melee Tables" in text


if __name__ == "__main__":
    test_melee_weapon_audit_generator_exists()
    test_generated_melee_weapon_report_shape()
    print("melee weapon audit checks passed")
