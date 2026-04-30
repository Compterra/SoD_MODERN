DIALOGS = [
[anyone, "gm_hire", [
   (try_begin),
	(this_or_next|eq, "$g_talk_troop", slavers_guild_master),
	(eq, "$g_talk_troop", slavers_rep),
	(assign, "$gm_party", slavers_sod_mercs),
	(assign, "$gm_party_elite", slavers_mercs_noble),
   (else_try),
    (faction_get_slot,"$gm_party", "$g_talk_troop_faction", slot_faction_sod_mercs),
    (faction_get_slot,"$gm_party_elite", "$g_talk_troop_faction", slot_faction_mercs_noble),
   (try_end),
   (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),
   (call_script, "script_merc_describe_guild_offer", "$g_talk_troop_faction"),
   ],"You want to hire single warriors, or a party of soldiers?^^Our guild is known for {s50}. Expect {s51}. We usually charge {s52}, and your standing currently earns {s53}.", "gm_hire1", []],
]
