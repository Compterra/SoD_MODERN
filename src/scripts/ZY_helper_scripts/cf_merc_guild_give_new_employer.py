SCRIPTS = [
("cf_merc_guild_give_new_employer",
	[
	(store_script_param_1, ":guild_no"),

	(call_script, "script_merc_update_guild_marshal_faction", ":guild_no", "fac_commoners"),

	(store_sub, ":kingdom_count", kingdoms_end, kingdoms_begin),
	(store_random_in_range, ":start_offset", 0, ":kingdom_count"),
	(assign, ":found", 0),
	(try_for_range, ":offset", 0, ":kingdom_count"),
		(eq, ":found", 0),
		(store_add, ":candidate", kingdoms_begin, ":start_offset"),
		(val_add, ":candidate", ":offset"),
		(try_begin),
			(ge, ":candidate", kingdoms_end),
			(val_sub, ":candidate", ":kingdom_count"),
		(try_end),
		(faction_slot_eq, ":candidate", slot_faction_state, sfs_active),
		(faction_slot_eq, ":candidate", slot_faction_merc_pact, 0),
		(faction_set_slot, ":candidate", slot_faction_merc_pact, ":guild_no"),
		(call_script, "script_merc_update_guild_marshal_faction", ":guild_no", ":candidate"),
		(assign, ":found", 1),
	(try_end),

	(eq, ":found", 1),

	]),
]
