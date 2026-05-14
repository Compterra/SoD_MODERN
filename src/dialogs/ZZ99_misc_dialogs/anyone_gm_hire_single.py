DIALOGS = [
[anyone,"gm_hire_single",
 [
   (eq, "$g_rep", "$g_talk_troop"),
   (gt, "$gm_party", 0),
   (store_party_size, ":available", "$gm_party"),
   (gt, ":available", 0),
   (assign, reg21, ":available"),
 ],
 "I have {reg21} contract soldiers quartered nearby. Review them yourself, and hire only the ones you want.", "gm_pretalk",
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
