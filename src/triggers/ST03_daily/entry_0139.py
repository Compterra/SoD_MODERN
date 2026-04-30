SIMPLE_TRIGGERS = [
(24, [
       (store_current_day, ":day"),
       (assign, ":last_kingdom", -1),

       (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),	   # truces ending
		   (faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
			   (try_begin),
			   (faction_slot_ge, ":kingdom_no", slot_faction_council_day, 5),
			   (assign, ":last_kingdom", ":kingdom_no"),
			   (try_end),
			 (try_for_range, ":truce_slot", faction_truce_slots_begin, faction_truce_slots_end),
			 (faction_get_slot, ":truce_day", ":kingdom_no", ":truce_slot"),
			   (try_begin),
				  (eq, ":truce_day", ":day"),
				  (store_sub, ":kingdom2_no", ":truce_slot", faction_truce_slots_begin),
				  (val_add, ":kingdom2_no", "fac_player_supporters_faction"), #twanx was a critical bug
				  (str_store_faction_name_link, s6, ":kingdom_no"),
				  (str_store_faction_name_link, s7, ":kingdom2_no"),
						 (try_begin),
					  (eq, ":kingdom_no", "fac_player_supporters_faction"),
					  (faction_slot_eq, ":kingdom2_no", slot_faction_state, sfs_active),
					  (display_log_message, "@Your truce with {s7} has lapsed. You may now attack them without penalty.", periwinkle),
						 (else_try),
					  (eq, "$g_sod_hide_messages", 0),
					  (lt, ":kingdom_no", ":kingdom2_no"),
					  (faction_slot_eq, ":kingdom2_no", slot_faction_state, sfs_active),
					  (display_log_message, "@The truce between {s6} and {s7} has lapsed. Their war may soon begin anew.", light_gray),
						 (try_end),
				  (faction_set_slot, ":kingdom_no", ":truce_slot", -1),
			   (try_end),
            (try_end),
	    (try_end), 
	   
	      (assign, ":kingdom_taking_decisions", -1),     				# call one kingdom council

							 
              (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
				  (faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
				  (faction_get_slot, ":council_day", ":kingdom_no", slot_faction_council_day), 
				  (store_random_in_range, ":rnd", 0, 3),	
				  (val_add, ":council_day", 1),			  
					(try_begin),
						 (ge, ":council_day", 9),
						 (assign, ":kingdom_taking_decisions", ":kingdom_no"), # make sure this kingdom is chosen if one didn't had council since 9+ days
					 (else_try),	 
						 (assign, ":chance", 0),
						 (try_begin),
							  (eq, ":kingdom_no", ":last_kingdom"),
							  (val_add, ":chance", 1),
							  (else_try),
							  (neg|faction_slot_ge, ":kingdom_no", slot_faction_power_evolution, 70), # make kingdoms in really bad situations call council more often
							  (val_add, ":chance", 1),
					     (try_end),
					     (try_begin),				 
							 (eq, ":kingdom_taking_decisions", -1),
							 (ge, ":council_day", 5),
							 (le, ":rnd", ":chance"),
							 (assign, ":kingdom_taking_decisions", ":kingdom_no"),
						 (try_end),
					 (try_end),
					(faction_set_slot, ":kingdom_no", slot_faction_council_day, ":council_day"),
              (try_end),
			  
			(try_begin),
               (eq, ":kingdom_taking_decisions", "fac_player_supporters_faction"),  # twan454 don't call council if player has chosen strategy
               (faction_slot_eq, "fac_player_supporters_faction", 207, 1),
			   (assign, ":kingdom_taking_decisions", -1),
			(try_end),   
 			   
         
            (gt, ":kingdom_taking_decisions", -1),
            (call_script, "script_set_faction_central_center", ":kingdom_taking_decisions"),
            (call_script, "script_set_faction_offensive_objective", ":kingdom_taking_decisions"), 
			(call_script, "script_set_faction_defensive_objective", ":kingdom_taking_decisions"),
            (faction_set_slot, ":kingdom_taking_decisions", slot_faction_council_day, 0),
			
			(try_begin),
			(eq, "$g_sod_debug", 1),
			(str_store_faction_name, s6, ":kingdom_taking_decisions"),
			(display_log_message, "@{s6} has held a council.", debug_color),
			(try_end),
       ]),
]
