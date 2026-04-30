DIALOGS = [
[anyone, "tavernkeeper_deliver_wine_lost", [], "What? I was waiting for that {s4} for weeks! And now you are telling me that you lost it? You may rest assured that I will let {s1} know about this.", "tavernkeeper_pretalk",
   [(add_xp_as_reward, 40),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (str_store_item_name, s4, ":quest_target_item"),
    (call_script, "script_store_troop_name", s1, ":quest_giver_troop"),
    (val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
    (call_script, "script_end_quest", "qst_deliver_wine"),
   ]],
]
