DIALOGS = [
[anyone|plyr, "boar_clan_talk", [
  (eq, "$g_sod_demand_money", "$g_encountered_party"),
  (store_troop_gold, ":plyr_gold", "trp_player"),
  (gt, ":plyr_gold", reg5),
  ], "Fine, I'll pay.", "boar_clan_barter", [
  (troop_remove_gold, "trp_player", reg5),
  (play_sound, "snd_money_paid"),
  ]],
]
