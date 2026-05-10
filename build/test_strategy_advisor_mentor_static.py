from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    troops = read("compile/module_troops.py")
    camp = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    council = read("src/menus/kingdom/talk_council_marshal.py")
    transition_player = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_after_5.py")
    transition_end = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_after_6.py")
    sa_council = read("src/menus/kingdom/sa_council.py")
    strings = read("compile/module_strings.py")
    order = read("src/dialogs/_order_dialogs.txt")
    doc = read("docs/STRATEGY_ADVISOR_MENTOR_DESIGN.md")
    troop_tree_return = read("src/menus/other/troop_trees_prsenatation_end.py")
    constants = read("src/constants/module_constants.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    mentor_script = read("src/scripts/ZY_helper_scripts/sod_strategy_advisor_mentor.py")
    diplomacy_system = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    diplomacy_peace = read("src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py")
    companion_quests = read("src/quests/0012_companion_personal_quests.py")
    quest_consequences = read("src/scripts/ZG_quests/sod_quest_outcome_apply_consequences.py")
    father_player = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_father.py")
    calradia_answer = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_calradia.py")
    name_player = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_name.py")
    name_answer = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_name.py")
    war_room = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room.py")
    war_room_clock = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_clock.py")
    war_room_allies = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_allies.py")
    war_room_company = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_company.py")
    war_room_frontier = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_frontier.py")
    war_room_minifactions = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions.py")
    war_room_minifactions_slavers = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_slavers.py")
    war_room_minifactions_jotnar = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_jotnar.py")
    war_room_minifactions_elephant = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_elephant.py")
    war_room_minifactions_black_khergits = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_black_khergits.py")
    war_room_minifactions_boar = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_boar.py")
    war_room_minifactions_serpent = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_serpent.py")
    war_room_minifactions_black_army = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_black_army.py")
    war_room_terror = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_terror.py")
    loyalty_answer = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_loyalty.py")
    father_mistakes = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_father_mistakes.py")
    trust_player = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_trust.py")
    trust_answer = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_trust.py")
    last_order_opening = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_opening.py")
    last_order_network = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_network.py")
    last_order_rescue = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_after_rescue.py")
    last_order_memory = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_memory.py")
    victory_finalize = read("src/scripts/ZC_parties/total_victory_finalize.py")
    kill_hero = read("src/scripts/ZF_factions/kill_kingdom_hero.py")
    reflect_imperial = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_imperial_victory.py")
    reflect_centurion = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_centurion_death.py")
    reflect_alliance = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_alliance_victory.py")
    reflect_ruthless = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_ruthless_victory.py")
    reflect_final = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_final_closure.py")
    old_advisor_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in (ROOT / "src/dialogs/ZA02_sod_court_and_strategy").glob("trp_sod_strategy_advisor_sa_select_general*.py")
    )

    assert '["sod_strategy_advisor", "Cassian Varro", "Cassian Varro"' in troops
    assert "legacy troop id sod_strategy_advisor" in troops
    assert "Speak with Cassian Varro." in camp
    assert "I wish to speak with Cassian Varro, Strategy Advisor." in council
    assert "Cassian Varro closes the campaign ledger." in troop_tree_return

    assert "Be my Strategy Advisor" in transition_player
    assert "cup and bed" not in transition_player
    assert "ale or woman" not in transition_player
    assert '(assign, "$g_sod_sa_in_court", 1)' in transition_end
    assert '(assign, "$sa_talk_after_siege", 0)' in transition_end
    assert '(troop_clear_inventory, "trp_sod_strategy_advisor")' in transition_end
    assert '(troop_equip_items, "trp_sod_strategy_advisor")' in transition_end

    assert "Cassian Varro asks for a private audience" in sa_council
    assert '(assign, "$sa_talk_after_siege", 0)' in sa_council
    for stale in ["Yor Strategy Advisor", "premission", "faithfuly", "script_change_player_honor"]:
        assert stale not in sa_council, f"stale sa_council text/penalty remains: {stale}"

    assert "My rule of soldiers is simple" in strings
    assert "You knew my father" in father_player
    assert "Roads, allies, and hungry villages" in calradia_answer
    assert "Why do some still call you the Strategy Advisor?" in name_player
    assert "Cassian Varro was a dangerous name inside the Legion" in name_answer
    assert "The long table is ready" in war_room
    assert "$g_sod_invasion_begin" in war_room_clock
    assert "script_sod_imperial_expedition_calculate_anti_legion_coalition" in war_room_allies
    assert "fund counter-intelligence" in war_room_allies
    assert "trusted mini-factions" in war_room_allies
    assert "Imperial Expeditionary Force is not a kingdom" in war_room_allies
    assert "script_sod_strategy_advisor_describe_company_morale_to_s3" in war_room_company
    assert "script_sod_strategy_advisor_describe_center_health_to_s4" in war_room_frontier
    assert "Minor powers matter because they move where kingdoms are too proud to look" in war_room_minifactions
    assert "profit from coercion echoes imperial logic" in war_room_minifactions_slavers.lower()
    assert "kin survival makes them stubborn" in war_room_minifactions_jotnar
    assert "sanctuary" in war_room_minifactions_elephant
    assert "mobile strategic infection" in war_room_minifactions_black_khergits
    assert "road moralists become toll tyrants" in war_room_minifactions_boar
    assert "The Serpent Host sees roads before lords do" in war_room_minifactions_serpent
    assert "mercenary loyalty is rented, not rooted" in war_room_minifactions_black_army
    assert "we may defeat the Legion and still leave its empire standing" in war_room_terror
    assert "You do not. That is the honest answer." in loyalty_answer
    assert "Do better than him there" in father_mistakes
    assert "How do you judge my command, Cassian?" in trust_player
    assert "script_sod_strategy_advisor_describe_trust_to_s1" in trust_answer

    for token in [
        "slot_troop_sod_mentor_trust",
        "slot_troop_sod_mentor_arc_stage",
        "slot_troop_sod_mentor_warning_state",
        "slot_troop_sod_mentor_last_reaction_day",
        "slot_troop_sod_mentor_legion_memory",
        "slot_troop_sod_mentor_first_imperial_victory",
        "slot_troop_sod_mentor_centurion_death",
        "slot_troop_sod_mentor_alliance_victory",
        "slot_troop_sod_mentor_ruthless_victory",
        "slot_troop_sod_mentor_final_closure",
        "slot_troop_sod_mentor_last_front_warning_day",
        "slot_troop_sod_mentor_last_treaty_comment_day",
        "sod_mentor_trust_reverent",
        "sod_mentor_warning_bitter",
        "sod_mentor_last_order_sabotage",
        "sod_mentor_last_order_rescue",
        "sod_mentor_last_order_exposed",
        "sod_mentor_last_order_burned",
    ]:
        assert token in constants, f"missing mentor constant: {token}"
    assert "script_sod_strategy_advisor_initialize_mentor" in game_start
    assert "script_sod_strategy_advisor_apply_player_action" in companion_depth
    for token in [
        "sod_strategy_advisor_initialize_mentor",
        "sod_strategy_advisor_get_trust_band_to_reg",
        "sod_strategy_advisor_describe_trust_to_s1",
        "sod_strategy_advisor_apply_player_action",
        "sod_companion_action_defeat_imperials",
        "sod_companion_action_buy_slaves",
        "sod_companion_action_unpaid_wages",
        "sod_companion_action_help_village",
        "sod_companion_action_cassian_last_order_sabotage",
        "sod_companion_action_cassian_last_order_rescue",
        "sod_companion_action_cassian_last_order_expose",
        "sod_companion_action_cassian_last_order_burn",
        "sod_strategy_advisor_start_last_order",
        "sod_strategy_advisor_resolve_last_order",
        "sod_strategy_advisor_record_imperial_victory",
        "sod_strategy_advisor_record_centurion_death",
        "sod_strategy_advisor_note_treaty_signed",
        "sod_strategy_advisor_warn_many_fronts",
        "sod_strategy_advisor_note_imperial_diplomacy_exception",
        "sod_strategy_advisor_describe_company_morale_to_s3",
        "sod_strategy_advisor_describe_center_health_to_s4",
        "Unpaid wages are no longer numbers in a ledger",
        "noble and faith troops are growing restless",
        "Threats can silence a complaint",
        "disciplined, well-supplied campaign",
        "Villages are the economic roots of your realm",
        "A castle is not a town with thicker walls",
        "Starving or diseased towns do not become loyal",
        "script_sod_quest_runtime_accept",
        "script_sod_quest_runtime_update",
        "script_sod_quest_runtime_complete",
        "script_sod_quest_dialogue_record_event",
        "script_sod_quest_journal_update",
        "slot_quest_sod_runtime_last_center",
    ]:
        assert token in mentor_script, f"missing mentor script token: {token}"
    assert "companion_cassian_last_order" in companion_quests
    assert "Cassian Varro: The Last Order" in companion_quests
    assert "The Old Network" in companion_quests
    assert "The Order Remembered" in companion_quests
    assert "Quest consequence applied" in quest_consequences
    assert '(eq, "$cheat_mode", 1)' in quest_consequences
    assert "A sealed order" in last_order_opening
    assert "dead drop near {s3}" in last_order_network
    assert "bring out the living" in last_order_rescue
    assert "I remember ash" in last_order_memory
    assert "script_sod_strategy_advisor_record_imperial_victory" in victory_finalize
    assert "script_sod_strategy_advisor_record_centurion_death" in kill_hero
    assert "script_sod_companion_dispatch_player_action" in mentor_script
    assert "sod_companion_try_cassian_mentor_arc_reactions" in companion_depth
    assert "Lezalit approves Cassian's choice" in companion_depth
    assert "Ymira thanks Cassian" in companion_depth
    assert "Bunduk approves of destroying a chain of command" in companion_depth
    assert "Marnid approves of dragging the ledger into daylight" in companion_depth
    assert "Borcha says secrets are like bad bridges" in companion_depth
    assert "Cassian, Lezalit, and Ymira clash over the Last Order" in companion_depth
    assert "Cassian, Marnid, and Borcha turn the old network" in companion_depth
    assert "script_sod_strategy_advisor_note_treaty_signed" in diplomacy_system
    assert "script_sod_strategy_advisor_warn_many_fronts" in diplomacy_system
    assert "script_sod_strategy_advisor_note_imperial_diplomacy_exception" in diplomacy_system
    assert "script_sod_strategy_advisor_note_treaty_signed" in diplomacy_peace
    assert "the Imperial Expeditionary Force is outside normal diplomacy" in mentor_script
    assert "active fronts will not make you look strong" in mentor_script
    assert "anti-Imperial league is not friendship" in mentor_script
    assert "impossible things become ordinary" in reflect_imperial
    assert "command knot has been cut" in reflect_centurion
    assert "A coalition is mud" in reflect_alliance
    assert "fear works. That is the trap" in reflect_ruthless
    assert "no longer my student" in reflect_final
    for stale in [
        "devour their own mother",
        "cannibalistic rituals",
        "unwanted babies",
        "self righteous",
        "Once thing",
        "capitol city",
        "My Lord",
        "my Lord",
        "Black Knergits",
        "Steepe",
        "Vaeghir",
        "famers",
    ]:
        assert stale not in old_advisor_text, f"stale old advisor text remains: {stale}"
    for fresh in [
        "hearthbound kin",
        "black-market web",
        "road moralists",
        "moving horde infection",
        "guard sanctuaries",
        "rented loyalty",
        "Profit from coercion echoes Imperial logic",
    ]:
        assert fresh in old_advisor_text, f"missing refreshed advisor text: {fresh}"

    advisor_dialogue_text = "\n".join([
        old_advisor_text,
        war_room_allies,
        war_room_minifactions_serpent,
        war_room_minifactions_slavers,
        loyalty_answer,
        reflect_final,
        mentor_script,
    ])
    for stale in [
        "Choose the lens:",
        "contract steel:",
        "what they do now:",
        "hearthbound kin:",
        "the tale:",
        "black-market web:",
        "one grim respect:",
        "are worse:",
        "remains useful:",
        "know for certain:",
        "In general:",
        "main divisions:",
        "tell you this:",
        "great capitals:",
        "what I protect:",
        "harder proof:",
        "stands at {reg4}:",
        "bones of a coalition:",
        "Their value is intelligence:",
        "But mark this:",
        "@Cassian:",
        "Cassian warns:",
        "Watch three signs:",
        "matter: root score",
        "town strain:",
    ]:
        assert stale not in advisor_dialogue_text, f"colon-heavy advisor phrasing remains: {stale}"

    for path in [
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_father.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_father.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_calradia.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_calradia.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_name.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_name.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_war_room.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_clock.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_allies.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_answer_company.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_company.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_frontier.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_slavers.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_slavers.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_jotnar.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_jotnar.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_elephant.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_elephant.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_black_khergits.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_black_khergits.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_boar.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_boar.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_serpent.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_serpent.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_black_army.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_minifactions_black_army.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_war_room_minifactions_back.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_war_room_terror.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_loyalty.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_father_mistakes.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_mentor_trust.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_mentor_trust.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_last_order_opening.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_opening.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_network.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_last_order_choice_sabotage.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_last_order_choice_rescue.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_last_order_choice_expose.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_sod_sa_last_order_choice_burn.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_last_order_memory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_imperial_victory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_imperial_victory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_centurion_death.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_centurion_death.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_alliance_victory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_alliance_victory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_ruthless_victory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_ruthless_victory.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_plyr_startegy_advisor_continue_reflect_final_closure.py",
        "ZA02_sod_court_and_strategy/trp_sod_strategy_advisor_sod_sa_reflect_final_closure.py",
    ]:
        assert path in order, f"mentor dialogue file missing from order: {path}"

    for checked in [
        "- [x] Rename `Strategy Advisor` in-game to **Cassian Varro**.",
        "- [x] Update random advice strings to use his voice.",
        "- [x] Add early mentor questions.",
        "- [x] Expand invasion timing dialogue into a \"Legion War Room\" conversation.",
        "- [x] Add dialogue where the player questions his loyalty after his years in the Legion.",
        "- [x] Add mentor trust slots/constants.",
        "- [x] Add action hook script.",
        "- [x] Add quest metadata.",
        "- [x] Add direct dialogue incident.",
        "- [x] Add first Imperial victory reflection.",
        "- [x] Add final mentor closure line.",
        "- [x] No post-dialogue close-window branch strands the player.",
    ]:
        assert checked in doc, f"design checklist not updated: {checked}"

    print("Strategy Advisor mentor static checks passed")


if __name__ == "__main__":
    main()
