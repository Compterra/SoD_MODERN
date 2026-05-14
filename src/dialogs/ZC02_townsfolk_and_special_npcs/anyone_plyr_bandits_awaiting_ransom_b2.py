DIALOGS = [
[anyone|plyr, "bandits_awaiting_ransom_b2", [(store_troop_gold, ":cur_gold", "trp_player"),
                                               (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                               (ge, ":cur_gold", ":quest_target_amount")],
   "All right. Here's your money. Let the girl go now.", "bandits_awaiting_ransom_pay", []],
]
