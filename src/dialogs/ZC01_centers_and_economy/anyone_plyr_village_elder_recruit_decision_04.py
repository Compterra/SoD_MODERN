DIALOGS = [
[anyone|plyr, "village_elder_recruit_decision",
    [
      (party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 1),
      # MORDACHAI - BUG FIX: handle case where player has < 10 denars
      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", 10),
    ],
   "No, not now.", "village_elder_pretalk", []],
]
