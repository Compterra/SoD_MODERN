# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_before(raw: str, first: str, second: str) -> None:
    assert first in raw, f"missing token: {first}"
    assert second in raw, f"missing token: {second}"
    assert raw.index(first) < raw.index(second), f"{first} should appear before {second}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected stale token: {token}"


def test_stale_short_dialogue_lines_are_tightened() -> None:
    village_moneyless = read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_moneyless.py")
    prisoner_offer = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_offer.py")
    prisoner_offer_again = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_prisoner_chat_offer_again.py")
    claimant_oath = read("src/dialogs/ZB01_lords_politics_and_family/anyone_loa_swear_oath_3.py")
    lord_oath = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_give_oath_4.py")
    automanage = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_automanage_select_melee.py")

    assert_contains(village_moneyless, "Your purse is too light for this")
    assert_contains(prisoner_offer, "Swear to my company and you will be paid, fed, and armed.")
    assert_contains(prisoner_offer_again, "Perhaps. State the offer again.")
    assert_contains(claimant_oath, "I will serve as your loyal knight while I have breath.")
    assert_contains(lord_oath, "I will remain your loyal {man/follower} while I have breath.")
    assert_contains(automanage, "Set melee weapon upgrades.")
    for raw in (village_moneyless, prisoner_offer, prisoner_offer_again, claimant_oath, lord_oath, automanage):
        assert_not_contains(raw, "embarrasing")
        assert_not_contains(raw, "....")


def test_lord_personality_greeting_is_wired_before_fallback() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    dialog = read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_personality_greeting.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_lord_first_line_to_s12"')
    assert_contains(scripts, "slot_lord_reputation_type")
    assert_contains(scripts, "lrep_martial")
    assert_contains(scripts, "lrep_quarrelsome")
    assert_contains(scripts, "lrep_selfrighteous")
    assert_contains(scripts, "lrep_cunning")
    assert_contains(scripts, "lrep_debauched")
    assert_contains(scripts, "lrep_goodnatured")
    assert_contains(scripts, "lrep_upstanding")
    assert_contains(scripts, "script_troop_get_player_relation")
    assert_contains(scripts, "$supported_pretender")
    assert_contains(scripts, "slot_faction_leader")
    assert_contains(scripts, "fac_player_supporters_faction")
    assert_contains(scripts, "Rebellion makes every greeting a test of nerve")
    assert_contains(scripts, "You stand before the one whose banner weighs on your road")
    assert_contains(scripts, "My liege. Your realm has more needs than hours")
    assert_contains(scripts, "Whether by oath, contract, or necessity")
    assert_contains(scripts, "Good. A face I do not have to weigh like bad coin")
    assert_contains(scripts, "Enemies who ask to talk usually want either time or witnesses")
    assert_contains(dialog, "script_sod_store_lord_first_line_to_s12")
    assert_contains(dialog, '"lord_start"')
    assert_contains(dialog, '"lord_talk"')
    assert_before(
        order,
        "ZA01_startup_and_dispatch/anyone_lord_start_tax_courier_rumor.py",
        "ZA01_startup_and_dispatch/anyone_lord_start_personality_greeting.py",
    )
    assert_before(
        order,
        "ZA01_startup_and_dispatch/anyone_lord_start_personality_greeting.py",
        "ZA01_startup_and_dispatch/anyone_lord_start_30.py",
    )


def test_mayor_social_weather_is_wired_before_fallbacks() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_social_weather.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_mayor_social_weather_to_s12"')
    assert_contains(scripts, "slot_center_is_besieged_by")
    assert_contains(scripts, "slot_town_prosperity")
    assert_contains(scripts, "slot_center_sod_security_pressure")
    assert_contains(scripts, "slot_center_accumulated_rents")
    assert_contains(scripts, "slot_center_sod_active_tax_courier")
    assert_contains(scripts, "slot_center_sod_tax_courier_losses")
    assert_contains(scripts, "slot_center_player_relation")
    assert_contains(scripts, "The town can pay men, or feed families")
    assert_contains(scripts, "A tax courier has already left our gate")
    assert_contains(scripts, "lost too many tax couriers")
    assert_contains(scripts, "tax chests are getting heavy")
    assert_contains(scripts, "Whether it thanks me for opening the door")
    assert_contains(scripts, "clerks argue more softly")
    assert_contains(scripts, "Every loaf in this town has three hands reaching for it")
    assert_contains(scripts, "The markets are loud")
    assert_contains(dialog, "script_sod_store_mayor_social_weather_to_s12")
    assert_contains(dialog, '"mayor_friendly_pretalk"')
    assert_contains(dialog, '"mayor_pretalk"')
    assert_contains(dialog, '"mayor_talk"')
    assert_before(
        order,
        "ZC01_centers_and_economy/anyone_mayor_social_weather.py",
        "ZC01_centers_and_economy/anyone_mayor_friendly_pretalk.py",
    )
    assert_before(
        order,
        "ZC01_centers_and_economy/anyone_mayor_social_weather.py",
        "ZC01_centers_and_economy/anyone_mayor_pretalk.py",
    )


