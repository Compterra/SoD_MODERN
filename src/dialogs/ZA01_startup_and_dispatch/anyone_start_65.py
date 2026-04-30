DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (ge, "$g_talk_troop_faction_relation", 0),
                     (le, "$talk_context", tc_siege_commander),
                     ],
   "Do I know you?", "lord_meet_neutral", []],
]
