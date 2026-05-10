DIALOGS = [
[anyone, "lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center),
                                  (party_get_attached_to, ":cur_center_no", "$g_talk_troop_party"),
                                  (try_begin),
                                    (lt, ":cur_center_no", 0),
                                    (party_get_cur_town, ":cur_center_no", "$g_talk_troop_party"),
                                  (try_end),
                                  (is_between, ":cur_center_no", centers_begin, centers_end),
                                  ],
   "We are resting at {s1}. Men mend faster near walls, and horses remember kindness better than soldiers do.", "lord_pretalk", [(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                              (str_store_party_name, s1, ":ai_object")]],
]
