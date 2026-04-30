DIALOGS = [
[trp_sod_marshal|plyr, "marshal_ai_choice", [(gt, reg0, 0)], "I want your advice. Change our strategy as you think it should be, now.", "marshal_ai", 
	 [(faction_set_slot, "fac_player_supporters_faction", 207, 0), 
	 (call_script, "script_set_faction_defensive_objective", "fac_player_supporters_faction"),
	 (call_script, "script_set_faction_offensive_objective", "fac_player_supporters_faction"),
	 (faction_set_slot, "fac_player_supporters_faction", 207, 1), 
	 ]],
]
