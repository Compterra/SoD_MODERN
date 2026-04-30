DIALOGS = [
[anyone|plyr, "party_encounter_mercs_hostile_attacker_2", [
  ],"We will fight you to the end!", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  ]],
]
