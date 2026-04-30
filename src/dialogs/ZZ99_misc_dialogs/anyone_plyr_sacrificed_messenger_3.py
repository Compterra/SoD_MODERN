DIALOGS = [
[anyone|plyr, "sacrificed_messenger_3", [],
   "Good. I will not forget your service. You will be rewarded when you return.", "close_window", [(party_remove_members, "p_main_party", "$g_talk_troop", 1),
                                     (set_spawn_radius, 0),
                                     (spawn_around_party, "p_main_party", "pt_sacrificed_messenger"),
                                     (assign, ":new_party", reg0),
                                     (party_add_members, ":new_party", "$g_talk_troop", 1),
                                     (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
                                     (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                     (party_set_ai_object, ":new_party", ":quest_target_center"),
                                     (party_set_flags, ":new_party", pf_default_behavior, 0),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, ":new_party")]],
]
