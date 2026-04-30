DIALOGS = [
[anyone , "start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     ],
   "Greetings, {playername}", "pretender_start", [(assign, "$pretender_told_story", 0)]],
]
