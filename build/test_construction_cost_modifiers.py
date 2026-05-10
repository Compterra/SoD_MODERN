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
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    presentation = read("src/presentations/0020_sod_fief_management/sod_fief_management.py")
    weekly = read("src/triggers/ST04_weekly/entry_0123.py")

    for token in (
        '"sod_get_center_construction_cost"',
        "sod_center_modifier_construction_cost_pct",
        "(val_mul, \":cost\", \":construction_cost_pct\")",
        "(val_div, \":cost\", 100)",
        "(assign, reg1, \":construction_cost_pct\")",
    ):
        assert_contains(construction, token)

    for token in (
        "script_sod_get_center_construction_cost",
        "$pres_sod_fief_selected",
        "$pres_sod_fief_selected_building",
        "local construction cost factor",
        "(assign, reg13, reg1)",
    ):
        assert_contains(presentation, token)

    for token in (
        "script_sod_get_center_construction_cost",
        ":ai_affordability_cost",
        ":ai_improvement_cost",
        "(store_div, \":ai_improvement_cost\", \":improvement_cost\", 4)",
    ):
        assert_contains(weekly, token)

    print("[construction_cost_modifiers] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
