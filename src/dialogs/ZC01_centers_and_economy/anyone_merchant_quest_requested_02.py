DIALOGS = [
[anyone, "merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_deliver_wine"), ], "You're looking for a job?\
 Actually I was looking for someone to deliver some {s4}.\
 Perhaps you can do that...", "merchant_quest_brief",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (str_store_item_name, s4, ":quest_target_item"),
    ]],
]
