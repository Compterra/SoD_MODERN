DIALOGS = [
[anyone|plyr, "gm_talk", [
	(faction_get_slot, ":mercenaries", "fac_player_faction", slot_faction_merc_pact),
	(eq, ":mercenaries", "$g_talk_troop_faction"),
	# (neq, "$g_rep", "$g_talk_troop"),
	], "Our pact has run its course. I mean to end it cleanly.", "gm_pact_cancel1",[]],
]
