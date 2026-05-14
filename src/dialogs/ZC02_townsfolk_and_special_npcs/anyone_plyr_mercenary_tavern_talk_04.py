DIALOGS = [
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (eq, ":free_capacity", 0)],
   "I have no room in the company for more hungry swords.", "tavern_mercenary_cant_lead", []],
]
