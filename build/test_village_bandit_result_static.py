from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    for rel in [
        "src/menus/other/continue_23.py",
        "src/menus/other/continue_24.py",
        "src/menus/other/continue_25.py",
    ]:
        raw = read(rel)
        assert '("continue", [(neq, "$g_battle_result", 1)], "Continue..."' in raw, (
            f"{rel} should hide failure continue after a successful village-bandit battle"
        )
        option_start = raw.index('("continue"')
        condition_block = raw[:option_start]
        assert '(eq, "$g_battle_result", 1)' in condition_block
        assert '(jump_to_menu,' in condition_block, (
            f"{rel} hides Continue on victory, so the success branch must route elsewhere"
        )
        assert '(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted)' in raw
        assert raw.index('(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted)') < raw.index('(call_script, "script_village_set_state", "$current_town", svs_looted)')

    infestation = read("src/menus/centers/village/village_bandits_defeated_accept_03.py")
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", 5)' in infestation
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", 3)' in infestation
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", 4)' in infestation
    assert '(call_script, "script_change_player_relation_with_center", "$g_encountered_party"' not in infestation
    assert '(quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$current_town")' in infestation
    assert '(quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$current_town")' in infestation

    for rel in [
        "src/menus/centers/village/village_bandits_defeated_accept.py",
        "src/menus/centers/village/village_bandits_defeated_accept_02.py",
        "src/menus/centers/village/village_bandits_defeated_accept_04.py",
    ]:
        raw = read(rel)
        assert '(call_script, "script_change_player_relation_with_center", "$g_encountered_party"' not in raw, (
            f"{rel} should use $current_town for village relation changes"
        )

    black_army = read("src/menus/centers/village/village_bandits_defeated_accept.py")
    assert '(gt, ":bandit_troop", 0)' in black_army
    assert black_army.index('(gt, ":bandit_troop", 0)') < black_army.index('(assign, "$g_sod_village_bandit_loot_troop", ":bandit_troop")')
    assert '(check_quest_active, "qst_black_army_aid_warband")' in black_army
    assert black_army.index('(check_quest_active, "qst_black_army_aid_warband")') < black_army.index('(call_script, "script_succeed_quest", "qst_black_army_aid_warband")')
    assert '(assign, "$g_sod_village_bandit_loot_troop", ":bandit_troop")' in black_army
    assert black_army.index('(assign, "$g_sod_village_bandit_loot_troop", ":bandit_troop")') < black_army.index('(party_set_slot, "$current_town", slot_village_infested_by_bandits, 0)')
    continue_option = black_army[black_army.index('("village_bandits_defeated_accept"'):]
    assert '(party_get_slot, ":bandit_troop", "$g_encountered_party", slot_village_infested_by_bandits)' not in continue_option
    assert '(change_screen_loot, "$g_sod_village_bandit_loot_troop")' in continue_option

    good_guys = read("src/menus/other/continue_27.py")
    option_start = good_guys.index('("continue"')
    condition_block = good_guys[:option_start]
    continue_option = good_guys[option_start:]
    assert "raped" not in good_guys
    assert '("continue", [(eq, "$g_battle_result", 1)], "Continue..."' in good_guys
    assert '(call_script, "script_succeed_quest", "qst_slavers_deal_with_good_guys")' not in condition_block
    assert '(script_sod_center_apply_population_delta' not in condition_block
    assert '(quest_slot_eq, "qst_slavers_deal_with_good_guys", slot_quest_target_center, "$current_town")' in continue_option
    assert '(quest_slot_eq, "qst_slavers_deal_with_good_guys", slot_quest_target_center, "$g_encountered_party")' not in good_guys
    assert continue_option.index('(call_script, "script_succeed_quest", "qst_slavers_deal_with_good_guys")') < continue_option.index('(jump_to_menu, "mnu_village")')
    assert continue_option.index('(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted)') < continue_option.index('(call_script, "script_sod_center_apply_population_delta", "$current_town", ":population_delta")')
    assert '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_abuse_village, 3)' in continue_option
    assert '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_dirty_profit, 2)' in continue_option

    jotnar_result = read("src/menus/other/continue_26.py")
    assert '(check_quest_active, "qst_jotnar_clan_aid_warband")' in jotnar_result
    assert jotnar_result.index('(check_quest_active, "qst_jotnar_clan_aid_warband")') < jotnar_result.index('(call_script, "script_succeed_quest", "qst_jotnar_clan_aid_warband")')

    village = read("src/menus/centers/village/recruit_volunteers.py")
    slaver_attack = village[village.index('("village_attack_farmers"'):]
    slaver_attack = slaver_attack[:slaver_attack.index('("village_wait"')]
    assert "Attack the armed villagers" in slaver_attack
    assert "self-proclaimed heroes" not in slaver_attack
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", -10)' in slaver_attack
    assert '(call_script, "script_change_player_relation_with_center", "$g_encountered_party", -10)' not in slaver_attack

    train_result = read("src/menus/other/continue_42.py")
    assert "tails between their legs" not in train_result
    assert "The bandits break. Those still standing flee the lanes" in train_result
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", -3)' in train_result
    assert '(call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3)' not in train_result

    train_success = read("src/menus/centers/village/village_bandits_defeated_accept_04.py")
    assert "tails between their legs" not in train_success
    assert "The bandits break. Those still standing flee the lanes" in train_success
    assert '(check_quest_active, "qst_train_peasants_against_bandits")' in train_success
    assert train_success.index('(check_quest_active, "qst_train_peasants_against_bandits")') < train_success.index('(call_script, "script_change_player_relation_with_center", "$current_town", 4)')

    for rel in [
        "src/menus/centers/village/village_bandits_defeated_accept_02.py",
        "src/menus/centers/village/village_bandits_defeated_accept_03.py",
    ]:
        raw = read(rel)
        assert '(gt, ":bandit_troop", 0)' in raw
        assert raw.index('(gt, ":bandit_troop", 0)') < raw.index('(party_set_slot, "$current_town", slot_village_infested_by_bandits, 0)')
        assert raw.index('(gt, ":bandit_troop", 0)') < raw.index('(call_script, "script_party_give_xp_and_gold", "p_temp_party")')

    revenge_success = read("src/menus/centers/village/village_bandits_defeated_accept_02.py")
    assert '(check_quest_active, "qst_jotnar_clan_revenge")' in revenge_success
    assert revenge_success.index('(check_quest_active, "qst_jotnar_clan_revenge")') < revenge_success.index('(call_script, "script_succeed_quest", "qst_jotnar_clan_revenge")')

    slaver_brief = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_22.py")
    assert "flourishing profit" not in slaver_brief
    assert "set things wrong" not in slaver_brief
    assert "The people of {s14} used to pay quietly." in slaver_brief
    slaver_accept = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_good_guys_accepted.py")
    assert "Good. Make it clean enough" in slaver_accept
    assert slaver_accept.index('(str_store_party_name_link, s14, ":village")') < slaver_accept.index('(str_store_string, s2, "@{s9} of {s4} has asked you to deal with the rebellious peasants at {s14}.")')
    slaver_decline = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_good_guys_ask_02.py")
    assert "No. Find someone else." in slaver_decline
    slaver_reward = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_20.py")
    assert "The road is ours again. You made that plain." in slaver_reward

    peasants_defeat = read("src/menus/other/defeated_by_peasants.py")
    assert "The peasants hold the village" in peasants_defeat
    assert '(check_quest_active, "qst_slavers_deal_with_good_guys")' in peasants_defeat
    assert '(quest_slot_eq, "qst_slavers_deal_with_good_guys", slot_quest_target_center, "$current_town")' in peasants_defeat
    assert peasants_defeat.index('(quest_slot_eq, "qst_slavers_deal_with_good_guys", slot_quest_target_center, "$current_town")') < peasants_defeat.index('(call_script, "script_fail_quest", "qst_slavers_deal_with_good_guys")')
    assert '(call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_retreat_or_fail, 1)' in peasants_defeat

    print("Village bandit result static checks passed")


if __name__ == "__main__":
    main()

