DIALOGS = [
[party_tpl|pt_slavers_caravan, "start", [(quest_get_slot, ":quest_target_party", "qst_slavers_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           ],
   "The coffles are counted, the guards are watching the road, and every delay eats into the price. We have made it this far; what is your next order?", "slavers_escort_merchant_caravan_talk", []],
]
