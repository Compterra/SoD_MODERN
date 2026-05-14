DIALOGS = [
[party_tpl|pt_black_army_caravan, "start", [(quest_get_slot, ":quest_target_party", "qst_black_army_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           ],
   "The wagons are sealed, the ledgers are dry, and the road is still asking questions. Give the word.", "black_army_escort_merchant_caravan_talk", []],
]
