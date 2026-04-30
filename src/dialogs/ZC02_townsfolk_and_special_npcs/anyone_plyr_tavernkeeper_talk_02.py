DIALOGS = [
[anyone|plyr, "tavernkeeper_talk", [(check_quest_active, "qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (lt, ":item_count", ":quest_target_amount"),
                                     (gt, ":item_count", 0),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost some of the cargo on the way.", "tavernkeeper_deliver_wine_incomplete", []],
]
