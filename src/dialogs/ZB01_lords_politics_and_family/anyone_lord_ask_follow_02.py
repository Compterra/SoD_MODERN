DIALOGS = [
[anyone, "lord_ask_follow", [(troop_get_slot, ":troop_renown", "$g_talk_troop", slot_troop_renown),
                              (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
                              (val_mul, ":troop_renown", 3),
                              (val_div, ":troop_renown", 4),
                              (lt, ":player_renown", ":troop_renown"),
                              ],
   "That would hardly be proper, {playername}. Why don't you follow me instead?", "close_window",
   [(assign, "$g_leave_encounter", 1)]],
]
