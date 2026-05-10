from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPORTS = [
    ("docs/reports/ammo_audit.md", "# Ammo Audit", "## Full Ammo Table"),
    ("docs/reports/troop_loadout_audit.md", "# Troop Loadout Audit", "## Full Loadout Table"),
    ("docs/reports/item_value_availability_audit.md", "# Item Value and Availability Audit", "## Watchlist"),
    ("docs/reports/imod_compatibility_audit.md", "# Item Modifier Compatibility Audit", "## Compatibility Watchlist"),
    ("docs/reports/goods_food_audit.md", "# Goods and Food Audit", "## Food Balance Table"),
    ("docs/reports/special_item_audit.md", "# Special Items Audit", "## Special Gear and Artifacts"),
]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_item_system_generator_exists():
    text = read("build/audit_item_systems.py")
    assert "ammo_audit.md" in text
    assert "troop_loadout_audit.md" in text
    assert "item_value_availability_audit.md" in text
    assert "imod_compatibility_audit.md" in text
    assert "goods_food_audit.md" in text
    assert "special_item_audit.md" in text
    assert "slot_item_food_bonus" in text
    assert "slot_item_intelligence_requirement" in text


def test_generated_item_system_reports_shape():
    for rel, title, section in REPORTS:
        text = read(rel)
        assert title in text
        assert "## Summary" in text
        assert section in text
    ammo = read("docs/reports/ammo_audit.md")
    assert "## Buyable Ammo Tiers" in ammo


if __name__ == "__main__":
    test_item_system_generator_exists()
    test_generated_item_system_reports_shape()
    print("item system audit checks passed")
