DIALOGS = [
[anyone, "kidnapped_girl_join", [], "Thank you. I will stay close.",
   "close_window", [(party_join),
                   (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   (assign, "$g_leave_encounter", 1)]],
]
