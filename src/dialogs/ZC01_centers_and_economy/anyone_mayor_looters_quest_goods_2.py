DIALOGS = [
[anyone, "mayor_looters_quest_goods_2", [
      (quest_slot_ge, "qst_deal_with_looters", slot_quest_target_item, 1),
      (quest_get_slot, reg1, "qst_deal_with_looters", slot_quest_target_item),
  ],
   "Excellent, here is the money for your {s6}. Do you have any more goods to give me? I still need {reg1} denars' worth of goods.",
   "mayor_looters_quest_goods_response", [
      ]],
]
