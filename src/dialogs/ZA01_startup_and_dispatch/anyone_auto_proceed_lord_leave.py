DIALOGS = [
[anyone|auto_proceed, "lord_leave", [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop")],
   "Go with my leave, {playername}. Bring back deeds before you bring back more counsel.", "close_window", [(eq, "$talk_context", tc_party_encounter), (assign, "$g_leave_encounter", 1)]],
]
