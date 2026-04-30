DIALOGS = [
[anyone, "merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_move_cattle_herd"),
                                       (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
                                       (str_store_party_name, s13, ":target_center"), ],
   "One of the merchants here is looking for herdsmen to take his cattle to the market at {s13}.", "merchant_quest_brief",
   []],
]
