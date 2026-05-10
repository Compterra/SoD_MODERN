DIALOGS = [
[anyone,"gm_pretalk", [
   ],"The contract table is still open. What else do you want from the company?", "gm_talk",[(faction_get_slot, ":mercs", "fac_player_faction", slot_faction_merc_pact),
		(faction_set_slot, "fac_player_supporters_faction", slot_faction_merc_pact, ":mercs"),
		(call_script, "script_update_faction_notes", "fac_player_supporters_faction"),
		(call_script, "script_update_faction_notes", ":mercs"),
		(faction_get_slot, ":base", ":mercs", slot_guild_base),
		(party_get_slot, ":leader", ":base", slot_town_lord),
		(call_script, "script_update_troop_notes", ":leader"),
   (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),]],
]
