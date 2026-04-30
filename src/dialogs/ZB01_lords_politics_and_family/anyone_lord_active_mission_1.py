DIALOGS = [
[anyone, "lord_active_mission_1", [(store_partner_quest, ":lords_quest"),
                                    (eq, ":lords_quest", "qst_lend_companion"),
                                    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                    (check_quest_active, "qst_lend_companion"),
                                    (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                                    (store_current_day, ":cur_day"),
                                    (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                                    (ge, ":cur_day", ":quest_target_amount"),
                                    ],
   "Oh, you want your companion back? I see...", "lord_lend_companion_end", []],
]
