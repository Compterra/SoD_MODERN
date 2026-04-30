DIALOGS = [
[anyone|plyr, "quest_smuggle_wine", [
                                     (quest_get_slot, ":quest_target_amount", "qst_slavers_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", "itm_wine"),
                                     (ge, ":item_count", ":quest_target_amount"),
                                     (assign, reg9, ":quest_target_amount"),
                                     ],
   "{reg9} units of wine, here they are.", "tavernkeeper_smuggle_wine", []],
]
