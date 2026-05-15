DIALOGS = [
[party_tpl|pt_sacrificed_messenger, "start", [
   (check_quest_active, "qst_incriminate_loyal_commander"),
   (neg|check_quest_concluded, "qst_incriminate_loyal_commander"),
   (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
   (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_target_party, "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
],
   "I am still carrying the letter. If I stop now, questions will follow.", "close_window", [(assign, "$g_leave_encounter", 1)]],
]
