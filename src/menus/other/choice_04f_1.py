MENUS = [
( "event_04f", mnf_disable_all_keys,
    "A rich merchant from {s1} come to you and offer {reg1} denars to free his daughter. You discover that some of your soldiers had kidnapped her and asked for ransom.",
    "none",
    [  	    (call_script, "script_get_closest_town", "p_main_party"),
	        (str_store_party_name, s1, reg0),
			(store_random_in_range, reg1, 2, 6),
			(val_mul, reg1, 100),
    ],
    [
      ("choice_04f_1", [], "Whip the guilties and free her.",
       [
        (call_script, "script_change_player_honor", 4),
		(assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", -5),
        (call_script, "script_change_player_relation_with_center", reg0, 5),
		(change_screen_return),
        ]
       ),

	  ("choice_04f_2", [], "Let her go for free.",
       [
        (call_script, "script_change_player_honor", 2),
	    (call_script, "script_change_player_relation_with_center", reg0, 2),
		(change_screen_return),
        ]
       ),

	  ("choice_04f_3", [], "Take the ransom for you, free her and punish your men.",
       [(troop_add_gold, "trp_player", reg1),
	    (call_script, "script_change_player_honor", -4),
	    (call_script, "script_change_player_party_morale", -10),
	    (call_script, "script_change_player_relation_with_center", reg0, -5),
		(assign, "$g_whiped_for_example", 1),
        (change_screen_return),
        ]
       ),

	  ("choice_04f_3", [], "Just take the ransom and free her.",
       [(troop_add_gold, "trp_player", reg1),
	    (call_script, "script_change_player_honor", -5),
	    (call_script, "script_change_player_relation_with_center", reg0, -5),
        (change_screen_return),
        ]
       ),

	  ("choice_04f_4", [], "Let your men have the ransom.",
       [(call_script, "script_change_player_honor", -4),
	   	(call_script, "script_change_player_party_morale", 10),
	    (call_script, "script_change_player_relation_with_center", reg0, -5),
        (change_screen_return),
        ]
       ),

        ]
       ),
]
