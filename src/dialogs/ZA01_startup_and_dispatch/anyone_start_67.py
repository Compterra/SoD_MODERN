DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                     (le, "$talk_context", tc_siege_commander),
                     ],
   "Well, {playername}...", "lord_start",
   []],
]
