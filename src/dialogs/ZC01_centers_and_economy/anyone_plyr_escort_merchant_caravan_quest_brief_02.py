DIALOGS = [
[anyone|plyr, "escort_merchant_caravan_quest_brief", [(party_get_num_companions, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (lt, ":party_size", ":quest_target_amount"), ],
   "I am afraid I don't have that many soldiers with me.", "merchant_quest_stall", []],
]
