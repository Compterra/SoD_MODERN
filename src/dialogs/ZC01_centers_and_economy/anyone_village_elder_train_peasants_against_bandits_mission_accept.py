DIALOGS = [
[anyone, "village_elder_train_peasants_against_bandits_mission_accept", [], "You will? Oh, splendid!\
 We would be deeply indebted to you, {sir/madam}.\
 I'll instruct the village folk to assemble here and receive your training.\
 If you can teach us how to defend ourselves, I promise you'll receive everything we can give you in return for your efforts.", "close_window",
   [
     (assign, "$g_leave_encounter", 1),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_center", "$current_town", 3),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     ]],
]
