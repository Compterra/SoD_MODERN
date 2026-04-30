DIALOGS = [
[anyone , "start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (assign, "$pretender_told_story", 0),
     (eq, "$g_talk_troop_met", 0),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     ],
   "Do I know you?.", "pretender_intro_1", []],
]
