DIALOGS = [
[anyone, "lord_ask_follow", [(party_get_slot, ":dont_follow_until_time", "$g_encountered_party", slot_party_dont_follow_player_until_time),
                              (store_current_hours, ":cur_time"),
                              (lt, ":cur_time", ":dont_follow_until_time")],
   "I enjoy your company, {playername}, but there are other things I must attend to. Perhaps in a few days I can ride with you again.", "close_window",
   [(assign, "$g_leave_encounter", 1)]],
]
