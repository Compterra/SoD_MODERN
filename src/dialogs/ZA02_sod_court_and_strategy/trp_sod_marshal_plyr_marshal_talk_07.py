DIALOGS = [
[trp_sod_marshal|plyr, "marshal_talk", [
	(faction_slot_eq, "fac_player_supporters_faction", slot_faction_marshall, 0),
	(assign, ":lord_count", 0),
	(try_for_range, ":cur_lord", kingdom_heroes_begin, kingdom_heroes_end),
		(store_troop_faction, ":trp_fac", ":cur_lord"),
		(eq, ":trp_fac", "fac_player_supporters_faction"),
        (troop_slot_eq, ":cur_lord", slot_troop_occupation, slto_kingdom_hero),
		(val_add, ":lord_count", 1),
	(try_end),
	(gt, ":lord_count", 3),
  ], "I wish to select a new Field Marshall.", "marshal_field_marshall1", []],
]
