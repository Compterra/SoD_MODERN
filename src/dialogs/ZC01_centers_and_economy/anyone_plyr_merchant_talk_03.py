DIALOGS = [
[anyone|plyr, "merchant_talk", [(eq, "$talk_context", tc_party_encounter), #TODO: For the moment don't let attacking if merchant has paid toll.
                                 (neg|party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                                 ], "I demand something from you!", "merchant_demand", []],
]
