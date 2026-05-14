SCRIPTS = [
("get_truce_day",	
	[ (store_script_param_1, ":kingdom_1"),
      (store_script_param_2, ":kingdom_2"),
	  (assign, reg1, 0),
	  (assign, ":truce_slot", faction_truce_slots_begin),
      (val_add, ":truce_slot", ":kingdom_2"),
      (val_sub, ":truce_slot", "fac_player_supporters_faction"),
	  (try_begin),
	    (is_between, ":truce_slot", faction_truce_slots_begin, faction_truce_slots_end),
	    (faction_get_slot, reg1, ":kingdom_1", ":truce_slot"),
	  (try_end),
]),
]
