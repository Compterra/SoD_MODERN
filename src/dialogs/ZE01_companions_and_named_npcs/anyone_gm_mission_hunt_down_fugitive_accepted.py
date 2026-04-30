DIALOGS = [
[anyone, "gm_mission_hunt_down_fugitive_accepted", [], "That's excellent, {playername}.\
 I will be grateful.\
 Well, good hunting to you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 3),
    (assign, "$g_leave_encounter", 1),
  (finish_mission),
   ]],
]
