DIALOGS = [
[anyone|auto_proceed, "lady_leave", [], "Farewell, {playername}.", "close_window", [(eq, "$talk_context", tc_party_encounter), (assign, "$g_leave_encounter", 1)]],
]
