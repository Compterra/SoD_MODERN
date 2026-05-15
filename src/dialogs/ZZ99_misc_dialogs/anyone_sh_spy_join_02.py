DIALOGS = [
[anyone, "sh_spy_join", [], "Good. I will keep up.",
   "close_window", [(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1),
                    (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1),
                    (assign, "$g_leave_encounter", 1),
                    (party_join),]],
]
