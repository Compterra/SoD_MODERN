DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (gt, "$g_encountered_party", 0),
                    (party_is_active, "$g_encountered_party"),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                    ],
   "Easy now. Your toll was paid less than three days ago, and the ink is barely dry in our ledger. If you want more than silver, speak plainly.", "merchant_talk", []],
]
