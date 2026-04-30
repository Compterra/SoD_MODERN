DIALOGS = [
[anyone|plyr, "merchant_quest_brief_deliver_wine", [(store_free_inventory_capacity, ":capacity"),
                                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                                     (ge, ":capacity", ":quest_target_amount"),
                                                     ],
      "Alright. I will make the delivery.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (troop_add_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
    (call_script, "script_start_quest", "qst_deliver_wine", "$g_talk_troop"),
    ]],
]
