DIALOGS = [
[anyone, "merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_escort_merchant_caravan")],
   "I am going to send a caravan of goods to {s8}.\
 However with all those bandits and deserters on the roads, I don't want to send them out without an escort.\
 If you can lead that caravan to {s8} in 15 days, you will earn {reg8} denars.\
 Of course your party needs to be at least {reg4} strong to offer them any protection.", "escort_merchant_caravan_quest_brief",
   [(quest_get_slot, reg8, "qst_escort_merchant_caravan", slot_quest_gold_reward),
    (quest_get_slot, reg4, "qst_escort_merchant_caravan", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (str_store_party_name, s8, ":quest_target_center"),
   ]],
]
