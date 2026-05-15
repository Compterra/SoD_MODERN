DIALOGS = [
[anyone, "cpehus_nihilistic_1", [], "Heh. I have waited for this moment, {playername}. Climactic battles bring a rare clarity: steel, dust, bodies, and the vanity of every oath men swear before they die. Come at me. Charge my formations. Test my flanks. I will answer with vigor enough to drown this field in blood.", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
