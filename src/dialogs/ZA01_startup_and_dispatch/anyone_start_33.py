DIALOGS = [
[anyone,"start", [
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),(eq,"$g_talk_troop", serpent_host_guild_master),(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),],
   "Hm, another daring youngster who tries to take on the world. I can see the fire in your eyes. So, what's the reason of your visit ?", "gm_talk",[]],
]
