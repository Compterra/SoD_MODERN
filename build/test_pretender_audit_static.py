from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_pretender_audit_exists() -> None:
    raw = read("docs/reports/pretender_system_audit.md")
    assert_contains(raw, "# Pretender System Audit")
    assert_contains(raw, "pretenders_begin")
    assert_contains(raw, "slot_troop_original_faction")
    assert_contains(raw, "slot_troop_pretender")
    assert_contains(raw, "script_rebellion_arguments")
    assert_contains(raw, "fac_player_supporters_faction")
    assert_contains(raw, "sod_house_rank_pretender")
    assert_contains(raw, "script_sod_pretender_get_claim_pressure_to_reg")


def test_family_audit_links_pretenders() -> None:
    raw = read("docs/reports/lord_family_structure_audit.md")
    assert_contains(raw, "docs/reports/pretender_system_audit.md")
    assert_contains(raw, "Pretenders are real existing claimant heroes")


if __name__ == "__main__":
    test_pretender_audit_exists()
    test_family_audit_links_pretenders()
    print("test_pretender_audit_static: OK")
