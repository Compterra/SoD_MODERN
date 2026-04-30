MENUS = [
(
    "town_tournament_won", mnf_disable_all_keys,
    "You have won the tournament of {s3}! You are filled with pride as the crowd cheers your name. In addition to honour, fame and glory, you earn a prize of {reg9} denars. {s8}",
    "none",
    [
      (str_store_party_name, s3, "$current_town"),
      (call_script, "script_change_troop_renown", "trp_player", 20),
      (call_script, "script_change_player_relation_with_center", "$current_town", 1),
      (assign, reg9, 200),
      (add_xp_to_troop, 250, "trp_player"),
      (troop_add_gold, "trp_player", reg9),
      (str_clear, s8),
      (store_add, ":total_win", "$g_tournament_bet_placed", "$g_tournament_bet_win_amount"),
	  (val_add, ":total_win", "$tournament_high_bet"),  #twan456
      (try_begin),
        (this_or_next|gt, "$g_tournament_bet_win_amount", 0),
		(gt, "$tournament_high_bet", 0),
        (assign, reg8, ":total_win"),
        (str_store_string, s8, "@Moreover, you earn {reg8} denars from the clever bets you placed on yourself..."),
      (try_end),
	  (assign, "$tournament_high_bet", 0),
      (troop_add_gold, "trp_player", ":total_win"),
      (assign, ":player_odds_sub", 0),
      (store_div, ":player_odds_sub", "$g_tournament_bet_win_amount", 5),
      (party_get_slot, ":player_odds", "$current_town", slot_town_player_odds),
      (val_sub, ":player_odds", ":player_odds_sub"),
      (val_max, ":player_odds", 250),
      (party_set_slot, "$current_town", slot_town_player_odds, ":player_odds"),
      (call_script, "script_play_victorious_sound"),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_town")]),
    ]
  ),
]
