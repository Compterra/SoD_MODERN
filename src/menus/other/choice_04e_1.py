MENUS = [
(
    "event_04e", mnf_disable_all_keys,
    "Your soldiers have catched a girl with foxy hair and accuse her to be a witch.",
    "none",
    [
    ],
    [
      ("choice_04e_1", [], "Gather some wood and burn her, foxy hair are a sure sign of her demonic pact !",
       [
        (call_script, "script_change_player_honor", -4),
        (call_script, "script_change_player_party_morale", 5),  
        (rest_for_hours, 2, 1, 1),
		(display_message, "@Gathering wood take 2 hours."),
		(change_screen_return),
        ]
       ),


	  ("choice_04e_2", [], "Free her, witches are just a legend.",
       [
        (call_script, "script_change_player_honor", 2),
        (call_script, "script_change_player_party_morale", -5),
        (change_screen_return),
        ]
       ),


      ("choice_04e_3", [], "Offer her to join your party.",
       [(call_script, "script_change_player_honor", 2),
	    (party_add_members, "p_main_party", "trp_follower_woman", 1),
        (call_script, "script_change_player_party_morale", -10),
        (change_screen_return),
        ]
       ),

        ]
       ),
]
