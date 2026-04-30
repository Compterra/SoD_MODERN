DIALOGS = [
[anyone, "merchant_quest_brief",
   [
    (eq, "$random_merchant_quest_no", "qst_move_cattle_herd"),
    (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
    (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
    (str_store_party_name, s13, ":target_center"),
    ],
   "The cattle herd must be at {s13} within 30 days. Sooner is better, much better, but it must be absolutely no later than 30 days."\
   " If you can do that, I'd be willing to pay you {reg8} denars for your trouble. Interested?", "move_cattle_herd_quest_brief",
   []],
]
