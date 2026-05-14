DIALOGS = [
[party_tpl|pt_merchant_caravan, "start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           ],
   "We have made it this far with axles whole, cargo dry, and every toll written down twice. Say the word, and we will keep to your lead.", "escort_merchant_caravan_talk", []],
]
