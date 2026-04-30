DIALOGS = [
[anyone|plyr, "lord_active_mission_2", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                         (store_partner_quest, ":lords_quest"),
                                         (eq, ":lords_quest", "qst_collect_taxes"),
                                         (check_quest_failed, "qst_collect_taxes"),
                                         (quest_get_slot, ":quest_gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
                                         (store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", ":quest_gold_reward"),
                                         (assign, reg19, ":quest_gold_reward"),
                                         (quest_get_slot, ":quest_target_center", "qst_collect_taxes", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         ],
   "Unfortunately, a revolt broke up while I was collecting the taxes.\
 I could only collect {reg19} denars.", "lord_collect_taxes_fail",
   []],
]
