DIALOGS = [
[anyone, "threaten_1", [], "We will fight you first", "end", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)]],
]
