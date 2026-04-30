DIALOGS = [
[anyone,"start", [
  (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
	(faction_get_slot, ":rep", "$g_talk_troop_faction", slot_guild_representative),
	(faction_get_slot, ":gm", "$g_talk_troop_faction", slot_guild_master),
	(this_or_next|eq, ":rep", "$g_talk_troop"),
	(eq, ":gm", "$g_talk_troop"),
  (faction_slot_eq, "fac_player_faction", slot_faction_merc_pact, "$g_talk_troop_faction"),
  (faction_get_slot, reg1, "$g_talk_troop_faction", player_debt_to_faction),
  (ge, "$g_sod_merc_weekly_paiment_not_paid_in_a_row", 3),
  (gt, reg1, 0),
  ],"{playername}! We haven't received our payment from you for over three weeks. You owe us {reg1} denars.", "gm_unpaid",[]],
]
