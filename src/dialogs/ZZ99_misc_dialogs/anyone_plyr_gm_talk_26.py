DIALOGS = [
[anyone|plyr, "gm_talk", [
   (neq, "$g_rep", "$g_talk_troop"),
   (ge, "$g_talk_troop_faction_relation", 30),
   ], "Trusted partners usually keep better doors open. What special service can you offer?", "gm_master_service",[]],
]
