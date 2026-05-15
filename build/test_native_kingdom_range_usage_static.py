from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    faith_event = read("src/menus/events/choice_25_1.py")
    random_active_faction = read(
        "src/scripts/ZF_factions/cf_get_random_active_faction_except_player_faction_and_faction.py"
    )
    tavern_travelers = read("src/scripts/ZY_helper_scripts/update_tavern_travelers.py")
    advisor_mentor = read("src/scripts/ZY_helper_scripts/sod_strategy_advisor_mentor.py")
    imperial_expedition = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    lord_offer = read("src/dialogs/ZA01_startup_and_dispatch/anyone_auto_proceed_lord_request_mission_ask.py")
    castle_patrol_orders = read("src/menus/centers/castle/castle_patrol_orders.py")

    assert faith_event.count(
        '(try_for_range, ":kingdom_no", native_kingdoms_begin, native_kingdoms_end)'
    ) == 3
    assert '(try_for_range, ":kingdom_no", "fac_kingdom_1", kingdoms_end)' not in faith_event
    assert '(neq, ":kingdom_no", "fac_player_supporters_faction")' not in faith_event

    assert random_active_faction.count(
        '(try_for_range, ":faction_no", native_kingdoms_begin, native_kingdoms_end)'
    ) == 2
    assert "(try_for_range, \":faction_no\", kingdoms_begin, kingdoms_end)" not in random_active_faction
    assert '"fac_player_supporters_faction"' not in random_active_faction
    assert "rebel_factions_begin" not in random_active_faction

    assert "(store_random_in_range, \":info_faction\", native_kingdoms_begin, native_kingdoms_end)" in tavern_travelers
    assert "(store_random_in_range, \":info_faction\", kingdoms_begin, kingdoms_end)" not in tavern_travelers
    assert '"fac_player_supporters_faction"' not in tavern_travelers

    assert '(try_for_range, ":kingdom_no", native_kingdoms_begin, native_kingdoms_end)' in advisor_mentor
    assert '(try_for_range, ":kingdom_no", native_kingdoms_begin, native_kingdoms_end)' in imperial_expedition
    assert "slot_troop_sod_mentor_alliance_victory" in advisor_mentor
    assert "sod_imperial_expedition_calculate_anti_legion_coalition" in imperial_expedition

    assert '(try_for_range, ":faction_no", native_kingdoms_begin, native_kingdoms_end)' in lord_offer
    assert '(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end)' not in lord_offer
    assert '(try_for_range, ":faction_no", native_kingdoms_begin, native_kingdoms_end)' in castle_patrol_orders
    assert '(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end)' not in castle_patrol_orders

    print("test_native_kingdom_range_usage_static: OK")


if __name__ == "__main__":
    main()
