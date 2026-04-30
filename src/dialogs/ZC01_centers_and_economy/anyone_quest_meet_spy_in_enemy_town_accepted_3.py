DIALOGS = [
[anyone, "quest_meet_spy_in_enemy_town_accepted_3", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                      (str_store_party_name_link, s13, ":quest_target_center"),
                                                      (troop_get_type, reg7, "$spy_quest_troop"),
                                                      (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                      (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                      (val_add, ":countersign", countersigns_begin),
                                                      (str_store_string, s11, ":secret_sign"),
                                                      (str_store_string, s12, ":countersign"), ],
   "Once you get to {s13} you must talk to the locals, the spy will be one of them. If you think you've found the spy, say the phrase '{s11}' The spy will respond with the phrase '{s12}' Thus you will know the other, and {reg7?she:he} will give you any information {reg7?she:he}'s gathered in my service.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
]
