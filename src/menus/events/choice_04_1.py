MENUS = [
(
    "event_04", mnf_disable_all_keys,
    "Your men have caught a country woman stealing food from your baggage. She begs you to spare her and send something back for her brothers.\
<< The harvest failed, my lord. My family will starve without help. >> Most of your men show little pity.",
    "none",
    [
      (call_script, "script_get_closest_village", "p_main_party"),
      (assign, "$sod_event_relation_center", reg0),
      (try_begin),
        (neg|is_between, "$sod_event_relation_center", centers_begin, centers_end),
        (assign, "$sod_event_relation_center", "p_village_1"),
      (try_end),
    ],
    [
      ("choice_04_1", [], "Let her go, and give her 100 denars for her family.",
       [
       (store_troop_gold, ":gold", "trp_player"),
       (try_begin),
        (ge, ":gold", 100),
        (call_script, "script_change_player_honor", 3),
        (call_script, "script_sod_player_charge_gold", 100),
	    (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", 5),
        (else_try),
        (display_message, "@You don't have enough gold to help her family.", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
	    (call_script, "script_change_player_party_morale", -5),
         (change_screen_return),
        ]
       ),
      ("choice_04_2", [], "You can go, but I won't give anything to a thief.",
       [
	    (call_script, "script_change_player_party_morale", -5),
	    (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -1),
        (change_screen_return),
        ]
       ),
	  ("choice_04_3", [], "The law allows no exception. Execute her.",
       [
	    (call_script, "script_change_player_honor", -2),
		(call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -10),
        (change_screen_return),
        ]
       ),
      ("choice_04_4", [(eq, "$g_sod_parental_advisory", 0)], "Hand her over to the camp followers.",
       [
       (call_script, "script_change_player_honor", -3),
       (call_script, "script_change_player_party_morale", 10),
	   (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -5),
       (change_screen_return),
        ]
       ),

	   ("choice_04_5", [(eq, "$character_gender", tf_male), (eq, "$g_sod_parental_advisory", 0)], "Offer her 50 denars for private company.",
       [
       (call_script, "script_change_player_honor", -1),
	   (store_troop_gold, ":gold", "trp_player"),
	    (try_begin),
        (ge, ":gold", 50),
        (call_script, "script_sod_player_charge_gold", 50),
        (else_try),
        (display_message, "@You don't have enough gold to pay her.", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
