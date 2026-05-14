DIALOGS = [
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (ge, ":free_capacity", 1)],
   "Your price is more than my purse can carry today.", "tavern_mercenary_cant_lead", []],
]
