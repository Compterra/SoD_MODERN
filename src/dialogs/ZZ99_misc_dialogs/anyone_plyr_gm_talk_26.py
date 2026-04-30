DIALOGS = [
[anyone|plyr, "gm_talk", [
   (neq, "$g_rep", "$g_talk_troop"),
   (ge, "$g_talk_troop_faction_relation", 30),
   ], "I want to discuss a special service for trusted partners.", "gm_master_service",[]],
]
