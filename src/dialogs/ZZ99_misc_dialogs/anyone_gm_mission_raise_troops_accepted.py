DIALOGS = [
[anyone, "gm_mission_raise_troops_accepted", [], "You've taken a weight off my shoulders, {playername}.\
 I'll advance you some money to help with expenses. Here, this purse should do it.\
 Thank you for your help.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 100),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 2),
    (assign, "$g_leave_encounter", 1),
  (finish_mission),
   ]],
]
