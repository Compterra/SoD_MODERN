# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GUARDED_PARTY_DIALOGS = (
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_38.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_79.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_80.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_83.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_151.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_stated_special_war_aims.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_stated_job_board_question.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_stated_organized_sponsor.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_stated_duel_challenge.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_hostile_leader_duel_refuses.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_special_raider_war_aims_black_khergit.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_special_raider_war_aims_conquistadors.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_special_raider_war_aims_elephant_guard.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_special_raider_war_aims_serpent.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_raider_job_board_question.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_organized_raider_sponsor_black_khergit.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_organized_raider_sponsor_conquistadors.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_organized_raider_sponsor_elephant_guard.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_organized_raider_sponsor_serpent.py",
)

GUARDED_FACTION_DIALOGS = (
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_84.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_85.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_86.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_87.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_89.py",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str, rel: str) -> None:
    if needle not in raw:
        raise AssertionError(f"{rel} missing guard: {needle}")


def main() -> int:
    start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start.py")
    assert_contains(start, '(gt, "$current_town", 0)', "anyone_start.py")
    assert_contains(start, '(ge, "$g_talk_troop_faction", 0)', "anyone_start.py")
    assert_contains(start, '(assign, "$g_talk_troop_faction_relation", 0)', "anyone_start.py")

    for rel in GUARDED_PARTY_DIALOGS:
        raw = read(rel)
        assert_contains(raw, '(gt, "$g_encountered_party", 0)', rel)
        assert_contains(raw, '(party_is_active, "$g_encountered_party")', rel)

    for rel in GUARDED_FACTION_DIALOGS:
        raw = read(rel)
        assert_contains(raw, '(ge, "$g_encountered_party_faction", 0)', rel)

    print("[dialog_invalid_party_guards_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
