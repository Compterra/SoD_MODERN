from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    fight_setup = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_fight_quest_02.py")
    player_response = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_fgtq_plyr_response.py")
    pact_debt = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_pact1_02.py")
    pact_employer = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_pact1_04.py")
    upgrade_camp = read("src/menus/camp/sod_upgrade_camp.py")
    upgrade_gate = read("src/scripts/ZY_helper_scripts/sod_troop_can_upgrade_at_center.py")
    abort_quest = read("src/scripts/ZG_quests/abort_quest.py")
    update_all_notes = read("src/scripts/ZJ_notes_and_information/update_all_notes.py")
    update_faction_notes = read("src/scripts/ZF_factions/update_faction_notes.py")
    legacy_employer = read("src/scripts/ZY_helper_scripts/cf_merc_guild_give_new_employer.py")
    player_pact = read("src/scripts/ZY_helper_scripts/merc_player_start_guild_pact.py")
    weekly_trigger = read("src/triggers/ST04_weekly/entry_0126.py")
    market_ai_clients = {
        "hire quote": read("src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py"),
        "standing report": read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py"),
        "guild supply": read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_guild_supply.py"),
        "kingdom demand": read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_demand.py"),
        "kingdom budget": read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_budget.py"),
        "guild weight": read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_guild_weight.py"),
        "village patrol demand": read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_village_patrol_demand.py"),
        "world pressure": read("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_world_activity_pressure.py"),
        "overview": read("src/scripts/ZY_helper_scripts/sod_merc_market_describe_overview_to_s20.py"),
        "kingdom demand text": read("src/scripts/ZY_helper_scripts/sod_merc_market_describe_kingdom_demand_to_s20.py"),
        "bid generation": read("src/scripts/ZY_helper_scripts/sod_merc_market_generate_bid.py"),
        "demand refresh": read("src/scripts/ZY_helper_scripts/sod_merc_market_refresh_kingdom_demands.py"),
        "preferred guild": read("src/scripts/ZY_helper_scripts/sod_merc_market_select_preferred_guild.py"),
        "bid acceptance": read("src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py"),
        "weekly pulse": read("src/scripts/ZY_helper_scripts/sod_merc_market_weekly_pulse.py"),
        "merc lord spawn": read("src/scripts/ZY_helper_scripts/sod_merc_lord_try_spawn_for_troop.py"),
        "merc lord battle outcome": read("src/scripts/ZY_helper_scripts/sod_merc_lord_note_battle_outcome.py"),
    }
    constants = read("src/constants/module_constants.py")

    assert 'guilds_begin = "fac_sod_merc_guild1"' in constants
    assert 'guilds_end = "fac_kingdom_6_mercenaries"' in constants

    for label, raw in {
        "fight setup": fight_setup,
        "player response": player_response,
    }.items():
        assert '(store_random_in_range, ":random_guild", guilds_begin, guilds_end)' in raw, label
        assert '(store_random_in_range, ":random_guild", "fac_sod_merc_guild1", "fac_sod_merc_guild6")' not in raw, label

    assert '(try_for_range, ":merc_guild", guilds_begin, guilds_end)' in pact_debt
    assert '(try_for_range, ":merc_guild", "fac_sod_merc_guild1", "fac_player_faction")' not in pact_debt

    assert '(assign, ":is_hired", 0)' in pact_employer
    assert '(try_for_range, "$temp_faction", native_kingdoms_begin, native_kingdoms_end)' in pact_employer
    assert '(try_for_range, "$temp_faction", kingdoms_begin, kingdoms_end)' not in pact_employer

    assert '(try_for_range, ":guild", guilds_begin, guilds_end)' in upgrade_camp
    assert '(try_for_range, ":guild", "fac_sod_merc_guild1", "fac_kingdom_6_mercenaries")' not in upgrade_camp

    assert upgrade_gate.count('(is_between, ":troop_faction", guilds_begin, guilds_end)') >= 2
    assert '(is_between, ":troop_faction", "fac_sod_merc_guild1", "fac_kingdom_6_mercenaries")' not in upgrade_gate

    assert '(is_between, ":quest_giver_faction", guilds_begin, guilds_end)' in abort_quest
    assert '(is_between, ":quest_giver_faction", "fac_sod_merc_guild1", "fac_player_faction")' not in abort_quest

    assert '(try_for_range, ":faction_no", guilds_begin, guilds_end)' in update_all_notes
    assert '(try_for_range, ":faction_no", "fac_sod_merc_guild1", "fac_kingdom_6_mercenaries")' not in update_all_notes

    assert '(is_between, ":faction_no", guilds_begin, guilds_end)' in update_faction_notes
    assert '(this_or_next|is_between, ":faction_no", "fac_sod_merc_guild1", "fac_sod_merc_guild7")' not in update_faction_notes
    assert '(try_for_range, ":employer", native_kingdoms_begin, native_kingdoms_end)' in update_faction_notes
    assert '(try_for_range, ":employer", kingdoms_begin, kingdoms_end)' not in update_faction_notes

    assert '(try_for_range, ":candidate", native_kingdoms_begin, native_kingdoms_end)' in legacy_employer
    assert '(try_for_range, ":candidate", kingdoms_begin, kingdoms_end)' not in legacy_employer
    assert '(neq, ":candidate", "fac_kingdom_6")' not in legacy_employer

    assert player_pact.count("native_kingdoms_begin, native_kingdoms_end") >= 2
    assert '(try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end)' not in player_pact
    assert '(try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end)' not in player_pact
    assert '(call_script, "script_merc_sync_player_guild_pact", ":guild_no")' in player_pact

    for label, raw in market_ai_clients.items():
        assert "native_kingdoms_begin" in raw, label
        assert "native_kingdoms_end" in raw, label
        assert "kingdoms_begin, kingdoms_end" not in raw, label
        assert '"fac_kingdom_6"' not in raw, label

    assert '(try_for_range, ":employer", kingdoms_begin, kingdoms_end)' in weekly_trigger
    assert '(is_between, ":employer", native_kingdoms_begin, native_kingdoms_end)' in weekly_trigger

    print("test_mercenary_guild_range_static: OK")


if __name__ == "__main__":
    main()
