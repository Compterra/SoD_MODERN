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
    tax = read("src/scripts/ZY_helper_scripts/sod_tax_extraction_profile.py")
    village = read("src/scripts/ZY_helper_scripts/sod_village_output_profile.py")
    town = read("src/scripts/ZY_helper_scripts/sod_town_market_profile.py")
    castle = read("src/scripts/ZY_helper_scripts/sod_castle_support_profile.py")
    faith = read("src/scripts/ZY_helper_scripts/sod_faith_system.py")
    laws = read("src/scripts/ZZ_common_array_processing/sod_law_reports.py")
    recon = read("src/scripts/ZD_centers/update_center_recon_notes.py")
    audit = read("build/audit_tax_social_pressure.py")

    for token in (
        '"sod_get_realm_tax_pressure_profile"',
        "slot_faction_law_tax_peasants",
        "slot_faction_law_tax_townspeople",
        "slot_faction_law_tax_nobles",
        "slot_faction_law_commoner_happiness",
        "slot_faction_law_merchant_happiness",
        "slot_faction_law_noble_happiness",
        "slot_faction_law_clergy_happiness",
        "slot_faction_law_unrest",
        "slot_faction_law_legitimacy",
        "slot_faction_law_holy_modifier",
        "slot_faction_diplomacy_decree_war_taxes",
        ":peasant_extraction",
        ":merchant_tariff_pressure",
        ":noble_obligation_pressure",
        ":clergy_faith_support_pressure",
        ":war_tax_pressure",
        ":total_social_pressure",
        ":revenue_modifier",
        ":recovery_modifier",
        ":migration_modifier",
        ":trade_volume_modifier",
        ":unrest_pressure",
        "(assign, reg15, \":tariff_capture_pct\")",
    ):
        assert_contains(tax, token)

    assert_contains(tax, "script_sod_get_realm_tax_pressure_profile")
    assert_contains(tax, "(assign, \":tax_pressure\", \":peasant_extraction\")")
    assert_contains(tax, "(assign, \":tax_pressure\", \":merchant_tariff_pressure\")")
    assert_contains(tax, "(assign, \":tax_pressure\", \":noble_obligation_pressure\")")

    for raw, tokens in (
        (village, (":peasant_extraction_pressure", ":commoner_happiness_delta", ":peasant_condition_drag")),
        (town, (":merchant_tariff_pressure", ":merchant_tariff_volume_drag", ":merchant_happiness_delta")),
        (castle, (":noble_obligation_pressure", ":noble_happiness_delta", ":noble_obligation_revenue")),
        (faith, (":clergy_faith_support_pressure", ":clergy_happiness_delta", ":clergy_institution_bonus")),
    ):
        for token in tokens:
            assert_contains(raw, token)

    for token in (
        "Tax social pressure",
        "Peasant extraction",
        "Merchant tariffs",
        "Noble obligations",
        "Clergy/faith support",
        "War taxes",
        "Happiness deltas",
    ):
        assert_contains(laws, token)

    for token in (
        "Local tax burden",
        "peasant extraction",
        "merchant tariffs",
        "noble obligations",
        "clergy support",
        "war taxes",
    ):
        assert_contains(recon, token)

    for token in (
        "Tax Social Pressure Audit",
        "Peasant extraction",
        "Merchant tariffs",
        "Noble obligations",
        "Clergy/faith support",
        "War taxes",
    ):
        assert_contains(audit, token)

    print("[tax_social_pressure] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
