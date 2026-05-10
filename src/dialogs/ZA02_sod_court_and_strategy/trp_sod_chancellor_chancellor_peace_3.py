DIALOGS = [
[trp_sod_chancellor, "chancellor_peace_3", [
      (faction_get_slot, ":ambition", "$temp", slot_faction_ambition),                   # twan new
	   (store_relation, ":rln", "fac_player_supporters_faction", "$temp"),
       (call_script, "script_get_number_of_factions_at_war_with_faction", "$temp"),
	   (assign, ":minimum_chance", reg0),                          #twan456 fix
	   (val_mul, ":minimum_chance", 3),
     	 (try_begin),
		   (eq, "$temp", "fac_kingdom_6"),
		   (assign, ":minimum_chance", 0),
		 (try_end),
		 (try_begin),
			 (gt, ":rln", -20),
			 (val_add, ":minimum_chance", 10),
		  (try_end),		 
       (store_div, ":chances_to_accept_peace", ":rln", 5), # - 20% with -100 relation  
       (val_mul, ":ambition", -10),
       (val_add, ":chances_to_accept_peace", ":ambition"),  
	   
	   (call_script, "script_compare_faction_faction_num_prisoners", "fac_player_supporters_faction", "$temp"),
         (try_begin),
         (ge, reg0, 0),
         (store_mul, ":bonus", reg0, 4),  # having more prisoners increase a lot the chances as the enemy wants to free his own lords (ie : +20% if you have their king prisoner)
            (try_begin),
            (eq, "$temp", "fac_kingdom_6"), #one invader lord count as 1/3 of another faction lord here
            (val_div, ":bonus", 3),  # twan new
            (try_end),
         (else_try),
         (assign, ":bonus", reg0),  # having less prisoners don't decrease the chances as much (ie : -5% if they have the king prisoner)
         (try_end),
       (val_add, ":chances_to_accept_peace", ":bonus"), 
	   
	   (faction_get_slot, ":ruler", "$temp", slot_faction_leader),
	   (call_script, "script_troop_get_player_relation", ":ruler"),
	   (val_div, reg0, 3),
	   (val_add, ":chances_to_accept_peace", reg0), 
	   
	   (store_mul, ":bonus", "$g_sod_diplomatic_difficulty", -15),
	   (val_add, ":chances_to_accept_peace", ":bonus"),
	   
	   (faction_get_slot, ":badboy", "fac_player_supporters_faction", slot_faction_badboy_rating),
	   (val_sub, ":badboy", 20),
	   (val_mul, ":badboy", 2),
	   (val_min, ":badboy", -10),
	   (val_sub, ":chances_to_accept_peace", ":badboy"),
	   
       (val_add, ":chances_to_accept_peace", 40),    # a nation with +4 ambition only has minimum chance to accept, a nation with -6 ambition very probably accept, with 0 ambition chances to accept are a little under 40%  
            (try_begin),
            (faction_slot_eq, "$temp", slot_faction_last_started_war, "fac_player_supporters_faction"),
            (faction_get_slot, ":war_date", "$temp", slot_faction_last_started_war_date),
            (store_current_day, ":cur_day"),
            (store_sub, ":war_duration", ":cur_day", ":war_date"),
            (store_sub, ":duration_factor", 40, ":war_duration"),
			(val_sub, ":chances_to_accept_peace", ":duration_factor"),
            (try_end),
	   (val_max, ":chances_to_accept_peace", ":minimum_chance"),                          # twan new       
       (str_store_faction_name, s7, "$temp"),	   
            
       (store_random_in_range, ":rnd", 0, 100),
	   (str_clear, s31),
	   
	   (try_begin),
	      (lt, ":rnd", ":chances_to_accept_peace"),
		  (str_store_string, s31, "@{s7} accepted your peace proposal ! The peace has been concluded."),
		  (call_script, "script_diplomacy_start_peace_between_kingdoms", "fac_player_supporters_faction", "$temp", 3), 
	    (else_try),
		  (store_current_day, ":current_day"),
		  (faction_set_slot, "$temp", slot_faction_last_refused_peace, ":current_day"),
		  (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
		  (store_div, ":maximum", ":renown", 4),
		  (store_div, ":minimum", ":renown", 12),
		  (val_max, ":minimum", 25),
		  (assign, ":renown_lost", ":rnd"),
		  (val_add, ":renown_lost", ":badboy"),
		  (val_min, ":renown_lost", ":maximum"),
		  (val_max, ":renown_lost", ":minimum"),
		  (str_store_string, s31, "@{s7} refused. Your reputation suffers from the failed proposal."),
		  (val_sub, ":renown", ":renown_lost"),
		  (val_max, ":renown", 0),
		  (troop_set_slot, "trp_player", slot_troop_renown, ":renown"),
		(try_end),              		
	   
], "{s31}", "chancellor_talk", []],
]
