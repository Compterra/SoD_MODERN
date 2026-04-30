DIALOGS = [
[anyone|plyr , "pretender_intro_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                      (str_store_faction_name, s12, ":original_faction"),
                                      (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                      (call_script, "script_store_troop_name", s11, ":original_ruler"), ],
   "I thought {s12} was ruled by {s11}?", "pretender_rebellion_cause_1", [(troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1), ]],
]
