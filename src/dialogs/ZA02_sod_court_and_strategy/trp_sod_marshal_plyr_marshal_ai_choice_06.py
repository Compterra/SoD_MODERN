DIALOGS = [
[trp_sod_marshal|plyr, "marshal_ai_choice", [(gt, reg0, 0)], "I want to give more importance to defense.", "marshal_ai", 
	 [ (faction_get_slot, ":ambition", "fac_player_supporters_faction", slot_faction_ambition),
	   (val_sub, ":ambition", 1),
	   (val_max, ":ambition", -6),
       (faction_set_slot, "fac_player_supporters_faction", slot_faction_ambition, ":ambition"),
       (faction_set_slot, "fac_player_supporters_faction", 207, 1),	]],
]
