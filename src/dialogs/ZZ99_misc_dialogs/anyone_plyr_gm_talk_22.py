DIALOGS = [
[anyone|plyr, "gm_talk", [
	(neq, "$g_talk_troop", slavers_guild_master),
	(faction_slot_eq, "$g_talk_troop_faction", slot_faction_upgrade_permission, 0),
	(neq, "$g_rep", "$g_talk_troop"),
	], "Give me leave to promote your guild soldiers in my own ranks.", "gm_promote",[]],
]
