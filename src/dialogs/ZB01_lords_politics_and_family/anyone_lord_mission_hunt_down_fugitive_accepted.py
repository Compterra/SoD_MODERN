DIALOGS = [
[anyone, "lord_mission_hunt_down_fugitive_accepted", [], "That's excellent, {playername}.\
 I will be grateful to you and so will the family of the man he murdered.\
 And of course the bounty on his head will be yours if you can get him.\
 Well, good hunting to you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    (assign, "$g_leave_encounter", 1),
   ]],
]
