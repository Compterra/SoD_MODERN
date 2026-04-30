DIALOGS = [
[anyone, "lord_propose_mercenary", [(call_script, "script_party_calculate_strength", "p_main_party", 0),
                                     (assign, ":offer_value", reg0),
                                     (val_add, ":offer_value", 100),
                                     (call_script, "script_round_value", ":offer_value"),
                                     (assign, ":offer_value", reg0),
                                     (assign, "$temp", ":offer_value"),
                                     (faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
                                     (neq, ":faction_leader", "$g_talk_troop"),
                                     (str_store_faction_name, s9, "$g_talk_troop_faction"),
                                     (call_script, "script_store_troop_name", s10, ":faction_leader"), ],
   "As it happens, {playername}, I promised {s10} that I would hire a company of mercenaries for an upcoming campaign.\
 What do you say to entering the service of {s9} as a mercenary captain?\
 I've no doubt that you would be up to the task.", "lord_mercenary_service", []],
]
