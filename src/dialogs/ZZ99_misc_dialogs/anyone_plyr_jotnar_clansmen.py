DIALOGS = [
[anyone|plyr, "jotnar_clansmen", [],
   "Yes, she sent me. Now I'll escort you to your base.", "close_window", [(assign, "$g_leave_encounter", 1),
   (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
   (party_set_ai_object, "$g_encountered_party", "p_main_party"),
   ]],
]
