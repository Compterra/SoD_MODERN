from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text, needle, path):
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main():
    helper_path = "src/scripts/ZY_helper_scripts/sod_realm_military_centralization_profile.py"
    party_path = "src/scripts/ZC_parties/party_get_ideal_size.py"
    law_report_path = "src/scripts/ZZ_common_array_processing/sod_law_reports.py"

    helper = read(helper_path)
    party = read(party_path)
    law_report = read(law_report_path)

    for needle in [
        "sod_get_realm_military_centralization_profile",
        "slot_faction_law_centralization",
        "slot_faction_law_militarization",
        "slot_faction_law_ruler_party_size_modifier",
        "slot_faction_law_lord_party_size_modifier",
        "slot_faction_law_noble_happiness",
        "slot_faction_law_legitimacy",
        "slot_faction_law_unrest",
        "(val_clamp, \":centralization\", -40, 61)",
        "(assign, reg2, \":ruler_centralization_modifier\")",
        "(assign, reg3, \":vassal_centralization_modifier\")",
    ]:
        assert_contains(helper, needle, helper_path)

    for needle in [
        "script_sod_get_realm_military_centralization_profile",
        "script_sod_get_castle_support_profile",
        "script_sod_get_town_market_profile",
        "script_sod_get_village_output_profile",
        ":ruler_law_modifier",
        ":vassal_law_modifier",
        ":centralized_fief_drag",
        ":decentralized_fief_bonus",
        ":military_fief_bonus",
        ":castle_military_power",
        ":town_liquidity",
        ":village_recruit_capacity",
    ]:
        assert_contains(party, needle, party_path)

    for needle in [
        "Military centralization",
        "Ruler host modifier",
        "Vassal host modifier",
        "Centralization {reg30}",
        "Militarization {reg31}",
        "Noble happiness {reg34}",
        "Unrest pressure {reg35}",
    ]:
        assert_contains(law_report, needle, law_report_path)

    print("[lord_party_size_centralization] OK")


if __name__ == "__main__":
    main()
