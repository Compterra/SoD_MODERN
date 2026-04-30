DIALOGS = [
[anyone,"start", [
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),(eq,"$g_talk_troop", "trp_boar_clan_guild_master"),(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),],
   "Welcome to our forward camp.  We do not get many visitors out here so I apologize for the manners of my men.", "gm_talk",[]],
]
