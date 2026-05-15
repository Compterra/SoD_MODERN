MENUS = [
(
    "event_04c", mnf_disable_all_keys,
    "You encounter the widow of one of your fallen soldiers. She says her family is starving without his wages.",
    "none",
    [
    ],
    [
      ("choice_04c_1", [], "His service is over. I owe the family nothing.",
       [
        (call_script, "script_change_player_honor", -2),
        (call_script, "script_change_player_party_morale", -5),
          (change_screen_return),
        ]
       ),


	  ("choice_04c_2", [], "Give her 50 denars and send her away.",
       [(store_troop_gold, ":gold", "trp_player"),
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


      ("choice_04c_3", [], "Give her 500 denars in compensation.",
       [(store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 500),
        (call_script, "script_change_player_honor", 3),
        (call_script, "script_sod_player_charge_gold", 500),
	    (call_script, "script_change_player_party_morale", 10),
        (else_try),
        (display_message, "@You don't have enough gold to compensate her.", quest_fail_color),
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
