DIALOGS = [
[anyone|plyr, "sod_prisoner_train_talk", [
  ], "Open the wagons. I am taking these captives out of your hands.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
