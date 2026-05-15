DIALOGS = [
[party_tpl|pt_bandits_awaiting_ransom, "start", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_slot_ge, "qst_kidnapped_girl", slot_quest_current_state, 2),
   (party_is_active, "$g_encountered_party"),
],
   "We are done. Take your road before we change our minds.", "bandits_awaiting_remeet", []],
]
