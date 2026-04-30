DIALOGS = [
[anyone, "start", [
		(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
		(faction_get_slot, ":rep", "$g_talk_troop_faction", slot_guild_representative),
		(faction_get_slot, ":gm", "$g_talk_troop_faction", slot_guild_master),
		(this_or_next|eq, ":rep", "$g_talk_troop"),
		(eq, ":gm", "$g_talk_troop"),
        (talk_info_show, 1),
		(call_script, "script_setup_talk_info"),
		(eq, 1, 0), ], "setup talk info", "close_window", [], ],
]
