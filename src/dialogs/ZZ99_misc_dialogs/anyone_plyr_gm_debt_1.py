DIALOGS = [
[anyone|plyr, "gm_debt_1", [
  (store_troop_gold, ":gold", "trp_player"),
  (ge, ":gold", reg1),
  ], "I'm a honest guy, here take the money.", "gm_pretalk",[
  (troop_remove_gold, "trp_player", reg1),
  (faction_set_slot, "$g_talk_troop_faction", player_debt_to_faction, 0),
  ]],
]
