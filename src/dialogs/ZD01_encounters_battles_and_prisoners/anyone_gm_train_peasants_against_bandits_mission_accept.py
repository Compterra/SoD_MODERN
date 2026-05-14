DIALOGS = [
[anyone, "gm_train_peasants_against_bandits_mission_accept", [], "Then we will make the drill yard earn its dust.\
 My fighters will assemble, and every lazy habit they brought with them can die there.", "close_window",
   [
  (finish_mission),
     (assign, "$g_leave_encounter", 1),
     (assign, "$elephant_guard_training_groups_defeted", 0),
     (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 3),
     (setup_quest_text, "qst_elephant_guard_train_peasants_against_bandits"),
     (str_store_string, s2, "@Elephant Guard guild master asked you to train the Elephant Guard fighters."),
     (call_script, "script_start_quest", "qst_elephant_guard_train_peasants_against_bandits", "$g_talk_troop"),
     ]],
]
