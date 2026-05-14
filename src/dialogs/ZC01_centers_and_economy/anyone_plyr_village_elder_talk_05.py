DIALOGS = [
[anyone|plyr, "village_elder_talk", [(party_slot_eq, "$current_town", slot_village_state, 0),
                                      (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1), ],
   "I need food and stores, and I will pay in coin rather than promises.", "village_elder_trade_begin", []],
]
