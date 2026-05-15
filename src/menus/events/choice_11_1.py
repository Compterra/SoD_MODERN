MENUS = [
(
    "event_11", mnf_disable_all_keys,
    "Good news, my lord. Your realm has seen an unusually rich harvest. The fields stand heavy with grain, the herds are fat, and everyone now claims credit: the workers who brought it in, the nobles who managed the land, the priests who call it a blessing, and courtiers who say it proves your wisdom. Who should benefit most?",
    "none",
    [

    ],
    [
      ("choice_11_1", [], "Reward hard work.",
       [
        (assign, ":affected_count", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (val_add, ":affected_count", 1),
            (try_begin),
                (party_slot_eq, ":center_no", slot_party_type, spt_village),
                (store_random_in_range, ":rand", 1, 30),
                (call_script, "script_sod_center_apply_population_delta", ":center_no", ":rand"),
            (else_try),
                (store_random_in_range, ":rand", 10, 80),
                (call_script, "script_sod_center_apply_population_delta", ":center_no", ":rand"),
            (try_end),
        (try_end),
        (try_begin),
          (gt, ":affected_count", 0),
          (display_message, "@Your fiefs benefit from the harvest.", quest_success_color),
        (else_try),
          (display_message, "@No affected fief could be found. The report is dismissed.", quest_fail_color),
        (try_end),
        (change_screen_return),
      ]
      ),
      ("choice_11_2", [], "Share the profits among the lords.",
      [
        (call_script, "script_change_player_honor", 10),
        (call_script, "script_change_troop_renown", "trp_player", 30),
        (change_screen_return),
      ]
      ),
      ("choice_11_3", [], "Call it God's blessing and donate to the Church.",
      [
        (val_add, "$g_sod_global_faith", 200),
        (val_clamp, "$g_sod_global_faith", -2000, 2001),
        (display_message, "@Faith in your realm grows stronger.", faith_color),
        (change_screen_return),
      ]
      ),
      ("choice_11_4", [], "Sell the surplus and levy a special grain tax.",
      [
        (troop_add_gold, "trp_player", 2000),
        (call_script, "script_change_player_honor", -5),
        (change_screen_return),
      ]
    ),
  ]
  ),
]
