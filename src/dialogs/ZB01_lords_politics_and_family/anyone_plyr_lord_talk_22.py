DIALOGS = [
[anyone|plyr, "lord_talk", [(eq, 1, 0), (le, "$talk_context", tc_party_encounter), (ge, "$g_talk_troop_faction_relation", 0)],
   "I have an offer for you.", "lord_talk_preoffer", []],
]
