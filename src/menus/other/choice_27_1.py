MENUS = [
(
    "event_27", mnf_disable_all_keys,
    "Some {s2} visit you. They think that the public sacrifice of virgins in all the towns and villages of your realm would help your religion to spread.\
People not sharing your faith will probably be extremely shocked by this, and killing these innocent would alwo lower your honor.",
    "none",
    [    (try_begin),
	    (eq, "$g_sod_faith", cb_the_void),
		(str_store_string, s2, "@priests of the Void"),
		(else_try),
		(str_store_string, s2, "@priests of the Old Golds"),
		(try_end),
    ],
    [
      ("choice_27_1", [], "Order the sacrifices (cost: 10 honor).", [
			(call_script, "script_change_player_honor", -10),
		    (val_add, "$g_sod_global_faith", 150),
		    (val_clamp, "$g_sod_global_faith", -2000, 2001),
	        (val_add, "$g_sod_clergy_happines", 10),
			
			(try_for_range, ":center_no", centers_begin, centers_end),
			(store_faction_of_party, ":center_fac", ":center_no"),
			(eq, ":center_fac", "fac_player_supporters_faction"),
			(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(try_begin),
				 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
				 (call_script, "script_change_player_relation_with_center", ":center_no", 5),
				 (party_get_slot, ":local_faith", ":center_no", slot_center_sod_local_faith),
				 (val_add, ":local_faith", 10),
				 (val_min, ":local_faith", 100),
				 (party_set_slot, ":center_no", slot_center_sod_local_faith, ":local_faith"),
				(else_try),
				(call_script, "script_change_player_relation_with_center", ":center_no", -10),
				(try_end),
			(try_end),
			
          (change_screen_return),
        ]
       ),
	   
        ("choice_27_2", [], "Only make some sacrifices, where your faith is strong.", [
            (call_script, "script_change_player_honor", -5),
			(assign, ":global_faith_effect", 0),
			
			(try_for_range, ":center_no", centers_begin, centers_end),
			(store_faction_of_party, ":center_fac", ":center_no"),
			(eq, ":center_fac", "fac_player_supporters_faction"),
			(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(try_begin),
				 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 20),
				 (call_script, "script_change_player_relation_with_center", ":center_no", 5),
				 (party_get_slot, ":local_faith", ":center_no", slot_center_sod_local_faith),
				 (val_add, ":local_faith", 5),
				 (val_min, ":local_faith", 100),
				 (val_add, ":global_faith_effect", 15),
				 (party_set_slot, ":center_no", slot_center_sod_local_faith, ":local_faith"),
				(try_end),
			(try_end),
			
			(val_min, ":global_faith_effect", 70),
			(val_add, "$g_sod_global_faith", ":global_faith_effect"),
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
			 
          (change_screen_return),
        ]
       ),
	   
	   ("choice_27_3", [], "Buy 1000 denars of goats and make animal sacrifices instead.", [
	   	   (val_sub, "$g_sod_clergy_happines", 10),
			(store_troop_gold, ":gold", "trp_player"),
			(try_begin),
            (ge, ":gold", 1000),
			
            (troop_remove_gold, "trp_player", 1000),
		    (val_add, "$g_sod_global_faith", 100),
		    (val_clamp, "$g_sod_global_faith", -2000, 2001),

				(try_for_range, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
				(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(try_begin),
				 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
				 (call_script, "script_change_player_relation_with_center", ":center_no", 5),
				 (party_get_slot, ":local_faith", ":center_no", slot_center_sod_local_faith),
				 (val_add, ":local_faith", 5),
				 (val_min, ":local_faith", 100),
				 (party_set_slot, ":center_no", slot_center_sod_local_faith, ":local_faith"),
				(else_try),
				(call_script, "script_change_player_relation_with_center", ":center_no", -5),
				(try_end),
			(try_end),
			
            (else_try),
            (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
            (call_script, "script_change_troop_renown", "trp_player", -5),
            (val_sub, "$g_sod_global_faith", 25),
            (val_clamp, "$g_sod_global_faith", -2000, 2001),
             (try_end),
          (change_screen_return),
        ]
       ),
	     
         ("choice_27_4", [], "Refuse to make sacrifices.", [
			 (val_sub, "$g_sod_global_faith", 80),
			 (val_clamp, "$g_sod_global_faith", -2000, 2001),
			 (val_sub, "$g_sod_clergy_happines", 10),
			 
          (change_screen_return),
        ]
       ),
	   
	    ("choice_27_5", [], "Refuse to make sacrifices and publicly condemn the priests for this silly idea.", [
			 (val_sub, "$g_sod_global_faith", 100),
			 (val_clamp, "$g_sod_global_faith", -2000, 2001),
			 (val_sub, "$g_sod_clergy_happines", 25),
			 
			 	(try_for_range, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
				(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
					 (call_script, "script_change_player_relation_with_center", ":center_no", -5),
					 (party_get_slot, ":local_faith", ":center_no", slot_center_sod_local_faith),
					 (val_sub, ":local_faith", 5),
					 (val_max, ":local_faith", 0),
					 (party_set_slot, ":center_no", slot_center_sod_local_faith, ":local_faith"),
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
