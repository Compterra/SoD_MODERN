MENUS = [
(
    "event_07", mnf_disable_all_keys,
    "A poor, unarmed rider approaches your party. Your men stop him, and he presents himself as a troubadour from {s1}. He asks leave to compose an ode to your generosity. Your men exchange glances, then look to you for an answer.",
    "none",
    [
      (assign, "$temp", -1),
      (str_store_string, s68, "@one of your fiefs"),
      (assign, ":stop", 0),
      (try_for_range, ":unused", 0, 9999),
        (eq, ":stop", 0),
        (store_random_party_in_range, "$temp", centers_begin, centers_end),
        (neg|party_slot_eq, "$temp", slot_party_type, spt_castle),
        (party_slot_eq, "$temp", slot_town_lord, "trp_player"),
        (assign, ":stop", 1),
        (str_store_party_name, s68, "$temp"),
      (try_end),
      (str_store_string_reg, s1, s68),
    ],
    [
      ("choice_07_1", [(is_between, "$temp", centers_begin, centers_end)], "Let him compose the ode and give him 300 denars.",
        [
          (store_troop_gold, ":gold", "trp_player"),
          (try_begin),
            (ge, ":gold", 300),
            (store_random_in_range, ":rand_no", 5, 20),
            (call_script, "script_change_troop_renown", "trp_player", ":rand_no"),
            (call_script, "script_change_player_relation_with_center", "$temp", 5),
            (call_script, "script_sod_player_charge_gold", 300),
            (else_try),
            (display_message, "@You don't have enough gold to reward the troubadour.", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -2),
          (try_end),
          (change_screen_return),
        ]
      ),
      ("choice_07_2", [(is_between, "$temp", centers_begin, centers_end)], "Let him compose the ode and give him 100 denars.",
        [
          (store_troop_gold, ":gold", "trp_player"),
          (try_begin),
            (ge, ":gold", 100),
            (call_script, "script_change_player_relation_with_center", "$temp", 2),
            (call_script, "script_sod_player_charge_gold", 100),
            (else_try),
            (display_message, "@You don't have enough gold to reward the troubadour.", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -2),
          (try_end),
          (change_screen_return),
        ]
      ),
      ("choice_07_3", [(is_between, "$temp", centers_begin, centers_end)], "Allow the ode, but offer no payment.",
        [
          (store_random_in_range, ":rand_no", -2, 2),
          (call_script, "script_change_player_relation_with_center", "$temp", ":rand_no"),
          (change_screen_return),
        ]
      ),
      ("choice_07_4", [], "Order your men to take the beggar out of your way.",
        [
          (call_script, "script_change_player_honor", -2),
          (change_screen_return),
        ]
      ),
      ("choice_07_no_center", [(neg|is_between, "$temp", centers_begin, centers_end)], "Continue.",
        [
          (display_message, "@No affected fief could be found. The report is dismissed.", quest_fail_color),
          (change_screen_return),
        ]
      ),
    ]
  ),
]
