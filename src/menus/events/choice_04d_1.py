MENUS = [
(
    "event_04d", mnf_disable_all_keys,
    "You encounter a group of villagers from {s1} surrounding a girl with foxy hair. They seem to be going to burn her as a witch.",
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
      ("choice_04d_1", [], "Let them, foxy hair are a sure sign of her demonic pact.",
       [
        (call_script, "script_change_player_honor", -3),
        (call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", 3),
          (change_screen_return),
        ]
       ),


	  ("choice_04d_2", [], "Free her, witches are just a legend.",
       [
        (call_script, "script_change_player_honor", 2),
		(call_script, "script_change_player_relation_with_center", "$sod_event_relation_center", -5),
        (change_screen_return),
        ]
       ),


      ("choice_04d_3", [], "Say you are going to investigate her case and offer her to join your party.",
       [(call_script, "script_change_player_honor", 2),
	    (party_add_members, "p_main_party", "trp_follower_woman", 1),
	    (call_script, "script_change_player_party_morale", -5),
        (change_screen_return),
        ]
       ),

        ]
       ),
]
