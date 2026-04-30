DIALOGS = [
[anyone,"start", [
  (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
	(faction_get_slot, ":rep", "$g_talk_troop_faction", slot_guild_representative),
	(faction_get_slot, ":gm", "$g_talk_troop_faction", slot_guild_master),
	(this_or_next|eq, ":rep", "$g_talk_troop"),
	(eq, ":gm", "$g_talk_troop"),
  (neg|faction_slot_eq, "fac_player_faction", slot_faction_merc_pact, "$g_talk_troop_faction"),
  (faction_get_slot, reg1, "$g_talk_troop_faction", player_debt_to_faction),
  (gt, reg1, 0),
  ],"{playername}! Give us our money back! You still owe us {reg1} denars.", "gm_debt_1",[]],
]
