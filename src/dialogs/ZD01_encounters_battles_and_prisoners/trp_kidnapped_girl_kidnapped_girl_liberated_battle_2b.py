DIALOGS = [
[trp_kidnapped_girl, "kidnapped_girl_liberated_battle_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!",
   "close_window", [(set_spawn_radius, 1),
                    (spawn_around_party, "p_main_party", "pt_kidnapped_girl"),
                    (assign, ":girl_party", reg0),
                    (party_set_icon, ":girl_party", "icon_woman"),
                    (party_set_ai_behavior, ":girl_party", ai_bhvr_hold),
                    (party_set_flags, ":girl_party", pf_default_behavior, 0),
                    (quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":girl_party"),
                    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2),
                    (assign, "$g_leave_encounter", 1)]],
]
