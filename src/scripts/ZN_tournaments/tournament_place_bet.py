SCRIPTS = [
("tournament_place_bet",
        [
          (store_script_param, ":bet_amount", 1),
          (call_script, "script_get_win_amount_for_tournament_bet"),
          (assign, ":win_amount", reg0),
          (val_mul, ":win_amount", ":bet_amount"),
          (val_div, ":win_amount", 100),
          (val_sub, ":win_amount", ":bet_amount"),
          (call_script, "script_sod_player_charge_gold", ":bet_amount"),
          (try_begin),
          (eq, reg1, 1),
          (val_add, "$g_tournament_bet_placed", ":bet_amount"),
          (val_add, "$g_tournament_bet_win_amount", ":win_amount"),
          (play_sound, "snd_money_paid"),
          (assign, "$g_tournament_last_bet_tier", "$g_tournament_cur_tier"),
          (try_end),
      ]),
]
