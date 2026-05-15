from __future__ import annotations

import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "ids"))
sys.path.insert(0, str(COMPILE / "headers"))

import module_constants  # type: ignore
import ID_factions  # type: ignore
import ID_items  # type: ignore
import ID_parties  # type: ignore
import ID_quests  # type: ignore
import ID_troops  # type: ignore


ID_MODULE_NAMES = (
    "ID_factions",
    "ID_items",
    "ID_map_icons",
    "ID_meshes",
    "ID_parties",
    "ID_quests",
    "ID_scene_props",
    "ID_scenes",
    "ID_strings",
    "ID_troops",
)

SOURCE_ASSIGNMENT_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=")


def load_id_namespaces() -> dict[str, dict[str, int]]:
    namespaces: dict[str, dict[str, int]] = {}
    for module_name in ID_MODULE_NAMES:
        module = __import__(module_name)
        namespaces[module_name] = {
            name: value
            for name, value in vars(module).items()
            if isinstance(value, int)
        }
    return namespaces


def source_constant_names() -> set[str]:
    names: set[str] = set()
    source = ROOT / "src" / "constants" / "module_constants.py"
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        match = SOURCE_ASSIGNMENT_RE.match(line)
        if match:
            names.add(match.group(1))
    return names


def resolve_value(
    value: object,
    namespaces: dict[str, dict[str, int]],
) -> tuple[str | None, int | None]:
    if isinstance(value, int):
        return "int", value
    if not isinstance(value, str):
        return None, None
    for namespace, assignments in namespaces.items():
        if value in assignments:
            return namespace, assignments[value]
    return None, None


def test_resolvable_generated_constant_ranges_are_ordered() -> None:
    namespaces = load_id_namespaces()
    constants = vars(module_constants)
    names = source_constant_names()
    issues: list[str] = []

    for begin_name in sorted(name for name in names if name.endswith("_begin")):
        stem = begin_name[: -len("_begin")]
        end_name = None
        end_is_inclusive = False
        if f"{stem}_end" in names:
            end_name = f"{stem}_end"
        elif f"{stem}_end_minus_one" in names:
            end_name = f"{stem}_end_minus_one"
            end_is_inclusive = True
        if end_name is None:
            continue

        begin_namespace, begin_index = resolve_value(constants.get(begin_name), namespaces)
        end_namespace, end_index = resolve_value(constants.get(end_name), namespaces)
        if begin_namespace is None or end_namespace is None:
            continue
        if end_is_inclusive:
            end_index += 1

        if begin_namespace != "int" and end_namespace != "int" and begin_namespace != end_namespace:
            issues.append(
                f"{begin_name}/{end_name} crosses namespaces: "
                f"{begin_namespace} -> {end_namespace}"
            )
        elif begin_index >= end_index:
            issues.append(
                f"{begin_name}/{end_name} is empty or inverted: "
                f"{begin_index} >= {end_index}"
            )

    assert not issues, "\n".join(issues)


def test_party_range_constants_resolve_to_existing_generated_party_ids() -> None:
    party_names = {
        name
        for name, value in vars(ID_parties).items()
        if name.startswith("p_") and isinstance(value, int)
    }
    constants = vars(module_constants)
    checked_constants = [
        "training_grounds_begin",
        "training_grounds_end",
        "swadian_merc_parties_begin",
        "swadian_merc_parties_end",
        "vaegir_merc_parties_begin",
        "vaegir_merc_parties_end",
        "merc_parties_begin",
        "merc_parties_end",
    ]
    missing = [
        f"{name}={constants.get(name)!r}"
        for name in checked_constants
        if constants.get(name) not in party_names
    ]
    assert not missing, "party range constant(s) point at missing party IDs: " + ", ".join(missing)


