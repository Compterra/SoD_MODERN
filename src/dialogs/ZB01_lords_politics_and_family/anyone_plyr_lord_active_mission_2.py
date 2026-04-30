DIALOGS = [
[anyone|plyr, "lord_active_mission_2", [
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active, "qst_capture_prisoners"),
                            (quest_slot_eq, "qst_capture_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
                            (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
                            (party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop"),
                            (ge, ":count_prisoners", ":quest_target_amount"),
                            (assign, reg1, ":quest_target_amount"),
                            (str_store_troop_name_plural, s1, ":quest_target_troop")],
   "Indeed. I brought you {reg1} {s1} as prisoners.", "lord_generic_mission_thank",
   [(quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
    (party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
    (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", ":quest_target_amount"),
    (call_script, "script_finish_quest", "qst_capture_prisoners", 100)]],
]
