DIALOGS = [
[anyone, "start", [
   (store_encountered_party, ":cur_party"),
   (party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
	(eq, "$talk_context", tc_party_encounter),
    (encountered_party_is_attacker),
	],"Halt!", "party_encounter_mercs_hostile_attacker", []],
]
