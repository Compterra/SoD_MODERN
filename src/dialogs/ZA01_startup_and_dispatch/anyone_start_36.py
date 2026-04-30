DIALOGS = [
[anyone, "start", [
   (store_encountered_party, ":cur_party"),
   (party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
	(eq, "$talk_context", tc_party_encounter),
	],"What do you want?", "party_encounter_mercs", []],
]
