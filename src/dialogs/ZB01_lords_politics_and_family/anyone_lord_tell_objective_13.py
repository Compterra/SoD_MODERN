DIALOGS = [
[anyone, "lord_tell_objective", [],
   "The situation has gone muddy. My scouts report {s1}, but the order beneath it no longer sits cleanly on the map.", "lord_pretalk", [(party_get_slot, reg1, "$g_talk_troop_party", slot_party_ai_state),
                                                (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],
]
