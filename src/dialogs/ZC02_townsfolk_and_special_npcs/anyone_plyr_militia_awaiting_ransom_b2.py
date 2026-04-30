DIALOGS = [
[anyone|plyr, "militia_awaiting_ransom_b2", [(store_troop_gold, ":cur_gold"),
                                               (quest_get_slot, ":quest_target_amount", "qst_serpent_host_free_spy", slot_quest_target_amount),
                                               (ge, ":cur_gold", ":quest_target_amount")],
   "All right. Here's your money. Let the spy go now.", "militia_awaiting_ransom_pay", []],
]
