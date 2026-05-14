DIALOGS = [
[party_tpl|pt_bandits_awaiting_ransom|plyr, "bandits_awaiting_ransom_intro_1", [(store_troop_gold, ":cur_gold", "trp_player"),
                                                                                  (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                                  (ge, ":cur_gold", ":quest_target_amount")
                                                                                  ],
   "Here, take the money. Just set the girl free.", "bandits_awaiting_ransom_pay", []],
]
