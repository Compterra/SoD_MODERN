SCRIPTS = [
( "calculate_badboy_decay",
  [ (assign, ":badboy_decay", 10), #twan456
    (try_for_range, ":center_no", centers_begin, centers_end),
    (store_faction_of_party, ":centerfac", ":center_no"),
    (eq, ":centerfac", "fac_player_supporters_faction"),
    (try_for_range, ":center_slot", 134, 139),
	(party_slot_eq, ":center_no", ":center_slot", 1),
	(val_add, ":badboy_decay", "$g_sod_building_shrine_badboy_decay"),
	(try_end),
	(try_for_range, ":center_slot", 139, 144),
	(party_slot_eq, ":center_no", ":center_slot", 1),
	(val_add, ":badboy_decay", "$g_sod_building_monastery_badboy_decay"),
	(try_end),
	(try_for_range, ":center_slot", 146, 151),
	(party_slot_eq, ":center_no", ":center_slot", 1),
	(val_add, ":badboy_decay", "$g_sod_building_temple_badboy_decay"),
	(try_end),
	(try_for_range, ":center_slot", 151, 156),
	(party_slot_eq, ":center_no", ":center_slot", 1),
	(val_add, ":badboy_decay", "$g_sod_building_chapel_badboy_decay"),
	(try_end),
	(try_begin),
	(party_slot_eq, ":center_no", slot_center_has_university, 1),
	(val_add, ":badboy_decay", "$g_sod_building_university_badboy_decay"),
	(try_end),
	(try_end),
	
	(store_mul, ":difficulty_bonus", "$g_sod_diplomatic_difficulty", -15),
	(val_add, ":badboy_decay", ":difficulty_bonus"),
	
	(try_for_range, ":kingdom_no", "fac_kingdom_1", "fac_kingdom_6"),  # relations effect on decay (effect of negative relations is limited as being at -100 is usual during a war)
	(store_relation, ":rln", ":kingdom_no", "fac_player_supporters_faction"),
	(val_max, ":rln", -40),
	(val_div, ":rln", 10),                                             # -4 to +10 twan new, it's still no more than +2,5 decay with +100 relations with all calradians  
	(val_add, ":badboy_decay", ":rln"),
	(try_end),
	
	(val_add, ":badboy_decay", "$player_honor"),
	(val_div, ":badboy_decay", 20),
	(val_max, ":badboy_decay", 1),
	                                                                                                # kingdom size effect
    (faction_get_slot, ":num_castles", "fac_player_supporters_faction", slot_faction_num_castles),  # help the player to deal with starting badboy
	(faction_get_slot, ":num_armies", "fac_player_supporters_faction", slot_faction_num_armies),
	(faction_get_slot, ":num_towns", "fac_player_supporters_faction", slot_faction_num_towns),
	(try_begin),
	(le, ":num_towns", 1),
	(le, ":num_castles", 1),
	(le, ":num_armies", 2),
	(val_add, ":badboy_decay", 2),
	(else_try),
	(le, ":num_towns", 2),
	(le, ":num_castles", 3),
	(lt, ":num_armies", 3),
	(val_add, ":badboy_decay", 1), 
	(else_try),
	(gt, ":num_towns", 3),             # -1 for 4 towns, -2 for 6, -3 for 8, etc...
	(val_sub, ":num_towns", 2),
    (val_div, ":num_towns", 2),
	(val_sub, ":badboy_decay", ":num_towns"),
	(try_end),
	
	(try_begin),
	(gt, "$g_sod_diplomatic_difficulty", -1),
	(val_clamp, ":badboy_decay", 0, 5),
	(else_try),
	(val_clamp, ":badboy_decay", 1, 7),
	(try_end),
	
	(try_begin),
	(faction_slot_eq, "fac_player_supporters_faction", slot_faction_badboy_rating, 40),
	(assign, ":badboy_decay", 8), # twan456 make badboy decrease to 32 the first week after a badboy war has started
	(try_end),
	
	(assign, reg0, ":badboy_decay"),
	]),
]
