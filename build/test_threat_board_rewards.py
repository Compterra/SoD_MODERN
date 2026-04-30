# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    reward = read("src/scripts/ZY_helper_scripts/sod_threat_board_calculate_reward.py")
    describe = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_offer.py")
    accept = read("src/scripts/ZY_helper_scripts/sod_threat_board_accept_contract.py")
    active = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_active_contract.py")
    complete = read("src/scripts/ZY_helper_scripts/sod_threat_board_complete_contract.py")
    defeated = read("src/scripts/ZY_helper_scripts/sod_threat_board_note_party_defeated.py")

    assert_contains(reward, "sod_threat_board_calculate_reward")
    assert_contains(reward, "store_sub, \":urgency\", 12, \":deadline_days\"")
    assert_contains(reward, "sod_threat_type_faction_problem")
    assert_contains(reward, "assign, reg(0), \":reward_gold\"")
    assert_contains(reward, "assign, reg(1), \":reward_xp\"")

    assert_contains(describe, "script_sod_threat_board_calculate_reward")
    assert_contains(describe, "{reg4} XP")
    assert_contains(accept, "script_sod_threat_board_calculate_reward")
    assert_contains(accept, "Contract sponsor: {s2}. Marked target: {s1}.")
    assert_contains(accept, "add_quest_note_from_sreg, \"qst_regional_threat_contract\", 4")
    assert_contains(active, "slot_quest_sod_threat_reward_xp")
    assert_contains(active, "{reg6} XP")
    assert_contains(complete, "{reg2} XP")
    assert_contains(defeated, "Marked target defeated: {s5}.")
    assert_contains(defeated, "add_quest_note_from_sreg, \"qst_regional_threat_contract\", 5")

    print("[threat_board_rewards] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
