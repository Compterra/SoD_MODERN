DIALOGS = [
[anyone|plyr, "slaver_world_caravan_talk", [
  ], "Open the cages. This traffic ends here.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
