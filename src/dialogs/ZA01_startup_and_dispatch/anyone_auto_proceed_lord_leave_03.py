DIALOGS = [
[anyone|auto_proceed, "lord_leave", [(ge, "$g_talk_troop_faction_relation", 0)],
   "Yes, yes. Farewell.", "close_window", [(eq, "$talk_context", tc_party_encounter), (assign, "$g_leave_encounter", 1)]],
]
