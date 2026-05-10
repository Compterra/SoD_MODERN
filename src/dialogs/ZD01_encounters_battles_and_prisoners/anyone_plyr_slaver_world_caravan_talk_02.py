DIALOGS = [
[anyone|plyr, "slaver_world_caravan_talk", [
  ], "Open the cages. This traffic ends here.", "close_window", [
    (call_script, "script_sod_slavers_apply_player_action", sod_slaver_action_hostile, 12),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
