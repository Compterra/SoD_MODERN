DIALOGS = [
[anyone, "tavernkeeper_buy_drinks_end",
   [], "Don't worry {sir/madam}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   [
       (call_script, "script_sod_player_charge_gold", "$temp"),
       (try_begin),
         (eq, reg1, 1),
         (play_sound, "snd_money_paid"),
         (call_script, "script_change_player_relation_with_center", "$current_town", 1),
         (store_current_hours, ":cur_hours"),
         (assign, "$buy_drinks_last_time", ":cur_hours"),
       (try_end),
       ]],
]
