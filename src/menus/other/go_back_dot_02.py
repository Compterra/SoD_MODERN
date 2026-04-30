MENUS = [
( "tournament_bet_more", 0,
  "You can make only one high bet per tournament, before the third round. It's hard to find people accepting to risk so much money, so the higher is the bet the less it's rewarding.^^{s3}^ Warning : there will be no refund.", "none",
  [ (store_troop_gold, ":gold", "trp_player"),
    (str_clear, s3), 
    (try_begin),
    (lt, reg9, 3),
	(ge, ":gold", 10000),
	(str_store_string, s3, "@A prince from a far away merchant city was visiting the town and accepts to bet against you."),
	(else_try),
	(lt, reg9, 5),
	(ge, ":gold", 10000),
	(str_store_string, s3, "@The owner of a trading company accepts to bet against you."),
    (lt, reg9, 7),
	(ge, ":gold", 5000),
    (str_store_string, s3, "@The richest merchant of the town accepts to bet against you."),
    (else_try),
    (lt, reg9, 9),
    (str_store_string, s3, "@A rich merchant accepts to bet against you."),
    (else_try),
    (str_store_string, s3, "@You only find one petty bookmaker to accept to bet against you."),
	(try_end), 
  ],        

  [ (
        "bet_100000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 100000), (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 3), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 90) ],
        "I bet 100,000 denars for 120,000.",
        [ (troop_remove_gold, "trp_player", 100000),
          (assign, "$tournament_high_bet", 120000),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),


  (
        "bet_75000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 75000), (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 4), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 80) ],
        "I bet 75,000 denars for 90,000.",
        [ (troop_remove_gold, "trp_player", 75000),
          (assign, "$tournament_high_bet", 90000),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

    (
        "bet_50000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 50000), (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 5), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 70) ],
        "I bet 50,000 denars for 60,000.",
        [ (troop_remove_gold, "trp_player", 50000),
          (assign, "$tournament_high_bet", 60000),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

     (
        "bet_20000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 20000), (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 6), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 60) ],
        "I bet 20,000 denars for 26,000.",
        [
		  (troop_remove_gold, "trp_player", 20000),
          (assign, "$tournament_high_bet", 26000),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),
      (
        "bet_20000b", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 20000), (eq, "$g_tournament_cur_tier", 1), (lt, reg9, 5), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 60) ],
        "I bet 20,000 denars for 25,000.",
        [
		  (troop_remove_gold, "trp_player", 20000),
          (assign, "$tournament_high_bet", 25000),
		  (play_sound, "snd_money_paid"),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

	 (
        "bet_10000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 10000), (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 7), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 50) ],
        "I bet 10,000 denars for 14,000.",
        [
		  (troop_remove_gold, "trp_player", 10000),
          (assign, "$tournament_high_bet", 14000),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

      (
        "bet_10000b", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 10000), (eq, "$g_tournament_cur_tier", 1), (lt, reg9, 6), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 50) ],
        "I bet 10,000 denars for 13,000.",
        [
		  (troop_remove_gold, "trp_player", 10000),
          (assign, "$tournament_high_bet", 13000),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

	 (
        "bet_10000c", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 10000), (eq, "$g_tournament_cur_tier", 2), (lt, reg9, 6), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 50) ],
        "I bet 10,000 denars for 12,500.",
        [
		  (troop_remove_gold, "trp_player", 10000),
          (assign, "$tournament_high_bet", 12500),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

      (
        "bet_5000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 5000), (le, "$g_tournament_cur_tier", 1), (lt, reg9, 8), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 30) ],
        "I bet 5,000 denars for 7,000.",
        [
		  (troop_remove_gold, "trp_player", 5000),
          (assign, "$tournament_high_bet", 7000),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),
	 (
        "bet_5000b", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 5000), (eq, "$g_tournament_cur_tier", 2), (lt, reg9, 7), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 30) ],
        "I bet 5,000 denars for 6,500.",
        [
		  (troop_remove_gold, "trp_player", 5000),
          (assign, "$tournament_high_bet", 6500),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),
      (
        "bet_3000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 3000),  (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 9), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 20) ],
        "I bet 3,000 denars for 4,500.",
        [
		  (troop_remove_gold, "trp_player", 3000),
          (assign, "$tournament_high_bet", 4500),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),
	  (
        "bet_3000b", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 3000),  (ge, "$g_tournament_cur_tier", 1), (lt, reg9, 8), (party_slot_ge, "$g_encountered_party", slot_town_prosperity, 20) ],
        "I bet 3,000 denars for 4,200.",
        [
		  (troop_remove_gold, "trp_player", 3000),
          (assign, "$tournament_high_bet", 4200),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),
      (
        "bet_1000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 1000), (eq, "$g_tournament_cur_tier", 0), (lt, reg9, 8) ],
        "I bet 1,000 denars for 2,000.",
        [
		  (troop_remove_gold, "trp_player", 1000),
          (assign, "$tournament_high_bet", 2000),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

	    (
        "bet_1000", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 1000),  (ge, "$g_tournament_cur_tier", 1), (lt, reg9, 9) ],
        "I bet 1,000 denars for 1,700.",
        [
		  (troop_remove_gold, "trp_player", 1000),
          (assign, "$tournament_high_bet", 1700),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

	  (
        "bet_500", [(store_troop_gold, ":gold", "trp_player"), (le, ":gold", 5000), (lt, reg9, 8) ],
        "I bet 500 denars for 1000.",
        [
		  (troop_remove_gold, "trp_player", 500),
          (assign, "$tournament_high_bet", 1000),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

	  	  (
        "bet_500", [ (ge, reg9, 8) ],   # if other bets aren't available there is always someone to accept that
        "I bet 500 denars for 800.",
        [
		  (troop_remove_gold, "trp_player", 500),
          (assign, "$tournament_high_bet", 800),
		  (play_sound, "snd_money_paid"),
		  (jump_to_menu, "mnu_tournament_bet"),
        ]
      ),

      ("go_back_dot", [], "Go back.", [ (jump_to_menu, "mnu_town_tournament"), ]),

	  ]),
]
