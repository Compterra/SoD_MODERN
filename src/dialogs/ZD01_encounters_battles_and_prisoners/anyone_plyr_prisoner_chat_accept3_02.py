DIALOGS = [
[anyone|plyr, "prisoner_chat_accept3", [(troops_can_join, 1)], "Excellent. Report to the quartermaster for provisions and equiment.  There is hard fighting ahead.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_prisoner_agreed, 0),
    (remove_troops_from_prisoners, "$g_talk_troop", 1),
    (party_add_members, "p_main_party", "$g_talk_troop", 1),
    (store_random_in_range, ":roll", 0, 100),
    (store_character_level, ":chance", "$g_talk_troop"),
    (try_begin),
      (lt, ":roll", ":chance"),
      (call_script, "script_change_troop_renown", "trp_player", 1),
    (try_end),
   ]],
]
