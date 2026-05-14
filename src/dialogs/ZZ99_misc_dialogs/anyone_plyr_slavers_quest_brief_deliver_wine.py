DIALOGS = [
[anyone|plyr, "slavers_quest_brief_deliver_wine", [(store_free_inventory_capacity, ":capacity"),
                                                     (quest_get_slot, ":quest_target_amount", "qst_slavers_deliver_wine", slot_quest_target_amount),
                                                     (ge, ":capacity", ":quest_target_amount"),
                                                     ],
      "I will make the delivery. See that the payment is ready.", "gm_pretalk",
   [(quest_get_slot, ":quest_target_amount", "qst_slavers_deliver_wine", slot_quest_target_amount),
    (troop_add_items, "trp_player", "itm_wine", ":quest_target_amount"),
    (call_script, "script_start_quest", "qst_slavers_deliver_wine", "$g_talk_troop"),
    ]],
]
