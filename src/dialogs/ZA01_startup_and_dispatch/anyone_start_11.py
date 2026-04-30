DIALOGS = [
[anyone, "start", [(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
					(faction_get_slot, ":rep", "$g_talk_troop_faction", slot_guild_representative),
					(eq, ":rep", "$g_talk_troop"),
					(assign, "$g_rep", "$g_talk_troop"),
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),
  ], "Yes?", "gm_talk",[]],
]
