DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter), (eq, "$g_encountered_party_type", spt_kingdom_caravan), (ge, "$g_encountered_party_relation", 0)],
   "Hail, friend.", "merchant_talk", []],
]
