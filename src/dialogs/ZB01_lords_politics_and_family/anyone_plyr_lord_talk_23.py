DIALOGS = [
[anyone|plyr, "lord_talk", [(eq, "$g_talk_troop_faction", "fac_player_supporters_faction"),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             ],
   "Take some of my troops into your command.", "lord_give_troops", []],
]
