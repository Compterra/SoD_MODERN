DIALOGS = [
[anyone, "tavernkeeper_buy_drinks_troops_end",
   [], "Don't worry {sir/madam}. Your men will enjoy their pints.", "tavernkeeper_pretalk",
   [
      (troop_remove_gold, "trp_player", "$temp"),
      (play_sound, "snd_money_paid"),
      (call_script, "script_change_player_party_morale", 20),
      (store_current_hours, ":cur_hours"),
      (assign, "$buy_drinks_last_time", ":cur_hours"),
      (rest_for_hours, 2, 5, 0)
   ]],
]
