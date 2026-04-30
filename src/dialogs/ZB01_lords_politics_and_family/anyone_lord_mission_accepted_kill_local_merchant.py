DIALOGS = [
[anyone, "lord_mission_accepted_kill_local_merchant", [], "Very good. I trust in your skill and discretion,\
 {playername}. Do not disappoint me.\
 Go now and wait for my word, I'll send you a message telling when and where you can catch the merchant.\
 Dispose of him for me and I shall reward you generously.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (assign, "$g_leave_town", 1),
    (assign, "$qst_kill_local_merchant_center", "$current_town"),
    (rest_for_hours, 10, 4, 0),
    (finish_mission),
    ]],
]
