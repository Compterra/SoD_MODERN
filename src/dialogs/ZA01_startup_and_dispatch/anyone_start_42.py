DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 1),
   ],
   "Please do not waste any more of my time today, {sir/madame}. Perhaps we shall meet again in our travels.", "close_window", [
       ]],
]