def test_village_elder_social_weather_is_wired_before_fallback() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_social_weather.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_village_elder_social_weather_to_s12"')
    assert_contains(scripts, "slot_village_state")
    assert_contains(scripts, "slot_center_sod_looter_raid_pressure")
    assert_contains(scripts, "slot_center_volunteer_troop_amount")
    assert_contains(scripts, "slot_center_player_relation")
    assert_contains(scripts, "There is smoke in every answer I give today")
    assert_contains(scripts, "A village can empty itself into armies")
    assert_contains(dialog, "script_sod_store_village_elder_social_weather_to_s12")
    assert_contains(dialog, '"village_elder_pretalk"')
    assert_contains(dialog, '"village_elder_talk"')
    assert_before(
        order,
        "ZC01_centers_and_economy/anyone_village_elder_social_weather.py",
        "ZC01_centers_and_economy/anyone_village_elder_pretalk.py",
    )


def test_goods_merchant_social_weather_is_wired_after_courier_rumor_before_fallback() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_social_weather.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_goods_merchant_social_weather_to_s12"')
    assert_contains(scripts, "slot_town_prosperity")
    assert_contains(scripts, "slot_center_sod_local_population")
    assert_contains(scripts, "slot_center_sod_local_health")
    assert_contains(scripts, "slot_center_sod_security_pressure")
    assert_contains(scripts, "slot_center_player_relation")
    assert_contains(scripts, "Caravans are counting guards before coin")
    assert_contains(scripts, "People still buy, but now they buy by the handful")
    assert_contains(scripts, "coin spends even when trust does not")
    assert_contains(scripts, "A reliable buyer is rarer than a cheap road")
    assert_contains(dialog, "script_sod_store_goods_merchant_social_weather_to_s12")
    assert_contains(dialog, '(is_between, "$current_town", centers_begin, centers_end)')
    assert_contains(dialog, '"goods_merchant_pretalk"')
    assert_contains(dialog, '"goods_merchant_talk"')
    assert_before(
        order,
        "ZC01_centers_and_economy/anyone_goods_merchant_tax_courier_rumor.py",
        "ZC01_centers_and_economy/anyone_goods_merchant_social_weather.py",
    )
    assert_before(
        order,
        "ZC01_centers_and_economy/anyone_goods_merchant_social_weather.py",
        "ZC01_centers_and_economy/anyone_goods_merchant_pretalk.py",
    )


def test_tavernkeeper_social_weather_is_wired_after_courier_rumor_before_fallback() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    dialog = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_social_weather.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_tavernkeeper_social_weather_to_s12"')
    assert_contains(scripts, "slot_town_prosperity")
    assert_contains(scripts, "slot_center_sod_local_health")
    assert_contains(scripts, "slot_center_sod_security_pressure")
    assert_contains(scripts, "slot_center_accumulated_rents")
    assert_contains(scripts, "slot_center_player_relation")
    assert_contains(scripts, "men drink like the door is listening")
    assert_contains(scripts, "Tax talk has been walking table to table")
    assert_contains(scripts, "not every whisper is kind")
    assert_contains(scripts, "stories more honest")
    assert_contains(dialog, '(is_between, "$current_town", centers_begin, centers_end)')
    assert_contains(dialog, "script_sod_store_tavernkeeper_social_weather_to_s12")
    assert_contains(dialog, '"tavernkeeper_pretalk"')
    assert_contains(dialog, '"tavernkeeper_talk"')
    assert_before(
        order,
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_tax_courier_rumor.py",
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_social_weather.py",
    )
    assert_before(
        order,
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_social_weather.py",
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_pretalk.py",
    )


def test_nonplayer_patrol_immersion_start_is_wired_before_functional_patrol_start() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    context = read("src/scripts/ZY_helper_scripts/sod_store_castle_patrol_dialog_context.py")
    dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_patrol_party_nonplayer_immersion_start.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_nonplayer_patrol_first_line_to_s12"')
    assert_contains(context, "We have not seen any hostile parties lately")
    assert_contains(context, "No hostile parties lately")
    assert_contains(context, "The road is not friendly")
    assert "No urgent raider sign" not in context
    assert_contains(scripts, "script_sod_player_can_command_castle_patrol")
    assert_contains(scripts, "script_sod_store_castle_patrol_dialog_context")
    assert_contains(scripts, "sod_castle_patrol_role_village_shield")
    assert_contains(scripts, "sod_castle_patrol_role_border_harasser")
    assert_contains(scripts, "sod_castle_patrol_role_caravan_screen")
    assert_contains(scripts, "sod_castle_patrol_status_damaged")
    assert_contains(scripts, "fac_player_supporters_faction")
    assert_contains(scripts, "we have learned to dislike surprises")
    assert_contains(dialog, "script_sod_store_nonplayer_patrol_first_line_to_s12")
    assert_contains(dialog, "pt_patrol_party")
    assert_contains(dialog, '"castle_patrol_talk"')
    assert_before(
        order,
        "ZA01_startup_and_dispatch/party_tpl_pt_patrol_party_nonplayer_immersion_start.py",
        "ZA01_startup_and_dispatch/party_tpl_pt_patrol_party_start.py",
    )


