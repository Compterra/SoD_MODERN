DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                    ],
   "What do you want? We paid our toll to you less than three days ago.", "merchant_talk", []],
]
