# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    troops = read("compile/module_troops.py")
    factions = read("compile/module_factions.py")
    module_parties = read("compile/module_parties.py")
    party_templates = read("compile/module_party_templates.py")
    mission = read("src/mission_templates/0043_sod_arena_duel_fight/sod_arena_duel_fight.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    hourly = read("src/triggers/ST02_every_hour/entry_0159.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    dialogs_order = read("src/dialogs/_order_dialogs.txt")
    menus_order = read("src/menus/_order_game_menus.txt")
    reports = read("src/menus/0000_hardcoded_mb1011/reports.py")
    report_submenus = read("src/menus/reports/report_submenus.py")
    dashboard = read("src/menus/reports/mercenary_world_activity_report.py")
    black_army = read("src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py")
    serpent_host = read("src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py")
    faction_notes = read("src/scripts/ZF_factions/update_faction_notes.py")

    for token in (
        "slot_faction_black_khergit_pressure",
        "slot_faction_black_khergit_camp_party",
        "slot_faction_black_khergit_target_center",
        "slot_faction_black_khergit_last_migration_day",
        "slot_faction_black_khergit_last_spawn_day",
        "slot_faction_black_khergit_tribute",
        "slot_faction_black_khergit_safe_passage_until",
        "slot_faction_black_khergit_camp_disrupted_until",
        "slot_faction_black_khergit_last_raid_report_day",
        "slot_faction_black_khergit_last_pressure_day",
        "slot_faction_black_khergit_target_lock_until",
        "slot_faction_black_khergit_last_seen_center",
        "slot_faction_black_khergit_last_seen_day",
        "slot_troop_black_khergit_khan_duel_losses",
        "slot_party_black_khergit_camp_activity",
        "slot_party_black_khergit_origin",
        "slot_party_black_khergit_target",
        "slot_party_black_khergit_role",
        "slot_party_black_khergit_response_until",
        "slot_party_black_khergit_response_target",
        "sod_black_khergit_role_camp",
        "sod_black_khergit_action_bribe_target",
        "sod_black_khergit_action_persuade_enemy",
        "sod_black_khergit_action_defeat_guards",
        "sod_black_khergit_action_duel_victory",
        "sod_black_khergit_action_duel_defeat",
    ):
        assert_contains(constants, token)

    assert_contains(troops, '"black_khergit_khan"')
    assert_contains(troops, "Temujin Black Sky")
    assert_contains(troops, "tf_hero|tf_mounted")
    assert_contains(factions, '("black_khergits", "Black Khergits"')
    assert_contains(factions, "0x0B1B3D")
    for kingdom in ("kingdom_1", "kingdom_2", "kingdom_3", "kingdom_4", "kingdom_5", "kingdom_6"):
        assert_contains(factions, f'("{kingdom}", -0.15)')
    assert_contains(module_parties, '"black_khergit_spawn_point"')
    assert_contains(module_parties, '"{!}black_khergit_sp"')
    assert_contains(module_parties, "pf_disabled|pf_is_static")
    assert_contains(module_parties, "fac_black_khergits")
    assert_contains(module_parties, "(155.349, -101.135)")

    for token in (
        '"black_khergit_raiders"',
        '"black_khergit_horde_camp"',
        '"black_khergit_night_guard"',
        "trp_black_khergit_horseman",
        "trp_black_khergit_guard",
        "trp_black_khergit_khan",
        "fac_black_khergits",
    ):
        assert_contains(party_templates, token)
    assert_contains(party_templates, '"black_khergit_raiders","Black Khergit Raiders",icon_khergit_horseman_b|carries_goods(8)')
    assert_contains(party_templates, "[(trp_black_khergit_guard,1,4),(trp_black_khergit_horseman,8,16)]")
    assert_contains(party_templates, '"black_khergit_horde_camp","Black Khergit Horde Camp",icon_khergit_horseman_b|carries_goods(80)')
    assert_contains(party_templates, "[(trp_black_khergit_khan,1,1),(trp_black_khergit_guard,25,45),(trp_black_khergit_horseman,80,130)]")
    assert_contains(party_templates, '"black_khergit_night_guard","Black Khergit Night Guard",icon_khergit_horseman_b|carries_goods(4)')
    assert_contains(party_templates, "[(trp_black_khergit_guard,3,7),(trp_black_khergit_horseman,8,14)]")

    for script_name in (
        '"sod_black_khergits_update_horde_state"',
        '"sod_black_khergits_initialize_world_presence"',
        '"sod_black_khergits_process_pressure_economy"',
        '"sod_black_khergits_lock_camped_ai"',
        '"sod_black_khergits_spawn_or_recover_camp"',
        '"sod_black_khergits_process_day_cycle"',
        '"sod_black_khergits_spawn_raids"',
        '"sod_black_khergits_apply_player_action"',
        '"sod_black_khergits_apply_safe_passage_to_party"',
        '"sod_black_khergits_scatter_or_cleanup_patrols"',
        '"sod_black_khergits_update_scout_intelligence"',
        '"sod_black_khergits_process_scattered_raider_aftermath"',
        '"sod_black_khergits_process_ai_responses"',
        '"sod_black_khergits_note_ai_battle_outcome"',
        '"sod_black_khergits_choose_relocation_target"',
        '"sod_black_khergits_resolve_khan_duel"',
        '"sod_black_khergits_strengthen_khan_after_duel_loss"',
        '"sod_black_khergits_enforce_player_standing"',
        '"sod_black_khergits_prepare_hire_offer"',
        '"sod_black_khergits_buy_hire_offer"',
        '"sod_black_khergits_release_hero_prisoners"',
        '"sod_black_khergits_prepare_prisoner_purchase_offer"',
        '"sod_black_khergits_buy_prisoners"',
        '"sod_black_khergits_refresh_active_parties"',
        '"sod_black_khergits_describe_status_to_s27"',
    ):
        assert_contains(scripts, script_name)

    assert_contains(scripts, "store_current_hours")
    assert_contains(scripts, '(faction_set_slot, "fac_black_khergits", slot_faction_black_khergit_pressure, 18)')
    assert_contains(game_start, "script_sod_black_khergits_initialize_world_presence")
    assert_contains(game_start, "script_ai_hire_mercenaries")
    assert_contains(scripts, '(assign, ":spawn_center", "p_black_khergit_spawn_point")')
    assert_contains(scripts, '(set_spawn_radius, 1)')
    assert_contains(scripts, '(party_set_icon, ":camp_party", "icon_khergit_horseman_b")')
    assert_contains(scripts, '(party_set_icon, ":camp_party", "icon_camp")')
    assert_contains(scripts, '(party_is_active, ":camp_party")')
    assert_contains(scripts, '(party_get_template_id, ":template", ":camp_party")')
    assert_contains(scripts, '(eq, ":template", "pt_black_khergit_horde_camp")')
    assert_contains(scripts, '(assign, ":camp_valid", 0)')
    assert_contains(scripts, '(call_script, "script_cf_sod_black_khergits_party_is_horde_camp", ":camp_party")')
    assert_contains(scripts, '(party_set_ai_initiative, ":camp_party", 0)')
    assert_contains(scripts, '(party_set_slot, ":camp_party", slot_party_ai_object, 0)')
    assert_contains(scripts, '(party_set_slot, ":camp_party", slot_party_follow_me, 0)')
    assert_contains(scripts, '(call_script, "script_sod_black_khergits_lock_camped_ai", ":camp_party")')
    assert_contains(scripts, '(eq, ":is_night", 1)')
    assert_contains(scripts, '(party_set_ai_behavior, ":camp_party", ai_bhvr_hold)')
    assert_contains(scripts, '(call_script, "script_sod_black_khergits_lock_camped_ai", ":party_no")')
    assert_contains(scripts, '(eq, ":is_night", 0)')
    assert_contains(scripts, '(party_slot_eq, ":camp_party", slot_party_black_khergit_target, ":target_center")')
    assert_contains(scripts, '(gt, ":camp_target_dist", 3)')
    assert_contains(scripts, '(party_set_ai_object, ":camp_party", ":target_center")')
    assert_contains(scripts, '(party_get_attached_to, ":attached_to", ":guard_party")')
    assert_contains(scripts, '(party_detach, ":guard_party")')
    assert_contains(scripts, '(party_set_ai_behavior, ":guard_party", ai_bhvr_travel_to_party)')
    assert_contains(scripts, '(party_set_ai_object, ":guard_party", ":camp_party")')
    assert_contains(scripts, '(le, ":guard_dist", 1)')
    assert_contains(scripts, 'script_party_prisoners_add_party_prisoners')
    assert_contains(scripts, 'script_party_remove_all_prisoners')
    assert_contains(scripts, 'script_remove_troop_from_prison')
    assert_contains(scripts, 'slot_troop_prisoner_of_party')
    assert_contains(scripts, '$g_sod_black_khergit_prisoner_buy_count')
    assert_contains(scripts, '$g_sod_black_khergit_prisoner_buy_cost')
    assert_contains(scripts, 'sod_black_khergits_release_hero_prisoners')
    assert_contains(scripts, 'sod_black_khergits_prepare_prisoner_purchase_offer')
    assert_contains(scripts, 'sod_black_khergits_buy_prisoners')
    assert_contains(scripts, '(party_attach_to_party, ":guard_party", ":camp_party")')
    assert_contains(scripts, '(party_set_ai_behavior, ":guard_party", ai_bhvr_hold)')
    assert_contains(scripts, '(party_set_icon, ":party_no", "icon_camp")')
    assert_contains(scripts, '(party_is_active, ":party_no")')
    assert_contains(scripts, '(neg|is_between, ":target_center", centers_begin, centers_end)')
    assert_contains(scripts, '(is_between, ":stored_target", centers_begin, centers_end)')
    assert_contains(scripts, '(party_set_slot, ":party_no", slot_party_black_khergit_origin, ":camp_party")')
    assert_contains(scripts, '(party_set_ai_patrol_radius, ":party_no", 8)')
    assert_contains(scripts, "slot_faction_black_khergit_target_lock_until")
    assert_contains(scripts, "script_sod_black_khergits_scatter_or_cleanup_patrols")
    assert_contains(scripts, "The Black Khergit Khan takes the silver")
    assert_contains(scripts, "night guards vanish and loose raiders scatter")
    assert_contains(scripts, '(party_set_ai_patrol_radius, ":party_no", 18)')
    assert_contains(scripts, "script_sod_black_khergits_update_scout_intelligence")
    assert_contains(scripts, "script_sod_black_khergits_process_scattered_raider_aftermath")
    assert_contains(scripts, "last seen near")
    assert_contains(scripts, "Deshavi finds steppe ash")
    assert_contains(scripts, "script_change_troop_renown")
    assert_contains(scripts, "sod_black_khergit_action_duel_victory")
    assert_contains(scripts, "sod_black_khergit_action_duel_defeat")
    assert_contains(scripts, "Temujin Black Sky yields the field")
    assert_contains(scripts, "script_sod_black_khergits_strengthen_khan_after_duel_loss")
    assert_contains(scripts, 'slot_troop_black_khergit_khan_duel_losses')
    assert_contains(scripts, '(add_xp_to_troop, ":xp_gain", "trp_black_khergit_khan")')
    assert_contains(scripts, '(troop_raise_attribute, "trp_black_khergit_khan", ca_strength, 1)')
    assert_contains(scripts, '(troop_raise_attribute, "trp_black_khergit_khan", ca_agility, 1)')
    assert_contains(scripts, '(troop_raise_skill, "trp_black_khergit_khan", "skl_ironflesh", 1)')
    assert_contains(scripts, '(troop_raise_skill, "trp_black_khergit_khan", "skl_power_strike", 1)')
    assert_contains(scripts, '(troop_raise_skill, "trp_black_khergit_khan", "skl_horse_archery", 1)')
    assert_contains(scripts, '(troop_raise_proficiency_linear, "trp_black_khergit_khan", wpt_archery, ":prof_bonus")')
    assert_contains(scripts, "Temujin Black Sky remembers defeat")
    assert_contains(scripts, '(call_script, "script_change_player_relation_with_faction", "fac_black_khergits", 10)')
    assert_contains(scripts, '(ge, ":player_relation", 100)')
    assert_contains(scripts, '(set_relation, "fac_black_khergits", "fac_player_faction", 100)')
    assert_contains(scripts, '(faction_set_slot, "fac_black_khergits", slot_faction_black_khergit_pressure, 0)')
    assert_contains(scripts, "blood-respected")
    assert_contains(scripts, 'party_add_members, "p_main_party", "trp_black_khergit_horseman"')
    assert_contains(scripts, 'party_add_members, "p_main_party", "trp_black_khergit_guard"')
    assert_contains(scripts, "$g_sod_black_khergit_hire_cost")
    assert_contains(scripts, "hire bargain cannot be completed")
    assert_contains(scripts, "script_sod_black_khergits_choose_relocation_target")
    assert_contains(scripts, "pt_black_khergit_night_guard")
    assert_contains(mission, "$g_sod_black_khergit_duel_active")
    assert_contains(mission, "script_sod_black_khergits_resolve_khan_duel")
    assert_contains(scripts, "pt_merchant_caravan")
    assert_contains(scripts, "road_dist")
    assert_contains(scripts, "(le, \":road_dist\", 18)")
    assert_contains(scripts, "slot_town_prosperity")
    assert_contains(scripts, "slot_town_wealth")
    assert_contains(scripts, "ai_bhvr_attack_party")
    assert_contains(scripts, "remove_party")
    assert_contains(scripts, "slot_faction_black_khergit_safe_passage_until")
    assert_contains(scripts, "slot_faction_black_khergit_camp_disrupted_until")
    assert_contains(scripts, "slot_faction_black_khergit_last_raid_report_day")
    assert_contains(scripts, "slot_faction_black_khergit_last_pressure_day")
    assert_contains(scripts, "party_ignore_player")
    assert_contains(scripts, "safe-passage hours")
    assert_contains(scripts, "camp disrupted until day")
    assert_contains(scripts, "days remaining")
    assert_contains(scripts, "last reported raid day")
    assert_contains(scripts, "Black Khergit raiders are stripping wealth")
    assert_contains(scripts, "Black Khergit riders have found a caravan")
    assert_contains(scripts, "script_sod_black_khergits_process_pressure_economy")
    assert_contains(scripts, "script_sod_black_khergits_refresh_active_parties")
    assert_contains(scripts, "spai_patrolling_around_center")
    assert_contains(spawns, "script_sod_black_khergits_spawn_or_recover_camp")
    assert_contains(spawns, "script_sod_black_khergits_spawn_raids")
    assert_contains(hourly, "script_sod_black_khergits_process_day_cycle")
    assert_contains(hourly, "script_sod_black_khergits_process_ai_responses")
    assert_contains(trigger_order, "ST02_every_hour/entry_0159.py")
    assert_contains(weekly, "script_sod_black_khergits_spawn_or_recover_camp")
    assert_contains(daily, "script_sod_black_khergits_spawn_raids")

    for dialog in (
        "party_tpl_pt_black_khergit_horde_camp_start.py",
        "party_tpl_pt_black_khergit_raiders_start.py",
        "party_tpl_pt_black_khergit_night_guard_start.py",
        "anyone_black_khergit_khan_audience_blood_respected.py",
        "anyone_black_khergit_khan_audience.py",
        "anyone_plyr_black_khergit_khan_talk_blood_respected.py",
        "anyone_black_khergit_khan_blood_respected_warmth.py",
        "anyone_plyr_black_khergit_khan_talk.py",
        "anyone_plyr_black_khergit_khan_talk_02.py",
        "anyone_plyr_black_khergit_khan_hire_offer.py",
        "anyone_black_khergit_khan_hire_offer.py",
        "anyone_plyr_black_khergit_khan_hire_confirm.py",
        "anyone_plyr_black_khergit_khan_hire_confirm_cannot_pay.py",
        "anyone_black_khergit_khan_hire_cannot_pay.py",
        "anyone_plyr_black_khergit_khan_hire_confirm_decline.py",
        "anyone_plyr_black_khergit_khan_prisoner_offer.py",
        "anyone_black_khergit_khan_prisoner_offer.py",
        "anyone_plyr_black_khergit_khan_prisoner_confirm.py",
        "anyone_plyr_black_khergit_khan_prisoner_confirm_cannot.py",
        "anyone_plyr_black_khergit_khan_prisoner_confirm_decline.py",
        "anyone_plyr_black_khergit_khan_duel.py",
        "anyone_plyr_black_khergit_khan_duel_no_horse.py",
        "anyone_black_khergit_khan_duel_no_horse.py",
        "anyone_plyr_black_khergit_khan_talk_03_blood_respected.py",
        "anyone_plyr_black_khergit_camp_talk_mark.py",
        "anyone_black_khergit_camp_mark.py",
        "anyone_plyr_black_khergit_camp_talk_02.py",
        "anyone_plyr_black_khergit_camp_talk_03.py",
    ):
        assert_contains(dialogs_order, dialog)

    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_talk.py"), "sod_black_khergit_action_bribe_target")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_audience_blood_respected.py"), "blood-respected friend")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_audience_blood_respected.py"), '(ge, ":relation", 100)')
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_blood_respected_warmth.py"), "Eat before you speak of roads")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_talk_03_blood_respected.py"), "friend")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_talk_02.py"), "sod_black_khergit_action_persuade_enemy")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_hire_offer.py"), "script_sod_black_khergits_prepare_hire_offer")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_hire_offer.py"), "slot_faction_black_khergit_pressure")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_hire_offer.py"), "{reg40} horsemen and {reg41} camp guards")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_hire_confirm.py"), "script_sod_black_khergits_buy_hire_offer")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_prisoner_offer.py"), "script_sod_black_khergits_prepare_prisoner_purchase_offer")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_prisoner_offer.py"), "Heroes we do not sell")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_prisoner_confirm.py"), "script_sod_black_khergits_buy_prisoners")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_duel.py"), "ek_horse")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_duel.py"), "mnu_sod_black_khergit_khan_duel_prepare")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_duel.py"), "(finish_mission)")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_camp_talk_02.py"), "sod_black_khergit_action_tribute")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_raider_talk_02.py"), "sod_black_khergit_action_defeat_raiders")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_guard_talk.py"), "sod_black_khergit_action_defeat_guards")
    horde_report = read("src/menus/reports/black_khergit_horde_report.py")
    assert_contains(horde_report, "Black Khergit Moving Horde")
    assert_contains(horde_report, "black_khergit_horde_report_bribe")
    assert_contains(horde_report, "sod_black_khergit_action_bribe_target")
    assert_contains(horde_report, "$g_sod_black_khergit_last_report_bribe_day")
    assert_contains(horde_report, "black_khergit_horde_report_enemy")
    assert_contains(horde_report, "sod_black_khergit_action_persuade_enemy")
    assert_contains(horde_report, "$g_sod_black_khergit_last_report_persuasion_day")
    assert_contains(reports, "mnu_mini_faction_reports")
    assert_contains(report_submenus, "mnu_black_khergit_horde_report")
    assert_contains(read("src/menus/_order_game_menus.txt"), "reports/black_khergit_horde_report.py")
    assert_contains(dashboard, "script_sod_black_khergits_describe_status_to_s27")
    assert_contains(black_army, "slot_party_black_khergit_camp_activity")
    assert_contains(serpent_host, "slot_faction_black_khergit_pressure")
    assert_contains(faction_notes, "script_sod_black_khergits_describe_status_to_s27")

    camp_start = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_black_khergit_horde_camp_start.py")
    assert_contains(camp_start, "store_current_hours")
    assert_contains(camp_start, "(store_mod, \":hour_of_day\", \":cur_hours\", 24)")
    assert_contains(camp_start, "(eq, \":is_night\", 1)")
    assert_contains(camp_start, '"black_khergit_camp_talk"')
    assert_contains(camp_start, "(eq, \":is_night\", 0)")
    assert_contains(camp_start, '"black_khergit_khan_field_audience"')
    for dialog in (
        "anyone_black_khergit_khan_field_audience_blood_respected.py",
        "anyone_black_khergit_khan_field_audience.py",
        "anyone_plyr_black_khergit_khan_field_talk_blood_respected.py",
        "anyone_black_khergit_khan_field_warm_road.py",
        "anyone_plyr_black_khergit_khan_field_talk_blood_respected_02.py",
        "anyone_black_khergit_khan_field_warm_route.py",
        "anyone_plyr_black_khergit_khan_field_talk_blood_respected_03.py",
        "anyone_plyr_black_khergit_khan_field_talk.py",
        "anyone_plyr_black_khergit_khan_field_talk_02.py",
        "anyone_plyr_black_khergit_khan_field_duel.py",
        "anyone_plyr_black_khergit_khan_field_duel_no_horse.py",
        "anyone_black_khergit_khan_field_duel_no_horse.py",
        "anyone_plyr_black_khergit_khan_field_about.py",
        "anyone_black_khergit_khan_field_about.py",
        "anyone_plyr_black_khergit_khan_field_attack.py",
        "anyone_plyr_black_khergit_khan_field_leave.py",
    ):
        assert_contains(dialogs_order, dialog)
    field_audience = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_field_audience.py")
    field_audience_warm = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_field_audience_blood_respected.py")
    field_warm_road = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_field_warm_road.py")
    field_warm_route = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_field_warm_route.py")
    field_talk = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_field_talk.py")
    field_duel = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_field_duel.py")
    field_about = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_field_about.py")
    khan_duel_menu = read("src/menus/duels/black_khergit_khan_duel_prepare.py")
    assert_contains(field_audience, "while the wheels are turning")
    assert_contains(field_audience_warm, '"black_khergit_khan_field_talk_blood_respected"')
    assert_contains(field_warm_road, "my scouts lower their bows")
    assert_contains(field_warm_route, "Your lands are not meat for my riders now")
    assert_contains(field_talk, "sod_black_khergit_action_bribe_target")
    assert_contains(field_duel, "mnu_sod_black_khergit_khan_duel_prepare")
    assert_contains(field_about, "A camp has roots. A horde has hunger.")
    assert_contains(menus_order, "duels/black_khergit_khan_duel_prepare.py")
    assert_contains(khan_duel_menu, '"sod_black_khergit_khan_duel_prepare"')
    assert_contains(khan_duel_menu, "(set_jump_entry, 56)")
    assert_contains(khan_duel_menu, '(set_visitor, 56, "trp_player")')
    assert_contains(khan_duel_menu, '(set_visitor, 58, "trp_black_khergit_khan")')
    assert_contains(khan_duel_menu, '(set_jump_mission, "mt_sod_arena_duel_fight")')
    assert_contains(khan_duel_menu, "(change_screen_mission)")

    print("[black_khergit_horde_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



