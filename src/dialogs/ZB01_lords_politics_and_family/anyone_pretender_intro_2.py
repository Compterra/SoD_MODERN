DIALOGS = [
[anyone , "pretender_intro_2", [(troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                                 (val_sub, ":rebellion_string", "fac_kingdom_1"),
                                 (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_intro"),
                                 (str_store_string, 48, ":rebellion_string"), ],
   "{s48}", "pretender_intro_3", []],
]
