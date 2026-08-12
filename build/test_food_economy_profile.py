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
    profile = read("src/scripts/ZY_helper_scripts/sod_center_food_profile.py")
    goods = read("src/scripts/ZY_helper_scripts/sod_consume_center_trade_goods.py")
    trade = read("src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py")
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    security = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    recon_brief = read("src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py")
    notes = read("docs/reports/food_economy_input_audit.md")

    for token in (
        '"sod_get_center_food_profile"',
        "slot_party_food_store",
        "script_center_get_food_store_limit",
        "script_center_get_food_consumption",
        "sod_center_modifier_food_security_flat",
        "(assign, reg0, \":food_store\")",
        "(assign, reg1, \":food_store_limit\")",
        "(assign, reg2, \":food_consumption\")",
        "(assign, reg3, \":food_days\")",
        "(assign, reg4, \":food_security\")",
        "(assign, reg5, \":food_capacity_ratio\")",
        "(assign, reg6, \":food_pressure\")",
        "(assign, reg7, \":food_unrest_pressure\")",
        "val_clamp, \":food_security\", 0, 2001",
    ):
        assert_contains(profile, token)

    assert_contains(goods, "script_sod_get_center_food_profile")
    assert_contains(goods, ":food_pressure")
    assert_contains(goods, "script_sod_change_center_wealth")
    assert_contains(goods, "script_change_center_health")
    assert_contains(goods, "script_change_center_prosperity")

    assert_contains(trade, "script_sod_get_center_food_profile")
    assert_contains(trade, ":food_pressure")
    assert_contains(trade, "script_sod_center_apply_food_delta")
    assert_contains(trade, "slot_party_food_store")

    assert_contains(construction, "script_sod_get_center_food_profile")
    assert_contains(construction, ":food_security")
    assert_contains(security, "script_sod_get_center_food_profile")
    assert_contains(security, ":food_unrest_pressure")
    assert_contains(population, "script_sod_get_center_food_profile")
    assert_contains(population, ":food_security")
    assert_contains(population, ":food_pressure")
    assert_contains(population, "lt, \":food_security\", 300")
    assert_contains(population, "ge, \":food_security\", 1400")
    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68")
    assert_contains(recon_brief, "Food stores")
    assert_contains(recon_brief, "script_sod_get_center_food_profile")

    assert_contains(notes, "Food Economy Input Audit")
    assert_contains(notes, "health")
    assert_contains(notes, "Migration and population")
    assert_contains(notes, "Construction labor")
    assert_contains(notes, "Trade demand")
    assert_contains(notes, "unrest")

    print("[food_economy_profile] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
