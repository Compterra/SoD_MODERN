MENUS = [
(
    "event_27", mnf_disable_all_keys,
    "Some {s2} visit you. They demand public human sacrifices in every town and village, claiming terror and devotion will help your religion spread. Those who do not share your faith will be horrified, and innocent blood will stain your honor.",
    "none",
    [    (try_begin),
	    (eq, "$g_sod_faith", cb_the_void),
		(str_store_string, s2, "@priests of the Void"),
		(else_try),
		(str_store_string, s2, "@priests of the Old Gods"),
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
	   
        ("choice_27_2", [], "Order sacrifices only where your faith is strong.", [
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
			
            (call_script, "script_sod_player_charge_gold", 1000),
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
            (display_message, "@You don't have enough gold to buy the sacrificial animals.", quest_fail_color),
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
	   
	    ("choice_27_5", [], "Refuse the sacrifices and publicly condemn the priests.", [
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
