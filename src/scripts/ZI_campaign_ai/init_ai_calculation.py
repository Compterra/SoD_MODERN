SCRIPTS = [
("init_ai_calculation",
    [(assign, "$g_calculating_ais", 1),  # make non center parties store a strength based on outdoor and siege, instead of one or the other

     (call_script, "script_party_calculate_strength", "p_main_party", 0), #will update slot_party_cached_strength
	  
	  (try_for_parties, ":party_no"),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_ai_mercenaries),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_player_mercenaries),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_player_patrol),
	  (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
	  (call_script, "script_party_calculate_strength", ":party_no", 0),
	  (try_end),                                                                 # SOD TWAN changes end

	  (try_for_range, ":cur_troop", heroes_begin, heroes_end),
      (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (gt, ":cur_troop_party", 0),
		(call_script, "script_party_calculate_strength", ":cur_troop_party", 0),
        (call_script, "script_party_calculate_and_set_nearby_friend_strength", ":cur_troop_party"),
      (try_end),
	  
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
	    (call_script, "script_party_calculate_strength", ":cur_center", 0),
        (call_script, "script_party_calculate_and_set_nearby_friend_strength", ":cur_center"),
      (try_end),
	  
	  (assign, "$g_calculating_ais", 0),
      (call_script, "script_party_calculate_and_set_nearby_friend_strength", "p_main_party"),
  ]),
]