def test_castle_patrol_authority_dialogue_covers_law_contraband_and_command_tone() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    order = read("src/dialogs/_order_dialogs.txt")
    ask = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_castle_patrol_talk_authority.py")
    answer = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_castle_patrol_authority.py")
    about = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_castle_patrol_about.py")
    demand = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_castle_patrol_demand_passage.py")
    bribe = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_castle_patrol_bribe.py")
    threaten = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_castle_patrol_threaten.py")
    order_join = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_castle_patrol_order_join_threat.py")
    order_report = read("src/scripts/ZY_helper_scripts/sod_store_castle_patrol_order_report.py")

    assert_contains(scripts, '("sod_store_castle_patrol_authority_to_s12"')
    assert_contains(scripts, "sod_castle_patrol_role_village_shield")
    assert_contains(scripts, "sod_castle_patrol_role_border_harasser")
    assert_contains(scripts, "sod_castle_patrol_role_caravan_screen")
    assert_contains(scripts, "sod_castle_patrol_role_campaign_screen")
    assert_contains(scripts, "sod_castle_patrol_role_emergency_relief")
    assert_contains(scripts, "Contraband, scouts, false pilgrims")
    assert_contains(scripts, "no stolen cattle, no pressed peasants")
    assert_contains(scripts, "manifests match wagons")
    assert_contains(scripts, "army pretending to be trade")
    assert_contains(scripts, "turn back contraband before it becomes bandit pay")

    assert_contains(ask, "What authority do you claim here")
    assert_contains(answer, "script_sod_store_castle_patrol_authority_to_s12")
    assert_contains(answer, '"castle_patrol_talk"')
    assert_contains(about, "bad papers")
    assert_contains(demand, "Lawful passage is not the same as uncounted passage")
    assert_contains(bribe, "buys discretion")
    assert_contains(threaten, "contraband hides under fine cloth")
    assert_contains(order_join, "the law arrive with teeth")
    assert_contains(order_report, "no urgent road target")
    assert "no valid target" not in order_report
    assert_before(
        order,
        "ZD01_encounters_battles_and_prisoners/anyone_castle_patrol_about.py",
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_castle_patrol_talk_authority.py",
    )
    assert_before(
        order,
        "ZD01_encounters_battles_and_prisoners/anyone_castle_patrol_authority.py",
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_castle_patrol_talk_raiders.py",
    )


def test_special_patrol_start_lines_are_relation_aware_and_faction_flavored() -> None:
    black_army = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_army_patrol_start.py")
    elephant_guard = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_elephant_guard_sanctuary_patrol_start.py")

    assert_contains(black_army, "pt_black_army_patrol")
    assert_contains(black_army, "fac_sod_merc_guild1")
    assert_contains(black_army, "fac_player_supporters_faction")
    assert_contains(black_army, "Our contract says this stretch stays open")
    assert_contains(black_army, "keeping the stretch passable and the account clean")
    assert_contains(black_army, "make trouble choose a cheaper road")
    assert_contains(black_army, '"black_army_world_patrol_talk"')

    assert_contains(elephant_guard, "pt_elephant_guard_sanctuary_patrol")
    assert_contains(elephant_guard, "fac_sod_merc_guild3")
    assert_contains(elephant_guard, "fac_player_supporters_faction")
    assert_contains(elephant_guard, "The Elephant's shadow is shelter")
    assert_contains(elephant_guard, "The villages know your name")
    assert_contains(elephant_guard, "already endured enough blood")
    assert_contains(elephant_guard, '"elephant_guard_world_talk"')


def test_world_presence_start_lines_are_relation_aware_for_conquistador_and_jotnar() -> None:
    procurement = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_conquistador_procurement_column_start.py")
    expedition = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_conquistador_expeditionary_camp_start.py")
    hearth_guard = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_jotnar_hearth_guard_start.py")
    winter_camp = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_jotnar_wintering_camp_start.py")

    assert_contains(procurement, "fac_sod_merc_guild2")
    assert_contains(procurement, "hostile hands near army stores")
    assert_contains(procurement, "do not become an army by standing in the road")
    assert_contains(procurement, '"conquistador_world_logistics_talk"')
    assert_contains(expedition, "fac_sod_merc_guild2")
    assert_contains(expedition, "under hard watch")
    assert_contains(expedition, "the quartermasters will hear you")
    assert_contains(expedition, '"conquistador_world_logistics_talk"')

    assert_contains(hearth_guard, "fac_sod_merc_guild4")
    assert_contains(hearth_guard, "the people who stand in front of them")
    assert_contains(hearth_guard, "friend of the hearth")
    assert_contains(hearth_guard, '"jotnar_world_hearth_talk"')
    assert_contains(winter_camp, "fac_sod_merc_guild4")
    assert_contains(winter_camp, "every cooking fire becomes a war fire")
    assert_contains(winter_camp, "Guests are measured by what they protect")
    assert_contains(winter_camp, '"jotnar_world_hearth_talk"')


def test_serpent_and_boar_start_lines_are_relation_aware() -> None:
    route_screen = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_serpent_host_route_screen_start.py")
    courier_lance = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_serpent_host_courier_lance_start.py")
    boar_fighters = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_boar_clan_fighters_start.py")
    boar_desert = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_boar_clan_fighters_desert_start.py")

    assert_contains(route_screen, "fac_sod_merc_guild5")
    assert_contains(route_screen, "fac_player_supporters_faction")
    assert_contains(route_screen, "hostile riders are the first delay we remove")
    assert_contains(route_screen, "Your name travels well enough")
    assert_contains(route_screen, '"serpent_host_world_route_talk"')
    assert_contains(courier_lance, "fac_sod_merc_guild5")
    assert_contains(courier_lance, "fac_player_supporters_faction")
    assert_contains(courier_lance, "enemies are distance with a pulse")
    assert_contains(courier_lance, "proving speed with steel")
    assert_contains(courier_lance, '"serpent_host_world_route_talk"')

    assert_contains(boar_fighters, "fac_sod_merc_guild7")
    assert_contains(boar_fighters, "fac_player_supporters_faction")
    assert_contains(boar_fighters, "interest for insults")
    assert_contains(boar_fighters, "road-friend")
    assert_contains(boar_fighters, '"boar_clan_meet"')
    assert_contains(boar_desert, "fac_sod_merc_guild7")
    assert_contains(boar_desert, "fac_player_supporters_faction")
    assert_contains(boar_desert, "do not need trees to make an ambush")
    assert_contains(boar_desert, "A familiar banner in hard country")
    assert_contains(boar_desert, '"boar_clan_meet"')


