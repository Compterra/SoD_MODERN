DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt, "$g_encountered_party_relation", 0),
                    (eq, "$g_encountered_party_faction", "fac_merchants"),
                    ],
   "What do you want? We are but simple merchants, we've no quarrel with you, so leave us alone.", "merchant_talk", []],
]
