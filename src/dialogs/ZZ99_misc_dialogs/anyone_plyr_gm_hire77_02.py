DIALOGS = [
[anyone|plyr, "gm_hire77", [
	(this_or_next|eq, "$g_talk_troop", black_army_guild_master),
	(eq, "$g_talk_troop", black_army_rep),
   ],"Yes, I want cavalry.", "gm_hire8", [
   (assign, "$temp_proportion", 1),]],
]
