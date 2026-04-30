DIALOGS = [
[party_tpl|pt_merchant_caravan, "start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 2),
                                           ],
   "We can cover the rest of the way ourselves. Thanks.", "close_window", [(assign, "$g_leave_encounter", 1)]],
]
