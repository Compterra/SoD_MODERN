DIALOGS = [
[anyone, "cpehus_capitalist_1", [], "Impudent upstart. How dare you meddle with the affairs of your superiors? Such boldness does not pass without consequence. My troops will cleanse these territories of your stain, and I will enjoy dispatching you myself.", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
