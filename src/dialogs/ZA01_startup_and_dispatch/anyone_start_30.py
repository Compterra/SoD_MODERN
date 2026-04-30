DIALOGS = [
[anyone,"start", [
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),(eq,"$g_talk_troop", conquistadors_guild_master),(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),],
   "Welcome, fellow fighter.  What brings you to our humble fort?", "gm_talk",[]],
]
