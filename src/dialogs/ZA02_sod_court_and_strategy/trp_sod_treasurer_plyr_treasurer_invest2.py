DIALOGS = [
[trp_sod_treasurer|plyr, "treasurer_invest2", [
    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", 500),
  ], "I will accept the risk. Invest 500 gold", "treasurer_ok", [
    (assign, "$g_sod_invested", 1),
    (store_current_day, ":cur_day"),
    (assign, "$g_sod_invested_day", ":cur_day"),
    (val_add, "$g_sod_invested_day", 5),
    (assign, "$g_sod_invested_gold", 500),
    (call_script, "script_sod_player_charge_gold", 500),
    (play_sound, "snd_money_paid"),
  ]],
]
