SCRIPTS = [
("order_best_besieger_party_to_guard_center",
    [
      (store_script_param, ":defeated_center", 1),
      (store_script_param, ":winner_faction", 2),
      (assign, ":best_party", -1),
      (assign, ":best_party_strength", 0),
	  
	  (str_store_party_name, s12, ":defeated_center"),
	  (str_store_faction_name, s13, ":winner_faction"),
     
    (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end), # tr0
        (troop_get_slot, ":kingdom_hero_party", ":kingdom_hero", slot_troop_leaded_party),
        (gt, ":kingdom_hero_party", 0),
        (party_is_active, ":kingdom_hero_party"), #twan it seems there were opcode invalid parties error coming from this script so I've added checks
        (store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":defeated_center"),
        (lt, ":dist", 5),
        (store_faction_of_party, ":kingdom_hero_party_faction", ":kingdom_hero_party"),
        (eq, ":winner_faction", ":kingdom_hero_party_faction"),
	
    	(try_begin), #tr1
        (this_or_next|faction_slot_eq, ":winner_faction", slot_faction_marshall, ":kingdom_hero"),    #If marshall has captured the castle, then do not leave him behind.
        (eq, ":kingdom_hero", "trp_player"),
		(assign, ":has_besiege_ai", 0),
        (else_try),
        (assign, ":has_besiege_ai", 1),		# twan453 removed ai checks, any nearby party can be chosen
        (try_end), #tr1
      
      (try_begin), #tr2
        (eq, ":has_besiege_ai", 1),
			 (try_begin),  # tr3 Sod Twan
				(eq, "$g_sod_deactivate_ai", 0),
				(call_script, "script_party_calculate_siege_or_not_strength", ":kingdom_hero_party", 1),
				(assign, ":kingdom_hero_party_strength", reg0),
				     (try_begin),
					 (party_slot_eq, ":defeated_center", slot_town_lord, ":kingdom_hero"),
					 (val_mul, reg0, 3),
					 (try_end),
				(else_try),      
				(party_get_slot, ":kingdom_hero_party_strength", ":kingdom_hero_party", slot_party_cached_strength), #recently calculated
			 (try_end), # tr3 sod twan end
       

    	(gt, ":kingdom_hero_party_strength", ":best_party_strength"),
        (assign, ":best_party_strength", ":kingdom_hero_party_strength"),
        (assign, ":best_party", ":kingdom_hero_party"),
		(assign, ":best_hero", ":kingdom_hero"),

      (try_end), # end tr2   
      
      (try_end),#tr0 end the try for range
    
      (try_begin), #tr4
        (gt, ":best_party", 0),
        (call_script, "script_party_set_ai_state", ":best_party", spai_holding_center, ":defeated_center"),
		(troop_set_slot, ":best_hero", slot_lord_initiative, -10),  # should make hero guard center at least until lords ai is recalculated
        (party_set_slot, ":best_party", slot_party_commander_party, -1),
        (party_set_flags, ":best_party", pf_default_behavior, 1),
	  (try_end), #tr4   #twan453new end
  ]),
]
