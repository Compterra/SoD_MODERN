# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    guard_about = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_guard_about.py")
    boar_encounter = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")

    if "script_sod_black_khergits_describe_status_to_s27" in guard_about:
        raise AssertionError("Night guard talk must not append the full horde status report")
    if "{s27}" in guard_about:
        raise AssertionError("Night guard talk must not use the full status string register")
    if "store_random_in_range, \":guard_line\", 0, 4" not in guard_about:
        raise AssertionError("Night guard talk should offer multiple authored variations")
    if guard_about.count("str_store_string, s5") < 4:
        raise AssertionError("Night guard talk should have at least four variations")
    if "frontier tribute" in guard_about or "Boar Clan warding" in guard_about:
        raise AssertionError("Black Khergit guard dialogue must not contain Boar Clan toll language")
    if "banked fire" not in guard_about or "sleeping camp" not in guard_about:
        raise AssertionError("Night guard dialogue should frame the Khan as resting while guards protect the sleeping camp")
    if "camp sleeps by day" in guard_about:
        raise AssertionError("Night guard dialogue must not claim the camp sleeps by day")
    if "frontier tribute" not in boar_encounter:
        raise AssertionError("Boar Clan toll language should remain in the Boar encounter path")

    print("[black_khergit_guard_dialog_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
