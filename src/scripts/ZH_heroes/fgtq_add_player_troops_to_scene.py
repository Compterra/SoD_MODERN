SCRIPTS = [
("fgtq_add_player_troops_to_scene", 
	[
		(store_script_param_1, ":amount"),
		
		(assign, ":entry_p", 1),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		(try_for_range, ":stack_no", 1, ":num_stacks"),
			(party_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
			(party_stack_get_troop_id, ":companion", "p_main_party", ":stack_no"),
			(try_for_range, ":unused", 0, ":stack_size"),
				(le, ":entry_p", ":amount"),
				(set_visitor, ":entry_p", ":companion"),
				(val_add, ":entry_p", 1),
			(try_end),
		(try_end),
	]),
]
