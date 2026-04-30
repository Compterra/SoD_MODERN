DIALOGS = [
[anyone|plyr, "town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation", [(assign, "$welfare_inquired", 1)]],
]
