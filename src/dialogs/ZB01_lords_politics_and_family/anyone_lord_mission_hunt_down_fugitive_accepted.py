DIALOGS = [
[anyone, "lord_mission_hunt_down_fugitive_accepted", [], "Then justice has a rider, {playername}.\
 The dead man's family wants an ending more than speeches, and the bounty will be yours if you bring it.\
 Hunt carefully; desperate men make ugly corners.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    (assign, "$g_leave_encounter", 1),
   ]],
]
