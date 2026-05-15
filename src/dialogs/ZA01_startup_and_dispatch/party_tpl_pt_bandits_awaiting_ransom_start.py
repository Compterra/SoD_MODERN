DIALOGS = [
[party_tpl|pt_bandits_awaiting_ransom, "start", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 0),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
   (party_count_prisoners_of_type, ":girl_prisoners", "$g_encountered_party", "trp_kidnapped_girl"),
   (gt, ":girl_prisoners", 0),
],
   "You brought the ransom? Hand it over, and quickly.", "bandits_awaiting_ransom_intro_1", [(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 1), ]],
]
