DIALOGS = [
[anyone,"start", [
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),(eq,"$g_talk_troop", slavers_guild_master),(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),],
   "What do you want, nobling ? I hope it's important, cos' my time is precious.", "gm_talk",[]],
]
