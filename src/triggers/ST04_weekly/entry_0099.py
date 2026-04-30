SIMPLE_TRIGGERS = [
(24 * 7,
  [
    #DEBUG
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (try_for_range, ":center_no", centers_begin, centers_end),

      # castles don't track faith (chapels are just for faith troop upgrades)
      (neg|is_between, ":center_no", castles_begin, castles_end),

      # only apply religious changes to centers in the players kingdom
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # +-5 relationship based on acceptance of the player's faith
      (party_get_slot, ":cur_relation", ":center_no", slot_center_player_relation),
      (party_get_slot, ":cur_faith", ":center_no", slot_center_sod_local_faith),
      (val_div, ":cur_faith", 20),
	  
	  #twan456 add badboy effect
	 
	  (faction_get_slot, ":badboy_rating", "fac_player_supporters_faction", slot_faction_badboy_rating),
	  (try_begin),
	    (le, ":badboy_rating", 16),
	    (store_sub, ":badboy_effect", 20, ":badboy_rating"),
        (val_div, ":badboy_effect", 4),
      (else_try),
        (ge, ":badboy_rating", 24),
        (store_sub, ":badboy_effect",  ":badboy_rating", 20),
		(val_div, ":badboy_effect", 4),
	  (else_try),
        (assign, ":badboy_effect", 0),
      (try_end), 		
	  
        (val_add, ":cur_faith", ":badboy_effect"),	#twan456 end
		(val_add, ":cur_relation", ":cur_faith"),		
		 

      # limit the downward spiral to -20 based purely on dislike of faith or badboy
      (this_or_next|gt, ":cur_faith", 0),
      (ge, ":cur_relation", -20),
      (val_min, ":cur_relation", 100),
      (val_clamp, ":cur_relation", -100, 101),
      (party_set_slot, ":center_no", slot_center_player_relation, ":cur_relation"),
    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
