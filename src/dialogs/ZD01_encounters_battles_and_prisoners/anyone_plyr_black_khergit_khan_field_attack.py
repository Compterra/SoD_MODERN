DIALOGS = [
[anyone|plyr, "black_khergit_khan_field_talk", [], "Then I will stop the horde here.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
