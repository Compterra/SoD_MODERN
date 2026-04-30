DIALOGS = [
[anyone|plyr, "tavern_traveler_answer", [(store_troop_gold, ":cur_gold", "trp_player"),
                                            (ge, ":cur_gold", 100)],
   "Here's 100 denars. Tell me what you know.", "tavern_traveler_continue", [(party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                                           (call_script, "script_update_faction_traveler_notes", ":info_faction"),
                                           (change_screen_notes, 2, ":info_faction"),
                                           ]],
]
