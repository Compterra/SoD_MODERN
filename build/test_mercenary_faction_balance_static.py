from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text, needle):
    assert needle in text, f"Missing expected text: {needle}"


def assert_not_contains(text, needle):
    assert needle not in text, f"Unexpected text: {needle}"


def test_elephant_and_boar_base_slots_are_expressive() -> None:
    constants = read("src/constants/module_constants.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")

    assert_contains(constants, 'elephant_guard_tier_1_unit_1  = "trp_elephant_guard_tribesman"')
    assert_contains(constants, 'elephant_guard_tier_1_unit_2  = "trp_elephant_guard_spearman"')
    assert_contains(constants, 'boar_clan_tier_1_unit_1       = "trp_boar_clan_clansman"')
    assert_contains(constants, 'boar_clan_tier_1_unit_2       = "trp_boar_clan_rider"')
    assert_contains(constants, 'boar_clan_noble       = "trp_boar_clan_tusk_rider"')

    assert_contains(game_start, "boar_clan_tier_1_unit_1")
    assert_contains(game_start, "boar_clan_tier_1_unit_2")
    assert_contains(game_start, "boar_clan_noble")
    assert_not_contains(game_start, '(faction_set_slot, "fac_sod_merc_guild7", slot_guild_tier_1_unit_2, "trp_boar_clan_clansman")')


def test_balance_audit_docs_record_recommendations() -> None:
    faction_audit = read("docs/MERCENARY_FACTION_BALANCE_AUDIT.md")
    cost_audit = read("docs/MERCENARY_TROOP_COST_ROLE_AUDIT.md")

    assert_contains(faction_audit, "The goal should not be")
    assert_contains(faction_audit, "Elephant Guard now uses `trp_elephant_guard_tribesman` / `trp_elephant_guard_spearman`")
    assert_contains(faction_audit, "Boar Clan now uses `trp_boar_clan_clansman` / `trp_boar_clan_rider`")
    assert_contains(faction_audit, "Use contract price, stock, relation, and world pressure as the first tuning levers before editing troop stats")

    assert_contains(cost_audit, "Mercenary Troop Cost And Role Audit")
    assert_contains(cost_audit, "script_game_get_troop_wage")
    assert_contains(cost_audit, "Elephant Guard second base slot now uses `trp_elephant_guard_spearman`")
    assert_contains(cost_audit, "Boar Clan second base slot now uses `trp_boar_clan_rider`")
