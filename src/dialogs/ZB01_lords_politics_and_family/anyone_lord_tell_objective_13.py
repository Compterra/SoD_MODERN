DIALOGS = [
[anyone, "lord_tell_objective", [],
   "I don't know: {reg1} {s1}", "lord_pretalk", [(party_get_slot, reg1, "$g_talk_troop_party", slot_party_ai_state),
                                                (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],
]
