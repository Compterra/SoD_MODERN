from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def test_capture_enemy_hero_turnin_rechecks_prisoner_before_reward() -> None:
    player_line = read(
        "src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_active_mission_2_02.py"
    )
    reward_line = read("src/dialogs/ZZ99_misc_dialogs/anyone_capture_enemy_hero_thank.py")

    active = '(check_quest_active, "qst_capture_enemy_hero")'
    count = '(party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop")'
    enough = '(ge, ":count_prisoners", 1)'
    remove = '(party_remove_prisoners, "p_main_party", ":quest_target_troop", 1)'
    reg5_reward = '(quest_get_slot, reg5, "qst_capture_enemy_hero", slot_quest_gold_reward)'
    reward = '(call_script, "script_troop_add_gold", "trp_player", ":reward")'
    end = '(call_script, "script_end_quest", "qst_capture_enemy_hero")'
    stale_message = "captured lord handoff could not be completed"

    assert active in player_line
    for token in (active, count, enough, remove, reg5_reward, reward, end, stale_message):
        assert token in reward_line
    assert reward_line.index(reg5_reward) < reward_line.index("Take these {reg5} denars")
    assert reward_line.index(active) < reward_line.index(count) < reward_line.index(enough)
    assert reward_line.index(enough) < reward_line.index(remove) < reward_line.index(reward)
    assert reward_line.index(reward) < reward_line.index(end)


def test_village_grain_turnin_rechecks_inventory_before_reward() -> None:
    player_line = read(
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_village_elder_active_mission_2.py"
    )
    reward_line = read(
        "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_deliver_grain_thank.py"
    )

    active = '(check_quest_active, "qst_deliver_grain")'
    count = '(call_script, "script_get_troop_item_amount", "trp_player", "itm_grain")'
    enough = '(ge, reg0, ":quest_target_amount")'
    remove = '(troop_remove_items, "trp_player", "itm_grain", ":quest_target_amount")'
    prosperity = '(call_script, "script_change_center_prosperity", "$current_town", 4)'
    relation = '(call_script, "script_change_player_relation_with_center", "$current_town", 5)'
    end = '(call_script, "script_end_quest", "qst_deliver_grain")'
    stale_message = "village grain delivery could not be completed"

    assert active in player_line
    for token in (active, count, enough, remove, prosperity, relation, end, stale_message):
        assert token in reward_line
    assert reward_line.index(count) < reward_line.index(active) < reward_line.index(enough)
    assert reward_line.index(enough) < reward_line.index(remove) < reward_line.index(prosperity)
    assert reward_line.index(prosperity) < reward_line.index(relation) < reward_line.index(end)


def test_tavernkeeper_wine_turnins_prepare_display_reward_before_text() -> None:
    full = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_deliver_wine.py")
    partial = read(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_deliver_wine_incomplete.py"
    )
    smuggle = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_smuggle_wine.py")
    smuggle_partial = read(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_smuggle_wine_incomplete.py"
    )

    full_reg = '(quest_get_slot, reg5, "qst_deliver_wine", slot_quest_gold_reward)'
    smuggle_reg = '(quest_get_slot, reg5, "qst_slavers_deliver_wine", slot_quest_gold_reward)'
    partial_reg = '(assign, reg5, ":quest_gold_reward")'

    assert full_reg in full
    assert full.index(full_reg) < full.index("take these {reg5} denars")
    assert partial_reg in partial
    assert partial.index(partial_reg) < partial.index("no more than {reg5} denars")
    assert smuggle_reg in smuggle
    assert smuggle.index(smuggle_reg) < smuggle.index("take these {reg5} denars")
    assert partial_reg in smuggle_partial
    assert smuggle_partial.index(partial_reg) < smuggle_partial.index("no more than {reg5} denars")


