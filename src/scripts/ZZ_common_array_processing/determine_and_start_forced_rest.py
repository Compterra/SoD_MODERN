SCRIPTS = [
("determine_and_start_forced_rest",
	  [	 
	  (assign, ":remaining_time", "$post_battle_forced_rest_time"),
	  
	  (assign, "$post_battle_forced_rest_time", 0),
	  
	  (store_div, ":defeated_enemy_strength", "$g_starting_strength_enemy_party", 3),
      (val_add, "$post_battle_forced_rest_time", ":defeated_enemy_strength"),
	  
	  (call_script, "script_party_count_fit_for_battle", "p_main_party"),
	  (assign, ":unwounded", reg0),
	  (party_get_num_companions, ":num_comp", "p_main_party"),
	  (party_get_num_prisoners, ":num_pris", "p_main_party"),
      (store_add, ":total_size", ":num_comp", ":num_pris"),
	  
	  (try_begin),
	  (ge, ":total_size", 120),
	  (store_div, ":big_party", ":total_size", 60),
	  (val_mul, "$post_battle_forced_rest_time", ":big_party"),  # double base duration for every 60 guys above 60
      (try_end),
	  
	  (try_begin),
		  (lt, ":num_comp", 20),
		  (eq, ":unwounded", ":total_size"),
		  (lt, ":remaining_time", 10),
		  (assign, "$post_battle_forced_rest_time", 0),
		  (assign, "$g_start_postbattle_forced_rest", 0),  # no forced rest if the character is quasi alone, has no wounded/prisoner and his party wasn't tired
	  
	  (else_try),
	  
		  (store_sub, ":small_party", 60, ":num_comp"),    # reduce duration if less than 60 companions
		  (val_min, ":small_party", 0),
		  (val_add, ":unwounded", ":small_party"),
		  (val_mul, ":unwounded", 100),
		  (val_div, ":unwounded", ":total_size"),   # prisoners slow the party and count as woundeds
		  (val_div, "$post_battle_forced_rest_time", ":unwounded"),
		  
		  (party_get_morale, ":morale", "p_main_party"),
		  (val_max, ":morale", 25),                 # low morale can triple duration no more
		  (val_mul, "$post_battle_forced_rest_time", 75),
		  (val_div, "$post_battle_forced_rest_time", ":morale"),
		  (val_max, "$post_battle_forced_rest_time", 12), # minimum added fatigue		  
		  
		  (val_add, "$post_battle_forced_rest_time", ":remaining_time"),
		  (val_min, "$post_battle_forced_rest_time", 60), # no more than 6 hours total
		  
		  (store_mul, ":chance_to_rest", "$post_battle_forced_rest_time", 2),   # instead of an unoticeable short rest after each battle
		  (val_sub, ":chance_to_rest", 10),                                     # make the party take an occasionnal long rest after several
		  (store_random_in_range, ":rnd", 0, 100),                              
		  
	  (try_begin),  
	  (eq, "$g_sod_debug", 1),
	  #(assign, ":rnd", 0),  #debug test forced rest
	  (assign, reg1, "$post_battle_forced_rest_time"),
	  (assign, reg2, ":defeated_enemy_strength"),
	  (assign, reg3, ":morale"),
	  (display_log_message, "@Forced rest system is working, forced rest time {reg1}, defeated army strength {reg2}, morale {reg3}.", debug_color),
      (try_end),
		  
	(try_begin),
    (lt, ":rnd", ":chance_to_rest"), 	
    (gt, "$post_battle_forced_rest_time", 12),  # twan456 no forced rest for minimum small battles exhaustion 	
	(assign, "$g_start_postbattle_forced_rest", 1),	
    (assign, "$g_is_in_forced_rest", 1),	
		 (try_begin),
		 (le, "$post_battle_forced_rest_time", 30),
         (rest_for_hours, 3, 1, 1), # rest will be interrupted by trigger 132
		 (else_try),
		 (rest_for_hours, 7, 2, 1), # rest at twice speed if resting for more than 3 hours
		 (try_end),	
    (try_end),
	  
	  (try_end),	  
	  ]),
]
