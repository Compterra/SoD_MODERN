DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt, "$g_encountered_party_relation", 0),
                    (eq, "$g_encountered_party_faction", "fac_merchants"),
                    ],
   "Keep your hands where my drivers can see them. We are merchants, not soldiers, and this road has taken enough from us already.", "merchant_talk", []],
]
