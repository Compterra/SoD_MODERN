DIALOGS = [
[anyone, "party_encounter_mercs_hostile_attacker", [
	(store_encountered_party, ":cur_party"),
	(party_get_slot, ":troop", ":cur_party", slot_party_boss),
	(call_script, "script_store_troop_name_link", s1, ":troop"),
	],"{s1} ordered us to bring you dead or alive. Surrender or die!", "party_encounter_mercs_hostile_attacker_2", []],
]
