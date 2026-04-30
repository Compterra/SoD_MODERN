DIALOGS = [
[party_tpl|pt_runaway_slaves, "start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 0),
                                        (get_party_ai_behavior, ":cur_ai_bhvr"),
                                        (neq, ":cur_ai_bhvr", ai_bhvr_travel_to_party)],
   "Good day {sir/madam}. We were heading back to {s5}, but I am afraid we lost our way.", "runaway_slave_talk_caught", []],
]
