from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    location_notes = read("src/scripts/ZH_heroes/update_troop_location_notes.py")
    troop_notes = read("src/scripts/ZH_heroes/update_troop_notes.py")
    faction_notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    faction_relations_report = read("src/menus/0000_hardcoded_mb1011/faction_relations_report.py")
    kill_hero = read("src/scripts/ZF_factions/kill_kingdom_hero.py")
    escape = read("src/scripts/ZC_parties/randomly_make_prisoner_heroes_escape_from_party.py")
    fief_counts = read("src/scripts/ZD_centers/print_troop_owned_centers_in_numbers_to_s0.py")

    assert_contains(location_notes, '(str_store_string, s68, "@She")')
    assert_contains(location_notes, '(str_store_string, s68, "@He")')
    assert_contains(location_notes, '(str_store_string, s69, "@her")')
    assert_contains(location_notes, '(str_store_string, s69, "@him")')
    assert_contains(location_notes, "@{s68} is dead.")
    assert_contains(location_notes, "The last time you saw {s69}, {s1}")
    assert_contains(location_notes, "The last time you heard about {s69}, {s1}")
    assert_not_contains(location_notes, "{reg1?She:He}")
    assert_not_contains(location_notes, "{reg1?her:him}")

    assert_contains(troop_notes, '(str_store_string, s69, "@She")')
    assert_contains(troop_notes, '(str_store_string, s69, "@He")')
    assert_contains(troop_notes, "Relation to you: {s70} ({reg60}).")
    assert_contains(troop_notes, "Temperament: {s74}.")
    assert_contains(troop_notes, "Family ties: {s75}.")
    for token in (
        "slot_troop_spouse",
        "slot_troop_father",
        "slot_troop_mother",
        "slot_troop_sibling",
        "slot_troop_son",
        "slot_troop_daughter",
    ):
        assert_contains(troop_notes, token)
    assert_contains(troop_notes, "martial; values command, courage, and decisive campaigning")
    assert_contains(troop_notes, "quarrelsome; quick to feud and slow to forget insults")
    assert_contains(troop_notes, "upstanding; principled, dutiful, and politically steady")
    assert_contains(troop_notes, "Household morale: {s60}.")
    assert_contains(troop_notes, "Claimant politics: {s73}.")
    assert_contains(troop_notes, "(str_store_faction_name_link, s71")
    assert_contains(troop_notes, '(try_for_range, ":employer", native_kingdoms_begin, native_kingdoms_end)')
    assert_contains(troop_notes, '(is_between, ":claimant_parent", native_kingdoms_begin, native_kingdoms_end)')
    assert_not_contains(troop_notes, '(try_for_range, ":employer", kingdoms_begin, kingdoms_end)')
    assert_not_contains(troop_notes, '(is_between, ":claimant_parent", kingdoms_begin, kingdoms_end)')
    assert_not_contains(troop_notes, "(str_store_string_reg, s60, s69)")
    assert_not_contains(troop_notes, "str_relation_mnus_100_ns")
    assert_not_contains(troop_notes, "{reg3?She:He}")
    assert_not_contains(troop_notes, '"@nowhere"')

    assert_contains(kill_hero, '(str_store_string, s68, "@She")')
    assert_contains(kill_hero, '(str_store_string, s68, "@He")')
    assert_contains(kill_hero, "@{s68} is dead.")
    assert_not_contains(kill_hero, "{reg1?She:He}")

    assert_contains(escape, '(str_store_string, s68, "@One of your prisoners, ")')
    assert_contains(escape, "(str_clear, s68)")
    assert_contains(escape, "@{s68}{s1} has escaped from captivity!")
    assert_not_contains(escape, "{reg0?One of your prisoners, :}")

    for token in ('"@village"', '"@villages"', '"@castle"', '"@castles"', '"@town"', '"@towns"'):
        assert_contains(fief_counts, token)
    assert_contains(fief_counts, "@{reg0} {s68}")
    assert_not_contains(fief_counts, "village{reg1?s:}")
    assert_not_contains(fief_counts, "castle{reg1?s:}")
    assert_not_contains(fief_counts, "town{reg1?s:}")

    assert_contains(faction_notes, "Recorded holdings: {s8}.")
    assert_contains(faction_notes, "Recorded vassals: {s10}.")
    assert_not_contains(faction_notes, '"@nowhere"')
    assert_not_contains(faction_notes, '"@noone"')

    assert_contains(faction_relations_report, "Your relations with the realms are")
    assert_contains(faction_relations_report, '"{s98}"')
    assert_contains(faction_relations_report, "str_store_string_reg, s96, s97")
    assert_contains(faction_relations_report, "str_store_string_reg, s95, s96")
    assert_not_contains(faction_relations_report, "Your relation with the factions are")
    assert_not_contains(faction_relations_report, '"{s1}"')
    assert_not_contains(faction_relations_report, "@{s2}^")

    print("test_hero_note_text_static: OK")


if __name__ == "__main__":
    main()
