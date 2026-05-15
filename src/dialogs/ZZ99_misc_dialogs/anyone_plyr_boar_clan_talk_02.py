DIALOGS = [
[anyone|plyr, "boar_clan_talk", [
  (eq, "$g_sod_demand_money", "$g_encountered_party"),
  ], "Your honor is just robbery dressed in clan colors. I'll break this toll myself.", "close_window", [
  (assign, "$g_sod_boar_toll_amount", 0),
  (call_script, "script_sod_boar_clan_apply_player_action", sod_boar_action_defy_toll, 10),
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)]],
]
