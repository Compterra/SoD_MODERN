DIALOGS = [
[anyone|plyr, "village_elder_recruit_decision",
    [
      (assign, ":num_volunteers", "$temp"),
      (ge, ":num_volunteers", 1),
      # MORDACHAI - BUG FIX: handle case where player has < 10 denars
      (store_troop_gold, ":gold", "trp_player"),
      (lt, ":gold", 10),
      (store_add, reg7, ":num_volunteers", -1),
    ],
   "Oh!  I don't seem to have enough money to pay for {reg7?any of them:him}!.", "village_elder_moneyless", []],
]
