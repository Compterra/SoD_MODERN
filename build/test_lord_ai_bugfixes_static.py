from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    troops = read("compile/module_troops.py")
    kill_hero = read("src/scripts/ZF_factions/kill_kingdom_hero.py")
    summon = read("src/scripts/ZY_helper_scripts/sod_player_kingdom_summon_marshal_campaign.py")
    court_campaign = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_campaign2.py")
    lord_campaign = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_give_order_call_to_arms.py")
    lord_ai = read("src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state.py")
    castle_patrol_trigger = read("src/triggers/ST03_daily/entry_0150.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    castle_patrol_process = read("src/scripts/ZY_helper_scripts/sod_process_castle_patrols.py")
    castle_patrol_spawn = read("src/scripts/ZY_helper_scripts/sod_try_spawn_castle_patrols.py")

    euscarl_line = next(line for line in troops.splitlines() if '["reserved_knight_6", "Euscarl"' in line)
    assert "itm_courser" in euscarl_line, "Euscarl should still be a mounted lord"
    assert "itm_tab_shield_heater_c" in euscarl_line, "Euscarl should still carry his shield"
    assert "itm_sword_two_handed_b" not in euscarl_line, "Euscarl should not carry the two-handed sword on horseback"
    assert "itm_sword_medieval_c" in euscarl_line, "Euscarl should carry a mounted-safe arming sword"

    assert "Claimants should not inherit by random chance" in kill_hero
    assert "(neg|is_between, \":candidat\", pretenders_begin, pretenders_end)" in kill_hero
    assert "(troop_set_slot, \":pretender\", slot_troop_pretender, 0)" not in kill_hero
    assert "(troop_set_faction, \":pretender\", \":troop_faction\")" not in kill_hero

    for token in [
        '"sod_player_kingdom_summon_marshal_campaign"',
        "(faction_get_slot, \":marshal_no\", \":faction_no\", slot_faction_marshall)",
        "(eq, \":marshal_no\", \"trp_player\")",
        "(assign, \":marshal_party\", \"p_main_party\")",
        "(troop_set_slot, \":lord_no\", slot_troop_player_order_state, spai_accompanying_army)",
        "(troop_set_slot, \":lord_no\", slot_troop_player_order_object, \":marshal_party\")",
        "(party_set_slot, \":lord_party\", slot_party_commander_party, \":marshal_party\")",
        "(call_script, \"script_party_set_ai_state\", \":lord_party\", spai_accompanying_army, \":marshal_party\")",
        "(call_script, \"script_sod_lord_update_strategic_intent\", \":lord_no\")",
    ]:
        assert token in summon, f"missing marshal summon helper token: {token}"

    assert "script_sod_player_kingdom_summon_marshal_campaign" in court_campaign
    assert "script_sod_player_kingdom_summon_marshal_campaign" in lord_campaign

    assert '(val_add, ":sum_chances", ":chance_patrol_around_center")' in lord_ai
    patrol_sum_index = lord_ai.index('(val_add, ":sum_chances", ":chance_patrol_around_center")')
    patrol_choice = '(call_script, "script_party_set_ai_state", ":party_no", spai_patrolling_around_center, ":target_patrol_around_center")'
    assert patrol_choice in lord_ai[patrol_sum_index:], "patrol chance must have a final random-choice branch"
    assert '(val_sub, ":random_no", ":chance_patrol_around_center")' in lord_ai[patrol_sum_index:]
    assert '(party_set_slot, ":party_no", slot_party_commander_party, -1)' in lord_ai[lord_ai.index(patrol_choice):]
    assert "Defensive patrols should stay in owned space" in lord_ai
    assert '(store_faction_of_party, ":patrol_target_faction", ":target_patrol_around_center")' in lord_ai
    assert '(neq, ":patrol_target_faction", ":faction_no")' in lord_ai
    assert '(call_script, "script_get_center_faction_relation_including_player", ":target_patrol_around_center", ":faction_no")' in lord_ai
    assert '(ge, reg0, 0)' in lord_ai[lord_ai.index("Defensive patrols should stay in owned space"):]
    assert '(assign, ":target_patrol_around_center", -1)' in lord_ai[lord_ai.index("Defensive patrols should stay in owned space"):]

    assert "SIMPLE_TRIGGERS = [" in castle_patrol_trigger
    assert 'script_sod_process_castle_patrols' in castle_patrol_trigger
    assert 'script_sod_try_spawn_castle_patrols' in castle_patrol_trigger
    assert "ST03_daily/entry_0150.py" in trigger_order
    assert "SCRIPTS = [" in castle_patrol_process
    assert "sod_support_type_castle_patrol" in castle_patrol_process
    assert "SCRIPTS = [" in castle_patrol_spawn
    assert "script_cf_sod_create_castle_patrol" in castle_patrol_spawn

    print("Lord AI bugfix static checks passed")


if __name__ == "__main__":
    main()
