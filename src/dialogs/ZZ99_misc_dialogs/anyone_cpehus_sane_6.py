DIALOGS = [
[anyone, "cpehus_sane_6", [], "No matter how hard I try, the outcome is always the same... it ends in blood. Form up, soldiers ! Today we FIGHT !", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
