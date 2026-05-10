from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text, needle, path):
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main():
    helper_path = "src/scripts/ZY_helper_scripts/sod_lord_reinforcement_support_profile.py"
    hire_path = "src/scripts/ZC_parties/hire_men_to_kingdom_hero_party.py"
    reinforce_path = "src/scripts/ZC_parties/cf_reinforce_party.py"
    activate_path = "src/scripts/ZF_factions/activate_deactivate_player_faction.py"

    helper = read(helper_path)
    hire = read(hire_path)
    reinforce = read(reinforce_path)
    activate = read(activate_path)

    for needle in [
        "# COST: O(owned centers + bound villages)",
        "sod_get_lord_reinforcement_support_profile",
        "script_sod_get_realm_military_centralization_profile",
        "script_sod_get_castle_support_profile",
        "script_sod_get_town_market_profile",
        "script_sod_get_village_output_profile",
        ":readiness",
        ":support_score",
        ":cost_pct",
        ":wealth_pct",
        ":security_drag",
        ":food_drag",
        "(assign, reg0, \":readiness\")",
        "(assign, reg2, \":rounds\")",
        "(assign, reg3, \":cost_pct\")",
        "(assign, reg4, \":wealth_pct\")",
    ]:
        assert_contains(helper, needle, helper_path)

    for needle in [
        "script_sod_get_lord_reinforcement_support_profile",
        ":reinforcement_readiness",
        ":reinforcement_support",
        ":effective_reinforcement_cost",
        ":wealth_pct",
        "(ge, \":reinforcement_readiness\", 35)",
        "(val_sub, \":cur_wealth\", \":effective_reinforcement_cost\")",
        "Muster readiness",
        "estate support",
    ]:
        assert_contains(hire, needle, hire_path)

    for needle in [
        "(eq, \":party_type\", spt_kingdom_hero_party)",
        "(party_stack_get_troop_id, \":leader\", \":party_no\", 0)",
        "(store_troop_faction, \":leader_faction\", \":leader\")",
        "(eq, \":leader_faction\", \"fac_player_supporters_faction\")",
        "(assign, \":party_faction\", \"fac_player_supporters_faction\")",
        "(troop_get_slot, \":party_faction\",  \":leader\", slot_troop_original_faction)",
        "(faction_get_slot, \":party_template_a\", \":party_faction\", slot_faction_reinforcements_a)",
    ]:
        assert_contains(reinforce, needle, reinforce_path)

    for needle in [
        "pt_sod_1_reinforcements_a",
        "pt_sod_2_reinforcements_a",
        "pt_sod_3_reinforcements_a",
        "pt_sod_4_reinforcements_a",
        "pt_sod_5_reinforcements_a",
    ]:
        assert_contains(activate, needle, activate_path)

    print("[lord_reinforcement_support] OK")


if __name__ == "__main__":
    main()
