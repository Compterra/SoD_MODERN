MENUS = [
(  "event_04i", mnf_disable_all_keys,
    "Some professionnal girls approach your party and offer their services to your men.",
    "none",
    [  	(party_get_num_companions, reg0, "p_main_party"),
        (val_mul, reg0, 15),
    ],
    [
      ("choice_04h_1", [], "Offer all your men some pleasure for {reg0} denars.",
       [
		(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", reg0),
        (call_script, "script_change_player_party_morale", 15),
        (troop_remove_gold, "trp_player", reg0),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
		(change_screen_return),
        ]
       ),

	  ("choice_04i_2", [], "Let the girls do their job if your men can pay.",
       [
	    (call_script, "script_change_player_party_morale", 5),
	    (call_script, "script_change_player_relation_with_center", reg0, -2),
		(change_screen_return),
        ]
       ),

	  ("choice_04i_3", [], "Let all your men take some pleasure without paying.",
       [(call_script, "script_change_player_party_morale", 10),
		(call_script, "script_change_player_honor", -3),
        (change_screen_return),
        ]
       ),

	  ("choice_04i_4", [], "Refuse the offer and sermon your men about prostitution.",
       [(call_script, "script_change_player_honor", 2),
	    (call_script, "script_change_player_party_morale", -10),
        (change_screen_return),
        ]
       ),
        ]
       ),
]
