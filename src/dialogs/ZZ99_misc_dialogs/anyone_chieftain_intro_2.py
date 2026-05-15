DIALOGS = [
[anyone, "chieftain_intro_2", [],
   "Ha Ha Ha! I don't have time for this. Kill {him/her}!", "close_window", [
  (assign, "$g_e_g_after_battle", 1),
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)]],
]
