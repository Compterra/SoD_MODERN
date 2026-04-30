DIALOGS = [
[anyone|plyr, "merchant_quest_about_job_2", [(store_partner_quest, ":partner_quest"),
                                              (eq, ":partner_quest", "qst_kidnapped_girl"),
                                              (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
                                              (neg|main_party_has_troop, "trp_kidnapped_girl")],
   "Unfortunately I lost the girl on the way here...", "lost_kidnapped_girl", []],
]
