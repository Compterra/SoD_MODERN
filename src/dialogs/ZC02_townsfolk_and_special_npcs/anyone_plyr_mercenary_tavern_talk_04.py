DIALOGS = [
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (eq, ":free_capacity", 0)],
   "That sounds good. But I can't lead any more men right now.", "tavern_mercenary_cant_lead", []],
]
