DIALOGS = [
[anyone, "kidnapped_girl_wait", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",
   [(party_set_icon, "$g_encountered_party", "icon_woman"),
    (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
    (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party"),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2),
    (assign, "$g_leave_encounter", 1)]],
]
