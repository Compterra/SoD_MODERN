DIALOGS = [
[party_tpl|pt_bandits_awaiting_ransom|plyr, "bandits_awaiting_ransom_intro_1", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 1),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
   (party_count_prisoners_of_type, ":girl_prisoners", "$g_encountered_party", "trp_kidnapped_girl"),
   (gt, ":girl_prisoners", 0),
   (store_troop_gold, ":cur_gold", "trp_player"),
   (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
   (ge, ":cur_gold", ":quest_target_amount")
],
   "Here is the ransom. Release her now.", "bandits_awaiting_ransom_pay", []],
]
