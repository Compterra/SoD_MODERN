from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    target = ROOT / rel
    if not target.exists() and rel.startswith("docs/reports/"):
        matches = sorted((ROOT / "docs" / "reports").rglob(Path(rel).name))
        if len(matches) == 1:
            target = matches[0]
    return target.read_text(encoding="utf-8")


def test_mount_audit_generator_exists():
    text = read("build/audit_mount_items.py")
    assert "mount_audit.md" in text
    assert "itp_type_horse" in text
    assert "get_hit_points" in text
    assert "get_missile_speed" in text
    assert "get_speed_rating" in text
    assert "get_body_armor" in text
    assert "get_thrust_damage" in text
    assert "itp_merchandise" in text
    assert "mount_tier" in text
    assert "item_usage" in text


def test_generated_mount_report_shape():
    text = read("docs/reports/mount_audit.md")
    assert "# Mount Audit" in text
    assert "## Global Summary" in text
    assert "## Top Mount Pressure" in text
    assert "## Mount Watchlist" in text
    assert "## Buyable Mount Outliers" in text
    assert "Singleton Top Tiers" in text
    assert "## Mount Tier Groups" in text
    assert "## Mounts by Tier" in text
    assert "Buyable Mounts" in text
    assert "Non-Buyable / Troop-Only Mounts" in text
    assert "## Full Mount Table" in text


if __name__ == "__main__":
    test_mount_audit_generator_exists()
    test_generated_mount_report_shape()
    print("mount audit checks passed")
