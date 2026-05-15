from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_dialogue_text_placeholders_are_expanded_before_display() -> None:
    mercs = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_120.py")
    farmers = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_village_farmers_start.py")
    fief_advice = read("src/dialogs/ZB01_lords_politics_and_family/anyone_center_captured_lord_advice_2.py")
    lord_intro = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_intro.py")
    oath = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_give_oath_go_on_2.py")
    siege_seneschal = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_74.py")
    new_seneschal = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_75.py")
    town_info = read("src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_ask_info.py")
    enemies = read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_tell_enemies.py")
    arena_intro = read("src/dialogs/ZC01_centers_and_economy/anyone_arena_master_intro_2.py")
    mayor_health = read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_public_health.py")
    mayor_peace_reward = read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_begin.py")
    seneschal_health = read("src/dialogs/ZZ99_misc_dialogs/anyone_seneschal_public_health.py")
    health_report = read("src/menus/kingdom/center_public_health_report.py")
    horses = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_15.py")
    arena = read("src/dialogs/ZC01_centers_and_economy/anyone_arena_master_ask_tournaments.py")
    merc_cant_lead = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavern_mercenary_cant_lead.py")
    traveler = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavern_traveler_lost_companion_thanks.py")
    prison_guard = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_prison_guard_ask_prisoners.py")
    deserter_barter = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_deserter_barter.py")
    mountain_bandit_toll = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_mountain_bandit_toll.py")
    lord_follow_spy_complete = read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_14.py")
    lord_follow_spy_partial = read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_15.py")
    lord_village_bandits_success = read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_21.py")
    lord_village_bandits_failure = read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_22.py")
    quest_memory_lines = [
        read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_quest_memory.py"),
        read("src/dialogs/ZA01_startup_and_dispatch/anyone_quest_flavor_start.py"),
        read("src/dialogs/ZA01_startup_and_dispatch/anyone_member_chat_quest_memory.py"),
        read("src/dialogs/ZA01_startup_and_dispatch/anyone_quest_flavor_member_chat.py"),
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_quest_flavor_battle_reason.py"),
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_quest_memory.py"),
    ]
    ally_thanks_intro = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_94.py")
    ally_thanks_high = read("src/dialogs/ZZ99_misc_dialogs/anyone_ally_thanks_meet_2.py")
    ally_thanks_fallback = read("src/dialogs/ZZ99_misc_dialogs/anyone_ally_thanks_meet_2_03.py")
    raid_caravan_accept = read("src/dialogs/ZA01_startup_and_dispatch/anyone_quest_raid_caravan_to_start_war_accepted.py")
    automanage_report = read("src/dialogs/ZZ99_misc_dialogs/anyone_member_automanage_report.py")
    automanage_select_1 = read("src/dialogs/ZZ99_misc_dialogs/anyone_member_automanage_select_melee_1.py")
    automanage_select_2 = read("src/dialogs/ZZ99_misc_dialogs/anyone_member_automanage_select_melee_2.py")
    caravan_escort_offer = read("src/dialogs/ZZ99_misc_dialogs/anyone_caravan_offer_protection_2_02.py")
    caravan_escort_accept = read("src/dialogs/ZZ99_misc_dialogs/anyone_caravan_offer_protection_6.py")
    caravan_escort_clear = read("src/dialogs/ZZ99_misc_dialogs/anyone_talk_caravan_escort_2b.py")
    automanage_slot_choices = [
        read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_automanage_select_melee_slot.py"),
        *[
            read(f"src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_automanage_select_melee_slot_{idx:02d}.py")
            for idx in range(2, 11)
        ],
    ]
    fight_guild_start_1 = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_05.py")
    fight_guild_start_2 = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_06.py")
    fight_guild_start_end = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_07.py")
    fight_guild_next = read("src/dialogs/ZZ99_misc_dialogs/anyone_fgtq_gm_next.py")
    cp_liberator = read("src/dialogs/ZZ99_misc_dialogs/anyone_cp_liberator_5.py")
    chancellor_fief_picker = read(
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_plyr_repeat_for_parties_chancellor_fiefs_which.py"
    )
    chancellor_fief_confirm = read(
        "src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_chancellor_fiefs_who.py"
    )
    marshal_ai = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_ai.py")
    center_assignment = read("src/dialogs/ZA01_startup_and_dispatch/anyone_event_triggered_03.py")
    mercenary_base_random = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_37.py")
    strategy_advisor_random = [
        read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_start.py"),
        read("src/dialogs/ZA01_startup_and_dispatch/trp_sod_strategy_advisor_event_triggered_02.py"),
    ]
    guildmaster_location = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_ask_location.py")

    for raw in (mercs, fief_advice, oath, horses, arena):
        assert_contains(raw, '"{s68}"')

    assert_contains(mercs, "Me and one of my mates are looking for a master")
    assert_contains(mercs, "Me and {reg3} of my mates are looking for a master")
    assert_not_contains(mercs, "{reg3?Me and")

    assert_contains(farmers, "We are taking our products to the market at {s12}.")
    assert_contains(farmers, "We are returning from the market at {s12} back to our village.")
    assert_not_contains(farmers, "{reg1?We are taking our products")

    assert_contains(fief_advice, '(str_store_string, s69, "@I")')
    assert_contains(fief_advice, '(str_store_party_name, s70, "$g_center_taken_by_player_faction")')
    assert_contains(fief_advice, "will be the new lady of {s70}.")
    assert_contains(fief_advice, "will be the new lord of {s70}.")
    assert_not_contains(fief_advice, "{reg6?I:{reg7?You:{s11}}}")
    assert_not_contains(fief_advice, "of {s1}.")

    assert_contains(lord_intro, "@{s9} and the lord of {s8}.")
    assert_contains(lord_intro, "@{s9}.")
    assert_not_contains(lord_intro, "{reg5? and the lord of {s8}")

    assert_contains(oath, "(str_store_party_name, s69, \"$g_invite_offered_center\")")
    assert_contains(oath, "Furthermore I give you the fief of {s69}")
    assert_not_contains(oath, "{reg1? Furthermore I give you")
    assert_not_contains(oath, "fief of {s1}")

    for raw in (siege_seneschal, new_seneschal):
        assert_contains(raw, '(str_store_party_name, s68, "$g_encountered_party")')
        assert_contains(raw, "{s68}")
        assert_not_contains(raw, "{s1}")
        assert_not_contains(raw, "nott")

    assert_contains(town_info, "We mostly produce {s5} here.")
    assert_contains(town_info, "We don't produce much here these days.")
    assert_not_contains(town_info, "{reg20?We mostly produce {s5} here")

    for raw in (mayor_health, seneschal_health):
        assert_contains(raw, '(str_store_string_reg, s68, s0)')
        assert_contains(raw, '"{s68}"')
        assert_not_contains(raw, '"{s0}"')

    assert_contains(health_report, '(str_store_string_reg, s68, s0)')
    assert_contains(health_report, "@{s1}: {s68}")
    assert_contains(health_report, '(str_store_string_reg, s97, s98)')
    assert_contains(health_report, "@{s97}^^{s1}: {s68}")
    assert_not_contains(health_report, "@{s8}^^{s1}: {s68}")
    assert_not_contains(health_report, "{s1}: {s0}")
    assert_not_contains(health_report, "{s8}^^{s1}: {s0}")

    peace_text_index = mayor_peace_reward.index('"{s68}"')
    peace_condition_block = mayor_peace_reward[:peace_text_index]
    peace_consequence_block = mayor_peace_reward[peace_text_index:]
    assert_contains(peace_condition_block, '(assign, reg12, ":quest_reward")')
    assert_contains(peace_condition_block, '(str_store_string, s68, "@{playername}, it was an incredible feat')
    assert_not_contains(peace_consequence_block, '(str_store_string, s1,')
    assert_not_contains(mayor_peace_reward, '"{s1}"')

    assert_contains(enemies, "He currently commands {reg0} men, of which around {reg1} are wounded.")
    assert_contains(enemies, "He currently commands {reg0} men.")
    assert_not_contains(enemies, "{reg1?, of which around {reg1} are wounded:}")

    assert_contains(horses, "bring us a {s13} mount")
    assert_contains(horses, "bring us {reg5} {s13} mounts")
    assert_not_contains(horses, "{reg5?{reg5}:a}")

    assert_contains(arena, "There won't be any tournaments any time soon.")
    assert_contains(arena, "A tournament is going to be held at {s15}.")
    assert_contains(arena, "Tournaments are going to be held at {s15}.")
    assert_not_contains(arena, "{reg2?There won't be any tournaments")

    assert_contains(arena_intro, "(str_store_party_name, s68, reg(2))")
    assert_contains(arena_intro, "here at {s68}")
    assert_not_contains(arena_intro, "{s1}")
    assert_not_contains(arena_intro, "(str_store_party_name, 1,")

    assert_contains(merc_cant_lead, '(str_store_string, s68, "@we will")')
    assert_contains(merc_cant_lead, '(str_store_string, s68, "@I will")')
    assert_contains(merc_cant_lead, "Then {s68} keep drinking where the work can find us.")
    assert_not_contains(merc_cant_lead, "{reg3?we will:I will}")

    assert_contains(traveler, '(str_store_string, s68, "@she")')
    assert_contains(traveler, '(str_store_string, s68, "@he")')
    assert_contains(traveler, '(str_store_string, s69, "@her")')
    assert_contains(traveler, '(str_store_string, s69, "@him")')
    assert_contains(traveler, "If {s68} is there, I will find {s69}.")
    assert_not_contains(traveler, "{reg3?she:he}")
    assert_not_contains(traveler, "{reg3?her:him}")

    assert_contains(prison_guard, "Currently, {s51} {s68} imprisoned here.")
    assert_contains(prison_guard, '(str_store_string, s68, "@are")')
    assert_contains(prison_guard, '(str_store_string, s68, "@is")')
    assert_not_contains(prison_guard, "{reg1?are:is}")

    for raw, tribute_global in (
        (deserter_barter, "$deserter_tribute"),
        (mountain_bandit_toll, "$bandit_tribute"),
    ):
        text_index = raw.index("{reg5} denars")
        condition_block = raw[:text_index]
        consequence_block = raw[text_index:]
        assert_contains(condition_block, f"(assign, reg5, \"{tribute_global}\")")
        assert_not_contains(consequence_block, f"(assign, reg5, \"{tribute_global}\")")

    for raw in (lord_follow_spy_complete, lord_follow_spy_partial):
        text_index = raw.index('"{s68}"')
        condition_block = raw[:text_index]
        consequence_block = raw[text_index:]
        assert_contains(condition_block, "(str_store_string, s68,")
        assert_not_contains(consequence_block, "(str_store_string, s1,")
        assert_not_contains(raw, '"{s1}"')

    for raw in (lord_village_bandits_success, lord_village_bandits_failure):
        text_index = raw.index("my village of {s68}")
        condition_block = raw[:text_index]
        consequence_block = raw[text_index:]
        assert_contains(condition_block, "(str_store_party_name, s68, \":village\")")
        assert_not_contains(consequence_block, "(str_store_party_name, s5, \":village\")")
        assert_not_contains(raw, "my village of {s5}")

    for raw in quest_memory_lines:
        text_index = raw.index('"{s68}"')
        condition_block = raw[:text_index]
        consequence_block = raw[text_index:]
        assert_contains(condition_block, "script_sod_quest_dialogue_read_memory")
        assert_contains(condition_block, "(str_store_string_reg, s68, s4)")
        assert_contains(condition_block, "(str_store_string_reg, s97, s68)")
        assert_not_contains(consequence_block, "script_sod_quest_dialogue_describe_")
        assert_not_contains(raw, '"{s1}"')

    for raw in (ally_thanks_intro, ally_thanks_high, ally_thanks_fallback):
        assert_contains(raw, '(call_script, "script_store_troop_name", s68, "$g_talk_troop")')
        assert_contains(raw, "{s68}")
        assert_not_contains(raw, "{s1}")

    text_index = raid_caravan_accept.index("{reg13} caravans")
    condition_block = raid_caravan_accept[:text_index]
    consequence_block = raid_caravan_accept[text_index:]
    assert_contains(condition_block, "(assign, reg13, \":quest_target_amount\")")
    assert_contains(condition_block, "(str_store_faction_name_link, s68, \":quest_target_faction\")")
    assert_contains(raid_caravan_accept, "fools in {s68}")
    assert_not_contains(consequence_block, "fools in {s13}")

    for raw in (automanage_report, automanage_select_1, automanage_select_2):
        assert_contains(raw, "script_print_wpn_upgrades_to_s0")
        assert_contains(raw, "(str_store_string_reg, s68, s0)")
        assert_not_contains(raw, "{s0}")

    text_index = caravan_escort_clear.index("reach {s68}")
    condition_block = caravan_escort_clear[:text_index]
    consequence_block = caravan_escort_clear[text_index:]
    assert_contains(condition_block, '(str_store_party_name, s68, "$caravan_escort_destination_town")')
    assert_not_contains(consequence_block, "str_store_party_name")
    assert_not_contains(caravan_escort_clear, "{s1}")

    for raw in (caravan_escort_offer, caravan_escort_accept):
        assert_contains(raw, "(str_store_party_name, s68, \":caravan_destination\")")
        assert_contains(raw, "{s68}")
        assert_not_contains(raw, "{s1}")
        assert_not_contains(raw, "(str_store_party_name, 1,")

    assert_contains(automanage_report, "My weapon slot upgrades are as follows: {s68}")
    assert_contains(automanage_report, "I'm currently {s69} and {s70}. {s2}")
    assert_not_contains(automanage_report, "I'm currently {s1} and {s4}. {s2}")
    assert_contains(automanage_select_1, "My weapon slot upgrades are as follows: {s68}")
    assert_contains(automanage_select_2, "My current weapon upgrade settings are: {s68}^^{s2}")
    for raw in automanage_slot_choices:
        assert_contains(raw, '(str_store_string, s68, ":type")')
        assert_contains(raw, '"{s68}"')
        assert_not_contains(raw, '(str_store_string, s1, ":type")')
        assert_not_contains(raw, '"{s1}"')

    for raw in (fight_guild_start_1, fight_guild_start_2):
        assert_contains(raw, "(str_store_string_reg, s68, s1)")
        assert_contains(raw, '"{s68}"')
        assert_not_contains(raw, '"{s1}"')

    for raw in (fight_guild_start_end, fight_guild_next):
        assert_contains(raw, "(str_store_string_reg, s68, s0)")
        assert_contains(raw, '"{s68}"')
        assert_not_contains(raw, '"{s0}"')

    assert_contains(cp_liberator, "honorary member of the {s68}.")
    assert_not_contains(cp_liberator, "{s0}")

    for raw in (chancellor_fief_picker, chancellor_fief_confirm):
        assert_contains(raw, "{s68} bound to {s69}")
        assert_contains(raw, "Town of {s68}")
        assert_contains(raw, "(str_store_string_reg, s97, s69)")
        assert_not_contains(raw, '(str_store_string, s69, "@{s69}')
        assert_not_contains(raw, "Village of {s1} bound")
        assert_not_contains(raw, "Town of {s1}+")
        assert_not_contains(raw, '"{s1} ({s2})')

    assert_contains(marshal_ai, "(str_store_string_reg, s97, s18)")
    assert_contains(marshal_ai, "Our lords strongly favor defense")
    assert_contains(marshal_ai, "Our lords are divided between attack and defense")
    assert_contains(marshal_ai, "Our lords strongly favor attack")
    assert_not_contains(marshal_ai, '(str_store_string, s18, "@{s18}')
    assert_not_contains(marshal_ai, "lords priority")

    assert_contains(center_assignment, '(str_store_party_name, s68, "$g_center_taken_by_player_faction")')
    assert_contains(center_assignment, "{s68} is not being managed")
    assert_not_contains(center_assignment, "{s1}")

    assert_contains(mercenary_base_random, '(call_script, "script_get_random_string_for_troop", s68, "$g_talk_troop")')
    assert_contains(mercenary_base_random, '"{s68}"')
    assert_not_contains(mercenary_base_random, "{s1}")

    for raw in strategy_advisor_random:
        assert_contains(raw, '(call_script, "script_get_random_string_for_troop", s68, "$g_talk_troop")')
        assert_contains(raw, '"{s68}"')
        assert_not_contains(raw, '"{s1}"')

    assert_contains(guildmaster_location, "(str_store_string_reg, s68, s1)")
    assert_contains(guildmaster_location, '"{s68}"')
    assert_not_contains(guildmaster_location, '"{s1}"')

if __name__ == "__main__":
    test_dialogue_text_placeholders_are_expanded_before_display()
    print("test_dialogue_text_placeholder_static: OK")
