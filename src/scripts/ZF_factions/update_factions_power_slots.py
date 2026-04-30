SCRIPTS = [
( "update_factions_power_slots",
 [    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
	  
		  (faction_get_slot, ":old_power", ":faction_no", slot_faction_old_power),
		  (faction_get_slot, ":stored_power", ":faction_no", slot_faction_current_power),
		  (faction_get_slot, ":last_power", ":faction_no", slot_faction_last_week_power),
		  (faction_set_slot, ":faction_no", slot_faction_last_week_power, ":stored_power"),
		  
		  (assign, ":new_old_power", ":old_power"),
		  (val_mul, ":new_old_power", 4),
		  (val_add, ":new_old_power", ":last_power"),
		  (val_div, ":new_old_power", 5),
		  
		  (faction_set_slot, ":faction_no", slot_faction_old_power, ":new_old_power"),

		  (call_script, "script_calculate_faction_power", ":faction_no"),  #updates the current power slot
		  (faction_get_slot, ":cur_power", ":faction_no", slot_faction_current_power), 
		  
		  (store_add, ":new_evolution", ":cur_power", ":stored_power"),        # compares the average power of the last week and this one                               
		  (val_mul, ":new_evolution", 50),									  # with an average of old power values (renewed every 5 weeks)
		  (val_div, ":new_evolution", ":new_old_power"),                       
		  
		  (faction_get_slot, ":old_evolution", ":faction_no", slot_faction_power_evolution), # mitigates a little evolution with the last so extreme evolutions should be very rare
		  (val_mul, ":new_evolution", 4),
		  (val_add, ":new_evolution", ":old_evolution"),
		  (val_div, ":new_evolution", 5),
		  
		  (faction_set_slot, ":faction_no", slot_faction_power_evolution, ":new_evolution"),	
	 

      (try_begin),
      (eq, "$g_sod_debug", 1),
      (assign, reg0, ":cur_power"),
	  (assign, reg1, ":last_power"),
	  (assign, reg2, ":old_power"),
	  (assign, reg3, ":new_old_power"),
	  (assign, reg4, ":stored_power"),
	  (assign, reg6, ":new_evolution"),
	  (str_store_faction_name, s3, ":faction_no"),
	  (display_log_message, "@{s3} has a current power of {reg0}, a last stored power of {reg4}, a last week power of {reg1} had a old power of {reg2} and now an old power of {reg3}, and its evolution is {reg6}.", debug_color),
	  (call_script, "script_update_faction_notes", ":faction_no"),	
	  (try_end),		  
	  (try_end),
	  ]),
]
