DIALOGS = [
[anyone, "kidnapped_girl_join", [], "Oh, thank you so much!",
   "close_window", [(party_join),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   (assign, "$g_leave_encounter", 1)]],
]
