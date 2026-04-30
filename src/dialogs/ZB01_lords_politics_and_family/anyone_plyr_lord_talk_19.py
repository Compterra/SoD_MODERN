DIALOGS = [
[anyone|plyr, "lord_talk", [(le, "$talk_context", tc_party_encounter),
                             (ge, "$g_talk_troop_faction_relation", 0),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (neq, "$players_kingdom", "$g_talk_troop_faction"),
                             (store_partner_quest, ":lords_quest"),
                             (neq, ":lords_quest", "qst_join_faction"),
                            ],
   "{s66}, I have come to offer you my sword in vassalage!", "lord_ask_enter_service", []],
]
