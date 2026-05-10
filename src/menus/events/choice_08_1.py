MENUS = [
(
    "event_08", mnf_disable_all_keys,
    "You spot a single man riding hard towards your party. With a gesture of your hand, your men run to meet him. Intercepted by your men he presents himself as an emissary from {s1} and without delay informs you that an influential man has died {s2} and that his family requests that you agree to declare an official day of mourning in {s1} in his honor. You...",
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
      (store_random_in_range, ":rand_no", 1, 10),
      (try_begin),
        (ge, ":rand_no", 8),
        (str_store_string , s2, "@of a fulminatng disease"),
      (else_try),
        (ge, ":rand_no", 5),
        (str_store_string , s2, "@in a hunting accident"),
      (else_try),
        (ge, ":rand_no", 3),
        (str_store_string , s2, "@assasinated"),
      (else_try),
        (ge, ":rand_no", 0),
        (str_store_string , s2, "@of an indigestion"),
      (try_end),
    ],
    [
      ("choice_08_1", [], "Agree to such request.",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
          (ge, ":gold", 100),
          (call_script, "script_change_player_relation_with_center", "$temp", 2),
          (call_script, "script_sod_player_charge_gold", 100),
        (else_try),
          (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
          (call_script, "script_change_troop_renown", "trp_player", -1),
        (try_end),
        (change_screen_return),
      ]
    ),
    ("choice_08_2", [], "Refuse to such request.",
      [
        (call_script, "script_change_player_relation_with_center", "$temp", -2),
        (change_screen_return),
      ]
    ),
  ]
  ),
]
