DIALOGS = [
[anyone|plyr, "kidnapped_girl_quest_brief", [],
      "Alright. I will take the ransom money to the bandits and bring back the girl.",
   "kidnapped_girl_quest_taken", [(set_spawn_radius, 4),
                                 (quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                 (spawn_around_party, ":quest_target_center", "pt_bandits_awaiting_ransom"),
                                 (assign, ":quest_target_party", reg0),
                                 (quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":quest_target_party"),
                                 (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                                 (party_set_ai_object, ":quest_target_party", "p_main_party"),
                                 (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                                 (call_script, "script_troop_add_gold", "trp_player", ":quest_target_amount"),
                                 (assign, reg12, ":quest_target_amount"),
                                 (call_script, "script_store_troop_name", s1, "$g_talk_troop"),
                                 (str_store_party_name_link, s4, "$g_encountered_party"),
                                 (str_store_party_name_link, s3, ":quest_target_center"),
                                 (setup_quest_text, "qst_kidnapped_girl"),
                                 (str_store_string, s2, "@Guildmaster of {s4} gave you {reg12} denars to pay the ransom of a girl kidnapped by bandits.\
 You are to meet the bandits near {s3} and pay them the ransom fee.\
 After that you are to bring the girl back to {s4}."),
                                 (call_script, "script_start_quest", "qst_kidnapped_girl", "$g_talk_troop"),
                                 ]],
]
