DIALOGS = [
[anyone|plyr, "gm_talk", [
	(neq, "$g_talk_troop", slavers_guild_master),
    (neq,"$g_talk_troop", "trp_boar_clan_guild_master"),
	(faction_get_slot, ":mercenaries", "fac_player_faction", slot_faction_merc_pact),
	(neq, ":mercenaries", "$g_talk_troop_faction"),
	(eq, "$g_sod_king", 1),
	(neq, "$g_rep", "$g_talk_troop"),
	], "Let us speak of a formal pact between my realm and your guild.", "gm_pact1",[]],
]
