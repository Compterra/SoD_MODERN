DIALOGS = [
[party_tpl|pt_runaway_serfs, "start", [(party_slot_eq, "$g_encountered_party", slot_town_center, 0)], #slot_town_center is used for first time meeting
   "Good day {sir/madam}.", "runaway_serf_intro_1",
   [(party_set_slot, "$g_encountered_party", slot_town_center, 1)]],
]
