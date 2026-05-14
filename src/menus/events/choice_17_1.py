MENUS = [
(
    "event_17", mnf_disable_all_keys,
    "Excellent global health policy causes population boom in whole kingdom.",
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
      ("choice_17_1", [], "Excellent!",
       [
        (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (val_add, "$g_sod_global_health", 1),
            (try_begin),
                (party_slot_eq, ":center_no", slot_party_type, spt_village),
                (store_random_in_range, ":rand", 20, 50),
                (call_script, "script_sod_center_apply_population_delta", ":center_no", ":rand"),
                (call_script, "script_sod_center_apply_health_delta", ":center_no", 10),
            (else_try),
                (store_random_in_range, ":rand", 50, 150),
                (call_script, "script_sod_center_apply_population_delta", ":center_no", ":rand"),
                (call_script, "script_sod_center_apply_health_delta", ":center_no", 10),
            (try_end),
        (try_end),
        (display_message, "@All Your fiefs experience population boom.", quest_success_color),
        (change_screen_return),
        ]
       ),
      ]
  ),
]
