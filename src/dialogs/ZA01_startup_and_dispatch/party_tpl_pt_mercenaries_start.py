DIALOGS = [
[party_tpl|pt_mercenaries, "start", [
  (store_party_size, reg1, "$g_encountered_party"),
  (call_script, "script_game_get_join_cost", "$g_talk_troop"),
  (val_mul, reg1, reg0),
  (store_relation, ":reln", "fac_manhunters", "fac_player_faction"),
  (ge, ":reln", 0),
  ], "Welcome, sir. You look like somene who could hire some men. We are ready to join you even now for {reg1} denars. Are you interested?", "mercenaries_talk", []],
]
