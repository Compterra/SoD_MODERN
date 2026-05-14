DIALOGS = [
[anyone, "village_elder_train_peasants_against_bandits_mission_accept", [], "Then we still have a chance.\
 I will gather the ones with steady hands and enough anger to stand in a line.\
 Teach them how to live through a raid, and the village will give what it can without hollowing itself out.", "close_window",
   [
     (assign, "$g_leave_encounter", 1),
     (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 2),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_center", "$current_town", 3),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     ]],
]
