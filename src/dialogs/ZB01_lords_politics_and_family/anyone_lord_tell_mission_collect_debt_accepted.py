DIALOGS = [
[anyone, "lord_tell_mission_collect_debt_accepted", [], "You made me very happy by accepting this {playername}. Please, talk to {s3} and don't leave him without my money.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
    (assign, "$g_leave_encounter", 1),
   ]],
]
