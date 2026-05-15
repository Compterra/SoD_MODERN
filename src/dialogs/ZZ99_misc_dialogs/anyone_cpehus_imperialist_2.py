DIALOGS = [
[anyone, "cpehus_imperialist_2", [], "Now face the combined might of all nations of the empire !", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
