MENUS = [
(
    "event_07", mnf_disable_all_keys,
    "A single rider, looking poor and unarmed, approaches your party. Intercepted by your men he presents himself as a troubadour from {s1} and requests your permission to compose an ode about your magnificency and generosity. Your men exchange glances and then look at you waiting for an answer. You...",
    "none",
    [
      (assign, ":stop", 0),
      (try_for_range, ":unused", 0, 9999),
        (eq, ":stop", 0),
        (store_random_party_in_range, "$temp", centers_begin, centers_end),
        (neg|party_slot_eq, "$temp", slot_party_type, spt_castle),
        (party_slot_eq, "$temp", slot_town_lord, "trp_player"),
        (assign, ":stop", 1),
        (str_store_party_name, s1, "$temp"),
      (try_end),
    ],
    [
      ("choice_07_1", [], "Grant such permission to the troubadour and cover the man with gold -300 denars-.",
        [
          (store_troop_gold, ":gold", "trp_player"),
          (try_begin),
            (ge, ":gold", 300),
            (store_random_in_range, ":rand_no", 5, 20),
            (call_script, "script_change_troop_renown", "trp_player", ":rand_no"),
            (call_script, "script_change_player_relation_with_center", "$temp", 5),
            (call_script, "script_sod_player_charge_gold", 300),
            (else_try),
            (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -2),
          (try_end),
          (change_screen_return),
        ]
      ),
      ("choice_07_2", [], "Grant permission and hand a purse with 100 denars to the man.",
        [
          (store_troop_gold, ":gold", "trp_player"),
          (try_begin),
            (ge, ":gold", 100),
            (call_script, "script_change_player_relation_with_center", "$temp", 2),
            (call_script, "script_sod_player_charge_gold", 100),
            (else_try),
            (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -2),
          (try_end),
          (change_screen_return),
        ]
      ),
      ("choice_07_3", [], "Allow the troubadour to compose the ode but offer him no payment.",
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
    ]
  ),
]
