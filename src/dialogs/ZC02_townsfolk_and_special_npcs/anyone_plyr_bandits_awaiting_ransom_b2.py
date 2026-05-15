DIALOGS = [
[anyone|plyr, "bandits_awaiting_ransom_b2", [
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
   "Fine. Take the ransom and let her go.", "bandits_awaiting_ransom_pay", []],
]
