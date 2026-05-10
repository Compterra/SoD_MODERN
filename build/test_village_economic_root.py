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
    profile = read("src/scripts/ZY_helper_scripts/sod_village_output_profile.py")
    production = read("src/triggers/ST99_other/entry_0036.py")
    farmers = read("src/scripts/ZC_parties/create_village_farmer_party.py")
    recruits = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    castle = read("src/scripts/ZY_helper_scripts/sod_castle_support_profile.py")
    boar = read("src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    notes = read("docs/reports/village_economic_root_audit.md")

    for token in (
        '"sod_get_village_output_profile"',
        "slot_center_sod_local_population",
        "slot_center_sod_local_health",
        "slot_town_prosperity",
        "slot_center_sod_local_prosperity",
        "slot_village_land_quality",
        "slot_village_number_of_cattle",
        "script_sod_get_center_food_profile",
        "script_sod_get_center_security_profile",
        "script_sod_get_center_tax_extraction_profile",
        ":tax_extraction_pressure",
        ":tax_retention_pct",
        "sod_center_modifier_production_output_pct",
        "sod_center_modifier_goods_export_supply_pct",
        "sod_center_modifier_cattle_growth_flat",
        "sod_center_modifier_cattle_output_pct",
        "slot_faction_boar_target_center",
        "slot_faction_boar_intimidation",
        "pt_boar_clan_fighters",
        "svs_looted",
        "svs_deserted",
        "(assign, reg0, \":workforce\")",
        "(assign, reg1, \":food_output\")",
        "(assign, reg2, \":cattle_output\")",
        "(assign, reg3, \":raw_material_output\")",
        "(assign, reg4, \":recruit_capacity\")",
        "(assign, reg5, \":labor_capacity\")",
        "(assign, reg6, \":fragility\")",
        "(assign, reg7, \":coercion_pressure\")",
        "(assign, reg8, \":reliability\")",
        "(assign, reg9, \":cattle_growth\")",
    ):
        assert_contains(profile, token)

    for token in (
        "script_sod_get_village_output_profile",
        ":food_output",
        ":cattle_output",
        ":raw_material_output",
        ":fragility",
        ":coercion_pressure",
        ":herd_delta",
        "script_center_change_trade_good_production",
        "itm_grain",
        "itm_flour",
        "itm_cattle_meat",
        "itm_wool",
        "itm_oil",
        "itm_iron",
    ):
        assert_contains(production, token)

    assert_contains(farmers, "script_sod_get_village_output_profile")
    assert_contains(farmers, ":village_workforce")
    assert_contains(farmers, ":village_labor_capacity")
    assert_contains(farmers, ":village_fragility")
    assert_contains(farmers, ":village_reliability")
    assert_contains(farmers, "party_remove_members")
    assert_contains(recruits, "get_center_recruitable_population")
    assert_contains(recruits, "spend_center_population_for_recruitment")

    assert_contains(castle, "script_sod_get_village_output_profile")
    assert_contains(castle, ":village_food_output")
    assert_contains(castle, ":village_labor_capacity")
    assert_contains(castle, ":village_recruit_capacity")
    assert_contains(boar, "script_sod_get_village_output_profile")
    assert_contains(boar, ":village_fragility")
    assert_contains(boar, ":village_coercion_pressure")
    assert_contains(boar, "script_sod_change_center_wealth")
    assert_contains(boar, "script_sod_change_center_local_prosperity")
    assert_contains(recon, "Village root economy")
    assert_contains(recon, "Tax extraction")
    assert_contains(recon, "script_sod_get_village_output_profile")

    assert_contains(notes, "Village Economic Root Audit")
    assert_contains(notes, "trade-good production")
    assert_contains(notes, "Fragility")

    print("[village_economic_root] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
