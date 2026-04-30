MENUS = [
(
    "event_04", mnf_disable_all_keys,
    "Your men have catched a beautiful country woman who was trying to steal some food in your baggage. She is in need and begs you to let her go with something for her brothers.\
<< Harvest was poor and can't feed the whole family. You are our only chance to survive my lord... >> she begs you when most of your men, showing no pity, look at her with brilliant eyes.",
    "none",
    [

    ],
    [
      ("choice_04_1", [], "This can't be! Here take 100 denars.",
       [
       (store_troop_gold, ":gold", "trp_player"),
       (try_begin),
        (ge, ":gold", 100),
        (call_script, "script_change_player_honor", 3),
        (troop_remove_gold, "trp_player", 100),
	    (call_script, "script_get_closest_village", "p_main_party"),
	    (call_script, "script_change_player_relation_with_center", reg0, 5),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
		(try_end),
	    (call_script, "script_change_player_party_morale", -5),
         (change_screen_return),
        ]
       ),
      ("choice_04_2", [], "You can go, but I won't give anything to a thief.",
       [
	    (call_script, "script_change_player_party_morale", -5),
	    (call_script, "script_get_closest_village", "p_main_party"),
	    (call_script, "script_change_player_relation_with_center", reg0, -1),
        (change_screen_return),
        ]
       ),
	  ("choice_04_3", [], "My law suffer no exception, execute her.",
       [
	    (call_script, "script_change_player_honor", -2),
		(call_script, "script_get_closest_village", "p_main_party"),
		(call_script, "script_change_player_relation_with_center", reg0, -10),
        (change_screen_return),
        ]
       ),
      ("choice_04_4", [(eq, "$g_sod_parental_advisory", 0)], "Why starve when my army could use services of such a pretty young girl?",
       [
       (call_script, "script_change_player_honor", -3),
       (call_script, "script_change_player_party_morale", 10),
	   (call_script, "script_get_closest_village", "p_main_party"),
	   (call_script, "script_change_player_relation_with_center", reg0, -5),
       (change_screen_return),
        ]
       ),

	   ("choice_04_5", [(eq, "$character_gender", tf_male), (eq, "$g_sod_parental_advisory", 0)], "I'll give you 50 denars after some time in my tent.",
       [
       (call_script, "script_change_player_honor", -1),
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
