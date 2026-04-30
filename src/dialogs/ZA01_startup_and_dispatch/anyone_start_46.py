DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
   ],
   "My offer to rejoin you still stands, if you'll have me.", "companion_rehire", []],
]
