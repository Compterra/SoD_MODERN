DIALOGS = [
[anyone,"start", [
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),(eq,"$g_talk_troop", elephant_guard_guild_master),(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),],
   "Greetings, wandering soul. The wind of fate foretold that we would met.", "gm_talk",[]],
]
