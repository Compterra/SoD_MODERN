DIALOGS = [
[anyone|plyr, "town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this village?", "town_dweller_ask_info", [(assign, "$info_inquired", 1)]],
]
