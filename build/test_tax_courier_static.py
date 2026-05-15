# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def assert_before(raw: str, first: str, second: str) -> None:
    assert first in raw, f"missing token: {first}"
    assert second in raw, f"missing token: {second}"
    assert raw.index(first) < raw.index(second), f"{first} should appear before {second}"


def test_tax_courier_constants_and_slots_exist() -> None:
    constants = read("src/constants/module_constants.py")
    for token in (
        "spt_messenger",
        "sod_messenger_role_tax_courier = 1",
        "sod_tax_courier_status_traveling = 1",
        "sod_tax_courier_status_delivered = 2",
        "sod_tax_courier_status_lost = 3",
        "sod_tax_courier_status_expired = 4",
        "slot_party_sod_messenger_role",
        "slot_party_sod_tax_courier_origin_center",
        "slot_party_sod_tax_courier_recipient_troop",
        "slot_party_sod_tax_courier_destination_party",
        "slot_party_sod_tax_courier_amount",
        "slot_party_sod_tax_courier_rents",
        "slot_party_sod_tax_courier_tariffs",
        "slot_party_sod_tax_courier_created_day",
        "slot_party_sod_tax_courier_expiry_day",
        "slot_party_sod_tax_courier_status",
        "slot_center_sod_active_tax_courier",
        "slot_center_sod_last_tax_courier_day",
        "slot_center_sod_tax_courier_losses",
    ):
        assert_contains(constants, token)


def test_ai_dispatch_replaces_weekly_invisible_transfer() -> None:
    weekly = read("src/triggers/ST04_weekly/entry_0039.py")
    assert_contains(weekly, '"script_sod_try_dispatch_ai_tax_courier_from_center"')
    assert_contains(weekly, '"script_sod_try_dispatch_player_tax_courier_from_center"')
    assert_contains(weekly, "(eq, \":town_lord\", \"trp_player\")")
    assert "val_mul, \":accumulated_rents\", 80" not in weekly
    assert "val_add, \":troop_wealth\", \":accumulated_rents\"" not in weekly


def test_tax_courier_scripts_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    for token in (
        '("sod_tax_courier_center_has_remittance_building"',
        '("cf_sod_tax_courier_origin_safe_to_dispatch"',
        '("cf_sod_tax_courier_destination_safe"',
        '("sod_tax_courier_resolve_destination"',
        '("cf_sod_create_tax_courier"',
        '("sod_try_dispatch_player_tax_courier_from_center"',
        '("sod_try_dispatch_ai_tax_courier_from_center"',
        '("sod_process_tax_courier_parties"',
        '("sod_tax_courier_cleanup_party"',
        '("sod_tax_courier_resolve_defeated_by_party"',
        '("sod_tax_courier_apply_nonhostile_coercion_consequence"',
        '("sod_tax_courier_award_payload_to_player"',
        '("sod_tax_courier_surrender_to_player"',
    ):
        assert_contains(scripts, token)


def test_dispatch_accounting_and_safety_are_conservative() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    party_templates = read("compile/module_party_templates.py")
    triggers = read("compile/module_triggers.py")

    assert_contains(party_templates, '("messenger_party","Messenger"')
    assert_contains(party_templates, "merchant_personality,[])")
    create_start = scripts.index('("cf_sod_create_tax_courier"')
    create_end = scripts.index('("sod_try_dispatch_player_tax_courier_from_center"', create_start)
    create_script = scripts[create_start:create_end]
    assert_before(create_script, '(gt, ":courier_party", 0)', '(party_is_active, ":courier_party")')
    assert_before(create_script, '(party_is_active, ":courier_party")', '(party_set_faction, ":courier_party", ":origin_faction")')
    assert_contains(scripts, "(faction_get_slot, \":messenger_troop\", \":origin_faction\", slot_faction_messenger_troop)")
    assert_contains(scripts, "(assign, \":messenger_troop\", \"trp_swadian_messenger\")")
    assert_contains(scripts, "(party_add_leader, \":courier_party\", \":messenger_troop\")")
    assert_contains(triggers, '(store_random_party_of_template, reg(2), "pt_messenger_party")')
    assert_contains(triggers, "(party_slot_eq, reg(2), slot_party_sod_messenger_role, sod_messenger_role_none)")
    assert_contains(scripts, "(val_div, \":center_reserve\", 5)")
    assert_contains(scripts, "(val_mul, \":direct_share\", 60)")
    assert_contains(scripts, "(val_sub, \":courier_share\", \":direct_share\")")
    assert_contains(scripts, "(assign, \":minimum_payload\", 300)")
    assert_contains(scripts, "(assign, \":minimum_payload\", 800)")
    assert_contains(scripts, '"script_cf_sod_tax_courier_origin_safe_to_dispatch"')
    assert_contains(scripts, "slot_center_is_besieged_by")
    assert_contains(scripts, "svs_being_raided")
    assert_contains(scripts, "svs_looted")
    assert_contains(scripts, '("cf_sod_tax_courier_destination_safe"')
    assert_contains(scripts, "(call_script, \"script_cf_sod_tax_courier_destination_safe\", \":destination\")")
    assert_contains(scripts, "(call_script, \"script_cf_sod_tax_courier_destination_safe\", \":new_destination\")")
    assert_contains(scripts, "(assign, \":danger_radius\", 7)")
    assert_contains(scripts, "(party_set_ai_behavior, \":courier_party\", ai_bhvr_travel_to_party)")
    assert_contains(scripts, "@Your Tax Courier from {s68}")
    assert_contains(scripts, "@Tax Courier from {s68}")
    assert_contains(scripts, "(party_set_name, \":courier_party\", s69)")
    assert_not_contains(scripts, "@Your Tax Courier from {s1}")
    assert_not_contains(scripts, "@Tax Courier from {s1}")
    assert_not_contains(scripts, "(party_set_name, \":courier_party\", s2)")
    assert_contains(scripts, "script_sod_center_clear_revenue_accounts")


