DIALOGS = [
[anyone, "quest_meet_spy_in_enemy_town_accepted_end", [(quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                        (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                        (val_add, ":countersign", countersigns_begin),
                                                        (str_store_string, s11, ":secret_sign"),
                                                        (str_store_string, s12, ":countersign")],
   "Good luck, {playername}. Remember, the secret phrase is '{s11}' The counterphrase is '{s12}' Bring any reports back to me, and I'll compensate you for your trouble.", "lord_pretalk",
   []],
]
