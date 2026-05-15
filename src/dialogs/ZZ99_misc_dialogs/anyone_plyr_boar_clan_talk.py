DIALOGS = [
[anyone|plyr, "boar_clan_talk", [
  (neq, "$g_sod_demand_money", "$g_encountered_party"),
  ], "I warn you, it will be the other way around! Ah, why do I even bother?! Let's get to the action!", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)]],
]
