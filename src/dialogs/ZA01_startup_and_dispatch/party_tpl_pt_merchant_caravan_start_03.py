DIALOGS = [
[party_tpl|pt_merchant_caravan, "start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 0),
                                           ],
   "Greetings. You must be our escort, right?", "merchant_caravan_intro_1", [(quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 1), ]],
]
