DIALOGS = [
[anyone, "lord_join_rebellion_suggest_cheat",
   [], "Cheat:Allright.",
   "lord_join_rebellion_ask_for_order",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
     (call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),
     (assign, "$g_leave_encounter", 1),
     ]],
]
