SIMPLE_TRIGGERS = [
(24*7,
   [
       (try_for_range, ":center_no", centers_begin, centers_end),
		 (party_slot_ge, ":center_no", slot_town_lord, "trp_player"),
         (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":center_no"),
         (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
           (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":stack_no"),
           (neg|troop_is_hero, ":stack_troop"),
           (party_prisoner_stack_get_size, ":stack_size", ":center_no", ":stack_no"),
           (store_random_in_range, ":rand_no", 0, 40),
           (val_mul, ":stack_size", ":rand_no"),
           (val_div, ":stack_size", 100),
           (party_remove_prisoners, ":center_no", ":stack_troop", ":stack_size"),
		   
		   (store_faction_of_party, ":center_fac", ":center_no"),  #twan456 begin
		   
		   (faction_get_slot, ":transfer_system", "fac_player_faction", slot_faction_center_transfer_option),
		   (assign, ":continue", 0),

				 (try_begin),
					(eq, ":transfer_system", 0),
					(eq, "$g_sod_deactivate_ai", 0),
					(assign, ":continue", 1),
					(else_try),
					(eq, ":transfer_system", 1),
					(eq, "$g_sod_deactivate_ai", 0),
					(neq, ":center_fac", "fac_player_supporters_faction"),
					(assign, ":continue", 1),   				
				 (try_end),
				 
		      (try_begin),		 
				(eq, ":continue", 1), 
				 
				(store_character_level, ":troop_level", ":stack_troop"),   #twan456
				(try_begin),
                   (party_slot_eq, ":center_no", slot_center_has_prisoner_tower, 1),  
                   (val_mul, ":troop_level", 2),
				   (else_try),
				   (val_mul, ":troop_level", 3),
                (try_end),   	

				(val_add, ":troop_level", ":stack_size"),				
				 
				(store_random_in_range, ":rnd", 0, 100),        # reduce the chance to recruit high level prisoners
		        (gt, ":rnd", ":troop_level"),
		   
			   (party_get_num_companion_stacks, ":num_companion_stacks", ":center_no"),
			   
			   (lt, ":num_companion_stacks", 30), #always let some space
		       		
			   (party_add_members, ":center_no", ":stack_troop", ":stack_size"), 
			   (try_end), #twan456end
         (try_end),
       (try_end),
    ]),
]
