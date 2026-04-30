DIALOGS = [
[trp_sod_chancellor, "chancellor_peace", [ 
	 (neg|faction_slot_ge, "fac_player_supporters_faction", slot_faction_num_towns, 3),
	 (faction_slot_ge, "fac_player_supporters_faction", slot_faction_badboy_rating, 15)], 
	 "Other rulers prefer to kill the snake your are for them in its egg, they won't listen to your ambassadors as long you own less than three towns.", "chancellor_talk", []],
]
