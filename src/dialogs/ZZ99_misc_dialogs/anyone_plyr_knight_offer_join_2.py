DIALOGS = [
[anyone|plyr, "knight_offer_join_2", [(gt, reg6, 0), (store_troop_gold, ":gold", "trp_player"), (gt, ":gold", reg6)],
   "Here, take it, all {reg6} denars you need. 'Tis only money.", "knight_offer_join_accept", [(troop_remove_gold, "trp_player", reg6), (play_sound, "snd_money_paid"), ]],
]
