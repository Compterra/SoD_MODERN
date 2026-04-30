DIALOGS = [
[anyone|plyr, "quest_smuggle_wine", [
                                     (store_item_kind_count, ":item_count", "itm_wine"),
                                     (eq, ":item_count", 0),
                                     (quest_get_slot, reg9, "qst_slavers_deliver_wine", slot_quest_target_amount),
                                     ],
   "I lost the cargo on the way.", "tavernkeeper_smuggle_wine_lost", []],
]
