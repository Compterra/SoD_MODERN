DIALOGS = [
[anyone|plyr, "lord_talk", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active, "qst_lend_companion"),
                            (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                            (store_current_day, ":cur_day"),
                            (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                            (ge, ":cur_day", ":quest_target_amount"),
                            (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
                            (call_script, "script_store_troop_name", s14, ":quest_target_troop"),
                            (troop_get_type, reg3, ":quest_target_troop"),
                            ],
   "I should like {s14} returned to me, {s65}, if you no longer require {reg3?her:his} services.", "lord_lend_companion_end",
   []],
]
