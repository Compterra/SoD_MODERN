DIALOGS = [
[anyone, "start",
   [
     (is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
     (gt, "$last_lost_companion", 0),
     (assign, ":companion_found_town", -1),
     (troop_get_slot, ":companion_found_town", "$last_lost_companion", slot_troop_cur_center),
     (is_between, ":companion_found_town", towns_begin, towns_end),
     (call_script, "script_store_troop_name", s10, "$last_lost_companion"),
     (str_store_party_name, s11, ":companion_found_town"),
     ],
   "Greetings, {playername}. I saw your companion {s10} at a tavern in {s11} some days ago. I thought you might like to know.", "tavern_traveler_lost_companion_thanks",
   [(assign, "$last_lost_companion", 0)]],
]
