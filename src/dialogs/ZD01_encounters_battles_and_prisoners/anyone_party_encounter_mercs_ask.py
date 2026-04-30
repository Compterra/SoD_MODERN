DIALOGS = [
[anyone, "party_encounter_mercs_ask", [
	(store_encountered_party, ":cur_party"),
	(party_get_slot, ":troop", ":cur_party", slot_party_boss),
	(call_script, "script_store_troop_name", s1, ":troop"),
	(str_store_faction_name, s2, "$g_encountered_party_faction"),
	(store_troop_faction, ":troop_fac", ":troop"),
	(str_store_faction_name, s3, ":troop_fac"),
	],"We are mercenaries from {s2} hired by {s1} of {s3}.", "party_encounter_mercs", []],
]
