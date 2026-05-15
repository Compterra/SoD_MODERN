MENUS = [
(
    "event_06", mnf_disable_all_keys,
    "A mob of angry {s1} dwellers are complaining about corrupt tax collectors. They demand justice. The situation is getting worse by the minute. It looks like a riot is about to begin unless you do something.",
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
      ("choice_06_1", [(is_between, "$temp", centers_begin, centers_end)], "Begin an investigation and compensate the peasants for their loss.",
        [
          (store_troop_gold, ":gold", "trp_player"),
          (try_begin),
            (ge, ":gold", 300),
            (call_script, "script_change_player_relation_with_center", "$temp", 2),
            (call_script, "script_sod_player_charge_gold", 300),
            (else_try),
            (display_message, "@You don't have enough gold to compensate the victims.", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -5),
            (call_script, "script_change_player_relation_with_center", "$temp", -5),
          (try_end),
          (change_screen_return),
        ]
      ),
      ("choice_06_2", [(is_between, "$temp", centers_begin, centers_end)], "Send guards to contain the riot before it spreads.",
        [
          (call_script, "script_change_player_relation_with_center", "$temp", -5),
          (change_screen_return),
        ]
      ),
      ("choice_06_3", [(is_between, "$temp", centers_begin, centers_end)], "Break the mob and collect the overdue taxes.",
        [
          (call_script, "script_change_player_honor", -3),
          (call_script, "script_change_player_relation_with_center", "$temp", -10),
		  (store_random_in_range, ":taxes", 100, 400),
          (troop_add_gold, "trp_player", ":taxes"),
          (change_screen_return),
        ]
      ),
      ("choice_06_no_center", [(neg|is_between, "$temp", centers_begin, centers_end)], "Continue.",
        [
          (display_message, "@No affected fief could be found. The report is dismissed.", quest_fail_color),
          (change_screen_return),
        ]
      ),
    ]
  ),
]
