MENUS = [
(
    "event_08", mnf_disable_all_keys,
    "You spot a single man riding hard towards your party. With a gesture of your hand, your men run to meet him. Intercepted by your men he presents himself as an emissary from {s1} and without delay informs you that an influential man has died {s2} and that his family requests that you agree to declare an official day of mourning in {s1} in his honor. You...",
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
      (store_random_in_range, ":rand_no", 1, 10),
      (try_begin),
        (ge, ":rand_no", 8),
        (str_store_string , s2, "@of a sudden fever"),
      (else_try),
        (ge, ":rand_no", 5),
        (str_store_string , s2, "@in a hunting accident"),
      (else_try),
        (ge, ":rand_no", 3),
        (str_store_string , s2, "@after being assassinated"),
      (else_try),
        (ge, ":rand_no", 0),
        (str_store_string , s2, "@after a brief illness"),
      (try_end),
    ],
    [
      ("choice_08_1", [(is_between, "$temp", centers_begin, centers_end)], "Declare the day of mourning.",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
          (ge, ":gold", 100),
          (call_script, "script_change_player_relation_with_center", "$temp", 2),
          (call_script, "script_sod_player_charge_gold", 100),
        (else_try),
          (display_message, "@You don't have enough gold to fund the day of mourning.", quest_fail_color),
          (call_script, "script_change_troop_renown", "trp_player", -1),
        (try_end),
        (change_screen_return),
      ]
    ),
    ("choice_08_2", [(is_between, "$temp", centers_begin, centers_end)], "Refuse the request.",
      [
        (call_script, "script_change_player_relation_with_center", "$temp", -2),
        (change_screen_return),
      ]
    ),
    ("choice_08_no_center", [(neg|is_between, "$temp", centers_begin, centers_end)], "Continue.",
      [
        (display_message, "@No affected fief could be found. The report is dismissed.", quest_fail_color),
        (change_screen_return),
      ]
    ),
  ]
  ),
]
