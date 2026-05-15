DIALOGS = [
[anyone|plyr, "gm_talk", [
							(store_partner_quest, "$g_lords_quest"),
							(eq, "$g_lords_quest", "qst_bc_capture_prisoners"),
                            (check_quest_active, "qst_bc_capture_prisoners"),
                            (quest_slot_eq, "qst_bc_capture_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_bc_capture_prisoners", slot_quest_target_amount),
                            (quest_get_slot, ":quest_target_troop", "qst_bc_capture_prisoners", slot_quest_target_troop),
                            (party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop"),
                            (ge, ":count_prisoners", ":quest_target_amount"),
                            (assign, reg1, ":quest_target_amount"),
                            (str_store_troop_name_plural, s1, ":quest_target_troop")],
   "I brought you {reg1} {s1} as prisoners.", "gm_qst_bc_capture_prisoners",
   []],
]
