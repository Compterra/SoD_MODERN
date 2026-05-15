DIALOGS = [
[anyone|plyr, "capitalist_avoid_battle_ask", [
	], "That's outrageous ! You know what ? I'll just plant a blade into your innards.", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ]],
]
