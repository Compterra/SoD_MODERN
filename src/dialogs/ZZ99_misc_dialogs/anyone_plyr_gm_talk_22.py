DIALOGS = [
[anyone|plyr, "gm_talk", [
	(neq, "$g_talk_troop", slavers_guild_master),
	(faction_slot_eq, "$g_talk_troop_faction", slot_faction_upgrade_permission, 0),
	(neq, "$g_rep", "$g_talk_troop"),
	], "Can you give me permission to promote soldiers from your guild?", "gm_promote",[]],
]
