DIALOGS = [
[anyone|plyr, "bandit_barter_2", [[store_troop_gold, reg(2)], [ge, reg(2), "$bandit_tribute"], [assign, reg(5), "$bandit_tribute"]],
   "Very well, take it.", "bandit_barter_3a", [(call_script, "script_sod_player_charge_gold", "$bandit_tribute"), (play_sound, "snd_money_paid"), ]],
]
