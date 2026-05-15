MENUS = [
(  "event_04h", mnf_disable_all_keys,
    "Some of your scouts have caught and abused a country girl from {s1}.",
    "none",
    [  	    (call_script, "script_get_closest_village", "p_main_party"),
            (assign, "$sod_event_relation_center", reg0),
            (try_begin),
              (neg|is_between, "$sod_event_relation_center", centers_begin, centers_end),
              (assign, "$sod_event_relation_center", "p_village_1"),
            (try_end),
	        (str_store_party_name, s1, "$sod_event_relation_center"),
    ],
    [
      ("choice_04h_1", [], "Punish the guilty men and give her 300 denars.",
       [
        (call_script, "script_change_player_honor", 2),
		(assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", -10),
		(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 300),
        (call_script, "script_change_player_honor", 2),
        (call_script, "script_sod_player_charge_gold", 300),
	    (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", 2),
        (else_try),
        (display_message, "@You don't have enough gold to pay compensation.", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
		(change_screen_return),
        ]
       ),

	  ("choice_04h_2", [], "Punish the guilty men, but pay her nothing.",
       [
        (call_script, "script_change_player_honor", 2),
		(assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", -10),
	    (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -2),
		(change_screen_return),
        ]
       ),

	  ("choice_04h_3", [], "Give her 300 denars but don't punish your men.",
       [(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 300),
        (call_script, "script_change_player_honor", 2),
        (call_script, "script_sod_player_charge_gold", 300),
        (else_try),
        (display_message, "@You don't have enough gold to pay compensation.", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
        (change_screen_return),
        ]
       ),

	  ("choice_04h_4", [], "No money for her, no punishment for your men.",
       [(call_script, "script_change_player_honor", -3),
	    (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -4),
        (change_screen_return),
        ]
       ),

      ("choice_04h_5", [], "Hand her over to the rest of the camp.",
       [(call_script, "script_change_player_honor", -4),
	    (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -8),
	    (call_script, "script_change_player_party_morale", 10),
        (change_screen_return),
        ]
       ),

	   ("choice_04h_6", [], "Silence her and punish the scouts for hiding it from the company.",
       [(call_script, "script_change_player_honor", -10),
	    (assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", 5),
        (change_screen_return),
        ]
       ),

        ]
       ),
]
