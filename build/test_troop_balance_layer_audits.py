from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_generator_shape():
    text = read("build/audit_troop_balance_layers.py")
    assert "Upgrade Path Smoothness Audit" in text
    assert "Troop Role Consistency Audit" in text
    assert "Faction Doctrine Comparison Audit" in text
    assert "KT0 vs Equipment Audit" in text
    assert "build_fit_rows" in text
    assert "parse_upgrades" in text
    assert "edge_notes" in text
    assert "role_notes" in text
    assert "kt0_notes" in text


def test_reports_exist_and_cover_requested_layers():
    expected = {
        "docs/reports/upgrade_path_smoothness_audit.md": [
            "Upgrade Path Smoothness Audit",
            "Kit drops",
            "KT0 drops",
            "role shift",
        ],
        "docs/reports/troop_role_consistency_audit.md": [
            "Troop Role Consistency Audit",
            "Role consistency flags",
            "Support Exceptions",
        ],
        "docs/reports/faction_doctrine_comparison_audit.md": [
            "Faction Doctrine Comparison Audit",
            "Avg kit",
            "Avg KT0 open",
            "mini-faction doctrine",
        ],
        "docs/reports/kt0_vs_equipment_audit.md": [
            "KT0 vs Equipment Audit",
            "KT0/equipment flags",
            "KT0 O/D/H/Open",
        ],
    }
    for rel, needles in expected.items():
        text = read(rel)
        for needle in needles:
            assert needle in text


if __name__ == "__main__":
    test_generator_shape()
    test_reports_exist_and_cover_requested_layers()
    print("troop balance layer audit checks passed")
