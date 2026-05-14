DIALOGS = [
[anyone|plyr, "lord_talk", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (ge, "$g_talk_troop_faction_relation", 0),
                             (store_partner_quest, ":lords_quest"),
                             (lt, ":lords_quest", 0),
                             ],
   "What needs doing that you would trust to my hands?", "lord_request_mission_ask", []],
]
