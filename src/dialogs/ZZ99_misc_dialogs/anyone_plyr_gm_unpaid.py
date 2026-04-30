DIALOGS = [
[anyone|plyr, "gm_unpaid", [
  (store_troop_gold, ":gold", "trp_player"),
  (ge, ":gold", reg1),
  ], "Here take the money.", "gm_pretalk",[
  (troop_remove_gold, "trp_player", reg1),
  (faction_set_slot, "$g_mercs_to_be_paid", player_debt_to_faction, 0),
  (assign, "$g_sod_merc_weekly_paiment_not_paid_in_a_row", 0),
  (val_add, "$g_sod_merc_weekly_paiment_paid_in_a_row", 1),
  ]],
]
