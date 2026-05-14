DIALOGS = [
[anyone, "party_encounter_mercs_hostile_attacker", [
	(store_encountered_party, ":cur_party"),
	(party_get_slot, ":troop", ":cur_party", slot_party_boss),
	(try_begin),
		(is_between, ":troop", 0, "trp_last_troop"),
		(call_script, "script_store_troop_name_link", s1, ":troop"),
	(else_try),
		(str_store_string, s1, "@Our paymaster"),
	(try_end),
	],"{s1} ordered us to bring you dead or alive. Surrender or die!", "party_encounter_mercs_hostile_attacker_2", []],
]
