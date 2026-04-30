DIALOGS = [
[party_tpl|pt_runaway_serfs, "runaway_serf_go_back", [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                                       (str_store_party_name, s5, ":home_center")],
   "All right {sir/madam}. As you wish. We'll head back to {s5} now.", "close_window",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (party_set_ai_object, "$g_encountered_party", ":quest_object_center"),
    (assign, "$g_leave_encounter", 1)]],
]
