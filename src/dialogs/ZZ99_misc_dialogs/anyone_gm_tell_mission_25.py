DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_slavers_escort_merchant_caravan")],
   "I hate to confess, but we could use some help delivering some human cattle to {s8}, cos' we lack the manpower for a proper escorting band for reasons beyond my authority. Take your own gang for the job and lead the rabble to their destination.  If they try to flee, feel free to discipline them a bit, just make sure they arrive in one piece.  Of course, you'll get paid for the effort.  Can you handle it?", "slavers_escort_merchant_caravan_quest_brief",
   [(quest_get_slot, reg8, "qst_slavers_escort_merchant_caravan", slot_quest_gold_reward),
    (quest_get_slot, reg4, "qst_slavers_escort_merchant_caravan", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_center", "qst_slavers_escort_merchant_caravan", slot_quest_target_center),
    (str_store_party_name, s8, ":quest_target_center"),
   ]],
]
