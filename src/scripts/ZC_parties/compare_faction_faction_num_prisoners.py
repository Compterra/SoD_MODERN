SCRIPTS = [
("compare_faction_faction_num_prisoners",

    [ (store_script_param_1, ":faction_1"),
      (store_script_param_2, ":faction_2"),

      (assign, ":result", 0),
      
      (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
      (troop_slot_ge, ":kingdom_hero", slot_troop_prisoner_of_party, 0),
      
      (troop_get_slot, ":prisoner_of", ":kingdom_hero", slot_troop_prisoner_of_party),
      (store_troop_faction, ":hero_faction", ":kingdom_hero"),
      (store_faction_of_party, ":keeper_faction", ":prisoner_of"),

      (try_begin),
	  (eq, ":keeper_faction", ":faction_1"),
	  (faction_slot_eq, ":faction_2", slot_faction_leader, ":kingdom_hero"),
	  (val_add, ":result", 5),
	  (else_try),
	  (eq, ":keeper_faction", ":faction_2"),
	  (faction_slot_eq, ":faction_1", slot_faction_leader, ":kingdom_hero"),
	  (val_add, ":result", -5),
	  (else_try),	  
      (eq, ":hero_faction", ":faction_2"),
      (eq, ":keeper_faction", ":faction_1"),
      (val_add, ":result", 1),
      (else_try),
      (eq, ":hero_faction", ":faction_1"),
      (eq, ":keeper_faction", ":faction_2"),
      (val_add, ":result", -1),
      (try_end),

      (try_end),
      
      (assign, reg0, ":result"),
      
]),
]
