DIALOGS = [
[anyone|plyr, "sod_prisoner_train_talk", [
    (store_faction_of_party, ":train_faction", "$g_encountered_party"),
    (store_relation, ":relation", ":train_faction", "fac_player_supporters_faction"),
    (lt, ":relation", 0),
  ], "This train is a strategic target. I will see it stopped.", "close_window", [
    (call_script, "script_sod_player_accept_prisoner_train_quest_hook", "$g_encountered_party", 2),
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
