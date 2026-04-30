DIALOGS = [
[anyone|auto_proceed, "lord_leave", [(ge, "$g_talk_troop_relation", 10)],
   "Good journeys to you, {playername}.", "close_window", [(eq, "$talk_context", tc_party_encounter), (assign, "$g_leave_encounter", 1)]],
]
