from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_lord_family_validator_exists() -> None:
    raw = read("build/audit_lord_family_structure.py")
    assert_contains(raw, "Lord Family Validation Report")
    assert_contains(raw, "parse_seed_relations")
    assert_contains(raw, "complete_family_relations")
    assert_contains(raw, "build_house_identities")
    assert_contains(raw, "House Identity Layer")
    assert_contains(raw, "slot_troop_sod_house_id")
    assert_contains(raw, "slot_troop_sod_house_head")
    assert_contains(raw, "sod_house_rank_lord")
    assert_contains(raw, "sod_house_rank_pretender")
    assert_contains(raw, "pretenders_begin")
    assert_contains(raw, "ladies_without_family_anchor")
    assert_contains(raw, "spouse_not_reciprocal")
    assert_contains(raw, "parent_child_not_reciprocal")
    assert_contains(raw, "child_parent_not_reciprocal")
    assert_contains(raw, "Model Depth Warnings")
    assert_contains(raw, "lord_family_validation_report.md")


def test_lord_family_audit_references_validator() -> None:
    raw = read("docs/reports/lord_family_structure_audit.md")
    assert_contains(raw, "## Validator Pass")
    assert_contains(raw, "build/audit_lord_family_structure.py")
    assert_contains(raw, "docs/reports/lord_family_validation_report.md")


def test_house_identity_source_wired() -> None:
    constants = read("src/constants/module_constants.py")
    assert_contains(constants, "slot_troop_sod_house_id")
    assert_contains(constants, "slot_troop_sod_house_rank")
    assert_contains(constants, "slot_troop_sod_house_head")
    assert_contains(constants, "slot_troop_sod_house_grievance")
    assert_contains(constants, "slot_troop_sod_house_loyalty")
    assert_contains(constants, "slot_troop_sod_house_claim_strength")
    assert_contains(constants, "sod_house_rank_lord")
    assert_contains(constants, "sod_house_rank_lady")

    script = read("src/scripts/ZY_helper_scripts/sod_initialize_house_identity.py")
    assert_contains(script, "sod_initialize_house_identity")
    assert_contains(script, "slot_troop_sod_house_head")
    assert_contains(script, "slot_troop_spouse")
    assert_contains(script, "slot_troop_sod_house_claim_strength")

    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    assert_contains(game_start, '(call_script, "script_sod_initialize_house_identity")')


if __name__ == "__main__":
    test_lord_family_validator_exists()
    test_lord_family_audit_references_validator()
    test_house_identity_source_wired()
    print("test_lord_family_audit_static: OK")
