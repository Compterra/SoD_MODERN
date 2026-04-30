DIALOGS = [
[anyone|plyr, "lord_talk", [(troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (check_quest_active, "qst_rescue_lord_by_replace"),
                             (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, "$g_talk_troop"),
                             (neg|check_quest_succeeded, "qst_rescue_lord_by_replace")],
   "Fear not, I am here to rescue you.", "lord_rescue_by_replace_offer", []],
]
