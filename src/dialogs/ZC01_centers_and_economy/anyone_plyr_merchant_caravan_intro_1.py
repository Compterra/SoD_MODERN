DIALOGS = [
[anyone|plyr, "merchant_caravan_intro_1", [], "Yes. My name is {playername}. I will lead you to {s1}.",
   "merchant_caravan_intro_2", [(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                               (str_store_party_name, s1, ":quest_target_center"),
                               ]],
]
