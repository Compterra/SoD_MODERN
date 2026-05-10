DIALOGS = [
[anyone|plyr, "town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$info_inquired", 0)], "What should an outsider know about this town?", "town_dweller_ask_info", [(assign, "$info_inquired", 1)]],
]
