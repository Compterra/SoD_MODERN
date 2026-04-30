DIALOGS = [
[anyone|plyr, "village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 1),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (ge, ":gold", "$temp"), ],
   "One.", "village_elder_buy_cattle_complete", [(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 1, "$temp"),
                                                       ]],
]
