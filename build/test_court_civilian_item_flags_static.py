# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COURT_VISIBLE_ITEMS = (
    "antboots2",
    "margloves2",
    "marboots1",
    "marboots3",
    "villgloves1",
    "villgloves2",
    "villboots1",
    "villboots2",
    "noble_start_boots",
    "bashkir_boots",
    "oprichnik_boots",
    "noble_padded_leather",
    "dynasty_tabard",
    "black_army_leather_gloves",
    "dynasty_outfit",
    "dynasty_oufit_greaves",
    "elephant_guard_gloves",
    "dark_plate2",
    "darkboots",
    "darkgauntlets",
    "horned_helm1",
)

EXPECTED_USAGE_FILES = (
    ROOT / "src/scripts/ZZ_common_array_processing/sod_initialize_vassals.py",
    ROOT / "src/scripts/ZZ_common_array_processing/sod_initialize_strategy_advisor.py",
    ROOT / "src/menus/kingdom/sa_council.py",
    ROOT / "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_after_6.py",
    ROOT / "compile/module_troops.py",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def item_line(items: str, item_id: str) -> str:
    for line in items.splitlines():
        if f'["{item_id}"' in line:
            return line
    raise AssertionError(f"Missing item definition for {item_id}")


def main() -> int:
    items = read("compile/module_items.py")
    usage_text = "\n".join(path.read_text(encoding="utf-8") for path in EXPECTED_USAGE_FILES)

    missing_flags = []
    missing_usage = []
    for item_id in COURT_VISIBLE_ITEMS:
        line = item_line(items, item_id)
        if "itp_civilian" not in line:
            missing_flags.append(item_id)
        if f'"itm_{item_id}"' not in usage_text and f"itm_{item_id}" not in usage_text:
            missing_usage.append(item_id)

    if missing_flags:
        raise AssertionError(
            "Court-visible clothing items must be civilian-safe: "
            + ", ".join(missing_flags)
        )
    if missing_usage:
        raise AssertionError(
            "Test list should only include items used by court/start/civilian outfit flows: "
            + ", ".join(missing_usage)
        )

    print("[court_civilian_item_flags_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
