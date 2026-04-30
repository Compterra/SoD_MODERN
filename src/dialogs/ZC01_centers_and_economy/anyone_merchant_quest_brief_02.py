DIALOGS = [
[anyone, "merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_deliver_wine")],
   "I have a cargo of {s6} that needs to be delivered to the tavern in {s4}.\
 If you can take {reg5} units of {s6} to {s4} in 7 days, you may earn {reg8} denars.\
 What do you say?", "merchant_quest_brief_deliver_wine",
   [(quest_get_slot, reg5, "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, reg8, "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_center", "qst_deliver_wine", slot_quest_target_center),
    (call_script, "script_store_troop_name", s9, "$g_talk_troop"),
    (str_store_party_name_link, s3, "$g_encountered_party"),
    (str_store_party_name_link, s4, ":quest_target_center"),
    (str_store_item_name, s6, ":quest_target_item"),
    (setup_quest_text, "qst_deliver_wine"),
    (str_store_string, s2, "@{s9} of {s3} asked you to deliver {reg5} units of {s6} to the tavern in {s4} within 7 days."),
    #s2 should not be changed until the decision is made
   ]],
]
