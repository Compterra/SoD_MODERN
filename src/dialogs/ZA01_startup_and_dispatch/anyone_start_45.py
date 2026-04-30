DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
   ],
   "Yes?", "companion_recruit_secondchance", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1),
       ]],
]
