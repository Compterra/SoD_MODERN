DIALOGS = [
[anyone, "lord_mission_accepted_kill_local_merchant", [], "Good. This must look like misfortune, not command.\
 Wait for my word, {playername}; I will send the hour and place when the merchant is most exposed.\
 Do this quietly, and the reward will be generous enough to buy silence twice over.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (assign, "$g_leave_town", 1),
    (assign, "$qst_kill_local_merchant_center", "$current_town"),
    (rest_for_hours, 10, 4, 0),
    (finish_mission),
    ]],
]
