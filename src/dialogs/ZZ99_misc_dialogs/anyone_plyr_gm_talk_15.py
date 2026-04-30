DIALOGS = [
[anyone|plyr, "gm_talk", [
   (str_store_faction_name, s1, "$g_talk_troop_faction"),
   (neq, "$g_rep", "$g_talk_troop"),
   ], "What is so special about {s1}?", "gm_guild_special",[]],
]
