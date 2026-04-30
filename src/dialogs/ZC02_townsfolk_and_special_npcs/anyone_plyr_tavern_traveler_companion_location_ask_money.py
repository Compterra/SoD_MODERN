DIALOGS = [
[anyone|plyr, "tavern_traveler_companion_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 30),
     ], "All right. Here is 30 denars.", "tavern_traveler_companion_location_tell",
   [
     (troop_remove_gold, "trp_player", 30),
     (play_sound, "snd_money_paid"),
     ]],
]
