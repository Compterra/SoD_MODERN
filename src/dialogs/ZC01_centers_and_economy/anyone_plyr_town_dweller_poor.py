DIALOGS = [
[anyone|plyr, "town_dweller_poor", [(store_troop_gold, ":gold", "trp_player"),
                                     (ge, ":gold", 300),
                                     ],
   "Then take these 300 denars. I hope this will help you and your family.", "town_dweller_poor_paid",
   [(troop_remove_gold, "trp_player", 300), (play_sound, "snd_money_paid"), ]],
]
