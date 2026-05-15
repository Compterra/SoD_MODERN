DIALOGS = [
[anyone, "cpehus_crusader_2", [], "Rejoice, children of Marsus ! This day we exterminate the hateful descendants of the {s31} ! Observe how Marsus will reward our offerings with exulting victory !", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