def test_semantic_troop_and_faction_ranges_do_not_include_story_npcs() -> None:
    troop_names_by_id = {
        value: name
        for name, value in vars(ID_troops).items()
        if name.startswith("trp_") and isinstance(value, int)
    }
    faction_names_by_id = {
        value: name
        for name, value in vars(ID_factions).items()
        if name.startswith("fac_") and isinstance(value, int)
    }

    village_elder_begin = ID_troops.trp_village_1_elder
    village_elder_end = ID_troops.trp_rtc_garran_ashwake
    assert module_constants.village_elders_begin == "trp_village_1_elder"
    assert module_constants.village_elders_end == "trp_rtc_garran_ashwake"
    assert village_elder_end - village_elder_begin == 90
    for troop_id in range(village_elder_begin, village_elder_end):
        assert re.match(r"^trp_village_\d+_elder$", troop_names_by_id[troop_id])

    assert ID_troops.trp_rtc_garran_ashwake not in range(village_elder_begin, village_elder_end)
    assert ID_troops.trp_seven_ash_wulfred_carr not in range(village_elder_begin, village_elder_end)

    guild_master_begin = ID_troops.trp_black_army_guild_master
    guild_master_end = ID_troops.trp_slave_hero
    assert module_constants.guild_masters_begin == "trp_black_army_guild_master"
    assert module_constants.guild_masters_end == "trp_slave_hero"
    assert guild_master_end - guild_master_begin == 7
    for troop_id in range(guild_master_begin, guild_master_end):
        assert re.match(r"^trp_.*guild_master$", troop_names_by_id[troop_id])
    assert ID_troops.trp_slave_hero not in range(guild_master_begin, guild_master_end)

    guild_begin = ID_factions.fac_sod_merc_guild1
    guild_end = ID_factions.fac_kingdom_6_mercenaries
    assert module_constants.guilds_begin == "fac_sod_merc_guild1"
    assert module_constants.guilds_end == "fac_kingdom_6_mercenaries"
    assert guild_end - guild_begin == 7
    for faction_id in range(guild_begin, guild_end):
        assert re.match(r"^fac_sod_merc_guild\d+$", faction_names_by_id[faction_id])
    assert ID_factions.fac_kingdom_6_mercenaries not in range(guild_begin, guild_end)


def _names_by_id(module: object, prefix: str) -> dict[int, str]:
    return {
        value: name
        for name, value in vars(module).items()
        if name.startswith(prefix) and isinstance(value, int)
    }


def _assert_range_names(
    label: str,
    begin: int,
    end: int,
    names_by_id: dict[int, str],
    pattern: str,
    expected_count: int | None = None,
) -> None:
    assert begin < end, f"{label} range is empty or inverted"
    if expected_count is not None:
        assert end - begin == expected_count, f"{label} count changed: {end - begin}"
    bad = [
        names_by_id.get(identifier, f"<missing {identifier}>")
        for identifier in range(begin, end)
        if not re.match(pattern, names_by_id.get(identifier, ""))
    ]
    assert not bad, f"{label} range has unexpected members: {bad[:20]}"


