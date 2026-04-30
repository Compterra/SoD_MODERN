DIALOGS = [
[anyone|plyr, "bandit_barter_2", [[store_troop_gold, reg(2)], [ge, reg(2), "$bandit_tribute"], [assign, reg(5), "$bandit_tribute"]],
   "Very well, take it.", "bandit_barter_3a", [(troop_remove_gold, "trp_player", "$bandit_tribute"), (play_sound, "snd_money_paid"), ]],
]
