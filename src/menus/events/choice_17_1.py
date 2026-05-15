MENUS = [
(
    "event_17", mnf_disable_all_keys,
    "Excellent global health policy has caused a population boom across your realm.",
    "none",
    [],
    [
      ("choice_17_1", [], "Excellent.",
       [
        (assign, ":affected_count", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (val_add, ":affected_count", 1),
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
        (try_begin),
          (gt, ":affected_count", 0),
          (val_add, "$g_sod_global_health", 1),
          (display_message, "@All your fiefs experience a population boom.", quest_success_color),
        (else_try),
          (display_message, "@No affected fief could be found. The report is dismissed.", quest_fail_color),
        (try_end),
        (change_screen_return),
        ]
       ),
      ]
  ),
]
