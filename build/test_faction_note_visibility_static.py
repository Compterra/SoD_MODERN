from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def assert_not_contains(text: str, needle: str, path: str) -> None:
    if needle in text:
        raise AssertionError(f"{path} unexpectedly contains {needle!r}")


def main() -> None:
    helper_path = "src/scripts/ZY_helper_scripts/sod_faction_note_visibility.py"
    notes_path = "src/scripts/ZF_factions/update_faction_notes.py"
    traveler_path = "src/scripts/ZF_factions/update_faction_traveler_notes.py"
    helper = read(helper_path)
    notes = read(notes_path)
    traveler = read(traveler_path)

    for needle in (
        '"sod_faction_should_show_notes"',
        '"fac_player_supporters_faction"',
        '"fac_kingdom_6"',
        "rebel_factions_begin, rebel_factions_end",
        "Defeated native kingdoms intentionally retain their historical Notes entry",
        "eq, \":requires_realm_presence\", 1",
        "slot_faction_state, sfs_active",
        "try_for_range, \":center_no\", centers_begin, centers_end",
        "try_for_range, \":troop_no\", kingdom_heroes_begin, kingdom_heroes_end",
        "neq, \":troop_no\", \":faction_leader\"",
        "slot_troop_occupation, slto_kingdom_hero",
        "this_or_next|eq, \":has_fief\", 1",
        "eq, \":has_vassal\", 1",
    ):
        assert_contains(helper, needle, helper_path)

    assert_not_contains(
        helper,
        'is_between, ":faction_no", kingdoms_begin, kingdoms_end',
        helper_path,
    )

    for text, path in ((notes, notes_path), (traveler, traveler_path)):
        assert_contains(text, "script_sod_faction_should_show_notes", path)

    assert_contains(notes, "Clearing both note types removes an obsolete realm", notes_path)
    assert_contains(notes, "add_faction_note_from_sreg, \":faction_no\", 0, s68, 0", notes_path)
    assert_contains(notes, "add_faction_note_from_sreg, \":faction_no\", 1, s68, 0", notes_path)
    assert_contains(traveler, "add_faction_note_from_sreg, \":faction_no\", 1, s68, 0", traveler_path)

    print("[faction_note_visibility] OK")


if __name__ == "__main__":
    main()
