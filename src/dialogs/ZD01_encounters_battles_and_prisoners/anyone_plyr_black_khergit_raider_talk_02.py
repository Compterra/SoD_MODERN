DIALOGS = [
[anyone|plyr, "black_khergit_raider_talk", [], "I will break this raid myself.", "close_window", [
    (call_script, "script_sod_black_khergits_apply_player_action", sod_black_khergit_action_defeat_raiders, 8),
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
