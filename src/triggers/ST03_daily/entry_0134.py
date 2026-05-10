SIMPLE_TRIGGERS = [
(6,
   [
    (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
		(party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
		(party_get_slot, ":trainers", ":cur_center", slot_center_trainers),
		(gt, ":trainers", 0),
		
		(party_get_num_companion_stacks, ":num_stacks", ":cur_center"),
		(try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":cur_troop", ":cur_center", ":i_stack"),
			(troop_get_slot, ":sod_soldier", ":cur_troop", slot_troop_sod_soldier),
			(party_stack_get_size, ":stack_size", ":cur_center", ":i_stack"),
			(store_mul, ":exp", ":trainers", ":stack_size"), 
			
			(try_begin),
				(eq, ":sod_soldier", 1),
				(party_slot_eq, ":cur_center", slot_center_has_barracks, 1),
				(party_add_xp_to_stack, ":cur_center", ":i_stack", ":exp"),
			(else_try),
				(eq, ":sod_soldier", 2),
				(party_slot_eq, ":cur_center", slot_center_has_range, 1),
				(party_add_xp_to_stack, ":cur_center", ":i_stack", ":exp"),
			(else_try),
				(eq, ":sod_soldier", 3),
				(party_slot_eq, ":cur_center", slot_center_has_stables, 1),
				(party_add_xp_to_stack, ":cur_center", ":i_stack", ":exp"),
			(try_end),
		(try_end),
		
		(party_upgrade_with_xp, ":cur_center", 1, 1),
	(try_end),
    ]),
]
