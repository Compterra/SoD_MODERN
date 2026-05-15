DIALOGS = [
[anyone, "bandits_awaiting_ransom_b", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 1),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
],
   "You saw enough. Now pay, or we settle this another way.", "bandits_awaiting_ransom_b2", []],
]
