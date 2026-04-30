MENUS = [
(
    "event_04c", mnf_disable_all_keys,
    "You encounter the widow of one of the soldiers who died at your service, she explains you that their family is starving without his wages.",
    "none",
    [
    ],
    [
      ("choice_04c_1", [], "He was a good soldier, but not good enough I guess.",
       [
        (call_script, "script_change_player_honor", -2),
        (call_script, "script_change_player_party_morale", -5),
          (change_screen_return),
        ]
       ),


	  ("choice_04c_2", [], "Here are 50 denars now stop complaining.",
       [(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 50),
        (troop_remove_gold, "trp_player", 50),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
        (change_screen_return),
        ]
       ),


      ("choice_04c_3", [], "Here are 500 denars to compensate the loss of your husband.",
       [(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 500),
        (call_script, "script_change_player_honor", 3),
        (troop_remove_gold, "trp_player", 500),
	    (call_script, "script_change_player_party_morale", 10),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
        (change_screen_return),
        ]
       ),

	   ("choice_04c_4", [(eq, "$character_gender", tf_male), (eq, "$g_sod_parental_advisory", 0)], "I'll give you 50 denars after some time in my tent.",
       [
       (call_script, "script_change_player_honor", -1),
	   (call_script, "script_change_player_party_morale", -5),
	   (store_troop_gold, ":gold", "trp_player"),
	    (try_begin),
        (ge, ":gold", 50),
        (troop_remove_gold, "trp_player", 50),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
