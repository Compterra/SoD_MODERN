DIALOGS = [
[anyone|plyr, "gm_talk", [
   (str_store_faction_name, s1, "$g_talk_troop_faction"),
   (neq, "$g_rep", "$g_talk_troop"),
   ], "How did {s1} become the company standing before me?", "gm_guild_history",[]],
]
