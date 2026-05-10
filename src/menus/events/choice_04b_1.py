MENUS = [
(
    "event_04b", mnf_disable_all_keys,
    "Your scouts have catched a fat merchant who was travelling without escort. He presents himself as a citizen of {s1} and ask you to let him go.",
    "none",
    [  (call_script, "script_get_closest_town", "p_main_party"),
       (assign, "$sod_event_relation_center", reg0),
       (try_begin),
         (neg|is_between, "$sod_event_relation_center", centers_begin, centers_end),
         (assign, "$sod_event_relation_center", "p_town_1"),
       (try_end),
	   (str_store_party_name, s1, "$sod_event_relation_center"),

    ],
    [
      ("choice_04b_1", [], "Let him go.",
       [
        (call_script, "script_change_player_honor", 1),
          (change_screen_return),
        ]
       ),
      ("choice_04b_2", [], "Ask him to pay for free passage.",
       [
       (call_script, "script_change_player_honor", -1),
	   (troop_add_gold, "trp_player", 100),
        (change_screen_return),
        ]
       ),
	  ("choice_04b_2", [], "Steal his money and abandon him.",
       [
       (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -10),
       (store_random_in_range, ":rnd", 500, 1000),
       (troop_add_gold, "trp_player", ":rnd"),
	   (call_script, "script_change_player_honor", -3),
        (change_screen_return),
        ]
       ),
      ("choice_04b_3", [], "Take his money and execute him.",
       [
       (call_script, "script_change_player_honor", -5),
       (store_random_in_range, ":rnd", 500, 1000),
       (troop_add_gold, "trp_player", ":rnd"),
	   (call_script, "script_change_player_honor", -6),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
