DIALOGS = [
[anyone|plyr, "lord_talk", [(le, "$talk_context", tc_party_encounter),
                             (ge, "$g_talk_troop_faction_relation", 0),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
                             (eq, "$player_has_homage", 1),
                            ],
   "{s66}, I wish to be released from my oath to you.", "lord_ask_leave_service", []],
]
