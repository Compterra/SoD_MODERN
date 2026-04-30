DIALOGS = [
[anyone, "lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center)],
   "We are laying waste to the village of {s1}.", "lord_pretalk", [(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],
]
