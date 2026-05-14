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
    items = read("compile/module_items.py")
    council = read("src/menus/kingdom/sa_council.py")
    after_dialog = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_after_6.py")
    troops = read("compile/module_troops.py")

    for item_id in (
        "dynasty_outfit",
        "dynasty_oufit_greaves",
        "elephant_guard_gloves",
    ):
        item_line = next((line for line in items.splitlines() if f'["{item_id}"' in line), "")
        if "itp_civilian" not in item_line:
            raise AssertionError(f"{item_id} must be civilian-safe for castle scenes")
        assert_contains(council, f'"itm_{item_id}"')
        assert_contains(after_dialog, f'"itm_{item_id}"')
        assert_contains(troops, f"itm_{item_id}")

    if 'troop_clear_inventory, "trp_sod_strategy_advisor"' not in council:
        raise AssertionError("Council conversion should reset Cassian to court equipment")
    if 'troop_clear_inventory, "trp_sod_strategy_advisor"' not in after_dialog:
        raise AssertionError("Dialogue conversion should reset Cassian to court equipment")

    print("[cassian_civilian_clothes_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
