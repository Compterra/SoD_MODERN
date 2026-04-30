MENUS = [
(
    "tournament_bet", 0,
    "The odds against you are {reg5} to {reg6}{reg1? You have already made regular bets of {reg1} denars on yourself, and if you win, you will earn {reg2} denars.:}{s2}^^ How much do you want to bet?",
    "none",
    [
      (assign, reg1, "$g_tournament_bet_placed"),
      (store_add, reg2, "$g_tournament_bet_win_amount", "$g_tournament_bet_placed"),
      (call_script, "script_get_win_amount_for_tournament_bet"),
      (assign, ":player_odds", reg0),
      (assign, ":min_dif", 100000),
      (assign, ":min_dif_divisor", 1),
      (assign, ":min_dif_multiplier", 1),
      (try_for_range, ":cur_multiplier", 1, 50),
        (try_for_range, ":cur_divisor", 1, 50),
          (store_mul, ":result", 100, ":cur_multiplier"),
          (val_div, ":result", ":cur_divisor"),
          (store_sub, ":difference", ":player_odds", ":result"),
          (val_abs, ":difference"),
          (lt, ":difference", ":min_dif"),
          (assign, ":min_dif", ":difference"),
          (assign, ":min_dif_divisor", ":cur_divisor"),
          (assign, ":min_dif_multiplier", ":cur_multiplier"),
        (try_end),
      (try_end),
      (assign, reg5, ":min_dif_multiplier"),
      (assign, reg6, ":min_dif_divisor"),
	  (try_begin),
	  (gt, "$tournament_high_bet", 0),
	  (assign, reg8, "$tournament_high_bet"),
		  (try_begin),
		  (gt, reg1, 0),
		  (str_store_string, s2, "@. You also made an higher bet for {reg8} more denars."),
		  (else_try),
		  (str_store_string, s2, "@. You have made an high bet for {reg8} denars."),
		  (try_end),
	  (else_try),
	  (str_store_string, s2, "@."),
	  (try_end),
	  (store_random_in_range, reg9, 0, 10),    #twan 456 determine available high bets
           (try_begin),
             (ge, reg5, 10),
             (store_sub, ":bonus", reg5, 9),  #give more chance to find bets with high odds (=when player hasn't won a lot)
             (val_sub, reg9, ":bonus"),
			(else_try),
			 (lt, reg5, 9),
			 (store_sub, ":bonus", 9, reg5),
			 (val_add, reg9, ":bonus"),
           (try_end),
    ],
    [
	    (
        "bet_more", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 500), (eq, "$tournament_high_bet", 0), (le, "$g_tournament_cur_tier", 2) ],
        "I want to bet more !",
        [
          (jump_to_menu, "mnu_tournament_bet_more"),
        ]
      ),                     #twan456end

      (
        "bet_1", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 100) ],
        "100 denars.",
        [
          (assign, "$temp", 100),
          (jump_to_menu, "mnu_tournament_bet_confirm"),
        ]
      ),
      (
        "bet_2", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 50) ],
        "50 denars.",
        [
          (assign, "$temp", 50),
          (jump_to_menu, "mnu_tournament_bet_confirm"),
        ]
      ),
      (
        "bet_3", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 20) ],
        "20 denars.",
        [
          (assign, "$temp", 20),
          (jump_to_menu, "mnu_tournament_bet_confirm"),
        ]
      ),
      (
        "bet_4", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 10) ],
        "10 denars.",
        [
          (assign, "$temp", 10),
          (jump_to_menu, "mnu_tournament_bet_confirm"),
        ]
      ),
      (
        "bet_5", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 5) ],
        "5 denars.",
        [
          (assign, "$temp", 5),
          (jump_to_menu, "mnu_tournament_bet_confirm"),
        ]
      ),

      ("go_back_dot", [], "Go back.", [ (jump_to_menu, "mnu_town_tournament"), ]),
    ]
  ),
]
