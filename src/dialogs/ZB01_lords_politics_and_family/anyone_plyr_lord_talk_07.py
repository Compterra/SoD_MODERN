DIALOGS = [
[anyone|plyr, "lord_talk", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active, "qst_duel_for_lady"),
                            (neg|check_quest_concluded, "qst_duel_for_lady"),
                            (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_giver_troop", "qst_duel_for_lady", slot_quest_giver_troop),
                            (call_script, "script_store_troop_name", 1, ":quest_giver_troop")],
   "I want you to take back your accusations against {s1}.", "lord_challenge_duel_for_lady", []],
]
