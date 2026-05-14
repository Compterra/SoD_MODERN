DIALOGS = [
[anyone,"gm_hire_single",
 [
   (gt, "$gm_party", 0),
   (store_party_size, ":available", "$gm_party"),
   (gt, ":available", 0),
   (assign, reg21, ":available"),
 ],
 "I can put {reg21} ordinary blades before you. Pay their price, and they are yours to command.", "gm_pretalk",
 [
   (set_mercenary_source_party,"$gm_party"),
   (store_troop_gold, ":before", "trp_player"),
   (change_screen_buy_mercenaries),
   (store_troop_gold, ":after", "trp_player"),
   (store_sub, reg0, ":before", ":after"),
   (val_max, reg0, 0),
   (val_add, "$g_sod_weekly_troops_hired", reg0),
   (val_clamp, "$g_sod_weekly_troops_hired", 0, 2000001),
 ]],
]
