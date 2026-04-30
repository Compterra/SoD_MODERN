DIALOGS = [
[anyone|plyr, "lord_talk",
   [
     (eq, "$talk_context", tc_party_encounter),
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (party_slot_eq, "$g_encountered_party", slot_party_following_player, 0),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
     ],
   "Will you follow me? I have a plan.", "lord_ask_follow", []],
]