def test_merchant_caravan_world_talk_is_wired_after_escort_starts() -> None:
    escort_intro = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_03.py")
    escort_followup = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_04.py")
    world_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_05.py")
    world_ask = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_merchant_caravan_world_talk.py")
    world_about = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_merchant_caravan_world_about.py")
    world_leave = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_merchant_caravan_world_talk_02.py")
    black_army = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_army_caravan_start_02.py")
    slavers = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start_02.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(escort_intro, "losing the cargo to raiders is a tax with knives")
    assert_contains(escort_followup, "every toll written down twice")
    assert_contains(black_army, "road is still asking questions")
    assert_contains(slavers, "every delay eats into the price")

    assert_contains(world_start, "pt_merchant_caravan")
    assert_contains(world_start, "qst_escort_merchant_caravan")
    assert_contains(world_start, "merchant_caravan_world_talk")
    assert_contains(world_start, "road rumors")
    assert_contains(world_ask, "How are the roads treating you?")
    assert_contains(world_about, "Roads are ledgers with mud on them")
    assert_contains(world_leave, "$g_leave_encounter")
    assert_before(
        order,
        "ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_04.py",
        "ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_05.py",
    )
    assert_before(
        order,
        "ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_05.py",
        "ZC01_centers_and_economy/anyone_plyr_escort_merchant_caravan_talk.py",
    )


def test_deserter_start_lines_cover_hunger_service_and_mercy() -> None:
    hostile_script = read("src/scripts/ZY_helper_scripts/sod_store_hostile_greeting.py")
    deserters_paid = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_deserters_start.py")
    sod_deserters_paid = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_deserters_start.py")
    merc_deserters_paid = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_merc_deserters_start.py")
    deserters_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_deserters_start_02.py")
    sod_deserters_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_deserters_start_02.py")
    merc_deserters_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_merc_deserters_start_02.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(deserters_paid, "Hungry men keep promises")
    assert_contains(sod_deserters_paid, "captains remembered rations")
    assert_contains(merc_deserters_paid, "Contract also says every delay can be renegotiated")
    assert_contains(deserters_start, "script_sod_store_hostile_greeting")
    assert_contains(sod_deserters_start, "script_sod_store_hostile_greeting")
    assert_contains(merc_deserters_start, "script_sod_store_hostile_greeting")

    assert_contains(hostile_script, "Deserter graves follow your banner")
    assert_contains(hostile_script, "Some say you shelter broken soldiers")
    assert_contains(hostile_script, "Those colors were ours once")
    assert_contains(hostile_script, "Bread first, honor after")
    assert_contains(hostile_script, "Our lord sold us for taxes and banners")
    assert_contains(hostile_script, "We sold our swords once")
    assert_contains(hostile_script, "pt_sod_merc_deserters")
    assert_before(
        order,
        "ZA01_startup_and_dispatch/party_tpl_pt_deserters_start.py",
        "ZA01_startup_and_dispatch/party_tpl_pt_deserters_start_02.py",
    )


def test_bandit_lines_cover_strength_reputation_and_intimidation() -> None:
    hostile_script = read("src/scripts/ZY_helper_scripts/sod_store_hostile_greeting.py")
    looter_low = read("src/dialogs/ZD01_encounters_battles_and_prisoners/party_tpl_pt_bandits_plyr_looters_2.py")
    looter_high = read("src/dialogs/ZD01_encounters_battles_and_prisoners/party_tpl_pt_bandits_plyr_looters_2_02.py")
    bandit_attack = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_bandit_talk.py")
    bandit_barter = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_bandit_talk_02.py")
    bandit_intimidate = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_bandit_talk_intimidate.py")
    looter_intimidate = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_looters_2_intimidate.py")
    intimidate_accept = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_intimidate_accept.py")

    assert_contains(hostile_script, "Word says your purse opens faster than your sword")
    assert_contains(hostile_script, "That banner has scared enough road dogs")
    assert_contains(hostile_script, "Your purse rides louder than your horse")
    assert_contains(hostile_script, "Small company, bad road, worse luck")
    assert_contains(hostile_script, "too many shields for a clean robbery")
    assert_contains(hostile_script, "pt_mountain_bandits")
    assert_contains(hostile_script, "pt_forest_bandits")
    assert_contains(hostile_script, "pt_bandits")

    assert_contains(looter_low, "I may be new to this road")
    assert_contains(looter_high, "wrong purse and the wrong road")
    assert_contains(bandit_attack, "Earn it through my shield")
    assert_contains(bandit_barter, "do not mistake payment for fear")
    assert_contains(bandit_intimidate, "count your boots")
    assert_contains(looter_intimidate, "count your boots")
    assert_contains(intimidate_accept, "softer roads and poorer memories")
    assert_contains(intimidate_accept, "script_sod_note_hostile_reputation")
    assert_contains(intimidate_accept, "script_sod_resolve_hostile_party_noncombat")


