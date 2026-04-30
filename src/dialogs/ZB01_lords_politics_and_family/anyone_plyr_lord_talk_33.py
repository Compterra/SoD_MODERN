DIALOGS = [
[anyone|plyr, "lord_talk",
   [
     (eq, "$cheat_mode", 1),
     (gt, "$supported_pretender", 0),
     (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
     ],
   "CHEAT: Join our cause by force.", "lord_join_rebellion_suggest_cheat", []],
]
