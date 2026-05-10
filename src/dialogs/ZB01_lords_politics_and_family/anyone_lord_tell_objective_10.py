DIALOGS = [
[anyone, "lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
                                  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                  (party_is_active, ":ai_object"),
                                  ],
   "We are moving against {s1}. If steel must answer, I mean for ours to speak first.", "lord_pretalk",
   [
     (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
     (str_store_party_name, s1, ":ai_object")
     ]],
]
