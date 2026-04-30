DIALOGS = [
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (ge, ":free_capacity", 1)],
   "That sounds good. But I can't afford to hire any more men right now.", "tavern_mercenary_cant_lead", []],
]
