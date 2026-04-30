DIALOGS = [
[anyone, "merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_troublesome_bandits")],
  "I will pay you {reg8} denars if you hunt down those troublesome bandits.\
 It's dangerous work. But I believe that you are the {man/one} for it.\
 What do you say?", "troublesome_bandits_quest_brief", [(quest_get_slot, reg8, "qst_troublesome_bandits", slot_quest_gold_reward),
                                                       ]],
]
