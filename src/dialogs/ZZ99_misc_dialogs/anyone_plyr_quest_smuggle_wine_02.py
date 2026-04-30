DIALOGS = [
[anyone|plyr, "quest_smuggle_wine", [
									 (quest_get_slot, ":quest_target_amount", "qst_slavers_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", "itm_wine"),
                                     (lt, ":item_count", ":quest_target_amount"),
                                     (gt, ":item_count", 0),
                                     (assign, reg9, ":quest_target_amount"),
                                     ],
   "I lost some of the cargo on the way.", "tavernkeeper_smuggle_wine_incomplete", []],
]
