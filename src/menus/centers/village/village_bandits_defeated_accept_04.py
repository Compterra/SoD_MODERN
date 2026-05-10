MENUS = [
(
    "train_peasants_against_bandits_success", mnf_disable_all_keys,
    "The bandits are broken! Those few who remain run off with their tails between their legs, terrified of the peasants and their new champion. The villagers have little left in the way of wealth after their ordeal, but they offer you all they can find to show their gratitude.",
    "none",
    [(party_clear, "p_temp_party"),
     (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
     (call_script, "script_change_player_relation_with_center", "$current_town", 4),

     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_for_range, ":slot_no", num_equipment_kinds , max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 50),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (try_end),
     (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player", "$current_town", -1, -1),
    ],
    [
      ("village_bandits_defeated_accept", [], "Take it as your just due.", [(jump_to_menu, "mnu_auto_return_to_map"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (change_screen_loot, ":merchant_troop"),
                                                                       ]),
      ("village_bandits_defeated_cont", [], "Refuse, stating that they need these items more than you do.", [(call_script, "script_change_player_relation_with_center", "$current_town", 3),
                                                                                                             (call_script, "script_change_player_honor", 1),
                                                                                                                (change_screen_map)]),
    ],
  ),
]
