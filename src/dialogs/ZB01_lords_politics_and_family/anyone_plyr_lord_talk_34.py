DIALOGS = [
[anyone|plyr, "lord_talk", [(eq, "$cheat_mode", 1),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             ],
   "CHEAT: suggest a course of action.", "lord_suggest_action_ask", []],
]
