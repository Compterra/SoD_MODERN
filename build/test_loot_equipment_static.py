# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    protected = read("src/scripts/ZB_economy_and_trade/sod_auto_loot_item_is_protected.py")
    constants = read("src/constants/module_constants.py")
    set_protected = read("src/scripts/ZB_economy_and_trade/sod_set_auto_loot_item_protection.py")
    usability = read("src/scripts/ZB_economy_and_trade/troop_can_use_item.py")
    score = read("src/scripts/ZB_economy_and_trade/get_item_score_with_imod.py")
    value = read("src/scripts/ZB_economy_and_trade/get_item_cost_with_imod.py")
    evaluation = read("src/scripts/ZB_economy_and_trade/sod_describe_auto_loot_item_evaluation_to_s0.py")
    auto_sell_guard = read("src/scripts/ZB_economy_and_trade/sod_auto_sell_item_is_allowed.py")
    auto_sell = read("src/scripts/ZB_economy_and_trade/sod_auto_sell_companion_inventory_to_merchant.py")
    auto_buy_food = read("src/scripts/ZB_economy_and_trade/sod_auto_buy_food_from_merchant.py")
    repairable = read("src/scripts/ZB_economy_and_trade/sod_item_modifier_is_repairable.py")
    repair_service = read("src/scripts/ZB_economy_and_trade/sod_item_can_be_repaired_by_service.py")
    repair_cost = read("src/scripts/ZB_economy_and_trade/sod_get_item_repair_cost.py")
    repair_party = read("src/scripts/ZB_economy_and_trade/sod_repair_player_party_equipment.py")
    repair_troop = read("src/scripts/ZB_economy_and_trade/sod_repair_troop_equipment.py")
    degrade_item = read("src/scripts/ZB_economy_and_trade/sod_get_degraded_imod_for_item.py")
    degrade_party = read("src/scripts/ZB_economy_and_trade/sod_degrade_player_party_equipment_after_battle.py")
    degrade_troop = read("src/scripts/ZB_economy_and_trade/sod_degrade_troop_equipped_items_after_battle.py")
    transfer_free = read("src/scripts/ZB_economy_and_trade/sod_transfer_inventory_slot_to_free_inventory.py")
    transfer_slot = read("src/scripts/ZB_economy_and_trade/sod_transfer_inventory_slot_to_slot.py")
    recover = read("src/scripts/ZB_economy_and_trade/sod_recover_protected_items_from_loot_pool.py")
    auto_loot_all = read("src/scripts/ZZ_common_array_processing/auto_loot_all.py")
    auto_loot = read("src/scripts/ZH_heroes/auto_loot_troop.py")
    loot_player_items = read("src/scripts/ZB_economy_and_trade/loot_player_items.py")
    scan = read("src/scripts/ZB_economy_and_trade/scan_for_best_item_of_type.py")
    menu = read("src/menus/prisoners/manage_loot_pool.py")
    town_trade = read("src/menus/centers/town/trade_with_arms_merchant.py")
    total_victory = read("src/menus/other/continue_06.py")
    total_defeat = read("src/menus/other/total_defeat.py")
    weapon_dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk.py")
    armor_dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk_02.py")
    horse_dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk_03.py")
    town_merchant_dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_town_merchant_talk_04.py")
    goods_dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_goods_merchant_talk_02.py")
    village_dialog = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_trade_talk_03.py")
    doc = read("docs/reports/references_features/custom_commander_light_feature_audit.md")

    assert_contains(constants, "slot_item_sod_auto_loot_protected")
    assert_contains(constants, "sod_repair_service_weapons")
    assert_contains(constants, "sod_repair_service_armor")
    assert_contains(constants, "sod_repair_service_horses")
    assert_contains(constants, "slot_item_artifact_set_piece         = 168")
    assert_contains(constants, "slot_item_artifact_progress_begin    = 180")
    assert_contains(set_protected, "sod_set_auto_loot_item_protection")
    assert_contains(set_protected, "slot_item_sod_auto_loot_protected")

    for token in (
        "slot_item_artifact_flags",
        "slot_item_sod_auto_loot_protected",
        "books_begin",
        "books_end",
        "trade_goods_begin",
        "trade_goods_end",
    ):
        assert_contains(protected, token)

    for helper in (transfer_free, transfer_slot):
        assert_contains(helper, "script_sod_auto_loot_item_is_protected")
        assert_contains(helper, "troop_get_inventory_slot_modifier")
        assert_contains(helper, "troop_inventory_slot_get_item_amount")
        assert_contains(helper, "troop_inventory_slot_set_item_amount")
        assert_contains(helper, "slot_item_artifact_current_owner")
        assert_contains(helper, "slot_item_artifact_last_modifier")
        assert_contains(helper, "assign, reg0, 1")

    assert_contains(recover, "sod_recover_protected_items_from_loot_pool")
    assert_contains(recover, "script_sod_auto_loot_item_is_protected")
    assert_contains(recover, "script_sod_transfer_inventory_slot_to_free_inventory")
    assert_contains(recover, "your inventory is full")
    assert_contains(menu, "script_sod_recover_protected_items_from_loot_pool")

    assert "troop_add_item" not in auto_loot
    assert_contains(auto_loot, "script_sod_transfer_inventory_slot_to_free_inventory")
    assert_contains(auto_loot, "script_sod_transfer_inventory_slot_to_slot")
    assert_contains(auto_loot, 'item_slot_eq, ":item", slot_item_cant_use_on_horseback, 0')
    assert_contains(auto_loot_all, "script_auto_loot_troop")
    assert_contains(auto_loot_all, "slot_troop_restrict_mounted")
    assert_contains(auto_loot_all, "Companions choose in party order and make two redistribution passes")
    assert_contains(auto_loot_all, "item(s) equipped")
    assert_contains(scan, "script_sod_auto_loot_item_is_protected")

    assert_contains(usability, "(assign, \":skill\", 0)")
    assert_contains(usability, "itp_type_book")
    assert_contains(usability, "ca_intelligence")
    for token in (
        "itp_type_horse",
        "skl_riding",
        "itp_type_bow",
        "skl_power_draw",
        "itp_type_thrown",
        "skl_power_throw",
        "itp_type_shield",
        "skl_shield",
        "ca_strength",
        "slot_item_imod_require",
    ):
        assert_contains(usability, token)

    for token in (
        "horse score",
        "shield score",
        "armor score",
        "weapon score",
        "missiles score",
        "imod_large_bag",
    ):
        assert_contains(score, token)
    assert_contains(value, "slot_item_imod_cost")
    assert_contains(value, "(store_div, reg0, \":cost\", 100)")

    for token in (
        "sod_describe_auto_loot_item_evaluation_to_s68",
        "sod_describe_auto_loot_item_evaluation_to_s0",
        "script_sod_describe_auto_loot_item_evaluation_to_s68",
        "(str_store_string_reg, s0, s68)",
        "protected from automation",
        "cannot be used on horseback",
        "requirements are not met",
        "score {reg21}",
        "modifier-adjusted value {reg22} denars",
    ):
        assert_contains(evaluation, token)
    if "(str_store_string, s0," in evaluation:
        raise AssertionError("auto-loot evaluation should compose feature text in s68 before compatibility copying to s0")

    for token in (
        "sod_auto_sell_item_is_allowed",
        "script_sod_auto_loot_item_is_protected",
        "itp_type_goods",
        "itp_type_book",
        "itp_type_horse",
        "itp_type_animal",
        "script_get_item_cost_with_imod",
        "price_limit",
    ):
        assert_contains(auto_sell_guard, token)

    for token in (
        "sod_auto_sell_companion_inventory_to_merchant",
        "script_sod_auto_sell_item_is_allowed",
        "script_sod_transfer_inventory_slot_to_free_inventory",
        "script_game_get_item_sell_price_factor",
        "store_troop_gold",
        "store_free_inventory_capacity",
        "troop_remove_gold",
        "troop_add_gold",
        "companions_begin",
        "slto_player_companion",
    ):
        assert_contains(auto_sell, token)

    for token in (
        "sod_auto_buy_food_from_merchant",
        "food_begin",
        "food_end",
        "itm_cattle_meat",
        "imod_rotten",
        "script_game_get_item_buy_price_factor",
        "script_sod_transfer_inventory_slot_to_free_inventory",
        "store_free_inventory_capacity",
        "script_sod_player_charge_gold",
        "(eq, reg1, 1)",
        "troop_add_gold",
        "target_variety",
        "max_purchases",
        "started_variety",
        "Food variety is now {reg25}/{reg26}",
        "only buys non-rotten food types you do not already carry",
    ):
        assert_contains(auto_buy_food, token)

    for token in (
        "sod_auto_sell_companion_spares",
        "sod_auto_sell_companion_spares_broad",
        "sod_auto_buy_missing_food",
        "script_sod_auto_sell_companion_inventory_to_merchant",
        "script_sod_auto_buy_food_from_merchant",
    ):
        assert_contains(town_trade, token)

    assert_contains(town_merchant_dialog, "Sell low-value spare gear carried by my companions.")
    assert_contains(town_merchant_dialog, "Sell ordinary spare gear carried by my companions.")
    assert_contains(town_trade, "Buy up to 4 food varieties missing from your stores.")
    assert_contains(goods_dialog, "Buy up to four food types my party is missing.")
    assert_contains(village_dialog, "Buy up to four food types my party is missing.")

    for token in (
        "imod_cracked",
        "imod_rusty",
        "imod_bent",
        "imod_chipped",
        "imod_battered",
        "imod_lame",
        "imod_swaybacked",
    ):
        assert_contains(repairable, token)

    for token in (
        "sod_item_can_be_repaired_by_service",
        "script_sod_auto_loot_item_is_protected",
        "sod_repair_service_weapons",
        "sod_repair_service_armor",
        "sod_repair_service_horses",
        "itp_type_horse",
    ):
        assert_contains(repair_service, token)

    for token in (
        "sod_get_item_repair_cost",
        "script_sod_item_modifier_is_repairable",
        "script_get_item_cost_with_imod",
        "imod_plain",
        "val_max, \":repair_cost\", 10",
    ):
        assert_contains(repair_cost, token)

    for token in (
        "sod_repair_troop_equipment",
        "script_sod_item_can_be_repaired_by_service",
        "script_sod_get_item_repair_cost",
        "ek_item_0",
        "ek_food",
        "script_sod_player_charge_gold",
        "(eq, reg1, 1)",
        "troop_set_inventory_slot_modifier",
        "imod_plain",
        "gt, \":repair_cost\", 0",
    ):
        assert_contains(repair_troop, token)

    for token in (
        "sod_repair_player_party_equipment",
        "script_sod_repair_troop_equipment",
        "companions_begin",
        "Repaired {reg21} damaged equipment item(s)",
    ):
        assert_contains(repair_party, token)

    for token in (
        "sod_get_degraded_imod_for_item",
        "script_sod_auto_loot_item_is_protected",
        "eq, \":imod\", imod_plain",
        "imod_chipped",
        "imod_battered",
        "imod_swaybacked",
    ):
        assert_contains(degrade_item, token)

    for token in (
        "sod_degrade_troop_equipped_items_after_battle",
        "val_clamp, \":chance\", 0, 101",
        "gt, \":chance\", 0",
        "ek_item_0",
        "ek_food",
        "store_random_in_range",
        "troop_set_inventory_slot_modifier",
    ):
        assert_contains(degrade_troop, token)

    for token in (
        "sod_degrade_player_party_equipment_after_battle",
        "script_sod_degrade_troop_equipped_items_after_battle",
        "wear_chance\", 4",
        "Battle wear damaged",
    ):
        assert_contains(degrade_party, token)

    for token in (
        "sod_repair_weapons",
        "sod_repair_armor",
        "sod_repair_horses",
        "script_sod_repair_player_party_equipment",
        "(party_slot_ge, \"$current_town\", slot_center_has_blacksmith, 1)",
        "(party_slot_ge, \"$current_town\", slot_center_has_stables, 1)",
    ):
        assert_contains(town_trade, token)

    assert_contains(total_victory, "script_sod_degrade_player_party_equipment_after_battle")

    for token in (
        '(assign, ":defeat_enemy_valid", 0)',
        '(party_is_active, "$g_enemy_party")',
        '(assign, "$g_enemy_party", -1)',
        '(eq, ":defeat_enemy_valid", 1)',
        '(party_get_num_companion_stacks, ":num_enemy_stacks", "$g_enemy_party")',
        '(distribute_party_among_party_group, "p_temp_party", "$g_enemy_party")',
        '(party_clear, "p_temp_party")',
    ):
        assert_contains(total_defeat, token)
    assert total_defeat.index('(party_is_active, "$g_enemy_party")') < total_defeat.index('(party_stack_get_troop_id, ":captor_troop", "$g_enemy_party", 0)')
    assert total_defeat.index('(eq, ":defeat_enemy_valid", 1)') < total_defeat.index('(distribute_party_among_party_group, "p_temp_party", "$g_enemy_party")')
    assert total_defeat.index('(eq, ":defeat_enemy_valid", 1)') < total_defeat.index('(call_script, "script_loot_player_items", "$g_enemy_party")')

    for token in (
        "(store_script_param, \":enemy_party_no\", 1)",
        "(party_is_active, \":enemy_party_no\")",
        "(gt, \":cur_gold\", 0)",
        "(val_max, \":max_lost\", 1)",
        "(val_min, \":max_lost\", \":cur_gold\")",
        "(val_min, \":min_lost\", \":max_lost\")",
        "(eq, \":min_lost\", \":max_lost\")",
        "(assign, \":lost_gold\", \":max_lost\")",
        "(store_random_in_range, \":lost_gold\", \":min_lost\", \":max_lost\")",
    ):
        assert_contains(loot_player_items, token)
    assert loot_player_items.index("(party_is_active, \":enemy_party_no\")") < loot_player_items.index("(party_get_slot, \":cur_loot_slot\", \":enemy_party_no\", slot_party_next_looted_item_slot)")
    assert_contains(weapon_dialog, "My company's weapons have earned scars. Put an edge back on them.")
    assert_contains(weapon_dialog, "slot_center_has_blacksmith")
    assert_contains(armor_dialog, "My company's armor has taken honest blows. Make it fit for another fight.")
    assert_contains(armor_dialog, "slot_center_has_blacksmith")
    assert_contains(horse_dialog, "My mounts are carrying old pain. See what can be mended.")
    assert_contains(horse_dialog, "slot_center_has_stables")

    for token in (
        "- [x] Audit every `$pool_troop` use",
        "- [x] Add or document loot-pool entry/exit invariants",
        "- [x] Decide final leftover-pool behavior",
        "- [x] Add a dedicated \"recover protected items\"",
        "- [x] Add static tests for auto-loot protection coverage",
        "- [x] Confirm companion auto-loot priority policy",
        "- [x] Keep or tune the two-pass redistribution behavior",
        "- [x] Add a player-facing result summary",
        "- [x] Decide whether alternate weapon-set support belongs in this pass",
        "- [x] Map companion weapon preference categories",
        "- [x] Expose companion upgrade settings",
        "- [x] Add batch controls",
        "- [x] Add shared transfer helpers that preserve item id, modifier, amount, and protected-item state.",
        "- [x] Route new inventory automation through transfer helpers",
        "- [x] Expand \"protected\" beyond the first guardrail",
        "- [x] Audit `script_troop_can_use_item`",
        "- [x] Extend item usability checks to books",
        "- [x] Ensure mounted companions reject items marked unusable on horseback",
        "- [x] Review item scoring formulas",
        "- [x] Add debug/report output explaining why an item was selected or rejected.",
        "- [x] Centralize modifier-aware item value logic",
        "- [x] Audit all modifier-aware value callers",
        "- [x] Decide whether auto-sell targets player inventory",
        "- [x] Implement strong auto-sell defaults",
        "- [x] Add auto-sell controls",
        "- [x] Verify merchant gold and merchant capacity",
        "- [x] Decide whether auto-buy food",
        "- [x] Prevent auto-buy food",
        "- [x] Add regression tests for modifier preservation",
        "slot_item_sod_auto_loot_protected",
        "script_sod_describe_auto_loot_item_evaluation_to_s68",
        "script_sod_describe_auto_loot_item_evaluation_to_s0",
        "compatibility wrapper",
        "script_sod_auto_sell_item_is_allowed",
    ):
        assert_contains(doc, token)

    print("[loot_equipment_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
