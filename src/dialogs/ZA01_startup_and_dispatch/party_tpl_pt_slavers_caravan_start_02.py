DIALOGS = [
[party_tpl|pt_slavers_caravan, "start", [(quest_get_slot, ":quest_target_party", "qst_slavers_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           ],
   "Eh. We've made it this far... What do you want us to do?", "slavers_escort_merchant_caravan_talk", []],
]
