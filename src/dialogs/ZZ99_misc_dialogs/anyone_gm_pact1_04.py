DIALOGS = [
[anyone, "gm_pact1",[
   (assign, ":is_hired", 0),
   (try_for_range, "$temp_faction", native_kingdoms_begin, native_kingdoms_end),
	(faction_get_slot, ":mercenaries", "$temp_faction", slot_faction_merc_pact),
	(eq, ":mercenaries", "$g_talk_troop_faction"),
	(assign, ":is_hired", 1),
	(try_end),
	(eq, ":is_hired", 1),
	], "We already have an employer, he pays us well, so we're not interested... Unless you want to pay better. Currently we're receiving 500 weekly. What's yours proposition?", "gm_pact_e2",[]],
]
