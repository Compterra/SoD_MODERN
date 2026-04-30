DIALOGS = [
[anyone, "merchant_quest_about_job_5b", [],
   "Do you expect me to believe that? You are going to pay that ransom fee back! Go and bring the money now!",
   "close_window", [(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                   (val_add, "$debt_to_merchants_guild", ":quest_target_amount"),
                   ]],
]
