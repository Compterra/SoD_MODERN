DIALOGS = [
[party_tpl|pt_bandits_awaiting_ransom, "start", [(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 0), ],
   "Are you the one that brought the ransom? Quick, give us the money now.", "bandits_awaiting_ransom_intro_1", [(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 1), ]],
]
