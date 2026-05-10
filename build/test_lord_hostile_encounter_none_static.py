from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_generic_lord_fight_fallback_does_not_say_none() -> None:
    fallback = read(
        "src/dialogs/ZA01_startup_and_dispatch/"
        "anyone_auto_proceed_party_encounter_lord_hostile_attacker_2_fight_02.py"
    )
    assert '[anyone, "party_encounter_lord_hostile_attacker_2_fight"' in fallback
    assert '"none"' not in fallback
    assert "Draw your steel" in fallback


def test_generic_lord_surrender_fallback_does_not_say_none() -> None:
    fallback = read(
        "src/dialogs/ZB01_lords_politics_and_family/"
        "anyone_party_encounter_lord_hostile_attacker_2_surrender_10.py"
    )
    assert '"none"' not in fallback
    assert "Lay down your arms" in fallback


if __name__ == "__main__":
    test_generic_lord_fight_fallback_does_not_say_none()
    test_generic_lord_surrender_fallback_does_not_say_none()
    print("test_lord_hostile_encounter_none_static: OK")
