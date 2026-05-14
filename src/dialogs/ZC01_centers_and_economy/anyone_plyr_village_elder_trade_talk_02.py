DIALOGS = [
[anyone|plyr, "village_elder_trade_talk", [(party_slot_eq, "$current_town", slot_village_state, 0),
                                      (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                                      (assign, ":quest_village", 0),
                                      (try_begin),
                                        (check_quest_active, "qst_deliver_cattle"),
                                        (quest_slot_eq, "qst_deliver_cattle", slot_quest_target_center, "$current_town"),
                                        (assign, ":quest_village", 1),
                                      (try_end),
                                      (eq, ":quest_village", 0),
                                      ],
   "If the herd can spare cattle, I will buy them cleanly.", "village_elder_buy_cattle", []],
]
