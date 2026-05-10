DIALOGS = [
[trp_sod_treasurer|plyr, "treasurer_invest2", [
    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", 0),
  ], "Risk?  Risk means nothing. Shut your mouth and invest everything!", "treasurer_ok", [
    (assign, "$g_sod_invested", 1),
    (store_current_day, ":cur_day"),
    (assign, "$g_sod_invested_day", ":cur_day"),
    (val_add, "$g_sod_invested_day", 5),
    (store_troop_gold, ":gold", "trp_player"),
    (assign, "$g_sod_invested_gold", ":gold"),
    (call_script, "script_sod_player_charge_gold", ":gold"),
    (play_sound, "snd_money_paid"),
  ]],
]
