# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError("Missing expected token: %s" % needle)


def main() -> int:
    pipeline = read("src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py")
    assert_contains(pipeline, '"sod_center_apply_cattle_delta"')
    assert_contains(pipeline, "slot_village_number_of_cattle")
    assert_contains(pipeline, "(val_clamp, \":new_cattle\", 0, 201)")
    assert_contains(pipeline, "(assign, reg1, \":actual_delta\")")

    expected_callers = (
        "src/scripts/ZD_centers/buy_cattle_from_village.py",
        "src/menus/other/continue_30.py",
        "src/menus/other/continue_31.py",
        "src/scripts/ZC_parties/remove_cattles_if_herd_is_close_to_party.py",
        "src/triggers/ST99_other/entry_0036.py",
        "src/scripts/ZY_helper_scripts/sod_apply_center_investment.py",
        "src/scripts/ZY_helper_scripts/sod_threat_board_apply_economy_effect.py",
    )
    for rel in expected_callers:
        assert_contains(read(rel), "script_sod_center_apply_cattle_delta")

    direct_write_allowed = {
        "src/scripts/ZA_hardcoded_game_scripts/game_start.py",
        "src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py",
        "src/scripts/ZY_helper_scripts/sod_normalize_center_population.py",
    }
    offenders = []
    for base in ("src/scripts", "src/triggers", "src/menus"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel in direct_write_allowed:
                continue
            raw = path.read_text(encoding="utf-8")
            if "party_set_slot" in raw and "slot_village_number_of_cattle" in raw:
                offenders.append(rel)
    if offenders:
        raise AssertionError("Unexpected direct cattle writes: %s" % ", ".join(sorted(offenders)))

    print("[cattle_pipeline_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
