DIALOGS = [
[anyone, "tavernkeeper_buy_drinks_end",
   [], "Don't worry {sir/madam}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   [
       (troop_remove_gold, "trp_player", "$temp"),
       (play_sound, "snd_money_paid"),
       (call_script, "script_change_player_relation_with_center", "$current_town", 1),
       (store_current_hours, ":cur_hours"),
       (assign, "$buy_drinks_last_time", ":cur_hours"),
       ]],
]
