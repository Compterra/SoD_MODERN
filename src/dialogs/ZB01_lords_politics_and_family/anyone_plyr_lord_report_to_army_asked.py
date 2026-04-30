DIALOGS = [
[anyone|plyr, "lord_report_to_army_asked", [(quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
                                             (call_script, "script_party_count_fit_for_battle", "p_main_party"),
                                             (gt, reg0, ":quest_target_amount"), # +1 for player
                                             ],
   "I have a company of good, hardened soldiers with me. We are ready to join you.", "lord_report_to_army_completed",
   []],
]
