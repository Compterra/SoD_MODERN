DIALOGS = [
[anyone, "boar_clan_attack", [
      ], "Wha- you rotten son of a...! We'll teach you some manners! Come 'ere, lads! I found food for the dogs!", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)]],
]
