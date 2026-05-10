DIALOGS = [
[anyone|plyr, "black_army_world_patrol_talk", [
  ], "Then you can be broken like any other armed band.", "close_window", [
    (call_script, "script_sod_black_army_apply_player_action", sod_black_army_action_attack_patrol, 25),
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
