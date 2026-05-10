DIALOGS = [
[anyone, "lord_tell_objective",
   [
     (assign, ":pass", 0),
     (try_begin),
       (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_undefined),
       (assign, ":pass", 1),
     (else_try),
       (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
       (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
       (neg|party_is_active, ":ai_object"),
       (assign, ":pass", 1),
     (try_end),
     (eq, ":pass", 1),
     ],
   "We are reading the map again. Sometimes the wisest order is the one you do not give too early.", "lord_pretalk", []],
]