def test_tavernkeeper_wine_turnins_recheck_cargo_before_reward() -> None:
    checks = {
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_deliver_wine.py": (
            "qst_deliver_wine",
            '(store_item_kind_count, ":item_count", ":quest_target_item")',
            '(ge, ":item_count", ":quest_target_amount")',
            '(troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount")',
            "wine delivery could not be completed",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_deliver_wine_incomplete.py": (
            "qst_deliver_wine",
            '(store_item_kind_count, ":item_count", ":quest_target_item")',
            '(lt, ":item_count", ":quest_target_amount")',
            '(troop_remove_items, "trp_player", ":quest_target_item", ":item_count")',
            "partial wine delivery could not be completed",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_smuggle_wine.py": (
            "qst_slavers_deliver_wine",
            '(store_item_kind_count, ":item_count", "itm_wine")',
            '(ge, ":item_count", ":quest_target_amount")',
            '(troop_remove_items, "trp_player", "itm_wine", ":quest_target_amount")',
            "smuggled wine delivery could not be completed",
        ),
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_smuggle_wine_incomplete.py": (
            "qst_slavers_deliver_wine",
            '(store_item_kind_count, ":item_count", "itm_wine")',
            '(lt, ":item_count", ":quest_target_amount")',
            '(troop_remove_items, "trp_player", "itm_wine", ":item_count")',
            "partial smuggled wine delivery could not be completed",
        ),
    }
    for rel, (quest, count, enough, remove, stale_message) in checks.items():
        raw = read(rel)
        active = f'(check_quest_active, "{quest}")'
        end = f'(call_script, "script_end_quest", "{quest}")'
        assert active in raw
        for token in (count, enough, remove, end, stale_message):
            assert token in raw
        assert raw.index(count) < raw.index(remove) < raw.index(end)


def test_smuggled_wine_partial_delivery_uses_slavers_debt_global() -> None:
    raw = read(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_smuggle_wine_incomplete.py"
    )
    debt = '(assign, ":debt", "$qst_slavers_deliver_wine_debt")'
    wrong_debt = '(assign, ":debt", "$qst_deliver_wine_debt")'
    assert debt in raw
    assert wrong_debt not in raw
    assert raw.index(debt) < raw.index('(faction_get_slot, ":plyr_debt", "fac_sod_merc_guild6", player_debt_to_faction)')


def test_lost_wine_reports_prepare_display_and_recheck_cargo() -> None:
    merchant = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_deliver_wine_lost.py")
    smuggled = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_smuggle_wine_lost.py")
    smuggled_player = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_quest_smuggle_wine_03.py")

    merchant_active = '(check_quest_active, "qst_deliver_wine")'
    merchant_count = '(store_item_kind_count, ":item_count", ":quest_target_item")'
    merchant_empty = '(eq, ":item_count", 0)'
    merchant_item = '(str_store_item_name, s4, ":quest_target_item")'
    merchant_giver = '(call_script, "script_store_troop_name", s1, ":quest_giver_troop")'
    merchant_debt = '(val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt")'
    merchant_end = '(call_script, "script_end_quest", "qst_deliver_wine")'

    for token in (
        merchant_active,
        merchant_count,
        merchant_empty,
        merchant_item,
        merchant_giver,
        merchant_debt,
        merchant_end,
        "lost wine report could not be completed",
    ):
        assert token in merchant
    assert merchant.index(merchant_item) < merchant.index("waiting for that {s4}")
    assert merchant.index(merchant_giver) < merchant.index("let {s1} know")
    assert merchant.index(merchant_count) < merchant.index(merchant_debt) < merchant.index(merchant_end)

    smuggled_active = '(check_quest_active, "qst_slavers_deliver_wine")'
    smuggled_count = '(store_item_kind_count, ":item_count", "itm_wine")'
    smuggled_empty = '(eq, ":item_count", 0)'
    smuggled_debt = '(val_add, ":plyr_debt", "$qst_slavers_deliver_wine_debt")'
    smuggled_fail = '(call_script, "script_fail_quest", "qst_slavers_deliver_wine")'
    smuggled_end = '(call_script, "script_end_quest", "qst_slavers_deliver_wine")'

    assert smuggled_active in smuggled_player
    for token in (
        smuggled_active,
        smuggled_count,
        smuggled_empty,
        smuggled_debt,
        smuggled_fail,
        smuggled_end,
        "lost smuggled wine report could not be completed",
    ):
        assert token in smuggled
    assert smuggled.index(smuggled_count) < smuggled.index(smuggled_debt)
    assert smuggled.index(smuggled_debt) < smuggled.index(smuggled_fail) < smuggled.index(smuggled_end)
