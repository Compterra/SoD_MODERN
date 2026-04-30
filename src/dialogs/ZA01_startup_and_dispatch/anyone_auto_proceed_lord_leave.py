DIALOGS = [
[anyone|auto_proceed, "lord_leave", [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop")],
   "Of course, {playername}. Farewell.", "close_window", [(eq, "$talk_context", tc_party_encounter), (assign, "$g_leave_encounter", 1)]],
]
