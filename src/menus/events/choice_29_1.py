MENUS = [
(
    "event_29", mnf_disable_all_keys,
    "Some philosophers visit you. They complain about the strength of supersticion in your realm villages. They think you should publicly affirm that no god\
or spirit exist and so condemn the priests of false religions and other magicians abusing your naive country men.",
    "none",
    [
    ],
    [
      ("choice_29_1", [], "Order your sheriffs to make examples and execute all priests or magicians they find.", [
	  	  (call_script, "script_change_player_honor", -4),
		  (val_add, "$g_sod_global_faith", 100),
		  (val_clamp, "$g_sod_global_faith", -2000, 2001),
		  (val_add, "$g_sod_clergy_happines", 10),
		  		(try_for_range, ":center_no", villages_begin, villages_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 20),
					(else_try),
					(call_script, "script_change_player_relation_with_center", ":center_no", -5),
					(try_end),
				(try_end),
          (change_screen_return),
        ]
       ),
             ("choice_29_2", [], "Condemn supersticion and bannish priests and magicians from your realm.", [
			(val_add, "$g_sod_global_faith", 50),
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
		    (val_add, "$g_sod_clergy_happines", 10),
		  		(try_for_range, ":center_no", villages_begin, villages_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
					(else_try),
					(call_script, "script_change_player_relation_with_center", ":center_no", -5),
					(try_end),
				(try_end), 
          (change_screen_return),
        ]
       ),
             ("choice_29_3", [], "Ignore the philosophers request.", [
			(val_sub, "$g_sod_global_faith", 50),
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
		    (val_sub, "$g_sod_clergy_happines", 10),
          (change_screen_return),
        ]
       ),
             ("choice_29_4", [], "Guarantee freedom of religion in your realm.", [
			(val_sub, "$g_sod_global_faith", 100),
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
		    (val_sub, "$g_sod_clergy_happines", 20), 
				(try_for_range, ":center_no", villages_begin, villages_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
					(else_try),
					(call_script, "script_change_player_relation_with_center", ":center_no", 5),
					(try_end),
				(try_end), 
          (change_screen_return),
        ]
       ),
      ]
  ),
]
