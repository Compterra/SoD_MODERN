# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected stale token: {needle}")


def main() -> int:
    entry = read("src/dialogs/ZA01_startup_and_dispatch/anyone_auto_proceed_defeat_lord_answer_1_08.py")
    assert_contains(entry, '"defeat_lord_answer_1"')
    assert_contains(entry, "slcp_nihilistic")
    assert_contains(entry, '"cpdla_nihilistic_1"')
    assert_not_contains(entry, '"cpdla1_nihilistic_1"')

    default_death = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_2.py")
    assert_contains(default_death, '"cpdla_nihilistic_2"')
    assert_contains(default_death, '"close_window"')
    assert_contains(default_death, '(call_script, "script_kill_kingdom_hero", "$g_talk_troop")')
    assert_contains(default_death, '(assign, "$g_leave_encounter", 1)')
    assert_not_contains(default_death, '"cpdla_nihilistic_3"')

    confession = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_4_02.py")
    assert_contains(confession, '"cpdla_nihilistic_2"')
    assert_contains(confession, '"cpdla_nihilistic_3"')
    assert_contains(confession, '"cpdla_nihilistic_4"')
    assert_contains(confession, '"cpdla_nihilistic_5"')

    close_rot = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_cpdla_nihilistic_4.py")
    assert_contains(close_rot, '(call_script, "script_kill_kingdom_hero", "$g_talk_troop")')

    print("[nihilistic_centurion_dialog_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
