DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", 10),
                     (le, "$talk_context", tc_siege_commander),
                     ],
   "Good to see you again {playername}...", "lord_start", []],
]
