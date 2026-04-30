SIMPLE_TRIGGERS = [
(24*10, 
     [  (assign, ":difficulty_factor", "$g_sod_difficulty"),
	    (val_mul, ":difficulty_factor", 10),

		(assign, ":diplomatic_factor", "$g_sod_diplomatic_difficulty"),
		(val_mul, ":diplomatic_factor", 5),
		
		(val_add, ":difficulty_factor", ":diplomatic_factor"),
		# Safety: keep score factor in sane bounds.
		(val_clamp, ":difficulty_factor", -100, 101),
		
         (try_begin),
           (eq, "$g_sod_deactivate_forced_rest", 0),
           (val_add, ":difficulty_factor", 4),
         (try_end),  
		 
         (try_begin),
		   (this_or_next|faction_slot_eq, "fac_player_faction", slot_faction_center_transfer_option, 1),
		   (faction_slot_eq, "fac_player_faction", slot_faction_center_transfer_option, 3),
		   (val_add, ":difficulty_factor", 1),
		 (try_end),

         (try_begin),
            (neq, ":difficulty_factor", "$g_sod_global_difficulty"),
            (val_add, "$g_sod_global_difficulty", ":difficulty_factor"),
            (val_div, "$g_sod_global_difficulty", 2),   			
			(val_clamp, "$g_sod_global_difficulty", -100, 101),
         (try_end), 
  ]),
]