def test_player_courier_collection_and_toggle_are_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    camp = read("src/menus/0000_hardcoded_mb1011/camp_action.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    pay_day = read("src/menus/0000_hardcoded_mb1011/pay_day.py")

    assert_contains(scripts, '("sod_try_dispatch_player_tax_courier_from_center"')
    assert_contains(scripts, "(eq, \"$g_sod_player_tax_couriers_enabled\", 1)")
    assert_contains(scripts, "(party_slot_eq, \":center_no\", slot_town_lord, \"trp_player\")")
    assert_contains(scripts, "(call_script, \"script_cf_sod_create_tax_courier\", \":center_no\", \"trp_player\"")
    assert_contains(scripts, "(eq, \":recipient_lord\", \"trp_player\")")
    assert_contains(scripts, "(assign, reg0, \"p_main_party\")")
    assert_contains(scripts, "(call_script, \"script_troop_add_gold\", \"trp_player\", \":payload\")")
    assert_contains(scripts, "for your coffers")
    assert_contains(scripts, "delivered {reg1} denars to your coffers")
    assert_contains(camp, "camp_disable_player_tax_couriers")
    assert_contains(camp, "camp_enable_player_tax_couriers")
    assert_contains(camp, "(assign, \"$g_sod_player_tax_couriers_enabled\", 0)")
    assert_contains(camp, "(assign, \"$g_sod_player_tax_couriers_enabled\", 1)")
    assert_contains(game_start, "(assign, \"$g_sod_player_tax_couriers_enabled\", 1)")
    assert_contains(pay_day, "(neq, \"$g_sod_player_tax_couriers_enabled\", 1)")


def test_non_native_factions_use_dedicated_messenger_troops() -> None:
    troops = read("compile/module_troops.py")
    ids = read("compile/ids/ID_troops.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    player_faction = read("src/scripts/ZF_factions/activate_deactivate_player_faction.py")

    for troop_id in (
        "ief_messenger",
        "sod_ant_messenger",
        "sod_mar_messenger",
        "sod_ade_messenger",
        "sod_vil_messenger",
        "sod_zer_messenger",
    ):
        assert_contains(troops, f'["{troop_id}"')
        assert_contains(ids, f"trp_{troop_id} = ")
        troop_block = troops[troops.index(f'["{troop_id}"'):]
        troop_block = troop_block[: troop_block.index("],\n\n") + 3]
        assert_contains(troop_block, "tf_mounted")
        assert_contains(troop_block, "tf_guarantee_horse")
        assert_contains(troop_block, "agi_21|level(25)")
        assert_contains(troop_block, "knows_riding_7")

    assert_contains(game_start, 'slot_faction_messenger_troop, "trp_ief_messenger"')
    assert 'slot_faction_messenger_troop, "trp_ief_speculatores"' not in game_start
    for troop_id in (
        "trp_sod_ant_messenger",
        "trp_sod_mar_messenger",
        "trp_sod_ade_messenger",
        "trp_sod_vil_messenger",
        "trp_sod_zer_messenger",
    ):
        assert_contains(player_faction, f'slot_faction_messenger_troop, "{troop_id}"')
    for old_troop_id in (
        "trp_sod_ant_scout",
        "trp_sod_mar_scout",
        "trp_sod_ade_light",
        "trp_sod_vil_scout",
        "trp_sod_zer_1_cavalry",
    ):
        assert f'slot_faction_messenger_troop, "{old_troop_id}"' not in player_faction


def test_processing_handles_delivery_expiry_and_loss_cleanup() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    assert_contains(scripts, "(party_get_slot, \":created_day\", \":courier_party\", slot_party_sod_tax_courier_created_day)")
    assert_contains(scripts, "(party_get_slot, \":expiry_day\", \":courier_party\", slot_party_sod_tax_courier_expiry_day)")
    assert_before(
        scripts,
        "(ge, \":cur_day\", \":expiry_day\")",
        "(call_script, \"script_sod_tax_courier_resolve_destination\", \":origin_center\", \":recipient_lord\")",
    )
    assert_contains(scripts, "expired; {reg1} denars return to the center accounts")
    assert_contains(scripts, "expired after hostile control changed")
    assert_contains(scripts, "(assign, \":destination_invalid\", 0)")
    assert_contains(scripts, "(le, \":destination\", 0)")
    assert_contains(scripts, "(party_set_slot, \":courier_party\", slot_party_sod_tax_courier_destination_party, -1)")
    assert_contains(scripts, "has no valid destination")
    assert_contains(scripts, "reroutes to {s3}")
    assert_contains(scripts, "for {s2} has no valid destination")
    assert_contains(scripts, "slot_center_sod_tax_courier_losses")
    assert_contains(scripts, "(party_set_slot, \":origin_center\", slot_center_sod_active_tax_courier, 0)")
    assert_contains(scripts, "(party_set_slot, \":courier_party\", slot_party_sod_tax_courier_amount, 0)")
    assert_contains(scripts, "(party_set_slot, \":courier_party\", slot_party_sod_tax_courier_status, sod_tax_courier_status_expired)")
    assert_contains(scripts, "(party_set_slot, \":courier_party\", slot_party_sod_tax_courier_status, sod_tax_courier_status_lost)")
    assert_contains(scripts, "script_sod_tax_courier_cleanup_party")
    assert_contains(scripts, "(party_set_slot, \":courier_party\", slot_party_sod_messenger_role, sod_messenger_role_none)")
    assert_contains(scripts, "(party_set_slot, \":courier_party\", slot_party_sod_tax_courier_destination_party, -1)")
    assert_contains(scripts, "(remove_party, \":courier_party\")")


def test_interception_dialog_and_battle_hooks_are_wired() -> None:
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_messenger_party_start.py")
    player_victory = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    simulate_battle = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")

    assert_contains(dialog_order, "ZA01_startup_and_dispatch/party_tpl_pt_messenger_party_start.py")
    assert_contains(dialog, "party_tpl|pt_messenger_party")
    assert_contains(dialog, "sod_messenger_role_tax_courier")
    assert_contains(dialog, "tax_courier_player_talk")
    assert_contains(dialog, 'slot_party_sod_tax_courier_recipient_troop, "trp_player"')
    assert_contains(dialog, "tax_courier_nonhostile_talk")
    assert_contains(dialog, "script_sod_tax_courier_apply_nonhostile_coercion_consequence")
    assert_contains(dialog, "skl_persuasion")
    assert_contains(dialog, "script_sod_tax_courier_surrender_to_player")
    assert_contains(player_victory, "script_sod_tax_courier_award_payload_to_player")
    assert_contains(simulate_battle, "script_sod_tax_courier_resolve_defeated_by_party")


def test_nonhostile_courier_coercion_has_reputation_consequences() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    assert_contains(scripts, '("sod_tax_courier_apply_nonhostile_coercion_consequence"')
    assert_contains(scripts, "(ge, \":relation\", 0)")
    assert_contains(scripts, '"script_change_player_relation_with_faction", ":courier_faction", -5')
    assert_contains(scripts, '"script_change_player_honor", -2')
    assert_contains(scripts, "sod_diplomacy_memory_caravan_attack")
    assert_contains(scripts, "Relations with {s68} suffer")
    assert_not_contains(scripts, "Relations with {s3} suffer")


def test_tax_courier_social_dialogue_is_wired() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_tax_couriers.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    dialog_order = read("src/dialogs/_order_dialogs.txt")
    courier_dialog = read("src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_messenger_party_start.py")
    lord = read("src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_tax_courier_rumor.py")
    tavern = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_tax_courier_rumor.py")
    merchant = read("src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_tax_courier_rumor.py")
    companion = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_member_chat_tax_courier_jeremus.py")

    assert_contains(scripts, '("sod_tax_courier_record_social_event"')
    assert_contains(scripts, '("sod_store_tax_courier_rumor_to_s12"')
    assert_contains(scripts, "(assign, \"$g_sod_tax_courier_last_social_event\", \":event_type\")")
    assert_contains(scripts, "(val_add, \"$g_sod_tax_courier_nonhostile_coercions\", 1)")
    assert_contains(scripts, "The room lowers its voice around strongboxes now")
    assert_contains(scripts, "A realm does not run on frightened clerks")
    assert_contains(scripts, "Taxes move like blood")
    assert_contains(game_start, "(assign, \"$g_sod_tax_courier_last_social_event\", 0)")
    assert_contains(game_start, "(assign, \"$g_sod_tax_courier_companion_rumor_seen_day\", -100)")
    assert_contains(courier_dialog, "Couriers trade stories")
    assert_contains(courier_dialog, "script_sod_tax_courier_record_social_event")
    assert_contains(lord, "script_sod_store_tax_courier_rumor_to_s12\", 2")
    assert_contains(tavern, "script_sod_store_tax_courier_rumor_to_s12\", 1")
    assert_contains(merchant, "script_sod_store_tax_courier_rumor_to_s12\", 3")
    assert_contains(companion, "trp_npc12")
    assert_contains(companion, "script_sod_companion_shift_approval")
    assert_contains(companion, "teaching harmless men to fear our shadow")
    assert_before(
        dialog_order,
        "ZA01_startup_and_dispatch/anyone_lord_start_tax_courier_rumor.py",
        "ZA01_startup_and_dispatch/anyone_lord_start_30.py",
    )
    assert_before(
        dialog_order,
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_tax_courier_rumor.py",
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_pretalk.py",
    )
    assert_before(
        dialog_order,
        "ZC01_centers_and_economy/anyone_goods_merchant_tax_courier_rumor.py",
        "ZC01_centers_and_economy/anyone_goods_merchant_pretalk.py",
    )
    assert_before(
        dialog_order,
        "ZE01_companions_and_named_npcs/anyone_member_chat_tax_courier_jeremus.py",
        "ZA01_startup_and_dispatch/anyone_member_chat_06.py",
    )


def test_daily_processing_trigger_is_wired() -> None:
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    daily = read("src/triggers/ST03_daily/entry_0167.py")
    assert_contains(trigger_order, "ST03_daily/entry_0167.py")
    assert_contains(daily, '"script_sod_process_tax_courier_parties"')


def test_generated_compile_contains_tax_courier_system() -> None:
    scripts = read("compile/module_scripts.py")
    triggers = read("compile/module_simple_triggers.py")
    dialogs = read("compile/module_dialogs.py")
    constants = read("compile/module_constants.py")
    for token in (
        "sod_try_dispatch_player_tax_courier_from_center",
        "sod_try_dispatch_ai_tax_courier_from_center",
        "sod_process_tax_courier_parties",
        "sod_tax_courier_resolve_defeated_by_party",
        "sod_tax_courier_apply_nonhostile_coercion_consequence",
        "sod_tax_courier_surrender_to_player",
    ):
        assert_contains(scripts, token)
    assert_contains(triggers, '"script_sod_try_dispatch_player_tax_courier_from_center"')
    assert_contains(triggers, '"script_sod_try_dispatch_ai_tax_courier_from_center"')
    assert_contains(triggers, '"script_sod_process_tax_courier_parties"')
    assert_contains(dialogs, "tax_courier_hostile_talk")
    assert_contains(dialogs, "tax_courier_player_talk")
    assert_contains(dialogs, "tax_courier_nonhostile_talk")
    assert_contains(constants, "slot_center_sod_active_tax_courier")


if __name__ == "__main__":
    test_tax_courier_constants_and_slots_exist()
    test_ai_dispatch_replaces_weekly_invisible_transfer()
    test_tax_courier_scripts_are_wired()
    test_dispatch_accounting_and_safety_are_conservative()
    test_player_courier_collection_and_toggle_are_wired()
    test_non_native_factions_use_dedicated_messenger_troops()
    test_processing_handles_delivery_expiry_and_loss_cleanup()
    test_interception_dialog_and_battle_hooks_are_wired()
    test_nonhostile_courier_coercion_has_reputation_consequences()
    test_tax_courier_social_dialogue_is_wired()
    test_daily_processing_trigger_is_wired()
    test_generated_compile_contains_tax_courier_system()
    print("test_tax_courier_static: OK")
