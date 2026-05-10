DIALOGS = [
[anyone|plyr,"mate_chat_contract_cancel2", [
		(assign, ":total_cost", 0),
		(party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop", "$g_encountered_party", ":i_stack"),
			(party_stack_get_size, ":stack_size", "$g_encountered_party", ":i_stack"),
			(call_script, "script_game_get_troop_wage", ":stack_troop", "p_main_party"),
			(assign, ":cur_cost", reg0),
			(val_mul, ":cur_cost", ":stack_size"),
			(val_add, ":total_cost", ":cur_cost"),
        (try_end),
		(store_troop_gold, ":gold", "trp_player"),
		(ge, ":gold", ":total_cost"),
		(assign, reg19, ":total_cost"),
	], "Here you are, {reg19} denars. The account is closed.", "close_window",[
		(call_script, "script_sod_player_charge_gold", reg19),
		(call_script, "script_merc_party_change_state", "$g_encountered_party"),
	]],
]
