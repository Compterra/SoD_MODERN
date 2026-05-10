DIALOGS = [
[anyone, "lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_accompanying_army)],
   "We are riding with {s1}. A single banner is proud; several banners together are harder to bury.", "lord_pretalk", [(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                      (str_store_party_name, s1, ":ai_object")]],
]
