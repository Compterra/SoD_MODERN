MENUS = [
(
    "event_10", mnf_disable_all_keys,
    "My Liege. Fear of your rule is driving people out of {s1}. They are leaving for safer lands.",
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
      ("choice_10_1", [(is_between, "$temp", centers_begin, centers_end)], "Hold a festival to calm them. Lose 500 denars.",
      [
        (str_store_party_name_link, s1, "$temp"),
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
          (ge, ":gold", 500),
          (call_script, "script_sod_player_charge_gold", 500),
          (display_message, "@You managed to stop people from leaving {s1}.", quest_success_color),
        (else_try),
          (display_message, "@You don't have enough gold to hold the festival.", quest_fail_color),
          (call_script, "script_change_troop_renown", "trp_player", -2),
          (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
          (assign, ":temp_center_population", ":center_population"),
          (val_div, ":temp_center_population", 10),
          (store_mul, ":population_delta", ":temp_center_population", -1),
          (display_message, "@Many people have left {s1}.", quest_fail_color),
          (call_script, "script_sod_center_apply_population_delta", "$temp", ":population_delta"),
        (try_end),
        (change_screen_return),
        ]
      ),
      ("choice_10_2", [(is_between, "$temp", centers_begin, centers_end)], "Let them leave.",
      [
        (str_store_party_name_link, s1, "$temp"),
        (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
        (assign, ":temp_center_population", ":center_population"),
        (val_div, ":temp_center_population", 10),
        (store_mul, ":population_delta", ":temp_center_population", -1),
        (display_message, "@Many people have left {s1}.", quest_fail_color),
        (call_script, "script_sod_center_apply_population_delta", "$temp", ":population_delta"),
        (change_screen_return),
      ]
      ),
      ("choice_10_3", [(is_between, "$temp", centers_begin, centers_end)], "They don't yet know how bad I can be. Give them a lesson.",
      [
        (call_script, "script_change_player_relation_with_center", "$temp", -10),
        (call_script, "script_change_player_honor", -5),
        (display_message, "@You managed to stop people from leaving {s1}.", quest_success_color),
        (change_screen_return),
      ]
      ),
      ("choice_10_no_center", [(neg|is_between, "$temp", centers_begin, centers_end)], "Continue.",
      [
        (display_message, "@No affected fief could be found. The report is dismissed.", quest_fail_color),
        (change_screen_return),
      ]
      ),
    ]
  ),
]
