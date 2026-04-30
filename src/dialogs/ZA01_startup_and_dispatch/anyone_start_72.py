DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
                     (eq, "$g_talk_troop_met", 0),
                     (le, "$talk_context", tc_siege_commander),
                     ],
   "I say, you don't look familiar...", "lady_premeet", []],
]