def test_guild_master_social_weather_is_wired_before_pretalk_fallback() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    dialog = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_pretalk_social_weather.py")
    fallback = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_pretalk.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '("sod_store_guild_master_social_weather_to_s12"')
    assert_contains(scripts, "slot_guild_base")
    assert_contains(scripts, "slot_center_sod_security_pressure")
    assert_contains(scripts, "slot_center_accumulated_rents")
    assert_contains(scripts, "slot_town_prosperity")
    assert_contains(scripts, "Road danger is becoming market weather")
    assert_contains(scripts, "Tax chests have been moving loudly")
    assert_contains(scripts, "Poor markets make sharp employers")
    assert_contains(scripts, "reliable partners bring business")
    assert_contains(dialog, "script_sod_store_guild_master_social_weather_to_s12")
    assert_contains(dialog, "$g_talk_troop")
    assert_contains(dialog, '"gm_pretalk"')
    assert_contains(dialog, '"gm_talk"')
    assert_contains(dialog, "script_update_faction_notes")
    assert_contains(dialog, "script_update_troop_notes")
    assert_contains(fallback, "The contract table is still open")
    assert_before(
        order,
        "ZZ99_misc_dialogs/anyone_gm_pretalk_social_weather.py",
        "ZZ99_misc_dialogs/anyone_gm_pretalk.py",
    )


