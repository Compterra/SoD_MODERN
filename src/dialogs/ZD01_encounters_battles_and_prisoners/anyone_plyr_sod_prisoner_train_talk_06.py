DIALOGS = [
[anyone|plyr, "sod_prisoner_train_talk", [
    (store_faction_of_party, ":train_faction", "$g_encountered_party"),
    (store_relation, ":relation", ":train_faction", "fac_player_supporters_faction"),
    (ge, ":relation", 0),
  ], "I will escort this train until the road is clear.", "close_window", [
    (call_script, "script_sod_player_accept_prisoner_train_quest_hook", "$g_encountered_party", 1),
    (assign, "$g_leave_encounter", 1),
  ]],
]