def test_semantic_center_and_service_troop_ranges_are_pure() -> None:
    troop_names_by_id = _names_by_id(ID_troops, "trp_")
    party_names_by_id = _names_by_id(ID_parties, "p_")

    _assert_range_names(
        "towns",
        ID_parties.p_town_1,
        ID_parties.p_castle_1,
        party_names_by_id,
        r"^p_town_\d+$",
        18,
    )
    _assert_range_names(
        "castles",
        ID_parties.p_castle_1,
        ID_parties.p_village_1,
        party_names_by_id,
        r"^p_castle_\d+$",
        40,
    )
    _assert_range_names(
        "villages",
        ID_parties.p_village_1,
        ID_parties.p_salt_mine,
        party_names_by_id,
        r"^p_village_\d+$",
        90,
    )
    _assert_range_names(
        "walled centers",
        ID_parties.p_town_1,
        ID_parties.p_village_1,
        party_names_by_id,
        r"^p_(town|castle)_\d+$",
        58,
    )
    _assert_range_names(
        "centers",
        ID_parties.p_town_1,
        ID_parties.p_salt_mine,
        party_names_by_id,
        r"^p_(town|castle|village)_\d+$",
        148,
    )
    assert ID_parties.p_salt_mine not in range(ID_parties.p_town_1, ID_parties.p_salt_mine)

    assert module_constants.imperial_invasion_entry_villages_begin == "p_village_16"
    assert module_constants.imperial_invasion_entry_villages_end == "p_village_67"
    _assert_range_names(
        "imperial invasion entry villages",
        ID_parties.p_village_16,
        ID_parties.p_village_67,
        party_names_by_id,
        r"^p_village_\d+$",
        8,
    )
    assert [
        party_names_by_id[index]
        for index in range(ID_parties.p_village_16, ID_parties.p_village_67)
    ] == [
        "p_village_16",
        "p_village_21",
        "p_village_35",
        "p_village_41",
        "p_village_46",
        "p_village_47",
        "p_village_48",
        "p_village_61",
    ]

    service_ranges = [
        ("arena masters", ID_troops.trp_town_1_arena_master, ID_troops.trp_town_1_armorer, r"^trp_town_\d+_arena_master$", 18),
        ("armor merchants", ID_troops.trp_town_1_armorer, ID_troops.trp_town_1_weaponsmith, r"^trp_town_\d+_armorer$", 18),
        ("weapon merchants", ID_troops.trp_town_1_weaponsmith, ID_troops.trp_town_1_tavernkeeper, r"^trp_town_\d+_weaponsmith$", 18),
        ("tavernkeepers", ID_troops.trp_town_1_tavernkeeper, ID_troops.trp_town_1_merchant, r"^trp_town_\d+_tavernkeeper$", 18),
        ("goods merchants", ID_troops.trp_town_1_merchant, ID_troops.trp_town_1_horse_merchant, r"^trp_(town_\d+|salt_mine)_merchant$", 19),
        ("horse merchants", ID_troops.trp_town_1_horse_merchant, ID_troops.trp_town_1_mayor, r"^trp_town_\d+_horse_merchant$", 18),
        ("mayors", ID_troops.trp_town_1_mayor, ID_troops.trp_village_1_elder, r"^trp_town_\d+_mayor$", 18),
        ("town walkers", ID_troops.trp_town_walker_1, ID_troops.trp_village_walker_1, r"^trp_town_walker_\d+$", 2),
        ("village walkers", ID_troops.trp_village_walker_1, ID_troops.trp_spy_walker_1, r"^trp_village_walker_\d+$", 2),
        ("spy walkers", ID_troops.trp_spy_walker_1, ID_troops.trp_tournament_master, r"^trp_spy_walker_\d+$", 2),
        ("ransom brokers", ID_troops.trp_ransom_broker_1, ID_troops.trp_tavern_traveler_1, r"^trp_ransom_broker_\d+$", 10),
        ("tavern travelers", ID_troops.trp_tavern_traveler_1, ID_troops.trp_tavern_bookseller_1, r"^trp_tavern_traveler_\d+$", 10),
        ("tavern booksellers", ID_troops.trp_tavern_bookseller_1, ID_troops.trp_tavern_minstrel_1, r"^trp_tavern_bookseller_\d+$", 2),
        ("tavern minstrels", ID_troops.trp_tavern_minstrel_1, ID_troops.trp_npc1, r"^trp_tavern_minstrel_\d+$", 1),
    ]
    for label, begin, end, pattern, expected_count in service_ranges:
        _assert_range_names(label, begin, end, troop_names_by_id, pattern, expected_count)


