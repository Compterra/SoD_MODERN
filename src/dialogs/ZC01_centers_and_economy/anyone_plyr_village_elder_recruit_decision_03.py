DIALOGS = [
[anyone|plyr, "village_elder_recruit_decision",
    [
      (assign, ":num_volunteers", "$temp"),
      (ge, ":num_volunteers", 1),
      # MORDACHAI - BUG FIX: handle case where player has < 10 denars
      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", 10),
      (store_add, reg7, ":num_volunteers", -1),
    ],
   "Tell {reg7?them:him} to make ready.", "village_elder_pretalk", [(call_script, "script_village_recruit_volunteers_recruit"), ]],
]
