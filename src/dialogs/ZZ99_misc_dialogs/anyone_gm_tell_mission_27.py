DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_black_army_escort_merchant_caravan")],
   "We are preparing to send out a supply caravan to {s8} to reinforce the defenses there. Now, you may wonder, why would we need any help for that? Let me explain, princeling. In this case, not only the material supplies, but the troops sent along matter as well. There's no point in supplies if there is no manpower to use them up, correct? Now, if the caravan has to travel across greater distances, there is a big risk of potential attacks which exhaust and wound many escorting troops and also delay their arrival, while they are supposed to reach their destination within as short time as possible. This is where YOU come in. Ensure a fast and safe travel for the boys, and expect your reward as soon as they reach their destination. Understood?", "black_army_escort_merchant_caravan_quest_brief",
   [(quest_get_slot, reg8, "qst_black_army_escort_merchant_caravan", slot_quest_gold_reward),
    (quest_get_slot, reg4, "qst_black_army_escort_merchant_caravan", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_center", "qst_black_army_escort_merchant_caravan", slot_quest_target_center),
    (str_store_party_name, s8, ":quest_target_center"),
   ]],
]
