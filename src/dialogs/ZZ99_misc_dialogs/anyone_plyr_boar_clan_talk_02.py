DIALOGS = [
[anyone|plyr, "boar_clan_talk", [
  (eq, "$g_sod_demand_money", "$g_encountered_party"),
  ], "Your honor is just robbery dressed in clan colors. I'll break this toll myself.", "close_window", [
  (assign, "$g_sod_boar_toll_amount", 0),
  (call_script, "script_sod_boar_clan_apply_player_action", sod_boar_action_defy_toll, 10),
  (encounter_attack)]],
]
