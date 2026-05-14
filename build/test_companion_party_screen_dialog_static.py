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
    hostile_fallback = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_154.py")
    assert_contains(hostile_fallback, '"Surrender or die. Make your choice"')
    assert_contains(hostile_fallback, '(eq, "$talk_context", tc_party_encounter)')
    assert_contains(hostile_fallback, '(gt, "$g_encountered_party", 0)')
    assert_contains(hostile_fallback, '(party_is_active, "$g_encountered_party")')
    assert_contains(hostile_fallback, '(gt, "$encountered_party_hostile", 0)')

    if '[anyone, "start", [], "Surrender or die. Make your choice"' in hostile_fallback:
        raise AssertionError("Hostile fallback must not be unconditional; it leaks into companion party-screen chat")

    member_chat = read("src/dialogs/ZA01_startup_and_dispatch/anyone_member_chat.py")
    assert_contains(member_chat, '(ge, "$g_talk_troop_faction", 0)')
    assert_contains(member_chat, '(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop")')

    print("[companion_party_screen_dialog_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