def test_visible_dialogue_avoids_flat_menu_voice_backouts() -> None:
    stale_phrases = (
        '"Never mind."',
        '"Anything else?"',
        '"What do you want?"',
        '"Good day."',
        "Good day.",
        "Alright.",
        '"Okay"',
        "I must leave now",
        "I must beg my leave",
        "I guess I should leave now",
        '"I want to ask you something"',
        "Tell me about what you do again",
        "What can you tell me about this land",
        "ERROR:",
        "[ERROR]",
        "no valid target",
        "No valid target",
        "Nothing. Sorry",
        "Thanks, but I don't really care",
        "Sorry friend",
        "Sorry. I don't have time",
        "Sorry. I don't have that amount",
        "Sorry. I can't",
        "Sorry, I can't take on anyone else right now now",
        "Alright then.",
        "What do you want us to do",
        "Thank you master.",
        "Good luck.",
        "This must be your unlucky day indeed",
        "baddest guys",
        "we consider your offer",
        "I guess we'll just have to",
        "we'll let you go now",
        "What is this caravan doing out here",
        "What is this hearth guard doing here",
        "Who are you carrying?",
        "Sorry to trouble you",
        "You will? I am so happy",
        "Buy them.",
        "Have you any progress to report",
        "Please take these",
        "I heard that you have lost",
        "You will? Oh, splendid",
        "Forgive me for bothering",
        "I can't be bothered",
        "Ask help from someone else",
        "Then I will go and find",
        "How much grain do you need",
        "How many men do you need",
        "Then I will talk to",
        "Forgive me, but I doubt",
        "Here take the money",
        "Please, give me more time",
        "If you could recruit",
        "As you wish, we will attack",
        "I shall be accompanying",
        "Very well, we go to",
        "That should be possible. Very well",
        "As you wish, {playername}.",
        "Very well. You have given me your solemn oath",
        "Farewell then, {playername}, and good luck",
        "Your enemies are my enemies.",
        "Very well then, you've my blessing",
        "Very well. Make your case.",
        "Farewell for now, then.",
        "I can't support you any longer.",
        "Very well, it's all here",
        "Well, all right.",
        "That's all I wanted to know. Thank you.",
        "I may or may not have an answer",
        "Yes, yes. Farewell.",
        "Aye, I'll do it.",
        "I'll do it",
        "I'll do that.",
        "Allright, I'll do it.",
        "I can't do this.",
        "I am too busy to go after him",
        "I am too busy these days",
        "I don't have the time",
        "I am afraid I won't be able",
        "I'm affraid I won't be able",
        "I fear I must decline.",
        "You can count on me.",
        "Consider it done",
        "Certainly, it would be no trouble.",
        "Of course, I can do this",
        "I am sorry, but no.",
        "Sorry, sir, I have other plans.",
        "I am not a cutthroat, find someone else.",
        "Excellent, {playername}, excellent",
        "That's excellent, {playername}",
        "I appreciate it, {playername}. Here's the letter",
        "Excellent! You know what to do",
        "Excellent! Make your way",
        "We'll be praying for you night and day",
        "Thank you, {sir/madam}, but we do not really need anything right now",
        "Many thanks, my friend",
        "All right. I will do my best.",
        "All right. I will remember that.",
    )
    for path in (ROOT / "src/dialogs").rglob("*.py"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        for phrase in stale_phrases:
            assert phrase not in raw, f"{path.relative_to(ROOT)} still has flat menu voice: {phrase}"
    helper_dialogue = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    for phrase in stale_phrases:
        assert phrase not in helper_dialogue, f"sod_dialogue_immersion.py still has flat menu voice: {phrase}"

    assert_contains(
        read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_recruit_secondchance_02.py"),
        "The road is not ready for both of us yet",
    )
    assert_contains(
        read("src/dialogs/ZC02_townsfolk_and_special_npcs/trp_ramun_the_slave_trader_plyr_ramun_introduce_1_02.py"),
        "I have heard enough of this market",
    )
    assert_contains(
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prison_guard_talk_03.py"),
        "I have no business past the bars",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_supported_pretender_pretalk.py"),
        "The claim is still before us",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_looters_quest_destroyed_2_02.py"),
        "The roads are breathing easier now",
    )
    assert_contains(
        read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_02.py"),
        "May the road show you better manners",
    )
    assert_contains(
        read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_slavers_caravan_start.py"),
        "Spend it before the road takes it back",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_enemy_lord_tell_mission_02.py"),
        "There is no errand between us today",
    )
    assert_contains(
        read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_jester_plyr_jester_talk_08.py"),
        "Keep the bells warm",
    )
    assert_contains(
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_barter.py"),
        "the only bargain the road ever keeps",
    )
    assert_contains(
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_bandit_barter_3a.py"),
        "Coin weighs less than blood",
    )
    assert_contains(
        read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_troublesome_bandits_start.py"),
        "The town sent a hunter",
    )
    assert_contains(
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_slaver_world_caravan_talk.py"),
        "drag chains across this road",
    )
    assert_contains(
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_army_world_patrol_talk.py"),
        "Whose contract keeps your boots",
    )
    assert_contains(
        read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_sod_prisoner_train_talk.py"),
        "Name the chains in your wagons",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_mayor_begin_03.py"),
        "The watch still counts empty stalls",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_train_peasants_against_bandits_mission_accept.py"),
        "Teach them how to live through a raid",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_farmer_from_bandit_village_barter.py"),
        "seed hidden under floorboards",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_raise_troops_2.py"),
        "contracts are outpacing our barracks",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_tell_mission_collect_debt.py"),
        "put your ledger in front of",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_suggest_attack_enemy_party3.py"),
        "where the war can feel it",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_suggets_attack_enemy_castle3.py"),
        "test {s1}'s walls",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_give_oath_10.py"),
        "your courage is no longer only your own",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_convince_accept_06.py"),
        "made war harder to defend",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_pretender_end.py"),
        "A claim survives on more than courage",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told.py"),
        "Give me the charge",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_collect_taxes_told_02.py"),
        "Tax work makes enemies slowly",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_tell_mission_follow_spy_2.py"),
        "If your spy has a shadow",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_quest_looters_choice.py"),
        "feeding on the road",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_raid_caravan.py"),
        "war by another name",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_move_cattle_herd_quest_brief.py"),
        "stubborn horns included",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_sacrificed_messenger_3_02.py"),
        "dress murder as necessity",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_accepted.py"),
        "the charge is yours",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_deliver_message_accepted.py"),
        "sealed and paid for the road",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_hunt_down_fugitive_accepted.py"),
        "justice has a rider",
    )
    assert_contains(
        read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_mission_told_deliver_cattle_to_army_accepted.py"),
        "hunger starts giving orders",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_quest_meet_spy_in_enemy_town_accepted.py"),
        "a corpse or a trap",
    )
    assert_contains(
        read("src/dialogs/ZC01_centers_and_economy/anyone_village_elder_deliver_grain_mission_accept.py"),
        "supper, seed, and one less argument",
    )
    assert_contains(
        read("src/dialogs/ZZ99_misc_dialogs/anyone_capture_enemy_hero_thank.py"),
        "leverage with a pulse",
    )


def test_high_frequency_town_player_lines_have_scene_voice() -> None:
    checks = {
        "src/dialogs/ZC01_centers_and_economy/anyone_mayor_begin_09.py": "The town ledger is open",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_goods_merchant_talk.py": "Put the scales out",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk.py": "steel that has not yet disappointed",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk_02.py": "armor worth trusting",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk_03.py": "horses with road left",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_talk_04.py": "trouble has reached the village",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_talk_05.py": "coin rather than promises",
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_trade_begin.py": "if the village can spare them",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_dweller_talk_07.py": "when the watch is not listening",
        "src/dialogs/ZC01_centers_and_economy/anyone_town_dweller_ask_rumor.py": "not every name is safe",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_ransom_broker_info_talk_02.py": "before I start counting chains",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_trainer_talk_03.py": "Enough bruises for now",
    }
    for path, token in checks.items():
        assert_contains(read(path), token)


def test_legacy_copy_typos_do_not_regress() -> None:
    guild_history = read("src/dialogs/ZC01_centers_and_economy/anyone_gm_guild_history2_02.py")
    assert_contains(guild_history, "Prince Aahil")
    assert_contains(guild_history, "illegal duel")
    assert "Price Aahil" not in guild_history
    assert "illegal dual" not in guild_history

    common_execution = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_die4.py")
    assert_contains(common_execution, "You slit the prisoner's throat")
    assert "their throat" not in common_execution
    assert "his corpse" not in common_execution

    lord_execution = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_treason_execute.py")
    assert_contains(lord_execution, "watch the body sag to the floor")
    assert "satisfied, as his corpse" not in lord_execution


def test_companion_recruitment_flow_preserves_slot_driven_intro_chain() -> None:
    compiled = read("compile/module_dialogs.py")
    order = read("src/dialogs/_order_dialogs.txt")
    recruit_files = list((ROOT / "src/dialogs/ZE01_companions_and_named_npcs").glob("*companion_recruit*.py"))

    expected_edges = (
        "anyone::start->companion_recruit_intro_response",
        "anyone|plyr::companion_recruit_intro_response->companion_recruit_backstory_a",
        "anyone::companion_recruit_backstory_a->companion_recruit_backstory_b",
        "anyone::companion_recruit_backstory_b->companion_recruit_backstory_c",
        "anyone::companion_recruit_backstory_c->companion_recruit_backstory_response",
        "anyone|plyr::companion_recruit_backstory_response->companion_recruit_signup",
        "anyone::companion_recruit_signup->companion_recruit_signup_b",
        "anyone::companion_recruit_signup_b->companion_recruit_signup_response",
        "anyone|plyr::companion_recruit_signup_response->companion_recruit_payment",
        "anyone::companion_recruit_payment->companion_recruit_payment_response",
        "anyone|plyr::companion_recruit_payment_response->companion_recruit_signup_confirm",
        "anyone::companion_recruit_signup_confirm->close_window",
    )
    for edge in expected_edges:
        assert_contains(compiled, edge)

    for forbidden in (
        "anyone::companion_recruit_intro_response->companion_recruit_backstory_response",
        "anyone::event_triggered->companion_recruit_backstory_response",
        "anyone::event_triggered->companion_recruit_signup_response",
        "anyone::event_triggered->companion_recruit_payment_response",
        "plyr::companion_recruit_signup_response->close_window [no_conditions]",
        "plyr::companion_recruit_payment_response->companion_recruit_signup_response",
    ):
        assert forbidden not in compiled, f"companion recruit flow has unsafe edge: {forbidden}"

    slot_files = {
        "anyone_companion_recruit_backstory_a.py": "slot_troop_backstory_a",
        "anyone_companion_recruit_backstory_b.py": "slot_troop_backstory_b",
        "anyone_companion_recruit_backstory_c.py": "slot_troop_backstory_c",
        "anyone_companion_recruit_signup.py": "slot_troop_signup",
        "anyone_companion_recruit_signup_b.py": "slot_troop_signup_2",
        "anyone_companion_recruit_payment.py": "str_npc1_payment",
        "anyone_companion_recruit_backstory_delayed.py": "slot_troop_backstory_delayed",
    }
    for filename, token in slot_files.items():
        raw = read(f"src/dialogs/ZE01_companions_and_named_npcs/{filename}")
        assert_contains(raw, token)
        assert '"event_triggered"' not in raw, f"{filename} must not hijack generic event_triggered"

    recruit_register_files = {
        "anyone_companion_recruit_backstory_a.py": "{s68}",
        "anyone_companion_recruit_backstory_b.py": "{s68}",
        "anyone_companion_recruit_backstory_c.py": "{s68}",
        "anyone_companion_recruit_backstory_delayed.py": "{s68}",
        "anyone_companion_recruit_signup.py": "{s68}",
        "anyone_companion_recruit_signup_b.py": "{s68}",
        "anyone_companion_recruit_payment.py": "{s68}",
        "anyone_plyr_companion_recruit_intro_response.py": "{s69}",
        "anyone_plyr_companion_recruit_intro_response_02.py": "{s69}",
        "anyone_plyr_companion_recruit_backstory_response.py": "{s69}",
        "anyone_plyr_companion_recruit_backstory_response_02.py": "{s69}",
        "anyone_plyr_companion_recruit_signup_response_02.py": "{s69}",
        "anyone_plyr_companion_recruit_signup_response_03.py": "{s69}",
        "anyone_plyr_companion_recruit_payment_response.py": "{s69}",
        "anyone_plyr_companion_recruit_payment_response_02.py": "Your price is beyond my purse today.",
    }
    for filename, display_register in recruit_register_files.items():
        raw = read(f"src/dialogs/ZE01_companions_and_named_npcs/{filename}")
        assert_contains(raw, '(is_between, "$g_talk_troop", companions_begin, companions_end)')
        assert_contains(raw, display_register)
        for stale_register in ("{s5}", "{s6}", "{s7}"):
            assert_not_contains(raw, stale_register)
        for stale_store in (
            "(str_store_string, 5,",
            "(str_store_string, 6,",
            "(str_store_string, 7,",
            "(str_store_string, s5,",
            "(str_store_string, s6,",
            "(str_store_string, s7,",
            "(str_store_party_name, 20,",
        ):
            assert_not_contains(raw, stale_store)

    recruit_script = read("src/scripts/ZH_heroes/recruit_troop_as_companion.py")
    assert_contains(recruit_script, '(is_between, ":troop_no", 0, "trp_last_troop")')
    assert_contains(recruit_script, '(str_store_troop_name, s68, ":troop_no")')
    assert_contains(recruit_script, "@{s68} has joined your party.")
    assert_contains(recruit_script, "the company cannot identify them")
    assert_not_contains(recruit_script, "(str_store_troop_name, s6,")
    assert_not_contains(recruit_script, "@{s6} has joined your party")

    for path in recruit_files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        assert "event_triggered" not in raw, f"{path.relative_to(ROOT)} should not use event_triggered"

    assert_before(
        order,
        "ZA01_startup_and_dispatch/anyone_start_43.py",
        "ZE01_companions_and_named_npcs/anyone_plyr_companion_recruit_intro_response.py",
    )
    assert_before(
        order,
        "ZE01_companions_and_named_npcs/anyone_companion_recruit_backstory_a.py",
        "ZE01_companions_and_named_npcs/anyone_companion_recruit_signup.py",
    )


def test_high_frequency_lord_guild_and_gate_choices_have_scene_voice() -> None:
    checks = {
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_talk_18.py": "trust to my hands",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_talk_20.py": "carry your banner",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_talk_26.py": "army gathers here",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_20.py": "available soldiers before me",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_21.py": "formal pact",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_castle_gate_guard_talk_02.py": "asking for audience",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_castle_guard_intro_1.py": "business for your lord's ears",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_trainer_talk_combat.py": "steel from finding soft places",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_arena_intro_3.py": "once the shouting starts",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavern_traveler_talk_02.py": "rumors point",
    }
    for path, token in checks.items():
        assert_contains(read(path), token)


def test_common_mission_and_story_lines_avoid_placeholder_voice() -> None:
    checks = {
        "src/dialogs/ZC01_centers_and_economy/anyone_mayor_begin_07.py": "streets a little room to breathe",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_tell_mission_03.py": "dignity, baggage, and temper intact",
        "src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_24.py": "a grave with a banner",
        "src/dialogs/ZZ99_misc_dialogs/anyone_legate_joining_7.py": "tasteless sense of theater",
        "src/dialogs/ZZ99_misc_dialogs/anyone_cpehus_sane_1.py": "prefer my head where it is",
    }
    for path, token in checks.items():
        assert_contains(read(path), token)


def test_reports_and_tutorials_avoid_debug_copy() -> None:
    strings = read("compile/module_strings.py")
    guild_progress = read("src/scripts/ZY_helper_scripts/merc_describe_guild_progression.py")
    guild_summary = read("src/scripts/ZY_helper_scripts/merc_describe_report_summary.py")
    guild_standing = read("src/scripts/ZY_helper_scripts/merc_describe_standing_report.py")
    threat_contract = read("src/scripts/ZY_helper_scripts/sod_threat_board_describe_active_contract.py")
    threat_fail = read("src/scripts/ZY_helper_scripts/sod_threat_board_fail_contract.py")
    law_reports = read("src/scripts/ZZ_common_array_processing/sod_law_reports.py")

    for raw in (strings, guild_progress, guild_summary, guild_standing, threat_contract, threat_fail, law_reports):
        assert_not_contains(raw, "TODO:")
        assert_not_contains(raw, "Quest tier:")
        assert_not_contains(raw, "No active contract.")
        assert_not_contains(raw, "No active job board contract")
        assert_not_contains(raw, "This law record is invalid.")

    assert_contains(strings, "Follow the order marker and form up at the flag.")
    assert_contains(guild_progress, "Only courier work is being offered.")
    assert_contains(guild_summary, "No guild pact is on the books.")
    assert_contains(guild_standing, "Guild doors open in stages")
    assert_contains(threat_contract, "Regional Threat Warrant")
    assert_contains(threat_fail, "There is no posted warrant to abandon.")
    assert_contains(law_reports, "The court cannot read this law entry.")


def test_common_accept_refuse_and_exit_lines_have_scene_voice() -> None:
    checks = {
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk_03.py": "more than my purse can carry",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavern_mercenary_cant_lead.py": "work can find us",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_give_order_answer.py": "business has teeth",
        "src/dialogs/ZB01_lords_politics_and_family/anyone_lord_give_order_answer_2.py": "My men move at once",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_escort_merchant_caravan_quest_brief_03.py": "another shield",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_goods_merchant_talk_03.py": "Keep the scales covered",
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavern_traveler_talk_04.py": "my own to test",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_seneschal_talk_03.py": "household books",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_member_talk_06.py": "Back to the line",
    }
    for path, token in checks.items():
        assert_contains(read(path), token)


if __name__ == "__main__":
    test_lord_personality_greeting_is_wired_before_fallback()
    test_mayor_social_weather_is_wired_before_fallbacks()
    test_village_elder_social_weather_is_wired_before_fallback()
    test_goods_merchant_social_weather_is_wired_after_courier_rumor_before_fallback()
    test_tavernkeeper_social_weather_is_wired_after_courier_rumor_before_fallback()
    test_nonplayer_patrol_immersion_start_is_wired_before_functional_patrol_start()
    test_castle_patrol_authority_dialogue_covers_law_contraband_and_command_tone()
    test_special_patrol_start_lines_are_relation_aware_and_faction_flavored()
    test_world_presence_start_lines_are_relation_aware_for_conquistador_and_jotnar()
    test_serpent_and_boar_start_lines_are_relation_aware()
    test_merchant_caravan_world_talk_is_wired_after_escort_starts()
    test_deserter_start_lines_cover_hunger_service_and_mercy()
    test_bandit_lines_cover_strength_reputation_and_intimidation()
    test_guild_master_social_weather_is_wired_before_pretalk_fallback()
    test_visible_dialogue_avoids_flat_menu_voice_backouts()
    test_companion_recruitment_flow_preserves_slot_driven_intro_chain()
    test_high_frequency_town_player_lines_have_scene_voice()
    test_high_frequency_lord_guild_and_gate_choices_have_scene_voice()
    test_common_mission_and_story_lines_avoid_placeholder_voice()
    test_reports_and_tutorials_avoid_debug_copy()
    test_common_accept_refuse_and_exit_lines_have_scene_voice()
    print("test_dialogue_immersion_static: OK")
