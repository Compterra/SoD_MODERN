MENUS = [
(
    "event_16", mnf_disable_all_keys,
    "Excellent news. Robust health policy in {s1} caused a population boom.",
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
      ("choice_16_1", [], "Excellent!",              #twan454
        [
          (str_store_party_name_link, s1, "$temp"),
          (call_script, "script_change_center_prosperity", "$temp", -5),
          (val_sub, "$g_sod_global_health", 1),
          (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
          (assign, ":temp_center_population", ":center_population"),
          (val_div, ":temp_center_population", 10),
          (call_script, "script_sod_center_apply_population_delta", "$temp", ":temp_center_population"),
          (call_script, "script_sod_center_apply_health_delta", "$temp", 7),
          (display_message, "@Population and health of {s1} increases.", quest_success_color),
          (change_screen_return),
        ]
      ),
      ("choice_16_2", [], "Cut their taxes to strenghten the effect (1000 denars).",
        [
          (str_store_party_name_link, s1, "$temp"),
          (store_troop_gold, ":gold", "trp_player"),
          (try_begin),
            (ge, ":gold", 1000),
            (call_script, "script_sod_player_charge_gold", 1000),
            (call_script, "script_change_player_relation_with_center", "$temp", 5),
            (call_script, "script_change_center_prosperity", "$temp", 5),
            (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
            (assign, ":temp_center_population", ":center_population"),
            (val_div, ":temp_center_population", 5),
            (call_script, "script_sod_center_apply_population_delta", "$temp", ":temp_center_population"),
            (call_script, "script_sod_center_apply_health_delta", "$temp", 10),
            (display_message, "@Population, prosperity, Your popularity and health of {s1} greatly increases.", quest_success_color),
          (else_try),
            (display_message, "@You don't have enough gold. How embarrassing! Still, population and health of {s1} rise.", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -2),
            (party_get_slot, ":center_population", "$temp", slot_center_sod_local_population),
            (assign, ":temp_center_population", ":center_population"),
            (val_div, ":temp_center_population", 10),
            (call_script, "script_sod_center_apply_population_delta", "$temp", ":temp_center_population"),
            (call_script, "script_sod_center_apply_health_delta", "$temp", 7),
          (try_end),
          (change_screen_return),  #twan454
        ]
      ),
    ]
  ),
]
