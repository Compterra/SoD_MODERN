DIALOGS = [
[anyone, "sh_spy_join", [(neg|party_can_join)], "There is no room for me in your company. Make space, or tell me where to hide.",
   "close_window", [(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
                    (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
                    (quest_set_slot, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party"),
                    (quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1),
                    (assign, "$g_leave_encounter", 1)]],
]
