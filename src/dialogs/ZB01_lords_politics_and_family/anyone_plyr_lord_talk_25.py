DIALOGS = [
[anyone|plyr, "lord_talk",
   [
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     (eq, "$g_sod_king"),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     ],
   "I have a new task for you.", "lord_give_order_ask", []],
]
