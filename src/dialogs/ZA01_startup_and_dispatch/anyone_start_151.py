DIALOGS = [
[anyone, "start",
    [
      (store_faction_of_party, ":cur_faction", "$g_encountered_party"),
      (eq, ":cur_faction", "fac_player_faction"),
    ],
    "Yes?", "mate_chat_talk", [(assign, "$g_leave_encounter", 1)]],
]
