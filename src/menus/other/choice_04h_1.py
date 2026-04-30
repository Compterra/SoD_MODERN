MENUS = [
(  "event_04h", mnf_disable_all_keys,
    "Some of your scouts have catched a country girl from {s1} and abused her.",
    "none",
    [  	    (call_script, "script_get_closest_village", "p_main_party"),
	        (str_store_party_name, s1, reg0),
    ],
    [
      ("choice_04h_1", [], "Whip the guilties and give her 300 denars to forget.",
       [
        (call_script, "script_change_player_honor", 2),
		(assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", -10),
		(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 300),
        (call_script, "script_change_player_honor", 2),
        (troop_remove_gold, "trp_player", 300),
	    (call_script, "script_change_player_relation_with_center", reg0, 2),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
		(change_screen_return),
        ]
       ),

	  ("choice_04h_2", [], "Whip the guilties but don't give her money.",
       [
        (call_script, "script_change_player_honor", 2),
		(assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", -10),
	    (call_script, "script_change_player_relation_with_center", reg0, -2),
		(change_screen_return),
        ]
       ),

	  ("choice_04h_3", [], "Give her 300 denars but don't punish your men.",
       [(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 300),
        (call_script, "script_change_player_honor", 2),
        (troop_remove_gold, "trp_player", 300),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
        (change_screen_return),
        ]
       ),

	  ("choice_04h_4", [], "No money for her, no whip for your men.",
       [(call_script, "script_change_player_honor", -3),
	    (call_script, "script_change_player_relation_with_center", reg0, -4),
        (change_screen_return),
        ]
       ),

      ("choice_04h_5", [], "Let your other soldiers play with her.",
       [(call_script, "script_change_player_honor", -4),
	    (call_script, "script_change_player_relation_with_center", reg0, -8),
	    (call_script, "script_change_player_party_morale", 10),
        (change_screen_return),
        ]
       ),

	   ("choice_04h_6", [], "This, also cut her tongue so she can't tell her tale and whip the scouts for not sharing with the party.",
       [(call_script, "script_change_player_honor", -10),
	    (assign, "$g_whiped_for_example", 1),
	    (call_script, "script_change_player_party_morale", 5),
        (change_screen_return),
        ]
       ),

        ]
       ),
]
