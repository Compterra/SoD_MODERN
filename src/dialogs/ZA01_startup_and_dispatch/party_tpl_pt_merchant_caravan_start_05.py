DIALOGS = [
[party_tpl|pt_merchant_caravan, "start", [
   (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
   (neq, "$g_encountered_party", ":quest_target_party"),
   (eq, "$talk_context", tc_party_encounter),
  ],
   "Mind the mules, friend. We carry stamped goods, counted coin, and enough road rumors to make a tax collector sweat. Speak your business plainly.", "merchant_caravan_world_talk", []],
]
