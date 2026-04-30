DIALOGS = [
[trp_kidnapped_girl, "kidnapped_girl_liberated_map_2a", [], "Oh really? Thank you so much!",
   "close_window", [(party_join),
                    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                    (assign, "$g_leave_encounter", 1)]],
]
