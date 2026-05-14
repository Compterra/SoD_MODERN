DIALOGS = [
[anyone, "lord_give_order_answer_2",
   [
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (party_slot_eq, ":party_no", slot_party_ai_state, "$temp"),
     (party_slot_eq, ":party_no", slot_party_ai_object, "$temp_2"),
     (assign, "$g_leave_encounter", 1),
     ],
   "Then it is done. My men move at once.", "close_window",
   []],
]
