DIALOGS = [
[anyone|plyr, "merchant_talk", [(eq, "$talk_context", tc_party_encounter), #TODO: For the moment don't let attacking if merchant has paid toll.
                                 (gt, "$g_encountered_party", 0),
                                 (party_is_active, "$g_encountered_party"),
                                 (neq, "$g_encountered_party_faction", "$players_kingdom"),
                                 (ge, "$g_talk_troop_faction_relation", 0),
                                 (neg|party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                                 ], "You will pay a toll for this road.", "merchant_demand", []],
]
