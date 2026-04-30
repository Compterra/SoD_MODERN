SCRIPTS = [
("calculate_average_lord_wealth",
  [ 
     (assign, ":num_heroes", 0),
     (assign, ":total_wealth", 0),
    
    (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
	(store_troop_faction, ":hero_fac", ":kingdom_hero"),
	(try_begin),
	(faction_slot_eq, ":hero_fac", slot_faction_state, sfs_active),
	(is_between, ":hero_fac", kingdoms_begin, kingdoms_end),
    (val_add, ":num_heroes", 1),
    (troop_get_slot, ":wealth", ":kingdom_hero", slot_troop_wealth),
    (val_add, ":total_wealth", ":wealth"),
	(try_end),
    (try_end),

    (try_begin),
    (gt, ":num_heroes", 0),
    (store_div, "$g_average_lord_wealth", ":total_wealth", ":num_heroes"),
    (else_try),
    (assign, "$g_average_lord_wealth", 0),
    (try_end),
    (val_max, "$g_average_lord_wealth", 1),
	
	(try_begin),
	(eq, "$g_sod_debug", 1),
	(assign, reg0, "$g_average_lord_wealth"),
	(display_log_message, "@Average lords wealth {reg0}", debug_color), # debug
    (try_end), 
 ]),
]
