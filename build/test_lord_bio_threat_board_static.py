from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    lord_notes = read("src/scripts/ZH_heroes/update_troop_notes.py")
    offer = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_offer.py")
    active = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_active_contract.py")
    menu = read("src/menus/reports/regional_threat_board.py")

    assert_contains(lord_notes, "Campaign posture:")
    assert_contains(lord_notes, "slot_party_ai_state")
    assert_contains(lord_notes, "spai_besieging_center")
    assert_contains(lord_notes, "spai_holding_center")
    assert_contains(lord_notes, "spai_patrolling_around_center")
    assert_contains(lord_notes, "spai_accompanying_army")

    assert_contains(offer, "expected {s3}")
    assert_contains(offer, "recommended force {reg5}+ fit troops")
    assert_contains(offer, "suggested_strength")
    assert_contains(active, "recommended force {reg7}+ fit troops")
    assert_contains(menu, "expected enemy, tier, recommended force, reward, and deadline")

    print("[lord_bio_threat_board_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