def test_semantic_actor_and_quest_ranges_are_stable() -> None:
    troop_names_by_id = _names_by_id(ID_troops, "trp_")
    quest_names_by_id = _names_by_id(ID_quests, "qst_")
    faction_names_by_id = _names_by_id(ID_factions, "fac_")

    _assert_range_names(
        "kings",
        ID_troops.trp_kingdom_1_lord,
        ID_troops.trp_knight_1_1,
        troop_names_by_id,
        r"^trp_kingdom_\d+_lord$",
        6,
    )
    _assert_range_names(
        "pretenders",
        ID_troops.trp_kingdom_1_pretender,
        ID_troops.trp_black_army_guild_master,
        troop_names_by_id,
        r"^trp_kingdom_\d+_pretender$",
        5,
    )
    _assert_range_names(
        "kingdom ladies",
        ID_troops.trp_knight_1_1_wife,
        ID_troops.trp_heroes_end,
        troop_names_by_id,
        r"^trp_knight_\d+_\d+_(wife|daughter)$",
        20,
    )
    _assert_range_names(
        "companions",
        ID_troops.trp_npc1,
        ID_troops.trp_diego_companion,
        troop_names_by_id,
        r"^trp_npc\d+$",
        16,
    )
    _assert_range_names(
        "special companions",
        ID_troops.trp_diego_companion,
        ID_troops.trp_kingdom_heroes_including_player_begin,
        troop_names_by_id,
        r"^trp_diego_companion$",
        1,
    )
    _assert_range_names(
        "rebel factions",
        ID_factions.fac_kingdom_1_rebels,
        ID_factions.fac_kingdoms_end,
        faction_names_by_id,
        r"^fac_kingdom_\d+_rebels$",
        5,
    )

    # M&B 1.011 Native-era scripts treat kingdoms_begin/end as the broad
    # political realm band, including player supporters and rebel claimants.
    broad_kingdom_members = [
        faction_names_by_id[faction_id]
        for faction_id in range(ID_factions.fac_player_supporters_faction, ID_factions.fac_kingdoms_end)
    ]
    assert broad_kingdom_members == [
        "fac_player_supporters_faction",
        "fac_kingdom_1",
        "fac_kingdom_2",
        "fac_kingdom_3",
        "fac_kingdom_4",
        "fac_kingdom_5",
        "fac_kingdom_6",
        "fac_kingdom_1_rebels",
        "fac_kingdom_2_rebels",
        "fac_kingdom_3_rebels",
        "fac_kingdom_4_rebels",
        "fac_kingdom_5_rebels",
    ]

    assert module_constants.pre_invasion_realms_begin == "fac_player_supporters_faction"
    assert module_constants.pre_invasion_realms_end == "fac_kingdom_6"
    assert [
        faction_names_by_id[faction_id]
        for faction_id in range(ID_factions.fac_player_supporters_faction, ID_factions.fac_kingdom_6)
    ] == [
        "fac_player_supporters_faction",
        "fac_kingdom_1",
        "fac_kingdom_2",
        "fac_kingdom_3",
        "fac_kingdom_4",
        "fac_kingdom_5",
    ]

    assert module_constants.native_kingdoms_begin == "fac_kingdom_1"
    assert module_constants.native_kingdoms_end == "fac_kingdom_6"
    assert [
        faction_names_by_id[faction_id]
        for faction_id in range(ID_factions.fac_kingdom_1, ID_factions.fac_kingdom_6)
    ] == [
        "fac_kingdom_1",
        "fac_kingdom_2",
        "fac_kingdom_3",
        "fac_kingdom_4",
        "fac_kingdom_5",
    ]

    quest_ranges = [
        ("lord quests", ID_quests.qst_deliver_message, ID_quests.qst_follow_army, 18),
        ("village elder quests", ID_quests.qst_deliver_grain, ID_quests.qst_eliminate_bandits_infesting_village, 3),
        ("mayor quests", ID_quests.qst_move_cattle_herd, ID_quests.qst_deliver_grain, 8),
        ("lady quests", ID_quests.qst_rescue_lord_by_replace, ID_quests.qst_move_cattle_herd, 3),
        ("army quests", ID_quests.qst_deliver_cattle_to_army, ID_quests.qst_rescue_lord_by_replace, 3),
    ]
    for label, begin, end, expected_count in quest_ranges:
        assert begin < end, f"{label} is empty or inverted"
        assert end - begin == expected_count, f"{label} count changed"
        assert all(name.startswith("qst_") for name in (quest_names_by_id[index] for index in range(begin, end)))


def test_semantic_item_range_boundaries_are_stable() -> None:
    assert module_constants.trade_goods_begin == "itm_smoked_fish"
    assert module_constants.trade_goods_end == "itm_tutorial_sword"
    assert module_constants.food_begin == "itm_smoked_fish"
    assert module_constants.food_end == "itm_spice"
    assert module_constants.books_begin == "itm_book_tactics"
    assert module_constants.books_end == "itm_smoked_fish"
    assert module_constants.horses_begin == "itm_sumpter_horse"
    assert module_constants.horses_end == "itm_leather_gloves"
    assert module_constants.armors_begin == "itm_leather_gloves"
    assert module_constants.armors_end == "itm_arrows"
    assert module_constants.ranged_weapons_begin == "itm_arrows"
    assert module_constants.ranged_weapons_end == "itm_wooden_stick"
    assert module_constants.weapons_begin == "itm_wooden_stick"
    assert module_constants.weapons_end == "itm_wooden_shield"
    assert module_constants.shields_begin == "itm_wooden_shield"
    assert module_constants.shields_end == "itm_bascinetnasal"

    assert ID_items.itm_sumpter_horse < ID_items.itm_leather_gloves < ID_items.itm_arrows
    assert ID_items.itm_arrows < ID_items.itm_wooden_stick < ID_items.itm_wooden_shield


if __name__ == "__main__":
    test_resolvable_generated_constant_ranges_are_ordered()
    test_party_range_constants_resolve_to_existing_generated_party_ids()
    test_semantic_troop_and_faction_ranges_do_not_include_story_npcs()
    test_semantic_center_and_service_troop_ranges_are_pure()
    test_semantic_actor_and_quest_ranges_are_stable()
    test_semantic_item_range_boundaries_are_stable()
    print("test_constant_ranges_static: OK")
