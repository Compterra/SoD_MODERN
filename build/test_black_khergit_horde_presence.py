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
    party_templates = read("compile/module_party_templates.py")
    mission = read("src/mission_templates/0043_sod_arena_duel_fight/sod_arena_duel_fight.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    spawns = read("src/scripts/ZZ_common_array_processing/spawn_bandits.py")
    daily = read("src/triggers/ST03_daily/entry_0158.py")
    hourly = read("src/triggers/ST02_every_hour/entry_0159.py")
    weekly = read("src/triggers/ST04_weekly/entry_0126.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    dialogs_order = read("src/dialogs/_order_dialogs.txt")
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

    for script_name in (
        '"sod_black_khergits_update_horde_state"',
        '"sod_black_khergits_process_pressure_economy"',
        '"sod_black_khergits_spawn_or_recover_camp"',
        '"sod_black_khergits_process_day_cycle"',
        '"sod_black_khergits_spawn_raids"',
        '"sod_black_khergits_apply_player_action"',
        '"sod_black_khergits_apply_safe_passage_to_party"',
        '"sod_black_khergits_scatter_or_cleanup_patrols"',
        '"sod_black_khergits_update_scout_intelligence"',
        '"sod_black_khergits_process_scattered_raider_aftermath"',
        '"sod_black_khergits_choose_relocation_target"',
        '"sod_black_khergits_resolve_khan_duel"',
        '"sod_black_khergits_strengthen_khan_after_duel_loss"',
        '"sod_black_khergits_enforce_player_standing"',
        '"sod_black_khergits_prepare_hire_offer"',
        '"sod_black_khergits_buy_hire_offer"',
        '"sod_black_khergits_refresh_active_parties"',
        '"sod_black_khergits_describe_status_to_s27"',
    ):
        assert_contains(scripts, script_name)

    assert_contains(scripts, "store_current_hours")
    assert_contains(scripts, '(party_set_icon, ":camp_party", "icon_khergit_horseman_b")')
    assert_contains(scripts, '(party_set_icon, ":camp_party", "icon_camp")')
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
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_duel.py"), "trp_black_khergit_khan")
    assert_contains(read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_duel.py"), "ek_horse")
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

    print("[black_khergit_horde_presence] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



