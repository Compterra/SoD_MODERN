DIALOGS = [
[anyone|plyr, "deserter_barter_2", [(store_troop_gold, reg(2)), (ge, reg(2), "$deserter_tribute"), (assign, reg(5), "$deserter_tribute")],
   "All right here's your {reg5} denars.", "deserter_barter_3a", [(call_script, "script_sod_player_charge_gold", "$deserter_tribute"), (play_sound, "snd_money_paid"), ]],
]
