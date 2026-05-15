DIALOGS = [
[anyone|plyr, "militia_awaiting_ransom_b2", [(store_troop_gold, ":cur_gold", "trp_player"),
                                               (check_quest_active, "qst_serpent_host_free_spy"),
                                               (neg|check_quest_concluded, "qst_serpent_host_free_spy"),
                                               (quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party"),
                                               (party_is_active, "$g_encountered_party"),
                                               (quest_get_slot, ":quest_target_amount", "qst_serpent_host_free_spy", slot_quest_target_amount),
                                               (ge, ":cur_gold", ":quest_target_amount")],
   "All right. Here's your money. Let the spy go now.", "militia_awaiting_ransom_pay", []],
]
