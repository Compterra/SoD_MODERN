DIALOGS = [
[anyone, "merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_kidnapped_girl")],
  "The amount the bandits ask as ransom is {reg12} denars.\
 I will give you that money once you accept to take the quest.\
 You have 15 days to take the money to the bandits who will be waiting near the village of {s4}.\
 Those bastards said that they are going to kill the poor girl if they don't get the money by that time.\
 You will get your pay of {reg8} denars when you bring the girl safely back here.",
   "kidnapped_girl_quest_brief", [(quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (str_store_party_name, s4, ":quest_target_center"),
                                 (quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_gold_reward),
                                 (quest_get_slot, reg12, "qst_kidnapped_girl", slot_quest_target_amount),
                                 ]],
]
