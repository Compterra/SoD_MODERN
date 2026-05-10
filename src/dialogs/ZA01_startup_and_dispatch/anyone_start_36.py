DIALOGS = [
[anyone, "start", [
   (store_encountered_party, ":cur_party"),
   (party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
	(eq, "$talk_context", tc_party_encounter),
	],"You have found sellswords under arms, not villagers with empty hands. State your offer, warning, or challenge.", "party_encounter_mercs", []],
]
