from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    target = ROOT / rel
    if not target.exists() and rel.startswith("docs/reports/"):
        matches = sorted((ROOT / "docs" / "reports").rglob(Path(rel).name))
        if len(matches) == 1:
            target = matches[0]
    return target.read_text(encoding="utf-8")


def test_tier_fit_generator_exists():
    text = read("build/audit_troop_equipment_tier_fit.py")
    assert "troop_equipment_tier_fit_audit.md" in text
    assert "build_rows" in text
    assert "all_item_rows" in text
    assert "fit_tier" in text
    assert "level_tier" in text
    assert "does not suggest changing troop inventories" in text


def test_tier_fit_report_shape():
    text = read("docs/reports/troop_equipment_tier_fit_audit.md")
    assert "# Troop Equipment Tier Fit Audit" in text
    assert "## Faction Summary" in text
    assert "## Highest Priority Flags" in text
    assert "## Full Faction Tables" in text
    assert "Tree tier" in text
    assert "Fit tier" in text
    assert "player_supporters_faction" in text


if __name__ == "__main__":
    test_tier_fit_generator_exists()
    test_tier_fit_report_shape()
    print("troop equipment tier fit audit checks passed")
