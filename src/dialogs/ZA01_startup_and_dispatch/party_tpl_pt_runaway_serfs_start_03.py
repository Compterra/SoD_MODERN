DIALOGS = [
[party_tpl|pt_runaway_serfs, "start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 0),
                                        (get_party_ai_object, ":cur_ai_object"),
                                        (quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (neq, ":home_center", ":cur_ai_object")],
   "Good day {sir/madam}. We were heading back to {s5}, but I am afraid we lost our way.", "runaway_serf_talk_caught", []],
]
