# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError("Missing expected token: %s" % needle)


def main() -> int:
    profile = read("src/scripts/ZY_helper_scripts/sod_center_security_profile.py")
    threat = read("src/scripts/ZD_centers/get_center_threat_level.py")
    bandits = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    desperation_trigger = read("src/triggers/ST04_weekly/entry_0105.py")
    desperation = read("src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py")
    raids = read("src/scripts/ZD_centers/process_village_raids.py")
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    caravan = read("src/scripts/ZB_economy_and_trade/cf_select_random_town_at_peace_with_faction_in_trade_route.py")
    offers = read("src/scripts/ZY_helper_scripts/sod_threat_board_generate_offers.py")
    economy = read("src/scripts/ZY_helper_scripts/sod_threat_board_apply_economy_effect.py")
    stakes = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_center_stakes.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    recon_brief = read("src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py")
    village_state = read("src/scripts/ZD_centers/village_set_state.py")
    population = read("src/scripts/ZZ_common_array_processing/update_center_population_supply.py")
    direct_loot = read("src/menus/other/continue_27.py")
    audit = read("build/audit_security_threat_system.py")

    for token in (
        '"sod_get_center_security_profile"',
        '"sod_get_center_security_economy_profile"',
        '"sod_apply_center_raid_resistance"',
        "sod_center_modifier_security_flat",
        "sod_center_modifier_threat_reduction_flat",
        "sod_center_modifier_raid_resistance_pct",
        "sod_center_modifier_bandit_spawn_reduction_pct",
        "sod_center_modifier_desperation_bandit_reduction_pct",
        "sod_center_modifier_warning_range_flat",
        "sod_center_modifier_patrol_response_pct",
        "sod_center_modifier_unrest_flat",
        "sod_center_modifier_unrest_reduction_flat",
        "slot_quest_sod_threat_sponsor_center",
        "slot_quest_sod_threat_tier",
        "slot_center_sod_local_population",
        "script_sod_get_center_food_profile",
        "fac_sod_merc_guild1",
        "fac_sod_merc_guild5",
        ":contract_security",
        ":trade_security_pct",
        ":recovery_security_pct",
        ":bandit_pressure_pct",
        ":raid_damage_pct",
        ":merchant_confidence",
        ":route_security",
        ":expected_defense",
        ":defense_gap",
        ":internal_threat",
        "(assign, reg10, \":vulnerability\")",
        "(assign, reg11, \":contract_security\")",
    ):
        assert_contains(profile, token)

    assert_contains(threat, "script_sod_get_center_security_profile")
    assert_contains(bandits, "script_sod_get_center_security_profile")
    assert_contains(bandits, "script_sod_get_center_security_economy_profile")
    assert_contains(bandits, ":bandit_spawn_reduction")
    assert_contains(bandits, ":desperation_bandit_reduction")
    assert_contains(bandits, ":bandit_pressure_pct")
    assert_contains(desperation_trigger, "script_sod_center_weekly_apply_security_desperation")
    assert_contains(desperation, "script_sod_get_center_security_economy_profile")
    assert_contains(desperation, ":desperation_bandit_reduction")
    assert_contains(desperation, ":bandit_pressure_pct")
    assert_contains(desperation, ":effective_threat")
    assert_contains(desperation, ":recovery_security_pct")
    assert_contains(raids, "script_sod_get_center_security_profile")
    assert_contains(raids, ":raid_resistance")
    assert_contains(raids, ":patrol_response")
    assert_contains(raids, "script_sod_get_center_security_economy_profile")
    assert_contains(raids, ":recovery_security_pct")
    assert_contains(construction, "script_sod_get_center_security_profile")
    assert_contains(construction, ":effective_threat")
    assert_contains(construction, ":unrest_pressure")
    assert_contains(caravan, "script_sod_get_center_security_profile")
    assert_contains(caravan, "script_sod_get_center_security_economy_profile")
    assert_contains(caravan, ":route_threat_penalty")
    assert_contains(caravan, ":trade_security_pct")
    assert_contains(caravan, ":route_security")
    assert_contains(offers, "script_sod_get_center_security_profile")
    assert_contains(offers, ":effective_threat")
    assert_contains(offers, ":vulnerability")
    assert_contains(economy, "script_sod_apply_center_raid_resistance")
    assert_contains(population, "script_sod_get_center_security_economy_profile")
    assert_contains(population, ":security_recovery_pct")
    assert_contains(population, ":bandit_pressure_pct")
    assert_contains(population, ":raid_damage_pct")
    assert_contains(population, ":merchant_confidence")
    assert_contains(village_state, "script_sod_apply_center_raid_resistance")
    assert_contains(direct_loot, "script_sod_apply_center_raid_resistance")
    assert_contains(direct_loot, "slot_center_sod_local_population")
    assert_contains(stakes, "Local stakes:")
    assert_contains(stakes, "reg(17), \":security\"")
    assert_contains(stakes, "reg(18), \":effective_threat\"")
    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68")
    assert_contains(recon_brief, "script_sod_get_center_security_profile")
    assert_contains(recon_brief, "The roads are")
    assert_contains(audit, "Security Threat System Audit")
    assert_contains(audit, "SECURITY_MODIFIERS")
    assert_contains(audit, "Population recovery security")

    print("[security_threat_system] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
