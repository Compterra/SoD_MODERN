DIALOGS = [
[anyone, "spy_wait", [], "Do not leave me here long. Sukbathar needs my report.", "close_window",
   [(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
    (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
    (quest_set_slot, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party"),
    (quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1),
    (assign, "$g_leave_encounter", 1)]],
]
