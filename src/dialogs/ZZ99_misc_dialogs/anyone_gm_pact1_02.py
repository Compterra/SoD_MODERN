DIALOGS = [
[anyone, "gm_pact1",[
	(assign, ":has_debt", 0),
	(try_for_range, ":merc_guild", "fac_sod_merc_guild1", "fac_player_faction"),
		(eq, ":has_debt", 0),
		(faction_get_slot, ":debt", ":merc_guild", player_debt_to_faction),
		(gt, ":debt", 0),
		(assign, ":has_debt", 1),
	(try_end),
	(neq, ":has_debt", 0),
	], "I have heard that you didn't pay one of the guilds for they work, we don't want an insolvent employer.", "gm_pretalk",[]],
]
