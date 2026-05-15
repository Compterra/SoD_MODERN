DIALOGS = [
[anyone|plyr, "bandits_awaiting_ransom_intro_1", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 1),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
],
   "Show me the girl first.", "bandits_awaiting_ransom_b", []],
]
