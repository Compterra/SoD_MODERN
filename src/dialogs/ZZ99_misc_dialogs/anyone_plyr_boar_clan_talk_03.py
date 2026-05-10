DIALOGS = [
[anyone|plyr, "boar_clan_talk", [
  (eq, "$g_sod_demand_money", "$g_encountered_party"),
  (assign, reg5, "$g_sod_boar_toll_amount"),
  (val_clamp, reg5, 1, 1001),
  (assign, "$g_sod_boar_toll_amount", reg5),
  (store_troop_gold, ":plyr_gold", "trp_player"),
  (ge, ":plyr_gold", reg5),
  ], "Fine. Take your road tribute.", "boar_clan_barter", [
  (assign, reg5, "$g_sod_boar_toll_amount"),
  (val_clamp, reg5, 1, 1001),
  (assign, "$g_sod_boar_toll_amount", reg5),
  (call_script, "script_sod_player_charge_gold", reg5),
  (call_script, "script_sod_boar_clan_apply_player_action", sod_boar_action_pay_toll, reg5),
  (play_sound, "snd_money_paid"),
  ]],
]
