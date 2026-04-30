DIALOGS = [
[anyone|auto_proceed, "lord_leave", [],
   "We will meet again.", "close_window", [(eq, "$talk_context", tc_party_encounter), (assign, "$g_leave_encounter", 1)]],
]
