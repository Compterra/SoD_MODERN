MENUS = [
(
    "event_10", mnf_disable_all_keys,
    "My Liege. You sow fear in hearts of your subjects. People are leaving {s1} to live under better ruler.",
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
      ("choice_10_1", [], "I'm not that bad. Organize festival. Lose 500 denars.",
      [
        (str_store_party_name_link, s1, "$temp"),
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
          (ge, ":gold", 500),
          (troop_remove_gold, "trp_player", 500),
          (display_message, "@You managed to stop people from leaving {s1}.", quest_success_color),
        (else_try),
          (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
          (call_script, "script_change_troop_renown", "trp_player", -2),
          (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
          (assign, ":temp_center_population", ":center_population"),
          (val_div, ":temp_center_population", 10),
          (val_sub, ":center_population", ":temp_center_population"),
          (display_message, "@Many people have left {s1}.", quest_fail_color),
          (party_set_slot, "$temp", slot_center_sod_local_population, ":center_population"),
        (try_end),
        (change_screen_return),
        ]
      ),
      ("choice_10_2", [], "As if I care...",
      [
        (str_store_party_name_link, s1, "$temp"),
        (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
        (assign, ":temp_center_population", ":center_population"),
        (val_div, ":temp_center_population", 10),
        (val_sub, ":center_population", ":temp_center_population"),
        (display_message, "@Many people have left {s1}.", quest_fail_color),
        (party_set_slot, "$temp", slot_center_sod_local_population, ":center_population"),
        (change_screen_return),
      ]
      ),
      ("choice_10_3", [], "They don't yet know how bad I can be. Give them a lesson.",
      [
        (call_script, "script_change_player_relation_with_center", "$temp", -10),
        (call_script, "script_change_player_honor", -5),
        (display_message, "@You managed to stop people from leaving {s1}.", quest_success_color),
        (change_screen_return),
      ]
      ),
    ]
  ),
]
